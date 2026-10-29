# How to configure and manage a bucket inventory in Object Storage

Source: https://docs.nebius.com/object-storage/buckets/configure-inventory

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to configure and manage a bucket inventory in Object Storage

Create a [bucket inventory](https://docs.nebius.com/object-storage/buckets/inventory.md) configuration to get scheduled reports on the contents of a bucket. You can create up to five configurations for the same bucket and temporarily disable report generation without deleting the configuration when needed.

## Prerequisites

**Web console**

* To create, modify or delete inventory configurations, make sure that you have at least the `storage.editor` [role](https://docs.nebius.com/iam/authorization/roles.md) for the bucket, its parent project or tenant.
* To use another bucket as the destination for reports, make sure that you have at least the `storage.uploader` role for the destination bucket, its parent project or tenant.
* To view inventory configurations, make sure that you have at least the `storage.viewer` role for the bucket, its parent project or tenant.

**Nebius AI Cloud CLI**

* [Install](https://docs.nebius.com/cli/install.md) and [configure](https://docs.nebius.com/cli/configure.md) the Nebius AI Cloud CLI.
* To create, modify or delete inventory configurations, make sure that you have at least the `storage.editor` [role](https://docs.nebius.com/iam/authorization/roles.md) for the bucket, its parent project or tenant.
* To use another bucket as the destination for reports, make sure that you have at least the `storage.uploader` role for the destination bucket, its parent project or tenant.
* To view inventory configurations, make sure that you have at least the `storage.viewer` role for the bucket, its parent project or tenant.

**Terraform**

* [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
* To create, modify or delete inventory configurations, make sure that you have at least the `storage.editor` [role](https://docs.nebius.com/iam/authorization/roles.md) for the bucket, its parent project or tenant.
* To use another bucket as the destination for reports, make sure that you have at least the `storage.uploader` role for the destination bucket, its parent project or tenant.
* To view inventory configurations, make sure that you have at least the `storage.viewer` role for the bucket, its parent project or tenant.

## How to create an inventory configuration

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.

2. Open the page of the bucket where you want to create an inventory configuration.

3. Click **Add** → **Inventory configuration**.

4. Set the inventory configuration parameters:

   * **Name**: Name of the configuration. Object Storage uses it both in the list of configurations and in the [keys of report objects](https://docs.nebius.com/object-storage/buckets/inventory.md#where-object-storage-delivers-reports).

   * (Optional) **Source prefix**: Prefix that filters source objects included in the report. The report only contains objects whose keys start with this prefix.

   * **Project**: Project that contains the bucket where Object Storage delivers the reports.

   * **Bucket**: Bucket where Object Storage delivers the reports. You can select the current bucket or a different one in the same [region](https://docs.nebius.com/overview/regions.md).

   * (Optional) **Destination prefix**: Prefix that Object Storage adds to the keys of report objects. For example, `test_dir/`. Use it to keep reports separate from other objects in the destination bucket.

   * **Schedule**: How often Object Storage generates a report — **Daily** or **Weekly**. For details, see [How Object Storage generates reports](https://docs.nebius.com/object-storage/buckets/inventory.md#how-object-storage-generates-reports).

   * **Output format**: Format and compression of report objects:

     * **CSV compressed with GZIP**
     * **Apache Parquet compressed with Snappy**

   * **Object versions**: Whether a report lists only the current version of every object (**Current version only**) or all its versions (**Include all versions**).

   * **Optional metadata fields to export**: Additional object metadata that Object Storage can include in a report. For more information, see [What a report contains](https://docs.nebius.com/object-storage/buckets/inventory.md#what-a-report-contains).

5. Click **Create**.

The configuration will appear on the **Inventory configuration** tab of the bucket and become active.

**Nebius AI Cloud CLI**

1. Get the ID of the bucket where you want to create an inventory configuration:

   ```bash theme={null}
   export SOURCE_BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <source_bucket_name> \
     --format jsonpath='{.metadata.id}')
   ```

2. Get the ID of the bucket where Object Storage will deliver reports:

   ```bash theme={null}
   export DESTINATION_BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <destination_bucket_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Create an inventory configuration:

   ```bash theme={null}
   nebius storage inventory create \
     --parent-id $SOURCE_BUCKET_ID \
     --name <configuration_name> \
     --destination-bucket-id $DESTINATION_BUCKET_ID \
     --destination-prefix <destination_prefix> \
     --source-prefix <source_prefix> \
     --schedule daily \
     --output-format csv_gzip \
     --enabled=true \
     --noncurrent-versions=true \
     --optional-fields "last_access,checksum_algorithms"
   ```

   The command contains the following parameters:

   * `--parent-id`: ID of the bucket where you create the inventory configuration.
   * `--destination-bucket-id`: ID of the bucket where Object Storage delivers reports. The bucket must be in the same [region](https://docs.nebius.com/overview/regions.md) as the source bucket.
   * `--destination-prefix` (optional): Prefix that Object Storage adds to the keys of report objects.
   * `--source-prefix` (optional): Prefix that filters source objects included in the report.
   * `--schedule`: How often Object Storage generates a report: `daily` or `weekly`.
   * `--output-format`: Format and compression of report objects: `csv_gzip` or `parquet_snappy`.
   * `--enabled`: Enables report generation for the inventory configuration. Set it to `true` when you create a configuration that should start generating reports.
   * `--noncurrent-versions` (optional): Includes noncurrent object versions in the report. Set it to `true` if you want the report to include all object versions. The bucket must have [versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) enabled.
   * `--optional-fields` (optional): Additional object metadata fields to include in the report. The example exports the last access time and checksum algorithms.

**Terraform**

1. Add an inventory configuration to your Terraform configuration:

   ```hcl theme={null}
   resource "nebius_storage_v1_inventory" "inventory" {
     parent_id             = "<source_bucket_ID>"
     name                  = "<configuration_name>"
     destination_bucket_id = "<destination_bucket_ID>"
     destination_prefix    = "<destination_prefix>"
     source_prefix         = "<source_prefix>"
     schedule              = "DAILY"
     output_format         = "CSV_GZIP"
     enabled               = true
     noncurrent_versions   = true
     optional_fields       = ["LAST_ACCESS", "CHECKSUM_ALGORITHMS"]
   }
   ```

   The configuration contains the following arguments:

   * `parent_id`: ID of the bucket where you create the inventory configuration.
   * `destination_bucket_id`: ID of the bucket where Object Storage delivers reports. The bucket must be in the same [region](https://docs.nebius.com/overview/regions.md) as the source bucket.
   * `destination_prefix` (optional): Prefix that Object Storage adds to the keys of report objects.
   * `source_prefix` (optional): Prefix that filters source objects included in the report.
   * `schedule`: How often Object Storage generates a report: `DAILY` or `WEEKLY`.
   * `output_format`: Format and compression of report objects: `CSV_GZIP` or `PARQUET_SNAPPY`.
   * `enabled`: Enables report generation for the inventory configuration. Set it to `true` when you create a configuration that should start generating reports.
   * `noncurrent_versions` (optional): Includes noncurrent object versions in the report. Set it to `true` if you want the report to include all object versions. The bucket must have [versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) enabled.
   * `optional_fields` (optional): Additional object metadata fields to include in the report. The example exports the last access time and checksum algorithms.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

> [!NOTE]
>
> To report on all object versions, [enable versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) in the bucket where you want to create an inventory configuration. Otherwise, the report will only list current versions.

## How to view inventory configurations

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the page of the bucket where you want to view inventory configurations.
3. Go to the **Inventory configuration** tab.
4. To see all parameters of a specific configuration, open its page.

**Nebius AI Cloud CLI**

1. Get the ID of the bucket whose inventory configurations you want to view:

   ```bash theme={null}
   export SOURCE_BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <source_bucket_name> \
     --format jsonpath='{.metadata.id}')
   ```

2. List inventory configurations:

   ```bash theme={null}
   nebius storage inventory list --parent-id $SOURCE_BUCKET_ID
   ```

3. To see all parameters of a specific configuration, get it by name:

   ```bash theme={null}
   nebius storage inventory get-by-name \
     --parent-id $SOURCE_BUCKET_ID \
     --name <configuration_name>
   ```

**Terraform**

With Terraform, you can retrieve a specific inventory configuration by name or ID. The following example shows how to retrieve it by name.

1. Add a data source for the inventory configuration:

   ```hcl theme={null}
   data "nebius_storage_v1_inventory" "inventory" {
     parent_id = "<source_bucket_ID>"
     name      = "<configuration_name>"
   }

   output "inventory_configuration" {
     value = data.nebius_storage_v1_inventory.inventory
   }
   ```

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

## How to get a report

Object Storage delivers reports as regular objects, so you work with them as with any other objects in a bucket. Reports are always compressed.

> [!NOTE]
>
> A complete report can consist of multiple objects. To get the complete report, download every object listed in the `files` array of the `manifest.json` file.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the page of the destination bucket that you set in the configuration.
3. Find the report objects you need. Object Storage stores them under the `<destination_prefix>/<bucket_name>/<configuration_name>/data/` prefix, where `<bucket_name>` is the bucket that you analyze. For more information, see [Where Object Storage delivers reports](https://docs.nebius.com/object-storage/buckets/inventory.md#where-object-storage-delivers-reports).
4. [Download](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-download) the report objects.

**AWS CLI**

1. Make sure that the [AWS CLI is configured](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) to work with Object Storage.
2. Download a report object:

   ```sh theme={null}
   aws s3 cp \
     s3://<destination_bucket_name>/<destination_prefix>/<bucket_name>/<configuration_name>/data/<inventory_file> \
     <local/destination/path/>
   ```

   Repeat this command for every object listed in the `files` array of the `manifest.json` file.

   For more information about downloading objects, see [Uploading and downloading objects in Object Storage](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-download).

> [!TIP]
>
> To make sure that the report is complete, compare each report object's checksum with the corresponding checksum in the `manifest.json` file.

## How to modify an inventory configuration

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the page of the bucket where you want to modify an inventory configuration.
3. Go to the **Inventory configuration** tab.
4. Next to the configuration that you want to modify, click  → **Edit**.
5. Change the inventory configuration parameters and click **Save changes**.

**Nebius AI Cloud CLI**

1. Get the ID of the bucket where the inventory configuration is created:

   ```bash theme={null}
   export SOURCE_BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <source_bucket_name> \
     --format jsonpath='{.metadata.id}')
   ```

2. Get the inventory configuration ID:

   ```bash theme={null}
   export INVENTORY_ID=$(nebius storage inventory get-by-name \
     --parent-id $SOURCE_BUCKET_ID \
     --name <configuration_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Update the inventory configuration:

   ```bash theme={null}
   nebius storage inventory update \
     --id $INVENTORY_ID \
     --destination-prefix <new_destination_prefix> \
     --schedule weekly \
     --output-format parquet_snappy
   ```

   In the command, add only the parameters that you want to change.

**Terraform**

1. In your Terraform configuration, change the arguments of the corresponding `nebius_storage_v1_inventory` resource. For example:

   ```hcl theme={null}
   resource "nebius_storage_v1_inventory" "inventory" {
     parent_id             = "<source_bucket_ID>"
     name                  = "<configuration_name>"
     destination_bucket_id = "<destination_bucket_ID>"
     destination_prefix    = "<new_destination_prefix>"
     source_prefix         = "<source_prefix>"
     schedule              = "WEEKLY"
     output_format         = "PARQUET_SNAPPY"
     enabled               = true
     noncurrent_versions   = true
     optional_fields       = ["LAST_ACCESS", "CHECKSUM_ALGORITHMS"]
   }
   ```

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

Your changes will apply to the reports generated after the configuration change. Reports delivered earlier remain unchanged.

## How to stop or resume an inventory configuration

Stop a configuration when you no longer need new reports but want to keep the configuration.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the page of the bucket where you want to stop or resume an inventory configuration.
3. Go to the **Inventory configuration** tab.
4. Next to the configuration you want to stop or resume, click  and then select one of the following:

   * **Stop**: Object Storage stops generating reports, and the configuration status changes to **Stopped**.
   * **Resume**: Object Storage resumes report generation according to the configuration schedule. It doesn't generate a report immediately.

**Nebius AI Cloud CLI**

1. Get the ID of the bucket where the inventory configuration is created:

   ```bash theme={null}
   export SOURCE_BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <source_bucket_name> \
     --format jsonpath='{.metadata.id}')
   ```

2. Get the inventory configuration ID:

   ```bash theme={null}
   export INVENTORY_ID=$(nebius storage inventory get-by-name \
     --parent-id $SOURCE_BUCKET_ID \
     --name <configuration_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Run one of the following commands:

   * To stop generating reports:

     ```bash theme={null}
     nebius storage inventory update \
       --id $INVENTORY_ID \
       --enabled=false
     ```

   * To resume generating reports:

     ```bash theme={null}
     nebius storage inventory update \
       --id $INVENTORY_ID \
       --enabled=true
     ```

**Terraform**

1. In the corresponding `nebius_storage_v1_inventory` resource, change the `enabled` argument:

   * To stop generating reports, set `enabled` to `false`:

     ```hcl theme={null}
     resource "nebius_storage_v1_inventory" "inventory" {
       parent_id             = "<source_bucket_ID>"
       name                  = "<configuration_name>"
       destination_bucket_id = "<destination_bucket_ID>"
       destination_prefix    = "<destination_prefix>"
       source_prefix         = "<source_prefix>"
       schedule              = "DAILY"
       output_format         = "CSV_GZIP"
       enabled               = false
       noncurrent_versions   = true
       optional_fields       = ["LAST_ACCESS", "CHECKSUM_ALGORITHMS"]
     }
     ```

   * To resume generating reports, set `enabled` to `true`:

     ```hcl theme={null}
     resource "nebius_storage_v1_inventory" "inventory" {
       parent_id             = "<source_bucket_ID>"
       name                  = "<configuration_name>"
       destination_bucket_id = "<destination_bucket_ID>"
       destination_prefix    = "<destination_prefix>"
       source_prefix         = "<source_prefix>"
       schedule              = "DAILY"
       output_format         = "CSV_GZIP"
       enabled               = true
       noncurrent_versions   = true
       optional_fields       = ["LAST_ACCESS", "CHECKSUM_ALGORITHMS"]
     }
     ```

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

## How to delete an inventory configuration

> [!WARNING]
>
> Deleting an inventory configuration is permanent. To keep a configuration but stop generating new reports, [stop it](#how-to-stop-or-resume-an-inventory-configuration) instead.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the page of the bucket where you want to delete an inventory configuration.
3. Go to the **Inventory configuration** tab.
4. Next to the configuration you want to delete, click  → **Delete**.
5. Enter the inventory configuration name and click **Delete inventory configuration**.

**Nebius AI Cloud CLI**

1. Get the ID of the bucket where the inventory configuration is created:

   ```bash theme={null}
   export SOURCE_BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <source_bucket_name> \
     --format jsonpath='{.metadata.id}')
   ```

2. Get the inventory configuration ID:

   ```bash theme={null}
   export INVENTORY_ID=$(nebius storage inventory get-by-name \
     --parent-id $SOURCE_BUCKET_ID \
     --name <configuration_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Delete the inventory configuration:

   ```bash theme={null}
   nebius storage inventory delete --id $INVENTORY_ID
   ```

**Terraform**

1. Remove the corresponding `nebius_storage_v1_inventory` resource from the Terraform configuration.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

Object Storage doesn't delete the reports that it has already delivered to the destination bucket. To remove them, [delete these objects](https://docs.nebius.com/object-storage/objects/manage.md#how-to-delete-objects) or [configure lifecycle rules](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md) for them.
