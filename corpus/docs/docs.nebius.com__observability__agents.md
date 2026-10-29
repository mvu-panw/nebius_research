# Observability agents

Source: https://docs.nebius.com/observability/agents

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Observability agents

Nebius AI Cloud Observability uses two agents for different purposes:

* [Monitoring agent](https://docs.nebius.com/observability/agents/monitoring-agent.md) collects system metrics from virtual machines and Managed Service for Kubernetes® nodes for visualization on preconfigured dashboards. It can also [collect journald logs from VMs](https://docs.nebius.com/observability/logs/journald.md).

* [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md) ingests logs from Managed Service for Kubernetes clusters into Observability.

See the detailed comparison of the two agents below:

| Feature | **Nebius Observability Agent for Kubernetes** | **Monitoring agent** |
| - | - | - |
| **Purpose** | Ingests logs from Managed Service for Kubernetes clusters into Observability | Collects system-level metrics (CPU, RAM, GPU, etc.) and journald logs from Compute VMs |
| **Deployed on** | Managed Service for Kubernetes clusters | Compute virtual machines and Managed Service for Kubernetes nodes |
| **Collected data** | Application and infrastructure logs | System metrics (for example, GPU, vCPU, memory and OS) and journald logs |
| **Installation** | Manual (via Helm chart) | Automatic (preinstalled on new VMs and Managed Kubernetes nodes) |
| **Components** | Helm chart with the log collection agent | `nebius-observability-agent`, `nebius-observability-agent-updater` |
| **Data enrichment** | Adds metadata: cluster ID, pod name, container image tag, etc. | Adds labels: resource ID, project ID, etc. |
| **Data destination** | Observability Logs | Observability Metrics (web console dashboards) |
| **Management** | Version controlled via Helm and customizable installation | Managed via SSH, supports disabling updates |
| **Use case** | Centralized log ingestion for observability and troubleshooting | Visual monitoring of infrastructure resource usage |
