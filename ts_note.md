copy from 
https://github.com/oxc/ComfyUI/tree/docker


## Docker

There are prebuilt docker images for AMD and NVIDIA GPUs on [GitHub Packages](https://ghcr.io/comfyanonymous/comfyui).

You can pull them to your local docker registry with:

```shell
# For NVIDIA GPUs
docker pull ghcr.io/comfyanonymous/comfyui:latest-cu121
# For AMD GPUs
docker pull ghcr.io/comfyanonymous/comfyui:latest-rocm5.6

# For AMD GPUs with ROCm 5.7
docker pull ghcr.io/comfyanonymous/comfyui:latest-rocm5.7-nightly
# For CPU only
docker pull ghcr.io/comfyanonymous/comfyui:latest-cpu
```

### Building images manually

You can build a docker image with the Dockerfile in this repo.

Specify PYTORCH_INSTALL_ARGS build arg with one of the PyTorch commands above to build for AMD or NVIDIA GPUs.

```docker buildx --build-arg PYTORCH_INSTALL_ARGS="--index-url https://download.pytorch.org/whl/cu121" .```

```docker buildx --build-arg PYTORCH_INSTALL_ARGS="--index-url https://download.pytorch.org/whl/rocm5.6" .```

```docker buildx --build-arg PYTORCH_INSTALL_ARGS="--pre --index-url https://download.pytorch.org/whl/nightly/rocm5.7" .```

This dockerfile requires BuildKit to be enabled. If your docker does not support the buildx command, you can
enable BuildKit by setting the DOCKER_BUILDKIT environment variable.

```DOCKER_BUILDKIT=1 docker build --build-arg PYTORCH_INSTALL_ARGS="--index-url https://download.pytorch.org/whl/cu121" .```

NOTE: For building the CPU-only image, it is recommended that you add the --cpu flag to the EXTRA_ARGS build arg:

```docker buildx --build-arg PYTORCH_INSTALL_ARGS="--index-url https://download.pytorch.org/whl/cpu" --build-arg EXTRA_ARGS=--cpu .```



rsync -avzh --partial --progress -e "ssh -i /path/to/your/key.pem" user@210.58.xxx.45:/data/docker_images/custom_comfyui_240109.tar /path/to/destination/custom_comfyui_240109.tar


 rsync -avzh --partial -e "ssh -i /home/tuanshu/.ssh/fu-yuan-tan-hpc-key.pem" --progress centos@210.58.113.45:/data/docker_images/custom_comfyui_240109.tar custom_comfyui_240109.tar

rsync -avzh --partial -e "ssh -i /home/tuanshu/.ssh/fu-yuan-tan-hpc-key.pem" --progress centos@210.58.113.45:/data/docker_images/custom_comfyui_240109.tar custom_comfyui_240109.tar

 C:\Users\TuanShu\.ssh

rsync -avzh --partial -e "ssh -i /home/tuanshu/.ssh/fu-yuan-tan-hpc-key.pem" --progress centos@210.58.113.45:/data/repos/stable-diffusion-docker/sd-models/sd_xl_turbo_1.0_fp16.safetensors sd_xl_turbo_1.0_fp16.safetensors


