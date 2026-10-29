# How to ingest traces directly with OpenTelemetry exporters

Source: https://docs.nebius.com/observability/traces/direct-ingest

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to ingest traces directly with OpenTelemetry exporters

Nebius AI Cloud accepts traces from applications that send OpenTelemetry Protocol (OTLP) data over gRPC. Configure the OpenTelemetry exporter in your application to write traces directly to a regional Tracing writer endpoint.

Use this method when your application already uses OpenTelemetry and you do not want to route traces through [Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/traces/ingest.md).

## Prerequisites

1. If you don’t have a service account for observability services, [create one](https://docs.nebius.com/iam/service-accounts/manage.md).

2. Make sure that the service account is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam/service-accounts) section of the web console.

   If the service account is not in the required group, click  → **Add to group**, and select `editors`. Only users with the `admin` role can add a service account to a group.

3. [Issue a static key](https://docs.nebius.com/iam/authorization/static-keys/manage.md#creating-a-static-key) for the service account. Set the `service` parameter to `OBSERVABILITY`. Copy the token of the static key. You will need it later in the configuration steps.

In addition, add the OpenTelemetry SDK and the OTLP gRPC trace exporter to your application.

## Endpoint and headers

The direct tracing writer accepts OTLP over gRPC on port `443`.

Use the following endpoint:

```text theme={null}
write.tracing.<region_ID>.nebius.cloud:443
```

In this endpoint, replace `<region_ID>` with the [region ID](https://docs.nebius.com/overview/regions.md) of the project where you want to store traces.

Some OpenTelemetry SDKs expect a URL instead of `host:port`. For those SDKs, use the same endpoint with the `https://` scheme:

```text theme={null}
https://write.tracing.<region_ID>.nebius.cloud:443
```

Include the following gRPC metadata headers with each request:

* `authorization`: `Bearer <static_token>`
* `iam-container`: `<project_ID>`

In these headers, specify the following values:

* `<static_token>`: The static key token that you obtained during the [prerequisites](#prerequisites).
* `<project_ID>`: The [ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) of the project where you want to store traces.

Do not append `/v1/traces` to the endpoint for OTLP over gRPC.

## Configuring an exporter

The following examples show how to configure an OTLP gRPC trace exporter. Add instrumentation for your framework or libraries separately.

Before running an application, pass the endpoint parameters and the static key token to it:

```bash theme={null}
export NEBIUS_REGION_ID=<region_ID>
export NEBIUS_PROJECT_ID=<project_ID>
export NEBIUS_STATIC_TOKEN=<static_token>
```

**Python**

```python theme={null}
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

region_id = os.environ["NEBIUS_REGION_ID"]
project_id = os.environ["NEBIUS_PROJECT_ID"]
static_token = os.environ["NEBIUS_STATIC_TOKEN"]

resource = Resource.create({"service.name": "my-service"})
provider = TracerProvider(resource=resource)

# Send traces to the Nebius AI Cloud OTLP/gRPC writer.
exporter = OTLPSpanExporter(
    endpoint=f"https://write.tracing.{region_id}.nebius.cloud:443",
    headers={
        "authorization": f"Bearer {static_token}",
        "iam-container": project_id,
    },
)

provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-service")
```

**TypeScript**

```typescript theme={null}
import { Metadata } from "@grpc/grpc-js";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";
import { resourceFromAttributes } from "@opentelemetry/resources";
import { NodeSDK } from "@opentelemetry/sdk-node";
import { ATTR_SERVICE_NAME } from "@opentelemetry/semantic-conventions";

const regionId = process.env.NEBIUS_REGION_ID;
const projectId = process.env.NEBIUS_PROJECT_ID;
const staticToken = process.env.NEBIUS_STATIC_TOKEN;

if (!regionId || !projectId || !staticToken) {
  throw new Error("Set NEBIUS_REGION_ID, NEBIUS_PROJECT_ID and NEBIUS_STATIC_TOKEN");
}

const metadata = new Metadata();
metadata.set("authorization", `Bearer ${staticToken}`);
metadata.set("iam-container", projectId);

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: "my-service",
  }),
  traceExporter: new OTLPTraceExporter({
    url: `https://write.tracing.${regionId}.nebius.cloud:443`,
    metadata,
  }),
});

sdk.start();
```

**Go**

```go theme={null}
package main

import (
	"context"
	"fmt"
	"os"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
)

func configureTracing(ctx context.Context) (*sdktrace.TracerProvider, error) {
	regionID := os.Getenv("NEBIUS_REGION_ID")
	projectID := os.Getenv("NEBIUS_PROJECT_ID")
	staticToken := os.Getenv("NEBIUS_STATIC_TOKEN")

	if regionID == "" || projectID == "" || staticToken == "" {
		return nil, fmt.Errorf("set NEBIUS_REGION_ID, NEBIUS_PROJECT_ID and NEBIUS_STATIC_TOKEN")
	}

	// Send traces to the Nebius AI Cloud OTLP/gRPC writer.
	exporter, err := otlptracegrpc.New(ctx,
		otlptracegrpc.WithEndpoint(fmt.Sprintf("write.tracing.%s.nebius.cloud:443", regionID)),
		otlptracegrpc.WithHeaders(map[string]string{
			"authorization": "Bearer " + staticToken,
			"iam-container": projectID,
		}),
	)
	if err != nil {
		return nil, err
	}

	provider := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(resource.NewSchemaless(
			attribute.String("service.name", "my-service"),
		)),
	)
	otel.SetTracerProvider(provider)

	return provider, nil
}
```

When your application stops, shut down the tracer provider to flush spans that are still buffered.

## Viewing traces

After configuring the exporter, generate traces from your application. To view and analyze the traces, see [How to view traces](https://docs.nebius.com/observability/traces/grafana.md).

## See also

* [How to ingest traces with Nebius Observability Agent for Kubernetes](https://docs.nebius.com/observability/traces/ingest.md)
* [How to view traces](https://docs.nebius.com/observability/traces/grafana.md)
* [OpenTelemetry documentation](https://opentelemetry.io/docs/)
