from pydantic import BaseModel,ConfigDict,Field


class MagicArgs(BaseModel):
    model_config = ConfigDict(extra="forbid",strict=True)
    a : int = Field(description="the first param of the magic operation")
    b : int = Field(description="the second param of the magic operation")


def magic_operation(a : int,b : int):
    return a + b




