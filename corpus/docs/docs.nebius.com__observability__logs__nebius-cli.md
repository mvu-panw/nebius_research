# How to query logs with Nebius AI Cloud CLI

Source: https://docs.nebius.com/observability/logs/nebius-cli

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to query logs with Nebius AI Cloud CLI

The Nebius AI Cloud CLI includes built-in commands for querying and analyzing logs directly from the terminal. The `--bucket` parameter automatically applies the `__bucket__` stream selector, so you don't need to include it in your LogQL query. Take into account the [limitations of our LogQL implementation](https://docs.nebius.com/observability/logs/query-language.md).

## Prerequisites

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Running log queries

To run log queries, use the [nebius logging query](https://docs.nebius.com/cli/reference/logging/query.md) command:

```bash theme={null}
nebius logging query '<query>' --bucket <log_bucket>
```

* In your log query (log stream selector), use [LogQL as implemented in Nebius AI Cloud](https://docs.nebius.com/observability/logs/query-language.md), and [labels and their values](#getting-labels-and-their-values) that the log bucket supports.
* In `--bucket`, specify the log bucket. `--bucket` replaces the `__bucket__` label, you don't need to include `__bucket__` in your log query (log stream selector). `--bucket` supports the following values:

  * `sp_serial`: Compute virtual machines (serial logs)
  * `sp_mk8s_control_plane`: Managed Kubernetes clusters (control plane logs)
  * `sp_mk8s_audit_logs`: Managed Kubernetes clusters (audit logs)
  * `sp_mlflow`: Managed MLflow clusters
  * `sp_postgres`: Managed PostgreSQL clusters
  * `sp_k8srelease`: applications for Managed Kubernetes
  * `default`: [user-ingested logs](https://docs.nebius.com/observability/logs/ingest/index.md)

> For example:
>
> * To review errors that occurred on Compute virtual machines in the last 15 minutes, run the following command:
>
>   ```bash theme={null}
>   nebius logging query '{level="error"}' --bucket sp_serial --since 15m
>   ```
>
> * To search for `pgbouncer` in Managed Service for PostgreSQL® logs in the last 15 minutes, run the following command:
>
>   ```bash theme={null}
>   nebius logging query '{} |= "pgbouncer"' --bucket sp_postgres --since 15m
>   ```

### Getting labels and their values

To help you build your log query, get the list of supported labels and their values for each bucket by running the [nebius logging labels](https://docs.nebius.com/cli/reference/logging/labels.md) and [nebius logging label-values](https://docs.nebius.com/cli/reference/logging/label-values.md) commands.

> For example:
>
> ```bash theme={null}
> nebius logging labels --bucket sp_mk8s_control_plane
> nebius logging label-values level --bucket sp_mk8s_control_plane
> ```

### Streaming logs

To stream logs in real time, add `--follow` to your `nebius logging query` command.

> For example:
>
> ```bash theme={null}
> nebius logging query '{level="error"} |= "ProvisioningRequest"' \
>   --bucket sp_mk8s_control_plane --follow
> ```

## Running metric queries

To run [metric queries](https://grafana.com/docs/loki/latest/query/metric_queries/), use the [nebius logging metrics](https://docs.nebius.com/cli/reference/logging/metrics.md) command:

```bash theme={null}
nebius logging metrics '<query>' --bucket <log_bucket>
```

Requirements for the query and the log bucket are the same as for [log queries](#running-log-queries).

> For example:
>
> * To get the error rate in serial logs from Compute virtual machines in the last 15 minutes, run the following command:
>
>   ```bash theme={null}
>   nebius logging metrics 'rate({level="error"}[15m])' --bucket sp_serial
>   ```
>
> * To count Managed Kubernetes control plane logs per level in the last 5 minutes, run the following command:
>
>   ```bash theme={null}
>   nebius logging metrics 'sum by (level)(count_over_time({}[5m]))' \
>     --bucket sp_mk8s_control_plane --step 5m
>   ```
