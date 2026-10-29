# Monitoring volumes in Nebius AI Cloud

Source: https://docs.nebius.com/compute/monitoring/volumes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring volumes in Nebius AI Cloud

You can monitor disk and filesystem statuses on the dashboards in the Nebius AI Cloud [web console](https://console.nebius.com). There are two ways to find the required dashboard:

* Go to  **Observability** → [Metrics](https://console.nebius.com/observability/metrics) and select the resource you would like to review.
* Go to the page of the resource you would like to review and switch to the **Metrics** tab.

Use the dashboard to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/compute/resources/quotas-limits.md) increases and quickly identify anomalies. In case of volume issues, dashboards help the Nebius support team investigate the issue.

Data for the dashboard is collected automatically.

## Explore the dashboard

The volume usage data becomes available 5–10 minutes after the volume is mounted.

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## Disk monitoring metrics

* **Disk read latency by quantiles**

  Percentiles of the disk read requests latency. Measured in milliseconds.

* **Disk write latency by quantiles**

  Percentiles of the disk write requests latency. Measured in milliseconds.

* **Disk read throttler latency by quantiles**

  Percentiles of the disk write operations latency due to disk quota excess. Measured in milliseconds.

* **Disk write throttler latency by quantiles**

  Percentiles of the disk write operations latency due to disk quota excess. Measured in milliseconds.

* **Disk read operations**

  Average read IOPS. Measured in operations per second.

* **Disk write operations**

  Average write IOPS. Measured in operations per second.

* **Disk read bytes**

  Average read throughput. Measured in bytes per second.

* **Disk write bytes**

  Average write throughput. Measured in bytes per second.

* **Disk used quota**

  Percentage of disk quota on read and write operations per second utilization.

## Filesystem monitoring metrics

* **Read latency by quantiles**

  Percentiles of the filesystem write requests latency. Measured in milliseconds.

* **Write latency by quantiles**

  Percentiles of the filesystem read requests latency. Measured in milliseconds.

* **Read operations**

  Average read IOPS. Measured in operations per second.

* **Write operations**

  Average write IOPS. Measured in operations per second.

* **Read bytes**

  Average read throughput. Measured in bytes per second.

* **Write bytes**

  Average write throughput. Measured in bytes per second.

* **Read errors**

  Number of times a filesystem fails to read data.

* **Write errors**

  Number of times a filesystem fails to write data.

* **Index operations**

  Number of indexing actions (reads, writes, updates and deletions) performed in a time period.

* **Index errors**

  Number of failed indexing operations in a time period.
