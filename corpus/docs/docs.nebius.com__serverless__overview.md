# About Serverless AI

Source: https://docs.nebius.com/serverless/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# About Serverless AI

Serverless AI is a Nebius AI Cloud service for running containerized AI workloads without creating or managing virtual machines (VMs) or clusters. It supports the full AI/ML development workflow: build prototypes and run experiments in interactive Devlab environments, run training, fine-tuning and data processing workloads as jobs, and serve models and applications through endpoints. Provide a container image or select a template, and Serverless AI provisions the compute and storage resources required for each workload.

Devlabs, endpoints and jobs run on Compute virtual machines, with usage-based, per-second billing. The underlying VMs are managed by Serverless AI. You can connect to them via SSH, but they aren't shown as Compute resources and can't be managed or modified directly like other Compute VMs.

## Devlabs, endpoints and jobs

Serverless AI supports the end-to-end AI/ML workflow through three deployment types. Choose the deployment type that best fits what you want to do:

* **Experiment and prototype**: Write code, explore models and data in a browser-based IDE or notebook → **Devlab**.
* **Run a task to completion**: Train or fine-tune a model, preprocess data, run batch inference or evaluation → **Job**.
* **Serve requests**: Host a model or application at a URL for real-time inference → **Endpoint**.

Rather than providing three separate paths, these deployment types are designed for three stages that most projects move through. You can prototype in a Devlab, submit the working code as a job and then serve the result as an endpoint. Starting with one doesn't prevent you from using the others.

The following table compares the three deployment types:

| | **Devlab** | **Job** | **Endpoint** |
| - | - | - | - |
| **Use cases** | Coding and prototyping in a browser-based IDE or notebook | Preprocessing data, training and fine-tuning models, running batch inference, evaluating models, running scientific simulations | Serving and A/B-testing models, running real-time inference |
| **Workflow** | Interactive development and prototyping; long-lived session that you start and stop | Non-interactive, terminates upon task completion or timeout | Interactive, responds to requests until you terminate it |
| **Stop/start** | Yes | No | Yes |
| **Public URL for requests** | Yes (web UI and declared ports) | No | Yes |
| **Storage** | Data under the workspace path on the container disk persists across stop and restart | Data on the container disk is removed when the job finishes or is deleted | Data on the container disk is removed when you stop or delete the endpoint |
| **Typical lifetime** | Minutes to days | Minutes to days | Hours to days |
| **Guides** | [Getting started with Devlabs](https://docs.nebius.com/serverless/quickstart/devlabs.md) | [Getting started with jobs](https://docs.nebius.com/serverless/quickstart/jobs.md) | [Getting started with endpoints](https://docs.nebius.com/serverless/quickstart/endpoints.md) |

## Observability and debugging

Each Serverless AI deployment (a Devlab, an endpoint or a job) has a [status](https://docs.nebius.com/serverless/lifecycle.md) that indicates the current stage in the lifecycle. You can view its status and logs on the resource page under **Devlabs**, **Jobs** or **Endpoints** in the web console.

Deployments also report GPU and vCPU utilization metrics on the **Metrics** tab of this page. To investigate errors or unexpected outcomes, see [Debugging failed deployments](https://docs.nebius.com/serverless/jobs/failure.md).

For metric definitions and details, see [Monitoring deployments](https://docs.nebius.com/serverless/monitoring.md).

## Pricing and quotas

Serverless AI follows Compute billing and quota rules. Billing depends on whether the deployment is running or stopped:

* While a Devlab, job or endpoint is running, you are billed for its computing resources and storage.
* While a Devlab is stopped, you are billed for the entire container disk, but not for computing resources.
* While an endpoint is stopped, you are not billed for computing resources or storage.

Mounted [Object Storage buckets](https://docs.nebius.com/object-storage/overview.md#buckets) and [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) are billed separately, including when the deployment is stopped.

For more details, see [Pricing and quotas](https://docs.nebius.com/serverless/pricing-quotas.md).

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
