# When to use Audit Logs

Source: https://docs.nebius.com/audit-logs/use-cases

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# When to use Audit Logs

Audit Logs allows you to view and filter events for your [tenant](https://docs.nebius.com/iam/overview.md#tenants). This article helps you understand which filters to set when you investigate specific situations, such as:

1. [When you suspect a security incident](#potential-security-incidents).
2. [When resource changes lead to unexpected spending](#unexpected-spending).

Audit events are stored per region, so repeat the search in each relevant region.

## Potential security incidents

If you suspect a security incident in your tenant, Audit Logs can help you track down the events that occurred at the time and investigate possible causes.

### Who made changes to resources, and when?

If you encounter a suspicious change in resources of a given type, review the events that involve resource changes:

**Web console**

* Enter `CREATE`, `UPDATE` or `DELETE` in the **Action** field to see all resource changes.
* Fill in the **Resource type** field to see the changes that concern a specific resource type.

For example, enter `DELETE` in the **Action** field and `computeinstance` in the **Resource type** field to find out which Compute virtual machines were deleted.

See the **Subject** column to find out who made the change.

**CLI**

Set the following filters:

* `action` equal to `CREATE`, `UPDATE` or `DELETE`.
* `resource.metadata.type` equal to the resource type. For example, `computeinstance` for a Compute virtual machine.

For example, to find out which Compute virtual machines were created in the period:

```bash theme={null}
nebius audit v2 audit-event list \
   --parent-id <tenant_ID> \
   --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
   --filter "action='CREATE' AND resource.metadata.type='computeinstance'" \
   --region <region_ID>
```

See the `authentication.subject` parameter of the response to find out who made the change.

### What happened at the time of the incident?

To gain more context when investigating an incident, create granular filters to review the events:

**CLI**

To combine filters, use the following options:

* `AND` logical operator.
* Comparison operators: `=` (equals), `!=` (not equals), `:` (contains).
* [Regular expressions](https://en.wikipedia.org/wiki/Regular_expression#Syntax) (for example, `regex(resource.name, '^.*prod.*$')` to show resources with `prod` in their names).
* Limit the number of entries you receive by using the `--page-size` parameter.

For example, to view 10 events where the user `example@nebius.com` deleted virtual machines between April 1 and April 5, run:

```bash theme={null}
nebius audit v2 audit-event list \
   --parent-id <tenant_ID> \
   --start 2025-04-01T00:00:00Z --end 2025-04-06T00:00:00Z \
   --filter "authentication.subject.name='example@nebius.com' \
      AND action='DELETE' \
      AND resource.metadata.type='computeinstance'" \
   --page-size=10 \
   --region <region_ID>
```

If there are more than 10 events, get the `next_page_token` value from the response and run the same command again with an additional `--page-token=<next_page_token>` parameter to get the next batch.

## Unexpected spending

If you see a sudden increase in spending, Audit Logs can help you find out more about the resources that are used in your tenant.

### What happened with a specific resource?

A particular resource may cause more spending than you expected. Get the events that are associated with this resource:

**Web console**

Enter the resource ID in the **Resource ID** field.

**CLI**

* If you know the resource name, filter by `resource.metadata.name`.
* If you know the resource ID, filter by `resource.metadata.id`.

For example:

```bash theme={null}
nebius audit v2 audit-event list \
   --parent-id <tenant_ID> \
   --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
   --filter "resource.metadata.name='<name>'" \
   --region <region_ID>
```

### Who created a new resource?

Unexpected spending may be caused by creating more resources than necessary. To investigate who created them, get the resource creation events:

**Web console**

Fill in the **Resource type** field and enter `CREATE` in the **Action** field to see when resources of a specific type were created.

For example, enter `computeinstance` in the **Resource type** field and `CREATE` in the **Action** field to see all events where a Compute virtual machine was created.

See the **Subject** column to find out who made the change.

**CLI**

Set the following filters:

* `action` equal to `CREATE`.
* `resource.metadata.type` equal to the resource type. For example, `computeinstance` for a Compute virtual machine.

For example:

```bash theme={null}
nebius audit v2 audit-event list \
   --parent-id <tenant_ID> \
   --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
   --filter "action='CREATE' AND resource.metadata.type='computeinstance'" \
   --region <region_ID>
```

See the `authentication.subject` parameter of the response to find out who made the change.
