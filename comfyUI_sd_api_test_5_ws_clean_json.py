# This is an example that uses the websockets api to know when a prompt execution is done
# Once the prompt execution is done it downloads the images using the /history endpoint

import json
import urllib.parse
import urllib.request
import uuid

import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)

server_address = "210.58.113.45:6601"
client_id = str(uuid.uuid4())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images


prompt_text = """
{
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "cat red apple forest cold ",
      "clip": [
        "20",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
      "clip": [
        "20",
        1
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "8": {
    "inputs": {
      "samples": [
        "13",
        0
      ],
      "vae": [
        "20",
        2
      ]
    },
    "class_type": "VAEDecode"
  },
  "13": {
    "inputs": {
      "add_noise": true,
      "noise_seed": 0,
      "cfg": 1,
      "model": [
        "20",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "sampler": [
        "14",
        0
      ],
      "sigmas": [
        "22",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "SamplerCustom"
  },
  "14": {
    "inputs": {
      "sampler_name": "euler_ancestral"
    },
    "class_type": "KSamplerSelect"
  },
  "20": {
    "inputs": {
      "ckpt_name": "sd_xl_turbo_1.0_fp16.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "22": {
    "inputs": {
      "steps": 1,
      "denoise": 1,
      "model": [
        "20",
        0
      ]
    },
    "class_type": "SDTurboScheduler"
  },
  "25": {
    "inputs": {
      "images": [
        "8",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Dummy"
    }
  }
}
"""

prompt = json.loads(prompt_text)
# set the text prompt for our positive CLIPTextEncode
prompt["6"]["inputs"]["text"] = "cat red apple forest"

# set the seed for our KSampler node
# prompt["3"]["inputs"]["seed"] = 5

ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, prompt)

import io

from PIL import Image

# 遍歷獲取的圖像數據
for node_id, images_data in images.items():
    for index, image_data in enumerate(images_data):
        # 將二進制數據轉換為圖像
        image = Image.open(io.BytesIO(image_data))

        # 構建文件名並保存圖像
        filename = f"image_{node_id}_{index}.png"
        image.save(filename)

        print(f"圖像已保存為: {filename}")


# Commented out code to display the output images:

# for node_id in images:
#     for image_data in images[node_id]:
#         from PIL import Image
#         import io
#         image = Image.open(io.BytesIO(image_data))
#         image.show()
