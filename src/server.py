import asyncio
from fastmcp import FastMCP
from typing import Any, Dict, List, Optional, Literal, cast, Mapping
from pydantic import BaseModel, Field
from chepy import Chepy
import base64
import string
import inspect


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
    """Returns a dictionary of available Chepy operations and their parameters."""

    hidden = [
        "copy",
        "web",
        "read_file",
        "load_file",
        "http_request",
        "load_dir",
        "o",
        "out",
        "change_state",
        "save_buffer",
    ]
    ops = {}
    for name in dir(Chepy):
        if not name.startswith("_") and name not in hidden:
            func = getattr(Chepy, name)
            if callable(func):
                sig = str(inspect.signature(func))
                ops[name] = sig  # remove self
    return ops


if __name__ == "__main__":
    mcp.run()
