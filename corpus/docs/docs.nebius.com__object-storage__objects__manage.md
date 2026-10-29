# Managing objects in Object Storage buckets

Source: https://docs.nebius.com/object-storage/objects/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing objects in Object Storage buckets

In Object Storage, you work with files and folders called *objects* and place them in containers called buckets. This guide will help you manage objects in buckets.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**AWS CLI**

Install and configure the AWS CLI. It provides simple commands for object management, like `aws s3 cp` to move objects between a bucket and a local computer and `aws s3 rm` to delete them.

For more details on installing and configuring, see [How to get started with Object Storage: Create your first bucket](https://docs.nebius.com/object-storage/quickstart.md) and the guide on the [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md).

### Object naming requirements

Each Object Storage object has a *key*. This key can contain [prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) — they act similarly to folders, organizing objects into groups.

To avoid issues with your objects, follow these requirements:

* Object keys can be up to 1024 bytes long, case sensitive.
* Use UTF-8 alphanumeric characters, slashes (`/`) and certain [special characters](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-guidelines).

For more information on character usage and which characters to avoid, see the [AWS object naming guidelines](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-guidelines).

## How to view objects

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket to view the objects in. The page shows a table with the following columns: **Key**, **Size**, **Storage class** and **Last modified**.
3. To see the contents of a folder, click the folder name in the **Key** column.

**AWS CLI**

* To list all the prefixes and all the first-level objects in your Object Storage bucket:

  ```sh theme={null}
  aws s3 ls s3://<bucket_name>/[<prefix_for_object_keys>]
  ```

* To list all the objects with a specific prefix in your Object Storage bucket:

  ```sh theme={null}
  aws s3 ls s3://<bucket_name>/[<prefix_for_object_keys>] --recursive --human-readable --summarize
  ```

* To list all the objects arranged alphabetically by prefix in your Object Storage bucket:

  ```sh theme={null}
  aws s3 ls s3://<bucket_name>/ --recursive --human-readable --summarize
  ```

You can find more information on the `ls` command in the [AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/ls.html).

## How to share an object with a pre-signed URL

A *pre-signed URL* grants temporary access to an object without requiring the recipient to have Nebius AI Cloud credentials. The URL is signed with the credentials of the account that creates it, and anyone with the URL can download the object until the URL expires.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket that contains the object.
3. In the object's row, click  → **Get link**. The pre-signed URL is copied to the clipboard. The URL is valid for one hour.

**AWS CLI**

Pre-signed URLs must be created by accounts with [Object Storage roles](https://docs.nebius.com/object-storage/supported-actions.md) that support the `GetObject` action, because the URL uses the permissions of the creator.

To generate a pre-signed URL for downloading an object, use the `presign` command:

```sh theme={null}
aws s3 presign s3://<bucket_name>/<object_key>
```

By default, the URL is valid for 3600 seconds (1 hour). To set a different expiration time, add the `--expires-in` parameter with a value in seconds, up to 604800 seconds (7 days):

```sh theme={null}
aws s3 presign s3://<bucket_name>/<object_key> --expires-in <seconds>
```

The command uses the Object Storage [credentials](https://docs.nebius.com/object-storage/quickstart.md#configure-access-credentials-and-aws-cli-settings) from your AWS CLI configuration, so the resulting URL can be opened in a browser or passed to a tool like `curl` or `wget`.

For more information on the `presign` command, see [AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/presign.html).

## How to verify object integrity

> [!NOTE]
>
> The web console does not show checksum metadata. Use the AWS CLI to upload objects with a checksum and to retrieve the checksum of stored objects.

Object Storage supports end-to-end integrity checks for the objects you upload. When you upload an object, you can provide its checksum along with the upload request. Object Storage then calculates the checksum of the stored object and compares it with the one you provided. If the checksums match, both the object and its checksum are stored, and the checksum can be retrieved later through `HeadObject` or `GetObject` requests. If the checksums don't match, the upload fails with an error.

Both simple and multipart uploads support integrity checks. If no checksum is sent with the upload, Object Storage still calculates and stores one for the object, but this checksum is not validated during the upload.

The AWS CLI v2 automatically calculates and sends a checksum on every upload, using `CRC64NVME` by default, and verifies the checksum on every download. You only need to specify `--checksum-algorithm` if you want to use a different algorithm.

### Supported checksum algorithms

* `CRC64NVME` (default)
* `CRC32`
* `CRC32C`
* `SHA1`
* `SHA256`

### Uploading an object with a checksum

To use a specific checksum algorithm, set the `--checksum-algorithm` parameter:

```sh theme={null}
aws s3 cp <local_file_path> s3://<bucket_name>/<object_key> --checksum-algorithm SHA256
```

Object Storage recalculates the checksum on receipt. If it doesn't match the one sent by the AWS CLI, the upload fails.

### Retrieving the checksum of an object

To retrieve the stored checksum of an existing object, use the `head-object` command with the `--checksum-mode` parameter set to `ENABLED`:

```sh theme={null}
aws s3api head-object \
    --bucket <bucket_name> \
    --key <object_key> \
    --checksum-mode ENABLED
```

The output includes a checksum field, where the field name indicates the checksum algorithm and the value is a Base64-encoded checksum. For example:

```json theme={null}
{
    "ChecksumSHA256": "<base64_encoded_checksum>"
}
```

## How to rename an object

> [!NOTE]
>
> Renaming objects is not supported in the web console.

You can rename an object in your Object Storage bucket by using the following sequence:

1. Copy the object in question with a new name. You can also update an object's prefix:

   ```sh theme={null}
   aws s3 cp \
       s3://<bucket_name>/[<prefix_for_old_object_key>] \ # prefix and name of the object to rename
       s3://<bucket_name>/[<prefix_for_new_object_key>]   # desired prefix and name of the object
   ```

2. Remove the old copy of the renamed object:

   ```sh theme={null}
   aws s3 rm s3://<bucket_name>/[<prefix_for_old_object_key>]
   ```

## How to delete objects

### Deleting a single object

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket that contains the object.
3. Next to the object, click  → **Delete**.
4. In the **Delete object** window, type the object name in the confirmation field and click **Delete object**.

**AWS CLI**

To remove the object with a specified key:

```sh theme={null}
aws s3 rm s3://<bucket_name>/<object_key>
```

You can find more information on the `rm` command in the [AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html).

### Deleting multiple objects

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket that contains the objects.
3. In the **Select** column, select the checkbox next to each object to delete. To select all the objects in the bucket, use the checkbox in the column header.
4. In the banner that appears, click  **Delete**.
5. In the **Delete objects** window, type the bucket name in the confirmation field and click **Delete objects**.

**AWS CLI**

To delete all the objects with a specified prefix:

```sh theme={null}
aws s3 rm --recursive s3://<bucket_name>/[<prefix_for_object_keys>]
```

You can find more information on the `rm` command in the [AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html).

### Deleting all objects

**Web console**

To remove all the objects from a bucket, delete this bucket and create a new one in its place:

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Remove the existing bucket:
   1. Save the name and parameters of the bucket from which you want to remove all the objects.
   2. Next to the bucket, click  → **Delete**.
   3. Confirm the bucket deletion. Allow some time for your bucket to be deleted. You can monitor the status of your deleted bucket by selecting **Deleted** in the panel.
3. Recreate your bucket:
   1. Click  **Create bucket**.
   2. Under **Bucket name**, specify the bucket name you copied from the deleted bucket.
   3. Set the [bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters).
   4. Click **Create bucket**.

**s5cmd**

To delete all the objects from the bucket:

1. Prepare the Object Storage endpoint URL (`endpoint-url`) for the bucket in question. It should follow this pattern:

   ```url theme={null}
   https://storage.<region_ID>.nebius.cloud
   ```

   You can find your project's Region ID in the [Nebius AI Cloud regions](https://docs.nebius.com/overview/regions.mdx#public-regions) page.

2. Run the following command:

   ```sh theme={null}
   s5cmd \
     --endpoint-url <endpoint-url> \
     rm --all-versions "s3://<bucket_name>/*"
   ```

**AWS CLI**

> [!TIP]
>
> The AWS API limit per `delete-objects` call is 1000 keys. The `--max-items` flag value meets that constraint. If your bucket contains more than 1000 objects or delete markers, run each command again as needed until all of them are removed.

* To delete all the objects from the bucket, run the following command:

  ```sh theme={null}
  aws s3api delete-objects \
    --bucket <bucket_name> \
    --delete \
    "$(aws s3api list-object-versions \
    --bucket <bucket_name> \
    --query '{Objects: Versions[].{Key: Key, VersionId: VersionId}}' \
    --max-items 1000)"
  ```

* If your bucket has [versioning](https://docs.nebius.com/object-storage/buckets/versioning.mdx) enabled, also remove all delete markers:

  ```sh theme={null}
  aws s3api delete-objects \
    --bucket <bucket_name> \
    --delete \
    "$(aws s3api list-object-versions \
    --bucket <bucket_name> \
    --query '{Objects: DeleteMarkers[].{Key: Key, VersionId: VersionId}}' \
    --max-items 1000)"
  ```

You can find more information on the `delete-objects` S3 API command in the [AWS CLI reference](https://docs.aws.amazon.com/cli/latest/reference/s3api/delete-objects.html).

When an object is deleted from a bucket in Object Storage, it becomes immediately inaccessible and cannot be restored. The actual object data is then physically deleted from Nebius AI Cloud servers within 4 days.

## See also

* [Working with Object Storage buckets and objects using the AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md)
* [Sharing objects with presigned URLs in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
* [cp in AWS CLI reference](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)
* [ls in AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/ls.html)
* [rm in AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html)
* [Checksum validation in AWS CLI](https://docs.aws.amazon.com/cli/latest/topic/s3-faq.html#q-does-the-aws-cli-validate-checksums)
* [Checking object integrity in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html)
