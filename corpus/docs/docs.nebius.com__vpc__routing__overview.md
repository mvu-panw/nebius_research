# Routing in Nebius AI Cloud

Source: https://docs.nebius.com/vpc/routing/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Routing in Nebius AI Cloud

Routing in Nebius AI Cloud determines how traffic moves within and between [networks](https://docs.nebius.com/vpc/overview.md#network) and [subnets](https://docs.nebius.com/vpc/overview.md#subnet), as well as to and from the internet. Nebius AI Cloud provides resources called *routing tables (route tables)* and *routes* that you can use to customize the routing of egress traffic and implement advanced networking scenarios, such as [custom NAT gateways](https://docs.nebius.com/vpc/routing/custom-nat-gateway.md) or segmented architectures.

## Default routing rules

By default, the pre-created networks, subnets and routing tables in every [project](https://docs.nebius.com/iam/overview.md#projects) implement the following rules for traffic that are sent from the project's resources:

* Traffic from one resource in a network to another is always routed within that network, ignoring routes from default and custom routing tables. You cannot modify this behavior, bypass it by using custom routes or disable it.
* All other traffic from the network is routed according to the network's [default routing table](#default-routing-tables):

  * Traffic to private IP addresses outside the network is discarded.
  * Traffic to public IP addresses is routed to the internet through the [default egress gateway](#default-egress-gateway).

  You can modify the default routing table to configure routing across the network, or create [custom routing tables](#custom-routing-tables) and assign them to specific subnets.

### Default egress gateway

You can route traffic from Nebius AI Cloud resources to public IP addresses through the *default egress gateway*. You can specify the default egress gateway as the next hop only in routes with the destination CIDR block `0.0.0.0/0`.

When traffic is routed through the default egress gateway, the gateway sets the traffic's source IP address to the public IP address of the original resource. If this resource does not have a public address, the default egress gateway sets the traffic's source IP address to a dynamic public IP address from a common pool shared between all projects in a region.

## Routing tables and routes

A *routing table*, or a *route table*, is assigned to a subnet and defines how to route traffic from the subnet's resources. Each routing table contains a set of *routes*. A route contains the list of destination CIDR blocks and the next hop for them. If a routing table applies to a resource, and this resource sends traffic to an IP address that belongs to a CIDR block in one of the table's routes, this traffic is routed to the next hop defined in the route.

Virtual Networks supports two types of routing tables: default and custom.

### Default routing tables

Each network is created with a *default routing table* named `default-route-table-***`. It has one route with the destination CIDR block `0.0.0.0/0` (all IP addresses) and the default egress gateway as the next hop:

```yaml theme={null}
metadata:
  id: vpcroute-***
  parent_id: vpcroutetable-*** # Default routing table
spec:
  destination:
    cidr: 0.0.0.0/0
  next_hop:
    default_egress_gateway: true
```

> **Description of the parameters**
>
> * `.metadata.id`: ID of the route.
> * `.metadata.parent_id`: ID of the routing table. The parent resource of a route is a routing table; the parent resource of a routing table is a [project](https://docs.nebius.com/iam/overview.md#projects).
> * `.spec.destination.cidr`: CIDR block of egress traffic destinations to which the route applies.
> * `.spec.next_hop`: Next hop to which matching egress traffic is routed:
>
>   * `.spec.next_hop.default_egress_gateway`: All egress traffic to the internet is routed through the [default egress gateway](#default-egress-gateway). The traffic that is routed to private addresses outside the resource's network is discarded.
>
>     The parameter only supports the `true` value.

By default, each subnet created within a network gets assigned the network's default routing table, meaning that all traffic from resources within the subnet to public IP addresses is routed to the internet.

You can modify the default routing table of a network by [adding](https://docs.nebius.com/vpc/routing/manage.md#adding-routes-to-routing-tables) or [deleting routes](https://docs.nebius.com/vpc/routing/manage.md#deleting-routes). This affects all network's subnets that do not have custom routing tables assigned.

If you add a route with a CIDR block other than `0.0.0.0/0`, use the [custom route example](#custom-routing-tables) below. In particular, replace the `default_egress_gateway` parameter with the `allocation_id` parameter.

### Custom routing tables

You can [create your own routing tables](https://docs.nebius.com/vpc/routing/manage.md#creating-routing-tables) and [assign them to subnets](https://docs.nebius.com/vpc/routing/manage.md#assigning-routing-tables-to-subnets). A routing table is associated with a network, and you can assign it only to subnets of that network. A subnet is either assigned a custom routing table, or a subnet inherits its network's default routing table.

Example of a custom route:

```yaml theme={null}
metadata:
  id: vpcroute-***
  parent_id: vpcroutetable-***
spec:
  destination:
    cidr: <CIDR_block>
  next_hop:
    # Contains either allocation_id or default_egress_gateway
    allocation_id: vpcallocation-***
    default_egress_gateway: true
```

> **Description of the parameters**
>
> * `.metadata.id`: ID of the route.
>
> * `.metadata.parent_id`: ID of the routing table. The parent resource of a route is a routing table; the parent resource of a routing table is a [project](https://docs.nebius.com/iam/overview.md#projects).
>
> * `.spec.destination.cidr`: CIDR block of egress traffic destinations to which the route applies. If a resource sends traffic to an IP address that belongs to CIDR blocks of multiple routes in a routing table, the route with the longest subnet mask applies, according to the [longest prefix match](https://en.wikipedia.org/wiki/Longest_prefix_match).
>
>   > For example, consider a routing table with the following routes and their CIDR blocks:
>   >
>   > * Route A: `10.0.0.0/8` → next hop A
>   > * Route B: `10.14.0.0/16` → next hop B
>   >
>   > When a resource sends traffic to `10.14.15.114`, it is routed to the next hop B because `10.14.0.0/16` has a longer, 16-bit subnet mask (and thus, a longer prefix match with `10.14.15.114`).
>
> * `.spec.next_hop`: Next hop to which matching egress traffic is routed. The next hop can be one of the following:
>
>   * `.spec.next_hop.allocation_id`: ID of the [allocation](https://docs.nebius.com/vpc/overview.md#allocation). You can use this parameter with any destination CIDR block.
>
>     > [!WARNING]
>     >
>     > If the next hop of a route is an allocation that is not assigned to a resource, the egress traffic that matches the route is discarded.
>
>   * `.spec.next_hop.default_egress_gateway`: All egress traffic to the internet is routed through the [default egress gateway](#default-egress-gateway). The traffic that is routed to private addresses outside the resource's network is discarded.
>
>     You can only use this parameter with the destination CIDR block `0.0.0.0/0`.
>
>     The parameter only supports the `true` value.

### Empty routing tables

If you delete all routes in a routing table, resources in subnets that have this routing table assigned can only communicate with other resources within their network. All traffic to private IP addresses outside the network and to public IP addresses is discarded.
