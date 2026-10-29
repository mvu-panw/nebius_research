# Logs in Nebius AI Cloud

Source: https://docs.nebius.com/observability/logging

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Logs in Nebius AI Cloud

In Nebius AI Cloud, you can view logs in various forms:

* Go to  **Observability** → [Logs](https://console.nebius.com/observability/logs).
  * Use the **Bucket** drop-down list to switch between User logs [ingested from the Managed Service for Kubernetes®](https://docs.nebius.com/observability/logs/ingest.md) (if available) and service logs.
* Go to the page of the resource you would like to review in the [web console](https://console.nebius.com) and switch to the **Logs** tab.
* [Export logs](https://docs.nebius.com/observability/logs/export.md) to view them in JSON or Apache Parquet format.
* View logs in [Grafana®](https://docs.nebius.com/observability/logs/grafana.md) by connecting a Loki data source.
* Query logs from the terminal using the [Nebius AI Cloud CLI](https://docs.nebius.com/observability/logs/nebius-cli.md) or [LogCLI](https://docs.nebius.com/observability/logs/logcli.md).

Logs are available for the following services:

* [Compute](https://docs.nebius.com/compute/index.md) (serial logs of virtual machines)
* [Managed Service for MLflow](https://docs.nebius.com/mlflow/index.md)
* [Managed Service for PostgreSQL®](https://docs.nebius.com/postgresql/index.md)
* [Applications for Managed Service for Kubernetes®](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/index.md)
* [Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/index.md)

You can also collect your own logs, ingest them into Nebius AI Cloud Observability and analyze them in a unified environment (for example, in Grafana).

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
