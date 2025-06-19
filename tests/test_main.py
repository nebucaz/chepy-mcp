import unittest

# import asyncio
from server.main import mcp, setup_server
from fastmcp import Client

# from servers.data_format import data_format_mcp


class TestChepyMain(unittest.IsolatedAsyncioTestCase):
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

            self.assertIn("personalized_greeting", tool_names)
            self.assertIn("data_format_to_base64", tool_names)
            self.assertIn("data_format_from_base64", tool_names)


if __name__ == "__main__":
    unittest.main()
