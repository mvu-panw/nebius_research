# How to manage filesystem buckets

Source: https://docs.nebius.com/object-storage/buckets/filesystem-buckets

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage filesystem buckets

A *filesystem bucket* adds the Object Storage interface to an existing shared filesystem. You can attach a bucket to a [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to read or write data by using an S3-compatible API, or copy data from S3-compatible storage to the filesystem by using a data transfer or S3-compatible tools, such as [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md) or [s5cmd](https://github.com/peak/s5cmd).

Files from the filesystem are immediately visible as S3 objects when a filesystem bucket is attached. Objects in the filesystem bucket are also stored in the filesystem as files.

> [!WARNING]
>
> Filesystem buckets are excluded from the [Object Storage service level policy](https://docs.nebius.com/legal/sla-levels/storage.md) and are not covered by the Object Storage SLA.

Filesystem buckets in Object Storage are [in preview](https://docs.nebius.com/overview/services.md#service-and-application-stages).

Filesystem buckets count toward your bucket quota in Object Storage. For more information, see [Quotas and limits in Object Storage](https://docs.nebius.com/object-storage/resources/quotas-limits.md).

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console. Alternatively, the [compute.use-via-object-storage role](https://docs.nebius.com/iam/authorization/roles.md#compute) gives access to shared filesystems through Object Storage.
2. If you don't have a shared filesystem yet, [create one](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-shared-filesystem).

**Nebius AI Cloud CLI**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console. Alternatively, the [compute.use-via-object-storage role](https://docs.nebius.com/iam/authorization/roles.md#compute) gives access to shared filesystems through Object Storage.
2. If you don't have a shared filesystem yet, [create one](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-shared-filesystem).
3. [Install and configure the Nebius AI Cloud CLI](https://docs.nebius.com/cli/quickstart.md).

## How to create a filesystem bucket

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Click **Create resource** → **Filesystem bucket**.
3. Specify the filesystem bucket parameters:

   * **Filesystem**: From the list, select the shared filesystem that you want to attach the bucket to.
   * **Bucket name**: Specify the name of the filesystem bucket. By default, the web console generates a name automatically, and you can keep it or replace it with your own name. The name must be unique across the region. For more information, see [Naming](https://docs.nebius.com/object-storage/overview.md#naming).
   * (Optional) **Directory path**: Specify the directory inside the filesystem that should back this filesystem bucket. Only files in this directory are accessible via the S3 endpoint. If you leave the field empty or specify `/`, the filesystem bucket is attached at the filesystem root. If you specify a directory that doesn't exist yet, it will be created.
   * (Optional) **Data plane audit logs**: Enable this option if you want to [log](https://docs.nebius.com/object-storage/logs.md) data plane operations for the filesystem bucket.
4. (Optional) Configure **Advanced settings**.

   Files and folders in the attached filesystem will have POSIX ownership and permission attributes according to the values set in the following settings. The configured attributes do not affect how the bucket reads files and folders from the attached filesystem.

   * **Write UID**: User ID assigned to files and directories. The default value is `0`.
   * **Write GID**: Group ID assigned to files and directories. The default value is `0`.
   * **File permissions**: Permissions assigned to files. Specify the permissions as a four-digit octal value. The default value is `0644` (`rw-r--r--`), which means that the owner can read and write the file, and the group and others can only read it.
   * **Folder permissions**: Permissions assigned to folders. Specify the permissions as a four-digit octal value. To enable the sticky bit, use `1` as the first digit, for example, `1777`. On a folder, the sticky bit restricts deletion and renaming of its contents to the content owner, folder owner and `root`. The default value is `0755` (`rwxr-xr-x`), which means that the owner can read, write and access the directory, and the group and others can only read and access it.
5. Click **Create bucket**.

The filesystem bucket becomes available immediately after creation. You can find it in one of the following ways:

* Go to  **Storage** → **Shared filesystems**, open the shared filesystem and then switch to the **Attached buckets** tab.
* Go to  **Storage** → **Object Storage** and then open the **Filesystem buckets** tab.

**Nebius AI Cloud CLI**

1. Get the ID of the filesystem you want to attach a bucket to:

   ```bash theme={null}
   nebius compute filesystem list --parent-id <project_ID>
   ```

   In the `--parent-id` parameter, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3).

2. Create a filesystem bucket:

   ```bash theme={null}
   nebius storage bucket create \
     --parent-id <project_ID> \
     --name <bucket_name> \
     --filesystem-bucket-filesystem-id <filesystem_ID> \
     --filesystem-bucket-directory <directory_path> \
     --filesystem-bucket-gid <GID> \
     --filesystem-bucket-uid <UID> \
     --filesystem-bucket-file-mode <file_mode> \
     --filesystem-bucket-directory-mode <directory_mode> \
     --object-audit-logging <all|mutate_only|none>
   ```

   The command contains the following parameters:

   * `--parent-id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3) of the project where you create the filesystem bucket.
   * `--name`: Name of the filesystem bucket. The name must be unique across the region. For more information, see [Naming](https://docs.nebius.com/object-storage/overview.md#naming).
   * `--filesystem-bucket-filesystem-id`: ID of the shared filesystem that you want to attach to the filesystem bucket.
   * `--filesystem-bucket-directory` (optional): Directory inside the shared filesystem that serves as the filesystem bucket root. The path must be absolute and normalized, without `.`, `..` or repeated `/` characters. If omitted or empty, the filesystem root (`/`) is used.
   * `--filesystem-bucket-gid` (optional): Group ID assigned to files and directories written through S3. The default value is `0`.
   * `--filesystem-bucket-uid` (optional): User ID assigned to files and directories written through S3. The default value is `0`.
   * `--filesystem-bucket-file-mode` (optional): POSIX permissions assigned to files uploaded through S3. Specify the permissions as a four-digit octal value. The default value is `0644` (`rw-r--r--`), which means that the owner can read and write the file, and the group and others can only read it.
   * `--filesystem-bucket-directory-mode` (optional): POSIX permissions assigned to directories created through S3 operations. Specify the permissions as a four-digit octal value. To enable the sticky bit, use `1` as the first digit, for example, `1777`. On a directory, the sticky bit restricts deletion and renaming of its contents to the content owner, directory owner and `root`. The default value is `0755` (`rwxr-xr-x`), which means that the owner can read, write and access the directory, and the group and others can only read and access it.
   * `--object-audit-logging` (optional): Configures data plane [logging](https://docs.nebius.com/object-storage/logs.md#how-to-configure-data-plane-logs) for the filesystem bucket.

   In both interfaces, specify permissions as four-digit octal values. The defaults are `0644` for files and `0755` for directories.

3. Verify that the filesystem bucket was created:

   ```bash theme={null}
   nebius storage bucket get-by-name \
     --parent-id <project_ID> \
     --name <bucket_name>
   ```

The command output includes the ID of the filesystem bucket in `metadata.id`.

## How to use a filesystem bucket

After you create a filesystem bucket, you can use it to access data stored in the filesystem. The data uploaded to the filesystem bucket is also stored in the filesystem. You can [upload and download objects](https://docs.nebius.com/object-storage/objects/upload-download.md) as well as [manage objects](https://docs.nebius.com/object-storage/objects/manage.md) as you do in regular Object Storage buckets that are not attached to a filesystem.

### Data transfers

You can transfer data from S3-compatible storage to the attached filesystem in one of the following ways:

* Create a [data transfer](https://docs.nebius.com/object-storage/transfer/overview.md) from the S3-compatible storage to the filesystem bucket.
* Use an S3-compatible tool, such as [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md), [rclone](https://rclone.org/docs/) or [s5cmd](https://github.com/peak/s5cmd), to upload objects to the filesystem bucket.

## How to update a filesystem bucket

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.

2. Open the **Filesystem buckets** tab and select the filesystem bucket.

3. Go to the **Settings** tab.

4. Update the settings:

   * **Data plane audit logs**: Enable or disable logging. If logging is enabled, select **Log all events** or **Log only changes in objects**. For details, see [Logged data plane actions](https://docs.nebius.com/object-storage/logs.md#logged-data-plane-actions).
   * **Advanced settings**: Change the **Write UID**, **Write GID**, **File permissions** or **Folder permissions** values assigned to files that are uploaded to the filesystem bucket. For file and folder permissions, specify a four-digit octal value. To enable the sticky bit for folders, use `1` as the first digit, for example, `1777`.

5. Click **Save changes**.

**Nebius AI Cloud CLI**

To update data plane audit logging, POSIX ownership or permissions, run:

```bash theme={null}
nebius storage bucket update \
  --id <filesystem_bucket_ID> \
  --filesystem-bucket-gid <GID> \
  --filesystem-bucket-uid <UID> \
  --filesystem-bucket-file-mode <file_mode> \
  --filesystem-bucket-directory-mode <directory_mode> \
  --object-audit-logging <all|mutate_only|none>
```

In the command, specify the parameters that you want to update:

* `--filesystem-bucket-gid`: Group ID assigned to files and directories written through S3.
* `--filesystem-bucket-uid`: User ID assigned to files and directories written through S3.
* `--filesystem-bucket-file-mode`: POSIX permissions assigned to files uploaded through S3. Specify the permissions as a four-digit octal value.
* `--filesystem-bucket-directory-mode`: POSIX permissions assigned to directories created through S3 operations. Specify the permissions as a four-digit octal value. To enable the sticky bit, use `1` as the first digit, for example, `1777`.
* `--object-audit-logging`: Data plane logging mode. Specify `all` to log all data plane events, `mutate_only` to log only events that change objects or `none` to disable logging.

## How to delete a filesystem bucket

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Open the **Filesystem buckets** tab.
3. Find the filesystem bucket and then click  → **Delete**.
4. Confirm the deletion.

**Nebius AI Cloud CLI**

1. Get the ID of the filesystem bucket:

   ```bash theme={null}
   nebius storage bucket list --parent-id <project_ID>
   ```

   In the `--parent-id` parameter, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3).

   In the output, filesystem buckets include the `spec.filesystem_bucket` field. Find the filesystem bucket by its name. The filesystem bucket ID is shown in `metadata.id`.

2. Delete the filesystem bucket:

   ```bash theme={null}
   nebius storage bucket delete --id <filesystem_bucket_ID>
   ```

3. Wait until the delete operation is complete.

Deleting a filesystem bucket removes only the Object Storage bucket interface. It does not delete the data stored on the attached filesystem.

## Limitations

Filesystem buckets have the following limitations:

* Temporary files with the `.tmp` suffix can be visible in `ListObjectsV2` results. Filesystem buckets use these files for atomic writes and clean them up on a best-effort basis.

* Bucket management has the following limitations:

  * After you create a bucket, you cannot change its type from regular to filesystem or from filesystem to regular.
  * [Bucket policies](https://docs.nebius.com/object-storage/buckets/bucket-policy.md) cannot be used to grant [anonymous access](https://docs.nebius.com/object-storage/buckets/bucket-policy.md#anonymous-access) to a filesystem bucket.
  * Delayed deletion and [bucket restoration](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-restore-buckets) are not supported.

* Object integrity checksums are not supported. For integrity checks in regular buckets, see [How to verify object integrity](https://docs.nebius.com/object-storage/objects/manage.md#how-to-verify-object-integrity).

* Object keys such as `a/b` and `a/b/c` cannot both exist as files, because `b` must be either a file or a directory on a filesystem. This can cause conflicts when migrating data from S3-compatible storage to a filesystem bucket.

* Some [S3 API methods and parameters](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md#supported-s3-api-methods) and [S3-compatible headers](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md#supported-s3-headers) have limited support or are not supported.
