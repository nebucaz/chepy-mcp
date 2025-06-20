import unittest
from src.server import mcp
from fastmcp import Client
import json


class TestChepyMain(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        pass

    async def test_chepy_operations_resource(self):
        async with Client(mcp) as client:
            result = await client.read_resource("resource://chepy_operations")
            ops = json.loads(result[0].text)
            self.assertIsInstance(ops, dict)
            self.assertIn("to_base64", ops)
            self.assertIn("from_base64", ops)


if __name__ == "__main__":
    unittest.main()
