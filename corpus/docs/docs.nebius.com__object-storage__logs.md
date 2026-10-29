# Logs in Object Storage

Source: https://docs.nebius.com/object-storage/logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Logs in Object Storage

Object Storage keeps logs of actions that are performed on buckets and objects. You can view and analyze these logs as events in the [Audit Logs](https://docs.nebius.com/audit-logs/index.md) service.

There are two types of logs in Object Storage:

* *Control plane logs* describe actions on buckets, such as creating and deleting buckets or getting and updating buckets' settings. Control plane logs are always available for all buckets.
* *Data plane logs* describe actions on objects, such as uploading, downloading and deleting objects. By default, Object Storage does not keep data plane logs for your buckets. For each individual bucket, you can enable partial or full data plane logging. This can help you identify object usage patterns to optimize storage costs, improve performance of critical parts of your applications and comply with regulations, such as the [Health Insurance Portability and Accountability Act](https://www.hhs.gov/hipaa/index.html) (HIPAA).

  > [!NOTE]
  >
  > Data plane logs are in [preview](https://docs.nebius.com/overview/services.md#preview). Before enabling them, [contact support](https://console.nebius.com/support/create-ticket).

  Audit Logs has a throughput quota for data plane logs. Logs beyond that quota are not recorded. You can monitor data plane events to avoid exceeding the quota. For more information, see [Quotas in Audit Logs](https://docs.nebius.com/audit-logs/resources/quotas-limits.md).

## How to configure data plane logs

To configure data plane logs for a bucket, you need the `admin` [role](https://docs.nebius.com/iam/authorization/roles.md) for the bucket, its parent project or tenant.

**Web console**

You can configure data plane logs when [creating a bucket](https://console.nebius.com/storage/create) or on the **Settings** page of an existing bucket:

1. Enable or disable the **Data plane Audit Logs** setting.
2. If the setting is on, choose whether to log all actions or only actions that change objects. See the [list of logged data plane actions](#logged-data-plane-actions).

**Nebius AI Cloud CLI**

To configure data plane logs when [creating](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets) (`nebius storage bucket create`) or [modifying buckets](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-modify-buckets) (`nebius storage bucket update`), add the `--object-audit-logging` parameter to the command:

* `--object-audit-logging all`: All data plane actions are logged.
* `--object-audit-logging mutate_only`: Only data plane actions that change objects are logged.
* `--object-audit-logging none` (default): Data plane actions are not logged.

See the [list of logged data plane actions](#logged-data-plane-actions).

For example, to enable full data plane logging in an existing bucket, run the following command:

```bash theme={null}
nebius storage bucket update \
  --id <bucket_ID> \
  --object-audit-logging all
```

**Terraform**

To configure data plane logs when [creating](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets) or [modifying buckets](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-modify-buckets), add the `object_audit_logging` parameter to the `nebius_storage_v1_bucket` resource:

* `object_audit_logging = "all"`: All data plane actions are logged.
* `object_audit_logging = "mutate_only"`: Only data plane actions that change objects are logged.
* `object_audit_logging = "none"` (default): Data plane actions are not logged.

See the [list of logged data plane actions](#logged-data-plane-actions).

For example, to enable full data plane logging in a bucket, use the following configuration:

```hcl theme={null}
resource "nebius_storage_v1_bucket" "my_bucket" {
  name                 = "<bucket_name>"
  parent_id            = "<project_ID>"
  object_audit_logging = "all"
}
```

For more information about the `nebius_storage_v1_bucket` resource, see the [Terraform provider documentation](https://docs.nebius.com/terraform-provider/reference/resources/storage_v1_bucket.md).

Changes to existing buckets may take some time to apply. For example, if you enable data plane logs in an existing bucket, there may be a delay before logging begins.

### Logged data plane actions

Depending on whether you enabled all data plane logs (`all`) or only logs for actions that change objects (`mutate_only`), Object Storage logs actions that are performed by using the following [S3 API methods](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html):

| Method | `all` | `mutate_only` |
| - | - | - |
| `PutObject` | ✓ | ✓ |
| `CopyObject` | ✓ | ✓ |
| `CreateMultipartUpload` | ✓ | ✓ |
| `UploadPart` | ✓ | ✓ |
| `UploadPartCopy` | ✓ | ✓ |
| `AbortMultipartUpload` | ✓ | ✓ |
| `CompleteMultipartUpload` | ✓ | ✓ |
| `DeleteObject` | ✓ | ✓ |
| `DeleteObjects` | ✓ | ✓ |
| `DeleteObjectVersion` | ✓ | ✓ |
| `GetObject` | ✓ | — |
| `HeadObject` | ✓ | — |
| `ListParts` | ✓ | — |
| `ListObjectVersions` | ✓ | — |
| `ListObjects` | ✓ | — |
| `ListMultipartUploads` | ✓ | — |

Actions that do not create, read, update or delete objects themselves, such as `GetObjectAcl` or `PutObjectTagging`, are not logged, even if Object Storage supports them. Requests that result in HTTP client errors `400 Bad Request` and `429 Too Many Requests` are also not logged.

## How to view logs

You can view control plane logs and data plane logs from buckets that have them enabled in Audit Logs:

**Web console**

1. In the sidebar, go to  **Administration** → **Audit Logs**.
2. Select the region to search for Object Storage audit events.
3. Select **Control plane** or **Data plane**.
4. Filter events by the `STORAGE` service. If this filter is not displayed, click **Filters** and then select **Service**.

**Nebius AI Cloud CLI**

Run [nebius audit v2 audit-event list](https://docs.nebius.com/cli/reference/audit/v2/audit-event/list.md) to get control plane logs:

```bash theme={null}
nebius audit v2 audit-event list \
  --parent-id <tenant_ID> \
  --start <time_in_ISO_8601> \
  --end <time_in_ISO_8601> \
  --filter "service.name='STORAGE'" \
  --event-type control_plane \
  --region <region_ID>
```

In the command above, specify:

* `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
* `--start`: Start time for the search, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
* `--end`: End time for the search, in the ISO 8601 format.
* `--region`: [Region](https://docs.nebius.com/overview/regions.md) to search for Object Storage audit events.
* `--filter`: Filter expression. Set it to `service.name='STORAGE'` to return only Object Storage events. For more information, see [How to filter audit events](https://docs.nebius.com/audit-logs/events/filter.md).
* `--event-type`: Type of audit event. Set it to `control_plane` to return control plane logs.

To get data plane logs, replace `--event-type control_plane` with `--event-type data_plane`:

```bash theme={null}
nebius audit v2 audit-event list \
  --parent-id <tenant_ID> \
  --start <time_in_ISO_8601> \
  --end <time_in_ISO_8601> \
  --filter "service.name='STORAGE'" \
  --event-type data_plane \
  --region <region_ID>
```

For more details, see [Viewing events in Audit Logs](https://docs.nebius.com/audit-logs/events/view.md).

Parameters of an action, such as the bucket name and the object key, are returned in the `.request.parameters` field of the Audit Logs event. For example:

```json theme={null}
{
  "request": {
    "parameters": {
      "bucket_name": "bucket-test",
      "object_key": "data/config.yaml",
      "version": "0[isNull=true,isLatest=false]"
    }
  }
}
```

For more details, see [Structure and fields of events in Audit Logs](https://docs.nebius.com/audit-logs/events/reference.md).
