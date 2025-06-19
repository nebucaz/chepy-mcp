# https://github.com/modelcontextprotocol/python-sdk
# https://gofastmcp.com/getting-started/welcome
# run:
# install: mcp install server.py
# dev: mcp dev server.py
#
# https://github.com/securisec/chepy
# https://chepy.readthedocs.io/en/latest/
#

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

import asyncio
from fastmcp import FastMCP
from servers.data_format import data_format_mcp

# from chepy import Chepy
# from typing import Annotated
# from pydantic import Field

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


# Import subserver
async def setup_server():
    await mcp.import_server(
        server=data_format_mcp, prefix=None
    )  # import without prefix


if __name__ == "__main__":
    asyncio.run(setup_server())
    mcp.run()
