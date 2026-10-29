# Health management of worker nodes in Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/worker-nodes-health

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Health management of worker nodes in Soperator clusters

Soperator has built-in health checks that continuously monitor the fleet of worker nodes in your cluster, and an auto-healing system that isolates and replaces broken nodes. When deployed in Nebius AI Cloud (Managed Service for Soperator or Pro Solution for Soperator), Soperator also relies on maintenance events from the Compute service and Kubernetes® to auto-heal worker nodes. You can also use custom health checks to run additional checks on worker nodes.

## Health management in Soperator

### Built-in health checks

For all deployment types, Soperator runs built-in health checks on a schedule for each worker node with GPUs. Most of these checks are considered critical: if a worker node fails a critical check, Soperator marks it as requiring further action. Critical checks include, but are not limited to, the following checks:

* GPU checks:

  * [AllReduce](https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md#allreduce), an [NCCL test](https://github.com/NVIDIA/nccl-tests/tree/master) (with and without InfiniBand™, outside and inside Docker containers)
  * [CUDA samples](https://github.com/NVIDIA/cuda-samples), such as [vectorAdd](https://github.com/NVIDIA/cuda-samples/blob/master/Samples/0_Introduction/vectorAdd), [simpleMultiGPU](https://github.com/NVIDIA/cuda-samples/tree/master/Samples/0_Introduction/simpleMultiGPU), [deviceQuery](https://github.com/NVIDIA/cuda-samples/blob/master/Samples/1_Utilities/deviceQuery) and [p2pBandwidthLatencyTest](https://github.com/NVIDIA/cuda-samples/tree/master/Samples/5_Domain_Specific/p2pBandwidthLatencyTest)
  * [NVIDIA® Data Center GPU Manager](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html) (DCGM) diagnostics
  * GPU stress test

* RAM checks: bandwidth and latency

For technical details and the full list of checks, see these resources in the Soperator repository on GitHub:

* [Active Checks – Health and system checks framework](https://github.com/nebius/soperator/blob/main/docs/active-checks.md): description of checks' architecture and implementation
* `soperator-activechecks` Helm chart:

  * [values.yaml](https://github.com/nebius/soperator/blob/main/helm/soperator-activechecks/values.yaml): list of checks
  * [scripts/](https://github.com/nebius/soperator/tree/main/helm/soperator-activechecks/scripts): scripts for each check

### Node isolation

When a critical check fails, Soperator performs the *extensive check procedure*:

1. Drains the node, waiting for running Slurm jobs to finish. The drain reason has the `[node_problem]` prefix.
2. Moves the node into the *suspicious reservation*, preventing new jobs from being scheduled on it.
3. Runs extensive checks on the node, which include hardware-level tests and re-runs of most critical checks.

### Node replacement

If the extensive checks fail, Soperator drains the node. The drain reason now has the `[hardware_problem]` prefix — Soperator marks all worker nodes with this prefix as unhealthy Kubernetes nodes, which triggers automatic re-creation of the node.

If the node passes the extensive checks, Soperator removes it from the suspicious reservation, and jobs can run on the node again.

In Managed Service for Soperator and Pro Solution for Soperator, Compute may schedule maintenance for an underlying virtual machine (VM) of the worker node during the extensive check procedure. This typically indicates a hardware issue already detected by Compute. In this case, Soperator immediately stops the checks, and then drains and recreates the node.

### Custom health checks (Slurm prolog and epilog programs)

All Soperator deployment types support Slurm *prolog and epilog programs* for job steps. You can configure them by using `--task-prolog` and `--task-epilog` parameters of `srun`, either in [batch scripts](https://docs.nebius.com/slurm-soperator/jobs/index.md) or in direct `srun` calls. The prolog and epilog programs specified in `--task-prolog` and `--task-epilog` run on each worker node before and after the job step that is launched by the `srun` call. You can use them to run custom health checks on worker nodes.

> For example, you can run `nvidia-smi` before and after the training step in your batch script (`my_ml_job.sh`) to check the GPU utilization and health:
>
> ```bash title="my_ml_job.sh" highlight={5} theme={null}
> #!/bin/bash
>
> <batch_script_setup>  # Directives, preparation steps, etc.
>
> srun --cpus-per-task=16 --task-prolog="/mnt/checks/smi.sh" --task-epilog="/mnt/checks/smi.sh" python train.py
> ```
>
> ```bash title="/mnt/checks/smi.sh" theme={null}
> #!/bin/bash
>
> nvidia-smi
> ```

For more details about prolog and epilog programs, see [Slurm documentation](https://slurm.schedmd.com/prolog_epilog.html).

By default, Soperator doesn't auto-heal worker nodes that fail custom health checks. To set up custom auto-healing in your Managed Soperator or Pro Solution for Soperator clusters, [contact support](https://console.nebius.com/support/create-ticket) or your personal manager.

## Upstream health checks in Managed Soperator

In Managed Soperator, worker nodes are Compute virtual machines that serve as nodes in a Managed Service for Kubernetes cluster. Both Compute and Managed Kubernetes run their own health checks on worker nodes with GPUs, and Managed Soperator uses these health checks to automatically heal worker nodes, in addition to the [built-in health management system](#health-management-in-soperator).

### Compute

Compute continuously monitors hardware problems on VMs. When such a problem is detected on a VM, Compute [issues a maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md) for it.

If a VM with a maintenance event is associated with a GPU worker node in a Managed Soperator cluster, Managed Soperator drains the node, waiting for running Slurm jobs to finish, and then re-creates the node.

### Kubernetes

When Managed Service for Kubernetes signals a Kubernetes-specific maintenance condition that was not triggered by Compute, Managed Soperator drains the worker node, waiting for running Slurm jobs to finish, and then restarts the node.

For more details about maintenance events and automatic recovery of nodes, see [Managed Kubernetes documentation](https://docs.nebius.com/kubernetes/maintenance/index.md).

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
