# Viewing serial logs of virtual machines

Source: https://docs.nebius.com/compute/monitoring/serial-logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Viewing serial logs of virtual machines

Compute virtual machines write logs from a serial console. Serial logs may help you with troubleshooting VM startup and shutdown failures, operating system incidents or other similar issues.

Serial logs are kept for 14 days. The logs for deleted instances are also kept for 14 days, but you cannot see them in the [web console](#view-serial-logs-in-web-console). Use [Grafana®](#view-serial-logs-in-grafana) or [LogCLI](#query-serial-logs-with-logcli) to view logs of deleted instances.

Serial logs for Compute are free of charge.

## View serial logs in web console

**Web console**

To view the serial logs of a given virtual machine:

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, select the virtual machine you need and switch to the **Serial logs** tab.

To view all serial logs in one place:

1. In the sidebar, go to  **Observability** → [Logs](https://console.nebius.com/observability/logs).
2. Select the serial logs bucket.
3. Optionally, filter the logs by virtual machine ID.

## View serial logs in Grafana®

You can visualize the serial logs of services in Grafana.

After you [connect Grafana](https://docs.nebius.com/observability/logs/grafana.md#how-to-connect-grafana), set the `__bucket__` label value to `sp_serial`.

## Query serial logs with LogCLI

After you [set up LogCLI](https://docs.nebius.com/observability/logs/logcli.md), set the `__bucket__` label value to `sp_serial` in your queries, for example:

```bash theme={null}
logcli query '{__bucket__="sp_serial"}' --since 15m
```

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs’ permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
