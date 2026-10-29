# Quotas and constraints in Nebius AI Cloud Observability services

Source: https://docs.nebius.com/observability/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas and constraints in Nebius AI Cloud Observability services

## Quotas

*Quotas* define how much Nebius AI Cloud resources you can use. If you run out of a quota, you can increase it.

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

### Logs quotas

Logs have quotas on the total volume and number of pending log exports. The quota is released when the export is completed or when it fails.

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| :- | :- |
| Pending logs export requests size | 1 TiB (Nebius uses binary units. For example, a *mebibyte* (MiB) is 2\<sup>20\</sup> (1024\<sup>2\</sup>) bytes.) |
| Pending logs export requests | 3 |

## Constraints

*Constraints* are technical limitations that can't be changed directly.

### Metrics constraints

Metrics have the following constraints on entries you can request:

* Time series per request: 3000
* Points per time series: 10 000
* Samples that can be processed per request: 1 000 000
* Samples that can be aggregated during reading: 500 000
* Retention period: 14 days
* Labels per time series: 28

### Logs constraints

Logs have the following constraints:

**Storage**

* Retention period: 14 days. To request a longer retention period, [contact technical support](https://console.nebius.com/support).

**Writing**

* Size of a batch of log entries: 4 MB (uncompressed)
* Number of log entries per batch: 1000
* Size of a log entry: 256 KB
* Timestamp range for log entries: from the current time minus 3 days (`now-3d`) to the current time plus 1 day (`now+1d`)

**Reading**

* Lines per data point on a graph: 50
* Number of rows in a response: 1000
