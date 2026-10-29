# Uploading and downloading objects in Object Storage

Source: https://docs.nebius.com/object-storage/objects/upload-download

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Uploading and downloading objects in Object Storage

In Object Storage, you work with files and folders called objects and place them in containers called buckets. This guide will help you upload files to buckets and download them.

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

## How to upload

### Uploading a single file

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.

2. Select the bucket where you want to upload a file.

3. Upload a file:

   1. Click  **Add** → **Object**.
   2. In the window that opens, select the file to upload.
   3. Click **Upload**.

4. Check that the **Objects** tab shows the new object.

**AWS CLI**

> [!WARNING]
>
> The [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md) does not support uploading objects to a storage class that differs from the bucket's default. To do that, use [s5cmd](https://github.com/peak/s5cmd).

This command uploads a specified local file to your Object Storage bucket with a specified prefix:

```sh theme={null}
aws s3 cp <source/path> s3://<bucket_name>/<object_key>
```

The object is uploaded to the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) that is set as default for the bucket.

You can find more information on the `cp` command in the [AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html).

**s5cmd**

This command uploads a specified local file to your Object Storage bucket with a specified prefix:

```sh theme={null}
s5cmd cp <source/path> s3://<bucket_name>/<object_key>
```

The object is uploaded to the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) that is set as default for the bucket. If you need a different class, add the `--storage-class <STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT>` parameter to this command.

### Uploading a single file in parts

