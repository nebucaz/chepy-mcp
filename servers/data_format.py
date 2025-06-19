from fastmcp import FastMCP
from chepy import Chepy
from typing import Annotated
from pydantic import Field

data_format_mcp = FastMCP(name="DataFormat")

@data_format_mcp.tool()
def to_base64(input: Annotated[str, Field(description="String to be encoded")]) -> str:
    """
        Encode the input string to base64
    """
    # to_base64() returns binary string b'' - it will be encoded by fastmcp using str()
    # and wrapped with quotes (""). Therefore decoding/convert to string, before returning
    return Chepy(input).to_base64().out.decode('utf-8')


@data_format_mcp.tool()
def from_base64(input: Annotated[str, Field(description="String to be decoded")]) -> str:
    """
        Decode base64 encoded string
    """
    return Chepy(input).from_base64().out.decode('utf-8')