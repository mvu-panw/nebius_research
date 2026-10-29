# Bucket inventory in Object Storage

Source: https://docs.nebius.com/object-storage/buckets/inventory

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Bucket inventory in Object Storage

*Bucket inventory* generates scheduled reports that list the contents of a bucket. Object Storage delivers every report to the destination bucket of your choice as a set of objects in compressed CSV or [Apache Parquet](https://parquet.apache.org/) format.

Use bucket inventory reports to audit stored objects, review object metadata, and prepare data for analytics or compliance workflows.

> [!NOTE]
>
> Bucket inventory is [in preview](https://docs.nebius.com/overview/services.md#service-and-application-stages) and is available in all [Nebius AI Cloud regions](https://docs.nebius.com/overview/regions.md).

Object Storage prepares reports asynchronously in the background, so they don't add to the bucket request rate.

You can create up to five inventory configurations for the same bucket. For example, you can generate a daily report on the current versions of objects and a weekly report that includes all versions. Object Storage processes the configurations of a single bucket one after another.

For details on how to set up scheduled reports, see [How to configure bucket inventory in Object Storage](https://docs.nebius.com/object-storage/buckets/configure-inventory.md).

## How Object Storage generates reports

Object Storage creates reports according to the schedule of the configuration: **Daily** or **Weekly**. The exact time when a report is generated is not guaranteed.

Objects in a report come in no particular order.

A report is a snapshot of the bucket at the moment when Object Storage creates it. Because of this, it may not reflect the objects that were created, deleted or replaced with a new version while the report was being generated.

## What a report contains

Every row of a report describes one object. The following fields are always included:

| Field | Description |
| - | - |
| Bucket name | Name of the bucket. |
| Key | Object key. |
| ETag | Object entity tag. For more information on how Object Storage computes it, see [Behavioral differences](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md#behavioral-differences). |
| Last modified date | Date and time of the last object change. |
| Size | Object size in bytes. |
| Storage class | [Storage class](https://docs.nebius.com/object-storage/storage-classes.md) that the object is stored in. |

You can also include the following optional fields in a report:

| Field | Description |
| - | - |
| Last access time | Date and time of the last access to the object. |
| Checksum algorithms | Algorithms that Object Storage used to compute the object checksum. |
| Intelligent storage class tier | Tier of the object if it is stored in the Intelligent [storage class](https://docs.nebius.com/object-storage/storage-classes.md). |
| Multipart upload flag | `True` if the object was uploaded as a multipart upload. |
| Lifecycle expiration date | Date when an expiration [lifecycle rule](https://docs.nebius.com/object-storage/objects/lifecycles.md) deletes the object. |
| Tags | Tags assigned to the object. |
| Version ID | ID of the object version. |
| IsLatest | `True` if this version is the current version of the object. |
| Delete marker | `True` if this version is a delete marker. |

The Version ID, IsLatest and Delete marker fields only contain data if the configuration includes all object versions.

## How last access time tracking works

Object Storage starts tracking last access time for a bucket when you configure an inventory report that includes the **Last access time** optional field or a [last-access lifecycle rule](https://docs.nebius.com/object-storage/objects/lifecycles.md#last-access-lifecycle-rules). Tracking starts on the day you create such a configuration or rule (or the next day).

Reports don't include object access events that happened before tracking started. For example, if an object was accessed yesterday and you enable a report with the **Last access time** field today, the report won't show yesterday's access time.

Object Storage stops tracking last access time when the bucket has no inventory configurations with the **Last access time** field and no last-access lifecycle rules.

## Where Object Storage delivers reports

Object Storage writes every report to the destination bucket as a separate set of objects, so a new report never overwrites the previous one:

```text theme={null}
<destination_prefix>/<bucket_name>/<configuration_name>/data/<inventory_file>
<destination_prefix>/<bucket_name>/<configuration_name>/<timestamp>/manifest.json
<destination_prefix>/<bucket_name>/<configuration_name>/<timestamp>/manifest.checksum
<destination_prefix>/<bucket_name>/<configuration_name>/hive/dt=<date>/symlink.txt
```

The keys consist of the following parts:

* `<destination_prefix>`: Prefix that you set in the configuration. Use it to keep inventory reports separate from other objects in the destination bucket.
* `<bucket_name>`: Name of the bucket.
* `<configuration_name>`: Name of the inventory configuration.
* `<inventory_file>`: Name of the report object.
* `<timestamp>`: Moment when Object Storage created the report.

Along with the report itself, Object Storage delivers the following files:

* `manifest.json`: Metadata of the report, including the output format, the list of report objects and their checksums:

  ```json theme={null}
  {
    "sourceBucket": "<source_bucket>",
    "destinationBucket": "<destination_bucket>",
    "version": "2016-11-30",
    "creationTimestamp": "1781830800000",
    "fileFormat": "CSV",
    "fileSchema": "Bucket, Key, VersionId, IsLatest, IsDeleteMarker, Size, LastModifiedDate, ETag, StorageClass, IsMultipartUploaded, ChecksumAlgorithm",
    "files": [
      {
        "key": "<destination_prefix>/<bucket_name>/<configuration_name>/data/<inventory_file>",
        "size": 2997,
        "MD5checksum": "d25aa73bd27695113232a479d925278b"
      }
    ]
  }
  ```

* `manifest.checksum`: MD5 checksum of `manifest.json`.

* `symlink.txt`: [Apache Hive](https://hive.apache.org)-compatible symlink that contains the key of the report object, so that query engines can read the report as a partitioned table.

## Limitations

> [!WARNING]
>
> Bucket inventory fully manages the report objects in the destination bucket. If you create an object whose key matches the key of a report, Object Storage overwrites this object.

* The destination bucket must be an Object Storage bucket in the same [region](https://docs.nebius.com/overview/regions.md) as the bucket where you want to create an inventory configuration.

* Object Storage builds every report as a multipart upload. If the process restarts, the report starts from scratch, and an incomplete multipart upload can remain in the destination bucket. To clean up any incomplete uploads, configure an [expiration lifecycle rule](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-expiration-lifecycle-rules) that aborts them.

* The S3 API actions that manage inventory configurations are not supported. For details, see [Compatibility of Amazon S3 API with Object Storage](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md).
