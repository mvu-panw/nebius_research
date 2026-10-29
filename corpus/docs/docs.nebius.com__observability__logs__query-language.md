# LogQL implementation by Nebius AI Cloud

Source: https://docs.nebius.com/observability/logs/query-language

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# LogQL implementation by Nebius AI Cloud

Logs in Nebius AI Cloud support the [LogQL](https://grafana.com/docs/loki/latest/query/) query language. You can use LogQL in the [Nebius AI Cloud CLI](https://docs.nebius.com/observability/logs/nebius-cli.md), [Grafana®](https://docs.nebius.com/observability/logs/grafana.md) and [LogCLI](https://docs.nebius.com/observability/logs/logcli.md). This page covers the supported syntax with examples and [limitations](#limitations) specific to Nebius AI Cloud.

## Stream selectors

Every LogQL query starts with a stream selector inside curly braces. You must always specify the `__bucket__` label (or `--bucket` when [using the Nebius AI Cloud CLI](https://docs.nebius.com/observability/logs/nebius-cli.md)) to select the log bucket:

* `sp_serial`: Compute virtual machines (serial logs)
* `sp_mk8s_control_plane`: Managed Kubernetes clusters (control plane logs)
* `sp_mk8s_audit_logs`: Managed Kubernetes clusters (audit logs)
* `sp_mlflow`: Managed MLflow clusters
* `sp_postgres`: Managed PostgreSQL clusters
* `sp_k8srelease`: applications for Managed Kubernetes
* `default`: [user-ingested logs](https://docs.nebius.com/observability/logs/ingest/index.md)

```
{__bucket__="sp_postgres"}
```

Supported matching operators:

| Operator | Description | Example |
| - | - | - |
| `=` | Exact match | `{__bucket__="sp_postgres", container="pgbouncer"}` |
| `!=` | Negation | `{__bucket__="sp_postgres", container!="pgbouncer"}` |
| `=~` | Regex match | `{__bucket__="sp_postgres", container=~"pg.*"}` |
| `!~` | Regex negation | `{__bucket__="sp_postgres", container!~"pgbouncer\|odyssey"}` |

## Line filters

After the stream selector, chain line filters to search the log message text:

| Operator | Description | Example |
| - | - | - |
| `\|=` | Line contains text | `{...} \|= "error"` |
| `!=` | Line doesn't contain text | `{...} != "healthcheck"` |
| `\|~` | Line matches regex | `{...} \|~ "status=5\\d+"` |
| `!~` | Line doesn't match regex | `{...} !~ "GET /health"` |

You can chain multiple filters to narrow results:

```
{__bucket__="sp_postgres"} |= "ERROR" != "vacuum"
```

## Examples

### Basic log search

Find deadlocks in PostgreSQL® logs:

```
{__bucket__="sp_postgres"} |= "deadlock detected"
```

Find deadlocks excluding autovacuum-related messages:

```
{__bucket__="sp_postgres"} |= "deadlock detected" != "autovacuum"
```

### Filter by log level

```
{__bucket__="default"} | level="error"
```

### Search with regex

Find HTTP 5xx status codes:

```
{__bucket__="default"} |~ "status=5\\d+"
```

### Find slow requests

```
{__bucket__="default"} | duration > 1s
```

## Limitations

The LogQL implementation in Nebius AI Cloud has the following limitations:

* You must always include `__bucket__` in the stream selector, or use the `--bucket` parameter in [Nebius AI Cloud CLI commands](https://docs.nebius.com/observability/logs/nebius-cli.md). Queries without it return no entries.
* The `step` value (interval between points) must be smaller than the `range` value (the interval over which aggregation is performed).
* Alerts on aggregated metrics values are not supported.
* The entries with non-empty `__error__` value are ignored. As a result, filtering by error is not possible.
* The following functions are not supported:

  * `bytes_rate`, `bytes_over_time` functions
  * `absent_over_time` (because alerts on aggregated metrics values are not supported)
  * `topk`, `bottomk` without aggregation by label (because no entries are shown when labels are empty)
  * `sort`, `sort_desc` aggregations
  * `without` aggregation clauses
  * `vector` function
  * `approx_topk` aggregation

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
