import unittest
from server.main import mcp
from fastmcp import Client
import json


class TestChepyMain(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup runs before each test method
        # await setup_server()
        pass

    async def test_hello_world(self):
        async with Client(mcp) as client:
            result = await client.call_tool("personalized_greeting", {"name": "World"})
            # result = await client.read_resource("greetings", {"name": "World"})
            self.assertEqual(result[0].text, "Hello, World!")

    async def test_chepy_operations_resource(self):
        async with Client(mcp) as client:
            result = await client.read_resource("resource://chepy_operations")
            ops = json.loads(result[0].text)
            self.assertIsInstance(ops, dict)
            self.assertIn("to_base64", ops)
            self.assertIn("from_base64", ops)


if __name__ == "__main__":
    unittest.main()
