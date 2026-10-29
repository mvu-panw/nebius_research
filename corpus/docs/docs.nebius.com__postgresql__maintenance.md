# Maintenance in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/maintenance

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Maintenance in Managed Service for PostgreSQL®

Nebius AI Cloud performs maintenance of the Managed PostgreSQL clusters. This page explains how to get information about the maintenance schedule and reschedule maintenance operations.

## Prerequisites

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Install [jq](https://jqlang.github.io/jq/) to extract IDs and tokens from the JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

## How to get a list of all maintenance operations

Run the following command to get a list of all past and upcoming maintenance operations:

```bash theme={null}
nebius maintenance v1alpha1 maintenance list
```

This command returns a list of all maintenance operations. You can use this information to make sure that you are not relying on a resource that is unavailable due to maintenance. Each item contains:

* `metadata.id`: The ID of the maintenance operation. You can use this ID to [get the details of an operation](#how-to-get-the-details-of-a-maintenance-operation) or [edit it](#how-to-reschedule-a-maintenance-operation).
* `metadata.parent_id`: The ID of the project that contains the resource affected by the maintenance.
* `metadata.created_at`: The time that the maintenance operation was created.
* `spec.scheduled_at`: The time that maintenance is scheduled for, in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
* `status.affected_resources`: The identifiers of resources affected by the maintenance and the ID of the project they belong to (`parent_id`).

  If the maintenance event affects your resources in another service, they are also listed here. You can [filter the output](#filtering-the-output) to see only the affected resources for Managed PostgreSQL clusters.
* `status.state`: The state of the maintenance, for example, `STATE_FINISHED`, `STATE_SCHEDULED` or `STATE_CANCELLED`.
* `status.reschedulable`: If set to `true`, and `status.state` is set to `STATE_SCHEDULED`, you can reschedule the maintenance.

### Filtering the output

To filter the list output by PostgreSQL clusters, run the following command:

```bash theme={null}
nebius maintenance v1alpha1 maintenance list \
  --format json \
| jq '
  .items[]
  | select(any(.status.affected_resources[]?; .id | startswith("postgresql-")))
  | .status.affected_resources |= map(select(.id | startswith("postgresql-")))
'
```

This command returns only maintenance operations that affect PostgreSQL clusters, and removes resources belonging to other Nebius AI Cloud services from the `affected_resources` array of each list item.

## How to get the details of a maintenance operation

To get the details related to a maintenance operation, run the following command:

```bash theme={null}
nebius maintenance v1alpha1 maintenance get --id <maintenance_operation_ID>
```

This command returns the details of a maintenance operation. The details returned are the same as the ones returned when you [list](#how-to-get-a-list-of-all-maintenance-operations) all maintenance operations.

> **Output example**
>
> ```yaml theme={null}
> metadata:
>     id: maintenance_***
>     parent_id: project-***
>     created_at: "2025-09-22T14:40:59.845329Z"
> spec:
>     scheduled_at: "2025-10-01T14:28:20Z"
> status:
>     affected_resources:
>       - id: postgresql-***
>         parent_id: project-***
>     started_at: "2025-10-01T14:28:21.162373Z"
>     finished_at: "2025-10-01T14:34:38.363547Z"
>     state: STATE_FINISHED
>     reschedulable: true
> ```

## How to reschedule a maintenance operation

You can reschedule a maintenance operation if it meets the following conditions:

* `status.state` is set to `STATE_SCHEDULED`.
* `reschedulable` is set to `true`.

To reschedule maintenance:

1. Run the following command:

   ```bash theme={null}
   nebius maintenance v1alpha1 maintenance edit --id <maintenance_operation_ID>
   ```

2. In the editor that opens, change the value of `spec.scheduled_at` to your desired time in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format. Keep in mind that you can only specify a date and time that is in the future.

3. When prompted, confirm the update.

After you reschedule a maintenance operation, use the `get` command to [check the updated details](#how-to-get-the-details-of-a-maintenance-operation).

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
