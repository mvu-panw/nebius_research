# Speech synthesis in Serverless AI

Source: https://docs.nebius.com/serverless/tutorials/tts

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Speech synthesis in Serverless AI

You can convert text to speech (TTS) by using Serverless AI. To do so:

1. Create a Docker image powered by the [Piper](https://github.com/OHF-Voice/piper1-gpl) engine for TTS.
2. Run a fine-tuning job based on this image. This job produces an [Open Neural Network Exchange](https://onnx.ai) (ONNX) model for TTS.
3. Deploy the model as a Serverless AI endpoint.
4. Synthesize speech from text by using the deployed model.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram) (VMs)
* [Boot disks](https://docs.nebius.com/compute/resources/pricing.md#disks) attached to the VMs
* Used space in Standard storage in an [Object Storage bucket](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data)

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

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
      * **Preset**: 16 CPUs — 64 GiB RAM.
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
        --name my-vm \
        --boot-disk-existing-disk-id <boot_disk_ID> \
        --boot-disk-attach-mode READ_WRITE \
        --resources-platform cpu-d3 \
        --resources-preset 16vcpu-64gb \
        --network-interfaces "[{\"name\": \"eth0\", \"subnet_id\": \"<subnet_ID>\", \"ip_address\": {}, \"public_ip_address\": {}}]" \
        --cloud-init-user-data "$USER_DATA"
      ```

      This command creates a VM without GPUs, assigns a dynamic public IP address and configures SSH access.

      For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

   **Terraform**

   1. Create a boot disk by using the following configuration:

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

      ```hcl theme={null}
      resource "nebius_compute_v1_instance" "my_vm" {
        name      = "my-vm"
        parent_id = "<project_ID>"
        resources = {
          platform = "cpu-d3"
          preset   = "16vcpu-64gb"
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

   4. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   5. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

   **Go SDK**

   1. Create a boot disk:

      ```go theme={null}
      createDiskSvc := sdk.Services().Compute().V1().Disk()
      createDiskOp, err := createDiskSvc.Create(
          ctx,
          &compute.CreateDiskRequest{
              Metadata: &common.ResourceMetadata{
                  ParentId: "<project_ID>",
                  Name:     "my-boot-disk",
              },
              Spec: &compute.DiskSpec{
                  Size: &compute.DiskSpec_SizeGibibytes{
                      SizeGibibytes: 100,
                  },
                  Type: compute.DiskSpec_NETWORK_SSD,
                  BlockSizeBytes: 4096,
                  Source: &compute.DiskSpec_SourceImageFamily{
                      SourceImageFamily: &compute.SourceImageFamily{
                          ImageFamily: "ubuntu24.04-driverless",
                      },
                  },
              },
          },
      )
      if err != nil {
          return fmt.Errorf("create disk: %w", err)
      }
      if _, err = createDiskOp.Wait(ctx); err != nil {
          return fmt.Errorf("wait for disk creation: %w", err)
      }
      fmt.Println(createDiskOp.ResourceID())
      ```

      To get the project ID, go to the [web console](https://console.nebius.com) and expand the list of projects. Next to the project's name, click  → **Copy project ID**.

   2. Create the VM:

      ```go theme={null}
      createVMSvc := sdk.Services().Compute().V1().Instance()
      publicKey, err := os.ReadFile(
          os.Getenv("HOME") + "/.ssh/id_ed25519.pub",
      )
      if err != nil {
          return fmt.Errorf("read SSH public key: %w", err)
      }
      userData := "#cloud-config\nusers:\n  - name: user\n" +
          "    sudo: ALL=(ALL) NOPASSWD:ALL\n" +
          "    shell: /bin/bash\n    ssh_authorized_keys:\n" +
          "      - " + string(publicKey)
      createVMOp, err := createVMSvc.Create(
          ctx,
          &compute.CreateInstanceRequest{
              Metadata: &common.ResourceMetadata{
                  ParentId: "<project_ID>",
                  Name:     "my-vm",
              },
              Spec: &compute.InstanceSpec{
                  Resources: &compute.ResourcesSpec{
                      Platform: "cpu-d3",
                      Size: &compute.ResourcesSpec_Preset{
                          Preset: "16vcpu-64gb",
                      },
                  },
                  BootDisk: &compute.AttachedDiskSpec{
                      AttachMode: compute.AttachedDiskSpec_READ_WRITE,
                      Type: &compute.AttachedDiskSpec_ExistingDisk{
                          ExistingDisk: &compute.ExistingDisk{
                              Id: "<boot_disk_ID>",
                          },
                      },
                  },
                  NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                      {
                          Name: "eth0",
                          SubnetId: "<subnet_ID>",
                          IpAddress: &compute.IPAddress{},
                          PublicIpAddress: &compute.PublicIPAddress{},
                      },
                  },
                  CloudInitUserData: userData,
              },
          },
      )
      if err != nil {
          return fmt.Errorf("create VM: %w", err)
      }
      if _, err = createVMOp.Wait(ctx); err != nil {
          return fmt.Errorf("wait for VM creation: %w", err)
      }
      ```

      This code creates a VM without GPUs, assigns a dynamic public IP address and configures SSH access for `user` with the public key stored in `~/.ssh/id_ed25519.pub`.

      The code uses the following values:

      * `Spec.BootDisk.Type.ExistingDisk.Id`: ID of the boot disk created in the previous step. The code in that step prints it.
      * `Spec.NetworkInterfaces[].SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).

   **Python SDK**

   1. Create a boot disk:

      ```python theme={null}
      create_disk_service = DiskServiceClient(sdk)
      create_disk_operation = await create_disk_service.create(
          CreateDiskRequest(
              metadata=ResourceMetadata(
                  parent_id="<project_ID>",
                  name="my-boot-disk",
              ),
              spec=DiskSpec(
                  size_gibibytes=100,
                  type=DiskSpec.DiskType.NETWORK_SSD,
                  block_size_bytes=4096,
                  source_image_family=SourceImageFamily(
                      image_family="ubuntu24.04-driverless",
                  ),
              ),
          ),
      )
      await create_disk_operation.wait()
      print(create_disk_operation.resource_id)
      ```

      To get the project ID, go to the [web console](https://console.nebius.com) and expand the list of projects. Next to the project's name, click  → **Copy project ID**.

   2. Create the VM:

      ```python theme={null}
      create_vm_service = InstanceServiceClient(sdk)
      public_key = Path.home().joinpath(
          ".ssh/id_ed25519.pub",
      ).read_text()
      user_data = (
          "#cloud-config\nusers:\n  - name: user\n"
          "    sudo: ALL=(ALL) NOPASSWD:ALL\n"
          "    shell: /bin/bash\n"
          "    ssh_authorized_keys:\n"
          f"      - {public_key}"
      )
      create_vm_operation = await create_vm_service.create(
          CreateInstanceRequest(
              metadata=ResourceMetadata(
                  parent_id="<project_ID>",
                  name="my-vm",
              ),
              spec=InstanceSpec(
                  resources=ResourcesSpec(
                      platform="cpu-d3",
                      preset="16vcpu-64gb",
                  ),
                  boot_disk=AttachedDiskSpec(
                      attach_mode=(
                          AttachedDiskSpec.AttachMode.READ_WRITE
                      ),
                      existing_disk=ExistingDisk(
                          id="<boot_disk_ID>",
                      ),
                  ),
                  network_interfaces=[
                      NetworkInterfaceSpec(
                          name="eth0",
                          subnet_id="<subnet_ID>",
                          ip_address=IPAddress(),
                          public_ip_address=PublicIPAddress(),
                      ),
                  ],
                  cloud_init_user_data=user_data,
              ),
          ),
      )
      await create_vm_operation.wait()
      ```

      This code creates a VM without GPUs, assigns a dynamic public IP address and configures SSH access for `user` with the public key stored in `~/.ssh/id_ed25519.pub`.

      The code uses the following values:

      * `spec.boot_disk.existing_disk.id`: ID of the boot disk created in the previous step. The code in that step prints it.
      * `spec.network_interfaces[].subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).

   **JavaScript SDK**

   1. Create a boot disk:

      ```ts theme={null}
      const createDiskService = new DiskService(sdk);
      const createDiskOperation = await createDiskService.create(
        CreateDiskRequest.create({
          metadata: {
            parentId: "<project_ID>",
            name: "my-boot-disk",
          },
          spec: {
            size: {
              $case: "sizeGibibytes",
              sizeGibibytes: 100,
            },
            type: DiskSpec_DiskType.NETWORK_SSD,
            blockSizeBytes: 4096,
            source: {
              $case: "sourceImageFamily",
              sourceImageFamily: SourceImageFamily.create({
                imageFamily: "ubuntu24.04-driverless",
              }),
            },
          },
        }),
      ).result;
      await createDiskOperation.wait();
      console.log(createDiskOperation.resourceId());
      ```

      To get the project ID, go to the [web console](https://console.nebius.com) and expand the list of projects. Next to the project's name, click  → **Copy project ID**.

   2. Create the VM:

      ```ts theme={null}
      const createVmService = new InstanceService(sdk);
      const publicKey = readFileSync(
        `${process.env.HOME}/.ssh/id_ed25519.pub`,
        "utf8",
      );
      const userData = "#cloud-config\nusers:\n  - name: user\n" +
        "    sudo: ALL=(ALL) NOPASSWD:ALL\n" +
        "    shell: /bin/bash\n    ssh_authorized_keys:\n" +
        `      - ${publicKey}`;
      const createVmOperation = await createVmService.create(
        CreateInstanceRequest.create({
          metadata: {
            parentId: "<project_ID>",
            name: "my-vm",
          },
          spec: {
            resources: {
              platform: "cpu-d3",
              size: { $case: "preset", preset: "16vcpu-64gb" },
            },
            bootDisk: {
              attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
              type: {
                $case: "existingDisk",
                existingDisk: { id: "<boot_disk_ID>" },
              },
            },
            networkInterfaces: [{
              name: "eth0",
              subnetId: "<subnet_ID>",
              ipAddress: {},
              publicIpAddress: {},
            }],
            cloudInitUserData: userData,
          },
        }),
      ).result;
      await createVmOperation.wait();
      ```

      This code creates a VM without GPUs, assigns a dynamic public IP address and configures SSH access for `user` with the public key stored in `~/.ssh/id_ed25519.pub`.

      The code uses the following values:

      * `spec.bootDisk.type.existingDisk.id`: ID of the boot disk created in the previous step. The code in that step prints it.
      * `spec.networkInterfaces[].subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).

2. Create a bucket to store fine-tuning artifacts.

   **Web console**

   1. In the web console, go to  **Storage** → **Object Storage**.

   2. Click  **Create bucket**.

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

   **Go SDK**

   ```go theme={null}
   createBucketSvc := sdk.Services().Storage().V1().Bucket()
   createBucketOp, err := createBucketSvc.Create(
       ctx,
       &storage.CreateBucketRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "my-tts-bucket",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create bucket: %w", err)
   }
   if _, err = createBucketOp.Wait(ctx); err != nil {
       return fmt.Errorf("wait for bucket creation: %w", err)
   }
   ```

   In the code, set `Metadata.ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   **Python SDK**

   ```python theme={null}
   create_bucket_service = BucketServiceClient(sdk)
   create_bucket_operation = await create_bucket_service.create(
       CreateBucketRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="my-tts-bucket",
           ),
       ),
   )
   await create_bucket_operation.wait()
   ```

   In the code, set `metadata.parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   **JavaScript SDK**

   ```ts theme={null}
   const createBucketService = new BucketService(sdk);
   const createBucketOperation = await createBucketService.create(
     CreateBucketRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "my-tts-bucket",
       },
     }),
   ).result;
   await createBucketOperation.wait();
   ```

   In the code, set `metadata.parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

### Prepare a dataset

On a local machine, prepare a dataset for training the ONNX model. After that, upload the dataset to the bucket.

1. Create a working directory:

   ```bash theme={null}
   mkdir -p ~/voice-demo-upload/input/raw
   cd ~/voice-demo-upload
   ```

2. Create and activate a [virtual Python environment](https://docs.python.org/3/library/venv.html):

   ```bash theme={null}
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. In this environment, install the required Python dependencies for the dataset preparation:

   ```bash theme={null}
   pip3 install --upgrade pip
   pip3 install datasets soundfile torchcodec torch
   ```

4. Install [FFmpeg](https://www.ffmpeg.org). This is a tool that allows you to record and convert audio, and that is [required for TorchCodec](https://github.com/meta-pytorch/torchcodec?tab=readme-ov-file#installing-cpu-only-torchcodec).

   You can install FFmpeg by running `conda install "ffmpeg"` or `brew install "ffmpeg"` (macOS only).

5. Download five training samples from Hugging Face:

   ```python theme={null}
   python3 - <<'PY'
   from pathlib import Path
   from datasets import load_dataset, Audio

   out = Path("input/raw")
   out.mkdir(parents=True, exist_ok=True)

   ds = load_dataset(
       "openslr/librispeech_asr",
       "clean",
       split="train.100",
       streaming=True,
   )

   ds = ds.cast_column("audio", Audio(decode=False))

   for i, row in enumerate(ds.take(5)):
       audio = row["audio"]
       audio_bytes = audio.get("bytes")

       if not audio_bytes:
           raise RuntimeError(f"No audio bytes found for sample {i}")

       with open(out / f"sample_{i:04d}.flac", "wb") as f:
           f.write(audio_bytes)

   print("Done")
   PY
   ```

6. After the script prints `Done`, check that the samples are downloaded:

   ```bash theme={null}
   find ~/voice-demo-upload/input -maxdepth 3 -type f | sort
   ```

   The output should be the following:

   ```text theme={null}
   ~/voice-demo-upload/input/raw/sample_0000.flac
   ~/voice-demo-upload/input/raw/sample_0001.flac
   ~/voice-demo-upload/input/raw/sample_0002.flac
   ~/voice-demo-upload/input/raw/sample_0003.flac
   ~/voice-demo-upload/input/raw/sample_0004.flac
   ```

7. Upload the `input` folder to the bucket created earlier:

   **Web console**

   1. In the web console, go to  **Storage** → **Object Storage**.
   2. Open the bucket page.
   3. Create the `/mnt/data/input/raw` directory. To do so, click **Add** → **Folder** for every directory in this path.
   4. Go to `/mnt/data/input/raw` and then click **Add** → **Object**.
   5. Upload the samples.

### Prepare files for the Docker image

1. To connect to the VM, get its public IP address:

   **Web console**

   1. In the web console, go to  **Compute** → **Virtual machines**.
   2. On the **Standalone VMs** tab, open the VM page.
   3. In **Network** → **Public IPv4**, copy the address.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius compute instance get-by-name --name my-vm \
     --format jsonpath='{.status.network_interfaces[0].public_ip_address.address}'
   ```

   **Go SDK**

   ```go theme={null}
   getVMSvc := sdk.Services().Compute().V1().Instance()
   vm, err := getVMSvc.GetByName(
       ctx,
       &common.GetByNameRequest{Name: "my-vm"},
   )
   if err != nil {
       return fmt.Errorf("get VM by name: %w", err)
   }
   fmt.Println(vm.GetStatus().GetNetworkInterfaces()[0].
       GetPublicIpAddress().GetAddress())
   ```

   The code prints the public IP address of the VM.

   **Python SDK**

   ```python theme={null}
   get_vm_service = InstanceServiceClient(sdk)
   vm = await get_vm_service.get_by_name(
       GetByNameRequest(name="my-vm"),
   )
   print(vm.status.network_interfaces[0].public_ip_address.address)
   ```

   The code prints the public IP address of the VM.

   **JavaScript SDK**

   ```ts theme={null}
   const getVmService = new InstanceService(sdk);
   const vm = await getVmService.getByName(
     GetByNameRequest.create({ name: "my-vm" }),
   );
   console.log(
     vm.status?.networkInterfaces[0]?.publicIpAddress?.address,
   );
   ```

   The code prints the public IP address of the VM.

2. [Connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) by using SSH:
   ```bash theme={null}
   ssh <username>@<IP_address>
   ```
   Specify the username that you set when creating the VM.

3. On the VM, create a working directory:

   ```bash theme={null}
   mkdir ~/piper-nebius
   cd ~/piper-nebius
   ```

4. In this directory, create the following files for building the Docker image:

   > **train.py**
   >
   > ```python theme={null}
   > #!/usr/bin/env python3
   > import argparse
   > import csv
   > import shutil
   > import subprocess
   > import sys
   > import urllib.request
   > from pathlib import Path
   >
   > import torch
   > import whisper
   >
   >
   > BASE_CKPT_URL = (
   >     "https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/"
   >     "en/en_US/lessac/medium/epoch%3D2164-step%3D1355540.ckpt"
   > )
   >
   >
   > def run(cmd, cwd=None):
   >     print("+", " ".join(cmd), flush=True)
   >     subprocess.run(cmd, cwd=cwd, check=True)
   >
   >
   > def parse_args():
   >     parser = argparse.ArgumentParser(description="Train a Piper voice model non-interactively.")
   >     parser.add_argument("--raw-dir", default="/mnt/data/input/raw")
   >     parser.add_argument("--work-dir", default="/mnt/data/work")
   >     parser.add_argument("--output-dir", default="/mnt/data/output")
   >     parser.add_argument("--voice-name", default="custom_voice")
   >     parser.add_argument("--espeak-voice", default="en-us")
   >     parser.add_argument("--sample-rate", type=int, default=22050)
   >     parser.add_argument("--segment-seconds", type=int, default=10)
   >     parser.add_argument("--whisper-model", default="turbo")
   >     parser.add_argument("--max-epochs", type=int, default=4000)
   >     parser.add_argument("--batch-size", type=int, default=32)
   >     parser.add_argument("--num-workers", type=int, default=8)
   >     parser.add_argument("--base-ckpt-url", default=BASE_CKPT_URL)
   >     parser.add_argument("--no-base-ckpt", action="store_true")
   >     parser.add_argument("--device", default="cuda")
   >     parser.add_argument("--piper-repo", default="/opt/piper1-gpl")
   >     return parser.parse_args()
   >
   >
   > def collect_audio_files(raw_dir: Path):
   >     exts = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
   >     files = sorted(p for p in raw_dir.rglob("*") if p.suffix.lower() in exts)
   >     if not files:
   >         raise FileNotFoundError(f"No audio files found under {raw_dir}")
   >     return files
   >
   >
   > def segment_audio(files, wav_dir: Path, segment_seconds: int, sample_rate: int):
   >     wav_dir.mkdir(parents=True, exist_ok=True)
   >     for src in files:
   >         stem = src.stem.replace(" ", "_")
   >         out_pattern = wav_dir / f"{stem}_%04d.wav"
   >         run(
   >             [
   >                 "ffmpeg",
   >                 "-y",
   >                 "-i",
   >                 str(src),
   >                 "-vn",
   >                 "-ac",
   >                 "1",
   >                 "-ar",
   >                 str(sample_rate),
   >                 "-c:a",
   >                 "pcm_s16le",
   >                 "-f",
   >                 "segment",
   >                 "-segment_time",
   >                 str(segment_seconds),
   >                 str(out_pattern),
   >             ]
   >         )
   >
   >
   > def transcribe_segments(wav_dir: Path, metadata_path: Path, whisper_model: str, device: str):
   >     model = whisper.load_model(whisper_model).to(device)
   >     wav_files = sorted(wav_dir.glob("*.wav"))
   >     if not wav_files:
   >         raise FileNotFoundError(f"No segmented wav files found under {wav_dir}")
   >
   >     with metadata_path.open("w", encoding="utf-8", newline="") as f:
   >         writer = csv.writer(f, delimiter="|", lineterminator="\n")
   >         for wav_path in wav_files:
   >             result = model.transcribe(str(wav_path))
   >             transcript = " ".join(result["text"].strip().split())
   >             if transcript:
   >                 writer.writerow([wav_path.stem, transcript])
   >
   >
   > def download_base_checkpoint(url: str, checkpoint_path: Path):
   >     checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
   >     print(f"+ download {url} -> {checkpoint_path}", flush=True)
   >     urllib.request.urlretrieve(url, checkpoint_path)
   >
   >
   > def sanitize_checkpoint(checkpoint_path: Path):
   >     checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
   >     checkpoint["hyper_parameters"] = {}
   >     torch.save(checkpoint, checkpoint_path)
   >
   >
   > def latest_checkpoint(logs_dir: Path):
   >     checkpoints = sorted(logs_dir.glob("**/checkpoints/*.ckpt"), key=lambda p: p.stat().st_mtime)
   >     if not checkpoints:
   >         raise FileNotFoundError(f"No checkpoints found under {logs_dir}")
   >     return checkpoints[-1]
   >
   >
   > def main():
   >     args = parse_args()
   >
   >     raw_dir = Path(args.raw_dir)
   >     work_dir = Path(args.work_dir)
   >     output_dir = Path(args.output_dir)
   >     wav_dir = work_dir / "wav"
   >     metadata_path = work_dir / "metadata.csv"
   >     cache_dir = work_dir / "cache"
   >     config_path = work_dir / "config.json"
   >     base_ckpt_path = work_dir / "base.ckpt"
   >     logs_dir = Path(args.piper_repo) / "lightning_logs"
   >
   >     work_dir.mkdir(parents=True, exist_ok=True)
   >     output_dir.mkdir(parents=True, exist_ok=True)
   >
   >     audio_files = collect_audio_files(raw_dir)
   >     segment_audio(audio_files, wav_dir, args.segment_seconds, args.sample_rate)
   >     transcribe_segments(wav_dir, metadata_path, args.whisper_model, args.device)
   >
   >     if not args.no_base_ckpt:
   >         download_base_checkpoint(args.base_ckpt_url, base_ckpt_path)
   >         sanitize_checkpoint(base_ckpt_path)
   >
   >     fit_cmd = [
   >         sys.executable,
   >         "-m",
   >         "piper.train",
   >         "fit",
   >         "--data.voice_name",
   >         args.voice_name,
   >         "--data.csv_path",
   >         str(metadata_path),
   >         "--data.audio_dir",
   >         str(wav_dir),
   >         "--model.sample_rate",
   >         str(args.sample_rate),
   >         "--data.espeak_voice",
   >         args.espeak_voice,
   >         "--data.cache_dir",
   >         str(cache_dir),
   >         "--data.config_path",
   >         str(config_path),
   >         "--data.batch_size",
   >         str(args.batch_size),
   >         "--data.num_workers",
   >         str(args.num_workers),
   >         "--trainer.log_every_n_steps",
   >         "1",
   >         "--trainer.max_epochs",
   >         str(args.max_epochs),
   >         "--trainer.accelerator",
   >         "gpu",
   >         "--trainer.devices",
   >         "1",
   >     ]
   >
   >     if not args.no_base_ckpt:
   >         fit_cmd.extend(
   >             [
   >                 "--ckpt_path",
   >                 str(base_ckpt_path),
   >                 "--weights_only",
   >                 "true",
   >             ]
   >         )
   >
   >     run(fit_cmd, cwd=args.piper_repo)
   >
   >     checkpoint_path = latest_checkpoint(logs_dir)
   >     output_model = output_dir / "model.onnx"
   >     output_config = output_dir / "model.onnx.json"
   >
   >     run(
   >         [
   >             sys.executable,
   >             "-m",
   >             "piper.train.export_onnx",
   >             "--checkpoint",
   >             str(checkpoint_path),
   >             "--output-file",
   >             str(output_model),
   >         ],
   >         cwd=args.piper_repo,
   >     )
   >
   >     if config_path.exists():
   >         if output_config.exists():
   >             print(f"Config already exists at {output_config}, leaving as-is", flush=True)
   >         else:
   >             try:
   >                 shutil.copy2(config_path, output_config)
   >             except PermissionError:
   >                 try:
   >                     shutil.copyfile(config_path, output_config)
   >                 except PermissionError as exc:
   >                     print(
   >                         f"Warning: could not write config to {output_config}: {exc}. "
   >                         "Model export succeeded; continuing without output JSON copy.",
   >                         flush=True,
   >                     )
   >
   >     print(f"Training complete. ONNX model: {output_model}", flush=True)
   >
   >
   > if __name__ == "__main__":
   >     main()
   > ```

   > **app.py**
   >
   > ```python theme={null}
   > #!/usr/bin/env python3
   > import subprocess
   > import tempfile
   > from pathlib import Path
   >
   > from fastapi import FastAPI, HTTPException
   > from fastapi.responses import FileResponse
   > from pydantic import BaseModel
   >
   >
   > MODEL_PATH = Path("/mnt/data/output/model.onnx")
   > CONFIG_PATH = Path("/mnt/data/output/model.onnx.json")
   >
   > app = FastAPI(title="Piper Voice Endpoint")
   >
   >
   > class SynthesizeRequest(BaseModel):
   >     text: str
   >
   >
   > @app.get("/health")
   > def health():
   >     return {
   >         "ok": MODEL_PATH.exists(),
   >         "model": str(MODEL_PATH),
   >         "config": str(CONFIG_PATH),
   >     }
   >
   >
   > @app.post("/synthesize")
   > def synthesize(request: SynthesizeRequest):
   >     if not MODEL_PATH.exists():
   >         raise HTTPException(status_code=503, detail="model.onnx not found at /mnt/data/output")
   >
   >     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
   >         output_path = Path(tmp.name)
   >
   >     try:
   >         subprocess.run(
   >             ["piper", "-m", str(MODEL_PATH), "--output_file", str(output_path)],
   >             input=request.text,
   >             text=True,
   >             check=True,
   >         )
   >         return FileResponse(output_path, media_type="audio/wav", filename="speech.wav")
   >     except subprocess.CalledProcessError as exc:
   >         raise HTTPException(status_code=500, detail=f"inference failed: {exc}") from exc
   > ```

   > **requirements.txt**
   >
   > ```txt theme={null}
   > datasets
   > soundfile
   > torch<2.6
   > openai-whisper
   > fastapi
   > uvicorn[standard]
   > piper-phonemize
   > ```

   > **sitecustomize.py**
   >
   > ```python theme={null}
   > import pathlib
   > import torch.serialization
   >
   > torch.serialization.add_safe_globals([pathlib.PosixPath])
   > ```

   > **Dockerfile**
   >
   > ```dockerfile theme={null}
   > FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04
   >
   > ENV DEBIAN_FRONTEND=noninteractive
   > ENV PIPER_REPO=/opt/piper1-gpl
   > ENV PYTHONUNBUFFERED=1
   > ENV PYTHONPATH=/app
   >
   > RUN apt-get update && apt-get install -y \
   >     python3 \
   >     python3-pip \
   >     python3-venv \
   >     python3-dev \
   >     ffmpeg \
   >     git \
   >     wget \
   >     curl \
   >     cmake \
   >     build-essential \
   >     ninja-build \
   >     espeak-ng \
   >     && rm -rf /var/lib/apt/lists/*
   >
   > WORKDIR /app
   >
   > COPY requirements.txt /app/requirements.txt
   >
   > RUN python3 -m pip install --upgrade pip setuptools wheel scikit-build && \
   >     python3 -m pip install -r /app/requirements.txt
   >
   > RUN git clone https://github.com/OHF-voice/piper1-gpl.git ${PIPER_REPO} && \
   >     python3 -m pip install ${PIPER_REPO} && \
   >     cp /usr/local/lib/python3.10/dist-packages/piper/espeakbridge.so /tmp/espeakbridge.so && \
   >     cp /usr/local/lib/python3.10/dist-packages/piper/espeakbridge.pyi /tmp/espeakbridge.pyi && \
   >     python3 -m pip install -e ${PIPER_REPO}[train] && \
   >     cp /tmp/espeakbridge.so ${PIPER_REPO}/src/piper/espeakbridge.so && \
   >     cp /tmp/espeakbridge.pyi ${PIPER_REPO}/src/piper/espeakbridge.pyi && \
   >     ${PIPER_REPO}/build_monotonic_align.sh
   >
   > COPY train.py /app/train.py
   > COPY app.py /app/app.py
   > COPY sitecustomize.py /app/sitecustomize.py
   >
   > EXPOSE 8000
   >
   > CMD ["python3", "/app/train.py"]
   > ```

   To verify that all files are present, run `ls` or `tree`.

### Build and push the Docker image

On the VM:

1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

2. Install additional packages and prepare Docker for building the image:

   ```bash theme={null}
   sudo apt-get update
   sudo apt-get install -y git curl wget unzip python3 python3-venv python3-pip ca-certificates
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

6. In the `~/piper-nebius` directory, build the image:

   ```bash theme={null}
   docker build -t <repository>/<image>:piper-nebius-ui-tutorial .
   ```

   In the command, specify your public repository. For example, `myrepository/tts:piper-nebius-ui-tutorial`.

   This operation can take several minutes to complete.

7. Authenticate in Docker Hub:
   ```bash theme={null}
   docker login -u <username>
   ```
   Specify your username at Docker Hub and enter your password when prompted.

8. Push the image to the repository:

   ```bash theme={null}
   docker push <repository>/<image>:piper-nebius-ui-tutorial
   ```

   This operation can take several minutes to complete.

### Create and deploy the ONNX model by using a Serverless AI job and endpoint

1. Create a fine-tuning job that generates the ONNX model:

   **Web console**

   1. In the web console, go to  **Serverless AI** → **Jobs**.

   2. Click  **Create job**.

   3. On the page that opens, specify the following job parameters:

      * **Configuration**: Custom.

      * **Image path**: `<repository>/<image>:piper-nebius-ui-tutorial`. Set the image that you've pushed to the Docker repository.

      * **Entrypoint command**:

        ```bash theme={null}
        python3 /app/train.py --raw-dir /mnt/data/input/raw --work-dir /tmp/work --output-dir /mnt/data/output --voice-name demo_voice --no-base-ckpt --max-epochs 50 --batch-size 4 --num-workers 0
        ```

        > **Why the command contains exactly these arguments**
        >
        > * `--raw-dir /mnt/data/input/raw`: Matches the uploaded files.
        > * `--work-dir /tmp/work`: Properly saves files to Object Storage.
        > * `--output-dir /mnt/data/output`: Saves the exported ONNX model to the mounted volume.
        > * `--no-base-ckpt`: Helps avoid checkpoint compatibility problems in the dataset path.
        > * `--batch-size 4 --num-workers 0`: Make standard settings for a small dataset.

      * **Computing resources**: Keep the predefined settings.

      * **Mounted volumes**: Click **Attach volume** and select the bucket created earlier.

      * **Mount path**: `/mnt/data`.

   4. Click **Create job**.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius ai job create \
     --name my-job \
     --image <repository>/<image>:piper-nebius-ui-tutorial \
     --container-command python3 \
     --args "/app/train.py --raw-dir /mnt/data/input/raw --work-dir /tmp/work --output-dir /mnt/data/output --voice-name demo_voice --no-base-ckpt --max-epochs 50 --batch-size 4 --num-workers 0" \
     --volume "<bucket_ID>:/mnt/data" \
     --platform gpu-l40s-a \
     --preset 1gpu-8vcpu-32gb \
     --disk-size 250Gi \
     --subnet-id <subnet_ID>
   ```

   The command contains the following parameters:

   * `--name`: Job name.
   * `--image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `--container-command`: Entrypoint command for the job container.
   * `--args`: Arguments to pass to the entrypoint command.
   * `--volume`: Volume to mount to the job container. Specify the ID of the bucket created earlier. To get the bucket ID, run `nebius storage bucket list`.
   * `--platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `--preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `--disk-size`: Size of the job container disk.
   * `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

   **Go SDK**

   Run the following code:

   ```go theme={null}
   trainJobSvc := sdk.Services().Ai().V1().Job()
   trainArgs := "/app/train.py --raw-dir /mnt/data/input/raw " +
       "--work-dir /tmp/work --output-dir /mnt/data/output " +
       "--voice-name demo_voice --no-base-ckpt --max-epochs 50 " +
       "--batch-size 4 --num-workers 0"
   trainJobOp, err := trainJobSvc.Create(
       ctx,
       &ai.CreateJobRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "my-job",
           },
           Spec: &ai.JobSpec{
               Image: "<repository>/<image>:piper-nebius-ui-tutorial",
               ContainerCommand: "python3",
               Args: trainArgs,
               Volumes: []*ai.JobSpec_VolumeMount{
                   {
                       Source: "my-tts-bucket",
                       ContainerPath: "/mnt/data",
                       Mode: ai.JobSpec_VolumeMount_READ_WRITE,
                   },
               },
               Platform: "gpu-l40s-a",
               Preset:   "1gpu-8vcpu-32gb",
               // The CLI defaults to 24 hours.
               Timeout: durationpb.New(24 * time.Hour),
               // The CLI defaults to 16 GiB for GPU platforms.
               ShmSizeBytes: 17179869184,
               Disk: &ai.JobSpec_DiskSpec{
                   Type:      compute.DiskSpec_NETWORK_SSD,
                   SizeBytes: 268435456000,
               },
               SubnetId: "<subnet_ID>",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create job: %w", err)
   }
   if _, err = trainJobOp.Wait(ctx); err != nil {
       return fmt.Errorf("wait for job creation: %w", err)
   }
   ```

   The code sets the following parameters:

   * `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
   * `Metadata.Name`: Job name.
   * `Spec.Image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `Spec.ContainerCommand`: Entrypoint command for the job container.
   * `Spec.Args`: Arguments to pass to the entrypoint command.
   * `Spec.Volumes[].Source`: Volume to mount to the job container. The example uses the name of the `my-tts-bucket` bucket created earlier.
   * `Spec.Volumes[].ContainerPath`: Path where the bucket is mounted in the container.
   * `Spec.Platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `Spec.Preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `Spec.Timeout`: Duration after which the job is canceled if it has not completed.
   * `Spec.Disk.Type`: Disk type for the underlying VM.
   * `Spec.Disk.SizeBytes`: Size of the job container disk in bytes. The example sets 250 GiB.
   * `Spec.SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).

   **Python SDK**

   Run the following code:

   ```python theme={null}
   train_job_service = JobServiceClient(sdk)
   train_args = (
       "/app/train.py --raw-dir /mnt/data/input/raw "
       "--work-dir /tmp/work --output-dir /mnt/data/output "
       "--voice-name demo_voice --no-base-ckpt --max-epochs 50 "
       "--batch-size 4 --num-workers 0"
   )
   train_job_operation = await train_job_service.create(
       CreateJobRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="my-job",
           ),
           spec=JobSpec(
               image="<repository>/<image>:piper-nebius-ui-tutorial",
               container_command="python3",
               args=train_args,
               volumes=[
                   JobSpec__VolumeMount(
                       source="my-tts-bucket",
                       container_path="/mnt/data",
                       mode=JobSpec__VolumeMount__Mode.READ_WRITE,
                   ),
               ],
               platform="gpu-l40s-a",
               preset="1gpu-8vcpu-32gb",
               # The CLI defaults to 24 hours.
               timeout=timedelta(hours=24),
               # The CLI defaults to 16 GiB for GPU platforms.
               shm_size_bytes=17179869184,
               disk=JobSpec__DiskSpec(
                   type=DiskSpec__DiskType.NETWORK_SSD,
                   size_bytes=268435456000,
               ),
               subnet_id="<subnet_ID>",
           ),
       ),
   )
   await train_job_operation.wait()
   ```

   The code sets the following parameters:

   * `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
   * `metadata.name`: Job name.
   * `spec.image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `spec.container_command`: Entrypoint command for the job container.
   * `spec.args`: Arguments to pass to the entrypoint command.
   * `spec.volumes[].source`: Volume to mount to the job container. The example uses the name of the `my-tts-bucket` bucket created earlier.
   * `spec.volumes[].container_path`: Path where the bucket is mounted in the container.
   * `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.timeout`: Duration after which the job is canceled if it has not completed.
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.size_bytes`: Size of the job container disk in bytes. The example sets 250 GiB.
   * `spec.subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).

   **JavaScript SDK**

   Run the following code:

   ```ts theme={null}
   dayjs.extend(duration);
   const trainJobService = new JobService(sdk);
   const trainArgs = "/app/train.py --raw-dir /mnt/data/input/raw " +
     "--work-dir /tmp/work --output-dir /mnt/data/output " +
     "--voice-name demo_voice --no-base-ckpt --max-epochs 50 " +
     "--batch-size 4 --num-workers 0";
   const trainJobOperation = await trainJobService.create(
     CreateJobRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "my-job",
       },
       spec: {
         image: "<repository>/<image>:piper-nebius-ui-tutorial",
         containerCommand: "python3",
         args: trainArgs,
         volumes: [{
           source: "my-tts-bucket",
           containerPath: "/mnt/data",
           mode: JobSpec_VolumeMount_Mode.READ_WRITE,
         }],
         platform: "gpu-l40s-a",
         preset: "1gpu-8vcpu-32gb",
         // The CLI defaults to 24 hours.
         timeout: dayjs.duration(24, "hours"),
         // The CLI defaults to 16 GiB for GPU platforms.
         shmSizeBytes: 17179869184n,
         disk: {
           type: DiskSpec_DiskType.NETWORK_SSD,
           sizeBytes: 268435456000n,
         },
         subnetId: "<subnet_ID>",
       },
     }),
   ).result;
   await trainJobOperation.wait();
   ```

   The code sets the following parameters:

   * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
   * `metadata.name`: Job name.
   * `spec.image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `spec.containerCommand`: Entrypoint command for the job container.
   * `spec.args`: Arguments to pass to the entrypoint command.
   * `spec.volumes[].source`: Volume to mount to the job container. The example uses the name of the `my-tts-bucket` bucket created earlier.
   * `spec.volumes[].containerPath`: Path where the bucket is mounted in the container.
   * `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.timeout`: Duration after which the job is canceled if it has not completed.
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.sizeBytes`: Size of the job container disk in bytes, as a `bigint`. The example sets 250 GiB.
   * `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).

   After the job reaches the `Complete` status, the files `output/model.onnx` and `output/model.onnx.json` are created in the bucket. These files contain the produced model.

