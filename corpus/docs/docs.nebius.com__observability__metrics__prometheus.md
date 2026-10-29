# How to view metrics in Prometheus

Source: https://docs.nebius.com/observability/metrics/prometheus

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to view metrics in Prometheus

To work with metrics in Prometheus, connect Prometheus to Observability Metrics and query the data by using [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/).

## Prerequisites

1. If you don't have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant. For example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `viewers`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it for later steps.

## How to connect Prometheus

> [!NOTE]
>
> Prometheus can only show a limited amount of monitoring data. If you have a large infrastructure, consider connecting a data source in [Grafana®](https://docs.nebius.com/observability/metrics/grafana.md) instead.

1. [Download the latest release](https://prometheus.io/download) of Prometheus for your platform.

2. Extract the contents and switch to the folder with Prometheus:

   ```bash theme={null}
   tar xvfz prometheus-***.tar.gz
   cd prometheus-***
   ```

3. Create the `prometheus.yml` configuration file that configures Prometheus to retrieve the metrics. Use one of the following configurations depending on your Prometheus version:

   ```yaml Prometheus 3.x theme={null}
   scrape_configs:
     - job_name: 'Export time series from Nebius Observability'
       honor_labels: true
       scrape_interval: 15s
       scheme: https
       metrics_path: '/projects/<project_ID>/service-provider/prometheus/federate'
       params:
         match[]:
           - '{__name__=~".+"}'
       bearer_token: '<static_key_for_service_account>'
       static_configs:
         - targets:
           - 'read.monitoring.<region>.nebius.cloud'
   ```

   ```yaml Prometheus 2.x theme={null}
   scrape_configs:
     - job_name: 'Export time series from Nebius Observability'
       honor_labels: true
       scrape_interval: 15s
       scheme: https
       metric_name_validation_scheme: legacy
       scrape_protocols:
         - OpenMetricsText0.0.1
       metrics_path: '/projects/<project_ID>/service-provider/prometheus/federate'
       params:
         match[]:
           - '{__name__=~".+"}'
       bearer_token: '<static_key_for_service_account>'
       static_configs:
         - targets:
           - 'read.monitoring.<region>.nebius.cloud'
   ```

   In this file, change the following parameters:

   * `bearer_token`: Enter the static key that you [got earlier](#prerequisites).

   * `targets`: Specify the regional endpoint hostname in the format `read.monitoring.<region>.nebius.cloud`, using the ID from the [region list](https://docs.nebius.com/overview/regions.md). For example, for the `us-central1` region, use `read.monitoring.us-central1.nebius.cloud`.

   * `metrics_path`: Specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in the URL.

     Optionally, add a service in the path in the following format:

     ```yaml theme={null}
     metrics_path: '/projects/<project_ID>/buckets/<service>/prometheus/federate'
     ```

     The following services are available:

     * `compute`: metrics related to Compute virtual machines.
     * `gpu`: GPU-related metrics.
     * `nbs`: metrics related to Compute volumes.
     * `sp_storage`: metrics related to Object Storage.
     * `msp`: metrics related to Managed Service for PostgreSQL® and Managed Service for MLflow.

   * `match[]`: optionally specify which data Prometheus collects by filtering for labels or metric names. For example, to collect only metrics with the `disk` prefix, set the following value:

     ```yaml theme={null}
     match[]:
       - '{__name__=~"^disk.*"}'
     ```

   * `scrape_interval`: you can change the interval, but the recommended interval is no less than 15 seconds.

   > [!NOTE]
   >
   > If you need to scrape metrics from multiple regions, create a separate `scrape_config` job for each region, with that region's endpoint in `targets` and that region's [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in `metrics_path`.

4. Start Prometheus:

   ```bash theme={null}
   ./prometheus --config.file=prometheus.yml
   ```

## How to shard large scraping jobs

If a scraping job needs to return a large amount of data, shard (split) it into several jobs.

Use sharding when any of the following is true:

* Prometheus takes too long to retrieve metrics because one job requests too many time series.
* A large scraping job intermittently times out or becomes unreliable.
* You expect your cluster to grow significantly and want to avoid reworking the Prometheus configuration later.

To shard a scraping job, create multiple `scrape_configs` entries that use the same `metrics_path` but different `match[]` selectors. Make the selectors non-overlapping so that the same metric is not collected more than once.

> For example, when you collect only GPU metrics, split the requests by the `uuid` label:
>
> ```yaml theme={null}
> scrape_configs:
>  - job_name: 'Nebius Observability: GPU metrics, shard 1'
>    honor_labels: true
>    scrape_interval: 15s
>    scheme: https
>    metrics_path: '/projects/<project_ID>/buckets/gpu/prometheus/federate'
>    params:
>      match[]:
>        - '{uuid=~"GPU-[0-7].*"}'
>    bearer_token: '<static_key_for_service_account>'
>    static_configs:
>      - targets:
>        - 'read.monitoring.<region>.nebius.cloud'
>
>  - job_name: 'Nebius Observability: GPU metrics, shard 2'
>    honor_labels: true
>    scrape_interval: 15s
>    scheme: https
>    metrics_path: '/projects/<project_ID>/buckets/gpu/prometheus/federate'
>    params:
>      match[]:
>        - '{uuid=~"GPU-[8-9a-f].*"}'
>    bearer_token: '<static_key_for_service_account>'
>    static_configs:
>      - targets:
>        - 'read.monitoring.<region>.nebius.cloud'
>
>  - job_name: 'Nebius Observability: GPU metrics, shard 3'
>    honor_labels: true
>    scrape_interval: 15s
>    scheme: https
>    metrics_path: '/projects/<project_ID>/buckets/gpu/prometheus/federate'
>    params:
>      match[]:
>        - '{uuid=""}'
>    bearer_token: '<static_key_for_service_account>'
>    static_configs:
>      - targets:
>        - 'read.monitoring.<region>.nebius.cloud'
> ```

Choose one sharding strategy and use it consistently. For example, split requests by service, by metric name prefix or by a stable label that clearly partitions your infrastructure.

## How to explore and manage metrics

Open [http://localhost:9090](http://localhost:9090) in your browser and explore the metrics by using [PromQL queries](https://prometheus.io/docs/prometheus/latest/querying/basics/).

For example, to get all metrics related to Compute virtual machines, enter the following query:

```
{instance_id=~"computeinstance-.*"}
```

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
