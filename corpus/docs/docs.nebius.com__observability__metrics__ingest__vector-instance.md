# How to ingest metrics from a Vector instance

Source: https://docs.nebius.com/observability/metrics/ingest/vector-instance

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest metrics from a Vector instance

Observability supports receiving data in the Prometheus `remote_write` format. To start sending metrics from a [Vector](https://vector.dev/docs/) instance, set up a [sink](https://vector.dev/docs/reference/configuration/sinks/prometheus_remote_write/) of the `prometheus_remote_write` type.

## Prerequisites

1. If you don’t have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `editors`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it later in the configuration steps.

## How to configure a sink

1. Add the following `remote_write` section to the Vector configuration file:

   ```yaml theme={null}
   # Gather metrics from sources (for example, Vector's metrics from Vector itself)
   sources:
     vector_metrics:
       type: "internal_metrics"
      scrape_interval_secs: 15

   # Optional transformations

   # Send metrics to Observability via remote_write
   sinks:
     prometheus_remote_write:
       type: "prometheus_remote_write"
       inputs:
         - "vector_metrics"
       endpoint: "https://write.monitoring.<region_ID>.nebius.cloud/projects/<project_ID>/prometheus/api/v1/write"
       auth:
         strategy: "bearer"
         token: "<token_value>"
       healthcheck:
         enabled: false
   ```

   In this configuration, specify the following values:

   * Region ID from the [region list](https://docs.nebius.com/overview/regions.md).
   * [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).
   * Token value of the static key that you [got earlier](#prerequisites).

2. [Restart or reload your Vector instance](https://vector.dev/docs/administration/management/).

Now, your Vector instance sends metrics to Observability Metrics.