2. Deploy the model on a Serverless AI endpoint:

   **Web console**

   1. In the web console, go to  **Serverless AI** → **Endpoints**.

   2. Click  **Create endpoint**.

   3. On the page that opens, specify the following endpoint parameters:

      * **Configuration**: Custom.

      * **Image path**: `<repository>/<image>:piper-nebius-ui-tutorial`. Set the image that you've pushed to the Docker repository.

      * **Ports**: `8000`.

      * **Entrypoint command**:

        ```bash theme={null}
        uvicorn app:app --host 0.0.0.0 --port 8000
        ```

      * **Computing resources**: Keep the predefined settings.

      * **Mounted volumes**: Click **Attach volume** and select the bucket created earlier.

      * **Mount path**: `/mnt/data`.

      * **IP address**: Public static IP.

   4. Click **Create endpoint**.

   **CLI**

   Run the following command:

   ```bash theme={null}
   nebius ai endpoint create \
     --name my-endpoint \
     --image <repository>/<image>:piper-nebius-ui-tutorial \
     --container-port 8000 \
     --container-command uvicorn \
     --args "app:app --host 0.0.0.0 --port 8000" \
     --volume "<bucket_ID>:/mnt/data" \
     --subnet-id <subnet_ID> \
     --public
   ```

   The command contains the following parameters:

   * `--name`: Endpoint name.
   * `--image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `--container-port`: Port on which the application listens in the container.
   * `--container-command`: Entrypoint command for the endpoint container.
   * `--args`: Arguments to pass to the entrypoint command.
   * `--volume`: Volume to mount to the endpoint container. Specify the ID of the bucket created earlier. To get the bucket ID, run `nebius storage bucket list`.
   * `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
   * `--public` (optional): Assigns a public IP address to the endpoint.

   **Go SDK**

   Run the following code:

   ```go theme={null}
   ttsEndpointSvc := sdk.Services().Ai().V1().Endpoint()
   ttsEndpointOp, err := ttsEndpointSvc.Create(
       ctx,
       &ai.CreateEndpointRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "my-endpoint",
           },
           Spec: &ai.EndpointSpec{
               Image: "<repository>/<image>:piper-nebius-ui-tutorial",
               ContainerCommand: "uvicorn",
               Args: "app:app --host 0.0.0.0 --port 8000",
               Ports: []*ai.EndpointSpec_Port{
                   {
                       ContainerPort: 8000,
                       Protocol:      ai.EndpointSpec_Port_HTTP,
                   },
               },
               Volumes: []*ai.EndpointSpec_VolumeMount{
                   {
                       Source: "my-tts-bucket",
                       ContainerPath: "/mnt/data",
                       Mode: ai.EndpointSpec_VolumeMount_READ_WRITE,
                   },
               },
               // The CLI picks a default platform and preset.
               Platform: "gpu-l40s-a",
               Preset:   "1gpu-8vcpu-32gb",
               // The CLI defaults to 16 GiB for GPU platforms.
               ShmSizeBytes: 17179869184,
               // The CLI defaults to 250 GiB.
               Disk: &ai.EndpointSpec_DiskSpec{
                   Type:      compute.DiskSpec_NETWORK_SSD,
                   SizeBytes: 268435456000,
               },
               SubnetId: "<subnet_ID>",
               PublicIp: true,
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create endpoint: %w", err)
   }
   if _, err = ttsEndpointOp.Wait(ctx); err != nil {
       return fmt.Errorf("wait for endpoint creation: %w", err)
   }
   ```

   The code sets the following parameters:

   * `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
   * `Metadata.Name`: Endpoint name.
   * `Spec.Image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `Spec.ContainerCommand`: Entrypoint command for the endpoint container.
   * `Spec.Args`: Arguments to pass to the entrypoint command.
   * `Spec.Ports[].ContainerPort`: Port on which the application listens in the container.
   * `Spec.Ports[].Protocol`: Protocol used by the exposed port. An HTTP port is available through the endpoint's managed HTTPS URL.
   * `Spec.Volumes[].Source`: Volume to mount to the endpoint container. The example uses the name of the `my-tts-bucket` bucket created earlier.
   * `Spec.Volumes[].ContainerPath`: Path where the bucket is mounted in the container.
   * `Spec.Platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `Spec.Preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `Spec.Disk.Type`: Disk type for the underlying VM.
   * `Spec.Disk.SizeBytes`: Size of the endpoint container disk in bytes. The example sets 250 GiB.
   * `Spec.SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).
   * `Spec.PublicIp` (optional): Whether to assign a public IP address to the endpoint.

   **Python SDK**

   Run the following code:

   ```python theme={null}
   tts_endpoint_service = EndpointServiceClient(sdk)
   tts_endpoint_operation = await tts_endpoint_service.create(
       CreateEndpointRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="my-endpoint",
           ),
           spec=EndpointSpec(
               image="<repository>/<image>:piper-nebius-ui-tutorial",
               container_command="uvicorn",
               args="app:app --host 0.0.0.0 --port 8000",
               ports=[
                   EndpointSpec__Port(
                       container_port=8000,
                       protocol=EndpointSpec__Port__Protocol.HTTP,
                   ),
               ],
               volumes=[
                   EndpointSpec__VolumeMount(
                       source="my-tts-bucket",
                       container_path="/mnt/data",
                       mode=EndpointSpec__VolumeMount__Mode.READ_WRITE,
                   ),
               ],
               # The CLI picks a default platform and preset.
               platform="gpu-l40s-a",
               preset="1gpu-8vcpu-32gb",
               # The CLI defaults to 16 GiB for GPU platforms.
               shm_size_bytes=17179869184,
               # The CLI defaults to 250 GiB.
               disk=EndpointSpec__DiskSpec(
                   type=DiskSpec__DiskType.NETWORK_SSD,
                   size_bytes=268435456000,
               ),
               subnet_id="<subnet_ID>",
               public_ip=True,
           ),
       ),
   )
   await tts_endpoint_operation.wait()
   ```

   The code sets the following parameters:

   * `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
   * `metadata.name`: Endpoint name.
   * `spec.image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `spec.container_command`: Entrypoint command for the endpoint container.
   * `spec.args`: Arguments to pass to the entrypoint command.
   * `spec.ports[].container_port`: Port on which the application listens in the container.
   * `spec.ports[].protocol`: Protocol used by the exposed port. An HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.volumes[].source`: Volume to mount to the endpoint container. The example uses the name of the `my-tts-bucket` bucket created earlier.
   * `spec.volumes[].container_path`: Path where the bucket is mounted in the container.
   * `spec.platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.size_bytes`: Size of the endpoint container disk in bytes. The example sets 250 GiB.
   * `spec.subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).
   * `spec.public_ip` (optional): Whether to assign a public IP address to the endpoint.

   **JavaScript SDK**

   Run the following code:

   ```ts theme={null}
   const ttsEndpointService = new EndpointService(sdk);
   const ttsEndpointOperation = await ttsEndpointService.create(
     CreateEndpointRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "my-endpoint",
       },
       spec: {
         image: "<repository>/<image>:piper-nebius-ui-tutorial",
         containerCommand: "uvicorn",
         args: "app:app --host 0.0.0.0 --port 8000",
         ports: [{
           containerPort: 8000,
           protocol: EndpointSpec_Port_Protocol.HTTP,
         }],
         volumes: [{
           source: "my-tts-bucket",
           containerPath: "/mnt/data",
           mode: EndpointSpec_VolumeMount_Mode.READ_WRITE,
         }],
         // The CLI picks a default platform and preset.
         platform: "gpu-l40s-a",
         preset: "1gpu-8vcpu-32gb",
         // The CLI defaults to 16 GiB for GPU platforms.
         shmSizeBytes: 17179869184n,
         // The CLI defaults to 250 GiB.
         disk: {
           type: DiskSpec_DiskType.NETWORK_SSD,
           sizeBytes: 268435456000n,
         },
         subnetId: "<subnet_ID>",
         publicIp: true,
       },
     }),
   ).result;
   await ttsEndpointOperation.wait();
   ```

   The code sets the following parameters:

   * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
   * `metadata.name`: Endpoint name.
   * `spec.image`: Container image to run. Set the image that you've pushed to the Docker repository.
   * `spec.containerCommand`: Entrypoint command for the endpoint container.
   * `spec.args`: Arguments to pass to the entrypoint command.
   * `spec.ports[].containerPort`: Port on which the application listens in the container.
   * `spec.ports[].protocol`: Protocol used by the exposed port. An HTTP port is available through the endpoint's managed HTTPS URL.
   * `spec.volumes[].source`: Volume to mount to the endpoint container. The example uses the name of the `my-tts-bucket` bucket created earlier.
   * `spec.volumes[].containerPath`: Path where the bucket is mounted in the container.
   * `spec.platform`: VM platform for the endpoint. Every endpoint uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `spec.disk.type`: Disk type for the underlying VM.
   * `spec.disk.sizeBytes`: Size of the endpoint container disk in bytes, as a `bigint`. The example sets 250 GiB.
   * `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).
   * `spec.publicIp` (optional): Whether to assign a public IP address to the endpoint.

   Wait until the endpoint reaches the `Running` status.

