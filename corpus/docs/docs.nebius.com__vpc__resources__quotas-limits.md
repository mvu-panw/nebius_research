# Virtual Networks quotas and constraints

Source: https://docs.nebius.com/vpc/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Virtual Networks quotas and constraints

## Quotas

Virtual Networks has quotas on the number of networking resources.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| - | - |
| Allocations | 1000 |
| Public IPv4 addresses | 3 |
| Networks | 50 |
| Pools | 50 |
| Routes | 300 |
| Route tables | 30 |
| Subnets | 50 |
| [Security groups](https://docs.nebius.com/vpc/security-groups/overview.md) | 200 |
| Security rules | 1000 |

## Constraints

Certain Virtual Networks resources have technical constraints that can't be changed directly.

| Constraint name | Value |
| - | - |
| [Security groups](https://docs.nebius.com/vpc/security-groups/overview.md) associated with a network | 128 |
| Security groups assigned to a VM's network interface | 8 |
| Security rules in a security group | 60 |
| CIDR blocks in a security rule | 8 |
| Ports in a security rule | 8 |
