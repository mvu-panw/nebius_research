# Getting started with Serverless AI jobs: Run nvidia-smi within a job

Source: https://docs.nebius.com/serverless/quickstart/jobs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Serverless AI jobs: Run nvidia-smi within a job

You can use Serverless AI jobs to work with AI models and perform such operations as fine-tuning, scientific simulations, data processing or batch inference.

To get started with jobs, use the example below. It demonstrates how to run `nvidia-smi` in a Serverless AI job. As a result, you receive information about the GPUs of the virtual machine (VM) in which the job is running. In the web console, the **nvidia-smi** quick-start configuration runs the same kind of workload with settings already filled in.

## Prerequisites

**Web console**

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the **Number of virtual machines** (VMs) quota under **Compute**: it should have at least one VM available. If necessary, [increase the quota](https://docs.nebius.com/overview/quotas.md#change-quotas).

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
  ```

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the **Number of virtual machines** (VMs) quota under **Compute**: it should have at least one VM available. If necessary, [increase the quota](https://docs.nebius.com/overview/quotas.md#change-quotas).

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the **Number of virtual machines** (VMs) quota under **Compute**: it should have at least one VM available. If necessary, [increase the quota](https://docs.nebius.com/overview/quotas.md#change-quotas).

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the **Number of virtual machines** (VMs) quota under **Compute**: it should have at least one VM available. If necessary, [increase the quota](https://docs.nebius.com/overview/quotas.md#change-quotas).

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the **Number of virtual machines** (VMs) quota under **Compute**: it should have at least one VM available. If necessary, [increase the quota](https://docs.nebius.com/overview/quotas.md#change-quotas).

**REST API**

* Get an access token to [authenticate to the REST API](https://docs.nebius.com/rest-api/authentication.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the **Number of virtual machines** (VMs) quota under **Compute**: it should have at least one VM available. If necessary, [increase the quota](https://docs.nebius.com/overview/quotas.md#change-quotas).

## Steps

### Run a Serverless AI job

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.
2. Select the **nvidia-smi** quick start card.
   The quick start configuration uses a verified container image and prefilled job settings.
3. Click **Create job**.

**CLI**

Use `nebius ai create` to create a job step by step in the terminal. The command prompts you to enter values to pass as parameters, shows the resulting configuration and then creates the job.

1. Run the following command:

   ```bash theme={null}
   nebius ai job create \
     --name my-job \
     --image nvidia/cuda:13.1.1-runtime-ubuntu24.04 \
     --container-command bash \
     --args "-c nvidia-smi" \
     --platform gpu-l40s-a \
     --preset 1gpu-8vcpu-32gb \
     --timeout 1h \
     --subnet-id <subnet_ID>
   ```

   Alternatively, you can run `nebius ai create` and specify each value step by step with CLI prompts. The command pre-fills the following values:

   * `--name`: Job name.
   * `--image`: Container image to run. In the given example, the [nvidia/cuda:13.1.1-runtime-ubuntu24.04](https://hub.docker.com/layers/nvidia/cuda/13.1.1-runtime-ubuntu24.04/images/sha256-7ced05425d3bdea47c018551ee001f28081dd409efe1283872cd968ad3c1e957) image is used. It contains the Ubuntu 24.04 operating system as well as drivers and other components for GPUs.
   * `--container-command`: Terminal shell for commands to run.
   * `--args`: Arguments for `docker run` to pass to the entrypoint command. The specified arguments require the container to run `nvidia-smi`.
   * `--platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `--preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
   * `--timeout`: Duration after which the job is canceled if it has not completed.
   * `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
2. When the CLI prompts you to select a project, region or subnet, select from the values that are available.
3. Review the resulting configuration, then confirm creation.

**Go SDK**

Run the following code:

```go theme={null}
createJobService := sdk.Services().Ai().V1().Job()
createJobOperation, err := createJobService.Create(
    ctx,
    &ai.CreateJobRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name:     "my-job",
        },
        Spec: &ai.JobSpec{
            Image: "nvidia/cuda:13.1.1-runtime-ubuntu24.04",
            ContainerCommand: "bash",
            Args:             "-c nvidia-smi",
            Timeout:          durationpb.New(time.Hour),
            Platform:         "gpu-l40s-a",
            Preset:           "1gpu-8vcpu-32gb",
            SubnetId:         "<subnet_ID>",
            ShmSizeBytes: 17179869184,
            Disk: &ai.JobSpec_DiskSpec{
                Type: compute.DiskSpec_NETWORK_SSD,
                SizeBytes: 268435456000,
            },
        },
    },
)
if err != nil {
    return fmt.Errorf("create job: %w", err)
}
if _, err = createJobOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for job creation: %w", err)
}
```

In the code, set the following parameters:

* `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
* `Metadata.Name`: Job name.
* `Spec.Image`: Container image to run. In the given example, the [nvidia/cuda:13.1.1-runtime-ubuntu24.04](https://hub.docker.com/layers/nvidia/cuda/13.1.1-runtime-ubuntu24.04/images/sha256-7ced05425d3bdea47c018551ee001f28081dd409efe1283872cd968ad3c1e957) image is used. It contains the Ubuntu 24.04 operating system as well as drivers and other components for GPUs.
* `Spec.ContainerCommand`: Terminal shell for commands to run.
* `Spec.Args`: Arguments for `docker run` to pass to the entrypoint command. The specified arguments require the container to run `nvidia-smi`.
* `Spec.Timeout`: Duration after which the job is canceled if it has not completed, as a Go duration such as `durationpb.New(time.Hour)`.
* `Spec.Platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `Spec.Preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `Spec.SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3).
* `Spec.Disk.Type`: Disk type for the underlying VM.
* `Spec.Disk.SizeBytes`: Disk size in bytes. The example sets 250 GiB.

