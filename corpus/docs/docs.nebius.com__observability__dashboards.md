# Service dashboards

Source: https://docs.nebius.com/observability/dashboards

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Service dashboards

You can monitor Nebius AI Cloud resources on the preconfigured dashboards that are available in the [web console](https://console.nebius.com) or in Grafana®.

## Dashboards in the Nebius AI Cloud web console

You can view the metrics of Nebius AI Cloud resources on preconfigured dashboards in the [web console](https://console.nebius.com). There are two ways to find the required dashboard:

* Go to  **Observability** → [Metrics](https://console.nebius.com/observability/metrics) and select the resource you would like to review.
* Go to the page of the resource you would like to review and switch to the **Metrics** tab.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

The metrics displayed on the dashboards depend on the resource type. To view more metrics and create advanced visualizations, integrate Observability Metrics with [Prometheus](https://docs.nebius.com/observability/metrics/prometheus.md) or [Grafana®](https://docs.nebius.com/observability/metrics/grafana.md).

## Dashboards in the Grafana Marketplace

Nebius AI Cloud provides [pre-built Grafana dashboards](https://grafana.com/orgs/nebius/dashboards) available on the Grafana website.

The pre-built dashboards are also included in the [Grafana solution by Nebius](https://console.nebius.com/applications/overview/nebius/grafana-solution-by-nebius), an application for Managed Service for Kubernetes®.

## Installing a dashboard in Grafana

1. Connect the [Prometheus data source](https://docs.nebius.com/observability/metrics/grafana.md#how-to-connect-grafana-data-source).
2. [Import the dashboard into a Grafana instance](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/import-dashboards/) by either copying the dashboard ID or uploading the dashboard JSON file.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
