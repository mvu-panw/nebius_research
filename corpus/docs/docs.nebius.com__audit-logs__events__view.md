# Viewing events in Audit Logs

Source: https://docs.nebius.com/audit-logs/events/view

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Viewing events in Audit Logs

An *audit event* is a data record that captures something that happened in Nebius AI Cloud, along with metadata that provides additional context. The metadata shows how events relate to resources or to each other. Each event in Audit Logs has a JSON representation that conforms to the [CloudEvents specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md).

You can use the Nebius AI Cloud web console or CLI to view and filter audit events for your [tenant](https://docs.nebius.com/iam/overview.md#tenants).

## Prerequisites

* Identify the regions to search for the audit events you need.
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` or `auditlogs.audit-event-viewer` role within your tenant. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to view events

**Web console**

In the sidebar, go to  **Administration** → **Audit Logs**. To work with the events on this page, you can do the following:

* On the **Logs** tab:
  * Select the event type: **Control plane** or **Data plane**. Control plane events track management operations on resources (such as creating or deleting virtual machines). Data plane events track data access operations (such as reading or writing objects in Object Storage).
  * Select the region.
  * View event JSONs. To do this, click  in an event's row.
  * Filter events by period or [by using filters](https://docs.nebius.com/audit-logs/events/filter.md#how-to-filter-events-in-the-web-console). Click  **Filters** and select the filters you need.

* On the **Metrics** tab:
  * Select the event type: **Control plane** or **Data plane**.
  * Select the region.
  * View the number of events processed per second in a specific region and time period.
  * Only for data plane events, view information related to quota usage. For more information, see [Quotas in Audit Logs](https://docs.nebius.com/audit-logs/resources/quotas-limits.md).

**CLI**

1. Get all events in the tenant:

   ```bash theme={null}
   nebius audit v2 audit-event list \
      --parent-id <tenant_ID> \
      --start <time_in_ISO_8601> \
      --end <time_in_ISO_8601> \
      --region <region_ID>
   ```

   In the command above, specify:

   * `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
   * `--start`: Start time for the search, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
   * `--end`: End time for the search, in the ISO 8601 format.
   * `--region`: [Region](https://docs.nebius.com/overview/regions.md) to search for audit events.
     For example, to get all the events that happened in March 2025, run the following command:

   ```bash theme={null}
   nebius audit v2 audit-event list --parent-id <tenant_ID> \
     --start 2025-03-01T00:00:00Z \
     --end 2025-04-01T00:00:00Z \
     --region <region_ID>
   ```

2. (Optional) By default, only control plane events are shown.

   * **Control plane events** (default): Track management operations on resources, such as creating, updating or deleting virtual machines, clusters or other infrastructure resources.

   * **Data plane events**: Track data access operations, such as reading or writing objects in Object Storage buckets.

   To view data plane events, specify `data_plane` in the `--event-type` parameter:

   ```bash theme={null}
   nebius audit v2 audit-event list \
      --parent-id <tenant_ID> \
      --start <time_in_ISO_8601> \
      --end <time_in_ISO_8601> \
      --event-type data_plane \
      --region <region_ID>
   ```

3. (Optional) To narrow down events, use [filters](https://docs.nebius.com/audit-logs/events/filter.md#how-to-filter-events-by-using-the-cli).
