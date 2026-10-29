# Managing project limits for capacity block groups

Source: https://docs.nebius.com/overview/limits/manage-project-limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing project limits for capacity block groups

Use [project limits](https://docs.nebius.com/overview/limits/project-limits.md) (also called capacity allowance) to control how much of a capacity block group (CBG) a project can consume. This article explains how to view, set, remove and disable project limits for capacity block groups.

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to view project limits

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **Limits**.
2. Open the **Capacity block groups** tab.
3. Click the capacity block group that you want to view.
4. Open the **Project limits** tab.

The table shows the following for each project:

* **Usage**: Current GPU consumption from the CBG. If usage exceeds the project limit or the current CBG size, running workloads continue, but new CBG allocations are blocked. Usage above the CBG size is billed at [pay-as-you-go (PAYG) prices](https://docs.nebius.com/signup-billing/billing-models/payg.md#payg-prices).
* **Limit**: Configured and effective limits of GPU consumption, if they differ. The effective limit is always capped at the current CBG size.

**CLI**

To view the project limits for a specific CBG, run:

```bash theme={null}
nebius capacity capacity-allowance list-by-capacity-block-group \
  --capacity-block-group-id <CBG_ID>
```

To get the CBG ID, run:

```bash theme={null}
nebius capacity capacity-block-group list
```

## How to set a custom project limit

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **Limits**.
2. Open the **Capacity block groups** tab.
3. Click the capacity block group that you want to set a project limit for.
4. Open the **Project limits** tab.
5. In the row of the required project, click  → **Set custom limit**.
6. Enter the limit value and click **Save changes**.

**CLI**

To set a custom limit for a specific CBG, run:

```bash theme={null}
nebius capacity capacity-allowance create \
  --capacity-block-group-id <CBG_ID> \
  --parent-id <project_ID> \
  --limit <limit_value>
```

In the command, specify the parameters:

* `--capacity-block-group-id`: ID of the CBG where you want to set a custom limit. To get it, run:

  ```bash theme={null}
  nebius capacity capacity-block-group list
  ```

* `--parent-id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3).

* `--limit`: Project limit value you want to set.

> [!NOTE]
>
> Setting the limit to `0` [disables](https://docs.nebius.com/overview/limits/manage-project-limits.md#how-to-disable-cbg-usage-for-a-project) CBG usage for the project.

## How to remove a project limit

Removing a project limit removes the configured value. The effective limit becomes the current capacity block group size.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **Limits**.
2. Open the **Capacity block groups** tab.
3. Click the capacity block group that you want to remove a project limit from.
4. Open the **Project limits** tab.
5. In the row of the required project, click  → **Limit by CBG size**.

**CLI**

To remove a specific project limit from a CBG, run:

```bash theme={null}
nebius capacity capacity-allowance delete <capacity_allowance_ID>
```

In the command, specify the project limit ID. To get it, run:

```bash theme={null}
nebius capacity capacity-allowance list-by-capacity-block-group \
  --capacity-block-group-id <CBG_ID>
```

To get the CBG ID, run:

```bash theme={null}
nebius capacity capacity-block-group list
```

## How to disable CBG usage for a project

> [!WARNING]
>
> When you disable CBG usage, running workloads continue, but can't restart once stopped. New CBG allocations are not possible.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **Limits**.
2. Open the **Capacity block groups** tab.
3. Click the capacity block group where you want to disable CBG usage for a project.
4. Open the **Project limits** tab.
5. In the row of the required project, click  → **Disable CBG usage**.

You can also disable CBG usage for a project by setting the project limit to `0`.

**CLI**

To disable CBG usage for a project, set the project limit to `0`:

```bash theme={null}
nebius capacity capacity-allowance create \
  --capacity-block-group-id <CBG_ID> \
  --parent-id <project_ID> \
  --limit 0
```

In the command, specify the parameters:

* `--capacity-block-group-id`: CBG ID. To get it, run:

  ```bash theme={null}
  nebius capacity capacity-block-group list
  ```

* `--parent-id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3).
