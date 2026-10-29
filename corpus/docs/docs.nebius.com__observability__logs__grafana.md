# How to view logs in Grafana®

Source: https://docs.nebius.com/observability/logs/grafana

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to view logs in Grafana®

To view visualized log data in Grafana®, connect Grafana to Observability Logs and query the data using LogQL. Logs support LogQL with some [restrictions](https://docs.nebius.com/observability/logs/query-language.md).

## Prerequisites

1. If you don't have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant. For example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `viewers`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it for later steps.

## How to connect Grafana

Use one of these ways:

**Install Nebius application**

Install the [Grafana solution by Nebius](https://console.nebius.com/applications/overview/nebius/grafana-solution-by-nebius), an application for Managed Service for Kubernetes®. The application is configured to view logs.

**Connect a data source in Grafana**

1. Make sure that you have Grafana available, in any of these ways:
   * [Install Grafana on your local machine](https://grafana.com/docs/grafana/latest/setup-grafana/installation/).
   * [Create an account in Grafana Cloud](https://grafana.com/auth/sign-up/create-user).

2. Open Grafana in your browser.

3. In the side menu, select **Connections** → **Data sources**.

4. Click **Add new data source**.

5. Select **Loki**.

6. In the Loki configuration, enter the following settings:

   * **Connection** → **URL**: `https://read.logging.api.nebius.cloud/projects/<project_ID>`.
     In the URL, specify your [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * **Authentication** → **HTTP headers**: click **Add header** and enter `Authorization` and the value of the static key that you [got earlier](#prerequisites).

7. Click **Save and test**. If Loki is connected successfully, you should see the "Data source successfully connected" message.

## How to explore and manage logs

Explore the logs: construct [LogQL](https://docs.nebius.com/observability/logs/query-language.md) queries using **Builder** or create dashboards to visualize logs. Currently, the only supported stream selector label is `__bucket__`. It can have the following values:

* `sp_serial`: Compute virtual machines (serial logs)
* `sp_mk8s_control_plane`: Managed Kubernetes clusters (control plane logs)
* `sp_mk8s_audit_logs`: Managed Kubernetes clusters (audit logs)
* `sp_mlflow`: Managed MLflow clusters
* `sp_postgres`: Managed PostgreSQL clusters
* `sp_k8srelease`: applications for Managed Kubernetes
* `default`: [user-ingested logs](https://docs.nebius.com/observability/logs/ingest/index.md)

### Basic log search

Find deadlocks in a Managed Service for PostgreSQL® cluster:

```
{__bucket__="sp_postgres"} |= `deadlock detected`
```

### Filter by log level

```
{__bucket__="default"} | level="error"
```

### Exclude noisy entries

```
{__bucket__="sp_postgres"} |= `ERROR` != `vacuum` != `healthcheck`
```

For the full query syntax, see the [LogQL query language](https://docs.nebius.com/observability/logs/query-language.md) reference.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