After `Wait` completes, `createJobOperation.ResourceID()` returns the created job's ID. Save this value because you need it in later steps.

**Python SDK**

Run the following code:

```python theme={null}
create_job_service = JobServiceClient(sdk)
create_job_operation = await create_job_service.create(
    CreateJobRequest(
        metadata=ResourceMetadata(
            parent_id="<project_ID>",
            name="my-job",
        ),
        spec=JobSpec(
            image=(
                "nvidia/cuda:13.1.1-runtime-ubuntu24.04"
            ),
            container_command="bash",
            args="-c nvidia-smi",
            timeout=timedelta(hours=1),
            platform="gpu-l40s-a",
            preset="1gpu-8vcpu-32gb",
            subnet_id="<subnet_ID>",
            shm_size_bytes=17179869184,
            disk=JobSpec__DiskSpec(
                type=DiskSpec__DiskType.NETWORK_SSD,
                size_bytes=268435456000,
            ),
        ),
    ),
)
await create_job_operation.wait()
```

In the code, set the following parameters:

* `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
* `metadata.name`: Job name.
* `spec.image`: Container image to run. In the given example, the [nvidia/cuda:13.1.1-runtime-ubuntu24.04](https://hub.docker.com/layers/nvidia/cuda/13.1.1-runtime-ubuntu24.04/images/sha256-7ced05425d3bdea47c018551ee001f28081dd409efe1283872cd968ad3c1e957) image is used. It contains the Ubuntu 24.04 operating system as well as drivers and other components for GPUs.
* `spec.container_command`: Terminal shell for commands to run.
* `spec.args`: Arguments for `docker run` to pass to the entrypoint command. The specified arguments require the container to run `nvidia-smi`.
* `spec.timeout`: Duration after which the job is canceled if it has not completed, as a Python `timedelta` such as `timedelta(hours=1)`.
* `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `spec.subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3).
* `spec.disk.type`: Disk type for the underlying VM.
* `spec.disk.size_bytes`: Disk size in bytes. The example sets 250 GiB.

After `await create_job_operation.wait()` completes, `create_job_operation.resource_id` returns the created job's ID. Save this value because you need it in later steps.

**JavaScript SDK**

Run the following code:

```ts theme={null}
dayjs.extend(duration);
const jobTimeout = dayjs.duration(1, "hour");
const createJobService = new JobService(sdk);
const createJobOperation = await createJobService.create(
  CreateJobRequest.create({
    metadata: {
      parentId: "<project_ID>",
      name: "my-job",
    },
    spec: {
      image: "nvidia/cuda:13.1.1-runtime-ubuntu24.04",
      containerCommand: "bash",
      args: "-c nvidia-smi",
      timeout: jobTimeout,
      platform: "gpu-l40s-a",
      preset: "1gpu-8vcpu-32gb",
      subnetId: "<subnet_ID>",
      shmSizeBytes: 17179869184n,
      disk: {
        type: DiskSpec_DiskType.NETWORK_SSD,
        sizeBytes: 268435456000n,
      },
    },
  }),
).result;
await createJobOperation.wait();
```

In the code, set the following parameters:

* `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
* `metadata.name`: Job name.
* `spec.image`: Container image to run. In the given example, the [nvidia/cuda:13.1.1-runtime-ubuntu24.04](https://hub.docker.com/layers/nvidia/cuda/13.1.1-runtime-ubuntu24.04/images/sha256-7ced05425d3bdea47c018551ee001f28081dd409efe1283872cd968ad3c1e957) image is used. It contains the Ubuntu 24.04 operating system as well as drivers and other components for GPUs.
* `spec.containerCommand`: Terminal shell for commands to run.
* `spec.args`: Arguments for `docker run` to pass to the entrypoint command. The specified arguments require the container to run `nvidia-smi`.
* `spec.timeout`: Duration after which the job is canceled if it has not completed, as a `dayjs.Duration` such as `dayjs.duration(1, "hour")`.
* `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3).
* `spec.disk.type`: Disk type for the underlying VM.
* `spec.disk.sizeBytes`: Disk size in bytes, as a `bigint`. The example sets 250 GiB.

After `await createJobOperation.wait()` completes, `createJobOperation.resourceId()` returns the created job's ID. Save this value because you need it in later steps.

**REST API**

Send the following request:

```bash theme={null}
curl --request POST \
  --url 'https://api.nebius.cloud/ai/v1/jobs' \
  --header "Authorization: Bearer <access_token>" \
  --header 'Content-Type: application/json' \
  --data '{
    "metadata": {
      "parentId": "<project_ID>",
      "name": "my-job"
    },
    "spec": {
      "image": "nvidia/cuda:13.1.1-runtime-ubuntu24.04",
      "containerCommand": "bash",
      "args": "-c nvidia-smi",
      "platform": "gpu-l40s-a",
      "preset": "1gpu-8vcpu-32gb",
      "timeout": "3600s",
      "subnetId": "<subnet_ID>",
      "disk": {
        "type": "NETWORK_SSD",
        "sizeBytes": 268435456000
      }
    }
  }'

