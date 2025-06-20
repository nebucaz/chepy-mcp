from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

from lib.data_format import _to_base64, _from_base64

data_format_mcp = FastMCP(name="DataFormat")


@data_format_mcp.tool()
def to_base64(input: Annotated[str, Field(description="String to be encoded")]) -> str:
    """
    Encode the input string to base64
    """
    return _to_base64(input)


@data_format_mcp.tool()
def from_base64(
    input: Annotated[str, Field(description="String to be decoded")],
) -> str:
    """
    Decode base64 encoded string
    """
    return _from_base64(input)
