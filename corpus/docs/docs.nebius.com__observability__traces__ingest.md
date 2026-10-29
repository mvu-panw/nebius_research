# How to ingest traces with Nebius Observability Agent for Kubernetes®

Source: https://docs.nebius.com/observability/traces/ingest

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest traces with Nebius Observability Agent for Kubernetes®

Nebius Observability Agent for Kubernetes can receive traces from applications in your Managed Service for Kubernetes® clusters via [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otlp/) and forward them to Nebius AI Cloud. You can then view the traces in Grafana® using the Tempo data source.

## Prerequisites

1. If you don't have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant. For example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `viewers`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it for later steps.

1) Create a Managed Kubernetes cluster and [connect to it](https://docs.nebius.com/kubernetes/connect.md) by using `kubectl`.
2) [Install Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md).

## Enable trace collection

To collect traces from your Managed Service for Kubernetes cluster, enable traces in the Nebius Observability Agent for Kubernetes:

1. Create or update your `values.yaml` file:

   ```yaml theme={null}
   config:
     traces:
       enabled: true
   ```

2. Install or upgrade the Nebius Observability Agent for Kubernetes:

   ```bash theme={null}
   helm upgrade --install nebius-observability-agent oci://cr.nebius.cloud/observability/public/nebius-observability-agent-helm \
     --version $(curl https://artifacts.nebius.cloud/nebius-observability-agent/nebius-observability-agent-helm/latest-release) \
     --namespace observability --create-namespace \
     --values values.yaml
   ```

For more details on the agent configuration, see [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md).

## Send traces from your application

When traces are enabled, the Nebius Observability Agent for Kubernetes exposes an OTLP endpoint for receiving traces:

```
nebius-observability-agent.<namespace>.svc.cluster.local:4317
```

Where `<namespace>` is the namespace where the agent is installed (default: `observability`).

### Configure your application

Configure your application to send traces to the OTLP endpoint using OpenTelemetry SDK and OTLP exporter for your programming language:

* [Python](https://opentelemetry.io/docs/languages/python/)
* [Java](https://opentelemetry.io/docs/languages/java/)
* [Go](https://opentelemetry.io/docs/languages/go/)
* [JavaScript / Node.js](https://opentelemetry.io/docs/languages/js/)
* [.NET](https://opentelemetry.io/docs/languages/net/)
* [Ruby](https://opentelemetry.io/docs/languages/ruby/)
* [PHP](https://opentelemetry.io/docs/languages/php/)

You can also find instrumentation libraries for your framework in the [OpenTelemetry Registry](https://opentelemetry.io/ecosystem/registry/).

For applications that support OpenTelemetry auto-instrumentation, you can configure the OTLP endpoint using environment variables in your Managed Service for Kubernetes deployment:

```yaml theme={null}
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://nebius-observability-agent.<namespace>.svc.cluster.local:4317"
  - name: OTEL_EXPORTER_OTLP_PROTOCOL
    value: "grpc"
```

Replace `<namespace>` with the namespace where the Nebius Observability Agent for Kubernetes is installed.

## View traces

After configuring trace collection, you can view the traces in Grafana. For instructions on how to connect and explore traces, see [How to view traces in Grafana®](https://docs.nebius.com/observability/traces/grafana.md).

## See also

* [How to ingest traces directly with OpenTelemetry exporters](https://docs.nebius.com/observability/traces/direct-ingest.md)
* [How to view traces in Grafana®](https://docs.nebius.com/observability/traces/grafana.md)
* [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/agents/nebius-o11y-agent.md)
* [OpenTelemetry documentation](https://opentelemetry.io/docs/)
* [OpenTelemetry Registry](https://opentelemetry.io/ecosystem/registry/): find instrumentation libraries for your language or framework
