from typing import List, Union

from pydantic import BaseModel, Extra


class ComfyInput(BaseModel):
    class_name: str
    type_name: str


class ComfySimpleInput(BaseModel):
    input_name: str
    input_value: Union[str, int, float]


class ComfyNode(BaseModel):
    id: int
    class_name: str
    inputs: List[Union[ComfyInput, ComfySimpleInput]]
