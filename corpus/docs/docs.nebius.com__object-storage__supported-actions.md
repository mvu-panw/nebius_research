# Actions supported by Object Storage roles

Source: https://docs.nebius.com/object-storage/supported-actions

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Actions supported by Object Storage roles

Actions available to Object Storage users with specific [roles](https://docs.nebius.com/iam/authorization/roles.md) are based on the [Amazon S3 API methods](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html).

## Available actions per role

Object Storage roles support the following actions:

| Action | `storage.object-viewer` | `storage.object-lister` | `storage.editor` | `storage.viewer` | `storage.uploader` | `storage.object-editor` |
| - | - | - | - | - | - | - |
| `GetObject` | ✓ | — | ✓ | ✓ | — | ✓ |
| `HeadObject` | ✓ | — | ✓ | ✓ | — | ✓ |
| `PutObject` | — | — | ✓ | — | ✓ | ✓ |
| `DeleteObject` | — | — | ✓ | — | — | ✓ |
| `DeleteObjects` | — | — | ✓ | — | — | ✓ |
| `ListObjectsV2` | — | ✓ | ✓ | ✓ | — | ✓ |
| `ListObjects` | — | ✓ | ✓ | ✓ | — | ✓ |
| `ListObjectVersions` | — | ✓ | ✓ | ✓ | — | ✓ |
| `CreateMultipartUpload` | — | — | ✓ | — | ✓ | ✓ |
| `CompleteMultipartUpload` | — | — | ✓ | — | ✓ | ✓ |
| `AbortMultipartUpload` | — | — | ✓ | — | ✓ | ✓ |
| `ListMultipartUploads` | — | — | ✓ | ✓ | ✓ | ✓ |
| `UploadPart` | — | — | ✓ | — | ✓ | ✓ |
| `UploadPartCopy` | — | — | ✓ | — | ✓ | ✓ |
| `CopyObject` | — | — | ✓ | — | ✓ | ✓ |
| `PostObject` | — | — | ✓ | — | ✓ | ✓ |
| `HeadBucket` | — | — | ✓ | ✓ | ✓ | — |
| `CreateBucket` | — | — | ✓ | — | — | — |
| `GetBucketLifecycleConfiguration` | — | — | ✓ | ✓ | ✓ | — |
| `PutBucketLifecycleConfiguration` | — | — | ✓ | — | — | — |
| `PutBucketCORS` | — | — | ✓ | — | — | — |
| `PutBucketVersioning` | — | — | ✓ | — | — | — |
| `GetBucketVersioning` | — | — | ✓ | ✓ | ✓ | — |
| `GetBucketLocation` | — | — | ✓ | ✓ | ✓ | — |
| `GetObjectTagging` | ✓ | — | ✓ | ✓ | — | ✓ |
| `PutObjectTagging` | — | — | ✓ | — | ✓ | ✓ |
| `DeleteObjectTagging` | — | — | ✓ | — | — | ✓ |

Note that the `CopyObject` and `UploadPartCopy` actions require roles that have both Download and Upload [permissions](https://docs.nebius.com/iam/authorization/roles.md#object-storage).

> For example, to be able to copy an object, the user needs to have one of the following roles or combinations of roles:
>
> * `storage.viewer` + `storage.uploader`
> * `storage.object-viewer` + `storage.uploader`
> * `storage.editor`
> * `storage.object-editor`
