# Monitoring buckets in Nebius AI Cloud

Source: https://docs.nebius.com/object-storage/monitoring

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring buckets in Nebius AI Cloud

You can monitor bucket status on the dashboards in the Nebius AI Cloud web console. There are two ways to find the required dashboard:

* Go to  **Observability** → [Metrics](https://console.nebius.com/observability/metrics) and select the resource you would like to review.
* Go to the page of the bucket you would like to review and switch to the **Metrics** tab.

Use the dashboard to monitor current resource utilization, get information to schedule [quota](https://docs.nebius.com/object-storage/resources/quotas-limits.md) increases and quickly identify anomalies. In case of object storage issues, dashboards help the Nebius support team investigate the issue.

Data for the dashboard is collected automatically.

The bucket usage data becomes available 5–10 minutes after the bucket is created.

## Dashboard filters

Use time filters to view a specific period of usage.

By default, the data is refreshed every 15 seconds. You can configure this interval next to the time filters.

## Bucket monitoring metrics

* **Traffic**

  Amount of data transferred to and from storage. Measured in bytes per second.

* **Total bucket size**

  Storage space used by all objects in a bucket.

* **Read requests**

  Number of requests made to retrieve object contents from storage. Measured in requests per second.

* **Modify requests**

  Number of requests made to upload objects or modify object contents. Measured in requests per second.

* **Space by storage class**

  Storage space used by objects by [storage class](https://docs.nebius.com/object-storage/storage-classes.md). Measured in GiB.

* **Space by object type**

  Amount of storage used for objects of different types.

* **Object counts**

  Number of stored objects by type.

* **Object counts by storage class**

  Number of objects by storage class.

* **API Errors**

  Number of API errors by type of error.

* **Transition lifecycle failures**

  Number of failed storage class transitions caused by [transition lifecycle rules](https://docs.nebius.com/object-storage/objects/lifecycles.md#transition-lifecycle-rules).
