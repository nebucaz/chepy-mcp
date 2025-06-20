import asyncio
from fastmcp import FastMCP
from typing import Any, Dict, List, Optional, Literal, cast, Mapping
from pydantic import BaseModel, Field
from chepy import Chepy
import base64
import string
import inspect
import json


class ChepyOperation(BaseModel):
    function: str = Field(..., description="Name of the Chepy function")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the function")


class ChepyRecipeModel(BaseModel):
    input: str = Field(..., description="Input string to process")
    recipe: List[ChepyOperation] = Field(..., description="List of Chepy operations in recipe format")


class BakeOutputModel(BaseModel):
    type: Literal["text", "binary"]
    data: str  # plain text or base64-encoded binary


def is_printable_text(b: bytes) -> bool:
    try:
        s = b.decode("utf-8")
        return all(c in string.printable or c.isspace() for c in s)
    except UnicodeDecodeError:
        return False


mcp = FastMCP(name="MCP Server for python chepy")


@mcp.tool()
def bake(input_data: ChepyRecipeModel) -> BakeOutputModel:
    """
    Applies a pipeline of Chepy operations to the input string.
    Returns a BakeOutputModel with type and data fields.
    """
    # Convert Pydantic models to dicts for Chepy compatibility
    recipe_dicts = [op.model_dump() for op in input_data.recipe]
    recipe_dicts = cast(List[Mapping[str, Any]], recipe_dicts)
    c = Chepy(input_data.input).run_recipe(recipe_dicts)
    result = c.out
    if isinstance(result, bytes):
        if is_printable_text(result):
            return BakeOutputModel(type="text", data=result.decode("utf-8"))
        else:
            return BakeOutputModel(
                type="binary", data=base64.b64encode(result).decode("utf-8")
            )
    else:
        return BakeOutputModel(type="text", data=str(result))


@mcp.resource("resource://chepy_operations")
def get_chepy_operations() -> dict:
    """Returns a dictionary of available Chepy operations, their parameters, and descriptions."""
    hidden = {
        "copy", "web", "read_file", "load_file", "http_request", "load_dir", "o", "out",
        "change_state", "save_buffer", "copy_state", "create_state", "delete_buffer", "delete_state",
        "get_state", "set_state", "save_recipe", "load_recipe", "run_recipe", "print", "debug", "reset",
        "register", "set_register", "get_register", "pastebin_to_raw", "github_to_raw", "load_command",
        "run_script", "for_each", "fork", "callback", "switch_state", "eval_state",
        # state/buffer related
        "state", "buffer", "state_index", "state_count", "state_list", "state_dict", "state_keys",
        "state_values", "state_items", "state_clear", "state_pop", "state_update", "state_copy",
        "state_fromkeys", "state_get", "state_setdefault", "state_popitem", "state_viewitems",
        "state_viewkeys", "state_viewvalues"
    }
    ops = {}
    for name in dir(Chepy):
        if not name.startswith("_") and name not in hidden:
            func = getattr(Chepy, name)
            if callable(func):
                sig = str(inspect.signature(func))
                # Remove 'self' from signature
                if sig.startswith("(self, "):
                    sig = "(" + sig[len("(self, "):]  # remove 'self, '
                elif sig.startswith("(self)"):
                    sig = "()"
                # Remove return type annotation
                if "->" in sig:
                    sig = sig.split("->")[0].strip()
                # Get docstring (first line only)
                doc = inspect.getdoc(func)
                if doc:
                    doc = doc.split("\n")[0]
                else:
                    doc = ""
                ops[name] = {"signature": sig, "description": doc}
    return ops


def save_chepy_operations_to_json(filename: str = "chepy_operations.json"):
    ops = get_chepy_operations()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(ops, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    save_chepy_operations_to_json()
    mcp.run()
