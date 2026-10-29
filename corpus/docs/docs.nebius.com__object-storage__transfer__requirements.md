# Bucket requirements for data transfers

Source: https://docs.nebius.com/object-storage/transfer/requirements

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Bucket requirements for data transfers

You can transfer data between Nebius AI Cloud buckets or between a Nebius AI Cloud bucket and a supported S3-compatible storage service. Additionally, Azure Blob Storage containers are supported as data transfer sources. In every data transfer, either the source, the destination or both must be Nebius AI Cloud buckets. You can also use [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md) for data transfers.

## Supported external storage services

When transferring data from another S3-compatible storage service, verify the consistency of object metadata before starting the transfer. Object Storage relies on the source service to assign accurate timestamps of the last modification. If the source service sets timestamps incorrectly — for example, to dates in the past during object creation — such objects may be skipped during synchronization, even if they are new or updated.

The following table lists supported external storage services. This list is subject to change. If you want to add a provider that isn't listed, [contact support](https://console.nebius.com/support/create-ticket).

| Provider | Endpoints | Source | Destination |
| - | - | - | - |
| [Alibaba Cloud Object Storage Service](https://www.alibabacloud.com/help/en/oss/user-guide/oss-bucket-overview) | `https://oss-*.aliyuncs.com` | Yes | Yes, with limitations<sup>\*</sup> |
| [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html) | `https://s3.*.amazonaws.com`, `https://s3.dualstack.*.amazonaws.com` | Yes | Yes |
| [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal) | `https://*.blob.core.windows.net` | Yes | No |
| [Backblaze B2](https://www.backblaze.com/docs/cloud-storage-buckets) | `https://s3.*.backblazeb2.com` | Yes | Yes, with limitations<sup>\*</sup> |
| [Cloudflare R2](https://developers.cloudflare.com/r2/buckets/) | `https://*.r2.cloudflarestorage.com` | Yes | No |
| [Google Cloud Storage](https://cloud.google.com/storage/docs/buckets) | `https://storage.googleapis.com`, `https://storage.*.rep.googleapis.com` | Yes | No |
| [IBM Cloud Object Storage](https://cloud.ibm.com/docs/cloud-object-storage/cli?topic=cloud-object-storage-getting-started-cloud-object-storage) | `https://s3.*.cloud-object-storage.appdomain.cloud` | Yes | Yes |
| [MEGA S4](https://help.mega.io/megas4) | `https://s3.*.megas4.com` | Yes | Yes |
| [Oracle Cloud Infrastructure Object Storage](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/managingbuckets.htm) | `https://*.compat.objectstorage.*.oci.customer-oci.com`, `https://*.compat.objectstorage.*.oraclecloud.com` | Yes | No |
| [Supabase](https://supabase.com/docs/guides/storage/s3/compatibility) | `https://*.supabase.co/storage/v1/s3`, `https://*.storage.supabase.co/storage/v1/s3` | Yes | Yes, with limitations<sup>\*</sup> |
| [T3 Tigris Data](https://www.tigrisdata.com/) | `https://t3.storage.dev` | Yes | No |
| [Wasabi](https://docs.wasabi.com/docs/creating-a-bucket) | `https://s3.*.wasabisys.com`, `https://s3.wasabisys.com` | Yes | Yes, with limitations<sup>\*</sup> |

<sup>\*</sup> Alibaba Cloud Object Storage Service, Backblaze B2, Supabase and Wasabi don't support the `If-Match` and `If-None-Match` conditional request headers. For details, see [Limitations for conditional requests](#limitations-for-conditional-requests).

## Versioned buckets as sources

You can transfer data from versioned buckets. For versioned buckets, only the current object version is transferred.

## Access to buckets

When you [create a data transfer](https://docs.nebius.com/object-storage/transfer/launch.md), you provide credentials that Object Storage uses to access the buckets. These credentials belong to accounts in storage services, such as [service accounts](https://docs.nebius.com/iam/overview.md#accounts-and-members) in Nebius AI Cloud. The accounts perform actions on buckets and objects during the data transfer, so these accounts must have sufficient permissions to perform these actions.

For more information, see [Access to buckets for data transfers](https://docs.nebius.com/object-storage/transfer/access.md).

## Limitations for conditional requests

Alibaba Cloud Object Storage Service, Backblaze B2, Supabase and Wasabi don't support the `If-Match` and `If-None-Match` HTTP headers for conditional requests. When you use one of these providers as a transfer destination, guarantees for write and delete operations degrade to best-effort behavior:

* Protection of concurrent write and delete operations isn't enforced. The data transfer can't atomically verify that an object wasn't modified between the read and the write or delete operation. This creates a race condition where concurrent operations may silently overwrite changes or delete objects unexpectedly.

* If [overwriting and deleting unmanaged destination objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md#unmanaged-destination-objects) is disabled (`.spec.touch_unmanaged = false`), unmanaged objects may still be overwritten or deleted if another process writes to them between the read and write or delete operation.

* The enabled [overwriting destination objects if source is newer](https://docs.nebius.com/object-storage/transfer/destination-objects.md#overwriting-destination-objects) (`.spec.overwrite_strategy = IF_NEWER`) doesn't guarantee that only older objects are overwritten. If an object is written after the read operation but before the write operation, it won't be detected and may be overwritten.

* The enabled [deletion of destination objects that aren't in the source](https://docs.nebius.com/object-storage/transfer/destination-objects.md#deleting-destination-objects) (`.spec.enable_deletes_in_destination = true`) doesn't guarantee that only stale destination objects are deleted. If an object is written to the destination after the destination read operation but before deletion, it may be deleted.
