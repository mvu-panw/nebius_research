# Ephemeral nodes in Soperator

Source: https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Ephemeral nodes in Soperator

If you run both training and inference workloads on reserved GPU capacity, you can move nodes between them without taking down the entire Soperator cluster. *Ephemeral nodes* let you release specific worker nodes from a Soperator cluster and reuse the same [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md) for other workloads, such as inference in a separate Managed Service for Kubernetes® cluster.

Without ephemeral nodes, resizing a Soperator cluster to free GPUs for inference usually requires support-assisted operations. That process is slow, does not let you choose which nodes are removed and can interrupt running jobs or cause full-cluster downtime.

Ephemeral nodes help you:

* Reuse reserved GPU capacity across training and inference instead of buying pay-as-you-go capacity when demand shifts.
* Release or add specific worker nodes without stopping the entire Soperator cluster.
* Choose which nodes to deprovision, starting with idle nodes when possible.
* Move capacity on your own schedule, without waiting for support to resize the cluster.

> [!NOTE]
>
> Ephemeral nodes are available in Soperator clusters running version 3.0 or later. Nebius must also enable this feature in your cluster.

## How ephemeral nodes work

Ephemeral nodes rely on a shared [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md). A capacity block reserves a fixed number of GPUs in a region. Workloads that use the same capacity block draw GPUs from that pool.

In the typical setup, you have two Managed Service for Kubernetes clusters that share one capacity block:

* A **training cluster** that runs [Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/managed-soperator/manage.md).
* An **inference cluster** that runs inference workloads in one or more [node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md).

When you deprovision worker nodes in the Soperator cluster, those GPUs are released back to the capacity block. You can then assign them to an inference node group that uses the same capacity block. The reverse flow applies when you move capacity from inference back to training.

> [!NOTE]
>
> Both clusters must use the same capacity block group and GPU platform. If you are not sure how your capacity is set up, check the **Capacity block groups** tab on the **Limits** page in the [web console](https://console.nebius.com) or contact your Nebius manager.

## Deployment scenarios

How you move capacity depends on how your training and inference workloads are deployed. In both cases, GPUs move through the shared capacity block: worker nodes are released from Soperator, then consumed by an inference node group, or the other way around.

### Training and inference in separate Kubernetes clusters

In this scenario, one Managed Service for Kubernetes cluster hosts Soperator for training and a separate cluster hosts inference workloads in one or more node groups. Both clusters use the same capacity block group.

To move capacity in this layout, see [Moving capacity between training and inference workloads](https://docs.nebius.com/slurm-soperator/capacity/move-capacity.md).

### Training and inference in the same Kubernetes cluster

Soperator and inference can also run in different node groups within a single Managed Service for Kubernetes cluster. You still release worker nodes from the Soperator node group and adjust the inference node group size in the same cluster.

To move capacity in this layout, see [Moving capacity between training and inference workloads](https://docs.nebius.com/slurm-soperator/capacity/move-capacity.md).

## Slurm power management commands

In a Soperator cluster with ephemeral nodes enabled, you can provision and deprovision worker nodes with standard Slurm [power management](https://slurm.schedmd.com/power_save.html) commands. Run them from a [login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) after you connect to the cluster.

| Command | Behavior |
| - | - |
| `scontrol power up <node_list>` | Provisions the specified nodes in the Soperator cluster if free GPUs are available in the capacity block. |
| `scontrol power down <node_list>` | For each node, deprovisions the node when it is idle. Without the `asap` flag, power down has lower priority than starting new jobs from the queue, so Slurm may run queued jobs on the node before powering it down. |
| `scontrol power down asap <node_list>` | Same as `power down`, but also [drains](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md#how-to-drain-and-resume-a-node) the nodes so no new jobs are scheduled on them. Slurm waits only for the current job to finish (if any), then deprovisions the node. |
| `scontrol power down force <node_list>` | Deprovisions the nodes immediately and cancels all jobs running on them. |

Replace `<node_list>` in the commands above with a Slurm hostlist of worker node names, for example `worker-10,worker-11`, `worker-[10,11]` or `worker-[0-3,5-8,13],worker-cpu-18`. To check node names and states before you run a command, see [How to monitor job and node statuses in a Soperator cluster](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md).

> [!NOTE]
>
> If `scontrol power` commands do not work, [contact technical support](https://console.nebius.com/support/) and ask to upgrade the cluster to Soperator 3.0 or later and enable ephemeral nodes on the relevant worker node sets.

### Automatic node provisioning

Powered-down ephemeral nodes are automatically provisioned again when queued jobs need them. You can also trigger provisioning by submitting work with `srun` or `sbatch`: for ephemeral `CLOUD` nodes, these commands run `ResumeProgram`, and Soperator creates the corresponding worker Pods if capacity is available.

If you want to release nodes and keep them powered down even when queued jobs target them, also [drain](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md#how-to-drain-and-resume-a-node) the nodes:

```bash theme={null}
scontrol update NodeName=<node_list> State=drain Reason="prevent power up"
```

Use the same Slurm hostlist as in your `power down` command.

## See also

* [Moving capacity between training and inference workloads](https://docs.nebius.com/slurm-soperator/capacity/move-capacity.md)
* [Capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md)
* [Health management of worker nodes in Soperator clusters](https://docs.nebius.com/slurm-soperator/worker-nodes-health.md)
