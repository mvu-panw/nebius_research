# Monitoring clusters and nodes in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/monitoring

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring clusters and nodes in Managed Service for Kubernetes®

You can monitor Managed Service for Kubernetes cluster and nodes states on the dashboards in the Nebius AI Cloud web console.

Use the dashboards to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/kubernetes/resources/quotas-limits.md) increases and quickly identify anomalies. In case of issues with your cluster, dashboards help the Nebius support team investigate the issue.

Data for the dashboards is collected automatically. For more information about metrics collection, see [Monitoring agent on Compute virtual machines](https://docs.nebius.com/observability/agents/monitoring-agent.md).

## Explore the dashboards

The cluster usage data becomes available 5–10 minutes after nodes are created in the cluster. You can view it on the **Monitoring** tab of the cluster and the node group pages.

You can select specific nodes to check their health separately. On the cluster monitoring page, you can also select specific node groups.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## Monitoring metrics

Managed Service for Kubernetes nodes are hosted by Compute virtual machines and produce the same metrics. You can read about them in [Monitoring virtual machines in Nebius AI Cloud](https://docs.nebius.com/compute/monitoring/virtual-machines.md).
