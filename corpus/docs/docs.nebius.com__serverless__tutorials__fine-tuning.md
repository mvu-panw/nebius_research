# Fine-tuning a large language model by using a Serverless AI job and Axolotl

Source: https://docs.nebius.com/serverless/tutorials/fine-tuning

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Fine-tuning a large language model by using a Serverless AI job and Axolotl

You can use Serverless AI jobs to work with AI models and perform such operations as fine-tuning, scientific simulations, data processing or batch inference.

The example below demonstrates how to fine-tune the [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) large language model (LLM) with the support of the Low-Rank Adaptation (LoRA). This example also includes [Axolotl](https://axolotl.ai), an open-source tool for fine-tuning. Axolotl provides a [public container image](https://hub.docker.com/r/axolotlai/axolotl), which you deploy in a job and, as a result, run fine-tuning.

For a quick walkthrough of the web console workflow, watch the video below. If you prefer other interfaces or written instructions, follow the steps further down.

[YouTube video player](https://www.youtube.com/embed/ZjD489E0lls)

Visit [Nebius Academy](https://academy.nebius.com/trainer/nebius-ai-cloud-onboarding/lesson/b532ba82-1b87-4d8c-ae82-f99afa32d04d) for video tutorials to help you get started with Nebius AI Cloud.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram) (VMs)
* [Boot disks](https://docs.nebius.com/compute/resources/pricing.md#disks) attached to the VMs
* Used space in Standard storage in an [Object Storage bucket](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data)

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. Install and configure the Nebius AI Cloud CLI and the AWS CLI. Here are the instructions, depending on what tools you have already installed:

* [How to install both CLIs](https://docs.nebius.com/object-storage/quickstart.md#prepare-your-environment)
* [How to install the Nebius AI Cloud CLI only](https://docs.nebius.com/cli/install.md)
* How to [install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI only

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI to upload the configuration file to the bucket.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI to upload the configuration file to the bucket.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI to upload the configuration file to the bucket.

## Steps

### Prepare an Object Storage bucket

To store job results, mount an [Object Storage bucket](https://docs.nebius.com/object-storage/overview.md#buckets) to your job. Serverless AI deletes the job after its completion. Thus, the bucket preserves the job data: checkpoints and LoRA adapter weights of a fine-tuned model.

For visual guidance on creating a bucket and uploading objects in the web console, watch the video below. If you prefer other interfaces or written instructions, follow the steps further down.

[YouTube video player](https://www.youtube.com/embed/Cx7BlL6PdKk)

Visit [Nebius Academy](https://academy.nebius.com/trainer/nebius-ai-cloud-onboarding/lesson/b532ba82-1b87-4d8c-ae82-f99afa32d04d) for video tutorials to help you get started with Nebius AI Cloud.

1. Create a bucket:

   **Web console**

   1. In the [web console](https://console.nebius.com), go to  **Storage** → **Object Storage**.

   2. Click  **Create bucket**.

   3. Specify the `fine-tuning-axolotl` name for the bucket.

   4. In the **Maximum size** field, select **Unlimited**.

      Leave the other settings at their default values.

   5. Click **Create bucket**.

   **CLI**

   ```bash theme={null}
   nebius storage bucket create --name fine-tuning-axolotl
   ```

   **Go SDK**

   ```go theme={null}
   createBucketSvc := sdk.Services().Storage().V1().Bucket()
   bucketOp, err := createBucketSvc.Create(
       ctx,
       &storage.CreateBucketRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "fine-tuning-axolotl",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create bucket: %w", err)
   }
   if _, err = bucketOp.Wait(ctx); err != nil {
       return fmt.Errorf("wait for bucket creation: %w", err)
   }
   ```

   **Python SDK**

   ```python theme={null}
   create_bucket_service = BucketServiceClient(sdk)
   bucket_operation = await create_bucket_service.create(
       CreateBucketRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="fine-tuning-axolotl",
           ),
       ),
   )
   await bucket_operation.wait()
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const createBucketService = new BucketService(sdk);
   const bucketOperation = await createBucketService.create(
     CreateBucketRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "fine-tuning-axolotl",
       },
     }),
   ).result;
   await bucketOperation.wait();
   ```

2. Save the `config.yaml` file specified below. It is required for Axolotl to run fine-tuning.

   ```yaml theme={null}
   base_model: Qwen/Qwen2.5-0.5B

   load_in_4bit: true
   adapter: qlora

   datasets:
     - path: Salesforce/wikitext
       name: wikitext-2-raw-v1
       split: "train[:2000]"
       type: completion
       field: text

   sequence_len: 128
   micro_batch_size: 1
   gradient_accumulation_steps: 1

   learning_rate: 2e-4
   max_steps: 30
   val_set_size: 0
   logging_steps: 5

   output_dir: /workspace/output

   lora_r: 8
   lora_alpha: 16
   lora_dropout: 0.05
   lora_target_modules:
     - q_proj
     - k_proj
     - v_proj
     - o_proj
     - gate_proj
     - up_proj
     - down_proj
   ```

3. Upload this configuration file to the bucket:

   **Web console**

   1. In the web console, go to  **Storage** → **Object Storage**.
   2. Open the page of the `fine-tuning-axolotl` bucket.
   3. Click **Add** → **Object**.
   4. Upload the `config.yaml` file.

   **CLI**

   ```bash theme={null}
   aws s3 cp config.yaml s3://fine-tuning-axolotl/config.yaml
   ```

   The file is stored in the `fine-tuning-axolotl` bucket as the `config.yaml` object.

   Run this command in the directory where `config.yaml` is stored. Alternatively, specify an actual path to the file after `cp`.

   **Go SDK**

   ```bash theme={null}
   aws s3 cp config.yaml s3://fine-tuning-axolotl/config.yaml
   ```

   The file is stored in the `fine-tuning-axolotl` bucket as the `config.yaml` object.

   Run this command in the directory where `config.yaml` is stored. Alternatively, specify an actual path to the file after `cp`.

   **Python SDK**

   ```bash theme={null}
   aws s3 cp config.yaml s3://fine-tuning-axolotl/config.yaml
   ```

   The file is stored in the `fine-tuning-axolotl` bucket as the `config.yaml` object.

   Run this command in the directory where `config.yaml` is stored. Alternatively, specify an actual path to the file after `cp`.

   **JavaScript SDK**

   ```bash theme={null}
   aws s3 cp config.yaml s3://fine-tuning-axolotl/config.yaml
   ```

   The file is stored in the `fine-tuning-axolotl` bucket as the `config.yaml` object.

   Run this command in the directory where `config.yaml` is stored. Alternatively, specify an actual path to the file after `cp`.

### Run a fine-tuning job

Create a job that performs the following actions:

1. Runs an Axolotl container.
2. Mounts the bucket with the prepared configuration file in the read-write mode.
3. Executes fine-tuning.
4. Saves the fine-tuning results to the bucket.

To create and run such a job:

**Web console**

1. In the web console, go to  **Serverless AI** → **Jobs**.

2. Click  **Create job**.

3. In **Configuration**, select **Template**, and then select **Axolotl**.

4. On the page that opens, specify the job name and storage settings, and check the prefilled template settings:

   * **Name**: `fine-tuning-axolotl-qwen-lora`.

   * **Image path**: `docker.io/axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1`.

   * **Entrypoint command**:

     ```bash theme={null}
     bash -c "RUN_ID=run-$(date +%Y%m%d-%H%M%S); axolotl train /workspace/data/config.yaml && mkdir -p /workspace/data/output/$RUN_ID && cp -r /workspace/output/. /workspace/data/output/$RUN_ID"
     ```

   * **Computing resources**: With GPU.

   * **Available platform**: NVIDIA® L40S Intel.

   * **Preset**: 1 GPU — 8 CPUs — 32 GiB RAM.

   * **Container disk**, **Size**: 450 GiB.

   * **Mounted volumes**: Click **Attach volume** and select the `fine-tuning-axolotl` bucket.

   * **Mount path**: `/workspace/data`.

5. Click **Create job**.

**CLI**

Run the following command:

```bash theme={null}
nebius ai job create \
  --name "fine-tuning-axolotl-qwen-lora" \
  --subnet-id "<subnet_ID>" \
  --image docker.io/axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1 \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --disk-size 450Gi \
  --volume "<bucket_ID>:/workspace/data" \
  --container-command bash \
  --args '-c "RUN_ID=run-$(date +%Y%m%d-%H%M%S); axolotl train /workspace/data/config.yaml && mkdir -p /workspace/data/output/$RUN_ID && cp -r /workspace/output/. /workspace/data/output/$RUN_ID"'
```

The command contains the following parameters:

* `--name`: Job name.

* `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

* `--image`: Container image to run. In the given example, the [public Axolotl container image](https://hub.docker.com/r/axolotlai/axolotl) is used.

* `--platform`: Virtual machine (VM) platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).

* `--preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.

* `--disk-size`: Size of the job container disk.

* `--volume`: Volume to mount to the job container. Specify the ID of the `fine-tuning-axolotl` bucket created earlier. The bucket is used to store the job results and checkpoints.

  To get the bucket ID, run `nebius storage bucket get-by-name --name fine-tuning-axolotl`.

* `--container-command`: Entrypoint command for the job container.

* `--args`: Arguments for `docker run` to pass to the entrypoint command.

**Go SDK**

Run the following code:

```go theme={null}
createJobSvc := sdk.Services().Ai().V1().Job()
createJobOp, err := createJobSvc.Create(
    ctx,
    &ai.CreateJobRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name: "fine-tuning-axolotl-qwen-lora",
        },
        Spec: &ai.JobSpec{
            Image: "docker.io/axolotlai/" +
                "axolotl:main-20260309-py3.11-cu128-2.9.1",
            ContainerCommand: "bash",
            Args: "-c \"RUN_ID=run-$(date +%Y%m%d-%H%M%S); " +
                "axolotl train /workspace/data/config.yaml && " +
                "mkdir -p /workspace/data/output/$RUN_ID && " +
                "cp -r /workspace/output/. " +
                "/workspace/data/output/$RUN_ID\"",
            Platform: "gpu-l40s-a",
            Preset:   "1gpu-8vcpu-32gb",
            SubnetId: "<subnet_ID>",
            Timeout: durationpb.New(24 * time.Hour),
            ShmSizeBytes: 17179869184,
            Disk: &ai.JobSpec_DiskSpec{
                Type: compute.DiskSpec_NETWORK_SSD,
                SizeBytes: 483183820800,
            },
            Volumes: []*ai.JobSpec_VolumeMount{
                {
                    Source: "fine-tuning-axolotl",
                    ContainerPath: "/workspace/data",
                    Mode: ai.JobSpec_VolumeMount_READ_WRITE,
                },
            },
        },
    },
)
if err != nil {
    return fmt.Errorf("create job: %w", err)
}
if _, err = createJobOp.Wait(ctx); err != nil {
    return fmt.Errorf("wait for job creation: %w", err)
}
```

The code sets the following parameters:

* `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
* `Metadata.Name`: Job name.
* `Spec.SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).
* `Spec.Image`: Container image to run. In the given example, the [public Axolotl container image](https://hub.docker.com/r/axolotlai/axolotl) is used.
* `Spec.Platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `Spec.Preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `Spec.Disk.SizeBytes`: Size of the job container disk.
* `Spec.Volumes[].Source`: Volume to mount to the job container. The example uses the name of the `fine-tuning-axolotl` bucket created earlier. The bucket is used to store the job results and checkpoints.
* `Spec.Volumes[].ContainerPath`: Path where the bucket is mounted in the container. Axolotl reads the configuration file from this path.
* `Spec.ContainerCommand`: Entrypoint command for the job container.
* `Spec.Args`: Arguments for `docker run` to pass to the entrypoint command.

**Python SDK**

Run the following code:

```python theme={null}
create_job_service = JobServiceClient(sdk)
create_job_operation = await create_job_service.create(
    CreateJobRequest(
        metadata=ResourceMetadata(
            parent_id="<project_ID>",
            name="fine-tuning-axolotl-qwen-lora",
        ),
        spec=JobSpec(
            image=(
                "docker.io/axolotlai/axolotl:"
                "main-20260309-py3.11-cu128-2.9.1"
            ),
            container_command="bash",
            args=(
                '-c "RUN_ID=run-$(date +%Y%m%d-%H%M%S); '
                "axolotl train /workspace/data/config.yaml && "
                "mkdir -p /workspace/data/output/$RUN_ID && "
                "cp -r /workspace/output/. "
                '/workspace/data/output/$RUN_ID"'
            ),
            platform="gpu-l40s-a",
            preset="1gpu-8vcpu-32gb",
            subnet_id="<subnet_ID>",
            timeout=timedelta(hours=24),
            shm_size_bytes=17179869184,
            disk=JobSpec__DiskSpec(
                type=DiskSpec__DiskType.NETWORK_SSD,
                size_bytes=483183820800,
            ),
            volumes=[
                JobSpec__VolumeMount(
                    source="fine-tuning-axolotl",
                    container_path="/workspace/data",
                    mode=(
                        JobSpec__VolumeMount__Mode.READ_WRITE
                    ),
                ),
            ],
        ),
    ),
)
await create_job_operation.wait()
```

The code sets the following parameters:

* `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
* `metadata.name`: Job name.
* `spec.subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).
* `spec.image`: Container image to run. In the given example, the [public Axolotl container image](https://hub.docker.com/r/axolotlai/axolotl) is used.
* `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `spec.disk.size_bytes`: Size of the job container disk.
* `spec.volumes[].source`: Volume to mount to the job container. The example uses the name of the `fine-tuning-axolotl` bucket created earlier. The bucket is used to store the job results and checkpoints.
* `spec.volumes[].container_path`: Path where the bucket is mounted in the container. Axolotl reads the configuration file from this path.
* `spec.container_command`: Entrypoint command for the job container.
* `spec.args`: Arguments for `docker run` to pass to the entrypoint command.

**JavaScript SDK**

Run the following code:

```ts theme={null}
dayjs.extend(duration);
const createJobService = new JobService(sdk);
const createJobOperation = await createJobService.create(
  CreateJobRequest.create({
    metadata: {
      parentId: "<project_ID>",
      name: "fine-tuning-axolotl-qwen-lora",
    },
    spec: {
      image: "docker.io/axolotlai/axolotl:" +
        "main-20260309-py3.11-cu128-2.9.1",
      containerCommand: "bash",
      args: '-c "RUN_ID=run-$(date +%Y%m%d-%H%M%S); ' +
        "axolotl train /workspace/data/config.yaml && " +
        "mkdir -p /workspace/data/output/$RUN_ID && " +
        "cp -r /workspace/output/. " +
        '/workspace/data/output/$RUN_ID"',
      platform: "gpu-l40s-a",
      preset: "1gpu-8vcpu-32gb",
      subnetId: "<subnet_ID>",
      timeout: dayjs.duration(24, "hours"),
      shmSizeBytes: 17179869184n,
      disk: {
        type: DiskSpec_DiskType.NETWORK_SSD,
        sizeBytes: 483183820800n,
      },
      volumes: [{
        source: "fine-tuning-axolotl",
        containerPath: "/workspace/data",
        mode: JobSpec_VolumeMount_Mode.READ_WRITE,
      }],
    },
  }),
).result;
await createJobOperation.wait();
```

The code sets the following parameters:

* `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
* `metadata.name`: Job name.
* `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).
* `spec.image`: Container image to run. In the given example, the [public Axolotl container image](https://hub.docker.com/r/axolotlai/axolotl) is used.
* `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `spec.disk.sizeBytes`: Size of the job container disk, as a `bigint`.
* `spec.volumes[].source`: Volume to mount to the job container. The example uses the name of the `fine-tuning-axolotl` bucket created earlier. The bucket is used to store the job results and checkpoints.
* `spec.volumes[].containerPath`: Path where the bucket is mounted in the container. Axolotl reads the configuration file from this path.
* `spec.containerCommand`: Entrypoint command for the job container.
* `spec.args`: Arguments for `docker run` to pass to the entrypoint command.

The job takes several minutes to complete.

### Check the job results

1. View information about the job:

   **Web console**

   In the web console, go to  **Serverless AI** → **Jobs** and then open the page of the `fine-tuning-axolotl-qwen-lora` job. It contains information about the job state and configuration.

   **CLI**

   ```bash theme={null}
   nebius ai job get <job_ID>
   ```

   The command output shows the job state and configuration.

   To get the job ID, run `nebius ai job get-by-name --name fine-tuning-axolotl-qwen-lora`.

   **Go SDK**

   ```go theme={null}
   getJobSvc := sdk.Services().Ai().V1().Job()
   jobResult, err := getJobSvc.Get(
       ctx,
       &ai.GetJobRequest{Id: "<job_ID>"},
   )
   if err != nil {
       return fmt.Errorf("get job: %w", err)
   }
   fmt.Println(jobResult)
   ```

   The printed result shows the job state and configuration.

   To get the job ID, call `GetByName` on the job service with `ParentId` set to the project ID and `Name` set to `fine-tuning-axolotl-qwen-lora`, then read `Metadata.Id` from the response.

   **Python SDK**

   ```python theme={null}
   get_job_service = JobServiceClient(sdk)
   job_result = await get_job_service.get(
       GetJobRequest(id="<job_ID>"),
   )
   print(job_result)
   ```

   The printed result shows the job state and configuration.

   To get the job ID, call `get_by_name` on the job service with `parent_id` set to the project ID and `name` set to `fine-tuning-axolotl-qwen-lora`, then read `metadata.id` from the response.

   **JavaScript SDK**

   ```ts theme={null}
   const getJobService = new JobService(sdk);
   const jobResult = await getJobService.get(
     GetJobRequest.create({ id: "<job_ID>" }),
   );
   console.log(jobResult);
   ```

   The printed result shows the job state and configuration.

   To get the job ID, call `getByName` on the job service with `parentId` set to the project ID and `name` set to `fine-tuning-axolotl-qwen-lora`, then read `metadata.id` from the response.

2. Download LoRA adapter weights of the fine-tuning job. They are stored as files in the `output` directory, in the `fine-tuning-axolotl` bucket. To check these files, open the page of the `fine-tuning-axolotl` bucket in the [web console](https://console.nebius.com/).

   **Web console**

   To download a file, in its line, click  → **Download**.

   **CLI**

   Command example for downloading a file:

   ```bash theme={null}
   aws s3 cp s3://fine-tuning-axolotl/output/run-20260309-160510/checkpoint-30/adapter_config.json download/output/run-20260309-160510/checkpoint-30/adapter_config.json
   ```

   In this example, the `s3://...` path points to the file in the bucket, and the `download/...` path points to a local `download` directory.

   **Go SDK**

   Command example for downloading a file:

   ```bash theme={null}
   aws s3 cp s3://fine-tuning-axolotl/output/run-20260309-160510/checkpoint-30/adapter_config.json download/output/run-20260309-160510/checkpoint-30/adapter_config.json
   ```

   In this example, the `s3://...` path points to the file in the bucket, and the `download/...` path points to a local `download` directory.

   **Python SDK**

   Command example for downloading a file:

   ```bash theme={null}
   aws s3 cp s3://fine-tuning-axolotl/output/run-20260309-160510/checkpoint-30/adapter_config.json download/output/run-20260309-160510/checkpoint-30/adapter_config.json
   ```

   In this example, the `s3://...` path points to the file in the bucket, and the `download/...` path points to a local `download` directory.

   **JavaScript SDK**

   Command example for downloading a file:

   ```bash theme={null}
   aws s3 cp s3://fine-tuning-axolotl/output/run-20260309-160510/checkpoint-30/adapter_config.json download/output/run-20260309-160510/checkpoint-30/adapter_config.json
   ```

   In this example, the `s3://...` path points to the file in the bucket, and the `download/...` path points to a local `download` directory.

## How to delete the created resources

Used space in the created bucket is chargeable. If you don't need it, [delete the bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets), so Nebius AI Cloud doesn't charge for it.

## See also

* [Axolotl quickstart](https://docs.axolotl.ai/docs/getting-started.html)
* [Example: Fine-Tune Qwen3 14B with Axolotl](https://docs.axolotl.ai/examples/colab-notebooks/colab-axolotl-example.html)
* [Axolotl GitHub repository](https://github.com/axolotl-ai-cloud/axolotl)
