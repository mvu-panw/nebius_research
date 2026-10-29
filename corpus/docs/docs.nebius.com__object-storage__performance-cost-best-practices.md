# Performance and cost-efficiency best practices in Object Storage

Source: https://docs.nebius.com/object-storage/performance-cost-best-practices

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Performance and cost-efficiency best practices in Object Storage

When performing operations on your Object Storage buckets and objects, you can use optimizations and approaches described in this article to ensure better performance and save costs.

## List objects without delimiter

Using [ListObjects](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html), an S3 API action, with a delimiter is much slower than listing objects without a delimiter. Flat listing provides better performance, especially in buckets with a lot of objects. Consider organizing your object keys without creating multiple levels of nested folders, so that you can use flat listing without delimiters in most or all cases.

If your object keys use prefixes to represent folders, you can get a flat list of objects in a leaf folder (that is, a folder that does not have nested folders) more efficiently by specifying a prefix instead of a delimiter in `ListObjects`.

## Use object versioning only if required

For lower latency and higher throughput in high-load scenarios, we recommend using buckets with [versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) disabled.

## Use concurrency

The S3 API and many interfaces and SDKs for it, such as the [AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md), support concurrent requests, which brings significant performance boosts if used correctly. This even applies to GET operations over single objects; the performance effect can be made stronger for large objects if you use multipart uploads and properly align the sizes of upload parts and download ranges (see [below](#optimize-the-sizes-of-upload-parts-and-download-ranges)).

When experiencing performance issues, try increasing concurrency to fully utilize your bandwidth. To find the balance between performance and client machine utilization, increase the number of concurrent requests gradually, and stop as soon as there is no further performance gain. Increasing concurrency to several hundreds per client machine is not recommended.

To set the number of concurrent requests in the AWS CLI, run the following command (the default concurrency is 10):

```bash theme={null}
aws configure set max_concurrent_requests 20
```

## Use HTTP only for selected workloads

If encryption causes performance issues or when certificate configuration is too resource-intensive, you can request [HTTP access to the S3 API](https://docs.nebius.com/object-storage/http-access.md). HTTP access is disabled by default and can be enabled only for a specific bucket by [contacting support](https://console.nebius.com/support/create-ticket).

> [!WARNING]
>
> Use HTTP access only for requests that are safe to send without encryption. HTTP doesn't encrypt object data, request metadata or request headers in transit. IAM token authentication is also not allowed over HTTP.

## Avoid overwriting the same key concurrently

Sending multiple concurrent `PUT` requests with the same key is supported but performs poorly and leads to occasional timeout errors, especially in versioned buckets.

## Optimize the sizes of upload parts and download ranges

While the S3 API allows creating parts up to 5 GiB, it is usually more efficient to use smaller parts. Start with smaller parts, like 10–50 MiB, and only use larger parts if you need to upload very large objects or reduce the number of upload requests.

The best way to choose the part size is to treat each part as a unit of download concurrency. Ideally, the part size should ensure that each download range covers one or more upload parts without overlaps.

> For example, if you have a 1000 MiB object, and you want to download it using 10 threads, your part size should be at most 100 MiB. But it is often more practical to go even smaller, for example, 10 MiB. Make sure that every thread downloads a range that consists of 10 parts: 0–100 MiB (parts 1–10), 100–200 MiB (parts 11–20) and so on. In that case, you can easily increase concurrency and keep it efficient without needing to re-upload the object with more parts.

To set the upload part size (also known as the chunk size) in the AWS CLI, run the following command:

```bash theme={null}
aws configure set s3.multipart_chunksize 50MB
```

> [!NOTE]
>
> Using bigger part sizes may limit your upload concurrency. For example, uploading a 100 MiB file with 50 MiB part sizes cannot be performed with a concurrency of 3 or more.

## Clean up incomplete multipart uploads

The multipart upload of a very large object may be interrupted at any time (due to a network issue, machine restart or simply after being canceled manually). Until the multipart upload is complete, its parts that have already been uploaded continue to be stored in the bucket, and you are [charged for storing them](https://docs.nebius.com/object-storage/resources/pricing.md). By default, depending on when you created the bucket, Object Storage stores parts of incomplete multipart uploads for at least 30 days:

* For buckets created before November 9, 2026, Object Storage doesn't automatically delete incomplete multipart uploads and stores their parts indefinitely by default. You can [configure an expiration lifecycle rule](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-expiration-lifecycle-rules) that automatically cleans up incomplete multipart uploads in your bucket. For example, the following command creates a rule that deletes incomplete uploads seven days after initiation:

  ```bash theme={null}
  cat <<EOF > uploads_lifecycle.json
  {
    "Rules": [
      {
        "ID": "AbortMultipartUploads",
        "Status": "Enabled",
        "Filter": {
          "Prefix": ""
        },
        "AbortIncompleteMultipartUpload": {
          "DaysAfterInitiation": 7
        }
      }
    ]
  }
  EOF

  aws s3api put-bucket-lifecycle-configuration \
    --bucket <bucket_name> \
    --lifecycle-configuration file://uploads_lifecycle.json
  ```

* For buckets created on or after November 9, 2026, Object Storage automatically deletes incomplete multipart uploads after 30 days. To change this behavior, [create an expiration lifecycle rule](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-expiration-lifecycle-rules) to abort incomplete multipart uploads according to your preferred pattern. Creating such a rule disables the default automatic deletion, even if you set the rule status to disabled.
