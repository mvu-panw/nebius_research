# How data transfers work in Nebius AI Cloud

Source: https://docs.nebius.com/object-storage/transfer/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How data transfers work in Nebius AI Cloud

*Data transfers* allow you to move data between buckets. You can use a data transfer, for example, when you need to replicate and back up your data in a bucket, or when you want to migrate from a different region or third-party storage service.

Data transfers support both Object Storage in Nebius AI Cloud and S3-compatible third-party services as sources and destinations. For more information, see [Bucket requirements for data transfers](https://docs.nebius.com/object-storage/transfer/requirements.md).

You can manage data transfers in the web console or by using the CLI or the provider for Terraform. For instructions, see [Launching transfers](https://docs.nebius.com/object-storage/transfer/launch.md) and [Managing transfers](https://docs.nebius.com/object-storage/transfer/manage.md).

## Iterations

Data transfers consist of consecutive *iterations*. Each iteration passes the source and destination buckets once.

At each iteration, Object Storage performs the following operations in parallel:

* Lists objects in the source bucket by making a `ListObjects` request for every 1000 objects. For every listed source object, Object Storage makes `HeadObject` requests to both the source and destination buckets, and then determines which objects need to be transferred:

  * If you allow [overwriting destination objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md#overwriting-destination-objects), a source object that is newer than its destination pair (based on the `Last-Modified` header) overwrites it. If you also allow [overwriting unmanaged objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md#unmanaged-destination-objects), the same applies to objects in the destination that weren't copied from the source bucket during the current or past transfers.
  * After the first successful iteration, source objects that were last modified before the last successful iteration are skipped to reduce synchronization costs.
  * If the source and destination objects have identical data but different metadata, Object Storage doesn't transfer the object data again. Instead, it updates the destination object's metadata by making a `CopyObject` request with `MetadataDirective` set to `REPLACE`.

* If [deleting destination objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md#deleting-destination-objects) is enabled, Object Storage lists objects in the destination bucket by making a `ListObjects` request for every 1000 objects. Object Storage compares source and destination object lists, determines which destination objects don't have pairs in the source, and deletes them using `DeleteObject`. If [overwriting and deleting unmanaged objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md#unmanaged-destination-objects) is disabled, Object Storage doesn't delete destination objects that weren't copied from the source bucket during the current or past transfers.

* For every object that needs to be transferred:

  * If the object is less than 100 MB, it makes a single `GetObject` request to the source bucket and a single `PutObject` request to the destination bucket.
  * For larger objects, it makes the following requests:

    1. `CreateMultipartUpload` to the destination bucket.
    2. `GetObject` to the source bucket and `UploadPart` to the destination bucket for every approximately 50 MB of the object.
    3. `CompleteMultipartUpload` to the destination bucket after uploading all parts.

  The same logic applies to [blobs](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#blobs) in Azure Blob Storage containers, regardless of the type of blob.

### Number of iterations and empty iterations

You can configure a data transfer to stop after one iteration or after a number of consecutive empty iterations or to continue indefinitely.

An *empty iteration* is an iteration where no data is transferred or deleted.

To configure the number of iterations, choose a data transfer type in the web console or define a stop condition in the developer tools, such as the CLI. For transfers with more than one iteration, you can also set the interval between iterations. For more information, see [Data transfer types and stop conditions](https://docs.nebius.com/object-storage/transfer/stop-condition.md).

## Costs

The cost of a data transfer consists of the costs for the source and destination buckets. The data transfer itself doesn't incur additional costs.

| | **Destination: Nebius** | **Destination: external** |
| - | - | - |
| **Source: Nebius** | <ul><li>[HTTP requests](https://docs.nebius.com/object-storage/resources/pricing.md#http-requests-on-data) on source data: class B (GET, HEAD) operations, as described in [Iterations](#iterations)</li><li>[Egress traffic](https://docs.nebius.com/object-storage/resources/pricing.md#egress-traffic) from source (except when both buckets are in the same [region](https://docs.nebius.com/overview/regions.md))</li><li>[HTTP requests](https://docs.nebius.com/object-storage/resources/pricing.md#http-requests-on-data) on destination data: class A (PUT, POST, DELETE) and class B (HEAD) operations, as described in [Iterations](#iterations)</li><li>[Storing data](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data) in destination (once an object or its part is uploaded)</li></ul> | <ul><li>[HTTP requests](https://docs.nebius.com/object-storage/resources/pricing.md#http-requests-on-data) on source data: class B (GET, HEAD) operations, as described in [Iterations](#iterations)</li><li>[Egress traffic](https://docs.nebius.com/object-storage/resources/pricing.md#egress-traffic) from source</li><li>Destination costs: ingress traffic, requests, storage, etc. (see your provider's documentation)</li></ul> |
| **Source: external** | <ul><li>Source costs: egress traffic, requests, etc. (see your provider's documentation)</li><li>[HTTP requests](https://docs.nebius.com/object-storage/resources/pricing.md#http-requests-on-data) on destination data: class A (PUT, POST, DELETE) and class B (HEAD) operations, as described in [Iterations](#iterations)</li><li>[Storing data](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data) in destination (once an object or its part is uploaded)</li></ul> | *Not supported* |
