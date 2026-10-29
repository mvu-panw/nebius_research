# Creating and launching data transfers in Object Storage

Source: https://docs.nebius.com/object-storage/transfer/launch

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating and launching data transfers in Object Storage

Data transfers allow you to move data between buckets when you want to migrate or replicate it. For more information, see [How data transfers work](https://docs.nebius.com/object-storage/transfer/overview.md).

## Prerequisites

1. Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. Make sure that your account has access to the buckets. Prepare credentials for the buckets, for example, access and secret keys. For more information, see [Access to buckets for data transfers](https://docs.nebius.com/object-storage/transfer/access.md).

   > [!NOTE]
   >
   > To transfer data from S3-compatible storage to a [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems), create a [filesystem bucket](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md) attached to the filesystem first. Then, use the filesystem bucket as the destination bucket in the data transfer.

3. Configure the web console or a developer tool to work in the correct project:

   **Web console**

   In the [web console](https://console.nebius.com), select the project that contains the destination bucket (if it's in Nebius AI Cloud) or the source bucket (if the destination is in an external storage service).

   **CLI**

   1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
   2. Get the ID of the project that contains the destination bucket (if it's in Nebius AI Cloud) or the source bucket (if the destination is in an external storage service):

      ```bash theme={null}
      nebius storage bucket get <bucket_ID> --format jsonpath='{.metadata.parent_id}'
      ```

   **Terraform**

   1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
   2. Save to a [local variable](https://developer.hashicorp.com/terraform/language/values/locals) the ID of the project that contains the destination bucket (if it's in Nebius AI Cloud) or the source bucket (if the destination is in an external storage service):

      ```hcl theme={null}
      data "nebius_storage_v1_bucket" "nebius_bucket" {
        id = "<source_or_destination_bucket_ID>"
      }

      locals {
        transfer_project_id = data.nebius_storage_v1_bucket.nebius_bucket.parent_id
      }
      ```

## How to launch a data transfer

**Web console**

1. In the sidebar, go to  **Storage** → **Data Transfer** and then click  **Create data transfer**.

2. Configure the data transfer:

   1. Specify its name.

   2. Select the [data transfer type](https://docs.nebius.com/object-storage/transfer/stop-condition.md#data-transfer-type-web-console): one-time transfer or replication.

   3. Configure the source and destination buckets:

   4. Specify the path to the buckets.

      In the **Bucket** field, you can optionally add [object key prefixes](https://docs.nebius.com/object-storage/transfer/key-prefixes.md) to the bucket name. In the source, you filter objects. In the destination, you overwrite prefixes of the source objects.

      Filesystem buckets are listed in the **Bucket** field together with other buckets.

   5. Set [credentials](https://docs.nebius.com/object-storage/transfer/access.md#credentials).

   6. Configure how the data transfer [handles destination objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md). See the settings under **Overwriting destination objects**, **Deleting destination objects** and **Unmanaged objects**.

   7. Configure [limits on request rate and bandwidth](https://docs.nebius.com/object-storage/transfer/limits.md). If you don't set them or set them to zero, the default values apply:

      * Request rate: 4000 requests per second.
      * Bandwidth: 50 GiB/s.

3. Click **Create transfer**.

**CLI**

1. Create a `transfer.json` file with the data transfer configuration and replace values in the file. Use one of the files below, depending on the source and destination storage services:

   > **Nebius AI Cloud to Nebius AI Cloud**
   >
   > ```json transfer.json theme={null}
   > {
   >   "metadata": {
   >     "name": "<transfer_name>",
   >     "parent_id": "<project_ID>"
   >   },
   >   "spec": {
   >     "source": {
   >       "nebius": {
   >         "region": "<Nebius_AI_Cloud_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         // Either:
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         },
   >         // Or, for anonymous access:
   >         // "anonymous": {}
   >       },
   >       "prefix": "<source_object_key_prefix>" // Optional
   >     },
   >     "destination": {
   >       "nebius": {
   >         "region": "<Nebius_AI_Cloud_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         }
   >       },
   >       "prefix": "<destination_object_key_prefix>" // Optional
   >     },
   >
   >     // Either:
   >     "after_one_iteration": {},
   >     // Or:
   >     // "after_n_empty_iterations": {
   >     //   "empty_iterations_threshold": <number_of_empty_iterations>
   >     // },
   >     // Or:
   >     // "infinite": {},
   >     //
   >     // "inter_iteration_interval": "<HhMmSs>", // For example, "1h20m40s"
   >
   >     "overwrite_strategy": "<NEVER|IF_NEWER>",
   >     "enable_deletes_in_destination": true|false,
   >     "touch_unmanaged": true|false,  // Optional
   >     "limiters": {
   >       "requests_per_second": <request_rate_limit>,
   >       "bandwidth_bytes_per_second": <bandwidth_limit>
   >     }
   >   }
   > }
   > ```

   > **Nebius AI Cloud to another storage service**
   >
   > ```json transfer.json theme={null}
   > {
   >   "metadata": {
   >     "name": "<transfer_name>",
   >     "parent_id": "<project_ID>"
   >   },
   >   "spec": {
   >     "source": {
   >       "nebius": {
   >         "region": "<Nebius_AI_Cloud_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         // Either:
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         },
   >         // Or, for anonymous access:
   >         // "anonymous": {}
   >       },
   >       "prefix": "<source_object_key_prefix>" // Optional
   >     },
   >     "destination": {
   >       "s3_compatible": {
   >         "endpoint": "<storage_service_endpoint>",
   >         "region": "<bucket_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         // Either:
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         },
   >         // Or, for anonymous access:
   >         // "anonymous": {}
   >       },
   >       "prefix": "<destination_object_key_prefix>" // Optional
   >     },
   >
   >     // Either:
   >     "after_one_iteration": {},
   >     // Or:
   >     // "after_n_empty_iterations": {
   >     //   "empty_iterations_threshold": <number_of_empty_iterations>
   >     // },
   >     // Or:
   >     // "infinite": {},
   >     //
   >     // "inter_iteration_interval": "<HhMmSs>", // For example, "1h20m40s"
   >
   >     "overwrite_strategy": "<NEVER|IF_NEWER>",
   >     "enable_deletes_in_destination": true|false,
   >     "touch_unmanaged": true|false,  // Optional
   >     "limiters": {
   >       "requests_per_second": <request_rate_limit>,
   >       "bandwidth_bytes_per_second": <bandwidth_limit>
   >     }
   >   }
   > }
   > ```

   > **Azure Blob Storage to Nebius AI Cloud**
   >
   > ```json transfer.json theme={null}
   > {
   >   "metadata": {
   >     "name": "<transfer_name>",
   >     "parent_id": "<project_ID>"
   >   },
   >   "spec": {
   >     "source": {
   >       "azure_blob_storage": {
   >         "endpoint": "<Azure_Blob_Storage_endpoint>",
   >         "container_name": "<container_name>",
   >
   >         // Either:
   >         "azure_storage_account": {
   >           "account_name": "<Azure_storage_account_name>",
   >           "access_key": "<access_key>"
   >         },
   >         // Or, for anonymous access:
   >         // "anonymous": {}
   >       },
   >       "prefix": "<source_object_key_prefix>" // Optional
   >     },
   >     "destination": {
   >       "nebius": {
   >         "region": "<Nebius_AI_Cloud_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         }
   >       },
   >       "prefix": "<destination_object_key_prefix>" // Optional
   >     },
   >
   >     // Either:
   >     "after_one_iteration": {},
   >     // Or:
   >     // "after_n_empty_iterations": {
   >     //   "empty_iterations_threshold": <number_of_empty_iterations>
   >     // },
   >     // Or:
   >     // "infinite": {},
   >     //
   >     // "inter_iteration_interval": "<HhMmSs>", // For example, "1h20m40s"
   >
   >     "overwrite_strategy": "<NEVER|IF_NEWER>",
   >     "enable_deletes_in_destination": true|false,
   >     "touch_unmanaged": true|false,  // Optional
   >     "limiters": {
   >       "requests_per_second": <request_rate_limit>,
   >       "bandwidth_bytes_per_second": <bandwidth_limit>
   >     }
   >   }
   > }
   > ```

   > **Another storage service to Nebius AI Cloud**
   >
   > ```json transfer.json theme={null}
   > {
   >   "metadata": {
   >     "name": "<transfer_name>",
   >     "parent_id": "<project_ID>"
   >   },
   >   "spec": {
   >     "source": {
   >       "s3_compatible": {
   >         "endpoint": "<storage_service_endpoint>",
   >         "region": "<bucket_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         // Either:
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         },
   >         // Or, for anonymous access:
   >         // "anonymous": {}
   >       },
   >       "prefix": "<source_object_key_prefix>" // Optional
   >     },
   >     "destination": {
   >       "nebius": {
   >         "region": "<Nebius_AI_Cloud_region>",
   >         "bucket_name": "<bucket_name>",
   >
   >         "access_key": {
   >           "access_key_id": "<access_key>",
   >           "secret_access_key": "<secret_key>"
   >         }
   >       },
   >       "prefix": "<destination_object_key_prefix>" // Optional
   >     },
   >
   >     // Either:
   >     "after_one_iteration": {},
   >     // Or:
   >     // "after_n_empty_iterations": {
   >     //   "empty_iterations_threshold": <number_of_empty_iterations>
   >     // },
   >     // Or:
   >     // "infinite": {},
   >     //
   >     // "inter_iteration_interval": "<HhMmSs>", // For example, "1h20m40s"
   >
   >     "overwrite_strategy": "<NEVER|IF_NEWER>",
   >     "enable_deletes_in_destination": true|false,
   >     "touch_unmanaged": true|false,  // Optional
   >     "limiters": {
   >       "requests_per_second": <request_rate_limit>,
   >       "bandwidth_bytes_per_second": <bandwidth_limit>
   >     }
   >   }
   > }
   > ```

   For details, see:

   * [Examples](#examples)
   * [Reference](https://docs.nebius.com/cli/reference/storage/transfer/create.md) for the `nebius storage transfer create` CLI command
   * [Transfer configuration](https://docs.nebius.com/object-storage/transfer/stop-condition.md)

2. Launch the data transfer:

   ```bash theme={null}
   nebius storage transfer create \
     --parent-id <project_ID> \
     --file transfer.json
   ```

**Terraform**

1. Add a data transfer block to your Terraform configuration.

   We recommend using Terraform [ephemeral](https://docs.nebius.com/terraform-provider/sensitive-values.md#ephemerals-for-sensitive-values) resource blocks and write-only `sensitive` fields when passing access credentials for buckets. You can also use regular fields, but the credential values are then stored in Terraform plan and state files, which is less secure.

   The following examples show how to launch a data transfer for different sources and destinations:

   > **Nebius AI Cloud to Nebius AI Cloud**
   >
   > ```hcl theme={null}
   > ephemeral "nebius_iam_v2_access_key_secret" "ak_secret" {
   >   aws_access_key_id = "<access_key>"
   > }
   >
   > resource "nebius_storage_v1_transfer" "my_transfer" {
   >   name      = "<transfer_name>"
   >   parent_id = local.transfer_project_id
   >
   >   source {
   >     nebius {
   >       region      = "<Nebius_AI_Cloud_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       # Either:
   >       access_key {
   >         access_key_id     = "<access_key>"
   >       }
   >       # Or, for anonymous access:
   >       # anonymous {}
   >     }
   >     # Optional:
   >     prefix = "<source_object_key_prefix>"
   >   }
   >
   >   destination {
   >     nebius {
   >       region      = "<Nebius_AI_Cloud_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       access_key {
   >         access_key_id     = "<access_key>"
   >       }
   >     }
   >     # Optional:
   >     prefix = "<destination_object_key_prefix>"
   >   }
   >
   >   sensitive = {
   >     source = {
   >       nebius = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_iam_v2_access_key_secret.ak_secret.secret
   >         }
   >       }
   >     }
   >     destination = {
   >       nebius = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_iam_v2_access_key_secret.ak_secret.secret
   >         }
   >       }
   >     }
   >   }
   >
   >   # Either:
   >   after_one_iteration {}
   >   # Or:
   >   # after_n_empty_iterations {
   >   #   empty_iterations_threshold = <number_of_empty_iterations>
   >   # }
   >   # Or:
   >   # infinite {}
   >   #
   >   # inter_iteration_interval = "<HhMmSs>"  # Optional. For example, "1h20m40s"
   >
   >   overwrite_strategy            = "NEVER"  # Or "IF_NEWER"
   >   enable_deletes_in_destination = false
   >   touch_unmanaged               = false    # Optional
   >
   >   limiters {
   >     requests_per_second       = <request_rate_limit>
   >     bandwidth_bytes_per_second = <bandwidth_limit>
   >   }
   > }
   > ```

   > **Nebius AI Cloud to another storage service**
   >
   > ```hcl theme={null}
   > ephemeral "nebius_mysterybox_v1_secret_payload_entry" "transfer_secret" {
   >   secret_id = "<mysterybox_secret_ID>"
   >   key       = "<data_key_of_secret>"
   > }
   >
   > resource "nebius_storage_v1_transfer" "my_transfer" {
   >   name      = "<transfer_name>"
   >   parent_id = local.transfer_project_id
   >
   >   source {
   >     nebius {
   >       region      = "<Nebius_AI_Cloud_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       # Either:
   >       access_key {
   >         access_key_id     = "<source_access_key_ID>"
   >       }
   >       # Or, for anonymous access:
   >       # anonymous {}
   >     }
   >     # Optional:
   >     prefix = "<source_object_key_prefix>"
   >   }
   >
   >   destination {
   >     s3_compatible {
   >       endpoint    = "<storage_service_endpoint>"
   >       region      = "<bucket_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       # Either:
   >       access_key {
   >         access_key_id     = "<destination_access_key_ID>"
   >       }
   >       # Or, for anonymous access:
   >       # anonymous {}
   >     }
   >     # Optional:
   >     prefix = "<destination_object_key_prefix>"
   >   }
   >
   >   sensitive = {
   >     source = {
   >       nebius = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
   >         }
   >       }
   >     }
   >     destination = {
   >       s3_compatible = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
   >         }
   >       }
   >     }
   >   }
   >
   >   # Either:
   >   after_one_iteration {}
   >   # Or:
   >   # after_n_empty_iterations {
   >   #   empty_iterations_threshold = <number_of_empty_iterations>
   >   # }
   >   # Or:
   >   # infinite {}
   >   #
   >   # inter_iteration_interval       = "<HhMmSs>"  # Optional. For example, "1h20m40s"
   >
   >   overwrite_strategy             = "NEVER"     # Or "IF_NEWER"
   >   enable_deletes_in_destination  = false
   >   touch_unmanaged                = false       # Optional
   >
   >   limiters {
   >     requests_per_second      = <request_rate_limit>
   >     bandwidth_bytes_per_second = <bandwidth_limit>
   >   }
   > }
   > ```

   > **Azure Blob Storage to Nebius AI Cloud**
   >
   > ```hcl theme={null}
   > ephemeral "nebius_mysterybox_v1_secret_payload_entry" "transfer_secret" {
   >   secret_id = "<mysterybox_secret_ID>"
   >   key       = "<data_key_of_secret>"
   > }
   >
   > resource "nebius_storage_v1_transfer" "my_transfer" {
   >   name      = "<transfer_name>"
   >   parent_id = local.transfer_project_id
   >
   >   source {
   >     azure_blob_storage {
   >       endpoint       = "<Azure_Blob_Storage_endpoint>"
   >       container_name = "<container_name>"
   >
   >       # Either:
   >       azure_storage_account {
   >         account_name = "<Azure_storage_account_name>"
   >       }
   >       # Or, for anonymous access:
   >       # anonymous {}
   >     }
   >     # Optional:
   >     prefix = "<source_object_key_prefix>"
   >   }
   >
   >   destination {
   >     nebius {
   >       region      = "<Nebius_AI_Cloud_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       access_key {
   >         access_key_id     = "<destination_access_key_ID>"
   >       }
   >     }
   >     # Optional:
   >     prefix = "<destination_object_key_prefix>"
   >   }
   >
   >   sensitive = {
   >     source = {
   >       azure_blob_storage = {
   >         azure_storage_account = {
   >           access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
   >         }
   >       }
   >     }
   >     destination = {
   >       nebius = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
   >         }
   >       }
   >     }
   >   }
   >
   >   # Either:
   >   after_one_iteration {}
   >   # Or:
   >   # after_n_empty_iterations {
   >   #   empty_iterations_threshold = <number_of_empty_iterations>
   >   # }
   >   # Or:
   >   # infinite {}
   >   #
   >   # inter_iteration_interval       = "<HhMmSs>"  # Optional. For example, "1h20m40s"
   >
   >   overwrite_strategy             = "NEVER"     # Or "IF_NEWER"
   >   enable_deletes_in_destination  = false
   >   touch_unmanaged                = false       # Optional
   >
   >   limiters {
   >     requests_per_second      = <request_rate_limit>
   >     bandwidth_bytes_per_second = <bandwidth_limit>
   >   }
   > }
   > ```

   > **Another storage service to Nebius AI Cloud**
   >
   > ```hcl theme={null}
   > ephemeral "nebius_mysterybox_v1_secret_payload_entry" "transfer_secret" {
   >   secret_id = "<mysterybox_secret_ID>"
   >   key       = "<data_key_of_secret>"
   > }
   >
   > resource "nebius_storage_v1_transfer" "my_transfer" {
   >   name      = "<transfer_name>"
   >   parent_id = local.transfer_project_id
   >
   >   source {
   >     s3_compatible {
   >       endpoint    = "<storage_service_endpoint>"
   >       region      = "<bucket_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       # Either:
   >       access_key {
   >         access_key_id     = "<source_access_key_ID>"
   >       }
   >       # Or, for anonymous access:
   >       # anonymous {}
   >     }
   >     # Optional:
   >     prefix = "<source_object_key_prefix>"
   >   }
   >
   >   destination {
   >     nebius {
   >       region      = "<Nebius_AI_Cloud_region>"
   >       bucket_name = "<bucket_name>"
   >
   >       access_key {
   >         access_key_id     = "<destination_access_key_ID>"
   >       }
   >     }
   >     # Optional:
   >     prefix = "<destination_object_key_prefix>"
   >   }
   >
   >   sensitive = {
   >     source = {
   >       s3_compatible = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
   >         }
   >       }
   >     }
   >     destination = {
   >       nebius = {
   >         access_key = {
   >           secret_access_key = ephemeral.nebius_mysterybox_v1_secret_payload_entry.transfer_secret.data.string_value
   >         }
   >       }
   >     }
   >   }
   >
   >   # Either:
   >   after_one_iteration {}
   >   # Or:
   >   # after_n_empty_iterations {
   >   #   empty_iterations_threshold = <number_of_empty_iterations>
   >   # }
   >   # Or:
   >   # infinite {}
   >   #
   >   # inter_iteration_interval       = "<HhMmSs>"  # Optional. For example, "1h20m40s"
   >
   >   overwrite_strategy             = "NEVER"     # Or "IF_NEWER"
   >   enable_deletes_in_destination  = false
   >   touch_unmanaged                = false       # Optional
   >
   >   limiters {
   >     requests_per_second      = <request_rate_limit>
   >     bandwidth_bytes_per_second = <bandwidth_limit>
   >   }
   > }
   > ```

   > [!NOTE]
   >
   > The examples use the same secret for the source and destination. If needed, provide different secrets for each side.

   For details, see:

   * [Examples](#examples)
   * [Reference](https://docs.nebius.com/terraform-provider/reference/resources/storage_v1_transfer.md) for the `nebius_storage_v1_transfer` resource
   * [Transfer configuration](https://docs.nebius.com/object-storage/transfer/stop-condition.md)

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

## Examples

### One-time transfer between Nebius AI Cloud regions

The following configuration examples show how to create a one-time transfer (a transfer that stops after one iteration) from a bucket in the `eu-north1` region to a bucket in the `us-central1` region:

**Web console**

Create the data transfer in the project in `us-central1` where the destination bucket is located:

* **Type**: One-time transfer

* **Source**: Nebius

  * **Region**: `eu-north1`
  * **Bucket name** (example): `source_bucket`
  * **Credentials**: [Access and secret keys](https://docs.nebius.com/iam/service-accounts/access-keys.md)

* **Destination**: Nebius

  * **Region**: `us-central1`
  * **Bucket name** (example): `destination_bucket`
  * **Credentials**: Access and secret keys
  * **Overwriting destination objects**: Overwrite if source is newer
  * **Deleting destination objects**: Do not delete

**CLI**

The `.metadata.parent_id` parameter should be the ID of the project in `us-central1` that contains the destination bucket.

```json theme={null}
{
  "metadata": {
    "name": "eu-north1-to-us-central1-transfer",
    "parent_id": "project-***"
  },
  "spec": {
    "source": {
      "nebius": {
        "region": "eu-north1",
        "bucket_name": "source_bucket",
        "access_key": {
          "access_key_id": "****",
          "secret_access_key": "****"
        }
      }
    },
    "destination": {
      "nebius": {
        "region": "us-central1",
        "bucket_name": "destination_bucket",
        "access_key": {
          "access_key_id": "****",
          "secret_access_key": "****"
        }
      }
    },
    "after_one_iteration": {},
    "overwrite_strategy": "IF_NEWER",
    "enable_deletes_in_destination": false
  }
}
```

**Terraform**

The `parent_id` parameter should be the ID of the project in `us-central1` that contains the destination bucket.

```hcl theme={null}
ephemeral "nebius_iam_v2_access_key_secret" "ak_secret" {
  aws_access_key_id = "****"
}

resource "nebius_storage_v1_transfer" "my_transfer" {
  name      = "eu-north1-to-us-central1-transfer"
  parent_id = "project-***"

  source {
    nebius {
      region      = "eu-north1"
      bucket_name = "source_bucket"
      access_key {
        access_key_id     = "****"
      }
    }
  }

  destination {
    nebius {
      region      = "us-central1"
      bucket_name = "destination_bucket"
      access_key {
        access_key_id     = "****"
      }
    }
  }

  sensitive = {
    source = {
      nebius = {
        access_key = {
          secret_access_key = ephemeral.nebius_iam_v2_access_key_secret.ak_secret.secret
        }
      }
    }
    destination = {
      nebius = {
        access_key = {
          secret_access_key = ephemeral.nebius_iam_v2_access_key_secret.ak_secret.secret
        }
      }
    }
  }

  after_one_iteration {}

  overwrite_strategy = "IF_NEWER"
  enable_deletes_in_destination = false
}
```

### Replication between Nebius AI Cloud regions

The following configuration examples show how to create a replication (a continuous transfer that you stop manually) from a bucket in the `us-central1` region to a bucket in the `eu-north1` region:

**Web console**

Create the data transfer in the project in `eu-north1` where the destination bucket is located:

* **Type**: Replication

* **Source**: Nebius

  * **Region**: `us-central1`
  * **Bucket name** (example): `primary_bucket`
  * **Credentials**: [Access and secret keys](https://docs.nebius.com/iam/service-accounts/access-keys.md)

* **Destination**: Nebius

  * **Region**: `eu-north1`
  * **Bucket name** (example): `secondary_bucket`
  * **Credentials**: Access and secret keys
  * **Overwriting destination objects**: Overwrite if source is newer
  * **Deleting destination objects**: Delete if not in source

**CLI**

The `.metadata.parent_id` parameter should be the ID of the project in `eu-north1` that contains the destination bucket.

```json theme={null}
{
  "metadata": {
    "name": "us-central1-to-eu-north1-backup",
    "parent_id": "project-***"
  },
  "spec": {
    "source": {
      "nebius": {
        "region": "us-central1",
        "bucket_name": "primary_bucket",
        "access_key": {
          "access_key_id": "****",
          "secret_access_key": "****"
        }
      }
    },
    "destination": {
      "nebius": {
        "region": "eu-north1",
        "bucket_name": "secondary_bucket",
        "access_key": {
          "access_key_id": "****",
          "secret_access_key": "****"
        }
      }
    },
    "infinite": {},
    "overwrite_strategy": "IF_NEWER",
    "enable_deletes_in_destination": true
  }
}
```

**Terraform**

The `parent_id` parameter should be the ID of the project in `eu-north1` that contains the destination bucket.

```hcl theme={null}
ephemeral "nebius_iam_v2_access_key_secret" "ak_secret" {
  aws_access_key_id = "****"
}

resource "nebius_storage_v1_transfer" "my_transfer" {
  name      = "us-central1-to-eu-north1-backup"
  parent_id = "project-***"

  source {
    nebius {
      region      = "us-central1"
      bucket_name = "primary_bucket"
      access_key {
        access_key_id     = "****"
      }
    }
  }

  destination {
    nebius {
      region      = "eu-north1"
      bucket_name = "secondary_bucket"
      access_key {
        access_key_id     = "****"
      }
    }
  }

  sensitive = {
    source = {
      nebius = {
        access_key = {
          secret_access_key = ephemeral.nebius_iam_v2_access_key_secret.ak_secret.secret
        }
      }
    }
    destination = {
      nebius = {
        access_key = {
          secret_access_key = ephemeral.nebius_iam_v2_access_key_secret.ak_secret.secret
        }
      }
    }
  }

  infinite {}
  overwrite_strategy = "IF_NEWER"
  enable_deletes_in_destination = true
}
```
