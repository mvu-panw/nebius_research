# Managing AI workloads across Managed Service for Kubernetes® clusters with SkyPilot

Source: https://docs.nebius.com/3p-integrations/skypilot-mk8s

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing AI workloads across Managed Service for Kubernetes® clusters with SkyPilot

You can use [SkyPilot](https://docs.skypilot.co/en/latest/docs/index.html) as a single, declarative job surface that runs your AI workloads across one or more [Managed Service for Kubernetes](https://docs.nebius.com/kubernetes.md) clusters. SkyPilot picks the best cluster for each job based on hardware availability and the constraints in the task definition, and ensures fault tolerance across clusters when capacity is tight in the preferred one.

The SkyPilot placement logic combines constraint matching with policy:

* With *capability match*, SkyPilot filters clusters by whether they meet the requested hardware and features, such as the GPU model, the number of GPUs per node, InfiniBand™ or a shared filesystem.
* With *capacity chasing*, SkyPilot chases capacity across other clusters or regions when the preferred cluster has insufficient capacity.
* With *failover and retries*, SkyPilot handles provisioning failures, such as preemptions or insufficient capacity, by automatically retrying with other matching clusters.

## Costs

Nebius AI Cloud charges you only for [Managed Kubernetes nodes](https://docs.nebius.com/kubernetes/resources/pricing.md).

## Steps

### Install dependencies

1. Make sure you have Python 3.10 or higher [installed](https://www.python.org/downloads/).

2. Install SkyPilot with Kubernetes and Nebius support:

   ```bash theme={null}
   pip3 install "skypilot[kubernetes,nebius]"
   ```

### Prepare infrastructure

1. Deploy the Managed SkyPilot API Server:

   1. In the Nebius AI Cloud console, go to  **AI orchestration** → **SkyPilot**.
   2. Enter a name for the application or keep the default one.
   3. Select a **Platform** and a **Preset** (vCPUs and RAM) for the API server virtual machine.
   4. Click **Deploy application**.

2. Connect to the SkyPilot API server. On the application page in the web console, click **How to connect** and copy the `sky api login` command. Then run the command in your terminal:

   ```bash theme={null}
   sky api login -e "https://<gateway>.skypilot.gw.msp.<region>.nebius.cloud"
   ```

3. Check that SkyPilot can reach your project:

   ```bash theme={null}
   sky check kubernetes
   ```

   At this stage, no Managed Kubernetes clusters have been added yet, so the output looks similar to the following:

   ```text theme={null}
   Checking credentials to enable infra for SkyPilot.
     Kubernetes: disabled
       Reason [compute]: No available context found in kubeconfig.
   🎉 Enabled infra 🎉
     No infra to check/enabled.
   ```

   You will run the same command again later to confirm that the contexts are picked up.

4. [Create](https://docs.nebius.com/kubernetes/clusters/manage.md) at least one Managed Kubernetes cluster with a GPU node group. To demonstrate cross-cluster fault tolerance, create two or more clusters.

For more information about how to install SkyPilot and connect to it, see [Managing AI workloads on Compute virtual machines with SkyPilot](https://docs.nebius.com/3p-integrations/skypilot.md).

### Add Managed Kubernetes clusters to SkyPilot

The Managed SkyPilot API Server auto-discovers all Managed Kubernetes clusters in the same project. You don't need to add a local kubeconfig or configure a service account.

1. Open the SkyPilot dashboard. On the application page in the web console, click **How to connect** and then click on the public endpoint URL.

2. On the dashboard, go to the **Infra** tab and click **Refresh**.

   The dashboard lists the Managed Kubernetes clusters available to SkyPilot.

3. Verify that SkyPilot can access the clusters:

   ```bash theme={null}
   sky check kubernetes
   ```

   The output lists the enabled contexts:

   ```text theme={null}
   Kubernetes: enabled [compute]
     Allowed contexts:
     ├── <context_1>: enabled.
     └── <context_2>: enabled.
   🎉 Enabled infra 🎉
     Kubernetes [compute]
       Allowed contexts:
       ├── <context_1>
       └── <context_2>
   ```

4. (Optional) For detailed per-cluster and per-node GPU availability, run:

   ```bash theme={null}
   sky show-gpus
   ```

   The output shows the available GPUs and per-node availability:

   ```text theme={null}
   GPU   REQUESTABLE_QTY_PER_NODE  UTILIZATION
   H100  1, 2, 4, 8                24 of 24 free

   Kubernetes per-node GPU availability
   CONTEXT      NODE                       vCPU  Memory (GB)  GPU   GPU UTILIZATION  NODE STATUS
   <context_1>  computeinstance-<VM_ID_1>  -     -            H100  8 of 8 free      Healthy
   <context_1>  computeinstance-<VM_ID_2>  -     -            H100  8 of 8 free      Healthy
   ```

### (Optional) Limit clusters that SkyPilot uses

By default, SkyPilot can place jobs on any Managed Kubernetes cluster it discovers. To restrict SkyPilot to a subset of clusters for every user of this Managed SkyPilot API Server, set `kubernetes.allowed_contexts` in the dashboard:

1. In the SkyPilot dashboard, click **Configuration**.

2. In the **Edit SkyPilot API Server Configuration** textbox, paste the following YAML, listing the contexts in the order in which SkyPilot should evaluate them:

   ```yaml theme={null}
   kubernetes:
     allowed_contexts:
       - <context_1>
       - <context_2>
   ```

3. Click **Apply**.

To verify which contexts are enabled, run `sky check kubernetes` again.

### Run a job

Decide how SkyPilot should choose the target Managed Kubernetes cluster:

* **To let SkyPilot fail over across clusters**, run `sky launch` without specifying a cluster:

  ```bash theme={null}
  sky launch --gpus H100 --infra k8s echo 'Hello World'
  ```

  SkyPilot picks the first context that satisfies the request and submits the job:

  ```text theme={null}
  Considered resources (1 node):
  ----------------------------------------------------------------------------------------------------
   INFRA                       INSTANCE  vCPUs  Mem(GB)  GPUS    COST ($)  CHOSEN
  ----------------------------------------------------------------------------------------------------
   Kubernetes (<context_1>)    -         4      16       H100:1  0.00         ✔
  ----------------------------------------------------------------------------------------------------
  Launching a new cluster 'sky-...'. Proceed? [Y/n]: y
  ```

* **To target a specific Managed Kubernetes cluster**, set `--infra k8s/<context>`:

  ```bash theme={null}
  sky launch --gpus H100 --infra k8s/<context> echo 'Hello World'
  ```

  If the targeted cluster does not have the requested resources, SkyPilot returns an error:

  ```text theme={null}
  sky.exceptions.ResourcesUnavailableError: Kubernetes cluster does not contain any instances satisfying the request: 1x Kubernetes({'H100': 1}, region=<context>).
  To fix: relax or change the resource requirements.
  ```

In the `--gpus` parameter, set the node group [platform](https://docs.nebius.com/compute/virtual-machines/types.md), such as `H100`, `B300` or `L40S`.

Both examples run a Bash command as the entrypoint. You can also pass a YAML task definition instead. For examples, see the [SkyPilot quickstart](https://docs.skypilot.co/en/latest/getting-started/quickstart.html).

### (Optional) Monitor jobs

To list all SkyPilot jobs created during this tutorial and their statuses, run:

```bash theme={null}
sky status
```

To stream the logs of a job, run:

```bash theme={null}
sky logs <task_name>
```

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources, so Nebius AI Cloud doesn't charge for them:

* Delete SkyPilot jobs created during this tutorial:

  ```bash theme={null}
  sky down --all -y
  ```

* [Delete Managed Kubernetes clusters](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-delete-clusters).

* If you no longer need the Managed SkyPilot API Server, delete it in the Nebius AI Cloud console. Go to  **AI orchestration** → **SkyPilot**, open the application, go to the **Settings** tab and click **Delete application**.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
