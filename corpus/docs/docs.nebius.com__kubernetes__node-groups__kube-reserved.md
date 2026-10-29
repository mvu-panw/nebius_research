# kubeReserved values on worker nodes in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/node-groups/kube-reserved

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# kubeReserved values on worker nodes in Managed Service for Kubernetes®

In Managed Service for Kubernetes, the kubelet sets `kubeReserved` values on worker nodes to reserve resources for Kubernetes system components.

This article describes the default values and how the `memory` reservation is calculated.

## Default values

By default, worker nodes use the following `kubeReserved` values:

* `cpu`: `100m`
* `ephemeral-storage`: `1Gi`
* `memory`: `512Mi`

However, for worker nodes with GPUs, Managed Kubernetes calculates the `memory` reservation value from the size of RAM you select for the node. This helps account for a known Kubernetes issue where the kubelet may not observe `MemoryPressure` right away. For more information, see [Node-pressure Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/#known-issues) in the official Kubernetes documentation.

The calculation uses the following tiered approach:

* `255Mi` for nodes with less than 1 GiB of RAM
* `25%` of the first 4 GiB
* `20%` of the next 4 GiB (up to 8 GiB)
* `10%` of the next 8 GiB (up to 16 GiB)
* `6%` of the next 112 GiB (up to 128 GiB)
* `2%` of RAM above 128 GiB
* Plus `100Mi` on every node to handle Pod eviction

## Examples

The following table shows the resulting `memory` value in `kubeReserved` for the selected RAM size in your GPU nodes:

| Node RAM | `kubeReserved.memory` |
| - | - |
| 8 GiB | `1944Mi` |
| 16 GiB | `2763Mi` |
| 128 GiB | `9644Mi` |
| 256 GiB | `12266Mi` |

## See also

* [Node groups](https://docs.nebius.com/kubernetes/components.md#node-group)
* [Creating and modifying node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md)
