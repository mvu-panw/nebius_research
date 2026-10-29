# Static keys in Nebius AI Cloud

Source: https://docs.nebius.com/iam/authorization/static-keys

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Static keys in Nebius AI Cloud

Static keys provide a method of authentication in Nebius AI Cloud services from third-party tools and systems. Static keys are useful when you need long-term credentials. The lifetime of a static key is up to three years.

## Use cases

* Integrate Observability with third-party tools.

  You can authorize tools like Grafana® to access Nebius AI Cloud [metrics](https://docs.nebius.com/observability/metrics/grafana.md) and [logs](https://docs.nebius.com/observability/logs/grafana.md). For example, see [How to ingest metrics into Nebius AI Cloud](https://docs.nebius.com/observability/metrics/ingest/index.md).

* Access the Container Registry service from external systems.

  You can deploy artifacts from Container Registry to external systems that have no access to Nebius AI Cloud.

For security reasons, static keys are available only for these Nebius AI Cloud services.

## Limitations

* You can only use static keys for [service accounts](https://docs.nebius.com/iam/overview.md#accounts-and-members).
* Each static key is issued for a specific Nebius AI Cloud service and cannot be used for other services.
* Static key level of access cannot be greater than the level of access of the service account for which it is issued. For example, if the service account is only in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) with the `auditor` [role](https://docs.nebius.com/iam/authorization/roles.md#general-roles), the account is not allowed to view the metrics. Therefore, the static key issued for this service account does not let you fetch the metrics from Nebius Observability.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs’ permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
