# Security groups in Nebius AI Cloud

Source: https://docs.nebius.com/vpc/security-groups/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Security groups in Nebius AI Cloud

*Security groups* in Nebius AI Cloud serve as a firewall for your [Compute](https://docs.nebius.com/compute/index.md) virtual machines (VMs), controlling ingress and egress traffic at the packet level. Security groups consist of *security rules*; each security rule describes whether ingress or egress traffic with certain parameters (source, destination, protocol) should be allowed or denied. For a security group to apply to a VM, you need to add a VM's network interface to the security group.

Security groups and security rules are subject to [quotas and constraints](https://docs.nebius.com/vpc/resources/quotas-limits.md).

## Security groups and security rules

Each security group is associated with a [network](https://docs.nebius.com/vpc/overview.md#network) and can only apply to VMs in this network. The network ID is specified in the `.spec.network_id` parameter of the security group's specification:

```yaml theme={null}
metadata:
  id: vpcsecuritygroup-***
  parent_id: project-***
spec:
  network_id: vpcnetwork-***
```

Security rules are child resources of a security group. Here is an example of a security rule that denies TCP egress traffic to the `192.0.2.0/24` CIDR block on port 8888:

```yaml theme={null}
metadata:
  id: vpcsecurityrule-***
  parent_id: vpcsecuritygroup-***
spec:
  access: DENY
  egress:
    destination_cidrs:
      - 192.0.2.0/24
    destination_ports:
      - 8888
  protocol: TCP
  type: STATELESS
  priority: 500
```

> **Description of the parameters**
>
> * `.metadata.id`: ID of the security rule.
>
> * `.metadata.parent_id`: ID of the security group. The parent resource of a security rule is a security group; the parent resource of a security group is a [project](https://docs.nebius.com/iam/overview.md#projects).
>
> * `.spec.access`: Whether to `ALLOW` or `DENY` the ingress or egress traffic defined in the security rule.
>
> * `.spec.egress`: Source and destination of the egress traffic that should match the rule. Each security rule must have either `.spec.egress` or `.spec.ingress` (for ingress traffic).
>
>   * `.spec.egress.destination_cidrs`, `.spec.egress.destination_ports`: Lists of up to eight CIDR blocks and eight ports that the traffic goes to. Both egress and ingress rules support these parameters as well as `source_cidrs` and `source_ports`.
>
>     You can also specify a security group as the source in an ingress security rule (`.spec.ingress.source_security_group_id`) or as the destination in an egress security rule (`.spec.egress.destination_security_group_id`).
>
> * `.spec.protocol`: Networking protocol to which the rule applies. Supported values are `TCP`, `UDP`, `ICMP` and `ANY`.
>
>   > [!NOTE]
>   >
>   > Port filtering applies to `TCP` and `UDP` only. `ANY` and `ICMP` don't support port filtering.
>
> * `.spec.type`: Rule type. Supported values are `STATEFUL` (connection tracking is enabled; default) and `STATELESS` (connection tracking is disabled).
>
> * `.spec.priority`: Priority of the rule. 1 is the highest priority, 1000 is the lowest.

For instructions, see [Managing security groups and security rules](https://docs.nebius.com/vpc/security-groups/manage.md).

### Ignored CIDR blocks

Traffic to and from `169.254.0.0/16` (`169.254.0.0`–`169.254.255.255`) isn't evaluated by security groups. These IP addresses are reserved for internal Nebius use.

### Security rule types: stateful and stateless

A security rule can be stateful or stateless, which means it has connection tracking enabled or disabled:

* *Stateful* security rules track connections in which the matching traffic is sent and automatically allow the response traffic within the same connection, even if it doesn't match any other rule. For example, if a VM sends a request that a stateful security rule in the VM's security group allows, the response to this request is allowed by the same rule.
* *Stateless* security rules don't track connections like stateful security rules do. For your VM to be able to send or receive a response to ingress or egress traffic that a stateless security rule allows, you need to create a separate security rule.

### Security rule priorities

Each security rule has a *priority* from 1 to 1000.

When determining how to apply security rules to a traffic packet, Nebius AI Cloud looks for a matching security rule, starting from security rules with lower priority values — that is, going from 1 to 1000. Once a match is found, the lookup stops and the matching rule is applied. If no match is found, the traffic is denied. This means that adding a VM's network interface to an empty security group blocks all traffic to and from this network interface.

If two or more security rules have the same priority, security rules that deny traffic take precedence over security rules that allow traffic.

The default priority of a security rule is 500. Setting the priority at 0 is the same as the default value.

If you add a network interface of a VM to multiple security groups, all security rules from these security groups are combined into one list that is then looked up by *effective priority*. Effective priority is automatically calculated for each security rule from its priority and returned in its `.status.effective_priority` parameter:

```yaml theme={null}
metadata:
  id: vpcsecurityrule-***
status:
  effective_priority: 3001
```

### Security groups as sources or destinations in security rules

You can specify a security group as the source for an ingress security rule or as the destination for an egress security rule. For example:

```yaml theme={null}
metadata:
  id: vpcsecurityrule-***
spec:
  access: DENY
  egress:
    destination_security_group_id: vpcsecuritygroup-***
  priority: 500
  protocol: TCP
  type: STATELESS
```

The security group specified in a security rule and the security group that contains the security rule must be associated with the same network.

You can use the source/destination security group together with the source/destination CIDR blocks and ports in a security rule:

```yaml theme={null}
metadata:
  id: vpcsecurityrule-***
spec:
  egress:
    destination_cidrs:
      - 192.0.2.0/24
    destination_ports:
      - 8888
    destination_security_group_id: vpcsecuritygroup-***
  priority: 500
  protocol: TCP
  type: STATELESS
```

In this case, the security rule applies to VMs' network interfaces that have the specified security group *and* an IP address from one of the specified CIDR blocks assigned to them.

## Default security groups

Each network has a *default security group* that all VMs in this network are implicitly added to by default. It allows all ingress and egress traffic.

> **Security rules in a default security group**
>
> ```yaml theme={null}
> items:
>   - metadata:
>       id: vpcsecurityrule-***
>       parent_id: vpcsecuritygroup-***
>     spec:
>       access: ALLOW
>       ingress: {}
>       priority: 500
>       protocol: ANY
>       type: STATELESS
>   - metadata:
>       id: vpcsecurityrule-***
>       parent_id: vpcsecuritygroup-***
>     spec:
>       access: ALLOW
>       egress: {}
>       priority: 500
>       protocol: ANY
>       type: STATELESS
> ```

You can't change or delete default security groups.
