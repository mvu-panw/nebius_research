# How to use Grafana® to view metrics provided by Nebius AI Cloud

Source: https://docs.nebius.com/observability/metrics/grafana

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to use Grafana® to view metrics provided by Nebius AI Cloud

To view visualized metrics in Grafana dashboards, connect Grafana to Observability Metrics and query the data by using [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/).

> [!NOTE]
>
> This method only works for metrics provided by Nebius AI Cloud. To visualize your own metrics in Grafana, see [Connect Grafana to view your own metrics](https://docs.nebius.com/observability/metrics/ingest/index.md#connect-grafana-to-view-your-own-metrics).

## Prerequisites

1. If you don't have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant. For example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `viewers`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it for later steps.

## How to connect Grafana data source

Use one of these ways:

**Install Nebius application**

Install the [Grafana solution by Nebius](https://console.nebius.com/applications/overview/nebius/grafana-solution-by-nebius), an application for Managed Service for Kubernetes®. The application is configured to receive metrics.

**Connect a data source in Grafana**

1. Make sure that you have Grafana available, in any of these ways:
   * [Install Grafana on your local machine](https://grafana.com/docs/grafana/latest/setup-grafana/installation/).
   * [Create an account in Grafana Cloud](https://grafana.com/auth/sign-up/create-user).

2. Open Grafana in your browser.

3. In the side menu, select **Connections** → **Data sources**.

4. Click **Add new data source**.

5. Select **Prometheus**.

6. In the Prometheus configuration, enter the following settings:

   * **Connection** → **Prometheus server URL**: `https://read.monitoring.api.nebius.cloud/projects/<project_ID>/service-provider/prometheus`.

     In the URL, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * **Authentication** → **HTTP headers**: click **Add header** and enter `Authorization` and the value of the static key that you [got earlier](#prerequisites).

7. Click **Save and test**. If Prometheus is connected successfully, you should see the "Successfully queried the Prometheus API" message.

## How to explore and manage metrics

Explore the metrics: construct [PromQL queries](https://prometheus.io/docs/prometheus/latest/querying/basics/) by using **Builder** or create dashboards to visualize metrics.

For example, if you are looking to optimize costs, find virtual machines with consistently underutilized CPUs. Enter the following query:

```
{"system.cpu.load_average.15m", instance_id=~"computeinstance-.*"}
```

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
