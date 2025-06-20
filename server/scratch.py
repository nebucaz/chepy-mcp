class OperationModel(BaseModel):
    """
    Input model for a single operation
    """

    operation: str = Field(..., description="Name of the operation")
    args: [str]


class PipelineModel(BaseModel):
    """
    Input model for a chain of operations that are to be applied to the input
    Valid operations are: from_base64, to_base64
    """

    input: str = Field(
        ...,
        description="Input string on which the operations are applied sequentially",
    )
    operations: list[OperationModel] = Field(..., description="List of operations")
    args: list[str] = Field(
        ...,
        description="Array of strings to be passed as positional arguments to the operator",
    )
