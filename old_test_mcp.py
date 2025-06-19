import unittest

# import asyncio
from server import mcp, setup_server
from fastmcp import Client

# from servers.data_format import data_format_mcp


class TestChepyMCP(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup runs before each test method
        await setup_server()

    async def test_hello_world(self):
        async with Client(mcp) as client:
            result = await client.call_tool("personalized_greeting", {"name": "World"})
            # result = await client.read_resource("greetings", {"name": "World"})
            self.assertEqual(result[0].text, "Hello, World!")

    async def test_import(self):
        # Ensure the server is set up

        async with Client(mcp) as client:
            # Check that all tools are available
            tools = await client.list_tools()
            tool_names = [tool.name for tool in tools]

            # Main server tool
            self.assertIn("personalized_greeting", tool_names)

            """
            # Sub server tools with prefix
            self.assertIn("sub_calculate", tool_names)
            self.assertIn("sub_format_text", tool_names)

            # Test main tool
            result = await client.call_tool("main_tool", {"x": 3})
            self.assertEqual(result[0].text, "30")

            # Test imported sub tools
            result = await client.call_tool("sub_calculate", {"a": 10, "b": 5})
            self.assertEqual(result[0].text, "15")

            result = await client.call_tool(
                "sub_format_text", {"text": "WORLD", "uppercase": False}
            )
            self.assertEqual(result[0].text, "world")
            """


if __name__ == "__main__":
    unittest.main()
