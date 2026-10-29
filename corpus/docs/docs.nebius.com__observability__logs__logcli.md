# How to query logs with LogCLI

Source: https://docs.nebius.com/observability/logs/logcli

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to query logs with LogCLI

To work with logs in the terminal, you can use the [LogCLI](https://grafana.com/docs/loki/latest/query/logcli/getting-started/) command-line tool. Take into account the [limitations of our LogQL implementation](https://docs.nebius.com/observability/logs/query-language.md).

> [!TIP]
>
> For a simpler setup, consider using the built-in [Nebius AI Cloud CLI logging commands](https://docs.nebius.com/observability/logs/nebius-cli.md). LogCLI remains an option if you prefer Grafana® Loki-native tooling.

## Prerequisites

1. If you don't have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant. For example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `viewers`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it for later steps.

## How to query logs with LogCLI

1. Download LogCLI binary for your platform from the [Loki releases page](https://github.com/grafana/loki/releases).

2. Unzip the binary and move it to a directory that is part of your `$PATH`.

3. Save the static key that you [got earlier](#prerequisites) to a `LOKI_BEARER_TOKEN` environment variable:

   ```bash theme={null}
   export LOKI_BEARER_TOKEN=<static_key>
   ```

   Alternatively, get an [access token](https://docs.nebius.com/iam/authorization/access-tokens.md) for the current user of Nebius AI Cloud CLI:

   ```bash theme={null}
   LOKI_BEARER_TOKEN=$(nebius iam get-access-token)
   ```

4. Save the following URL to a `LOKI_ADDR` environment variable:

   ```bash theme={null}
   export LOKI_ADDR=https://read.logging.api.nebius.cloud/projects/<project_ID>
   ```

   In the URL, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

5. Run [LogQL](https://grafana.com/docs/loki/latest/query/) queries with `logcli`. Currently, the only supported label is `__bucket__`. It can have the following values:

   * `sp_serial`: Compute virtual machines (serial logs)
   * `sp_mk8s_control_plane`: Managed Kubernetes clusters (control plane logs)
   * `sp_mk8s_audit_logs`: Managed Kubernetes clusters (audit logs)
   * `sp_mlflow`: Managed MLflow clusters
   * `sp_postgres`: Managed PostgreSQL clusters
   * `sp_k8srelease`: applications for Managed Kubernetes
   * `default`: [user-ingested logs](https://docs.nebius.com/observability/logs/ingest/index.md)

   For example, to review errors that occurred in a Managed Service for PostgreSQL® cluster in the last 15 minutes, run the following command:

   ```bash theme={null}
   logcli query '{__bucket__="sp_postgres"} |= `ERROR`' --since 15m
   ```

   Instead of using environment variables, you can provide the access token and the URL when you run the command:

   ```bash theme={null}
   logcli query '{__bucket__="sp_postgres"} |= `ERROR`' \
     --since 15m \
     --bearer-token=$(nebius iam get-access-token) \
     --addr=https://read.logging.api.nebius.cloud/projects/<project_ID>
   ```

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
