# DNS quotas and constraints

Source: https://docs.nebius.com/vpc/dns/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# DNS quotas and constraints

## Quotas

DNS has a quota on the number of [DNS zones](https://docs.nebius.com/vpc/dns/overview.md). System-managed zones, for example, `<network_ID>.compute.internal.`, count toward this quota.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| - | - |
| DNS zones | 100 |

## Constraints

[DNS zones](https://docs.nebius.com/vpc/dns/manage-zones.md) and [DNS records](https://docs.nebius.com/vpc/dns/manage-records.md) have the following technical constraints:

| Constraint | Value |
| - | - |
| Records in a zone | 1000 |
| Records with the same relative name and type in a zone | 20 |
| Characters in a zone domain name, including the trailing dot | 252 |
| Characters in a record relative name | 252 |

To raise the number of records in a specific zone, or the number of records with the same relative name and type in it, [contact support](https://console.nebius.com/support).

### Zone domain name restrictions

Give a zone a domain name of at least two labels, for example, `my.example.`. Single-label names, such as `example.`, aren't available.

Nebius AI Cloud also reserves the domain names that it owns:

* The `internal.` domain
* `ns.internal.`, `compute.internal.` and `nebius.internal.` and all of their subdomains
* Domain names used for internal checks, such as `example.invalid.`

If you use one of these domain names, creating the zone fails with a `PermissionDenied` error that no general role lifts.
