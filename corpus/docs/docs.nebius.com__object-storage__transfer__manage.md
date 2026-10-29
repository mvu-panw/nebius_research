# Managing data transfers

Source: https://docs.nebius.com/object-storage/transfer/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing data transfers

After you [create](https://docs.nebius.com/object-storage/transfer/launch.md) a data transfer, you can modify certain parameters, stop and resume it, or delete it.

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to modify a data transfer

You can modify certain parameters of an existing data transfer:

* Name
* [Credentials](https://docs.nebius.com/object-storage/transfer/access.md#credentials) and [object key prefixes](https://docs.nebius.com/object-storage/transfer/key-prefixes.md) for both the source and destination buckets
* [Transfer type or stop condition](https://docs.nebius.com/object-storage/transfer/stop-condition.md)
* Inter-iteration interval
* [Settings for handling destination objects](https://docs.nebius.com/object-storage/transfer/destination-objects.md)
* [Limits on request rate and bandwidth](https://docs.nebius.com/object-storage/transfer/limits.md)

Changes may require several minutes to take effect, during which the old settings could still be in use temporarily.

You cannot change the names or endpoints of the source and destination buckets of a data transfer.

To modify a data transfer:

**Web console**

1. In the sidebar, go to  **Storage** → **Data Transfer**.
2. Open the page of the data transfer that you want to modify.
3. Switch to the **Settings** tab.
4. Modify the parameters and click **Save changes**.

**CLI**

1. To get the data transfer ID, get a list of data transfers:
   ```bash theme={null}
   nebius storage transfer list
   ```
   The data transfer ID is returned in the `.metadata.id` parameter.
2. Update the data transfer. For example, to change credentials for the source bucket in Nebius AI Cloud, run the following command:

   ```bash theme={null}
   nebius storage transfer update <data_transfer_ID> \
     --source-nebius-access-key-access-key-id <access_key> \
     --source-nebius-access-key-secret-access-key <secret_key>
   ```

   For more information about the command parameters, see the [command reference](https://docs.nebius.com/cli/reference/storage/transfer/update.md).

**Terraform**

1. Modify the [nebius\_storage\_v1\_transfer](https://docs.nebius.com/terraform-provider/reference/resources/storage_v1_transfer.md) resource in your Terraform configuration.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

## How to stop and resume a data transfer

When you stop a data transfer, all ongoing uploads of objects and their parts are canceled. When you resume a data transfer, it starts a new [iteration](https://docs.nebius.com/object-storage/transfer/overview.md#iterations).

**Web console**

1. In the sidebar, go to  **Storage** → **Data Transfer**.
2. Next to the name of the data transfer, click  → **Stop** or **Resume**.
3. Confirm the action.

**CLI**

1. To get the data transfer ID, get a list of data transfers:
   ```bash theme={null}
   nebius storage transfer list
   ```
   The data transfer ID is returned in the `.metadata.id` parameter.

2. To stop the data transfer, run the following command:

   ```bash theme={null}
   nebius storage transfer stop <data_transfer_ID>
   ```

3. To resume the data transfer, run the following command:

   ```bash theme={null}
   nebius storage transfer resume <data_transfer_ID>
   ```

## How to delete a data transfer

When you delete a data transfer, Object Storage stops it before deletion. Transferred objects are not affected.

**Web console**

1. In the sidebar, go to  **Storage** → **Data Transfer**.
2. Next to the name of the data transfer, click  → **Delete**.
3. Confirm the action.

**CLI**

1. To get the data transfer ID, get a list of data transfers:
   ```bash theme={null}
   nebius storage transfer list
   ```
   The data transfer ID is returned in the `.metadata.id` parameter.
2. Delete the data transfer:

   ```bash theme={null}
   nebius storage transfer delete <data_transfer_ID>
   ```

**Terraform**

1. Remove the corresponding `nebius_storage_v1_transfer` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```
