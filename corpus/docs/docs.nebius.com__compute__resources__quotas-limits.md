# Quotas in Compute

Source: https://docs.nebius.com/compute/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas in Compute

Compute has quotas on virtual machines (VMs), storage and InfiniBand™ usage.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

## Virtual machines

A VM and its resources count towards the quotas throughout the VM's lifecycle, from its creation to deletion, regardless of whether it is running or stopped.

These quotas apply to Compute VMs and also to Managed Service for Soperator and Managed Service for Kubernetes® nodes, which are based on Compute VMs.

Compute has different quotas for GPU and non-GPU virtual machines.

### GPU virtual machines

The default quota values depend on the [region](https://docs.nebius.com/overview/regions.md) in which you create GPU VMs. Private regions are marked with <sup>\*</sup>.

| Quota name | Default value, `eu-north1` | Default value, `eu-west1` | Default value, `me-west1` | Default value, `us-central1` | Default value, `uk-south1` | Default value, `uk-south2` | Default value, `eu-north2`\* | Default value, `eu-south1` | Default value, `eu-west2` | Default value, `us-north1` |
| - | - | - | - | - | - | - | - | - | - | - |
| [Regular VMs](https://docs.nebius.com/compute/virtual-machines/manage.md) | 12 | 12 | 12 | 12 | 12 | 12 | 0 | 12 | 12 | 12 |
| [Preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) | 8 | 8 | 8 | 8 | 8 | 8 | 0 | 8 | 8 | 8 |
| Total number of NVIDIA® B300 GPUs for regular VMs without reservations | *N/A* | *N/A* | *N/A* | *N/A* | 32 | *N/A* | *N/A* | *N/A* | 32 | 32 |
| Total NVIDIA® B200 GPUs for regular VMs without reservations | *N/A* | *N/A* | 0 | 0 | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* |
| Total NVIDIA® H200 GPUs for regular VMs without reservations | 32 | 8 | *N/A* | 0 | *N/A* | *N/A* | 0 | *N/A* | *N/A* | *N/A* |
| Total NVIDIA® H100 GPUs for regular VMs without reservations | 32 | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* |
| Total NVIDIA® RTX PRO™ 6000 GPUs for regular VMs without reservations | *N/A* | *N/A* | *N/A* | 0 | *N/A* | 32 | *N/A* | 32 | *N/A* | *N/A* |
| Total NVIDIA® L40S GPUs for regular VMs without reservations | 32 | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* | *N/A* |

### Non-GPU virtual machines

| Quota name | Default value, `eu-north1`, `us-central1` | Default value, `me-west1`, `uk-south1`, `uk-south2`, `eu-west1`, `eu-west2`, `eu-south1`, `us-north1` | Default value, `eu-north2`\* |
| - | - | - | - |
| Virtual machines | 12 | 12 | 0 |
| Total vCPUs across non-GPU VMs | 0 | 200 | 0 |

## Storage

| Quota name | Default value, `eu-north1` | Default value, `eu-west1` | Default value, `us-central1`, `me-west1`, `uk-south1`, `uk-south2`, `eu-west2`, `us-north1` | Default value, `eu-south1` | Default value, `eu-north2`\* |
| - | - | - | - | - | - |
| Disks | 32 | 32 | 32 | 32 | 0 |
| Total disk capacity (Network SSD) | 4 TiB | 2 TiB | 5 TiB | 5 TiB | 0 |
| Total disk capacity (Network SSD Non-replicated) | 4 TiB | 2 TiB | 5 TiB | 5 TiB | 0 |
| Total disk capacity (Network SSD IO M3) | 4 TiB | 2 TiB | 5 TiB | 5 TiB | 0 |
| Shared filesystems | 32 | 32 | 32 | 32 | 0 |
| Total shared filesystem capacity | 4 TiB | 2 TiB | 5 TiB | 5 TiB | 0 |
| Number of images | 5 | 5 | 5 | 5 | 0 |
| Total storage capacity of all images | 500 GiB | 500 GiB | 500 GiB | 500 GiB | 0 |
| Total number of disk snapshots | 32 | 32 | 32 | 32 | 32 |
| Total storage capacity of all disk snapshots | 1 TiB | 1 TiB | 1 TiB | 1 TiB | 1 TiB |

## InfiniBand

GPU cluster quotas apply to Compute GPU clusters and GPU clusters used by Managed Soperator or Managed Kubernetes.

| Quota name | Default value, `eu-north1`, `eu-west1`, `me-west1`, `us-central1`, `uk-south1`, `eu-west2`, `us-north1` | Default value, `eu-north2`\* |
| - | - | - |
| Number of GPU clusters | 5 | 0 |

## Network

See [Quotas in Virtual Networks](https://docs.nebius.com/vpc/resources/quotas-limits.md).

## Quota usage recommendations

Best practices for using VM quotas:

* When you create new VMs, calculate your available quotas, even if you plan to keep the VMs mostly in a stopped state.
* From time to time, review and delete unused VMs to free up quotas.
* If you need to temporarily free up VM resources, delete VMs instead of just stopping them.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
