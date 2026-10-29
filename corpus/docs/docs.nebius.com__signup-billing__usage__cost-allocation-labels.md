# Cost allocation labels in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/usage/cost-allocation-labels

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cost allocation labels in Nebius AI Cloud

Add labels to resources to group your costs the way you need, and see how costs are allocated across the groups. You can group resources by label where each label represents, for example, a particular service, application or team. To see a breakdown of costs, filter your costs by label on the [Billing → Usage](https://console.nebius.com/billing/consumption) page, or [export usage data as a CSV file](https://docs.nebius.com/signup-billing/usage/export.md) and check the `Tags` column.

A *label* represents a key-value pair you set on a resource when you create or update it. Keys and values can be arbitrary — set the ones convenient for you. On the **Usage** page, you can filter resources by both keys and values. For example, to check costs by application and team, you can set such labels as `application = argo-cd` and `application = gatekeeper` or `team = engineering` and `team = support`.

> [!NOTE]
>
> Cost allocation labels are only available for [Compute billable resources](https://docs.nebius.com/compute/resources/pricing.md). Labels assigned to other resources are unavailable in the billing report.

## How to set labels on resources

**CLI**

In the `create` or `update` command, add the `--labels` parameter. Example for a virtual machine:

```bash theme={null}
nebius compute instance create --labels <key>=<value> ...
```

To make sure that the label has been assigned to the resource successfully, check the resource configuration by using the `get` or `get-by-name` commands. For example:

```bash theme={null}
nebius compute instance get <VM_ID>
```

Output:

```text theme={null}
metadata:
  id: computeinstance-***
  ...
  labels:
    <key>: <value>
```

**Terraform**

In the resource configuration, add the `labels` parameter. Example for a virtual machine:

```hcl theme={null}
resource "nebius_compute_v1_instance" "my_vm" {
  labels = {
    <key> = "<value>"
  }
  # ...
}
```

## How to view the cost allocation breakdown by labels

You can check the cost allocation breakdown in the web console directly, or you can export usage data:

**Web console**

1. In the [web console](https://console.nebius.com/), go to  **Billing** → **Usage**.

2. If you select the  **Table** view:

   1. In the **Filter by** field, select `Label`.
   2. In the **Labels** field, select the keys and values of the needed labels.

      If you only select a key, all its values are automatically included.

3. If you select the  **Chart** view:

   1. In the **Group by** field, select `Label`.
   2. In the **Labels** field, select the keys of the needed labels. All values of the selected keys are automatically included.

As a result, the dashboard only shows the resources and costs that are relevant to the selected labels.

**Export**

1. [Export usage data as a CSV file](https://docs.nebius.com/signup-billing/usage/export.md#how-to-create-an-export).
2. Open the CSV file.
3. Filter data by the `Tags` column.

As a result, the report only shows the resources and costs that are relevant to the selected labels.
