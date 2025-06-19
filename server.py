# https://github.com/modelcontextprotocol/python-sdk
# https://gofastmcp.com/getting-started/welcome
# run: 
# install: mcp install server.py
# dev: mcp dev server.py
#
# https://github.com/securisec/chepy


from mcp.server.fastmcp import FastMCP

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


if __name__ == "__main__":
    mcp.run()