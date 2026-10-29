# How to configure a storage class in Object Storage

Source: https://docs.nebius.com/object-storage/configure-storage-classes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to configure a storage class in Object Storage

A storage class is one of a bucket's characteristics. You set it when you [create a bucket](https://docs.nebius.com/object-storage/configure-storage-classes.md#for-a-new-bucket), [edit it](https://docs.nebius.com/object-storage/configure-storage-classes.md#for-an-existing-bucket) or [upload an object](https://docs.nebius.com/object-storage/configure-storage-classes.md#how-to-upload-an-object-to-a-storage-class) to this bucket.

Object Storage supports three classes: Enhanced Throughput, Intelligent and Standard. They differ in price and performance.

For more information, see [Storage classes in Object Storage](https://docs.nebius.com/object-storage/storage-classes.md).

## How to set a default storage class for a bucket

Each bucket has a default storage class. All new objects are uploaded into this class unless you [explicitly define the class](#how-to-upload-an-object-to-a-storage-class).

By default, new buckets use the Standard storage class. You can change the default storage class both when you create a bucket and for an existing bucket. The new default storage class does not affect objects that are already in storage in the bucket.

> [!NOTE]
>
> You can use the **Force storage class** (`--force-storage-class`) [bucket parameter](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters) to make the default storage class override the storage class that you explicitly select for any individual object uploaded to the bucket.

### For a new bucket

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Click **Create resource** → **Bucket**.
3. Select the storage class in the bucket creation form.
4. Configure the other settings and create the bucket.

**Nebius AI Cloud CLI**

When you [create a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets), add the `--default-storage-class` parameter to set the default storage class:

```bash theme={null}
nebius storage bucket create \
  --default-storage-class <STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT> \
  ...
```

### For an existing bucket

**Web console**

1. In the sidebar, go to  **Storage** → **Object Storage**.
2. Select the bucket you need and switch to the **Settings** tab.
3. Select the storage class and save the changes.

**Nebius AI Cloud CLI**

When you [modify a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-modify-buckets), set the `--default-storage-class` parameter:

```bash theme={null}
nebius storage bucket update \
  --default-storage-class <STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT> \
  ...
```

## How to upload an object to a storage class

If you need to store an object in a different storage class than the default one for the bucket, set the storage class during upload.

> [!WARNING]
>
> The [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md) does not support uploading objects to a storage class that differs from the bucket's default. To do that, use [s5cmd](https://github.com/peak/s5cmd).

To [upload an object](https://docs.nebius.com/object-storage/objects/upload-download.md#uploading-a-single-file) to the desired storage class, set the `--storage-class` parameter in the upload command:

```bash s5cmd theme={null}
s5cmd cp \
   --storage-class <STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT> \
   ...
   <local_path> s3://<bucket>/<path>
```

To change the storage class of an object after you upload it, make a `copy-object` request that moves the object between storage classes:

```bash s5cmd theme={null}
s5cmd cp \
   --storage-class <STANDARD|ENHANCED_THROUGHPUT|INTELLIGENT> \
   ...
   s3://<bucket>/<path> s3://<bucket>/<path>
```
