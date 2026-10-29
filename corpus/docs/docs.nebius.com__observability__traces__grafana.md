# How to view traces in Grafana®

Source: https://docs.nebius.com/observability/traces/grafana

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to view traces in Grafana®

To view distributed traces that you ingest into Nebius AI Cloud, connect Grafana to Nebius AI Cloud and explore the traces using the Tempo data source.

## Prerequisites

1. If you don't have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant. For example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `viewers`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it for later steps.

## How to connect Grafana

Use one of these ways:

**Install Nebius application**

Install the [Grafana solution by Nebius](https://console.nebius.com/applications/overview/nebius/grafana-solution-by-nebius), an application for Managed Service for Kubernetes. The application is configured to view traces.

**Connect a data source in Grafana**

1. Make sure that you have Grafana available, in any of these ways:

   * [Install Grafana on your local machine](https://grafana.com/docs/grafana/latest/setup-grafana/installation/).
   * [Create an account in Grafana Cloud](https://grafana.com/auth/sign-up/create-user).

2. Open Grafana in your browser.

3. In the side menu, select **Connections** → **Data sources**.

4. Click **Add new data source**.

5. Select **Tempo**.

6. In the Tempo configuration, enter the following settings:

   * **Connection** → **URL**: `https://read.tracing.api.nebius.cloud/projects/<project_ID>/tempo`.

     In the URL, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * **Authentication** → **HTTP headers**: click **Add header** and enter `Authorization` with the value `Bearer <static_token>`, where `<static_token>` is the static key that you [got earlier](#prerequisites).

7. Click **Save and test**. If Tempo is connected successfully, you should see a success message.

## How to explore traces

After connecting Grafana, you can explore traces:

1. In the side menu, select **Explore**.
2. Select the **Tempo** data source.
3. Use the query builder to search for traces by service name, operation, duration, or other attributes.

You can also view traces using Grafana's TraceQL query language. For more information, see [TraceQL implementation by Nebius AI Cloud](https://docs.nebius.com/observability/traces/query-language.md).

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
