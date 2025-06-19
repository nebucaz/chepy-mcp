import unittest
from fastmcp import Client
from mcp.types import TextContent
from chepy import Chepy

from server.main import mcp, setup_server
# from servers.data_format import data_format_mcp


class TestChepyMCPDataFormat(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup runs before each test method
        await setup_server()

    async def test_to_base64(self):
        string_to_encode = (
            "The quick brown fox jumps over the lazy dog\n- 10 times in a row"
        )
        async with Client(mcp) as client:
            result: [TextContent] = await client.call_tool(
                "data_format_to_base64", {"input": string_to_encode}
            )

            # to_base64() returns binary string b''
            encoded = Chepy(string_to_encode).to_base64().out.decode("utf-8")
            self.assertEqual(encoded, result[0].text)

    async def test_from_base64(self):
        string_to_encode = (
            "The quick brown fox jumps over the lazy dog\n- 10 times in a row"
        )
        encoded = Chepy(string_to_encode).to_base64().out.decode("utf-8")

        async with Client(mcp) as client:
            result: [TextContent] = await client.call_tool(
                "data_format_from_base64", {"input": encoded}
            )
            self.assertEqual(string_to_encode, result[0].text)
