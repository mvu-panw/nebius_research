# How to manage Object Storage buckets

Source: https://docs.nebius.com/object-storage/buckets/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage Object Storage buckets

In Object Storage, files are stored in containers called *buckets*. You can create, modify, delete or restore them.

## Prerequisites

> [!NOTE]
>
> Below are prerequisites for the AWS CLI and Nebius AI Cloud CLI. Other interfaces do not have any prerequisites.

To manage buckets, install and configure at least one of the command line interfaces (CLIs) supported by Nebius AI Cloud:

* **AWS CLI** offers simple commands for bucket management, such as `aws s3 mb` to create buckets and `aws s3 rb` to delete them. For more advanced management, use `aws s3api` commands.
* **Nebius AI Cloud CLI** supports all Object Storage features, as well as other Nebius AI Cloud resources, such as virtual machines and Managed Service for Kubernetes® clusters.

For the commands in this guide to work, configure the CLIs to work with Nebius AI Cloud. For example, in Nebius AI Cloud CLI commands (`nebius`), the ID of the parent project (`--parent-id`) is not included because it is expected to be set in the CLI profile:

```sh theme={null}
nebius config set parent-id <project_ID>
```

You can also provide the project ID explicitly to creation commands, for example, `nebius storage bucket create --parent-id <project_ID> ...`

For more information on installation and configuration, see the following guides:

