# Tracing in Nebius AI Cloud

Source: https://docs.nebius.com/observability/tracing

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Tracing in Nebius AI Cloud

The Tracing service provides storage for traces, an API to write them and tools to visualize them in Grafana®.

The write API uses the OpenTelemetry format, with open-source SDKs for multiple programming languages. You can write traces through [Nebius Observability Agent for Kubernetes®](https://docs.nebius.com/observability/traces/ingest.md) or directly to [Tracing writers](https://docs.nebius.com/observability/traces/direct-ingest.md), and view them in [Grafana](https://docs.nebius.com/observability/traces/grafana.md) by connecting a data source.

Trace data is stored per project. Traces can be linked and viewed across all projects within a tenant for cross-project visibility.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
