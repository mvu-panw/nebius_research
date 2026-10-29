# About Virtual Networks

Source: https://docs.nebius.com/vpc/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# About Virtual Networks

Virtual Networks is a service that provides networking infrastructure to Nebius AI Cloud resources. The service's key resources are [networks](#network), [subnets](#subnet), [pools](#pool), [allocations](#allocation), [routing tables](#routing-table) and [DNS zones](#dns-zone).

When you create a project, Virtual Networks [automatically provides you](#default-virtual-networks-resources) with the required networking resources. You can use them as they are, change them, create new Virtual Networks resources or [customize the whole networking infrastructure](#customized-networking-infrastructure).

> [!NOTE]
>
> Virtual Networks currently supports only IPv4 addresses.

## Network

A *network* in Nebius AI Cloud is similar to a regular local area network. It ensures IP connectivity between resources within a network and isolates them from resources outside this network.

Some Nebius AI Cloud resources are network-specific, and they require a network to be part of their configuration. For example, these can include Managed Service for PostgreSQL® and Managed Service for MLflow clusters.

## Subnet

A *subnet* is a network segment that contains a certain range of IP addresses allocated in this network.

Some Nebius AI Cloud resources are subnet-specific, and they require a subnet to be part of their configuration. For example, these can include Compute virtual machines (VMs), Managed Service for Kubernetes® clusters or [allocations](#allocation).

When you create a resource within a subnet, the IP address of this resource is taken from the [pool](#pool) attached to this subnet (that is, from the IP address range of this subnet).

To reserve a range of IP addresses for a subnet, explicitly specify CIDR blocks in the configuration of this subnet. These CIDR blocks must be within the IP address range of the network, and other subnets must not use these blocks.

Alternatively, you can configure a subnet to transparently use the pools of the network that the subnet belongs to. All subnets of this network can concurrently use these pools.

## Pool

A *pool* reserves [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). You can assign a pool to a subnet or a network. A pool assigned to a network determines the allowed IP range of this network. A pool assigned to a subnet determines the IP range from which resources take IP addresses in this subnet.

Any pool has a source pool. CIDR blocks defined in a new pool must be a subset of the CIDR blocks of the source pool. For example, you can have a pool `10.0.0.0/8`, which has a child pool `10.0.0.0/16`, and `10.0.0.0/16` has a child pool `10.0.0.0/24`. For `10.0.0.0/24`, the source pool is `10.0.0.0/16`.

CIDR blocks that belong to different subnets within the same network cannot overlap.

## Allocation

An *allocation* is a reserved IP address. It can be a public or a private address. You can attach an allocation to a resource, such as a Compute VM, so other resources can reach it by using the IP address from the allocation.

An allocation is attributed to a subnet, so the IP address of the allocation must be within the IP address range of the subnet.

## Routing table

A *routing table*, or a *route table*, is assigned to a subnet and defines how to route traffic from the subnet's resources. Each routing table contains a set of *routes*. A route contains the list of destination CIDR blocks and the next hop for them. If a routing table applies to a resource, and this resource sends traffic to an IP address that belongs to a CIDR block in one of the table's routes, this traffic is routed to the next hop defined in the route.

You can create and manage custom routing tables that work together with default routing tables and built-in routing rules. For more details, see [Routing in Nebius AI Cloud](https://docs.nebius.com/vpc/routing/overview.md) and [Managing routing tables and routes](https://docs.nebius.com/vpc/routing/manage.md).

## DNS zone

A *DNS zone* is a container for a domain name and every name under it. A zone is attached to one network, and the names in it resolve only from workloads within this network.

Each network gets a system-managed zone that Nebius AI Cloud fills with the [FQDNs](https://docs.nebius.com/compute/virtual-machines/fqdn.md) of the VMs in the network. You can also create custom zones on the same network. For more details, see [About DNS](https://docs.nebius.com/vpc/dns/overview.md), [Managing DNS zones](https://docs.nebius.com/vpc/dns/manage-zones.md) and [Managing DNS records](https://docs.nebius.com/vpc/dns/manage-records.md).

## Default Virtual Networks resources

When you create a project, it is automatically provided with default Virtual Networks resources. This allows you to manage other Nebius AI Cloud resources that require networks, subnets, pools and allocations. You can use these default resources or create new ones.

Some Nebius AI Cloud resources automatically create Virtual Networks resources if the latter are not specified in the configuration. For example, Compute VMs create their own allocations unless you explicitly specify an existing allocation in the VM configuration.

For some other resources, you cannot change or cancel the implicit creation of Virtual Networks resources. For example, Managed Service for Kubernetes clusters create their own allocations.

The default Virtual Networks resources include the following:

* `default-network`: Network in a given project.
* `default-subnet`: Subnet within `default-network`. This subnet uses pools in `default-network`.
* `default-network-pool`: Pool of private IPv4 addresses that belongs to `default-network`. The CIDR block of this pool [depends on the region](https://docs.nebius.com/vpc/addressing/available-addresses.md) of the project.
* `default-public-pool`: Pool of public IPv4 addresses that belongs to `default-network`.
* `default-route-table-***`: Routing table within each network. It consists of one route that routes to the internet all egress traffic destined for public IP addresses. Each subnet in a network is assigned the network's default routing table by default.

You can customize, modify or delete most of the default resources, except for `default-public-pool`. This resource is shared across all projects in a tenant.

## Customized networking infrastructure

If you need a customized networking infrastructure, plan the configuration of the required resources in advance. You cannot change the configuration of Virtual Networks resources once they are attached to active workloads (for example, a Compute VM). To change such resources, you first need to delete the workloads. As these workloads are active, such changes are disruptive for the infrastructure.

Here are some examples when you might need a customized networking infrastructure:

* Multi-region deployment in Nebius AI Cloud
* Establishing connectivity between the environment in Nebius AI Cloud and an external infrastructure
* Particular IP addressing schema

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