* [How to get started with Object Storage: Create your first bucket](https://docs.nebius.com/object-storage/quickstart.md)
* [How to install Nebius AI Cloud CLI](https://docs.nebius.com/cli/install.md)
* [Working with Object Storage buckets and objects using the AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md)

## How to create buckets

For visual guidance on creating a bucket and uploading objects in the web console, watch the video below. If you prefer other interfaces or written instructions, follow the steps further down.

[YouTube video player](https://www.youtube.com/embed/Cx7BlL6PdKk)

Visit [Nebius Academy](https://academy.nebius.com/trainer/nebius-ai-cloud-onboarding/lesson/b532ba82-1b87-4d8c-ae82-f99afa32d04d) for video tutorials to help you get started with Nebius AI Cloud.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.

2. Click **Create resource** → **Bucket**.

3. (Optional) Specify the bucket name.

   The bucket name must be unique across the region. For more information, see [Naming](https://docs.nebius.com/object-storage/overview.md#naming).

4. Set the [bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters).

5. Click **Create bucket**.

**Nebius AI Cloud CLI**

To create a bucket, run the following command:

```bash theme={null}
nebius storage bucket create --name <bucket_name>
```

You can extend this command with more parameters, see [Bucket parameters](#bucket-parameters) and [Examples](#examples).

The bucket name must be unique across the region. For more information, see [Naming](https://docs.nebius.com/object-storage/overview.md#naming).

**AWS CLI**

```bash theme={null}
aws s3 mb s3://<bucket_name>
```

The `mb` in the command stands for "make bucket."

The bucket name must be unique across the region. For more information, see [Naming](https://docs.nebius.com/object-storage/overview.md#naming).

## How to modify buckets

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the page of the required bucket.
3. Go to the **Settings** tab.
4. Modify the [bucket parameters](#bucket-parameters).
5. Click **Save changes**.

**Nebius AI Cloud CLI**

To modify a bucket and change its [parameters](#bucket-parameters), run the following command:

```bash theme={null}
nebius storage bucket update --id $BUCKET_ID --max-size-bytes 268435456000
```

The bucket is patched by default. Only the parameters specified in the CLI command are changed. To perform a full update, add `--full` to the command. This will update all parameters with the values specified in the command or the default values.

## Bucket parameters

When creating or modifying a bucket, you can set the following parameters for it:

**Web console**

* **Bucket size**: Specify the bucket's maximum size or select **Unlimited** to have an unlimited capacity.
* **Storage class**: Select **Standard** for low-cost unlimited capacity or **Enhanced Throughput** for storage that requires high bandwidth and low latency access. For more information, see [Storage classes in Object Storage](https://docs.nebius.com/object-storage/storage-classes.md).
* **Force storage class**: Overrides the storage class specified explicitly when you upload an object to this bucket.
* **Versioning**: Allows you to track and record all object changes. For more information, see [Managing bucket versioning](https://docs.nebius.com/object-storage/buckets/versioning.md).
* **Data plane Audit Logs**: Configures data plane [logging](https://docs.nebius.com/object-storage/logs.md) for the bucket, in addition to always-on control plane logging. To manage this setting, you need the `admin` [role](https://docs.nebius.com/iam/authorization/roles.md) for the bucket, its parent project or tenant.

**Nebius AI Cloud CLI**

* `--versioning-policy enabled`: Allows versioning of objects in the bucket. For more details, see [Managing bucket versioning](https://docs.nebius.com/object-storage/buckets/versioning.md).

* `--max-size-bytes 107374182400`: Limits the total size of objects in the bucket.

* `--default-storage-class`: Sets the default [storage class](https://docs.nebius.com/object-storage/storage-classes.md) for the objects uploaded to the bucket.

* `--force-storage-class`: Makes the default storage class override storage classes that you specify explicitly when uploading objects to the bucket.

* `--lifecycle-configuration-rules '[{...}, {...}]'`: Adds object lifecycle rules to the bucket. For more information, see an [example below](#examples) and [Lifecycle rules for objects in Object Storage](https://docs.nebius.com/object-storage/objects/lifecycles.md).

* `--object-audit-logging <all|mutate_only|none>`: Configures data plane [logging](https://docs.nebius.com/object-storage/logs.md) for the bucket, in addition to always-on control plane logging. To manage this setting, you need the `admin` [role](https://docs.nebius.com/iam/authorization/roles.md) for the bucket, its parent project or tenant.

> [!NOTE]
>
> After you enable versioning for an *existing* bucket for the first time, it may take up to 15 minutes to come into effect. We recommend waiting 15 minutes before performing any write operations (`PUT` or `DELETE`) to avoid issues with object visibility and version tracking. If you enable or suspend versioning when *creating* a bucket, it is available immediately with no waiting period.

## How to delete buckets

### Delete an empty bucket

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Find the bucket and then click  → **Delete**.
3. Confirm the bucket deletion.

**Nebius AI Cloud CLI**

To delete an empty bucket, run the following command:

```bash theme={null}
export BUCKET_ID=$(nebius storage bucket get-by-name \
  --name <bucket_name> --format jsonpath='{.metadata.id}')
nebius storage bucket delete --id $BUCKET_ID
```

The command uses [jq](https://jqlang.github.io/jq/download/) to extract the bucket ID from the JSON output and pass it along.

> [!WARNING]
>
> If the bucket has versioning enabled, it may appear empty but still contain old versions of some objects. Make sure that you delete all versions of all objects in the bucket before you run this command. For more details, see [Managing objects in Object Storage buckets](https://docs.nebius.com/object-storage/objects/manage.md).

**AWS CLI**

To delete an empty bucket, run the following command:

```bash theme={null}
aws s3 rb s3://bucket-name
```

The `rb` in the command stands for "remove bucket."

> [!WARNING]
>
> If the bucket has versioning enabled, it may appear empty but still contain old versions of some objects. Make sure that you delete all versions of all objects in the bucket before you run this command. For more details, see [Managing objects in Object Storage buckets](https://docs.nebius.com/object-storage/objects/manage.md).

### Delete a non-empty bucket after a delay

In the web console, you can delete a non-empty bucket immediately or after a delay. If you use other interfaces, you can delete a non-empty bucket only after a delay.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.

2. Locate the bucket and then click  → **Delete**.

3. In the window that opens, select whether you want to delete the bucket now or later:

   * If you delete the bucket now, you cannot restore its objects after that.
   * If you want to delete the bucket later, this allows you to [restore the bucket](#how-to-restore-buckets) before the time elapses. When it elapses, the service deletes the bucket.

4. For the **Delete later** option, specify for how long Object Storage should postpone the bucket deletion.

5. Confirm the deletion.

If you selected the **Delete later** option, the bucket status changes to **To be deleted**. When the bucket is in this status, you cannot use or update it. The bucket is not visible in the AWS CLI.

> [!NOTE]
>
> Nebius AI Cloud still [charges](https://docs.nebius.com/object-storage/resources/pricing.md) you for the bucket in the **To be deleted** status.

**Nebius AI Cloud CLI**

1. Get the bucket ID:

   ```bash theme={null}
   export BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <bucket_name> --format jsonpath='{.metadata.id}')
   ```

   The command uses [jq](https://jqlang.github.io/jq/download/) to extract the bucket ID from the JSON output and pass it to the next commands.

2. Run one of the following commands:

   ```bash theme={null}
   nebius storage bucket delete --id $BUCKET_ID --ttl <delay_time>
   ```

   ```bash theme={null}
   nebius storage bucket delete --id $BUCKET_ID --purge-at <timestamp>
   ```

   * `--purge-at` specifies the timestamp when the bucket and all objects in it are deleted. For example: `'2025-01-01T18:33:31.827636Z'`.
   * `--ttl` specifies the delay after which the bucket and all objects in it are deleted. For example: `1h20m30s`. Specify `0s` to delete the bucket immediately.

The bucket is put into the `SCHEDULED_FOR_DELETION` status, and after the specified time passes, it is deleted. When the bucket is in this status, you cannot use or update it, but you can [restore it](#how-to-restore-buckets). The bucket is not visible in the AWS CLI.

> [!NOTE]
>
> Nebius AI Cloud still [charges](https://docs.nebius.com/object-storage/resources/pricing.md) you for the bucket in the `SCHEDULED_FOR_DELETION` status.

### Immediately delete a bucket scheduled for deletion

If you scheduled a bucket for deletion and you want to skip this schedule and delete the bucket immediately, do the following:

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Object Storage**.
2. Locate the bucket and then click  → **Delete now**.
3. Confirm the bucket deletion.

**Nebius AI Cloud CLI**

Run the following command:

```bash theme={null}
nebius storage bucket purge --id $BUCKET_ID
```

## How to restore buckets

If you scheduled a bucket for deletion and you want to restore it, do the following:

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Locate the bucket and then click **Restore**.
3. Confirm the bucket restoration.

**Nebius AI Cloud CLI**

Run the following command:

```bash theme={null}
nebius storage bucket undelete --id $BUCKET_ID
```

## Examples

**Nebius AI Cloud CLI**

* Creating a bucket with total objects size limited to 250 GiB (268,435,456,000 bytes):

  ```bash theme={null}
  nebius storage bucket create --name <bucket_name> \
    --max-size-bytes 268435456000
  ```

* Creating a bucket with an object lifecycle rule that deletes objects 90 days after their creation:

  ```bash theme={null}
  nebius storage bucket create --name <bucket_name> \
    --lifecycle-configuration-rules '[{
      "id": "lifecycle-delete-90-days-objects",
      "status": "ENABLED",
      "filter": {
        "prefix": ""
      },
      "expiration": {
        "days": 90
      }
    }]'
  ```

* Creating a bucket with a forced Standard default storage class that overrides the storage class that you select explicitly for any individual object uploaded to the bucket:

  ```bash theme={null}
  nebius storage bucket create --name <bucket_name> \
    --default-storage-class standard \
    --force-storage-class
  ```
