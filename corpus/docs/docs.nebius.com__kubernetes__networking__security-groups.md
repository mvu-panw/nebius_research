# Security groups in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/networking/security-groups

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Security groups in Managed Service for Kubernetes®

Managed Service for Kubernetes integrates with Virtual Networks security groups to control traffic to and from your cluster's nodes.

For a general overview of network security groups and how to create them, see [Security groups overview](https://docs.nebius.com/vpc/security-groups).

## System security groups

Nebius automatically creates and manages a *system security group* per cluster for your worker nodes. This security group guarantees that core Kubernetes connectivity, such as connectivity between the API server and kubelets, works correctly regardless of any additional security groups that you configure on your node groups.

The system security group is visible in your project, but it's marked as managed. You can't edit it or attach it to your own resources.

## User-defined security groups

You can [attach](https://docs.nebius.com/kubernetes/networking/manage-security-groups.md) your own security groups to node groups. When you do, each node in that group has both your security groups and the system security group attached. The system security group is always present and can't be overridden or removed.

If you don't specify any security groups when creating a node group, the network's default security group is attached alongside the system security group.

This means you can use your own security groups to restrict or allow additional traffic, such as traffic between node groups or to external services, without risking disruption to cluster operations.

## Default security groups

Every virtual machine (VM) or node group in Nebius AI Cloud is always added to at least one security group: the network's *default security group*. This applies automatically and can't be removed. It ensures that VMs always have a baseline set of rules even before any cluster-level or user-defined groups are applied.

## See also

* [How to attach security groups to a node group](https://docs.nebius.com/kubernetes/networking/manage-security-groups.md)
