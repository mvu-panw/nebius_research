# Compatibility of Amazon S3 API with Object Storage

Source: https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Compatibility of Amazon S3 API with Object Storage

Object Storage is compatible with the Amazon S3 API, so you can use your existing S3 tools, SDKs and workflows without additional configuration. This reference outlines the boundaries of that compatibility.

For bucket-level operations such as creating buckets or enabling versioning, S3-compatible tools generally work, but [Nebius AI Cloud API](https://docs.nebius.com/grpc-api/index.md), [CLI](https://docs.nebius.com/cli/index.md) and [Terraform provider](https://docs.nebius.com/terraform-provider.md) offer the most complete feature coverage.

## Unsupported S3 features

The following S3 features are not supported in Object Storage:

* **Object ACLs**: Per-object access control lists are not supported. Use [bucket policies](https://docs.nebius.com/object-storage/buckets/bucket-policy.md) for access control.
* **SSE-KMS and SSE-S3 encryption**: AWS-managed server-side encryption is not supported. All data stored in buckets is [encrypted](https://docs.nebius.com/security/encryption.md#buckets-in-object-storage) at both the service and infrastructure levels.
* **Object Lock and Legal Hold**: Write-once-read-many (WORM) retention policies are not supported.
* **S3 Select**: Query-in-place functionality is not supported. AWS has also discontinued S3 Select.
* **Static website hosting**: Serving bucket contents as a static website is not supported.
* **Bucket inventory**: S3 API actions for inventory configurations are not supported. To get scheduled reports on bucket contents, use [inventory configurations](https://docs.nebius.com/object-storage/buckets/inventory.md) in the [web console](https://console.nebius.com).
* **Replication**: Cross-region and cross-bucket replication rules are not supported. Use [data transfers](https://docs.nebius.com/object-storage/transfer/overview.md) to replicate data between buckets.
* **Event notifications**: S3 Event Notifications are not supported.
* **Object Ownership**: S3 Object Ownership is not supported.

## Behavioral differences

Object Storage behaves differently from S3 in the following cases:

* **ETag format**: In some cases, Object Storage computes ETag values with a non-MD5 algorithm. The ETag still changes whenever the object's content changes, but it is not always the MD5 hash of that content, so don't rely on it for integrity checks. For regular buckets, use the checksum headers (`X-Amz-Checksum-*`) to verify object integrity instead. For [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md), ETags are not based on object content, and integrity checksums are not supported: objects with the same content can have different ETags, and objects with different content can have the same ETag. MD5-based ETags can be enabled per bucket for simple objects and multipart upload parts on request — [contact support](https://console.nebius.com/support/create-ticket) to discuss your use case.

* **Conditional writes**: On `PutObject` requests that include `If-None-Match: "*"`, Object Storage checks whether the object exists *before* reading the request body, whereas S3 reads the full body first and checks the condition afterward. This reduces unnecessary data transfer when the condition fails, but a client that doesn't support the [Expect: 100-continue](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Expect) header might see unexpected errors.

* **Plain HTTP access**: By default, Object Storage accepts S3 API requests over HTTPS only. For selected buckets, you can request [HTTP access](https://docs.nebius.com/object-storage/http-access.md) for object data requests, such as `GetObject`, `PutObject` and `ListObjects`, and for the following bucket information requests: `HeadBucket`, `GetBucketVersioning` and `GetBucketLocation`.

* **Object versioning**: Only the current version of an object can have a `null` version ID. Once an object version becomes non-current, it's assigned a specific version identifier.

* **ListObjectVersions**: In `ListObjectVersions` responses, the `NextKeyMarker` and `NextVersionIdMarker` fields are opaque tokens that are only valid when passed back exactly as received from the previous `ListObjectVersions` response.

* **ListMultipartUploads**: `ListMultipartUploads` doesn't support the `delimiter` parameter, and common prefixes are not returned in responses.

* **Lifecycle configuration**: The deprecated XML format is not supported. Use the current format described in [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html).

## Supported S3 API methods

Object Storage supports the following S3 API methods. **Partial** means the method works with the limitation noted.

| Method | Support | Notes |
| - | - | - |
| `GetObject` | Partial | For [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md), the `partNumber` parameter is not supported. |
| `HeadObject` | Partial | For [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md), the `partNumber` parameter is not supported. |
| `PutObject` | Yes | |
| `CopyObject` | Yes | |
| `DeleteObject` | Yes | |
| `DeleteObjects` | Yes | |
| `GetObjectACL` | No | |
| `ListObjectsV2` | Yes | |
| `ListObjects` | Partial | Supported for backward compatibility; `ListObjectsV2` is recommended. |
| `ListObjectVersions` | Yes | |
| `PostObject` | Partial | Supported for basic use cases. [Contact support](https://console.nebius.com/support/create-ticket) if your workload depends on this method. |
| `GetObjectTagging` | Partial | Not supported for [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md). |
| `PutObjectTagging` | Partial | Not supported for [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md). |
| `DeleteObjectTagging` | Partial | Not supported for [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md). |
| `CreateMultipartUpload` | Yes | |
| `UploadPart` | Yes | |
| `UploadPartCopy` | Yes | |
| `CompleteMultipartUpload` | Partial | For [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md), multipart uploads larger than 1 TB are not recommended. |
| `AbortMultipartUpload` | Yes | |
| `ListMultipartUploads` | Yes | |
| `CreateBucket` | Yes | |
| `HeadBucket` | Yes | |
| `GetBucketLocation` | Yes | |
| `GetBucketVersioning` | Yes | |
| `PutBucketVersioning` | Partial | Not supported for [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md). |
| `GetBucketLifecycleConfiguration` | Yes | Only S3-compatible lifecycle rules are supported. |
| `PutBucketLifecycleConfiguration` | Partial | Not supported for [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md). |
| `PutBucketCORS` | Yes | |

## Supported S3 headers

Object Storage supports the following S3-compatible HTTP headers:

* `X-Amz-Copy-Source`
* `X-Amz-Copy-Source-If-Match`
* `X-Amz-Copy-Source-Range`
* `X-Amz-Date`
* `X-Amz-Delete-Marker`
* `X-Amz-Expiration`
* `X-Amz-Metadata-Directive`
* `X-Amz-Mp-Parts-Count`
* `X-Amz-Request-Id`
* `X-Amz-Storage-Class`
* `X-Amz-Version-Id`
* `X-Amz-Bucket-Region`
* `X-Amz-Meta-*`
* `If-Match`: Supported in `GetObject`, `PutObject`, `DeleteObject`
* `If-None-Match`: Supported in `GetObject`, `PutObject`
* `If-Modified-Since`, `If-Unmodified-Since`: Supported in `GetObject`
* `Access-Control-*`
* `X-Amz-Checksum-*`: Not supported for [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md)

> [!NOTE]
>
> For [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md), conditional requests with `If-*` headers have best-effort behavior: Object Storage can't atomically verify that an object wasn't modified between checking the condition and completing the operation.

## See also

* [Working with Object Storage buckets and objects using the AWS CLI](https://docs.nebius.com/object-storage/interfaces/aws-cli.md)
* [Actions supported by Object Storage roles](https://docs.nebius.com/object-storage/supported-actions.md)
* [How data transfers work in Object Storage](https://docs.nebius.com/object-storage/transfer/overview.md)
