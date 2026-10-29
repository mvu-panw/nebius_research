# How to filter audit events

Source: https://docs.nebius.com/audit-logs/events/filter

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to filter audit events

You can filter audit events when [viewing](https://docs.nebius.com/audit-logs/events/view.md) or [exporting](https://docs.nebius.com/audit-logs/events/export.md) them to narrow down the results. The filter syntax is the same for both operations, with one exception: the `authentication.subject.name` filter is not available in exports because it can contain email addresses that are [personally identifiable information (PII)](https://en.wikipedia.org/wiki/Personal_data).

## Filter operators

Supported operators include:

* `=` equals
* `!=` not equals
* `:` contains
* `regex` regular expression match

## How to filter events in the web console

To narrow down the events, you can use the following filters:

* **Event JSONs**: Search in JSON field values, but not a full-text search for a substring in the JSON event description. For example, if the JSON contains a `name` field with the value `Test User`, this filter finds `Test User` but cannot find `"name": "Test User"`.
* **Action**: Standard actions are `CREATE`, `UPDATE` or `DELETE`. Actions can differ by service. For example, for Compute resources, you can also specify `STOP` and `START`.
* **Ancestor ID**: ID of the resource ancestor, starting from the tenant.
* **Ancestor name**: Name of the resource ancestor, starting from the tenant.
* **Masked token**: [Access token](https://docs.nebius.com/iam/authorization/access-tokens.md) that was used to authorize the event. You can enter a part of the token here.
* **Resource ID**: ID of the resource on which actions were performed. For example, a Compute disk (`computedisk-***`), a service account (`serviceaccount-***`), etc.
* **Resource name**: Name of the resource on which actions were performed.
* **Resource type**: Type of the resource on which actions were performed. For example, `computedisk` or `mk8scluster`.
* **Service**: [Service](https://docs.nebius.com/audit-logs/services.md) in which the actions were performed.
* **Event class**: A string in the `ai.nebius.<service_name>.<resource_type>.<action>` format. It includes the `ai.nebius` prefix and refers to a Nebius AI Cloud service, type of resource in it and the action performed on this resource, for example, `ai.nebius.compute.computeinstance.delete`.
* **Static key ID**: ID of the [static key](https://docs.nebius.com/iam/authorization/static-keys/index.md) that was used to authorize the event.
* **Status**: Status of the operation associated with the event.
* **Subject ID**: ID of a user account or a service account that performed actions. The formats of user account IDs and service account IDs are `tenantuseraccount-***` and `serviceaccount-***`.
* **Subject name**: Name of a user account or a service account that performed actions. This filter is not available for exports.

Click `=` in a filter to choose if the events should contain or exclude the values you enter.

## How to filter events by using the CLI

To narrow down the events, you can use one or more of the following filters:

* **Resource ID or type**

  The type or ID of the resource on which actions were performed. ID formats include, for example, a `computeinstance-***` for a Compute virtual machine, `computedisk-***` for a Compute disk, `serviceaccount-***` for a service account.

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "resource.metadata.type='computeinstance'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "resource.metadata.id='computeinstance-***'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "resource.metadata.type='computeinstance'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "resource.metadata.id='computeinstance-***'" \
     --region <region_ID>
  ```

* **Resource ancestor ID or name**

  The ID or name of the resource ancestor, starting from the tenant. For example, you can check all the actions performed on virtual machines in one of your projects by specifying the project ID or name.

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "resource.hierarchy.id:'<ancestor_ID>'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "resource.hierarchy.name:'<ancestor_name>'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "resource.hierarchy.id:'<ancestor_ID>'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "resource.hierarchy.name:'<ancestor_name>'" \
     --region <region_ID>
  ```

* **Event action**

  Specify the action: `CREATE`, `UPDATE` or `DELETE`. Actions can differ by service. For example, for Compute resources, you can also specify `STOP` and `START`.

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "action='DELETE'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "action='DELETE'" \
     --region <region_ID>
  ```

* **Service** in which the event occurred.

  See the [list of services](https://docs.nebius.com/audit-logs/services.md).

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "service.name='COMPUTE'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "service.name='COMPUTE'" \
     --region <region_ID>
  ```

* **Event class**

  A string in the `ai.nebius.<service_name>.<resource_type>.<action>` format. It includes the `ai.nebius` prefix and refers to a Nebius AI Cloud service, type of resource in it and the action performed on this resource, for example, `ai.nebius.compute.computeinstance.delete`.

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "type='ai.nebius.compute.computeinstance.delete'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "type='ai.nebius.compute.computeinstance.delete'" \
     --region <region_ID>
  ```

* **Subject name or ID**

  The name or ID of a user account or a service account that performed actions. The formats of user account IDs and service account IDs are `tenantuseraccount-***` and `serviceaccount-***`. The `authentication.subject.name` filter is not available for exports.

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "authentication.subject.name='<user_email>'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "authentication.subject.tenant_user_id='tenantuseraccount-***'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "authentication.subject.service_account_id='serviceaccount-***'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "authentication.subject.tenant_user_id='tenantuseraccount-***'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "authentication.subject.service_account_id='serviceaccount-***'" \
     --region <region_ID>
  ```

* **Subject credentials**

  For [access tokens](https://docs.nebius.com/iam/authorization/access-tokens.md), use `authentication.token_credential.masked_token` without a signature. For AWS-compatible [access keys](https://docs.nebius.com/iam/service-accounts/access-keys.md), use `authentication.static_key_credential.id`.

  **View**

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "authentication.token_credential.masked_token='<token_without_signature>'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event list \
     --parent-id <tenant_ID> \
     --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
     --filter "authentication.static_key_credential.id='<access_key_ID>'" \
     --region <region_ID>
  ```

  **Export**

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "authentication.token_credential.masked_token='<token_without_signature>'" \
     --region <region_ID>
  ```

  ```bash theme={null}
  nebius audit v2 audit-event-export start \
     --parent-id <tenant_ID> \
     --params-from <time_in_ISO_8601> --params-to <time_in_ISO_8601> \
     --params-event-type <control_plane|data_plane> \
     --nebius-object-storage-bucket-by-id-id <bucket_ID> \
     --nebius-object-storage-object-prefix <prefix> \
     --params-filter "authentication.static_key_credential.id='<access_key_ID>'" \
     --region <region_ID>
  ```

## How to combine filters

To combine filters, use the following options:

* `AND` logical operator.
* Comparison operators: `=` (equals), `!=` (not equals), `:` (contains).
* [Regular expressions](https://en.wikipedia.org/wiki/Regular_expression#Syntax) (for example, `regex(resource.name, '^.*prod.*$')` to show resources with `prod` in their names).

## Examples

**View**

For example, to view all events where the user `example@nebius.com` deleted virtual machines between April 1 and April 5, run:

```bash theme={null}
nebius audit v2 audit-event list \
   --parent-id <tenant_ID> \
   --start <time_in_ISO_8601> --end <time_in_ISO_8601> \
   --filter "authentication.subject.tenant_user_id='example@nebius.com' \
      AND action='DELETE' \
      AND resource.metadata.type='computeinstance'" \
   --region <region_ID>
```

**Export**

For example, to export all events where a specific user deleted virtual machines between April 1 and April 5, run:

```bash theme={null}
nebius audit v2 audit-event-export start \
   --parent-id <tenant_ID> \
   --params-from 2025-04-01T00:00:00Z --params-to 2025-04-06T00:00:00Z \
   --params-event-type <control_plane|data_plane> \
   --nebius-object-storage-bucket-by-id-id <bucket_ID> \
   --nebius-object-storage-object-prefix <prefix> \
   --params-filter "authentication.subject.tenant_user_id='<tenant_user_ID>' \
      AND action='DELETE' \
      AND resource.metadata.type='computeinstance'" \
   --region <region_ID>
```

For more details about the fields, see [Structure and fields of events in Audit Logs](https://docs.nebius.com/audit-logs/events/reference.md).
