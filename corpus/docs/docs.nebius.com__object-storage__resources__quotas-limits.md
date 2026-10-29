# Quotas and constraints in Object Storage

Source: https://docs.nebius.com/object-storage/resources/quotas-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Quotas and constraints in Object Storage

## Quotas

Object Storage has quotas on buckets, storage size and inventory configurations for your [tenant](https://docs.nebius.com/iam/overview.md#tenants). Storage size quotas depend on the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) of an object.

| Quota name | Default value per [region](https://docs.nebius.com/overview/regions.md) |
| - | - |
| Total size of objects in Standard storage | 10 TiB |
| Total size of objects in Enhanced Throughput storage | 10 TiB |
| Total size of objects in Intelligent storage | 10 TiB |
| Buckets | 200 |

For details on what quotas are and how to manage them, see [Quotas in Nebius AI Cloud](https://docs.nebius.com/overview/quotas.md).

## Constraints

### Number of objects

The total number of objects in a bucket cannot exceed 1 billion. If you exceed this limit, the request fails with the `BucketObjectsCountExceeded` error (`HTTP 400`).

If the bucket has [versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) enabled, the total number of object versions in the bucket cannot exceed 100 million. This limit includes current and noncurrent versions.

To increase this limit for a specific bucket, [contact support](https://console.nebius.com/support).

### Number of inventory configurations

The total number of inventory configurations is limited to five per bucket and 100 per tenant.
