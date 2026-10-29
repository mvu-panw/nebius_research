# Access to buckets for data transfers

Source: https://docs.nebius.com/object-storage/transfer/access

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Access to buckets for data transfers

When you [create a data transfer](https://docs.nebius.com/object-storage/transfer/launch.md), you provide credentials that Object Storage uses to access the buckets. These credentials belong to accounts in storage services, such as [service accounts](https://docs.nebius.com/iam/overview.md#accounts-and-members) in Nebius AI Cloud. The accounts perform actions on buckets and objects during the data transfer, so these accounts must have sufficient permissions to perform these actions.

## Required permissions

Before you [launch a data transfer](https://docs.nebius.com/object-storage/transfer/launch.md), make sure that the service accounts at the source and destination have sufficient permissions to perform operations on buckets and objects. In Nebius AI Cloud, you can [add a service account to a group](https://docs.nebius.com/iam/authorization/groups/members.md) and either assign this group [roles](https://docs.nebius.com/iam/authorization/roles.md) with necessary permissions listed below, or set up [bucket policies](https://docs.nebius.com/object-storage/buckets/bucket-policy.md) for the group.

The table below lists the actions that must be permitted and the minimum roles that grant these permissions to accounts:

| Transfer side | Actions | Minimum Nebius AI Cloud roles |
| - | - | - |
| Source | `ListObjects`, `HeadObject`, `GetObject` | `storage.object-lister` + `storage.object-viewer` (combination) or `storage.viewer` (single role) |
| Destination | `HeadObject`, `PutObject`, `CreateMultipartUpload`, `UploadPart`, `CompleteMultipartUpload` | `storage.object-viewer` + `storage.uploader` (combination) or `storage.object-editor` (single role) |
| Destination (if [deleting destination objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md#deleting-destination-objects) is enabled) | Destination actions listed above, plus `ListObjects` and `DeleteObject` | `storage.object-editor` (single role) or `storage.editor` (single role) |

For more information about these actions, see [Iterations](https://docs.nebius.com/object-storage/transfer/overview.md#iterations).

## Credentials

Provide credentials when you create a data transfer. The account (such as a [service account](https://docs.nebius.com/iam/overview.md#accounts-and-members)) uses the credentials to access buckets and objects and operate with them.

### Credentials for S3-compatible storage services

For a bucket in Object Storage or another S3-compatible storage service, the required credentials are a pair of keys called *access and secret keys*, also known as *access key ID and secret access key*. Add these credentials to the transfer configuration when you [create](https://docs.nebius.com/object-storage/transfer/launch.md) or [modify](https://docs.nebius.com/object-storage/transfer/manage.md) a data transfer:

**Web console**

In the [web console](https://console.nebius.com/datatransfer), settings for credentials appear under **Source** and **Destination** when you create or modify a data transfer. To enter the access and secret keys, under **Credentials**, select **Access and secret keys**.

**CLI**

Use `.{source,destination}.{nebius,s3_compatible}.access_key` to add credentials. For example, when you're transferring data from a Nebius AI Cloud bucket (`.spec.source.nebius`) to an S3-compatible bucket (`.spec.destination.s3_compatible`), add credentials like this:

```json theme={null}
{
  "spec": {
    "source": {
      "nebius": {
        "access_key": {
          "access_key_id": "<source_access_key_ID>",
          "secret_access_key": "<source_secret_access_key>"
        },
        // Other source parameters
      }
    },
    "destination": {
      "s3_compatible": {
        "access_key": {
          "access_key_id": "<destination_access_key_ID>",
          "secret_access_key": "<destination_secret_access_key>"
        },
        // Other destination parameters
      }
    },
    // Other parameters
  }
}
```

Set the values of `.spec.{source,destination}.{nebius,s3_compatible}.access_key.{access_key_id,secret_access_key}` securely, for example, by using environment variables.

**Terraform**

Use `{source,destination}.{nebius,s3_compatible}.access_key` to add credentials. For example, when you're transferring data from a Nebius AI Cloud bucket (`source.nebius`) to an S3-compatible bucket (`destination.s3_compatible`), add credentials like this:

```hcl theme={null}
ephemeral "nebius_mysterybox_v1_secret_payload_entry" "transfer_secret" {
  secret_id = "<mysterybox_secret_ID>"
  key       = "<data_key_of_secret>"
}

resource "nebius_storage_v1_transfer" "example" {
  source {
    nebius {
      access_key {
        access_key_id = var.source_access_key_id
      }
    }
    # Other source parameters
  }

  destination {
    s3_compatible {
      access_key {
        access_key_id = var.destination_access_key_id
      }
    }
    # Other destination parameters
  }

  sensitive = {
    source = {
      nebius = {
        access_key = {
          secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
        }
      }
    }
    destination = {
      s3_compatible = {
        access_key = {
          secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
        }
      }
    }
  }

  # Other parameters
}
```

For `nebius_storage_v1_transfer`, we recommend retrieving credentials for storage services through Terraform ephemeral resource blocks and passing them through write-only `sensitive` fields so they aren't stored in the Terraform state. For more information, see [Working with sensitive values](https://docs.nebius.com/terraform-provider/sensitive-values.md).

You can also use regular [input variables](https://developer.hashicorp.com/terraform/language/values/variables), but the credential values are then stored in Terraform plan and state files, which is less secure.

To get access and secret keys for an Object Storage bucket, [create access keys](https://docs.nebius.com/iam/service-accounts/access-keys.md) for a service account that has the [required permissions](#required-permissions).

### Credentials for source containers in Azure Blob Storage

If your source bucket ([container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#containers)) is in Azure Blob Storage, provide credentials of your [storage account in Azure](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview): the name and [access key](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage).

Do not confuse a storage account with an Azure account. The storage account is used for data objects, such as blobs or files.

**Web console**

In the [web console](https://console.nebius.com/datatransfer), settings for credentials appear under **Source** when you create or modify a data transfer and select **Azure** as the source type. To enter the storage account name and access key, under **Credentials**, select **Access key**.

**CLI**

Use parameters in `.source.azure_blob_storage`:

```json theme={null}
{
  "spec": {
    "source": {
      "azure_blob_storage": {
        "endpoint": "<storage_account_endpoint>",
        "container_name": "<container_name>",
        "azure_storage_account": {
          "account_name": "<storage_account_name>",
          "access_key": "<access_key>"
        }
      }
    },
    // Destination and other parameters
  }
}
```

* `.spec.source.azure_blob_storage.endpoint`: Endpoint of the Azure storage account in the format `https://<storage_account_name>.blob.core.windows.net`.
* `.spec.source.azure_blob_storage.container_name`: Name of the source container in Azure Blob Storage.
* `.spec.source.azure_blob_storage.azure_storage_account.account_name`: Name of the storage account.
* `.spec.source.azure_blob_storage.azure_storage_account.access_key`: Access key from Azure that the storage account uses for authentication. Set this value securely, for example, by using environment variables.

**Terraform**

Use arguments in `source.azure_blob_storage`:

```hcl theme={null}
ephemeral "nebius_mysterybox_v1_secret_payload_entry" "transfer_secret" {
  secret_id = "<mysterybox_secret_ID>"
  key       = "<data_key_of_secret>"
}

resource "nebius_storage_v1_transfer" "example" {
  source {
    azure_blob_storage {
      endpoint       = var.source_storage_account_endpoint
      container_name = var.source_container_name

      azure_storage_account {
        account_name = var.source_storage_account_name
      }
    }
  }

  sensitive = {
    source = {
      azure_blob_storage = {
        azure_storage_account = {
          access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
        }
      }
    }
  }
  # Destination and other parameters
}
```

* `source.azure_blob_storage.endpoint`: Endpoint of the Azure storage account in the format `https://<storage_account_name>.blob.core.windows.net`.
* `source.azure_blob_storage.container_name`: Name of the source container in Azure Blob Storage.
* `source.azure_blob_storage.azure_storage_account.account_name`: Name of the storage account.
* `source.azure_blob_storage.azure_storage_account.access_key`: Access key from Azure that the storage account uses for authentication. For `nebius_storage_v1_transfer`, we recommend retrieving this key through Terraform ephemeral resource blocks and passing it through write-only `sensitive` fields. For more information, see [Working with sensitive values](https://docs.nebius.com/terraform-provider/sensitive-values.md). You can also use an [input variable](https://developer.hashicorp.com/terraform/language/values/variables), but the key value is then stored in Terraform plan and state files, which is less secure.

### Anonymous access

If a bucket has anonymous access enabled, meaning that all unauthenticated users have the [required permissions](#required-permissions) in the bucket, you can skip providing credentials:

**Web console**

In the [web console](https://console.nebius.com/datatransfer), settings for credentials appear under **Source** when you create or modify a data transfer. To set up anonymous access, under **Credentials**, select **Anonymous**.

**CLI**

Use `{"anonymous": {}}` in `.spec.source.{nebius,s3_compatible,azure_blob_storage}` or `.spec.destination.s3_compatible`. For example, when you're transferring data from a Nebius AI Cloud bucket (`.spec.source.nebius`), set up anonymous access like this:

```json theme={null}
{
  "spec": {
    "source": {
      "nebius": {
        "anonymous": {},
        // Other source parameters
      }
    },
    // Destination and other parameters
  }
}
```

**Terraform**

Use `anonymous {}` in `source.{nebius,s3_compatible,azure_blob_storage}` or `destination.s3_compatible`. For example, when you're transferring data from a Nebius AI Cloud bucket (`source.nebius`), set up anonymous access like this:

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example" {
  source {
    nebius {
      anonymous {}
    }
  }
  # Destination and other parameters
}
```

Destination buckets in Nebius AI Cloud don't support the anonymous access setting because Object Storage doesn't allow anonymous write access.
