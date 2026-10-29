# HTTP access to the Object Storage S3 API

Source: https://docs.nebius.com/object-storage/http-access

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# HTTP access to the Object Storage S3 API

By default, Object Storage accepts S3 API requests over HTTPS only. For selected buckets, you can request plain HTTP access and use `http://` instead of `https://` in the S3 API endpoint.

Plain HTTP access can reduce encryption-related performance overhead in workloads that send many S3 API requests or use clients where TLS certificate configuration is resource-intensive. Use it only when the security tradeoff is acceptable, as HTTP doesn't encrypt object data, request metadata or request headers in transit.

## How HTTP access works

HTTP access is a bucket-level setting and is disabled by default. [Contact support](https://console.nebius.com/support/create-ticket) if you want to enable it for a specific bucket.

When you request HTTP access, provide the bucket ID or name, the bucket [region](https://docs.nebius.com/overview/regions.md) and one of the following access modes:

* **Disabled**: HTTP access is not allowed. This is the default mode.
* **Region-local**: HTTP access is allowed only from Nebius AI Cloud virtual machines (VMs) in the same region as the bucket. Requests from other regions and from outside Nebius AI Cloud are rejected.
* **All**: HTTP access is allowed from any source, including VMs in any region and clients outside Nebius AI Cloud.

> **How to check the bucket HTTP access mode**
>
> **Web console**
>
> 1. Go to  **Storage** → **Object Storage**.
> 2. On the **Buckets** tab, check the bucket label. Buckets with HTTP access enabled show **HTTP - Region** or **HTTP - All**.
>
> **CLI**
>
> Run the following command:
>
> ```bash theme={null}
> nebius storage bucket get --id storagebucket-e***
> ```
>
> The bucket's HTTP access mode is returned in the `.status.insecure_endpoint.mode` field:
>
> ```yaml highlight={9-10} theme={null}
> metadata:
>   id: storagebucket-e***
>   parent_id: project-e00***
>   name: <bucket_name>
>   resource_version: "1"
>   ...
> status:
>   ...
>   insecure_endpoint:
>     mode: REGION_LOCAL
> ```

After HTTP access is enabled, use the same Object Storage endpoint as for HTTPS, but replace `https://` with `http://`.

> For example, if your HTTPS endpoint is `https://storage.eu-north1.nebius.cloud`, the HTTP endpoint is `http://storage.eu-north1.nebius.cloud`.

## Authentication

Plain HTTP access supports only [access key pair](https://docs.nebius.com/iam/service-accounts/access-keys.md) authentication.

> [!WARNING]
>
> Authentication with an IAM token is not allowed over HTTP because HTTP does not use encryption. If an application sends an IAM token over HTTP, consider the token compromised: revoke it and configure the application to use access key pair authentication instead.

## Supported requests

Plain HTTP access is supported for S3 API requests that work with objects, such as `GetObject`, `PutObject`, `DeleteObject` or `ListObjects`.

The following bucket information requests are also supported over HTTP:

* `HeadBucket`
* `GetBucketLocation`
* `GetBucketVersioning`

Use HTTPS for all other requests.

## Limitations

* [Chunked uploads](https://docs.aws.amazon.com/AmazonS3/latest/developerguide/sigv4-streaming.html) are not supported over HTTP. Use HTTPS for these uploads.
* HTTP access doesn't change Object Storage encryption at rest. Stored objects remain encrypted by default.
