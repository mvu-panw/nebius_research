# Soperator cluster architecture

Source: https://docs.nebius.com/slurm-soperator/overview/architecture

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Soperator cluster architecture

Soperator deploys Slurm to Kubernetes® clusters. In a Soperator cluster, Slurm nodes, storage and other components are Kubernetes resources: Pods, PersistentVolumes, etc.

The diagram below outlines the architecture of a Soperator cluster:

![soperator-architecture](https://mintcdn.com/nebius-ai-cloud/1Ha0sWR6e1mnIaHS/_assets/slurm-soperator/soperator-arch.svg?fit=max\&auto=format\&n=1Ha0sWR6e1mnIaHS\&q=85\&s=3e8b01d9a537b075dd8b2c0393d47f4e)

## Cluster specification and Slurm configuration

When Soperator is installed in a Kubernetes cluster, it adds the SlurmCluster [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) to it. This resource contains the specification of the Soperator cluster deployed in the Kubernetes cluster. The Slurm operator itself is a Pod that uses the SlurmCluster specification to create and reconcile the Kubernetes resources in the Soperator cluster, such as login, worker and controller nodes, and storage resources.

The configuration files of Slurm itself (`slurm.conf`, `gres.conf`, `cgroup.conf`, `plugstack.conf`, etc.) are [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) controlled by the Slurm operator. The operator renders them from the SlurmCluster specification and writes them to the shared root filesystem of the cluster, where every node reads them from `/etc/slurm`.

> [!WARNING]
>
> Configuration changes made with `scontrol` or by editing files in `/etc/slurm` are not persistent: the operator rewrites the Slurm configuration from the SlurmCluster specification on every update. To make a change permanent, change the SlurmCluster specification: in Managed Soperator, use the web console or other Nebius AI Cloud interfaces; in Pro Solution for Soperator, [contact support](https://console.nebius.com/support/create-ticket). For details, see [Slurm configuration](https://github.com/nebius/soperator/blob/main/docs/slurm-configuration.md) in the Soperator repository.

## Nodes

In Soperator clusters, all Slurm nodes are Kubernetes Pods. The main [types of Slurm nodes](https://slurm.schedmd.com/quickstart_admin.html#nodes) in Soperator clusters are the following:

* [Login nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#login-node) provide users with access to the cluster.
* [Worker nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#worker-node) execute Slurm jobs.
* [Controller nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#controller-node) manage scheduling and orchestration.

For simplicity, there are nodes that are not represented on the diagram in this article, for example, [DBD (database daemon) nodes](https://slurm.schedmd.com/quickstart_admin.html#dbd) for accounting, nodes that export metrics, nodes that other Kubernetes operators manage for backups and auto-healing.

### Login nodes

To work with a Slurm (submit jobs, check their status, write `sbatch` scripts and prepare data for them, etc.), users connect to its *login nodes*. The `sshd` daemon runs on every login node.

Soperator balances load between login nodes — each time a user connects to the cluster via SSH, they are directed to a random login node.

### Worker nodes

*Worker nodes*, also known as *compute nodes*, perform computations for Slurm jobs. The [slurmd](https://slurm.schedmd.com/slurmd.html) daemon runs on every worker node. It monitors, launches and terminates jobs.

For more information on how to work with login and worker nodes, see [Connecting to login and worker nodes](https://docs.nebius.com/slurm-soperator/clusters/connect.md).

### Controller nodes

*Controller nodes* orchestrate Slurm activities, such as job queuing, monitoring node states and allocating resources. The central management daemon, [slurmctld](https://slurm.schedmd.com/slurmctld.html), runs on all controller nodes.

## Persistent storage

Soperator's main storage feature is its *shared root filesystem*. It is mounted to all login and worker nodes in a special way — you see it as the root directory (`/`) in your SSH sessions and Slurm jobs. This helps maintain the traditional Slurm user experience where you work with the entire root filesystem on each node.

The filesystem is shared, which means you do not need to keep it identical across nodes manually. When you make changes to the filesystem on one node, these changes automatically show up on other nodes.

The shared root filesystem is implemented as a Kubernetes [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) (PV) that ensures data is preserved when nodes restart.

Soperator also uses PVs for system needs, like storing cluster and controller states, etc.

## Ephemeral storage

[Local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) are available on [supported platforms, presets and regions](https://docs.nebius.com/compute/storage/local-disks.md#availability). Unlike the shared root filesystem, local SSD disks are added to an individual node and are not shared across the cluster.

Use local SSD disks for data that can be recreated and benefits from high performance and low latency, such as scratch space, caches and intermediate files created by Slurm jobs. For durable or shared data, consider using persistent storage.

## See also

For more information about the Soperator cluster architecture, see:

* [Architecture](https://github.com/nebius/soperator/blob/dev/docs/architecture.md) in Soperator's GitHub repository.
* [Explaining Soperator, Nebius' open-source Kubernetes operator for Slurm](https://nebius.com/blog/posts/soperator-in-open-source-explained) in the Nebius blog.
