# Nebius Observability Agent for Kubernetes®

Source: https://docs.nebius.com/observability/agents/nebius-o11y-agent

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius Observability Agent for Kubernetes®

[Nebius Observability Agent for Kubernetes](https://console.nebius.com/applications/overview/nebius/nebius-observability-agent) is a Helm chart developed and maintained by Nebius AI Cloud, specifically designed for Managed Service for Kubernetes® clusters.

Nebius Observability Agent for Kubernetes provides:

* Out-of-the-box metrics collection with minimal configuration
* Built-in metric enrichment (for example, adds cluster ID and other metadata)
* High reliability and tight integration with Nebius AI Cloud
* Unified observability agent that can collect logs, metrics and traces

## Installation

### Basic installation

1. [Connect to your Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/connect.md).

2. Install the Nebius Observability Agent for Kubernetes:

   ```bash theme={null}
   helm install nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
     --version $(curl https://artifacts.nebius.cloud/nebius-observability-agent/nebius-observability-agent-helm/latest-release) \
     --namespace observability --create-namespace
   ```

   To use a [specific agent version](https://docs.nebius.com/observability/resources/nebius-o11y-agent-changelog.md), change the `--version` value, for example:

   ```bash theme={null}
   helm install nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
     --version 1.0.4 \
     --namespace observability --create-namespace
   ```

3. Check the installation:

   ```bash theme={null}
   kubectl get pods --namespace observability
   ```

### Installation with custom configuration

To customize the agent configuration, create a `values.yaml` file and install the agent with custom settings:

```bash theme={null}
helm install nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
  --version $(curl https://artifacts.nebius.cloud/nebius-observability-agent/nebius-observability-agent-helm/latest-release) \
  --namespace observability --create-namespace \
  --values values.yaml
```

## Configuration

### Basic configuration

You can customize the Nebius Observability Agent for Kubernetes behavior by creating a `values.yaml` file:

```yaml theme={null}
config:
  logs:
    enabled: true
    collectAgentLogs: false
    excludedNamespaces:
      - kube-system

  metrics:
    enabled: true
    collectAgentMetrics: false
    collectK8sClusterMetrics: false
```

### Configuration parameters

#### Log collection settings

* `config.logs.enabled`: Enable or disable log collection. Default: `true`.
* `config.logs.collectAgentLogs`: Parameter to collect logs from the Nebius Observability Agent for Kubernetes itself. Default: `false`.
* `config.logs.excludedNamespaces`: List of namespaces to exclude from log collection.

#### Metrics collection settings

* `config.metrics.enabled`: Enable or disable metrics collection. Default: `true`.
* `config.metrics.collectAgentMetrics`: Parameter to collect metrics from the Nebius Observability Agent for Kubernetes itself. Default: `false`.
* `config.metrics.collectK8sClusterMetrics`: Parameter to collect Kubernetes cluster-level metrics. Default: `false`.
* `config.metrics.excludedNamespaces`: List of namespaces to exclude from metrics collection.
* `config.metrics.labelAllowlist`: Regular expressions that control which labels from Pod, Service and Node objects are attached to scraped metrics. Each field (`podLabels`, `serviceLabels`, `nodeLabels`) is matched against label names.

  > **Example**
  >
  > ```yaml theme={null}
  > config:
  >   metrics:
  >     labelAllowlist:
  >       podLabels: ".+"
  >       serviceLabels: ".+"
  >       nodeLabels: "kubernetes_io_hostname|topology_kubernetes_io_.*|node_kubernetes_io_instance_type|nvidia_com_gpu_present|nebius_com_.*"
  > ```

  Default: `".+"` (all labels are attached).
* `config.metrics.batch.maxSizeBytes`: Maximum size, in bytes, of a single metrics export request. Batches exceeding the limit are split before sending. Default: `62914560` (60 MiB).
* `config.metrics.batch.maxSizeMessages`: Maximum number of data points in a single metrics export request. Batches exceeding the limit are split before sending. Default: `500000`.

#### Traces collection settings

* `config.traces.enabled`: Enable or disable trace collection. Default: `true`.

When traces are enabled, the agent exposes an OTLP endpoint for receiving traces from your applications:

```
nebius-observability-agent.<namespace>.svc.cluster.local:4317
```

Where `<namespace>` is the namespace where the agent is installed (for example, `observability`).

### Full observability configuration

To collect logs, metrics and traces, configure the `values.yaml` file in the following way:

```yaml theme={null}
config:
  logs:
    enabled: true
    collectAgentLogs: false
    excludedNamespaces:
      - kube-system

  metrics:
    enabled: true
    collectAgentMetrics: false
    collectK8sClusterMetrics: false

  traces:
    enabled: true
```

### Logs-only configuration

To collect only logs, configure the `values.yaml` file in the following way:

```yaml theme={null}
config:
  logs:
    enabled: true
    collectAgentLogs: false
    excludedNamespaces:
      - kube-system

  metrics:
    enabled: false
```

### Metrics-only configuration

To collect only metrics, configure the `values.yaml` file in the following way:

```yaml theme={null}
config:
  logs:
    enabled: false

  metrics:
    enabled: true
    collectAgentMetrics: false
    collectK8sClusterMetrics: false
```

### Combined logs and metrics configuration

To collect both logs and metrics, configure the `values.yaml` file in the following way:

```yaml theme={null}
config:
  logs:
    enabled: true
    collectAgentLogs: false
    excludedNamespaces:
      - kube-system

  metrics:
    enabled: true
    collectAgentMetrics: false
    collectK8sClusterMetrics: false
```

### Traces-only configuration

To collect only traces, configure the `values.yaml` file in the following way:

```yaml theme={null}
config:
  logs:
    enabled: false

  metrics:
    enabled: false

  traces:
    enabled: true
```

### Namespace exclusions

By default, the agent excludes the `kube-system` namespace to avoid collecting system-level logs and metrics. You can exclude additional namespaces by adding them to the `excludedNamespaces` list:

```yaml theme={null}
config:
  logs:
    excludedNamespaces:
      - kube-system
      - monitoring
      - cert-manager
      - istio-system

  metrics:
    excludedNamespaces:
      - kube-system
      - monitoring
      - cert-manager
      - istio-system
```

## Updating the agent

To update the Nebius Observability Agent for Kubernetes to a newer version, use the following command:

```bash theme={null}
helm upgrade nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
  --version $(curl https://artifacts.nebius.cloud/nebius-observability-agent/nebius-observability-agent-helm/latest-release) \
  --namespace observability \
  --values values.yaml
```

## Uninstalling the agent

To remove the Nebius Observability Agent for Kubernetes, use the following command:

```bash theme={null}
helm uninstall nebius-observability-agent --namespace observability
```

## Troubleshooting

If you encounter issues with the agent:

1. Check the agent pod status:

   ```bash theme={null}
   kubectl get pods --namespace observability
   kubectl describe pod <Pod_name> --namespace observability
   ```

2. View agent logs:

   ```bash theme={null}
   kubectl logs <Pod_name> --namespace observability
   ```

3. Verify the configuration:

   ```bash theme={null}
   helm get values nebius-observability-agent --namespace observability
   ```

## See also

* [How to ingest metrics with the agent](https://docs.nebius.com/observability/metrics/ingest/nebius-o11y-agent.md)
* [How to ingest logs with the agent](https://docs.nebius.com/observability/logs/ingest/nebius-o11y-agent.md)
* [How to send traces to the agent](https://docs.nebius.com/observability/traces/ingest.md)
* [Agent changelog](https://docs.nebius.com/observability/resources/nebius-o11y-agent-changelog.md)
