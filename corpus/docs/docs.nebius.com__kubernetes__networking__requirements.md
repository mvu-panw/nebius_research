# Network requirements for Managed Service for Kubernetes® clusters

Source: https://docs.nebius.com/kubernetes/networking/requirements

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Network requirements for Managed Service for Kubernetes® clusters

A Managed Service for Kubernetes cluster requires several blocks of IP addresses for its components. Before creating a cluster, make sure that you meet the IP address requirements:

* The required allocations fit into your free [quotas](https://docs.nebius.com/vpc/resources/quotas-limits.md).
* The [subnet](https://docs.nebius.com/vpc/overview.md#subnet) you select during cluster creation has enough free CIDR blocks.

> [!NOTE]
>
> If you use a default subnet, it already meets the CIDR block requirement. If you plan to [use a non-default subnet](https://docs.nebius.com/kubernetes/networking/non-default-subnet.md), check that the subnet has the necessary IP address allocations available.

If Managed Kubernetes is unable to allocate the IP addresses, cluster creation fails.

## Private IP address allocations

For the [control plane](https://docs.nebius.com/kubernetes/components.md#control-plane-components):

* 5 `/32` allocations:

  * 1 for the internal load balancer.
  * 4 for the control plane instances in case of high availability (3 for `etcd` instances and 1 more to enable control plane updates). If control plane high availability is disabled, 3 `/32` allocations are enough.

* 1 allocation for Kubernetes services. By default, a `/16` CIDR block is allocated, but you can set the `spec.kube_network.service_cidrs` parameter during cluster creation to specify a custom CIDR block, in range from `/12` to `/28`.

For [node groups](https://docs.nebius.com/kubernetes/components.md#node-group), per node:

* 1 `/24` allocation for Pods assigned to a node.
* 1 `/32` allocation for the internal IP address of a node.

With the default [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters), a rolling update does not require quota for additional nodes. If you configure a surge-based deployment strategy, make sure that you have enough available quota for the additional nodes that can be created during the update.

> [!WARNING]
>
> If you set a specific subnet for a node group or for the control plane, make sure that the required CIDR blocks are available within that subnet.

## Public IP address allocations

The public IP address of the cluster is allocated automatically from the Managed Kubernetes project and does not use up your quota.

If you have enabled public IP addresses for nodes in a node group (with the `spec.template.network_interfaces.public_ip_address` parameter), you need 1 `/32` public IP allocation for each node.

To allocate the public IP addresses for the nodes from a fixed list, create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) in your subnet's pool of public IP addresses and pass it to the `spec.template.network_interfaces.public_ip_address.allocation_id` parameter.
