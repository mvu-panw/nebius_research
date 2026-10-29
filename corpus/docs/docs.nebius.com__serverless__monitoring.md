# Metrics for endpoints and jobs

Source: https://docs.nebius.com/serverless/monitoring

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Metrics for endpoints and jobs

You can monitor computing and storage resources of your Serverless AI endpoints and jobs on the dashboards in the Nebius AI Cloud [web console](https://console.nebius.com/). To do so, go to the page of the job or endpoint whose utilization you want to check, and then switch to the **Metrics** tab.

Use the dashboards to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/serverless/pricing-quotas.md) increases and quickly identify anomalies. In case of endpoint and job issues, the dashboards help the Nebius support team investigate the issues.

Data for the dashboards is collected automatically. For more information about metrics collection, see [Monitoring agent on Compute virtual machines](https://docs.nebius.com/observability/agents/monitoring-agent.md).

## Explore the dashboard

Usage data for endpoints and jobs becomes available 5–10 minutes after a resource is created.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## Metrics

Serverless AI reports the same metrics as Compute virtual machines. View them on the **Metrics** tab of your job or endpoint; the underlying VMs aren't shown in Compute. For metric definitions, see [VM metrics](https://docs.nebius.com/compute/monitoring/virtual-machines.md#gpu-monitoring-metrics) and [volume metrics](https://docs.nebius.com/compute/monitoring/volumes.md#disk-monitoring-metrics).
