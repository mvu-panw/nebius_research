# Automatic job restarts

Source: https://docs.nebius.com/serverless/jobs/auto-restarts

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatic job restarts

By default, a job runs once and isn't restarted. You can set up a job to be automatically restarted when its container exits with an error.

> [!NOTE]
>
> Automatic restarts aren't available for Serverless AI endpoints.

## Prerequisites

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
  ```

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**REST API**

* Get an access token to [authenticate to the REST API](https://docs.nebius.com/rest-api/authentication.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Configuring automatic restarts

To turn automatic restarts on or off, set the restart policy when you [create the job](https://docs.nebius.com/serverless/jobs/manage.md#how-to-create-a-job). In the CLI, use the `--restart-policy` parameter. In the SDKs and the REST API, use the restart attempts parameter: `Spec.RestartAttempts` in Go, `spec.restart_attempts` in Python and `spec.restartAttempts` in JavaScript and the REST API. The values correspond as follows:

| CLI value | SDK and REST API value | Behavior |
| - | - | - |
| `never` | `0` or omitted | Default. The job runs once. If the container exits with an error, the job is marked as failed and isn't restarted. |
| `on-failure` | `-1`\* (In JavaScript, pass the value as a BigInt, such as -1n.) | If the container exits with a non-zero exit code, Serverless AI automatically restarts it. |

Automatic restarts occur when your container exits with an error while the job is running. They are useful for workloads that can fail transiently and succeed on a retry, for example, a training workload that can resume from a checkpoint after a crash.

For example, to create a job whose container restarts on failure:

**CLI**

```bash theme={null}
nebius ai job create \
  --name my-job \
  ... \
  --restart-policy on-failure
```

Instead of `...`, specify the other job parameters, as described in [How to create a job](https://docs.nebius.com/serverless/jobs/manage.md#cli-2).

**Go SDK**

```go theme={null}
restartJobService := sdk.Services().Ai().V1().Job()
restartJobOperation, err := restartJobService.Create(
    ctx,
    &ai.CreateJobRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name:     "my-job",
        },
        Spec: &ai.JobSpec{
            // ...
            // -1 restarts the container on failure without a limit.
            RestartAttempts: -1,
        },
    },
)
if err != nil {
    return fmt.Errorf("create job with restart policy: %w", err)
}
if _, err = restartJobOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for job with restart policy: %w", err)
}
```

Setting `Spec.RestartAttempts` to `-1` turns automatic restarts on. Instead of `// ...`, specify the other job parameters, as described in [How to create a job](https://docs.nebius.com/serverless/jobs/manage.md#go-sdk-2).

**Python SDK**

```python theme={null}
restart_job_service = JobServiceClient(sdk)
restart_job_operation = await restart_job_service.create(
    CreateJobRequest(
        metadata=ResourceMetadata(
            parent_id="<project_ID>",
            name="my-job",
        ),
        spec=JobSpec(
            # ...
            # -1 restarts the container on failure without a limit.
            restart_attempts=-1,
        ),
    ),
)
await restart_job_operation.wait()
```

Setting `spec.restart_attempts` to `-1` turns automatic restarts on. Instead of `# ...`, specify the other job parameters, as described in [How to create a job](https://docs.nebius.com/serverless/jobs/manage.md#python-sdk-2).

**JavaScript SDK**

```ts theme={null}
dayjs.extend(duration);
const restartJobService = new JobService(sdk);
const restartJobOperation = await restartJobService.create(
  CreateJobRequest.create({
    metadata: {
      parentId: "<project_ID>",
      name: "my-job",
    },
    spec: {
      // ...
      // -1 restarts the container on failure without a limit.
      restartAttempts: -1n,
    },
  }),
).result;
await restartJobOperation.wait();
```

Setting `spec.restartAttempts` to `-1n` turns automatic restarts on. Instead of `// ...`, specify the other job parameters, as described in [How to create a job](https://docs.nebius.com/serverless/jobs/manage.md#javascript-sdk-2).

**REST API**

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
      "restartAttempts": "-1",
      "subnetId": "<subnet_ID>",
      "shmSizeBytes": "17179869184",
      "disk": {
        "type": "NETWORK_SSD",
        "sizeBytes": "268435456000"
      }
    }
  }'
```

In the `Authorization` header, replace `<access_token>` with the access token that you got in the prerequisites.

Setting `spec.restartAttempts` to `"-1"` turns automatic restarts on. For the other parameters, see [How to create a job](https://docs.nebius.com/serverless/jobs/manage.md#rest-api-2).

## When jobs aren't restarted

The restart policy responds only to the container's own exit code. It doesn't recover from:

* **No available capacity at start**: if the requested compute can't be allocated when the job starts.
* **Preemption**: if you run on [preemptible compute](https://docs.nebius.com/compute/virtual-machines/preemptible.md) and Nebius AI Cloud reclaims (preempts) the underlying virtual machine (VM).
* **The underlying VM stopping unexpectedly**.
* **Startup failures and timeouts**.

In these cases, the job moves to the `ERROR` [status](https://docs.nebius.com/serverless/lifecycle.md) and isn't restarted automatically. To run it again, create a new job or restart it, for example with [nebius ai job restart](https://docs.nebius.com/cli/reference/ai/job/restart.md) in the CLI.

> [!TIP]
>
> For resilience against preemption or lost capacity, design your workload to be resumable, for example, write and resume from checkpoints, and resubmit the job rather than relying on automatic restarts.
