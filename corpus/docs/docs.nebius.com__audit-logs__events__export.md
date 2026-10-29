# How to export audit events to Object Storage

Source: https://docs.nebius.com/audit-logs/events/export

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to export audit events to Object Storage

*Audit event export* lets you deliver [audit events](https://docs.nebius.com/audit-logs/events/view.md) for a fixed time range to an [Object Storage bucket](https://docs.nebius.com/object-storage/overview.md#buckets). Exports are one-time and run asynchronously, writing files directly to the bucket. This is useful for long-term retention, processing data in external tools and [data portability](https://docs.nebius.com/overview/data-portability.md). After the export completes, you can download the exported objects from the bucket to store them locally or move them to a different provider.

## Prerequisites

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
* Identify the regions to export audit events from.
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` or `auditlogs.audit-event-exporter` role within your tenant. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
* Make sure that you have the `storage.uploader` role for the destination Object Storage bucket.

## How to export events

1. Copy the ID of the tenant you want to export events for:

   ```bash theme={null}
   nebius iam tenant list
   ```

2. Select an existing bucket or [create a new one](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets) in the region you export events from — the destination bucket must be in the same region as the events. Copy the bucket ID.

3. Start an export:

   ```bash theme={null}
   nebius audit v2 audit-event-export start \
      --parent-id <tenant_ID> \
      --params-from <time_in_ISO_8601> \
      --params-to <time_in_ISO_8601> \
      --region <region_ID> \
      --nebius-object-storage-bucket-by-id-id <bucket_ID> \
      --params-event-type <control_plane|data_plane> \
      --nebius-object-storage-object-prefix <prefix> \
      --params-filter "<filter_expression>"
   ```

   In the command above, specify:

   * `--parent-id`: Tenant ID that you copied earlier.
   * `--params-from`: Start time for the export, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
   * `--params-to`: End time for the export, in the ISO 8601 format.
   * `--region`: [Region](https://docs.nebius.com/overview/regions.md) to export audit events from.
   * `--nebius-object-storage-bucket-by-id-id`: Destination bucket ID that you copied earlier. The bucket must be in the same region as the exported events.
   * `--params-event-type` (optional): Type of audit event to export: `control_plane` or `data_plane`. Default: `control_plane`.
     * **Control plane events** (default): Track management operations on resources, such as creating, updating or deleting virtual machines, clusters or other infrastructure resources.
     * **Data plane events**: Track data access operations, such as reading or writing objects in Object Storage buckets.
   * `--nebius-object-storage-object-prefix` (optional): Object prefix. If you omit it, the `auditlogs` prefix is used by default.
   * `--params-filter` (optional): Filter expression to narrow down exported events. For more information, see [How to filter audit events](https://docs.nebius.com/audit-logs/events/filter.md).

The command returns an operation that confirms the export was created. The export itself continues running in the background.

## How to check the status of an export

To check the current state and parameters of an export, get it by ID:

```bash theme={null}
nebius audit v2 audit-event-export get --id <export_ID>
```

Export lifecycle states include `RUNNING`, `DONE`, `FAILED` and `CANCELED`.

## How to list exports

To find a specific export, list all exports created for a tenant:

```bash theme={null}
nebius audit v2 audit-event-export list --parent-id <tenant_ID> --region <region_ID>
```

Specify the region in the required `--region` parameter.

## How to download exported events

After an export reaches the `DONE` state, the exported audit events are available as objects in the destination bucket. To download these objects to your local machine for data portability or local storage:

1. [View the objects](https://docs.nebius.com/object-storage/objects/manage.md#how-to-view-objects) in the bucket to find the exported files. The objects are stored under the prefix that you specified when you launched the export, or under the default `auditlogs` prefix.

2. [Download the objects](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-download) from the bucket to your local machine. You can download a single object or all objects with a specific prefix.

   For example, to download all exported audit events with the default `auditlogs` prefix:

   ```bash theme={null}
   aws s3 cp --recursive \
       s3://<bucket_name>/auditlogs/ \
       <local_destination_path>
   ```

## How to cancel an export

To stop an active export, run:

```bash theme={null}
nebius audit v2 audit-event-export cancel --id <export_ID>
```

The export transitions to the `CANCELED` state. Data that is already written to the bucket is preserved.
