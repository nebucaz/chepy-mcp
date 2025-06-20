import unittest
from fastmcp import Client
from mcp.types import TextContent
from chepy import Chepy
from server.main import (
    BakePipelineModel,
    OperationModel,
    BakeOutputModel,
    mcp,
    setup_server,
)
import base64
import json


class TestBake(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup runs before each test method
        await setup_server()

    def _bake_logic(self, input_data: BakePipelineModel) -> BakeOutputModel:
        c = Chepy(input_data.input)
        for step in input_data.pipeline:
            func = getattr(c, step.op)
            params = step.params or {}
            c = func(**params)
        result = c.out
        if isinstance(result, bytes):
            return BakeOutputModel(
                type="binary", data=base64.b64encode(result).decode("utf-8")
            )
        else:
            return BakeOutputModel(type="text", data=str(result))

    def test_bake_base64_roundtrip(self):
        input_str = "hello world"
        pipeline = [OperationModel(op="to_base64"), OperationModel(op="from_base64")]
        model = BakePipelineModel(input=input_str, pipeline=pipeline)
        result = self._bake_logic(model)
        self.assertEqual(result.type, "text")
        self.assertEqual(result.data, input_str)

    async def test_bake_base64(self):
        string_to_encode = (
            "The quick brown fox jumps over the lazy dog\n- 10 times in a row"
        )
        pipeline = [OperationModel(op="to_base64"), OperationModel(op="from_base64")]
        model = BakePipelineModel(input=string_to_encode, pipeline=pipeline)

        async with Client(mcp) as client:
            result = await client.call_tool("bake", {"input_data": model})
            # Defensive: ensure result is a list and has 'text' attribute
            self.assertTrue(isinstance(result, list) and hasattr(result[0], "text"))
            bake_result: list[TextContent] = json.loads(result[0].text)
            self.assertEqual(bake_result["type"], "text")
            self.assertEqual(bake_result["data"], string_to_encode)


if __name__ == "__main__":
    unittest.main()
