# How to ingest application-level metrics from Managed Service for Kubernetes® using Prometheus Operator

Source: https://docs.nebius.com/observability/metrics/ingest/prometheus-operator

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest application-level metrics from Managed Service for Kubernetes® using Prometheus Operator

Observability collects system metrics for your Managed Service for Kubernetes cluster and nodes. You can also send application-level metrics by using the [Prometheus Operator](https://prometheus-operator.dev/docs/getting-started/introduction/). The Operator manages Prometheus clusters atop Kubernetes.

## Prerequisites

1. If you don’t have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `editors`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it later in the configuration steps.

## How to start ingesting metrics

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

4. Install and update the Prometheus Monitoring Community repository with Helm charts:

   ```bash theme={null}
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

5. Customize the [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/README.md) chart:

   1. Open the `values.yaml` file:

      ```bash theme={null}
      helm show values prometheus-community/kube-prometheus-stack > values.yaml
      ```

   2. Paste the following configuration into the `values.yaml`:

      ```yaml theme={null}
      grafana:
        enabled: false

      alertmanager:
        enabled: false

      prometheus:
        agentMode: true

        prometheusSpec:
          remoteWrite:      # Configure Prometheus to write scraped samples to a remote endpoint
            - name: Nebius
              url: https://write.monitoring.<region_ID>.nebius.cloud/projects/<project_ID>/prometheus/api/v1/write
              authorization:
                credentials:
                  name: nebius-o11y-token
                  key: token
      ```

      In this configuration, specify your region ID from the [region list](https://docs.nebius.com/overview/regions.md), and your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

      The configuration disables the bundled Grafana® and Alertmanager components, runs Prometheus in [agent mode](https://prometheus.io/blog/2021/11/16/agent/) and configures a write endpoint to push metrics to Observability Metrics.

6. Install the chart:

   ```bash theme={null}
   helm install prometheus-stack prometheus-community/kube-prometheus-stack \
     --namespace observability \
     --values values.yaml
   ```

7. Check the installation:

   ```bash theme={null}
   kubectl get pods --namespace observability
   ```

Now, Prometheus writes application-level metrics from your Managed Service for Kubernetes cluster to Observability Metrics.
