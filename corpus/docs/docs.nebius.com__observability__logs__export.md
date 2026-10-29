# Exporting logs

Source: https://docs.nebius.com/observability/logs/export

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Exporting logs

You can export logs for the Nebius AI Cloud resources you use. Log exports are stored as [objects](https://docs.nebius.com/object-storage/overview.md#objects) in [Object Storage buckets](https://docs.nebius.com/object-storage/overview.md).

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Make sure that you have sufficient [logging quotas](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-quotas).

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have:

   * Sufficient [logging quotas](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-quotas)
   * An [Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md) to store exported logs

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have:

   * Sufficient [logging quotas](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-quotas)
   * An [Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md) to store exported logs

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have:

   * Sufficient [logging quotas](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-quotas)
   * An [Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md) to store exported logs

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have:

   * Sufficient [logging quotas](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-quotas)
   * An [Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md) to store exported logs

> [!NOTE]
>
> You can [download](#how-to-download-exported-logs) and [delete](#how-to-delete-exported-logs) exported logs only in the web console or by using the AWS CLI, because these actions work with objects in Object Storage. If you use the AWS CLI, the prerequisites for [Managing objects in Object Storage buckets](https://docs.nebius.com/object-storage/objects/manage.md#prerequisites) apply.

## How to export logs

**Web console**

1. In the [web console](https://console.nebius.com), do one of the following:
   * Go to  **Observability** → **Logs** to view the logs for all Nebius AI Cloud resources you use.
   * Go to the page of the Nebius AI Cloud resource you would like to export the logs for and switch to the **Logs** tab.
2. Use the period filter to find the logs to export.
3. (Optional) Depending on the resource you are viewing the logs for, you can apply additional filters. From the  **Observability** → **Logs** page, you can filter by resource or log level.
   You can also use the [LogQL query language](https://docs.nebius.com/observability/logs/query-language.md) to filter logs.
4. Click  **Export logs**.
5. In the window that opens:
   * Select a time range.
   * Select an existing bucket or create a new one to store the logs. To create a new one, see [Bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters).
   * Select a format:
     * **.json.gzip**: JSON lines (one JSON object per line) compressed with Gzip.
     * **.parquet**: [Apache Parquet](https://parquet.apache.org/docs/).
6. Click **Export**.

**CLI**

Run the following command:

```bash theme={null}
nebius logging export create \
  --parent-id <project_ID> \
  --bucket-name <bucket_name> \
  --filter '<LogQL_match_expression>' \
  --from <time_in_ISO_8601> \
  --to <time_in_ISO_8601> \
  --log-format <output_format> \
  
```

In the command, specify the following parameters:

* `--parent-id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

* `--bucket-name`: The name of the bucket to store the exported logs. Alternatively, use `--bucket-id` to specify the destination bucket by its ID. You can get the ID by running the following command if you know the bucket name:

  ```bash theme={null}
  nebius storage bucket get-by-name --name <bucket_name>
  ```

* `--filter`: [LogQL](https://docs.nebius.com/observability/logs/query-language.md) match expression to filter logs in the project specified in `--parent-id`. Wrap the expression in single quotation marks.

* `--from`: Start date and time for the export, in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format (for example, `2026-04-01T20:00:00Z`).

* `--to`: End date and time for the export, in the ISO 8601 format.

* `--log-format`: Output format. Supported values:
  * `json-gzip`: JSON lines (one JSON object per line) compressed with Gzip.
  * `parquet`: [Apache Parquet](https://parquet.apache.org/docs/).

* `--object-prefix` (optional): Object prefix under which exported objects are written in the bucket. Defaults to `logs/`.

* `--bucket-parent-id` (optional): To export logs to a bucket that is in a different project than the one you specified in `--parent-id`, specify the Project ID of the project that the destination bucket belongs to.

The output looks like the following:

```yaml theme={null}
id: oplogexport-e00***
description: Export logs
created_at: "2026-04-23T08:53:18.032304664Z"
created_by: tenantuseraccount-e00***
finished_at: "2026-04-23T08:53:29.261207865Z"
request:
  params:
    log:
      filter:
        from: "2025-12-01T00:00:00Z"
        to: "2026-04-23T23:59:59Z"
        match_expression: '{__bucket__="default"}'
      format: PARQUET
    nebius_object_storage:
      by_name:
        name: my-bucket
  parent_id: project-e00***
resource_id: project-e00***
status: {}
```

Save the operation ID from the output `id` parameter.

**Go SDK**

Export logs:

```go theme={null}
exportFrom, err := time.Parse(
    time.RFC3339, "<time_in_ISO_8601>",
)
if err != nil {
    return err
}
exportTo, err := time.Parse(time.RFC3339, "<time_in_ISO_8601>")
if err != nil {
    return err
}
exportService := sdk.Services().Logging().V1().LogExport()
destination := &logging.NebiusObjectStorageDestination{
    Bucket: &logging.NebiusObjectStorageDestination_ByName{
        ByName: &logging.NebiusObjectStorageBucketByName{
            Name: "<bucket_name>",
            ParentId: "<project_ID>",
        },
    },
    ObjectPrefix: "",
}
exportOperation, err := exportService.ExportLogs(
    ctx,
    &logging.ExportLogsRequest{
        ParentId: "<project_ID>",
        Params: &logging.ExportParams{
            ExportMode: &logging.ExportParams_Log{
                Log: &logging.LogsExport{
                    Filter: &logging.ExportFilter{
                        From: timestamppb.New(exportFrom),
                        To: timestamppb.New(exportTo),
                        MatchExpression: `<LogQL_match_expression>`,
                    },
                    Format: logging.LogsExportFormat_PARQUET,
                },
            },
            ExportDestination:
                &logging.ExportParams_NebiusObjectStorage{
                    NebiusObjectStorage: destination,
                },
        },
    },
)
if err != nil {
    return err
}
fmt.Println(exportOperation.ID())

```

In the code, set the following parameters:

* `ParentId` in `ExportLogsRequest`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

* `Name` in `NebiusObjectStorageBucketByName`: The name of the bucket to store the exported logs. Alternatively, set `Bucket` to `&logging.NebiusObjectStorageDestination_Id{Id: "<bucket_ID>"}` to specify the destination bucket by its ID. You can get the ID from `Metadata.Id` in the response of the following code if you know the bucket name:

  ```go theme={null}
  bucketService := sdk.Services().Storage().V1().Bucket()
  bucket, err := bucketService.GetByName(
      ctx,
      &storage.GetBucketByNameRequest{
          ParentId: "<project_ID>",
          Name: "<bucket_name>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(bucket)
  ```

* `MatchExpression` in `ExportFilter`: [LogQL](https://docs.nebius.com/observability/logs/query-language.md) match expression to filter logs in the project specified in `ParentId` of `ExportLogsRequest`.

* The time strings parsed into `exportFrom` and `exportTo`: Start and end date and time for the export, in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format (for example, `2026-04-01T20:00:00Z`).

* `Format` in `LogsExport`: Output format. The code exports logs in Apache Parquet (`logging.LogsExportFormat_PARQUET`). To export JSON lines compressed with Gzip, use `logging.LogsExportFormat_JSON_GZIP`.

* `ObjectPrefix` (optional): Object prefix under which exported objects are written in the bucket. If you leave it empty, the prefix is `logs/`.

* `ParentId` in `NebiusObjectStorageBucketByName` (optional): To export logs to a bucket that is in a different project than the one you specified in `ParentId` of `ExportLogsRequest`, specify the Project ID of the project that the destination bucket belongs to.

Save the operation ID from the output.

**Python SDK**

Export logs:

```python theme={null}
export_service = LogExportServiceClient(sdk)
export_operation = await export_service.export_logs(
    ExportLogsRequest(
        parent_id="<project_ID>",
        params=ExportParams(
            log=LogsExport(
                filter=ExportFilter(
                    from_=datetime.fromisoformat("<time_in_ISO_8601>"),
                    to=datetime.fromisoformat("<time_in_ISO_8601>"),
                    match_expression='<LogQL_match_expression>',
                ),
                format=LogsExportFormat.PARQUET,
            ),
            nebius_object_storage=NebiusObjectStorageDestination(
                by_name=NebiusObjectStorageBucketByName(
                    name="<bucket_name>",
                    parent_id="<project_ID>",
                ),
                object_prefix="",
            ),
        ),
    ),
)
print(export_operation.id)

```

In the code, set the following parameters:

* `parent_id` in `ExportLogsRequest`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

* `name` in `NebiusObjectStorageBucketByName`: The name of the bucket to store the exported logs. Alternatively, replace `by_name` in `NebiusObjectStorageDestination` with `id="<bucket_ID>"` to specify the destination bucket by its ID. You can get the ID from `metadata.id` in the response of the following code if you know the bucket name:

  ```python theme={null}
  bucket_service = BucketServiceClient(sdk)
  bucket = await bucket_service.get_by_name(
      GetBucketByNameRequest(
          parent_id="<project_ID>",
          name="<bucket_name>",
      ),
  )
  print(bucket)
  ```

* `match_expression` in `ExportFilter`: [LogQL](https://docs.nebius.com/observability/logs/query-language.md) match expression to filter logs in the project specified in `parent_id` of `ExportLogsRequest`.

* `from_` and `to` in `ExportFilter`: Start and end date and time for the export, in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format (for example, `2026-04-01T20:00:00Z`).

* `format` in `LogsExport`: Output format. The code exports logs in Apache Parquet (`LogsExportFormat.PARQUET`). To export JSON lines compressed with Gzip, use `LogsExportFormat.JSON_GZIP`.

* `object_prefix` (optional): Object prefix under which exported objects are written in the bucket. If you leave it empty, the prefix is `logs/`.

* `parent_id` in `NebiusObjectStorageBucketByName` (optional): To export logs to a bucket that is in a different project than the one you specified in `parent_id` of `ExportLogsRequest`, specify the Project ID of the project that the destination bucket belongs to.

Save the operation ID from the output.

**JavaScript SDK**

Export logs:

```ts theme={null}
const exportService = new LogExportService(sdk);
const destination = NebiusObjectStorageDestination.create({
  bucket: {
    $case: "byName",
    byName: NebiusObjectStorageBucketByName.create({
      name: "<bucket_name>",
      parentId: "<project_ID>",
    }),
  },
  objectPrefix: "",
});
const exportOperation = await exportService.exportLogs(
  ExportLogsRequest.create({
    parentId: "<project_ID>",
    params: ExportParams.create({
      exportMode: {
        $case: "log",
        log: LogsExport.create({
          filter: ExportFilter.create({
            from: dayjs("<time_in_ISO_8601>"),
            to: dayjs("<time_in_ISO_8601>"),
            matchExpression: '<LogQL_match_expression>',
          }),
          format: LogsExportFormat.PARQUET,
        }),
      },
      exportDestination: {
        $case: "nebiusObjectStorage",
        nebiusObjectStorage: destination,
      },
    }),
  }),
).result;
console.log(exportOperation.id());

```

In the code, set the following parameters:

* `parentId` in `ExportLogsRequest`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

* `name` in `NebiusObjectStorageBucketByName`: The name of the bucket to store the exported logs. Alternatively, set `bucket` in `NebiusObjectStorageDestination` to `{ $case: "id", id: "<bucket_ID>" }` to specify the destination bucket by its ID. You can get the ID from `metadata.id` in the response of the following code if you know the bucket name:

  ```ts theme={null}
  const bucketService = new BucketService(sdk);
  const bucket = await bucketService.getByName(
    GetBucketByNameRequest.create({
      parentId: "<project_ID>",
      name: "<bucket_name>",
    }),
  ).result;
  console.log(bucket);
  ```

* `matchExpression` in `ExportFilter`: [LogQL](https://docs.nebius.com/observability/logs/query-language.md) match expression to filter logs in the project specified in `parentId` of `ExportLogsRequest`.

* `from` and `to` in `ExportFilter`: Start and end date and time for the export, in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format (for example, `2026-04-01T20:00:00Z`).

* `format` in `LogsExport`: Output format. The code exports logs in Apache Parquet (`LogsExportFormat.PARQUET`). To export JSON lines compressed with Gzip, use `LogsExportFormat.JSON_GZIP`.

* `objectPrefix` (optional): Object prefix under which exported objects are written in the bucket. If you leave it empty, the prefix is `logs/`.

* `parentId` in `NebiusObjectStorageBucketByName` (optional): To export logs to a bucket that is in a different project than the one you specified in `parentId` of `ExportLogsRequest`, specify the Project ID of the project that the destination bucket belongs to.

Save the operation ID from the output.

> [!NOTE]
>
> If the [Object Storage quota](https://docs.nebius.com/object-storage/resources/quotas-limits.md) is exceeded, the export fails due to timeout.

## How to inspect log exports

**Web console**

To view all of your log exports and open the destination bucket for an export:

1. In the [web console](https://console.nebius.com), go to  **Observability** → **Logs** → **Exports**. This tab shows the following information for each export:
   * **Operation ID**: The unique identifier for the export operation. Use this ID to distinguish between exports stored in the same bucket.
   * **Status**: `In progress`, `Finished` or `Canceled`.

2. Click  → **View bucket** next to an export. The exported logs are stored in the selected bucket with the following path structure:

   ```text theme={null}
   logs/<operation_ID>/<timestamp>/<segment_number>.<extension>
   ```

   Large exports may be split into segments and stored separately. The objects are numbered sequentially starting from `0`. In some cases, segments may be split further into parts, indicated by a dash (`-`) and the part number after the segment number.

   > **Example path**
   >
   > ```text theme={null}
   > logs/oplogexport-***/2026-01-15-10:30:00/1-2.parquet
   > ```

**CLI**

* To list the details and status of all export operations in a project, run:

  ```bash theme={null}
  nebius logging export list --parent-id <project_ID>
  ```

  In `--parent-id`, specify the [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you exported logs from.

* To check the details and status of a specific export operation, run:

  ```bash theme={null}
  nebius logging export get --id <operation_ID>
  ```

  In `--id`, specify the operation ID of the export.

  If the export is completed successfully, the `status` parameter in the output is empty (`status: {}`). If the export wasn't successful, the `status` parameter contains a `code` and a `message` that explains the issue.

**Go SDK**

* To list the details and status of all export operations in a project:

  ```go theme={null}
  exportListService := sdk.Services().Logging().V1().
      LogExport()
  exportList, err := exportListService.ListExports(
      ctx,
      &logging.ListExportsRequest{
          ParentId: "<project_ID>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(exportList)
  ```

  In `ParentId`, specify the [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you exported logs from.

* To check the details and status of a specific export operation:

  ```go theme={null}
  exportInfoService := sdk.Services().Logging().V1().
      LogExport()
  exportInfo, err := exportInfoService.GetExportInfo(
      ctx,
      &logging.GetExportInfoRequest{
          ExportOperationId: "<operation_ID>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(exportInfo)
  ```

  In `ExportOperationId`, specify the operation ID of the export.

**Python SDK**

* To list the details and status of all export operations in a project:

  ```python theme={null}
  export_list_service = LogExportServiceClient(sdk)
  export_list = await export_list_service.list_exports(
      ListExportsRequest(parent_id="<project_ID>"),
  )
  print(export_list)
  ```

  In `parent_id`, specify the [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you exported logs from.

* To check the details and status of a specific export operation:

  ```python theme={null}
  export_info_service = LogExportServiceClient(sdk)
  export_info = await export_info_service.get_export_info(
      GetExportInfoRequest(export_operation_id="<operation_ID>"),
  )
  print(export_info)
  ```

  In `export_operation_id`, specify the operation ID of the export.

**JavaScript SDK**

* To list the details and status of all export operations in a project:

  ```ts theme={null}
  const exportListService = new LogExportService(sdk);
  const exportList = await exportListService.listExports(
    ListExportsRequest.create({
      parentId: "<project_ID>",
    }),
  ).result;
  console.log(exportList);
  ```

  In `parentId`, specify the [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you exported logs from.

* To check the details and status of a specific export operation:

  ```ts theme={null}
  const exportInfoService = new LogExportService(sdk);
  const exportInfo = await exportInfoService.getExportInfo(
    GetExportInfoRequest.create({
      exportOperationId: "<operation_ID>",
    }),
  ).result;
  console.log(exportInfo);
  ```

  In `exportOperationId`, specify the operation ID of the export.

## How to cancel an export

You can cancel an export while its status is `In progress`. If an export has the status `Finished`, you can [delete the exported logs](#how-to-delete-exported-logs) instead.

**Web console**

To cancel an export:

1. On the **Logs** page, switch to the **Exports** tab.
2. Next to the export that you want to cancel, click **Cancel**.
3. In the window that opens, confirm the cancellation.

**CLI**

To cancel an export, run:

```bash theme={null}
nebius logging export cancel --id <operation_ID>
```

In `--id`, specify the operation ID of the export.

**Go SDK**

Cancel an export:

```go theme={null}
cancelResponseService := sdk.Services().Logging().V1().
    LogExport()
cancelResponse, err := cancelResponseService.CancelExportLogs(
    ctx,
    &logging.CancelExportLogsRequest{
        ExportOperationId: "<operation_ID>",
    },
)
if err != nil {
    return err
}
fmt.Println(cancelResponse)
```

In `ExportOperationId`, specify the operation ID of the export.

**Python SDK**

Cancel an export:

```python theme={null}
cancel_response_service = LogExportServiceClient(sdk)
cancel_response = await cancel_response_service.cancel_export_logs(
    CancelExportLogsRequest(export_operation_id="<operation_ID>"),
)
print(cancel_response)
```

In `export_operation_id`, specify the operation ID of the export.

**JavaScript SDK**

Cancel an export:

```ts theme={null}
const cancelResponseService = new LogExportService(sdk);
const cancelResponse = await cancelResponseService.cancelExportLogs(
  CancelExportLogsRequest.create({
    exportOperationId: "<operation_ID>",
  }),
).result;
console.log(cancelResponse);
```

In `exportOperationId`, specify the operation ID of the export.

## How to download exported logs

> [!NOTE]
>
> Exported logs are stored as [objects](https://docs.nebius.com/object-storage/overview.md#objects) in Object Storage buckets. Nebius developer tools don't support downloading objects. Use the web console or, alternatively, [download the log export objects with the AWS CLI](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-download).

1. In the [web console](https://console.nebius.com), go to  **Observability** → **Logs** → **Exports**.
2. Click  → **View bucket** next to the export.
3. In the bucket, open the folder where the logs are stored.
4. Navigate to the file that contains the exported logs.
5. Click  → **Download**.

## How to delete exported logs

> [!NOTE]
>
> Exported logs are stored as [objects](https://docs.nebius.com/object-storage/overview.md#objects) in Object Storage buckets. Nebius developer tools don't support deleting objects. Use the web console or, alternatively, [delete the log export objects with the AWS CLI](https://docs.nebius.com/object-storage/objects/manage.md#how-to-delete-objects).

1. In the [web console](https://console.nebius.com), go to  **Observability** → **Logs** → **Exports**.
2. Click  → **View bucket** next to the export.
3. In the bucket, open the folder where the logs are stored.
4. Navigate to the file that contains the exported logs.
5. Click  → **Delete**.
