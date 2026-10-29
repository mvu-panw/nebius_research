# TraceQL implementation by Nebius AI Cloud

Source: https://docs.nebius.com/observability/traces/query-language

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# TraceQL implementation by Nebius AI Cloud

The Tracing service supports a subset of the [TraceQL](https://grafana.com/docs/tempo/latest/traceql/construct-traceql-queries/) query language by Grafana®. Currently, only basic filters are supported.

## Examples

> **View traces with status code between 200 and 299**
>
> ```
> { resource.service.name="<service_name>" && span.http.status_code >= 200 && span.http.status_code < 300 }
> ```

> **Filter traces by duration**
>
> ```
> { resource.service.name="<service_name>" && duration > 1s }
> ```

> **Filter traces using regular expressions**
>
> ```
> { resource.service.name="<service_name>" && span.<attribute_name>=~"<string>.+" }
> ```

## Limitations

The following features are not supported:

* Pseudo-filters like `span:childCount`
* Pipe operators and functions like `select()`, `count()`
* Structural operators like `>>`, `!<`
