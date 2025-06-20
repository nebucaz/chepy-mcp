import unittest
from fastmcp import Client
from mcp.types import TextContent
from chepy import Chepy
from server.main import BakePipelineModel, OperationModel, mcp, setup_server


class TestBake(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup runs before each test method
        await setup_server()

    def _bake_logic(self, input_data: BakePipelineModel) -> str:
        c = Chepy(input_data.input)
        for step in input_data.pipeline:
            func = getattr(c, step.op)
            params = step.params or {}
            c = func(**params)
        return c.out

    def test_bake_base64_roundtrip(self):
        input_str = "hello world"
        pipeline = [OperationModel(op="to_base64"), OperationModel(op="from_base64")]
        model = BakePipelineModel(input=input_str, pipeline=pipeline)
        result = self._bake_logic(model)
        self.assertEqual(result, input_str)

    async def test_bake_base64(self):
        string_to_encode = (
            "The quick brown fox jumps over the lazy dog\n- 10 times in a row"
        )
        pipeline = [OperationModel(op="to_base64"), OperationModel(op="from_base64")]
        model = BakePipelineModel(input=string_to_encode, pipeline=pipeline)

        async with Client(mcp) as client:
            result: [TextContent] = await client.call_tool(
                "bake", {"input_data": model}
            )

            self.assertEqual(string_to_encode, result[0].text)


if __name__ == "__main__":
    unittest.main()
