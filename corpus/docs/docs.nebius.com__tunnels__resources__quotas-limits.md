# Nebius Tunnels limits and constraints

Source: https://docs.nebius.com/tunnels/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius Tunnels limits and constraints

Nebius Tunnels enforces platform-wide limits on traffic and client connections. These limits protect shared infrastructure and can't be changed in the web console.

Limits apply at three nested levels: region, project and tunnel. Each level is a shared pool of capacity: all tunnels in a [region](https://docs.nebius.com/overview/regions.md) share the region limit, all tunnels in a project share the project limit, and all clients of a tunnel share the tunnel limit. A tunnel never gets more than its own limit, but it can get less when other tunnels in its project or region are busy.

When aggregate usage reaches a limit, responses may take longer until usage drops below the limit.

### Traffic

Inbound and outbound traffic share the same limit.

| Level | Limit, inbound and outbound traffic |
| - | - |
| Region | 8 Gbps |
| Project | 600 Mbps |
| Tunnel | 120 Mbps |

### Client connections

*Client connections* are new connections from internet users to a tunnel's public URLs. The limits apply to the number of new connections per second.

| Level | Limit, connections per second |
| - | - |
| Region | 6000 |
| Project | 1500 |
| Tunnel | 300 |

## Constraints

Certain Nebius Tunnels settings have technical constraints that can't be changed directly.

| Constraint name | Value |
| - | - |
| Agent connection protocol | HTTP/2 over TLS |
| Supported service types | HTTP and TCP |
