# Video translation and dubbing in Serverless AI

Source: https://docs.nebius.com/serverless/tutorials/video-translation

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Video translation and dubbing in Serverless AI

With Serverless AI, you can translate and [dub a video](https://en.wikipedia.org/wiki/Dubbing) into another language. To do so, create a Docker image and run a fine-tuning job based on it. The job converts audio to text, translates the text and creates a dubbed video.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram) (VMs)
* [Boot disks](https://docs.nebius.com/compute/resources/pricing.md#disks) attached to the VMs
* Used space in Standard storage in an [Object Storage bucket](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data)

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Steps

### Prepare infrastructure

> [!NOTE]
>
> Create all resources in the same project.

1. Create a CPU-only VM. The VM is required to build the Docker image based on the VM's Linux operating system (OS). If you build the image on a non-Linux OS, the image architecture will be incompatible with Serverless AI, and the fine-tuning job will fail.

   Configure SSH access to the VM so that you can connect to it later.

   **Web console**

   1. In the [web console](https://console.nebius.com), go to  **Compute** → **Virtual machines**.

   2. Click **Create resource** → **Virtual machine**.

   3. On the page that opens, set the following VM configuration:

      * **Computing resources**: Without GPU.
      * **Platform**: Non-GPU AMD EPYC Genoa.
      * **Preset**: 4 CPUs — 16 GiB RAM.
      * **Boot disk operating system**: Ubuntu 24.04 LTS.
      * **Boot disk size**: At least 100 GiB.
      * **Public IP address**: `Auto assign dynamic IP`.
      * **Username and SSH key**: Configure access credentials.

   4. Click **Create VM**.

   **CLI**

   1. Create a boot disk:

      ```bash theme={null}
      nebius compute disk create \
        --name my-boot-disk \
        --size-gibibytes 100 \
        --type network_ssd \
        --source-image-family-image-family ubuntu24.04-driverless \
        --block-size-bytes 4096
      ```

   2. To add a user for connections to the VM, create a configuration by using the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:
      ```bash theme={null}
      export USER_DATA=$(jq -Rrs '.' <<EOF
      #cloud-config
      users:
        - name: $USER
          sudo: ALL=(ALL) NOPASSWD:ALL
          shell: /bin/bash
          ssh_authorized_keys:
            - $(cat ~/.ssh/id_ed25519.pub)
      EOF
      )
      ```

   3. Create the VM:

      ```bash theme={null}
      nebius compute instance create \
        --name vm-for-dubbing \
        --boot-disk-existing-disk-id <boot_disk_ID> \
        --boot-disk-attach-mode READ_WRITE \
        --resources-platform cpu-d3 \
        --resources-preset 4vcpu-16gb \
        --network-interfaces "[{\"name\": \"eth0\", \"subnet_id\": \"<subnet_ID>\", \"ip_address\": {}, \"public_ip_address\": {}}]" \
        --cloud-init-user-data "$USER_DATA"
      ```

      This command creates a VM without GPUs, assigns a dynamic public IP address and configures SSH access.

      For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

   **Terraform**

   1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

   2. Create a boot disk by using the following configuration:

      ```hcl theme={null}
      resource "nebius_compute_v1_disk" "my_boot_disk" {
        name           = "my-boot-disk"
        parent_id      = "<project_ID>"
        size_gibibytes = 100
        type           = "NETWORK_SSD"
        source_image_family = {
          image_family = "ubuntu24.04-driverless"
        }
        block_size_bytes = 4096
      }
      ```

      To get the project ID, go to the [web console](https://console.nebius.com) and expand the list of projects. Next to the project's name, click  → **Copy project ID**.

   3. To add a user for connections to the VM, create a configuration by using the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:
      ```bash theme={null}
      export USER_DATA=$(jq -Rrs '.' <<EOF
      #cloud-config
      users:
        - name: $USER
          sudo: ALL=(ALL) NOPASSWD:ALL
          shell: /bin/bash
          ssh_authorized_keys:
            - $(cat ~/.ssh/id_ed25519.pub)
      EOF
      )
      ```

   4. Create the VM:

      ```hcl theme={null}
      resource "nebius_compute_v1_instance" "my_vm" {
        name      = "my-vm"
        parent_id = "<project_ID>"
        resources = {
          platform = "cpu-d3"
          preset   = "4vcpu-16gb"
        }
        boot_disk = {
          existing_disk = {
            id = nebius_compute_v1_disk.my_boot_disk.id
          }
          attach_mode = "READ_WRITE"
        }
        cloud_init_user_data = var.user_data
        network_interfaces = [
          {
            name       = "eth0"
            ip_address = {}
            public_ip_address = {}
            subnet_id = "<subnet_ID>"
          }
        ]
      }
      ```

      This manifest creates a VM without GPUs, assigns a dynamic public IP address and configures SSH access.

      For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

   5. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   6. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

1) Create a bucket to store fine-tuning artifacts.

   **Web console**

   1. In the web console, go to  **Storage** → **Object Storage**.

   2. Click  **Create bucket**.

   3. In the **Maximum size** field, select **Unlimited**.

      Leave the other settings at their default values.

   4. Click **Create bucket**.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius storage bucket create --name my-tts-bucket
   ```

   **Terraform**

   1. Use the following configuration file:

      ```hcl theme={null}
      resource "nebius_storage_v1_bucket" "my_bucket" {
        name      = "my-tts-bucket"
        parent_id = "<project_ID>"
      }
      ```

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

### Prepare files for the Docker image

1. To connect to the VM, get its public IP address:

   **Web console**

   1. In the web console, go to  **Compute** → **Virtual machines**.
   2. On the **Standalone VMs** tab, open the VM page.
   3. In **Network** → **Public IPv4**, copy the address.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius compute instance get-by-name --name vm-for-dubbing \
     --format jsonpath='{.status.network_interfaces[0].public_ip_address.address}'
   ```

2. [Connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) by using SSH:
   ```bash theme={null}
   ssh <username>@<IP_address>
   ```
   Specify the username that you set when creating the VM.

3. On the VM, create a working directory:

   ```bash theme={null}
   mkdir ~/video-translation-nebius
   cd ~/video-translation-nebius
   ```

4. In this directory, create the following files for building the Docker image:

   > **requirements.txt**
   >
   > ```txt theme={null}
   > # Core API
   > fastapi==0.115.12
   > uvicorn[standard]==0.30.6
   > requests==2.32.3
   >
   > # ASR
   > openai-whisper==20250625
   >
   > # Translation
   > transformers==4.48.3
   > accelerate==1.6.0
   > sentencepiece==0.2.0
   >
   > # Text to speech
   > TTS==0.22.0
   >
   > # Media pipeline
   > moviepy==1.0.3
   >
   > # Torch stack
   > torch==2.5.1
   > torchaudio==2.5.1
   > ```

   > **process\_video.py**
   >
   > ```python theme={null}
   > #!/usr/bin/env python3
   > import argparse
   > import subprocess
   > from pathlib import Path
   > import requests
   > import torch
   > import whisper
   > from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
   > from TTS.api import TTS
   >
   > def run(cmd):
   >     print("+", " ".join(cmd), flush=True)
   >     subprocess.run(cmd, check=True)
   >
   > def download(url: str, dst: Path):
   >     with requests.get(url, stream=True, timeout=60) as r:
   >         r.raise_for_status()
   >         with dst.open("wb") as f:
   >             for chunk in r.iter_content(chunk_size=1024 * 1024):
   >                 if chunk:
   >                     f.write(chunk)
   >
   > def split_text(text: str, max_chars: int = 700):
   >     text = " ".join(text.split())
   >     chunks, cur = [], ""
   >     for sent in text.split(". "):
   >         s = sent.strip()
   >         if not s:
   >             continue
   >         s = s + ("" if s.endswith(".") else ".")
   >         if len(cur) + len(s) + 1 > max_chars:
   >             if cur:
   >                 chunks.append(cur.strip())
   >             cur = s
   >         else:
   >             cur = (cur + " " + s).strip()
   >     if cur:
   >         chunks.append(cur)
   >     return chunks
   >
   > def translate_text(text: str, target_lang: str):
   >     model_name = "jbochi/madlad400-3b-mt"
   >     tokenizer = AutoTokenizer.from_pretrained(model_name)
   >     model = AutoModelForSeq2SeqLM.from_pretrained(
   >         model_name,
   >         torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
   >         device_map="auto",
   >     )
   >     out = []
   >     for chunk in split_text(text):
   >         prompt = f"<2{target_lang}> {chunk}"
   >         ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
   >         gen = model.generate(**ids, max_new_tokens=512)
   >         out.append(tokenizer.decode(gen[0], skip_special_tokens=True))
   >     return " ".join(out).strip()
   >
   > def main():
   >     p = argparse.ArgumentParser()
   >     p.add_argument("--url", required=True)
   >     p.add_argument("--target-lang", default="de")
   >     p.add_argument("--work-dir", default="/tmp/work")
   >     p.add_argument("--output-dir", default="/mnt/data/output")
   >     p.add_argument("--tts-model", default="tts_models/de/thorsten/vits")
   >     args = p.parse_args()
   >
   >     work = Path(args.work_dir)
   >     out = Path(args.output_dir)
   >     work.mkdir(parents=True, exist_ok=True)
   >     out.mkdir(parents=True, exist_ok=True)
   >
   >     in_mp4 = work / "input.mp4"
   >     asr_wav = work / "asr.wav"
   >     dub_wav = work / "dub.wav"
   >     tmp_out_mp4 = work / "output_video_with_audio.mp4"
   >     out_mp4 = out / "output_video_with_audio.mp4"
   >     transcript_txt = out / "transcript.txt"
   >     translated_txt = out / "translated.txt"
   >
   >     download(args.url, in_mp4)
   >
   >     run(["ffmpeg", "-y", "-i", str(in_mp4), "-vn", "-ac", "1", "-ar", "16000", str(asr_wav)])
   >
   >     device = "cuda" if torch.cuda.is_available() else "cpu"
   >     asr = whisper.load_model("turbo", device=device)
   >     r = asr.transcribe(str(asr_wav))
   >     source_text = " ".join(r["text"].split())
   >     transcript_txt.write_text(source_text, encoding="utf-8")
   >
   >     translated = translate_text(source_text, args.target_lang)
   >     translated_txt.write_text(translated, encoding="utf-8")
   >
   >     tts = TTS(model_name=args.tts_model, gpu=torch.cuda.is_available())
   >     tts.tts_to_file(text=translated, file_path=str(dub_wav))
   >
   >     run([
   >         "ffmpeg", "-y",
   >         "-i", str(in_mp4),
   >         "-i", str(dub_wav),
   >         "-map", "0:v:0",
   >         "-map", "1:a:0",
   >         "-c:v", "copy",
   >         "-c:a", "aac",
   >         "-shortest",
   >         str(tmp_out_mp4),
   >     ])
   >
   >     # IMPORTANT: write locally first, then copy to mounted Object Storage
   >     with tmp_out_mp4.open("rb") as src, out_mp4.open("wb") as dst:
   >         dst.write(src.read())
   >
   >     print(f"Done: {out_mp4}", flush=True)
   >
   > if __name__ == "__main__":
   >     main()
   > ```

   > **app.py**
   >
   > ```python theme={null}
   > from fastapi import FastAPI, HTTPException
   > from fastapi.responses import FileResponse
   > from pathlib import Path
   >
   > app = FastAPI()
   > OUT = Path("/mnt/data/output")
   >
   > @app.get("/health")
   > def health():
   >     return {"ok": True, "output_dir": str(OUT), "exists": OUT.exists()}
   >
   > @app.get("/outputs")
   > def outputs():
   >     if not OUT.exists():
   >         return {"files": []}
   >     return {"files": sorted([p.name for p in OUT.iterdir() if p.is_file()])}
   >
   > @app.get("/download")
   > def download():
   >     f = OUT / "output_video_with_audio.mp4"
   >     if not f.exists():
   >         raise HTTPException(status_code=404, detail="output_video_with_audio.mp4 not found")
   >     return FileResponse(str(f), media_type="video/mp4", filename=f.name)
   > ```

   > **Dockerfile**
   >
   > ```dockerfile theme={null}
   > FROM nvidia/cuda:13.1.2-cudnn-runtime-ubuntu24.04
   >
   > ENV DEBIAN_FRONTEND=noninteractive
   > WORKDIR /app
   >
   > RUN apt-get update && apt-get install -y --no-install-recommends \
   >     software-properties-common curl git ffmpeg libgl1 libglib2.0-0 espeak-ng \
   >     && add-apt-repository ppa:deadsnakes/ppa -y \
   >     && apt-get update && apt-get install -y --no-install-recommends \
   >     python3.11 python3.11-venv python3.11-dev \
   >     && rm -rf /var/lib/apt/lists/*
   >
   > ENV VENV_PATH=/opt/venv
   > RUN python3.11 -m venv $VENV_PATH
   > ENV PATH="$VENV_PATH/bin:$PATH"
   >
   > COPY requirements.txt /app/requirements.txt
   > RUN pip install --upgrade pip setuptools wheel && \
   >     pip install --no-cache-dir -r /app/requirements.txt
   >
   > COPY process_video.py /app/process_video.py
   > COPY app.py /app/app.py
   >
   > EXPOSE 8000
   > CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
   > ```

   To verify that all files are present, run `ls` or `tree`.

5. Make the `process_video.py` file executable:

   ```bash theme={null}
   chmod +x process_video.py
   ```

### Build and push the Docker image

On the VM:

1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

2. Install additional packages and prepare Docker for building the image:

   ```bash theme={null}
   sudo apt-get update
   sudo apt-get install -y docker.io git curl wget unzip python3 python3-pip ca-certificates
   sudo usermod -aG docker "$USER"
   newgrp docker
   ```

3. Check that the Docker daemon is running:
   ```bash theme={null}
   docker ps
   ```
   If Docker is running, this command returns a table of containers (can be empty). If you don't see the table and the daemon isn't running, [launch it](https://docs.docker.com/engine/daemon/start/).

4. [Create an account](https://docs.docker.com/accounts/create-account/) in Docker Hub. Use it for authentication when you push your image to a repository.

5. [Create a public repository](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/) in Docker Hub. You will push your Docker image there.

6. In the `~/video-translation-nebius` directory, build the image:

   ```bash theme={null}
   docker build -t <repository>/<image>:video-translation-nebius .
   ```

   In the command, specify your public repository. For example, `myrepository/dubbing:video-translation-nebius`.

   This operation can take several minutes to complete.

7. Authenticate in Docker Hub:
   ```bash theme={null}
   docker login -u <username>
   ```
   Specify your username at Docker Hub and enter your password when prompted.

8. Push the image to the repository:

   ```bash theme={null}
   docker push <repository>/<image>:video-translation-nebius
   ```

   This operation can take several minutes to complete.

### Create a dubbed video

1. Create a fine-tuning job that generates a model for translation and that dubs the video:

   **Web console**

   1. In the web console, go to  **Serverless AI** → **Jobs**.

   2. Click  **Create job**.

   3. On the page that opens, specify the following job parameters:

      * **Configuration**: Custom.

      * **Image path**: `<repository>/<image>:video-translation-nebius`. Set the image that you've pushed to the Docker repository.

      * **Entrypoint command**:

        ```bash theme={null}
        python3 /app/process_video.py --url https://archive.org/download/BigBuckBunny_328/BigBuckBunny_512kb.mp4 --target-lang de --work-dir /tmp/work --output-dir /mnt/data/output
        ```

        The `--url` parameter contains a link to the video being processed. The `--target-lang` parameter specifies what language the audio track is translated into.

      * **Computing resources** and **Container disk**: Keep the predefined settings.

      * **Mounted volumes**: Click **Attach volume** and select the bucket created earlier.

      * **Mount path**: `/mnt/data`.

   4. Click **Create job**.

   > [!TIP]
   >
   > While the job is running, you can check its logs on the job's page, on the **Logs** tab. The logs show how the model is processing the audio, transcribing and translating the text.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius ai job create \
      --name fine-tune-model \
      --image <repository>/<image>:video-translation-nebius \
      --container-command python3 \
      --args "/app/process_video.py --url https://archive.org/download/BigBuckBunny_328/BigBuckBunny_512kb.mp4 --target-lang de --work-dir /tmp/work --output-dir /mnt/data/output" \
      --volume "<bucket_ID>:/mnt/data" \
      --platform gpu-l40s-a \
      --preset 1gpu-8vcpu-32gb \
      --disk-size 250Gi \
      --subnet-id <subnet_ID>
   ```

   In `--args`, the `--url` parameter contains a link to the video being processed. The `--target-lang` parameter specifies what language the audio track is translated into.

   To get the bucket ID, run `nebius storage bucket list`. For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

   > [!TIP]
   >
   > While the job is running, you can check its logs by using `nebius ai logs <job_ID>`. The logs show how the model is processing the audio, transcribing and translating the text.

   After the job reaches the `Complete` status, the following files are created in the bucket:

   * `output/transcript.txt`: Speech that the model recognized in the video.
   * `output/translated.txt`: Translation of this speech.
   * `output/output_video_with_audio.mp4`: Dubbed video.

   The speech-to-text (STT) quality in this tutorial is not production-level. Accuracy may be low with short sample videos and default model settings. That is expected because the tutorial's purpose is only to showcase the process of STT, video translation and dubbing. To improve the quality, use stronger STT or translation models, split audio into smaller segments and add audio post-processing.

2. Download the dubbed video:

   **Web console**

   1. Open the bucket's page and go to the `output` directory.
   2. In the line of the `output/output_video_with_audio.mp4` object, click  → **Download**.

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources, so Nebius AI Cloud doesn't charge for them:

* [CPU-only VM](https://docs.nebius.com/compute/virtual-machines/delete.md)
* [Boot disk](https://docs.nebius.com/compute/storage/manage.md#how-to-delete-a-volume) attached to the VM
* [Bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets)
