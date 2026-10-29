# How to ingest metrics into Nebius AI Cloud Observability

Source: https://docs.nebius.com/observability/metrics/ingest

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest metrics into Nebius AI Cloud Observability

To ingest your metrics into Nebius AI Cloud Observability, follow these steps:

1. If you want to ingest time series, [prepare your data](#prepare-time-series) in the correct format.

2. [Choose a way to ingest your metrics](#ingestion-methods) depending on the resource from which you collect them.

3. (Optional) [Connect Grafana®](#connect-grafana-to-view-your-own-metrics) to visualize your metrics.

## Ingestion methods

Choose how to ingest your metrics into the Observability service based on the type of resource from which you want to collect metrics:

* Managed Service for Kubernetes® cluster:

  * Recommended: [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/metrics/ingest/nebius-o11y-agent.md)
  * [Prometheus Operator](https://docs.nebius.com/observability/metrics/ingest/prometheus-operator.md)

* [Prometheus instance](https://docs.nebius.com/observability/metrics/ingest/prometheus-instance.md)

* [Vector instance](https://docs.nebius.com/observability/metrics/ingest/vector-instance.md)

## Prepare time series

One of the types of data you can ingest is a time series. A time series consists of ordered `timestamp, number` pairs and follows the [Prometheus time series format](https://prometheus.io/docs/concepts/data_model/). Each time series has a metric name and a set of labels (key-value pairs).

For example, in `device{operation="create"}`, `device` is the metric name, and `operation="create"` is the label. If you change a label value, for example, from `{operation="create"}` to `{operation="delete"}`, it results in a different time series.

> [!WARNING]
>
> Nebius AI Cloud supports time series with up to 46 labels. If this limit is exceeded, the time series is not stored, although the service still responds with `OK`.

To avoid data loss, keep your label sets compact and meaningful:

* Avoid high-cardinality labels that use too many different values, such as usernames or emails.
* Consider pre-aggregating metrics or using static identifiers where possible.

## Connect Grafana to view your own metrics

> [!NOTE]
>
> This method only works for metrics that you ingest yourself. To visualize in Grafana metrics provided by Nebius AI Cloud, see [Grafana](https://docs.nebius.com/observability/metrics/grafana.md).

After you ingest metrics from your resources, you can configure Grafana to view them by using one of these ways:

**Install Nebius application**

Install the [Grafana solution by Nebius](https://console.nebius.com/applications/overview/nebius/grafana-solution-by-nebius), an application for Managed Service for Kubernetes®. The application is configured to receive metrics.

**Connect data source in Grafana**

1. If you do not have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `editors`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it later in the configuration steps.

4. Make sure that you have Grafana available, in any of these ways:

   * [Install Grafana on your local machine](https://grafana.com/docs/grafana/latest/setup-grafana/installation/).
   * [Create an account in Grafana Cloud](https://grafana.com/auth/sign-up/create-user).

5. Open Grafana in your browser.

6. In the side menu, select **Connections** → **Data sources**.

7. Click **Add new data source**.

8. Select **Prometheus**.

9. In the Prometheus configuration, enter the following settings:

   * **Connection** → **Prometheus server URL**: `https://read.monitoring.api.nebius.cloud/projects/<project_ID>/prometheus`.

     In the URL, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * **Authentication** → **HTTP headers**: click **Add header** and enter `Authorization` and the value of the static key that you got earlier.

10. Click **Save and test**. If Prometheus is connected successfully, you should see the "Successfully queried the Prometheus API" message.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
