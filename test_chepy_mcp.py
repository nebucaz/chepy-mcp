#import pytest
import unittest
from server import mcp
from fastmcp import Client

"""
@pytest.fixture
def mcp_server():
    return mcp

async def test_tool_functionality(mcp_server):
    # Pass the server directly to the Client constructor
    async with Client(mcp_server) as client:
        result = await client.call_tool("greet", {"name": "World"})
        assert result[0].text == "Hello, World!"
"""
class TestChepyMCP(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup runs before each test method
        self.mcp_server = mcp
    
    async def test_hello_world(self):
        async with Client(self.mcp_server) as client:
            result = await client.call_tool("personalized_greeting", {"name": "World"})
            #result = await client.read_resource("greetings", {"name": "World"})
            self.assertEqual(result[0].text, "Hello, World!")

if __name__ == '__main__':
    unittest.main()