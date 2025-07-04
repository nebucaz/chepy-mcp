import unittest
from src.server import mcp, BakeOutputModel
from fastmcp import Client
import json
import secrets


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

    async def test_bake_base64(self):
        recipe = [
            {"function": "to_base64", "args": {}},
            {"function": "from_base64", "args": {}},
        ]
        payload = {"input": "hello world", "recipe": recipe}
        async with Client(mcp) as client:
            result = await client.call_tool("bake", {"input_data": payload})
            bake_result: BakeOutputModel = json.loads(result[0].text)
            self.assertEqual(bake_result["type"], "text")
            self.assertEqual(bake_result["data"], "hello world")

    async def test_bake_add(self):
        recipe = [
            {"function": "add", "args": {"n": 1}},
        ]
        payload = {"input": "1", "recipe": recipe}
        async with Client(mcp) as client:
            result = await client.call_tool("bake", {"input_data": payload})
            bake_result: BakeOutputModel = json.loads(result[0].text)
            self.assertEqual(bake_result["type"], "text")
            self.assertEqual(bake_result["data"], "2")

    async def test_bake_aes_encrypt_decrypt(self):
        key = secrets.token_bytes(16).hex()
        iv = secrets.token_bytes(16).hex()
        plaintext = "secret message"
        recipe = [
            {"function": "aes_encrypt", "args": {"key": key, "iv": iv}},
            {"function": "aes_decrypt", "args": {"key": key, "iv": iv}}
        ]
        payload = {"input": plaintext, "recipe": recipe}
        async with Client(mcp) as client:
            result = await client.call_tool("bake", {"input_data": payload})
            bake_result = json.loads(result[0].text)
            self.assertEqual(bake_result["type"], "text")
            self.assertEqual(bake_result["data"], plaintext)

if __name__ == "__main__":
    unittest.main()
