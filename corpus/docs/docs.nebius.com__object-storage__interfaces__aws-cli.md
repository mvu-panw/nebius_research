# Working with Object Storage buckets and objects using the AWS CLI

Source: https://docs.nebius.com/object-storage/interfaces/aws-cli

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Working with Object Storage buckets and objects using the AWS CLI

Object Storage is compatible with the Amazon S3 API, which allows you to operate resources using AWS CLI. This Nebius AI Cloud reference shows you how to set up and configure AWS CLI and how to use it to work with [buckets](#working-with-buckets) and [objects](#working-with-objects) complemented with useful [parameters](#useful-parameters-for-aws-cli-commands) you can apply.

For the list of supported Amazon S3 features and the few exceptions, see [Amazon S3 API Compatibility Reference](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md).

## Configuring AWS CLI

This section explains how to create a service account, grant it access to manage your resources and set up the AWS CLI to perform actions on the service account's behalf. This section also covers other settings that connect the AWS CLI with Nebius AI Cloud and Object Storage.

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> **AWS CLI setup instructions**
>
> 1. Create a service account and save its ID to an environment variable:
>
>    ```bash theme={null}
>    export SA_ID=$(nebius iam service-account create \
>      --name object-storage-sa \
>      --format jsonpath='{.metadata.id}')
>    ```
>
> 2. Grant edit access to the service account:
>
>    1. Get the tenant ID:
>
>       ```bash theme={null}
>       export PROJECT_ID=$(nebius config get parent-id)
>       export TENANT_ID=$(nebius iam project get $PROJECT_ID --format jsonpath='{.metadata.parent_id}')
>       ```
>
>    2. Get the ID of the default `editors` group:
>
>       ```bash theme={null}
>       export EDITORS_GROUP_ID=$(nebius iam group get-by-name \
>         --name editors --parent-id $TENANT_ID \
>         --format jsonpath='{.metadata.id}')
>       ```
>
>    3. Add the service account to `editors` group:
>
>       ```bash theme={null}
>       nebius iam group-membership create \
>         --parent-id $EDITORS_GROUP_ID \
>         --member-id $SA_ID
>       ```
>
> 3. Create an [access key](https://docs.nebius.com/iam/service-accounts/access-keys.md) for the service account and get its AWS-like ID and contents:
>
>    ```bash theme={null}
>    export ACCESS_KEY_ID=$(nebius iam v2 access-key create \
>      --account-service-account-id $SA_ID \
>      --description 'AWS CLI' \
>      --format json | jq -r '.metadata.id')
>    export ACCESS_KEY_AWS_ID=$(nebius iam v2 access-key get \
>      --id $ACCESS_KEY_ID \
>      --format json | jq -r '.status.aws_access_key_id')
>    export SECRET_ACCESS_KEY=$(nebius iam v2 access-key get \
>      --id $ACCESS_KEY_ID \
>      --format json | jq -r '.status.secret')
>    ```
>
> 4. Add the key to the AWS CLI configuration:
>
>    ```bash theme={null}
>    aws configure set aws_access_key_id $ACCESS_KEY_AWS_ID
>    aws configure set aws_secret_access_key $SECRET_ACCESS_KEY
>    ```
>
> 5. Depending on your project [region](https://docs.nebius.com/overview/regions.md), add the Nebius AI Cloud region ID and the Object Storage endpoint URL to the AWS CLI configuration:
>
>    ```bash theme={null}
>    aws configure set region <region_ID>
>    aws configure set endpoint_url https://storage.<region_ID>.nebius.cloud
>    ```
>
>    For example, run the following commands for a project in `eu-north1`:
>
>    ```bash theme={null}
>    aws configure set region eu-north1
>    aws configure set endpoint_url https://storage.eu-north1.nebius.cloud
>    ```

## Working with buckets

In Object Storage, you store your files in containers called *buckets*.

### Create a bucket

Use the [s3 mb](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mb.html) ("make bucket") command to create a bucket:

```bash theme={null}
aws s3 mb s3://<bucket_name>
```

> **Usage example**
>
> Run:
>
> ```bash theme={null}
> aws s3 mb s3://example-bucket
> ```
>
> Output:
>
> ```bash theme={null}
> make_bucket: example-bucket
> ```

### List your buckets

Use the [s3 ls](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/ls.html) ("LiSt") command to see all your available buckets:

```bash theme={null}
aws s3 ls
```

### Delete a bucket

Use the [s3 rb](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rb.html) ("remove bucket") command to delete an empty bucket:

```bash theme={null}
aws s3 rb s3://<bucket_name>
```

A bucket you want to delete must be completely empty. If you still have objects in your bucket, use the `--force` parameter to remove a non-empty bucket:

```bash theme={null}
aws s3 rb s3://<bucket_name> --force
```

> **Usage examples**
>
> **Empty bucket**
>
> Run:
>
> ```bash theme={null}
> aws s3 rb s3://example-bucket
> ```
>
> Output:
>
> ```bash theme={null}
> remove_bucket: example-bucket
> ```
>
> **Non-empty bucket (force delete)**
>
> In this example, the bucket `example-bucket` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt`.
>
> Run:
>
> ```bash theme={null}
> aws s3 rb s3://example-bucket --force
> ```
>
> Output:
>
> ```bash theme={null}
> delete: s3://example-bucket/euismod.txt
> delete: s3://example-bucket/litora.txt
> delete: s3://example-bucket/lorem.txt
> remove_bucket: example-bucket
> ```

### Configure lifecycle rules

You can use the AWS CLI to configure lifecycle rules for object expiration and storage-class transitions in a bucket.

When you update a bucket lifecycle configuration, provide the full configuration in JSON, including all existing rules that you want to keep. If you omit a rule or some of its parameters, the new configuration replaces the old one and the omitted data is removed.

To review the current lifecycle configuration of a bucket, run:

```bash theme={null}
aws s3api get-bucket-lifecycle-configuration --bucket <bucket_name>
```

To change a lifecycle configuration, prepare a JSON file that states a new configuration and apply this file:

```bash theme={null}
aws s3api put-bucket-lifecycle-configuration \
  --bucket <bucket_name> \
  --lifecycle-configuration file://lifecycle.json
```

> **Examples of JSON files**
>
> **Expiration**
>
> This example shows a lifecycle rule that deletes all objects in the bucket five days after their upload.
>
> ```json theme={null}
> {
>   "Rules": [
>     {
>       "ID": "<rule_ID>",
>       "Status": "Enabled",
>       "Filter": {},
>       "Expiration": {
>         "Days": 5
>       }
>     }
>   ]
> }
> ```
>
> **Transition of storage class**
>
> This example shows a lifecycle rule that transitions objects with the `expiring/` prefix to the `STANDARD` storage class after 30 days.
>
> ```json theme={null}
> {
>   "Rules": [
>     {
>       "ID": "<rule_ID>",
>       "Status": "Enabled",
>       "Filter": {
>       "Prefix": "expiring/"
>       },
>       "Transitions": [
>         {
>           "StorageClass": "STANDARD",
>           "Days": 30
>         }
>       ]
>     }
>   ]
> }
> ```

For more information, see [How to configure lifecycle rules in Object Storage](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md).

## Working with objects

In Object Storage, you work with files and folders called *objects*.

### Upload objects

> [!WARNING]
>
> The AWS CLI does not support uploading objects to a [storage class](https://docs.nebius.com/object-storage/storage-classes.md) that differs from the bucket's default. To do that, use [s5cmd](https://github.com/peak/s5cmd). For details, see [How to upload](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-upload).

You can choose to upload a single file or a whole folder containing any number of files:

**Single file**

Use the [s3 cp](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html) ("CoPy") command to upload a specified local file to your Object Storage bucket with a specified prefix:

```bash theme={null}
aws s3 cp <source/path> s3://<bucket_name>/<object_key>
```

> **Usage example**
>
> Run:
>
> ```bash theme={null}
> aws s3 cp lorem-ipsum/lorem.txt s3://example-bucket/lorem-ipsum/
> ```
>
> Output:
>
> ```bash theme={null}
> upload: lorem-ipsum/lorem.txt to s3://example-bucket/lorem-ipsum/lorem.txt
> ```

**Folder**

There are two ways to upload the contents of a specified local folder to your Object Storage bucket with a specified prefix:

* [s3 cp](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html) ("CoPy") command copies all the files from the source to the target:

  ```bash theme={null}
  aws s3 cp --recursive \
      <source/path/> s3://<bucket_name>/[<prefix_for_object_keys>]/
  ```

  The `--recursive` parameter used in the command above keeps copying files from the local folder until all available files have been copied.

  > **Usage example**
  >
  > In this example, the local folder `lorem-ipsum/` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt`.
  >
  > Run:
  >
  > ```bash theme={null}
  > aws s3 cp lorem-ipsum/ s3://example-bucket/lorem-ipsum/ --recursive
  > ```
  >
  > Output:
  >
  > ```bash theme={null}
  > upload: lorem-ipsum/lorem.txt to s3://example-bucket/lorem-ipsum/lorem.txt
  > upload: lorem-ipsum/litora.txt to s3://example-bucket/lorem-ipsum/litora.txt
  > upload: lorem-ipsum/euismod.txt to s3://example-bucket/lorem-ipsum/euismod.txt
  > ```

* [s3 sync](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/sync.html) command only copies new and updated files compared to the target:

  ```bash theme={null}
  aws s3 sync <local/destination/path/> s3://<bucket_name>/[<prefix_for_object_keys>]/
  ```

  > **Usage example**
  >
  > In this example, the local folder `lorem-ipsum/` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt`.
  >
  > Run:
  >
  > ```bash theme={null}
  > aws s3 sync lorem-ipsum/ s3://example-bucket/lorem-ipsum/
  > ```
  >
  > Output:
  >
  > ```bash theme={null}
  > upload: lorem-ipsum/lorem.txt to s3://example-bucket/lorem-ipsum/lorem.txt
  > upload: lorem-ipsum/litora.txt to s3://example-bucket/lorem-ipsum/litora.txt
  > upload: lorem-ipsum/euismod.txt to s3://example-bucket/lorem-ipsum/euismod.txt
  > ```

If the name of your local folder contains spaces, put it in single quotation marks. For example: `Documents/'My ML configurations'/`.

### List objects in your bucket

Use the [s3 ls](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/ls.html) ("LiSt") command with a `<bucket_name>` and a `[<prefix_for_object_keys>]` to see all your available objects:

```bash theme={null}
aws s3 ls s3://<bucket_name>/[<prefix_for_object_keys>] --recursive --human-readable --summarize
```

The command contains the following parameters:

* `--recursive` keeps listing objects in the bucket under all available object keys until all have been listed.
* `--human-readable` clearly defines data capacity units and rounds them up if necessary.
* `--summarize` below the list of objects, shows the total number and the total size of all the objects in the bucket.

> **Usage example**
>
> In this example, your Object Storage `example-bucket` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt` under the object key `lorem-ipsum/`.
>
> Run:
>
> ```bash theme={null}
> aws s3 ls s3://example-bucket/ --recursive --human-readable --summarize
> ```
>
> Output:
>
> ```bash theme={null}
> 2024-09-05 16:35:34  458 Bytes lorem-ipsum/euismod.txt
> 2024-09-05 16:35:35  442 Bytes lorem-ipsum/litora.txt
> 2024-09-05 16:35:35  505 Bytes lorem-ipsum/lorem.txt
>
> Total Objects: 3
>    Total Size: 1.4 KiB
> ```

### Move objects between buckets

Use the [s3 mv](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mv.html) ("MoVe") command to copy objects with a specified prefix from the source bucket to another destination bucket with a new prefix within your Object Storage cluster, then remove the objects at the origin:

```bash theme={null}
aws s3 mv s3://<origin_bucket_name>/[<prefix_for_object_keys>]/ s3://<target_bucket_name>/[<prefix_for_object_keys>]/ --recursive
```

The `--recursive` parameter used in the command above keeps listing objects in the bucket under all available object keys until all have been listed.

> **Usage example**
>
> In this example, your Object Storage `example-bucket` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt` under the object key `lorem-ipsum/`. You need to move these objects to `another-example-bucket` under the prefix `lorem-ipsum-mv/`.
>
> Run:
>
> ```bash theme={null}
> aws s3 mv s3://example-bucket/lorem-ipsum/ s3://another-example-bucket/lorem-ipsum-mv --recursive
> ```
>
> Output:
>
> ```bash theme={null}
> move: s3://example-bucket/lorem-ipsum/litora.txt to s3://another-example-bucket/lorem-ipsum-mv/litora.txt
> move: s3://example-bucket/lorem-ipsum/lorem.txt to s3://another-example-bucket/lorem-ipsum-mv/lorem.txt
> move: s3://example-bucket/lorem-ipsum/euismod.txt to s3://another-example-bucket/lorem-ipsum-mv/euismod.txt
> ```

### Download objects

**Single object**

Use the [s3 cp](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html) ("CoPy") command to download a specified object with a prefix from your Object Storage bucket to a destination on your local machine:

```bash theme={null}
aws s3 cp s3://<bucket_name>/<object_key> <local/destination/path/>
```

You can set a different name for a file you want to download in `<local/destination/path/>`.

> **Usage example**
>
> In this example, you'll download the `lorem.txt` file from the Object Storage `example-bucket` to the local `example-download/` folder as `lorem-download.txt`.
>
> Run:
>
> ```bash theme={null}
> aws s3 cp s3://example-bucket/lorem-ipsum/lorem.txt example-download/lorem-download.txt
> ```
>
> Output:
>
> ```bash theme={null}
> download: s3://quickstart-bucket/lorem-ipsum/lorem.txt to example-download/lorem-download.txt
> ```

**All objects with a prefix**

There are two ways to download all the objects with a specified prefix from your Object Storage bucket to a destination on your local machine:

* [s3 cp](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html) ("CoPy") command copies all the objects with a specified prefix from your Object Storage bucket to a destination on your local machine:

  ```bash theme={null}
  aws s3 cp --recursive \
      s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/>
  ```

  > **Usage example**
  >
  > In this example, your Object Storage `example-bucket` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt` under the object key `lorem-ipsum/`. They need to be downloaded into the local `example-download/` folder.
  >
  > Run:
  >
  > ```bash theme={null}
  > aws s3 cp --recursive s3://example-bucket/lorem-ipsum/ example-download/
  > ```
  >
  > Output:
  >
  > ```bash theme={null}
  > download: s3://example-bucket/lorem-ipsum/lorem.txt to example-download/lorem.txt
  > download: s3://example-bucket/lorem-ipsum/litora.txt to example-download/litora.txt
  > download: s3://example-bucket/lorem-ipsum/euismod.txt to example-download/euismod.txt
  > ```

* [s3 sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html) command copies new and updated files from your Object Storage bucket compared to a destination on your local machine:

  ```bash theme={null}
  aws s3 sync s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/>
  ```

  > **Usage example**
  >
  > In this example, your Object Storage `example-bucket` contains three text files: `lorem.txt`, `euismod.txt` and `litora.txt` under the object key `lorem-ipsum/`. They need to be downloaded into the local `example-download/` folder.
  >
  > Run:
  >
  > ```bash theme={null}
  > aws s3 sync s3://example-bucket/lorem-ipsum/ example-download/
  > ```
  >
  > Output:
  >
  > ```bash theme={null}
  > download: s3://example-bucket/lorem-ipsum/lorem.txt to example-download/lorem.txt
  > download: s3://example-bucket/lorem-ipsum/litora.txt to example-download/litora.txt
  > download: s3://example-bucket/lorem-ipsum/euismod.txt to example-download/euismod.txt
  > ```

If the name of your local folder contains spaces, put it in single quotation marks. For example: `Documents/'My ML configurations'/`.

### Delete objects

Use the [s3 rm](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html) ("ReMove") command to delete objects from your Object Storage bucket.

**Single object**

```bash theme={null}
aws s3 rm s3://<bucket_name>/<object_key>
```

**All objects with a prefix**

```bash theme={null}
aws s3 rm s3://<bucket_name>/[<prefix_for_object_keys>] --recursive
```

The `--recursive` parameter used in the command above keeps deleting objects in the bucket under the specified object key until all have been deleted.

## Useful parameters for AWS CLI commands

This section describes useful parameters you can use with most of the commands listed above.

### Include

When you use the [s3 cp](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html), [s3 sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html), [s3 mv](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mv.html) or [s3 rm](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html) command, you can apply the `--include` parameter to set the rule to **only** include parameters specified.

For example, your Object Storage bucket contains images and text files, but you want to download text files only. Set the rule as follows:

```bash theme={null}
aws s3 cp s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/> \
    --recursive \
    --include "*.txt"
```

In the command above:

* `--recursive` copies all the objects available at the source.
* `--include "*.txt"` applies the command only to `.txt` files.

  Note that you need to use multiple `--include` parameters to define more than one condition.

### Exclude

When you use the [s3 cp](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html), [s3 sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html), [s3 mv](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mv.html) or [s3 rm](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html) command, you can apply the `--exclude` parameter to set the rule to include all the files **except** the parameters specified.

For example, your Object Storage bucket contains images in `.png` and `.jpg` formats together with text files, but you want to download text files only. Set the rule as follows:

```bash theme={null}
aws s3 cp s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/> \
    --recursive \
    --exclude "*.png" --exclude "*.jpg"
```

In the command above:

* `--recursive` copies all the objects available at the source.
* `--exclude "*.png" --exclude "*.jpg"` applies the command to all file formats except `.png` and `.jpg`.

  Note that you need to use multiple `--exclude` parameters to define more than one condition.
