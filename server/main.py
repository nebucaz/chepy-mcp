# https://github.com/modelcontextprotocol/python-sdk
# https://gofastmcp.com/getting-started/welcome
# run:
# install: mcp install server.py
# dev: mcp dev server.py
#
# https://github.com/securisec/chepy
# https://chepy.readthedocs.io/en/latest/
#

import asyncio
from fastmcp import FastMCP
from servers.data_format_mcp import data_format_mcp
from typing import Annotated, Any, Dict, List, Optional
from pydantic import BaseModel, Field
from chepy import Chepy


class PipelineModel(BaseModel):
    """
    Input model for a chain of operations that are to be applied to the input
    Valid operations are: from_base64, to_base64
    """


class OperationModel(BaseModel):
    op: str = Field(
        ..., description="Name of the Chepy operation (e.g., 'rot13', 'base64_encode')"
    )
    params: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Parameters for the operation"
    )


class BakePipelineModel(BaseModel):
    input: str = Field(..., description="Input string to process")
    pipeline: List[OperationModel] = Field(
        ..., description="List of operations to apply in order"
    )


# Create a server instance with a descriptive name
mcp = FastMCP(name="MCP Server for python chepy")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b


@mcp.resource("resource://config")
def get_config() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}


# resource template
@mcp.tool()
def personalized_greeting(name: str) -> str:
    """
    Generates a personalized greeting for the given name.
    """
    return f"Hello, {name}!"


@mcp.tool()
def pipeline(input_data: PipelineModel) -> str:
    """
    Takes an input and a list of operations that are applied to the input string
    in the sequence they qre defined.
    """


@mcp.tool()
def bake(input_data: BakePipelineModel) -> str:
    """
    Applies a pipeline of Chepy operations to the input string.
    """
    c = Chepy(input_data.input)
    for step in input_data.pipeline:
        func = getattr(c, step.op)
        params = step.params or {}
        c = func(**params)
    return c.out


# Import subserver
async def setup_server():
    await mcp.import_server(server=data_format_mcp, prefix="data_format")
    # await mcp.import_server(data_format_mcp)
    # server=data_format_mcp, prefix=None


if __name__ == "__main__":
    asyncio.run(setup_server())
    mcp.run()


"""
from typing import Annotated
from pydantic import Field

def process_image(
    image_url: Annotated[str, Field(description="URL of the image to process")],
    resize: Annotated[bool, Field(description="Whether to resize the image")] = False,
    width: Annotated[int, Field(description="Target width in pixels", ge=1, le=2000)] = 800,
    format: Annotated[
        Literal["jpeg", "png", "webp"],
        Field(description="Output image format")
    ] = "jpeg"
) -> dict:

# Asynchronous tool (ideal for I/O-bound operations)
@mcp.tool
async def fetch_weather(city: str) -> dict:

@mcp.tool(
    name="find_products",           # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.", # Custom description
    tags={"catalog", "search"},      # Optional tags for organization/filtering
)
"""
