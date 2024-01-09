import importlib
import json
from typing import List, Union

from pydantic import BaseModel


# 定義模型
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


# 處理 ComfyInput 的函數
def process_comfy_input(input, nodes_dict):
    target_class = importlib.import_module("nodes").__dict__[input.class_name]
    type_index = target_class.RETURN_TYPES.index(input.type_name)
    return [str(nodes_dict[input.class_name]), type_index]


# 主函數
def generate_json(nodes_list: List[ComfyNode]):
    nodes_dict = {node.class_name: node.id for node in nodes_list}
    output = {}

    for node in nodes_list:
        node_data = {"class_type": node.class_name, "inputs": {}}
        for input in node.inputs:
            if isinstance(input, ComfySimpleInput):
                node_data["inputs"][input.input_name] = input.input_value
            elif isinstance(input, ComfyInput):
                node_data["inputs"][input.class_name.lower()] = process_comfy_input(input, nodes_dict)
        output[str(node.id)] = node_data

    return json.dumps(output, indent=2)


# 示例
nodes_list = [
    # 填充您的實例...
]

# 輸出 JSON
print(generate_json(nodes_list))
