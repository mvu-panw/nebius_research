# About Object Storage

Source: https://docs.nebius.com/object-storage/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# About Object Storage

Object Storage stores data for your ML/AI workloads.

For example, you train a text-to-text model with a dataset of several petabytes. Here is how you can use Object Storage for it:

1. **Data storage**: Upload your training data to a bucket. Each object in the bucket is a file with a piece of text data for training. Set this bucket as a data source for your training scripts.

2. **Checkpoint storage**: During the model training and running experiments, set the scripts to upload each model checkpoint to the dedicated bucket.

3. **Model registry**: Use Object Storage to distribute models across your services or consumers, or to leverage autoscaling during inference.

4. **Inference results storage**: During the model inference, store the inference results in an Object Storage bucket.

Your data in Object Storage is stored as *objects*: files in various formats together with their metadata. To organize the objects, you create containers called *buckets* in your [project](https://docs.nebius.com/iam/overview.md#projects) and upload objects into them.

## Buckets

A bucket is a container in Object Storage for storing files.

### Naming

A bucket name should be unique across the [region](https://docs.nebius.com/overview/regions.md). If you try to create a bucket with a name that is already taken by another bucket in the region, you will get a message about it.

The name must be 3 to 63 characters long and may contain lowercase Latin letters, numbers, dots and hyphens. It is used as a part of a URL for data access.

### URLs

Use the following template to access a bucket:

```url theme={null}
https://storage.<region_id>.nebius.cloud/<bucket_name>
```

In the URL above:

* `region_id`: the ID of the [region](https://docs.nebius.com/overview/regions.md) where the bucket is located.
* `bucket_name`: the name of the bucket you want to access.

For example, the URL for the `training-artifacts` bucket located in `eu-north1` (Finland) is:

```url theme={null}
https://storage.eu-north1.nebius.cloud/training-artifacts
```

## Objects

An object is a file in Object Storage together with its metadata.

### Naming

To avoid issues with your objects, follow these naming requirements:

* Object keys can be up to 1024 bytes long, case sensitive.
* Use UTF-8 alphanumeric characters, slashes (`/`) and certain [special characters](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-guidelines).

### Keys, prefixes and object hierarchy

Each Object Storage object has a *key*. The key can contain *prefixes* that act similarly to folders, organizing objects into groups.

Buckets have a flat structure: they have no folders in them; all objects in a bucket are at the same level of hierarchy. However, interfaces and tools supported by Object Storage, such as the [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md), can emulate folders. When listing objects, you can specify a *delimiter* to group object keys by common prefixes. A delimiter can be any string.

For example, if you use `/` as a delimiter and upload objects with the keys `training/object-1.txt` and `training/object-2.txt`, they'll be shown under the common prefix `training/`, like files in the same folder. The two uploaded objects will be accessible at `https://storage.<region_id>.nebius.cloud/<bucket_name>/training/object-1.txt` and `https://storage.<region_id>.nebius.cloud/<bucket_name>/training/object-2.txt` respectively.

### Storage classes

Object Storage provides [storage classes](https://docs.nebius.com/object-storage/storage-classes.md) to control settings for stored objects. You can set the default storage class for each bucket and upload individual objects to specific classes. In addition, you can [set up lifecycle rules](https://docs.nebius.com/object-storage/objects/lifecycles.md) to transition objects between classes.

### URLs

Use the following templates to access an object:

* `https://storage.<region_name>.nebius.cloud/<bucket_name>/<object_key>`
* `http://<bucket_name>.storage.<region_name>.nebius.cloud/<object_key>`

For example, the URL for the `requests.txt` object in the `training-artifacts` bucket located in `eu-north1` (Finland) is:

```url theme={null}
https://storage.eu-north1.nebius.cloud/training-artifacts/requests.txt
```

### Encryption

Nebius enforces strong encryption across all layers of data handling:

* **At rest:** all objects in Object Storage are encrypted using AES-256 by default.
* **In transit:** by default, communications use HTTPS (TLS 1.2 or higher). For selected buckets, you can request [HTTP access to the S3 API](https://docs.nebius.com/object-storage/http-access.md).

For more information about encryption at rest, see [Encryption in Nebius AI Cloud](https://docs.nebius.com/security/encryption.md).

## Actions with buckets and objects

In your project, you can [create buckets](https://docs.nebius.com/object-storage/buckets/manage.md), [upload objects](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-upload) to them and [download objects](https://docs.nebius.com/object-storage/objects/upload-download.md#how-to-download) from your buckets.
