# Nebius Tunnels Agent changelog

Source: https://docs.nebius.com/tunnels/resources/tunnels-agent-changelog

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius Tunnels Agent changelog

Nebius Tunnels Agent runs next to your application and connects to a regional Nebius edge endpoint over an outbound TLS connection. It proxies inbound traffic from public tunnel URLs to local HTTP or TCP services, so you can expose a service without opening inbound firewall ports. For more details, see [How to connect to a tunnel](https://docs.nebius.com/tunnels/connect.md).

**v1.2.0**

2026-09-21

You can now configure how the tunnel agent connects to your local services. The agent also spends less CPU on every request it forwards.

### Added

* Optional top-level `local_service` section that configures how the tunnel agent connects to your services:

  ```yaml theme={null}
  local_service:
    max_idle_conns: 400
    max_idle_conns_per_host: 200
    idle_conn_timeout: 120s
    dial_timeout: 5s
  ```

  * `max_idle_conns`: Maximum number of idle connections across all target addresses. Default: `200`.
  * `max_idle_conns_per_host`: Maximum number of idle connections per target address. Services with the same `target` value in the `services` section share the same pool. Default: `100`.
  * `idle_conn_timeout`: How long an idle connection stays in the pool. Default: `90s`.
  * `dial_timeout`: Timeout for opening a connection to a service. Default: `10s`.

  Every parameter is optional. To set the default values for them, omit the parameters or set them to `0`. Negative values are invalid, and the agent doesn't start with them.

  The pool parameters apply to the services that the tunnel serves over HTTP/1.1. Services served over HTTP/2, such as gRPC, multiplex requests over a single connection and don't use the pool. The `dial_timeout` parameter applies to services of every type, including `type: tcp`.

### Changed

* The agent keeps up to 100 idle connections per target address instead of 10, and 200 across all addresses instead of 100. Under concurrent load, it reuses these connections instead of opening a new one for every request. These limits apply to connections kept for reuse: the number of connections that the agent opens during peak moments depends on the number of concurrent requests and isn't limited by these parameters.
* The agent uses less CPU per forwarded request.
* Debug logs no longer contain request paths and target URLs, and error messages no longer contain the URL of a local service.

#### Artifacts

* **Binaries**: Linux (x86\_64, aarch64), macOS (arm64, x86\_64) and Windows (arm64, x86\_64) with a [checksums-sha256.txt](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/checksums-sha256.txt), covering every archive:

  * [nebius-tunnel-agent-linux-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/nebius-tunnel-agent-linux-x86_64.tar.gz)
  * [nebius-tunnel-agent-linux-aarch64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/nebius-tunnel-agent-linux-aarch64.tar.gz)
  * [nebius-tunnel-agent-darwin-arm64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/nebius-tunnel-agent-darwin-arm64.tar.gz)
  * [nebius-tunnel-agent-darwin-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/nebius-tunnel-agent-darwin-x86_64.tar.gz)
  * [nebius-tunnel-agent-windows-arm64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/nebius-tunnel-agent-windows-arm64.tar.gz)
  * [nebius-tunnel-agent-windows-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.2.0/nebius-tunnel-agent-windows-x86_64.tar.gz)

* **Container image**: `cr.eu-north1.nebius.cloud/marketplace/docker/nebius-tunnel-agent:1.2.0` (linux/amd64, linux/arm64).

* **Helm chart**: `oci://cr.eu-north1.nebius.cloud/marketplace/chart/nebius-tunnel-agent:1.2.0`.

**v1.1.0**

2026-09-09

TCP services can now use [Application-Layer Protocol Negotiation](https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation) (ALPN) on the public TLS endpoint. This lets PostgreSQL clients of version 17 or later connect through a tunnel with `sslnegotiation=direct`.

### Added

* Optional `alpn` parameter for services with `type: tcp`. The agent sends a list of protocols to the Nebius edge endpoint during registration, and the endpoint negotiates a protocol with the client:

  ```yaml theme={null}
  services:
    - name: postgres
      target: localhost:5432
      type: tcp
      alpn: [postgresql]
  ```

* Validation of the `alpn` parameter at the tunnel agent startup. The parameter can include up to 8 unique IDs, each 1 to 255 printable ASCII characters long and without spaces. Leading and trailing spaces are trimmed.

  HTTP services don't use `alpn`. To serve an HTTP service over HTTP/2, set `protocol: h2` instead.

Configurations created earlier keep working: a TCP service with an omitted or empty `alpn` parameter behaves as before.

The endpoint selects a protocol that the client offers, the service declares and the endpoint allows. The list of allowed protocols includes `postgresql`. If the client doesn't offer any matching protocol, the endpoint completes a TLS handshake without ALPN. Clients that require it, such as PostgreSQL clients with `sslnegotiation=direct`, can't connect.

#### Artifacts

* **Binaries**: Linux (x86\_64, aarch64), macOS (arm64, x86\_64) and Windows (arm64, x86\_64) with a [checksums-sha256.txt](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/checksums-sha256.txt), covering every archive:

  * [nebius-tunnel-agent-linux-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/nebius-tunnel-agent-linux-x86_64.tar.gz)
  * [nebius-tunnel-agent-linux-aarch64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/nebius-tunnel-agent-linux-aarch64.tar.gz)
  * [nebius-tunnel-agent-darwin-arm64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/nebius-tunnel-agent-darwin-arm64.tar.gz)
  * [nebius-tunnel-agent-darwin-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/nebius-tunnel-agent-darwin-x86_64.tar.gz)
  * [nebius-tunnel-agent-windows-arm64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/nebius-tunnel-agent-windows-arm64.tar.gz)
  * [nebius-tunnel-agent-windows-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.1.0/nebius-tunnel-agent-windows-x86_64.tar.gz)

* **Container image**: `cr.eu-north1.nebius.cloud/marketplace/docker/nebius-tunnel-agent:1.1.0` (linux/amd64, linux/arm64).

* **Helm chart**: `oci://cr.eu-north1.nebius.cloud/marketplace/chart/nebius-tunnel-agent:1.1.0`.

**v1.0.0**

2026-06-19

First public release of the Nebius Tunnels agent, a client-side tunnel that connects to Edge and proxies inbound traffic to local services.

### Added

* Tunnel agent that connects to Edge and proxies traffic to a local service.
* Release binaries for Linux (x86\_64, aarch64), macOS (arm64, x86\_64) and Windows (arm64, x86\_64).
* Multi-arch container image (linux/amd64, linux/arm64).
* Helm chart for running the agent in Kubernetes.

#### Artifacts

* **Binaries**: also mirrored under `.../latest/`,
  with a `checksums-sha256.txt`, covering every archive:

  * [nebius-tunnel-agent-linux-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.0.0/nebius-tunnel-agent-linux-x86_64.tar.gz)
  * [nebius-tunnel-agent-linux-aarch64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.0.0/nebius-tunnel-agent-linux-aarch64.tar.gz)
  * [nebius-tunnel-agent-darwin-arm64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.0.0/nebius-tunnel-agent-darwin-arm64.tar.gz)
  * [nebius-tunnel-agent-darwin-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.0.0/nebius-tunnel-agent-darwin-x86_64.tar.gz)
  * [nebius-tunnel-agent-windows-arm64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.0.0/nebius-tunnel-agent-windows-arm64.tar.gz)
  * [nebius-tunnel-agent-windows-x86\_64.tar.gz](https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent/1.0.0/nebius-tunnel-agent-windows-x86_64.tar.gz)

* **Container image**: `cr.eu-north1.nebius.cloud/marketplace/docker/nebius-tunnel-agent:1.0.0`, also tagged `:latest`.

* **Helm chart**: `oci://cr.eu-north1.nebius.cloud/marketplace/chart/nebius-tunnel-agent:1.0.0`, also tagged `:latest` (pull or install without `--version` to get the latest).
