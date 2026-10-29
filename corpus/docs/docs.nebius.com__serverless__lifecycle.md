# Lifecycle and statuses of Devlabs, endpoints and jobs

Source: https://docs.nebius.com/serverless/lifecycle

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Lifecycle and statuses of Devlabs, endpoints and jobs

Every Serverless AI Devlab, endpoint, and job has a status that indicates its current stage in the lifecycle. You can see the status in the [web console](https://console.nebius.com), or in the `status.state` field returned by the CLI and REST API.

## Devlab statuses

| Status | Description |
| - | - |
| `STATE_UNSPECIFIED` | Serverless AI has not classified the status yet. |
| `PROVISIONING` | The Devlab is being created and its resources, including the requested GPU platform and preset, are being allocated. |
| `STARTING` | Resources are ready and the Devlab is starting up. |
| `IMAGE_PULLING` | The container image is being downloaded. |
| `RUNNING` | The Devlab is up and reachable. Its managed HTTPS URL is available only in this state. |
| `STOPPING` | The Devlab is being stopped. |
| `STOPPED` | The Devlab has been stopped. You can restart it later. |
| `DELETING` | The Devlab is being deleted. |
| `FAILED` | The Devlab failed to start. |
| `ERROR` | The Devlab ran into an error. See [Failed and errored workloads](#failed-and-errored-workloads). |

## Endpoint statuses

| Status | Description |
| - | - |
| `STATE_UNSPECIFIED` | Serverless AI has not classified the status yet. |
| `PROVISIONING` | The endpoint is creating resources. |
| `STARTING` | The endpoint is being started. |
| `IMAGE_PULLING` | The endpoint is pulling the container image. |
| `RUNNING` | The endpoint is running and serving requests. |
| `STOPPING` | The endpoint is being stopped. |
| `STOPPED` | The endpoint has been stopped. You can start it again later. If an endpoint stops with the `Preempted` code, this means that the endpoint was running on a [preemptible virtual machine](https://docs.nebius.com/compute/virtual-machines/preemptible.md), but Nebius AI Cloud has stopped it. |
| `DELETING` | The endpoint is being deleted. |
| `ERROR` | The endpoint could not run because of either a problem with your workload or an internal Serverless AI error. |

## Job statuses

| Status | Description |
| - | - |
| `STATE_UNSPECIFIED` | Serverless AI has not classified the status yet. |
| `PROVISIONING` | The job is creating resources. |
| `STARTING` | The job is being started. |
| `IMAGE_PULLING` | The job is pulling the container image. |
| `RUNNING` | The job is running. |
| `COMPLETED` | The job has successfully completed. |
| `CANCELLING` | The job is being canceled. |
| `CANCELLED` | The job has been canceled. |
| `DELETING` | The job is being deleted. |
| `FAILED` | The job did not complete successfully, for example, because of an error in your code or image, or an exceeded timeout. |
| `ERROR` | An internal Serverless AI error occurred. |

## Typical transitions

When a Devlab or endpoint starts, it moves through the following statuses:

`PROVISIONING` → `STARTING` → `IMAGE_PULLING` → `RUNNING`

When you stop a Devlab and restart it, or stop an endpoint and start it again:

`RUNNING` → `STOPPING` → `STOPPED` → `STARTING` → `IMAGE_PULLING` → `RUNNING`

When a job runs to completion:

`PROVISIONING` → `STARTING` → `IMAGE_PULLING` → `RUNNING` → `COMPLETED`

When you cancel a running job:

`RUNNING` → `CANCELLING` → `CANCELLED`

`IMAGE_PULLING` can be quick enough that the status never surfaces, and a Devlab can return to `STARTING` after it. Read these flows as the statuses a workload can pass through rather than a fixed order.

## Provisioning and capacity

When you create or start a Devlab, endpoint or job, it first enters `PROVISIONING`, during which Serverless AI allocates the resources the workload needs, including the requested GPU platform and preset, and prepares it to run. If the requested capacity is available, `PROVISIONING` completes and the workload moves on to `STARTING` and `RUNNING`.

If the requested capacity is not immediately available, Serverless AI keeps trying for up to 30 minutes; this window doesn't depend on whether the workload uses regular or [preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md) compute. If capacity still is not available within that window, the workload moves on to `ERROR` with the `NotEnoughResources` code (see [FAILED vs. ERROR](#failed-vs-error)) and a message such as:

> Due to high demand, we can't start this workload. Please try to create another one with a different platform or preset.

The workload is not retried automatically. To run it, you can:

* Try a different platform or preset: capacity varies by GPU type and size.
* Try a different region, if your use case allows it.
* Retry a little later, as availability changes over time.

### Devlab specifics

* A Devlab's managed HTTPS URL is available only in the `RUNNING` state. If the managed HTTPS endpoint is enabled, the Devlab stays in `STARTING` until the endpoint is ready, and only then becomes `RUNNING`.
* Unlike jobs and endpoints, Devlabs are not preemptible and have no preempted state.
* `STOPPED` is a normal, resumable state, not a failure: you can restart the Devlab from it.
* If the virtual machine behind a running Devlab is lost, the Devlab reports `STOPPING` and then `STOPPED` with no status details and preserves the workspace disk. You can restart it normally.

## `FAILED` vs. `ERROR`

The `FAILED` and `ERROR` statuses indicate different kinds of problems:

* `FAILED` applies to jobs and Devlabs. For a job, it means the job did not complete successfully, for example, because of an error in your code, an incorrect entrypoint, a missing dependency in the image, or an exceeded timeout. For a Devlab, it means the Devlab failed to start.
* `ERROR` means Serverless AI could not run the workload. For jobs, this indicates an internal Serverless AI error rather than a problem with your workload. Endpoints have no `FAILED` status, so their `ERROR` covers workload problems as well, such as a container that could not start. For Devlabs, `ERROR` covers capacity and infrastructure problems.

To tell these causes apart, check the status details in the [web console](https://console.nebius.com), or the `status.state_details` field in the CLI, before you retry. Its `code` and `message` name the cause. The message wording can change; the `code` is the stable identifier.

For jobs, the `code` can be:

* `StartFailed`: A container that could not start.
* `ContainerFailed`: A workload that exited with a non-zero code.
* `TimeoutExceeded`: A job that ran out of time.
* `NotEnoughResources`: No capacity for the requested platform and preset.

For endpoints, the `code` can be:

| Code | Appears as | What it means | What to do |
| - | - | - | - |
| `NotEnoughResources` | `ERROR` | Capacity for the requested platform or preset is insufficient. | Try a different platform, preset or region, or try again later. |
| `StartFailed` | `ERROR` | The endpoint failed to start. | Verify the container image reference, credentials and parameters. |
| `VMStopped` | `ERROR` | The virtual machine stopped while the endpoint was starting. | Restart the endpoint. |
| `HttpsEndpointFailed` | `ERROR` | The HTTPS endpoint failed to start. | Restart the endpoint. If the problem persists, [contact support](https://console.nebius.com/support/create-ticket). |
| `OperationFailed` | `ERROR` | An operation on the endpoint failed. | Retry the operation. If the problem persists, [contact support](https://console.nebius.com/support/create-ticket). |

For Devlabs, the `code` can be:

| Code | Appears as | What it means | What to do |
| - | - | - | - |
| `NotEnoughResources` | `ERROR` | Capacity for the requested platform or preset is insufficient. | Try a different platform, preset or region, or try again later. |
| `StartFailed` | `FAILED` | The Devlab failed to start. | Verify the container image reference, credentials and parameters. |
| `VMStopped` | `ERROR` | The virtual machine stopped while the Devlab was starting. | Restart the Devlab. |
| `HttpsEndpointFailed` | `ERROR` | The HTTPS endpoint failed to become ready. | Restart the Devlab. If the problem persists, [contact support](https://console.nebius.com/support/create-ticket). |
| `OperationFailed` | `ERROR` | An operation on the Devlab failed. | Retry the operation. If the problem persists, [contact support](https://console.nebius.com/support/create-ticket). |

When the status details are empty, the cause is internal to Serverless AI. Retry your workload, and if the status persists, [contact support](https://console.nebius.com/support/create-ticket). For deeper investigation, see [Debugging failed Devlabs, jobs and endpoints](https://docs.nebius.com/serverless/jobs/failure.md).
