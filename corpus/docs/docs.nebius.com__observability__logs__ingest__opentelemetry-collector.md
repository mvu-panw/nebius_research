# How to ingest Managed Service for Kubernetes® logs with OpenTelemetry Collector

Source: https://docs.nebius.com/observability/logs/ingest/opentelemetry-collector

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest Managed Service for Kubernetes® logs with OpenTelemetry Collector

To ingest your Managed Service for Kubernetes cluster logs into Observability Logs, install the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) and create a ConfigMap with its settings.

## Prerequisites

1. If you don’t have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `editors`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it later in the configuration steps.

## Install and configure OpenTelemetry Collector

1. [Connect to your Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/connect.md).

2. Create a namespace for the observability components:

   ```bash theme={null}
   kubectl create namespace observability
   ```

3. Create a Kubernetes Secret for your token:

   ```bash theme={null}
   kubectl create secret generic nebius-o11y-token \
     --from-literal token=<token_value> --namespace observability
   ```

   In this command, specify the `token` value of the static key that you [got earlier](#prerequisites).

4. Create a ConfigMap with OpenTelemetry Collector settings:

   ```bash theme={null}
   kubectl create configmap nebius-otel-config \
     --from-literal=project-id=<project_ID> \
     --from-literal=endpoint=write.logging.<region_ID>.nebius.cloud:443 \
     --namespace observability
   ```

   In this command, specify your region ID from the [region list](https://docs.nebius.com/overview/regions.md), and your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

5. Install and update the OpenTelemetry repository with Helm charts:

   ```bash theme={null}
   helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
   helm repo update
   ```

6. Install the [opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-collector) chart:

   ```bash theme={null}
   helm install otel-collector open-telemetry/opentelemetry-collector \
     --namespace observability \
     --values https://raw.githubusercontent.com/nebius/observability/8f4913657058cbc81b3b4630a48b3641e642c910/charts/otel-collector/values/values-daemonset.yaml
   ```

7. Check the installation:

   ```bash theme={null}
   kubectl get pods --namespace observability
   ```

Now, OpenTelemetry Collector writes logs from your Managed Service for Kubernetes cluster to Observability Logs. Logs appear in the `default` bucket.

> [!TIP]
>
> [Connect Grafana®](https://docs.nebius.com/observability/logs/grafana.md) to view ingested logs within it.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
