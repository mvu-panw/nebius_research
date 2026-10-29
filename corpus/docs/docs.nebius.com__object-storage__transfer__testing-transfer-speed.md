# Testing data transfer speed with Warp

Source: https://docs.nebius.com/object-storage/transfer/testing-transfer-speed

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Testing data transfer speed with Warp

The data transfer service uses multiple threads and clients to maximize performance. As a result, testing the maximum transfer speed requires enough objects and data to keep these operations busy. Use at least 20,000 objects totaling about 20 TiB. The measured speed also depends on the network limitations of the source and destination endpoints.

These instructions use [Warp](https://github.com/minio/warp) to test data transfer speed and generate a test dataset in Nebius Object Storage. To generate the dataset in another S3-compatible storage service, adapt the endpoint, bucket and credential values to your provider.

> [!WARNING]
>
> Nebius AI Cloud charges you for the test data that you store. When you no longer need the test data, [delete the objects](https://docs.nebius.com/object-storage/objects/manage.md#deleting-multiple-objects). For details, see [Pricing in Object Storage](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data).

## Prerequisites

1. Install Warp:

   ```bash theme={null}
   wget https://dl.min.io/aistor/warp/release/linux-amd64/warp
   chmod +x warp
   ```

2. [Create an Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets).

3. Make sure that the project has enough [Object Storage quota](https://docs.nebius.com/object-storage/resources/quotas-limits.md#quotas) for about 20 TiB of test data.

4. [Create an access key](https://docs.nebius.com/iam/service-accounts/access-keys.md) for a service account that can read and upload objects in the bucket. For example, assign the service account the [`storage.editor` role](https://docs.nebius.com/iam/authorization/roles#object-storage) for the bucket or its parent project.

   You need its AWS-like ID and secret key to generate the test dataset. When you create the access key by using the CLI, the AWS-like ID and secret key are specified in the `.status.aws_access_key_id` and `.status.secret` parameters of the output.

   To create an access key, make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role.

## How to prepare a test dataset

1. Set the bucket endpoint, name and credentials as environment variables, and specify the ID of the [region](https://docs.nebius.com/overview/regions.md) that contains the bucket:

   ```bash theme={null}
   export S3_ENDPOINT="storage.<region_ID>.nebius.cloud:443"
   export S3_BUCKET="<bucket_name>"
   export S3_ACCESS_KEY="<AWS-like_ID>"
   export S3_SECRET_KEY="<secret_key>"
   ```

2. Generate the test dataset. Use the `--noclear` parameter to keep the generated objects in the bucket after the test:

   ```bash theme={null}
   ./warp get \
      --host "$S3_ENDPOINT" \
      --tls \
      --bucket "$S3_BUCKET" \
      --access-key "$S3_ACCESS_KEY" \
      --secret-key "$S3_SECRET_KEY" \
      --objects 20000 \
      --obj.size 1GiB \
      --duration 1m \
      --storage-class ENHANCED_THROUGHPUT \
      --concurrent 32 \
      --noclear
   ```

   This command generates a test dataset of 20,000 objects, each 1 GiB in size, and keeps it in the bucket specified in the environment variables. The [Enhanced Throughput storage class](https://docs.nebius.com/object-storage/storage-classes.md#enhanced-throughput-storage-class) provides the best transfer speed.

## How to test data transfer speed

1. [Create and launch a one-time data transfer](https://docs.nebius.com/object-storage/transfer/launch.md) from the test bucket.
2. While the data transfer is running, [monitor the test bucket](https://docs.nebius.com/object-storage/monitoring.md). Use the **Traffic** metric, measured in bytes per second, to observe the transfer speed.
