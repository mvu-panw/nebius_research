# Creating and deleting Soperator clusters in Managed Service for Soperator

Source: https://docs.nebius.com/slurm-soperator/managed-soperator/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating and deleting Soperator clusters in Managed Service for Soperator

You can create and manage Soperator clusters in Managed Service for Soperator in the [web console](https://console.nebius.com). A cluster includes login, controller and worker nodes, and provides a full Slurm environment for batch and interactive workloads.

## Prerequisites

* If you need worker nodes with GPUs, make sure that you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md) that reserve GPUs.
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* Generate at least one [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md) to connect to [Slurm login nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#nodes) as the default `root` user.

## How to create a cluster

**Web console**

1. In the sidebar, go to  **AI orchestration** → **Soperator**.

2. Click **Create cluster**.

3. In the **Overview**, configure the cluster's general parameters:

   1. Enter the cluster name.
   2. Add one or more SSH public keys (`ssh-ed25519 AAA***`) to access the login node.

4. Configure node sets. A cluster must have a [login node set](https://docs.nebius.com/slurm-soperator/overview/architecture.md#login-nodes) and at least one [worker node set](https://docs.nebius.com/slurm-soperator/overview/architecture.md#worker-nodes).

   1. For the login node set, specify a number of nodes.
   2. For each worker node set, specify the following:

      * Name.
      * Whether the nodes should use GPUs.
      * [Platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

      - Reservation ID from your [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md).
      - Number of nodes.

      If you already have a worker node set and would like to create another one with the same configuration, next to the worker set, click  → **Clone node set**.

   Each cluster also contains [service nodes](https://docs.nebius.com/slurm-soperator/managed-soperator/service-nodes.md): controller nodes, accounting nodes and Soperator system nodes. They are subject to billing and quotas in the same way as login and worker nodes.

5. Add visible and, optionally, hidden partitions. You can use the default partitions or define your own ones.

   Partitions group nodes into logical (and possibly overlapping) sets and define how workloads are scheduled on those node sets. See details in the [Slurm quickstart on partitions](https://slurm.schedmd.com/quickstart.html#arch).

   In Managed Soperator, hidden partitions are not listed by Slurm CLI tools as available (per the `Hidden` parameter in [slurm.conf](https://slurm.schedmd.com/slurm.conf.html#OPT_Hidden)), but you can create and manage them in the web console and other Nebius AI Cloud interfaces.

   > [!WARNING]
   >
   > Manage partitions only through the web console and other Nebius AI Cloud interfaces. A partition created or changed with `scontrol` inside the cluster is not part of the cluster configuration and is removed the next time Soperator updates the Slurm configuration. For details, see [Cluster specification and Slurm configuration](https://docs.nebius.com/slurm-soperator/overview/architecture.md#cluster-specification-and-slurm-configuration).

   For each partition, specify:

   * [PartitionName](https://slurm.schedmd.com/slurm.conf.html#OPT_PartitionName): A unique partition name that you will use when submitting jobs.
   * [Nodes](https://slurm.schedmd.com/slurm.conf.html#OPT_Nodes_1): The worker node sets that the partition can schedule jobs on. A partition can include one or more node sets, and a node set can belong to more than one partition.
   * [PriorityTier](https://slurm.schedmd.com/slurm.conf.html#OPT_PriorityTier): Determines how Soperator prioritizes partitions when resources are limited. A higher partition priority means that more jobs from this partition are favored for the same resources.
   * [DefaultTime](https://slurm.schedmd.com/slurm.conf.html#OPT_DefaultTime): The default time limit for jobs submitted to the partition, in `HH:MM:SS` format. Jobs inherit this limit unless they have a different time in their submission settings.
   * [DefMemPerNode](https://slurm.schedmd.com/slurm.conf.html#OPT_DefMemPerNode): The default amount of memory available to each node for jobs scheduled in the partition. Must not exceed the node capacity.
   * [PreemptMode](https://slurm.schedmd.com/slurm.conf.html#OPT_PreemptMode): Preemption mode controls what happens to currently running jobs when higher priority jobs require resources.

6. Add volumes. A cluster can include shared, local and memory volumes.

   * **Cluster volumes** are created per cluster and are available to all node sets.
   * **Shared volumes** are created per project and are available to all node sets.
   * **Local volumes** are created per node and store temporary or runtime data.
   * **Memory volumes** store data in RAM. You cannot change them.

   For more information about cluster and shared volumes, see [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md).

7. (Optional) If the selected platform and preset support local SSD disks, enable **Local SSD disks** to add ephemeral local storage to your cluster.

   > [!NOTE]
   >
   > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

8. Review the configuration on the **Review** page and click **Create cluster**.

### What's next

* [Connect to the cluster](https://docs.nebius.com/slurm-soperator/clusters/connect.md).
* To save costs when you are not using the cluster, [stop and start it](https://docs.nebius.com/slurm-soperator/managed-soperator/stop-start.md).

## How to delete a cluster

> [!WARNING]
>
> When you delete a cluster, all data stored on its nodes and volumes is permanently removed. If you want to stop using the cluster temporarily and save costs, see [stop and start it](https://docs.nebius.com/slurm-soperator/managed-soperator/stop-start.md).

1. In the sidebar, go to **Managed Soperator**.
2. In the list of clusters, find the one that you want to delete.
3. Next to the cluster, click  → **Delete**.
4. Enter the cluster name to confirm and click **Delete cluster**.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