Object Storage supports [multipart uploads](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html). For detailed instructions, see the [Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html#clisupportformpu).

> [!NOTE]
>
> For buckets created on or after November 9, 2026, Object Storage automatically deletes incomplete multipart uploads after 30 days. To change this behavior, [create an expiration lifecycle rule](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-expiration-lifecycle-rules) to abort incomplete multipart uploads according to your preferred pattern. Creating such a rule disables the default automatic deletion, even if you set the rule status to disabled.

### Uploading a folder

You can use the web console to create a folder in a bucket and [upload files to it](#uploading-a-single-file). With the AWS CLI, you can upload an entire local folder including its contents.

**Web console**

To create a folder:

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket where you want to create the folder.
3. Click  **Add** → **Folder**.
4. In the **Create folder** window, enter a name and click **Create**.

After you create the folder, you can [add files to it](#uploading-a-single-file).

**AWS CLI**

There are two ways to upload the contents of a specified local folder to your Object Storage bucket with a specified prefix:

* `cp` command copies all the files from the source:

  ```sh theme={null}
  aws s3 cp --recursive \
      <source/path/> s3://<bucket_name>/[<prefix_for_object_keys>]/
  ```

* `sync` command only copies new and updated files compared to the target:

  ```sh theme={null}
  aws s3 sync <local/destination/path/> s3://<bucket_name>/[<prefix_for_object_keys>]/
  ```

You can find more information on these commands in the AWS CLI reference:

* [cp](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)
* [sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html)

If the name of your local folder contains spaces, put it in single quotation marks. For example: `Documents/'My ML configurations'/`.

## How to download

You can download a single object from an Object Storage bucket with the web console or AWS CLI. The AWS CLI also lets you download all objects with a specified prefix.

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket that contains the object.
3. In the row of the object to download, click  → **Download**.

**AWS CLI**

To download a single object with a specified prefix from your Object Storage bucket to a destination on your local machine:

```sh theme={null}
aws s3 cp s3://<bucket_name>/<object_key> <local/destination/path/>
```

To download all the objects with a specified prefix, use one of the following commands:

* `cp` command:

  ```sh theme={null}
  aws s3 cp --recursive \
      s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/>
  ```

* `sync` command:

  ```sh theme={null}
  aws s3 sync s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/>
  ```

You can find more information on these commands in the AWS CLI reference:

* [cp](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)
* [sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html)

If the name of your local folder contains spaces, put it in single quotation marks. For example: `Documents/'My ML configurations'/`.

## Example with the AWS CLI

Assume that you already have an Object Storage bucket named `quickstart-bucket`. The example below shows how to upload objects to your bucket and download them using the AWS CLI.

1. Create a local folder from which you'll upload files to your bucket:

   ```sh theme={null}
   mkdir lorem-ipsum
   ```

2. Create the files to upload. Run the commands from the code block below:

   ```sh theme={null}
   echo 'Lorem ipsum odor amet, consectetuer adipiscing elit. Posuere ullamcorper hendrerit faucibus pellentesque sociosqu montes. Tempus ut sit rutrum etiam sodales, porttitor congue condimentum nulla. Facilisis sodales habitant mi justo duis. Hendrerit praesent sit facilisi congue felis primis lobortis mattis nibh. Augue netus laoreet magna class enim fringilla molestie ipsum. Quisque natoque ligula lobortis accumsan potenti? Convallis pellentesque magna enim suscipit risus mauris molestie parturient quam.' > lorem-ipsum/lorem.txt
   echo 'Euismod porta phasellus bibendum urna dolor tincidunt dapibus eu maecenas. Aliquet eget gravida; tempus curae potenti class. Lectus nibh nam donec sagittis donec felis posuere libero. Suspendisse accumsan suscipit blandit orci platea iaculis ac. Suspendisse egestas aptent aliquam sapien ut maximus. Litora ridiculus augue mi, ut aliquam amet. Fusce dignissim nulla venenatis dis himenaeos habitasse. Blandit primis massa eros gravida rhoncus nascetur nulla' > lorem-ipsum/euismod.txt
   echo 'Litora integer iaculis libero dui pretium porta scelerisque. Dis laoreet ipsum porta viverra ipsum sem feugiat. Arcu ex natoque commodo faucibus facilisis vivamus sagittis; ultricies quis. Senectus vivamus nec cras porttitor penatibus. Ipsum vitae integer elementum; sem gravida etiam. Vivamus purus nunc nunc et aenean class. Tempor sagittis sociosqu erat class laoreet iaculis nec. Tempus ligula pellentesque a molestie fames elit vivamus.' > lorem-ipsum/litora.txt
   ```

   This creates three text files in your new `lorem-ipsum/` folder:

   * `lorem.txt`
   * `euismod.txt`
   * `litora.txt`

3. Upload all the files from your `lorem-ipsum/` folder to your Object Storage bucket with the `lorem-ipsum` prefix:

   ```sh theme={null}
   aws s3 cp lorem-ipsum/ s3://quickstart-bucket/lorem-ipsum/ --recursive
   ```

   > **Output**
   >
   > ```sh theme={null}
   > upload: lorem-ipsum/lorem.txt to s3://quickstart-bucket/lorem-ipsum/lorem.txt
   > upload: lorem-ipsum/litora.txt to s3://quickstart-bucket/lorem-ipsum/litora.txt
   > upload: lorem-ipsum/euismod.txt to s3://quickstart-bucket/lorem-ipsum/euismod.txt
   > ```

4. [List](https://docs.nebius.com/object-storage/objects/manage.md#how-to-view-objects) the objects with the `lorem-ipsum` prefix in your bucket:

   ```sh theme={null}
   aws s3 ls s3://quickstart-bucket/lorem-ipsum --recursive --human-readable --summarize
   ```

   > **Output**
   >
   > ```sh theme={null}
   > YYYY-MM-DD HH:MM:SS  458 Bytes lorem-ipsum/euismod.txt
   > YYYY-MM-DD HH:MM:SS  442 Bytes lorem-ipsum/litora.txt
   > YYYY-MM-DD HH:MM:SS  505 Bytes lorem-ipsum/lorem.txt
   >
   > Total Objects: 3
   >     Total Size: 1.4 KiB
   > ```

5. Download the `lorem.txt` file from your bucket to the local `lorem-ipsum/` folder as `lorem-download.txt`:

   ```sh theme={null}
   aws s3 cp s3://quickstart-bucket/lorem-ipsum/lorem.txt lorem-ipsum/lorem-download.txt
   ```

   > **Output**
   >
   > ```sh theme={null}
   > download: s3://quickstart-bucket/lorem-ipsum/lorem.txt to lorem-ipsum/lorem-download.txt
   > ```

6. Check if the downloaded file is there:

   ```sh theme={null}
   ls lorem-ipsum/
   ```

   > **Output**
   >
   > ```sh theme={null}
   > euismod.txt        litora.txt         lorem-download.txt lorem.txt
   > ```

7. [Delete](https://docs.nebius.com/object-storage/objects/manage.md#how-to-delete-objects) all the files with the `lorem-ipsum` prefix from your Object Storage bucket:

   ```sh theme={null}
   aws s3 rm s3://quickstart-bucket/lorem-ipsum --recursive
   ```

   > **Output**
   >
   > ```sh theme={null}
   > delete: s3://quickstart-bucket/lorem-ipsum/litora.txt
   > delete: s3://quickstart-bucket/lorem-ipsum/euismod.txt
   > delete: s3://quickstart-bucket/lorem-ipsum/lorem.txt
   > ```

8. Remove the `lorem-ipsum/` folder from your computer:

   ```sh theme={null}
   rm -r lorem-ipsum/
   ```