### Synthesize speech

1. Get the endpoint's managed HTTPS URL:

   **Web console**

   1. In the web console, go to  **Serverless AI** → **Endpoints**.
   2. Open the page of the deployed endpoint.
   3. Copy the managed HTTPS URL (`https://...`) from the **Network** → **Public endpoints** field.

   **CLI**

   ```bash theme={null}
   nebius ai endpoint get <endpoint_ID> --format json \
     | jq -r '.status.public_endpoints[] | select(startswith("https://"))' | head -1
   ```

   To get the endpoint ID, run `nebius ai endpoint list`.

   **Go SDK**

   ```go theme={null}
   getEndpointService := sdk.Services().Ai().V1().Endpoint()
   endpoint, err := getEndpointService.Get(
       ctx,
       &ai.GetEndpointRequest{
           Id: "<endpoint_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("get endpoint: %w", err)
   }
   for _, address := range endpoint.GetStatus().GetPublicEndpoints() {
       if strings.HasPrefix(address, "https://") {
           fmt.Println(address)
           break
       }
   }
   ```

   The code prints the endpoint's managed HTTPS URL.

   To get the endpoint ID, list endpoints and copy the `Metadata.Id` of the required endpoint, as described in [Managing endpoints in Serverless AI](https://docs.nebius.com/serverless/endpoints/manage.md#go-sdk-3).

   **Python SDK**

   ```python theme={null}
   get_endpoint_service = EndpointServiceClient(sdk)
   endpoint = await get_endpoint_service.get(
       GetEndpointRequest(id="<endpoint_ID>"),
   )
   public_endpoint = next(
       (
           address
           for address in endpoint.status.public_endpoints
           if address.startswith("https://")
       ),
       None,
   )
   if public_endpoint is not None:
       print(public_endpoint)
   ```

   The code prints the endpoint's managed HTTPS URL.

   To get the endpoint ID, list endpoints and copy the `metadata.id` of the required endpoint, as described in [Managing endpoints in Serverless AI](https://docs.nebius.com/serverless/endpoints/manage.md#python-sdk-3).

   **JavaScript SDK**

   ```ts theme={null}
   const getEndpointService = new EndpointService(sdk);
   const endpoint = await getEndpointService.get(
     GetEndpointRequest.create({
       id: "<endpoint_ID>",
     }),
   );
   const publicEndpoint = endpoint.status?.publicEndpoints.find(
     (address) => address.startsWith("https://"),
   );
   if (publicEndpoint !== undefined) {
     console.log(publicEndpoint);
   }
   ```

   The code prints the endpoint's managed HTTPS URL.

   To get the endpoint ID, list endpoints and copy the `metadata.id` of the required endpoint, as described in [Managing endpoints in Serverless AI](https://docs.nebius.com/serverless/endpoints/manage.md#javascript-sdk-3).

2. To verify the endpoint health, run a health check:

   ```bash theme={null}
   curl <endpoint_URL>/health
   ```

   Expected output:

   ```text theme={null}
   {"ok":true,"model":"/mnt/data/output/model.onnx","config":"/mnt/data/output/model.onnx.json"}
   ```

   The `"ok":true` message shows that the endpoint is healthy.

3. To synthesize speech, call the endpoint:

   ```bash theme={null}
   curl -X POST "<endpoint_URL>/synthesize" \
      -H "Content-Type: application/json" \
      -d '{"text":"Hello world"}' \
      --output speech.wav
   ```

   The method generates the `speech.wav` file with the recorded `Hello world` phrase.

   The audio quality can be low because only five samples from a dataset were used to train the model. That is expected because the tutorial's purpose is only to showcase the process of the speech synthesis. To improve the audio quality, use a bigger dataset and more samples for the model training.

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources, so Nebius AI Cloud doesn't charge for them:

* [CPU-only VM](https://docs.nebius.com/compute/virtual-machines/delete.md).
* [Boot disk](https://docs.nebius.com/compute/storage/manage.md#how-to-delete-a-volume) attached to the VM.
* [Bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets).
* [Endpoint](https://docs.nebius.com/serverless/endpoints/manage.md#how-to-delete-an-endpoint). When you delete an endpoint, Serverless AI automatically deletes the endpoint VM and container (boot) disk.