```

In the `Authorization` header, replace `<access_token>` with the access token that you got in the prerequisites.

The request includes the following parameters:

* `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).
* `metadata.name`: Job name.
* `spec.image`: Container image to run. In the given example, the [nvidia/cuda:13.1.1-runtime-ubuntu24.04](https://hub.docker.com/layers/nvidia/cuda/13.1.1-runtime-ubuntu24.04/images/sha256-7ced05425d3bdea47c018551ee001f28081dd409efe1283872cd968ad3c1e957) image is used. It contains the Ubuntu 24.04 operating system as well as drivers and other components for GPUs.
* `spec.containerCommand`: Terminal shell for commands to run.
* `spec.args`: Arguments for `docker run` to pass to the entrypoint command. The specified arguments require the container to run `nvidia-smi`.
* `spec.platform`: VM platform for the job. Every job uses [Compute platforms and presets](https://docs.nebius.com/compute/virtual-machines/types.md).
* `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform.
* `spec.timeout`: Duration after which the job is canceled if it has not completed.
* `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
* `spec.disk.type`: Disk type for the underlying VM.
* `spec.disk.sizeBytes`: Disk size in bytes. The specified value is 250 GiB.

The response returns the job ID in the `resourceId` parameter. Save this value because you need it in later steps.

The job takes several minutes to complete. While the job is running, you can check its status and logs.

### Check the job status and results

> [!NOTE]
>
> Checking job logs is available only in the web console and CLI.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.
2. Next to the job, click **View logs**. Alternatively, select the job that you want to view the logs for and switch to the **Logs** tab.

**CLI**

1. Save the job ID to an environment variable:
   ```bash theme={null}
   export JOB_ID=$(nebius ai job get-by-name --name my-job \
     --format jsonpath='{.metadata.id}')
   ```
2. View information about the job:
   ```bash theme={null}
   nebius ai job get $JOB_ID
   ```
   The command output contains such data as the job status, start and finish times.
3. If the output doesn't indicate that the job has started, wait a few seconds. Next, run the previous command again and check that the job is running now.
4. When the job has started, check its logs:
   ```bash theme={null}
   nebius ai job logs $JOB_ID
   ```
   The logs contain information about the GPUs that `nvidia-smi` provides (in other words, the output of the `nvidia-smi` command).

You can run `nebius ai job get $JOB_ID` and `nebius ai job logs $JOB_ID` multiple times to determine whether the job is complete, and the full output of `nvidia-smi` is returned in logs.

**Go SDK**

Get the job and check the `status.state` value in the printed result:

```go theme={null}
getJobService := sdk.Services().Ai().V1().Job()
job, err := getJobService.Get(
    ctx,
    &ai.GetJobRequest{Id: "<job_ID>"},
)
if err != nil {
    return fmt.Errorf("get job: %w", err)
}
fmt.Println(job)
```

In `ai.GetJobRequest`, set `Id` to the job ID that you saved when you created the job.

If the state doesn't indicate that the job has started, wait a few seconds and run the code again. You can repeat the request until the job reaches the `COMPLETED` state.

**Python SDK**

Get the job and check the `status.state` value in the response:

```python theme={null}
get_job_service = JobServiceClient(sdk)
job = await get_job_service.get(
    GetJobRequest(id="<job_ID>"),
)
print(job)
```

In `GetJobRequest`, set `id` to the job ID that you saved when you created the job.

If the state doesn't indicate that the job has started, wait a few seconds and run the code again. You can repeat the request until the job reaches the `COMPLETED` state.

**JavaScript SDK**

Get the job and check the `status?.state` value in the response:

```ts theme={null}
const getJobService = new JobService(sdk);
const job = await getJobService.get(
  GetJobRequest.create({ id: "<job_ID>" }),
);
console.log(job);
```

In `GetJobRequest`, set `id` to the job ID that you saved when you created the job.

If the state doesn't indicate that the job has started, wait a few seconds and run the code again. You can repeat the request until the job reaches the `COMPLETED` state.

**REST API**

Get the job and check the `status.state` parameter in the response:

```bash theme={null}
curl --request GET \
  --url "https://api.nebius.cloud/ai/v1/jobs/<job_ID>" \
  --header "Authorization: Bearer <access_token>"
```

In the request, specify:

* Your access token in the `Authorization` header.
* In the request path, the job ID returned in the `resourceId` parameter when you created the job.

If the state doesn't indicate that the job has started, wait a few seconds and send the request again. You can repeat the request until the job reaches the `COMPLETED` state.

### (Optional) Delete the job

When the job is complete, Serverless AI automatically releases all allocated computing resources and the container disk of the job. When you delete a completed job, you remove it from the list of Serverless AI jobs.

If you delete a running job, all the resources are released as well.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.
2. Find the job and then click  → **Delete**.
3. In the window that opens, confirm deleting the job.

**CLI**

To delete the job, run the following command:

```bash theme={null}
nebius ai job delete $JOB_ID
```

**Go SDK**

To delete the job, run the following code:

```go theme={null}
deleteJobService := sdk.Services().Ai().V1().Job()
deleteJobOperation, err := deleteJobService.Delete(
    ctx,
    &ai.DeleteJobRequest{Id: "<job_ID>"},
)
if err != nil {
    return fmt.Errorf("delete job: %w", err)
}
if _, err = deleteJobOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for job deletion: %w", err)
}
```

In `ai.DeleteJobRequest`, set `Id` to the job ID that you saved when you created the job.

**Python SDK**

To delete the job, run the following code:

```python theme={null}
delete_job_service = JobServiceClient(sdk)
delete_job_operation = await delete_job_service.delete(
    DeleteJobRequest(id="<job_ID>"),
)
await delete_job_operation.wait()
```

In `DeleteJobRequest`, set `id` to the job ID that you saved when you created the job.

**JavaScript SDK**

To delete the job, run the following code:

```ts theme={null}
const deleteJobService = new JobService(sdk);
const deleteJobOperation = await deleteJobService.delete(
  DeleteJobRequest.create({ id: "<job_ID>" }),
).result;
await deleteJobOperation.wait();
```

In `DeleteJobRequest`, set `id` to the job ID that you saved when you created the job.

**REST API**

To delete the job, send the following request:

```bash theme={null}
curl --request DELETE \
  --url "https://api.nebius.cloud/ai/v1/jobs/<job_ID>" \
  --header "Authorization: Bearer <access_token>"
```

In the request, specify:

* Your access token in the `Authorization` header.
* In the request path, the job ID returned in the `resourceId` parameter when you created the job.
