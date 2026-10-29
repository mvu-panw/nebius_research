# How to ingest Managed Service for Kubernetes® logs into Observability Logs

Source: https://docs.nebius.com/observability/logs/ingest

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest Managed Service for Kubernetes® logs into Observability Logs

To ingest your Managed Service for Kubernetes cluster logs into Observability Logs, choose one of the following options:

* [Nebius Observability Agent for Kubernetes](#nebius-observability-agent-for-kubernetes-recommended)
* [OpenTelemetry Collector](#opentelemetry-collector)

## Nebius Observability Agent for Kubernetes (Recommended)

Nebius Observability Agent for Kubernetes is a Helm chart developed and maintained by Nebius AI Cloud, specifically designed for Managed Service for Kubernetes clusters.

Nebius Observability Agent for Kubernetes provides:

* Out-of-the-box log collection with minimal configuration
* Built-in log enrichment (for example, adds cluster ID and other metadata)
* High reliability and tight integration with Nebius AI Cloud

[How to ingest logs with Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/logs/ingest/nebius-o11y-agent.md)

## OpenTelemetry Collector

[OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) is an open-source, vendor-neutral observability framework that supports log collection and forwarding.

This option is ideal for environments where OpenTelemetry is already in use. It offers more flexibility and customization but requires more manual configuration and may not provide the same level of integration or metadata enrichment as the Nebius Observability Agent for Kubernetes.

[How to ingest logs with OpenTelemetry Collector](https://docs.nebius.com/observability/logs/ingest/opentelemetry-collector.md)
