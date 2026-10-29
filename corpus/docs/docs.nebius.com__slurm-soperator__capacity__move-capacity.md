# Moving capacity between training and inference workloads

Source: https://docs.nebius.com/slurm-soperator/capacity/move-capacity

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Moving capacity between training and inference workloads

If you share a [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md) between a Soperator cluster and an inference node group, you can move GPU capacity between them without stopping the entire Soperator cluster. The steps below are the same whether training and inference run in [separate Managed Service for Kubernetes clusters](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md#separate-kubernetes-clusters-for-training-and-inference) or in [different node groups within one cluster](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md#training-and-inference-in-the-same-kubernetes-cluster). Use Slurm power management commands to release or add worker nodes in Soperator, and change the inference node group size to consume or free capacity.

For information on how ephemeral nodes work, see [Ephemeral nodes in Soperator](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md).

## Prerequisites

1. [Reserve a capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md) that your Soperator worker nodes and inference node group share.

2. Make sure your Soperator cluster runs version 3.0 or later and has ephemeral nodes enabled. Nebius enables this at cluster provisioning time; when you request the cluster, ask your Nebius manager or [technical support](https://console.nebius.com/support/) to enable ephemeral nodes on the relevant worker node sets. If `scontrol power` commands do not work, ask support to upgrade the cluster or enable ephemeral nodes.

3. Set up an inference [node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups) that uses the same capacity block:

   * **Separate clusters:** [Create a Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) for inference workloads and add a node group to it.
   * **Same cluster:** [Add a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups) for inference workloads to the cluster that already runs Soperator.

4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

5. [Generate an SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md) and set up [access to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) in the Soperator cluster.

## How to move capacity from training to inference

When training nodes are idle but inference needs more GPUs, release nodes from Soperator and add them to the inference node group.

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) in the Soperator cluster.

2. List worker nodes and their states:

   ```bash theme={null}
   sinfo -Nel
   ```

   Choose nodes that are `idle` or that you are ready to drain. See [node states](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md#node-states) for details.

3. Release the chosen nodes from the Soperator cluster:

   * To deprovision nodes when they are idle, use plain `power down`. Without the `asap` parameter, power down has lower priority than starting new jobs from the queue, so Slurm may run queued jobs on the node before powering it down:

     ```bash theme={null}
     scontrol power down <node_list> Reason="move capacity to inference"
     ```

   * To [drain](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md#how-to-drain-and-resume-a-node) nodes so no new jobs are scheduled, wait for the current job to finish (if any), and then deprovision the nodes:

     ```bash theme={null}
     scontrol power down asap <node_list> Reason="move capacity to inference"
     ```

   * To power down nodes immediately and cancel running jobs:

     ```bash theme={null}
     scontrol power down force <node_list> Reason="move capacity to inference"
     ```

   Replace `<node_list>` in the commands above with a Slurm hostlist of worker node names, for example `worker-10,worker-11`, `worker-[10,11]`, or `worker-[0-3,5-8,13],worker-cpu-18`.

4. To prevent the nodes from powering back up automatically when queued jobs target them, [drain](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md#how-to-drain-and-resume-a-node) them:

   ```bash theme={null}
   scontrol update NodeName=<node_list> State=drain Reason="prevent power up"
   ```

   Use the same Slurm hostlist as in the `power down` command. For details, see [Automatic node provisioning](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md#automatic-node-provisioning).

5. Wait until the nodes are powered down. Confirm their state with the following command:

   ```bash theme={null}
   sinfo -N -o "%N %t %E"
   ```

   Powered-down ephemeral nodes remain in the node list with a powered-down cloud state. They no longer run worker Pods.

6. In the Managed Service for Kubernetes cluster that hosts your inference workloads, [increase the inference node group size](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-modify-node-groups) by the same number of nodes you released from Soperator. Use a node group that draws GPUs from the same capacity block group.

The released GPUs are now available to inference workloads.

## How to move capacity from inference to training

When inference traffic drops and you want to run training jobs on idle GPUs, scale down the inference node group and power worker nodes back on in Soperator.

1. In the Managed Service for Kubernetes cluster that hosts your inference workloads, [reduce the inference node group size](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-modify-node-groups) by the number of nodes you want to move to training. Wait until the nodes are removed and the GPUs are released to the capacity block.

2. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) in the Soperator cluster.

3. If you drained the nodes when you released them, resume them:

   ```bash theme={null}
   scontrol update NodeName=<node_list> State=resume
   ```

4. Power on worker nodes in Soperator:

   ```bash theme={null}
   scontrol power up <node_list>
   ```

   Replace `<node_list>` in the command above with a Slurm hostlist of worker node names to bring back, for example `worker-10,worker-11`, `worker-[10,11]`, or `worker-[0-3,5-8,13],worker-cpu-18`. Soperator creates worker Pods for the requested nodes if enough free GPUs remain in the capacity block.
   Alternatively, submit a job with `srun` or `sbatch` that needs those nodes; Slurm may power them on automatically. For details, see [Automatic node provisioning](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md#automatic-node-provisioning).

5. Confirm that the nodes are available for scheduling:

   ```bash theme={null}
   sinfo -N -o "%N %t %E"
   ```

   The powered-on nodes should move toward the `idle` state when they are ready for new jobs.

## See also

* [Ephemeral nodes in Soperator](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md)
* [How to monitor job and node statuses in a Soperator cluster](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md)
* [Creating and modifying Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md)
