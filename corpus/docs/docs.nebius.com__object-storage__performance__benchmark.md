# Performance benchmark tests with Warp in Object Storage

Source: https://docs.nebius.com/object-storage/performance/benchmark

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Performance benchmark tests with Warp in Object Storage

To test Object Storage performance, use [Warp](https://github.com/minio/warp). Warp is an open-source benchmarking utility designed to check performance of S3-compatible storage. It measures throughput and delivers reproducible, comparable results across any S3 environment.

## Prerequisites

1. Install Warp:

   ```bash theme={null}
   wget https://dl.min.io/aistor/warp/release/linux-amd64/warp
   chmod +x warp
   ```

2. [Create an Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets) if you don't have one.

3. [Create an access key](https://docs.nebius.com/iam/service-accounts/access-keys.md).

   You need its AWS-like ID and secret key to run benchmark tests. When you create the access key by using the CLI, the AWS-like ID and secret key are specified in the `.status.aws_access_key_id` and `.status.secret` parameters of the output.

   To create an access key, make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role.

## How to run benchmark tests

The example below showcases how to check the maximum single-node performance for read and write operations.

Warp provides multiple tests for S3 methods. If you want to test a different use case, see the [Warp repository](https://github.com/minio/warp) for documentation or [contact technical support](https://console.nebius.com/support/create-ticket).

To run benchmark tests:

1. Prepare environment variables for the tests:

   ```bash theme={null}
   export S3_ENDPOINT="storage.<region>.nebius.cloud:443"
   export S3_BUCKET="<bucket_name>"
   export S3_ACCESS_KEY="<AWS-like_ID>"
   export S3_SECRET_KEY="<secret_key>"
   ```

   In the `S3_ENDPOINT` variable, specify the same [region](https://docs.nebius.com/overview/regions.md) where your bucket is located.

2. Test the read performance:

   ```bash theme={null}
   ./warp get \
      --host "$S3_ENDPOINT" \
      --tls \
      --bucket "$S3_BUCKET" \
      --access-key "$S3_ACCESS_KEY" \
      --secret-key "$S3_SECRET_KEY" \
      --objects 5000 \
      --obj.size 10MiB \
      --duration 5m \
      --storage-class STANDARD \
      --concurrent 128
   ```

   Adjust the following parameters to your workload profile:

   * `--objects`: Number of objects to upload. The default value is `2500` but for better test results, specify at least `5000`.

   * `--obj.size`: Size of each generated object. Specify the value as `nKiB`, `nMiB` or `nGiB`, for example, `100KiB`. The default value is `10MiB`.

   * `--duration` (optional): Duration of the test. Specify the value as `Nm`, for example, `7m`. The default value is 5 minutes.

     Run the test for at least 5–10 minutes to see how stable the performance is.

   * `--storage-class` (optional): [Storage class](https://docs.nebius.com/object-storage/storage-classes.md) to use. Set `STANDARD` or `ENHANCED_THROUGHPUT`. If not specified, the default storage class of the bucket is applied.

   * `--concurrent`: Runs multiple concurrent operations per Warp client and sets the number of these operations. The default value is `20`.

     Adjust the value, according to the following recommendations:

     * The value range should be within 32–200.
     * For small objects, run the test with a higher concurrency. For large objects, run it with a lower concurrency.

     Try changing the number to find an optimal value. It depends on a selected storage class and on the machine where you run the test (for example, [Compute virtual machine](https://docs.nebius.com/compute/index.md), your local machine or the internet).

3. Test the write performance:

   ```bash theme={null}
   ./warp put \
     --host "$S3_ENDPOINT" \
     --tls \
     --bucket "$S3_BUCKET" \
     --access-key "$S3_ACCESS_KEY" \
     --secret-key "$S3_SECRET_KEY" \
     --obj.size 10MiB \
     --concurrent 128
   ```

   Adjust the `--obj.size` and `--concurrent` parameters in the same way as in the read performance test.
