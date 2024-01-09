import importlib
import json
from collections import defaultdict
from typing import Any, List, Optional, Union

from pydantic import BaseModel


# 定義模型
class ComfyInput(BaseModel):
    input_name: Optional[str]  # 這是給input側用的名稱, 下面的type_name是output側名稱
    class_name: str
    type_name: str
    input_id: Optional[str]  # in case there are dupe, use this


class ComfySimpleInput(BaseModel):
    input_name: str
    input_value: Any  # Union[bool, int, float, str]  # 順序matters


class ComfyNode(BaseModel):
    id: str
    class_name: str
    inputs: List[Union[ComfyInput, ComfySimpleInput]]


# 處理 ComfyInput 的函數
def process_comfy_input(input: ComfyInput, nodes_dict: dict):
    # 從 nodes.py 中動態導入相應的類別
    try:
        target_class = importlib.import_module("nodes_clean").__dict__[input.class_name]
    except:
        target_class = importlib.import_module("nodes_custom_sampler_clean").__dict__[input.class_name]

    # 獲取 type_index
    print(f'check input.type_name:{input.type_name}')
    print(f'check input.class_name:{input.class_name}')

    try:
        print(f"check target_class.RETURN_NAMES={target_class.RETURN_NAMES}")
        type_index = target_class.RETURN_NAMES.index(input.type_name)
    except:
        print('target class do not have RETURN_NAMES')
        type_index = target_class.RETURN_TYPES.index(input.type_name)

    # aquire id from node_list it self
    if input.input_id:
        class_id = input.input_id
    else:
        if len(nodes_dict[input.class_name]) > 1:
            raise ValueError("not unique class_name in list and input_id not specified.")

        class_id = nodes_dict[input.class_name][0]

    return [class_id, type_index]


# 主函數
def generate_json(nodes_list: List[ComfyNode]):
    nodes_dict = defaultdict(list)

    for node in nodes_list:
        nodes_dict[node.class_name].append(node.id)

    output = {}

    for node in nodes_list:
        node_data = {"inputs": {}, "class_type": node.class_name}
        for input in node.inputs:
            if isinstance(input, ComfySimpleInput):
                print(f"ComfySimpleInput, check input.input_value={input.input_value}")
                print(f"ComfySimpleInput, check type(input.input_value)={type(input.input_value)}")

                node_data["inputs"][input.input_name] = input.input_value
            elif isinstance(input, ComfyInput):
                # 根据 input.class_name 查找相应节点并获取其 id
                key = input.input_name or input.type_name.lower()  # 使用 type_name 作為 key

                node_data["inputs"][key] = process_comfy_input(input, nodes_dict)
        output[str(node.id)] = node_data

    return json.dumps(output, indent=2)


# 示例
nodes_list = [
    ComfyNode(
        id="5",
        class_name="EmptyLatentImage",
        inputs=[
            ComfySimpleInput(input_name="width", input_value=512),
            ComfySimpleInput(input_name="height", input_value=512),
            ComfySimpleInput(input_name="batch_size", input_value=1),
        ],
    ),
    ComfyNode(
        id="6",
        class_name="CLIPTextEncode",
        inputs=[
            ComfySimpleInput(input_name="text", input_value="cat red apple forest cold "),
            ComfyInput(class_name="CheckpointLoaderSimple", type_name="CLIP"),
        ],
    ),
    ComfyNode(
        id="7",
        class_name="CLIPTextEncode",
        inputs=[
            ComfySimpleInput(input_name="text", input_value="text, watermark"),
            ComfyInput(class_name="CheckpointLoaderSimple", type_name="CLIP"),
        ],
    ),
    ComfyNode(
        id="8",
        class_name="VAEDecode",
        inputs=[
            ComfyInput(class_name="SamplerCustom", type_name="output", input_name="samples"),  # not SAMPLES
            ComfyInput(class_name="CheckpointLoaderSimple", type_name="VAE"),
        ],
    ),
    ComfyNode(
        id="13",
        class_name="SamplerCustom",
        inputs=[
            ComfySimpleInput(input_name="add_noise", input_value=True),
            ComfySimpleInput(input_name="noise_seed", input_value=0),
            ComfySimpleInput(input_name="cfg", input_value=1),
            ComfyInput(class_name="CheckpointLoaderSimple", type_name="MODEL"),
            ComfyInput(class_name="CLIPTextEncode", type_name="CONDITIONING", input_id="6", input_name="positive"),
            ComfyInput(class_name="CLIPTextEncode", type_name="CONDITIONING", input_id="7", input_name="negative"),
            ComfyInput(class_name="KSamplerSelect", type_name="SAMPLER"),
            ComfyInput(class_name="SDTurboScheduler", type_name="SIGMAS"),
            ComfyInput(class_name="EmptyLatentImage", type_name="LATENT", input_name="latent_image"),
        ],
    ),
    ComfyNode(id="14", class_name="KSamplerSelect", inputs=[ComfySimpleInput(input_name="sampler_name", input_value="euler_ancestral")]),
    ComfyNode(
        id="20",
        class_name="CheckpointLoaderSimple",
        inputs=[ComfySimpleInput(input_name="ckpt_name", input_value="sd_xl_turbo_1.0_fp16.safetensors")],
    ),
    ComfyNode(
        id="22",
        class_name="SDTurboScheduler",
        inputs=[
            ComfySimpleInput(input_name="steps", input_value=1),
            ComfySimpleInput(input_name="denoise", input_value=1),
            ComfyInput(class_name="CheckpointLoaderSimple", type_name="MODEL"),
        ],
    ),
    ComfyNode(id="25", class_name="PreviewImage", inputs=[ComfyInput(class_name="VAEDecode", type_name="IMAGE", input_name="images")]),
]


# 輸出 JSON
print(generate_json(nodes_list))


simple_test = ComfyNode(
    id="5",
    class_name="EmptyLatentImage",
    inputs=[
        ComfySimpleInput(input_name="width", input_value=512),
        ComfySimpleInput(input_name="height", input_value=512),
        ComfySimpleInput(input_name="batch_size", input_value=1),
    ],
)


print(type(simple_test.inputs[0].input_value))
