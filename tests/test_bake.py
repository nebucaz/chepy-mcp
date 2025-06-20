import unittest
from fastmcp import Client
from src.server import BakePipelineModel, OperationModel, BakeOutputModel, mcp
import json


class TestBake(unittest.IsolatedAsyncioTestCase):
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

            bake_result: BakeOutputModel = json.loads(result[0].text)
            self.assertEqual(bake_result["type"], "text")
            self.assertEqual(bake_result["data"], string_to_encode)


if __name__ == "__main__":
    unittest.main()
