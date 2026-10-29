# Quotas in Managed Service for Soperator

Source: https://docs.nebius.com/slurm-soperator/managed-soperator/resources/quotas

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas in Managed Service for Soperator

Managed Service for Soperator shares some quotas with Compute.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

## Nodes (virtual machines)

Login, worker and [service nodes](https://docs.nebius.com/slurm-soperator/managed-soperator/service-nodes.md) in Managed Soperator clusters count towards the [Compute quota](https://docs.nebius.com/compute/resources/quotas-limits.md#virtual-machines) on the total number of vCPUs across non-GPU virtual machines (VMs).

The quotas on GPUs by type for regular VMs without reservations don't apply to Managed Soperator nodes because they require [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md) that reserve GPUs.

Compute quotas on total numbers of GPU VMs and non-GPU VMs are not affected by Managed Soperator nodes.

## Disks and shared filesystems

Disks and shared filesystems for login, worker and [service nodes](https://docs.nebius.com/slurm-soperator/managed-soperator/service-nodes.md) count towards [Compute quotas on storage capacity](https://docs.nebius.com/compute/resources/quotas-limits.md#storage) (total sizes of disks and shared filesystems by type). Quotas on total numbers of disks and shared filesystems are not affected by Managed Soperator clusters.
