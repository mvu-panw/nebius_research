# Exporting usage data as CSV in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/usage/export

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Exporting usage data as CSV in Nebius AI Cloud

An *export* helps you integrate Nebius usage data with external tools for cost analysis and reporting. The export delivers data in CSV format that complies with the [FinOps Open Cost and Usage Specification (FOCUS 1.2)](https://focus.finops.org/focus-specification/v1-2/). For known conformance gaps and workarounds, see [FOCUS conformance](https://docs.nebius.com/signup-billing/usage/focus-conformance.md). This specification is compatible with most industry-standard cost management systems.

The export contains detailed hourly information about everything that affects your invoice: commitment consumption, adjustments and taxes.

## Export types

There are two types of exports available:

* **One-time exports** that you can create in the [web console](https://console.nebius.com/) or by using [Nebius AI Cloud developer tools](https://docs.nebius.com/developer-tools.md).
* **Periodic export** that you configure in the [web console](https://console.nebius.com/). It runs automatically on a regular schedule and delivers data to your [Object Storage](https://docs.nebius.com/object-storage/index.md) bucket once per hour. You are charged for storing and working with data in Object Storage; for more details, see [Pricing in Object Storage](https://docs.nebius.com/object-storage/resources/pricing.md).

  > [!NOTE]
  >
  > You can have one active periodic export at a time for a given contract.

## One-time exports

### Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Nebius AI Cloud CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

### How to create an export

**Web console**

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Export**.
2. On the **One-time exports** tab, click  **Create export**.
3. Select the start and end months for your export and click **Create export**.

When the export is ready, the download will start automatically.

> [!NOTE]
>
> Export files remain available on the **One-time exports** tab for seven days after their creation.

**Nebius AI Cloud CLI**

Run the following command:

```bash theme={null}
nebius billing v1alpha1 one-time-export create \
  --parent-id contract-e00*** \
  --start-period <yyyy-mm> \
  --end-period <yyyy-mm> \
  --format export_format_focus_1_2_csv
```

In the command, specify the following parameters:

* `--parent-id`: Contract ID. To get it:

  1. Go to the [web console](https://console.nebius.com/).
  2. In the sidebar, go to  **Billing** → **Payments**.
  3. Switch to the **Billing details** tab and copy the contract ID in the **Payer** section.

* `--start-period`: Export start date in the `yyyy-mm` format.

* `--end-period`: Export end date in the `yyyy-mm` format.

* `--format`: Export format. Only `export_format_focus_1_2_csv` is supported.

The link to download the archive with the export is specified in the `.status.download_url` parameter of the output:

```yaml theme={null}
metadata:
  ...
spec:
  ...
status:
  ...
  download_url: 'https://storage.eu-north1.nebius.cloud/billing-report-exports-external/onetimeexport/...'
  ...
```

> [!NOTE]
>
> All export download links expire after 15 minutes, but the export files themselves remain available for seven days.

**Go SDK**

Create an export:

```go theme={null}
createExportService := sdk.Services().Billing().V1Alpha1().
    OneTimeExport()
exportOperation, err := createExportService.Create(
    ctx,
    &billing.CreateOneTimeExportRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "contract-e00***",
        },
        Spec: &billing.OneTimeExportSpec{
            StartPeriod: "<yyyy-mm>",
            EndPeriod: "<yyyy-mm>",
            Format:
                billing.ExportFormat_EXPORT_FORMAT_FOCUS_1_2_CSV,
        },
    },
)
if err != nil {
    return fmt.Errorf("create export: %w", err)
}
exportOperation, err = exportOperation.Wait(ctx)
if err != nil {
    return fmt.Errorf("wait for export creation: %w", err)
}
fmt.Println(exportOperation.ResourceID())
```

In the code, set the following parameters:

* `Metadata.ParentId`: Contract ID. To get it:

  1. Go to the [web console](https://console.nebius.com/).
  2. In the sidebar, go to  **Billing** → **Payments**.
  3. Switch to the **Billing details** tab and copy the contract ID from the **Payer** section.

* `Spec.StartPeriod`: Export start date in the `yyyy-mm` format.

* `Spec.EndPeriod`: Export end date in the `yyyy-mm` format.

* `Spec.Format`: Export format. Only `billing.ExportFormat_EXPORT_FORMAT_FOCUS_1_2_CSV` is supported.

The code prints the ID of the created export.

**Python SDK**

Create an export:

```python theme={null}
create_export_service = OneTimeExportServiceClient(sdk)
export_operation = await create_export_service.create(
    CreateOneTimeExportRequest(
        metadata=ResourceMetadata(
            parent_id="contract-e00***",
        ),
        spec=OneTimeExportSpec(
            start_period="<yyyy-mm>",
            end_period="<yyyy-mm>",
            format=ExportFormat.EXPORT_FORMAT_FOCUS_1_2_CSV,
        ),
    ),
)
await export_operation.wait()
print(export_operation.resource_id)
```

In the code, set the following parameters:

* `metadata.parent_id`: Contract ID. To get it:

  1. Go to the [web console](https://console.nebius.com/).
  2. In the sidebar, go to  **Billing** → **Payments**.
  3. Switch to the **Billing details** tab and copy the contract ID from the **Payer** section.

* `spec.start_period`: Export start date in the `yyyy-mm` format.

* `spec.end_period`: Export end date in the `yyyy-mm` format.

* `spec.format`: Export format. Only `ExportFormat.EXPORT_FORMAT_FOCUS_1_2_CSV` is supported.

The code prints the ID of the created export.

**JavaScript SDK**

Create an export:

```ts theme={null}
const createExportService = new OneTimeExportService(sdk);
const exportOperation = await createExportService.create(
  CreateOneTimeExportRequest.create({
    metadata: { parentId: "contract-e00***" },
    spec: {
      startPeriod: "<yyyy-mm>",
      endPeriod: "<yyyy-mm>",
      format: ExportFormat.EXPORT_FORMAT_FOCUS_1_2_CSV,
    },
  }),
).result;
await exportOperation.wait();
console.log(exportOperation.resourceId());
```

In the code, set the following parameters:

* `metadata.parentId`: Contract ID. To get it:

  1. Go to the [web console](https://console.nebius.com/).
  2. In the sidebar, go to  **Billing** → **Payments**.
  3. Switch to the **Billing details** tab and copy the contract ID from the **Payer** section.

* `spec.startPeriod`: Export start date in the `yyyy-mm` format.

* `spec.endPeriod`: Export end date in the `yyyy-mm` format.

* `spec.format`: Export format. Only `ExportFormat.EXPORT_FORMAT_FOCUS_1_2_CSV` is supported.

The code prints the ID of the created export.

### How to get export details

**Web console**

To find a previously created export:

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Export**.
2. Find the required export on the **One-time exports** tab.

**Nebius AI Cloud CLI**

To get details of a previously created export, run the following command:

```bash theme={null}
nebius billing v1alpha1 one-time-export get \
  --id billingonetimeexport-e00***
```

If you don't know the ID of the export, you can list all one-time exports created for a specific contract:

```bash theme={null}
nebius billing v1alpha1 one-time-export list \
  --parent-id contract-e00***
```

**Go SDK**

Get the export:

```go theme={null}
getExportService := sdk.Services().Billing().V1Alpha1().
    OneTimeExport()
export, err := getExportService.Get(
    ctx,
    &billing.GetOneTimeExportRequest{
        Id: "billingonetimeexport-e00***",
    },
)
if err != nil {
    return fmt.Errorf("get export: %w", err)
}
fmt.Println(export)
```

In the code, set `Id` to the export ID.

If you don't know the ID of the export, you can list all one-time exports created for a specific contract:

```go theme={null}
listExportsService := sdk.Services().Billing().V1Alpha1().
    OneTimeExport()
exports, err := listExportsService.List(
    ctx,
    &billing.ListOneTimeExportsRequest{
        ParentId: "contract-e00***",
    },
)
if err != nil {
    return fmt.Errorf("list exports: %w", err)
}
fmt.Println(exports)
```

In the code, set `ParentId` to the contract ID.

**Python SDK**

Get the export:

```python theme={null}
get_export_service = OneTimeExportServiceClient(sdk)
export = await get_export_service.get(
    GetOneTimeExportRequest(id="billingonetimeexport-e00***"),
)
print(export)
```

In the code, set `id` to the export ID.

If you don't know the ID of the export, you can list all one-time exports created for a specific contract:

```python theme={null}
list_exports_service = OneTimeExportServiceClient(sdk)
exports = await list_exports_service.list(
    ListOneTimeExportsRequest(
        parent_id="contract-e00***",
    ),
)
print(exports)
```

In the code, set `parent_id` to the contract ID.

**JavaScript SDK**

Get the export:

```ts theme={null}
const getExportService = new OneTimeExportService(sdk);
const billingExport = await getExportService.get(
  GetOneTimeExportRequest.create({ id: "billingonetimeexport-e00***" }),
).result;
console.log(billingExport);
```

In the code, set `id` to the export ID.

If you don't know the ID of the export, you can list all one-time exports created for a specific contract:

```ts theme={null}
const listExportsService = new OneTimeExportService(sdk);
const exports = await listExportsService.list(
  ListOneTimeExportsRequest.create({
    parentId: "contract-e00***",
  }),
).result;
console.log(exports);
```

In the code, set `parentId` to the contract ID.

## Periodic export

### Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

### How to create an export

To set up a periodic export of your usage data, do the following:

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Export**.

2. Switch to the **Periodic export** tab and click **Create export**.

   If you already have a periodic report configured, you need to [delete](#how-to-delete-an-export) it before you can create a new one.

3. In the window that opens, configure your export:

   1. Choose a month when the export should start.

   2. Choose a project and an Object Storage bucket to store usage data.

      You can choose an existing bucket or create a new one. New buckets use the **Standard** [storage class](https://docs.nebius.com/object-storage/storage-classes.md) by default.

   3. (Optional) Specify a bucket prefix: folder path within the bucket (for example, `/billing/export`).

4. Click **Create export**.

### How to view the export state

After you create the export, the **Periodic export** tab displays its configuration and state. You can view the following information:

* **Name and ID**: The export name and unique identifier.
* **Created**: The date and time when the export was created.
* **Last successful run**: The date and time of the most recent export run.
* **Status**: The current export status. For a **Failed** status, hover over the status to find out the reason for failure.
* **Destination bucket**: The link to the bucket where exported data is delivered.

### How to access the export files

To access files in an Object Storage bucket that stores the usage data, you must have at least the `storage.viewer` [role](https://docs.nebius.com/iam/authorization/roles.md#object-storage) at the level of the bucket, its parent project or tenant. By default, all users in the `viewers`, `editors` and `admins` [default groups](https://docs.nebius.com/iam/authorization/groups/index.md) in the tenant can access files in the bucket. You can also [set up a custom group](https://docs.nebius.com/iam/authorization/groups/manage.md) to restrict access to the bucket.

To download the export files:

**Web console**

1. On the **Periodic export** tab, open the **Destination bucket** link.
2. Next to the export file that you want to download, click  → **Download**.

**AWS CLI**

1. [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [configure it](https://docs.nebius.com/object-storage/interfaces/aws-cli.md) to work with your buckets in Nebius AI Cloud.
2. On the **Periodic export** tab, open the **Destination bucket** link.
3. Copy the bucket name and prefix from the bucket page.
4. Use them in the commands for [downloading the bucket objects](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-download).

### How to delete an export

You can delete the export to stop periodic data exports:

1. In the [web console](https://console.nebius.com/), go to  **Billing** → **Export**.
2. Switch to the **Periodic export** tab.
3. Next to the export, click  → **Delete export**.

Deleting the export does not remove existing export files from Object Storage. If you no longer need the exported files, [delete the corresponding bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) or [objects](https://docs.nebius.com/object-storage/objects/manage.md#how-to-delete-objects) separately.

## How to interpret the export results

The CSV with usage data follows the [FOCUS Column Library](https://focus.finops.org/focus-columns/) and adds Nebius AI Cloud-specific metadata columns. These columns include your [resource hierarchy](https://docs.nebius.com/iam/overview.md#resource-hierarchy) (for example, projects), the trial ID associated with a charge, and the contract price ID associated with a charge. For more information about the exported fields, see [FOCUS fields](https://docs.nebius.com/signup-billing/usage/focus-fields.md).

Exports always use the latest container name. If a container is deleted, we keep its last known name. If a container is renamed, the new name appears even in exports for earlier months.

If you use [commitment discounts](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md), `CommitmentDiscountStatus = Unused` shows the portion of the commitment that was prepaid but not consumed. You can also view the effective price for each VM by hour.

If your preemptible VM usage is charged with [spot pricing](https://docs.nebius.com/signup-billing/pricing-policy.md), the export can help you review the effective price over time.

If your bill for a month includes an adjustment, it appears as a separate line item in the CSV.
