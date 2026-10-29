# How to ingest metrics with Nebius Observability Agent for Kubernetes®

Source: https://docs.nebius.com/observability/metrics/ingest/nebius-o11y-agent

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest metrics with Nebius Observability Agent for Kubernetes®

Nebius Observability Agent for Kubernetes collects workload metrics from your Managed Service for Kubernetes® cluster and forwards them to Observability Metrics.

## Prerequisites

1. [Create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and [connect to it](https://docs.nebius.com/kubernetes/connect.md) by using `kubectl`.
2. [Install Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md).

## Update the agent

To enable metrics collection, create a `values.yaml` file and update your Nebius Observability Agent for Kubernetes installation:

1. Create a `values.yaml` file with metrics configuration:

   ```yaml theme={null}
   config:
     metrics:
       enabled: true
       collectAgentMetrics: false
       collectK8sClusterMetrics: false
   ```

2. Update your Nebius Observability Agent for Kubernetes installation:

   ```bash theme={null}
   helm upgrade nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
     --version $(curl https://artifacts.nebius.cloud/nebius-observability-agent/nebius-observability-agent-helm/latest-release) \
     --namespace observability \
     --values values.yaml
   ```

### Configuration parameters

* `config.metrics.enabled`: Enable or disable metrics collection. Default: `true`.
* `config.metrics.collectAgentMetrics`: Parameter to collect metrics from the Nebius Observability Agent for Kubernetes itself. Default: `false`.
* `config.metrics.collectK8sClusterMetrics`: Enable collection of Kubernetes infrastructure metrics (API servers, nodes, cAdvisor, Hubble). Default: `false`.
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

### Excluding namespaces

To exclude specific namespaces from metrics collection, add them to the `excludedNamespaces` list in the configuration:

```yaml theme={null}
config:
  metrics:
    enabled: true
    collectAgentMetrics: false
    excludedNamespaces:
      - kube-system
      - monitoring
      - cert-manager
      - istio-system
```

### Collecting both logs and metrics

To collect both [logs](https://docs.nebius.com/observability/logs/ingest/index.md) and metrics, extend the configuration:

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

## Collected targets

Nebius Observability Agent for Kubernetes automatically discovers and collects metrics from multiple Kubernetes targets:

### Service endpoints targets

* ***kubernetes-service-endpoints*** (scrape interval: 15s)

  Collects metrics from Kubernetes services with `prometheus.io/scrape: "true"` annotation. This target discovers services and scrapes their endpoints.

* ***kubernetes-service-endpoints-slow*** (scrape interval: 5m)

  Collects metrics from services with `prometheus.io/scrape_slow: "true"` annotation for less frequent scraping with extended timeout (30s).

### Pod targets

* ***kubernetes-pods*** (scrape interval: 15s)

  Collects metrics directly from Pods with `prometheus.io/scrape: "true"` annotation. Only scrapes Pods running on the same node as the agent (node-local collection).

* ***kubernetes-pods-slow*** (scrape interval: 5m)

  Collects metrics from Pods with `prometheus.io/scrape_slow: "true"` annotation for less frequent scraping with extended timeout (30s).

### (Optional) Kubernetes infrastructure targets

When `collectK8sClusterMetrics` is enabled, Nebius Observability Agent for Kubernetes also collects:

* ***kubernetes-apiservers***

  Collects metrics from Kubernetes API servers for cluster health monitoring.

* ***kubernetes-nodes***

  Collects node-level metrics via kubelet `/metrics` endpoint, including node resource usage and status.

* ***kubernetes-nodes-cadvisor***

  Collects container metrics via kubelet `/metrics/cadvisor` endpoint, providing detailed container resource usage.

* ***hubble*** (scrape interval: 15s)

  Collects network observability metrics from Cilium Hubble in the `kube-system` namespace, if available.

### Custom targets

* ***additionalTargets***

  User-defined custom scrape targets that can be configured via `config.metrics.additionalTargets` in the Helm values.

### Target filtering

* **Namespace filtering**: Targets in namespaces listed in `excludedNamespaces` are automatically excluded.
* **Node locality**: Pod and node targets are filtered to only collect metrics from the same node where the agent is running.
* **Pod state filtering**: Pods in `Pending`, `Succeeded`, `Failed` or `Completed` states are excluded from collection.

### Annotation requirements

For service and Pod targets to be discovered, they must have proper Prometheus annotations:

| Annotation | Required | Description | Default |
| - | - | - | - |
| `prometheus.io/scrape` | Yes | Enable metrics scraping | - |
| `prometheus.io/port` | Yes | Port number for metrics endpoint | - |
| `prometheus.io/path` | No | Metrics endpoint path | `/metrics` |
| `prometheus.io/scheme` | No | HTTP scheme (http/https) | `http` |
| `prometheus.io/scrape_slow` | No | Enable slow scraping (5m interval) | - |

## Data enrichment

The Nebius Observability Agent for Kubernetes enriches metrics with the following metadata:

* `k8s_cluster_id`: Cluster ID
* `k8s_node_group_id`: Node group ID
* `app.kubernetes.io/name`: Application name label
* `k8s.namespace.name`: Namespace name
* `k8s.deployment.name`: Deployment name (if applicable)
* `k8s.statefulset.name`: StatefulSet name (if applicable)
* `k8s.daemonset.name`: DaemonSet name (if applicable)
* `k8s.cronjob.name`: CronJob name (if applicable)
* `k8s.job.name`: Job name (if applicable)
* `k8s.node.name`: Node name
* `k8s.pod.name`: Pod name
* `k8s.pod.start_time`: Pod start time
* `container.image.tag`: Container image tag
* `k8s.container.restart_count`: Restart count of the container in the Pod
* `k8s_pod_uid`: Pod unique identifier

## Pod annotations for metrics scraping

For the Nebius Observability Agent for Kubernetes to scrape metrics from your applications, Pods must have the following annotations:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-application
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  ...
```

### Required annotations

* `prometheus.io/scrape`: Set to `"true"` to enable metrics scraping for this Pod.
* `prometheus.io/port`: The port number where your application exposes metrics (as a string).
* `prometheus.io/path`: The path where metrics are available. Default: `/metrics`.

### Example deployment with annotations

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 8080
```

Without these annotations, the Nebius Observability Agent for Kubernetes will not automatically discover and scrape metrics from your applications.

## Troubleshooting

If you encounter issues with metrics collection:

1. Verify that the agent is running:

   ```bash theme={null}
   kubectl get pods --namespace observability
   ```

2. Check agent logs for errors:

   ```bash theme={null}
   kubectl logs <Pod_name> --namespace observability
   ```

3. Check the status of targets by using Prometheus API exposed by the agent:

   1. Run the following command to forward the port to your local machine:

      ```bash theme={null}
      kubectl --namespace observability port-forward pod/<Pod_name> 8080:8080
      ```

   2. Open [http://127.0.0.1:8080/api/v1/targets](http://127.0.0.1:8080/api/v1/targets) in your browser to inspect the targets that the agent currently scrapes. For more details, see the `api/v1/targets` [Prometheus documentation](https://prometheus.io/docs/prometheus/latest/querying/api/#targets).
