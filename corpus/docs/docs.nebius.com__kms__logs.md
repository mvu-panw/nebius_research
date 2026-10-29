# Logs in Key Management Service

Source: https://docs.nebius.com/kms/logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Logs in Key Management Service

Key Management Service (KMS) keeps logs of actions that are performed on symmetric and asymmetric keys. You can view and analyze these logs as events in the [Audit Logs](https://docs.nebius.com/audit-logs/index.md) service.

KMS only supports *control plane logs*. They describe key management and lifecycle events, such as [creating](https://docs.nebius.com/kms/manage/create.md), [updating](https://docs.nebius.com/kms/manage/update.md), [deleting](https://docs.nebius.com/kms/manage/delete-restore.md) or [rotating](https://docs.nebius.com/kms/manage/rotate.md) a key.

## Prerequisites

**Web console**

Make sure that you have a role that allows you to [view audit events](https://docs.nebius.com/audit-logs/events/view.md#prerequisites).

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure that you have a role that allows you to [view audit events](https://docs.nebius.com/audit-logs/events/view.md#prerequisites).

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure that the service account you use with the SDK is in a group with a role that allows [viewing audit events](https://docs.nebius.com/audit-logs/events/view.md#prerequisites). The default `editors` group doesn't have this role.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure that the service account you use with the SDK is in a group with a role that allows [viewing audit events](https://docs.nebius.com/audit-logs/events/view.md#prerequisites). The default `editors` group doesn't have this role.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure that the service account you use with the SDK is in a group with a role that allows [viewing audit events](https://docs.nebius.com/audit-logs/events/view.md#prerequisites). The default `editors` group doesn't have this role.

## How to view logs

**Web console**

1. In the sidebar, go to  **Administration** → **Audit Logs**.
2. Select the region to search for KMS audit events.
3. Select **Control plane**.
4. Filter events by the `KMS` service. If this filter is not displayed, click **Filters** and then select **Service**.

**CLI**

Run [nebius audit v2 audit-event list](https://docs.nebius.com/cli/reference/audit/v2/audit-event/list.md):

```bash theme={null}
nebius audit v2 audit-event list \
   --parent-id <tenant_ID> \
   --start <time_in_ISO_8601> \
   --end <time_in_ISO_8601> \
   --filter "service.name='KMS'" \
   --event-type control_plane \
   --region <region_ID>
```

In the command, specify:

* `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
* `--start`: Start time for the search, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
* `--end`: End time for the search, in the ISO 8601 format.
* `--region`: [Region](https://docs.nebius.com/overview/regions.md) to search for KMS audit events.
* `--filter`: Filter expression. Set it to `service.name='KMS'` to return only KMS events. For more information, see [How to filter audit events](https://docs.nebius.com/audit-logs/events/filter.md).
* `--event-type`: Type of audit event. Set it to `control_plane` because KMS only supports control plane logs.

**Go SDK**

List KMS audit events:

```go theme={null}
auditService := sdk.Services().Audit().V2().AuditEvent()
startTime, err := time.Parse(time.RFC3339, "<time_in_ISO_8601>")
if err != nil {
    return fmt.Errorf("parse start time: %w", err)
}
endTime, err := time.Parse(time.RFC3339, "<time_in_ISO_8601>")
if err != nil {
    return fmt.Errorf("parse end time: %w", err)
}
events, err := auditService.List(
    ctx,
    &audit.ListAuditEventRequest{
        ParentId: "<tenant_ID>",
        Start: timestamppb.New(startTime),
        End: timestamppb.New(endTime),
        Filter: "service.name='KMS'",
        EventType: audit.EventType_CONTROL_PLANE,
        Region: "<region_ID>",
    },
)
if err != nil {
    return fmt.Errorf("list audit events: %w", err)
}
fmt.Println(events)
```

In the code, specify:

* `ParentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).
* `Start`: Start time for the search, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format with a timezone, for example, `2026-05-07T10:00:00Z`.
* `End`: End time for the search, in the ISO 8601 format with a timezone.
* `Filter`: Filter expression. Set it to `service.name='KMS'` to return only KMS events. For more information, see [How to filter audit events](https://docs.nebius.com/audit-logs/events/filter.md).
* `EventType`: Type of audit event. Set it to `audit.EventType_CONTROL_PLANE` because KMS only supports control plane logs.
* `Region`: [Region](https://docs.nebius.com/overview/regions.md) to search for KMS audit events.

**Python SDK**

List KMS audit events:

```python theme={null}
service = audit.AuditEventServiceClient(sdk)
events = await service.list(
    audit.ListAuditEventRequest(
        parent_id="<tenant_ID>",
        start=datetime.fromisoformat("<time_in_ISO_8601>"),
        end=datetime.fromisoformat("<time_in_ISO_8601>"),
        filter="service.name='KMS'",
        event_type=audit.EventType.CONTROL_PLANE,
        region="<region_ID>",
    ),
)
print(events)
```

In the code, specify:

* `parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).
* `start`: Start time for the search, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
* `end`: End time for the search, in the ISO 8601 format.
* `filter`: Filter expression. Set it to `service.name='KMS'` to return only KMS events. For more information, see [How to filter audit events](https://docs.nebius.com/audit-logs/events/filter.md).
* `event_type`: Type of audit event. Set it to `audit.EventType.CONTROL_PLANE` because KMS only supports control plane logs.
* `region`: [Region](https://docs.nebius.com/overview/regions.md) to search for KMS audit events.

**JavaScript SDK**

List KMS audit events:

```ts theme={null}
const auditService = new audit.AuditEventService(sdk);
const events = await auditService.list(
  audit.ListAuditEventRequest.create({
    parentId: "<tenant_ID>",
    start: dayjs("<time_in_ISO_8601>"),
    end: dayjs("<time_in_ISO_8601>"),
    filter: "service.name='KMS'",
    eventType: audit.EventType.CONTROL_PLANE,
    region: "<region_ID>",
  }),
).result;
console.log(events);
```

In the code, specify:

* `parentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).
* `start`: Start time for the search, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
* `end`: End time for the search, in the ISO 8601 format.
* `filter`: Filter expression. Set it to `service.name='KMS'` to return only KMS events. For more information, see [How to filter audit events](https://docs.nebius.com/audit-logs/events/filter.md).
* `eventType`: Type of audit event. Set it to `audit.EventType.CONTROL_PLANE` because KMS only supports control plane logs.
* `region`: [Region](https://docs.nebius.com/overview/regions.md) to search for KMS audit events.

For more details, see [Viewing events in Audit Logs](https://docs.nebius.com/audit-logs/events/view.md).

Parameters of an action, such as creating a key, are returned in the `.request.parameters` field of the Audit Logs event. For example:

```json theme={null}
{
  "request": {
    "parameters": {
      "metadata": {
        "id": "<key_ID>",
        "parent_id": "<project_ID>",
        "name": "<key_name>",
        "resource_version": "0",
        "labels": {}
      },
      "spec": {
        "description": "<key_description>",
        "algorithm": "<key_algorithm>"
      }
    }
  }
}
```

For more details, see [Structure and fields of events in Audit Logs](https://docs.nebius.com/audit-logs/events/reference.md).
