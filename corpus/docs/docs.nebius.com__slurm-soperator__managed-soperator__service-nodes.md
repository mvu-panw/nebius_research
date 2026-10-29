# Managed Service for Soperator service nodes

Source: https://docs.nebius.com/slurm-soperator/managed-soperator/service-nodes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managed Service for Soperator service nodes

In addition to login and worker nodes that you [create](https://docs.nebius.com/slurm-soperator/managed-soperator/manage.md) in your Managed Service for Soperator clusters, every cluster contains *service nodes* that facilitate the cluster's operation. Service nodes are [billed](https://docs.nebius.com/slurm-soperator/managed-soperator/resources/pricing.md) and count towards [quotas](https://docs.nebius.com/slurm-soperator/managed-soperator/resources/quotas.md) on vCPUs. You cannot configure service nodes.

## Service node types

Managed Soperator service nodes vary by function:

* *Controller nodes* orchestrate Slurm activities, such as job queuing, monitoring node states and allocating resources.
* *Accounting nodes,* also known as *database daemon nodes* or *DBD nodes,* collect accounting information for jobs and job steps that you run in the cluster.
* *Soperator system nodes* host Soperator tools that manage Nebius AI Cloud resources, certificates and telemetry.

For more details about controller and accounting nodes, see [Slurm documentation](https://slurm.schedmd.com/quickstart_admin.html#nodes).

## Service nodes in clusters

Each Managed Soperator cluster contains the following service nodes:

| Type | Number of nodes | Compute per node | Storage per node |
| - | - | - | - |
| Controller nodes | 2 | Non-GPU AMD EPYC Genoa, `8vcpu-32gb` | Network SSD disk, 512 GiB |
| Accounting nodes | 1 | Non-GPU AMD EPYC Genoa, `8vcpu-32gb` | Network SSD disk, 256 GiB; Network SSD IO M3 disk, 1024 GiB |
| Soperator system nodes | 3–5, autoscaled depending on load | Non-GPU AMD EPYC Genoa, `8vcpu-32gb` | Network SSD disk, 512 GiB |

Therefore, for billing and quota purposes, at least the following computing and storage resources are added to login and worker nodes of a cluster:

* Non-GPU AMD EPYC Genoa: 48 vCPUs, 192 GiB RAM
* Network SSD disks: 2816 GiB
* Network SSD IO M3 disk: 1024 GiB
