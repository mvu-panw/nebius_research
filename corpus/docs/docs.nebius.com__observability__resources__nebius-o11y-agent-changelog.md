# Nebius Observability Agent for Kubernetes® changelog

Source: https://docs.nebius.com/observability/resources/nebius-o11y-agent-changelog

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius Observability Agent for Kubernetes® changelog

Nebius Observability Agent for Kubernetes is the recommended way to ingest logs, metrics and traces from Managed Service for Kubernetes® into Nebius AI Cloud. For more details, see [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md).

**v1.0.9**

2026-09-28

### Added

* Service provider metrics from Managed Service for Kubernetes add-ons, such as Cilium and Hubble. The agent sends them to the [metrics provided by Nebius AI Cloud](https://docs.nebius.com/observability/metrics/grafana.md). In the [Grafana® solution by Nebius](https://console.nebius.com/applications/overview/nebius/grafana-solution-by-nebius), you can find them in the **Nebius Services** data source. Dashboards for these metrics will be added to the Grafana solution by Nebius later.

**v1.0.8**

2026-08-12

### Added

* Configuration parameters `config.metrics.batch.maxSizeBytes` and `config.metrics.batch.maxSizeMessages` to cap the size of a single metrics export request. Defaults: `62914560` (60 MiB) and `500000` data points.

### Fixed

* Fixed a bug where a batch of metrics exceeding the ingester request size limit could get stuck in the sending queue and block metrics delivery. Batches are now split based on the caps before sending.

**v1.0.7**

2026-06-30

### Fixed

* Fixed a bug where the Helm chart generated an invalid configuration when the logs pipeline was disabled (for example, metrics-only or traces-only setups).

**v1.0.6**

2026-06-12

### Added

* Configuration parameter `config.metrics.labelAllowlist` to control which labels from Pod, Service and Node objects are attached to scraped metrics. Each field (`podLabels`, `serviceLabels`, `nodeLabels`) is a regular expression matched against label names. Default: `".+"` (all labels are attached, same as before).

  Use it to bound label cardinality: metrics with more than 33 labels are silently dropped, and clusters with many labels on Node objects (for example, added by Node Feature Discovery or GPU Operator) or on Service objects can exceed this limit.

  Example configuration that limits labels from Node objects to a curated allowlist:

  ```yaml theme={null}
  config:
    metrics:
      labelAllowlist:
        podLabels: ".+"
        serviceLabels: ".+"
        nodeLabels: "kubernetes_io_hostname|topology_kubernetes_io_.*|node_kubernetes_io_instance_type|nvidia_com_gpu_present|nebius_com_.*"
  ```

### Fixed

* Removed the `k8s.node_group.id` label from kube-apiserver and etcd metrics. These metrics are cluster-wide, but each agent stamped them with its own node group ID, multiplying every `apiserver_*` and `etcd_*` time series by the number of node groups in the cluster and inflating the active time series count. Metrics local to a node keep the label.

**v1.0.5**

2026-01-30

### Added

* Traces collection and forwarding to Nebius AI Cloud. For more details, see [How to ingest traces with Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/traces/ingest.md).
* Configuration parameter `config.traces.enabled` to enable or disable trace collection. Default: `true`.
* OTLP endpoint for receiving traces from applications at `nebius-observability-agent.<namespace>.svc.cluster.local:4317`, where `<namespace>` is the Managed Service for Kubernetes namespace where the agent is installed (default: `observability`).

Example configuration to enable traces:

```yaml theme={null}
config:
  traces:
    enabled: true
```

**v1.0.4**

2025-09-02

### Fixed

* Fixed a wrong image tag in the Helm chart.

**v1.0.3**

2025-09-01

### Added

* Support for setting the metadata region in Helm values for Managed Service for Kubernetes clusters not running on Compute VMs.

* Configuration parameter `metadata.region` (for example, `eu-north1`) to specify the region when automatic detection is not available.

* Configuration parameter `metadata.parent_id` (for example, `project-e00abcde...`) to specify the parent project ID.

* Required setup commands for authentication:

  * `nebius iam auth-public-key generate --service-account-id {targetSaId} --output credentials.json`
  * `kubectl create secret --namespace=observability generic iam-credentials-file --from-file=credentials.json`

* The target service account (`target-sa-id`) must be granted the following permissions:

  * `logging.logs.writer` for sending logs to Observability Logs
  * `monitoring.metrics.writer` for sending metrics to Observability Metrics

Example configuration for clusters not running on Compute VMs:

```yaml theme={null}
config:
  iam:
    auth_scheme: "iam-credentials-file"
    credentials_file_secret_name: "iam-credentials-file"
    credentials_file_secret_key: "credentials.json"
  metadata:
    region: "eu-north1"
    parent_id: "project-e00abcde..."
```

**v1.0.2**

2025-08-12

### Added

* Metrics collection capability for Managed Service for Kubernetes workloads.
* Metrics forwarding to Observability Metrics.
* Configurable settings to choose between logs only, metrics only or both.
* Parameter to exclude agent logs from collection (`config.logs.collectAgentLogs: false`).
* Parameter to exclude agent metrics from collection (`config.metrics.collectAgentMetrics: false`).
* Metrics enrichment with cluster ID, node group ID and other Managed Service for Kubernetes metadata.

**v1.0.1**

2025-06-03

### Added

* Helm chart for Managed Service for Kubernetes.
* Out-of-the-box log collection from Managed Service for Kubernetes into Observability Logs with minimal configuration.
* Log enrichment (for example, cluster ID and metadata injection).
* Reliability features.
