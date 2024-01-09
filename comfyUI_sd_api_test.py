import base64
import io
import json

import requests
from PIL import Image, PngImagePlugin

url = "http://210.58.113.45:6601"  # "http://10.62.161.193:7865"

# payload = {"prompt": "puppy dog", "steps": 5}
payload = {
    "5": {
        "inputs": {"width": 512, "height": 512, "batch_size": 1},
        "class_type": "EmptyLatentImage",
        "_meta": {"title": "Empty Latent Image"},
    },
    "6": {
        "inputs": {"text": "anime girl cute cute", "clip": ["20", 1]},
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "CLIP Text Encode (Prompt)"},
    },
    "7": {
        "inputs": {"text": "text, watermark", "clip": ["20", 1]},
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "CLIP Text Encode (Prompt)"},
    },
    "8": {"inputs": {"samples": ["13", 0], "vae": ["20", 2]}, "class_type": "VAEDecode", "_meta": {"title": "VAE Decode"}},
    "13": {
        "inputs": {
            "add_noise": True,
            "noise_seed": 0,
            "cfg": 1,
            "model": ["20", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "sampler": ["14", 0],
            "sigmas": ["22", 0],
            "latent_image": ["5", 0],
        },
        "class_type": "SamplerCustom",
        "_meta": {"title": "SamplerCustom"},
    },
    "14": {"inputs": {"sampler_name": "euler_ancestral"}, "class_type": "KSamplerSelect", "_meta": {"title": "KSamplerSelect"}},
    "20": {
        "inputs": {"ckpt_name": "sd_xl_turbo_1.0_fp16.safetensors"},
        "class_type": "CheckpointLoaderSimple",
        "_meta": {"title": "Load Checkpoint"},
    },
    "22": {
        "inputs": {"steps": 1, "denoise": 1, "model": ["20", 0]},
        "class_type": "SDTurboScheduler",
        "_meta": {"title": "SDTurboScheduler"},
    },
    "25": {"inputs": {"images": ["8", 0]}, "class_type": "PreviewImage", "_meta": {"title": "Preview Image"}},
    "27": {"inputs": {"filename_prefix": "ComfyUI", "images": ["8", 0]}, "class_type": "SaveImage", "_meta": {"title": "Save Image"}},
}
# payload = {"prompt_not_existing": "puppy dog", "steps_not_existing": 5}

response = requests.post(url=f"{url}/prompt", json=payload)

print(response.content)
r = response.json()

for i in r["images"]:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

    png_payload = {"image": "data:image/png;base64," + i}
    response2 = requests.post(url=f"{url}/sdapi/v1/png-info", json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save("output.png", pnginfo=pnginfo)
