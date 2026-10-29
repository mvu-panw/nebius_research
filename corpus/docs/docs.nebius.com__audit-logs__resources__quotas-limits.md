# Quotas in Audit Logs

Source: https://docs.nebius.com/audit-logs/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas in Audit Logs

Audit Logs has a throughput quota on data plane events ([Object Storage logs](https://docs.nebius.com/object-storage/logs.md) of actions that are performed to objects in buckets).

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

## Data plane events

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| :- | :- |
| Number of data plane events per second | 1000 |

Events beyond the quota are dropped. To track event rates, quota usage and dropped events, [monitor your data plane events](#monitoring-data-plane-events).

### Monitoring data plane events

1. In the [web console](https://console.nebius.com), in the sidebar, go to  **Administration** → **Audit Logs**.
2. Switch to the **Metrics** tab.
3. Select **Data plane** for the event type.
4. Select a region and the period for which you want to view data plane event metrics.

The following graphs are available in this view:

* **Data plane processed rate**

  Events processed per second. Use this graph to understand your Object Storage activity.

* **Data plane quota usage**

  Events processed per second against the quota limit for the selected region. Use this graph to see if you are approaching the quota and need a [quota increase](https://docs.nebius.com/overview/quotas.md#change-quotas).

* **Data plane events dropped**

  Events dropped per second due to exceeding the quota. Use this graph to detect periods when events were dropped.
