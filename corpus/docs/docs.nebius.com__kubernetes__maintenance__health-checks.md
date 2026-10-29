# Health checks and automatic recovery of Managed Service for Kubernetes® nodes

Source: https://docs.nebius.com/kubernetes/maintenance/health-checks

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Health checks and automatic recovery of Managed Service for Kubernetes® nodes

Managed Service for Kubernetes runs *[Node Problem Detector](https://kubernetes.io/docs/tasks/debug/debug-cluster/monitor-node-health/)* (NPD) to monitor health checks. NPD is an open-source Kubernetes daemon that checks a node's health, detects problems on a node and reports them as [Kubernetes conditions](https://kubernetes.io/docs/reference/node/node-status/#condition) or [events](https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/). Managed Kubernetes runs NPD on each node in the cluster as a systemd service by default. NPD collects information about CPU usage, disk usage and network status.

Based on health checks, Managed Kubernetes automatically recovers nodes in a cluster. The service applies health checks in the following cases:

* A Network SSD Non-replicated (Network SSD NRD) boot disk experiences [input/output (I/O) issues](#i%2Fo-issues-of-a-network-ssd-nrd-boot-disk) and does not work correctly.
* A node is reporting a [false or unknown status](#false-or-unknown-status-of-a-node).
* A node is experiencing [problems with GPUs](#issues-with-gpus-on-a-node).

For information about the availability of health checks, see [How to enable or disable health checks in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/maintenance/enable-disable-health-checks.md).

## I/O issues of a Network SSD NRD boot disk

If a Network SSD NRD boot disk on a node is unavailable for reading data from the disk or writing to it, the boot disk reports I/O errors. If the errors persist for 30 seconds or more, Managed Kubernetes sets the Kubernetes condition `NebiusBootDiskIOError = True` for the node.

To fix the I/O issues, the service runs an automatic recovery: it deletes the node and then creates a new one with a different name and healthy boot disk.

## False or unknown status of a node

Managed Kubernetes runs health checks and sets the `Ready` Kubernetes condition to check a node's status. If the condition remains in the `False` status for more than five minutes, or if the condition remains in the `Unknown` status for more than 15 minutes, the service runs an automatic recovery. It deletes the node and then creates a healthy one with a different name.

## Issues with GPUs on a node

Managed Kubernetes runs several health checks for components of a GPU-based cluster. For example, the service checks GPUs, [InfiniBand™](https://docs.nebius.com/kubernetes/gpu/clusters.md) and NVLink by using the `nvidia-smi`, `dcgmi` and `dmesg` tools. Also, the service checks if a GPU node experiences [Xid errors](https://docs.nvidia.com/deploy/xid-errors/introduction.html) or problems with the [error correction code memory](https://en.wikipedia.org/wiki/ECC_memory).

Each GPU health check runs every five minutes. If all GPU health checks have passed, the `NebiusGPUError` Kubernetes condition is set to the `False` status.

If the condition is set to the `True` status, Managed Kubernetes automatically recovers the node:

1. To stop scheduling new Pods, Managed Kubernetes cordons the node.
2. The service waits until all workloads that consume GPUs are finished or stopped, and until these GPUs are released.
3. To remove existing Pods, Managed Kubernetes drains the node. The drain takes up to one hour.
4. Nebius AI Cloud stops the node (the Compute virtual machine which the node is based on).
5. Nebius AI Cloud starts the node.
6. Managed Kubernetes uncordons the node and enables scheduling new Pods.

As a result, Managed Kubernetes migrates the node to a different, healthy virtual machine.

Sometimes, a GPU-related issue is solved before Managed Kubernetes starts to drain the node. In this case, the service does not drain the node but uncordons it instead.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
