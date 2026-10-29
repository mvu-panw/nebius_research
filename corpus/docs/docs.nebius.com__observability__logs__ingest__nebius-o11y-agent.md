# How to ingest Managed Service for Kubernetes® logs with the Nebius Observability Agent for Kubernetes

Source: https://docs.nebius.com/observability/logs/ingest/nebius-o11y-agent

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest Managed Service for Kubernetes® logs with the Nebius Observability Agent for Kubernetes

Nebius Observability Agent for Kubernetes collects workload logs (Pod logs) from your Managed Service for Kubernetes cluster and forwards them to Observability Logs.

To install the Nebius Observability Agent for Kubernetes in your Managed Service for Kubernetes cluster, follow the guide in [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md).

By default, the agent automatically collects logs from all workloads in your cluster. After [installation](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md#installation), logs will appear in the `default` bucket in Observability Logs.

> [!TIP]
>
> [Connect Grafana®](https://docs.nebius.com/observability/logs/grafana.md) to view ingested logs within it.

## Log collection configuration

You can customize log collection by creating a `values.yaml` file and updating your Nebius Observability Agent for Kubernetes installation:

```bash theme={null}
helm upgrade nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
  --version $(curl https://artifacts.nebius.cloud/nebius-observability-agent/nebius-observability-agent-helm/latest-release) \
  --namespace observability \
  --values values.yaml
```

### Basic log configuration

```yaml theme={null}
config:
  logs:
    enabled: true
    collectAgentLogs: false
    excludedNamespaces:
      - kube-system
```

### Configuration parameters

* `config.logs.enabled`: Enable or disable log collection. Default: `true`.
* `config.logs.collectAgentLogs`: Parameter to collect logs from the Nebius Observability Agent for Kubernetes itself. Default: `false`.
* `config.logs.excludedNamespaces`: List of namespaces to exclude from log collection.

### Excluding namespaces

To avoid collecting logs from infrastructure or monitoring namespaces, exclude specific namespaces from the log collection:

```yaml theme={null}
config:
  logs:
    enabled: true
    collectAgentLogs: false
    excludedNamespaces:
      - kube-system
      - monitoring
      - cert-manager
      - istio-system
```

## Data enrichment

The Nebius Observability Agent for Kubernetes enriches logs with the following metadata:

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
* `k8s.container.restart_count`: Number of the container restarts in the Pod
* `k8s_pod_uid`: Pod unique identifier

## Troubleshooting

If you encounter issues with log or metric collection, do the following:

1. Verify the agent is running:

   ```bash theme={null}
   kubectl get pods --namespace observability
   ```

2. Check agent logs for errors:

   ```bash theme={null}
   kubectl logs <Pod_name> --namespace observability
   ```

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
