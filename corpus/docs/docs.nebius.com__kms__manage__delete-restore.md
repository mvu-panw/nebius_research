# How to delete and restore keys in Key Management Service

Source: https://docs.nebius.com/kms/manage/delete-restore

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to delete and restore keys in Key Management Service

After you delete a key in Key Management Service (KMS), you can no longer use it for [cryptographic operations](https://docs.nebius.com/kms/types-operations.md#cryptographic-operations-and-use-cases). A deleted key is retained for 30 days. During that period, you can restore the key. Otherwise, the key is permanently removed after 30 days.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**Terraform**

> [!NOTE]
>
> Restoring deleted keys is possible only by using the web console, the CLI or the SDKs.

1. Initialize Terraform in the working directory:
   ```bash theme={null}
   terraform init
   ```
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

## How to delete a key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Select filters:

   * **Active**
   * **Symmetric keys** or **Asymmetric keys**

3. In the line of the required key, click  → **Delete**.

4. In the window that opens, confirm the deletion.

5. Click **Delete key**.

The key appears in the list of deleted keys.

**CLI**

To delete a key, run the `delete` command for your key type:

* Symmetric key:

  ```bash theme={null}
  nebius kms symmetric-key delete --id kmssymkey-e0***
  ```

* Asymmetric key:

  ```bash theme={null}
  nebius kms asymmetric-key delete --id kmsasymkey-e0***
  ```

The command output shows that the key is deleted: `status: {}`.

> **How to get the key ID**
>
> * Symmetric key:
>
>   ```bash theme={null}
>   nebius kms symmetric-key list
>   ```
>
> * Asymmetric key:
>
>   ```bash theme={null}
>   nebius kms asymmetric-key list
>   ```

**Terraform**

1. Remove the corresponding `nebius_kms_v1_symmetric_key` or `nebius_kms_v1_asymmetric_key` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

To delete a key, call `Delete` for your key type:

* Symmetric key:

  ```go theme={null}
  symDeleteService := sdk.Services().KMS().V1().
      SymmetricKey()
  symDeleteOperation, err := symDeleteService.Delete(
      ctx,
      &kms.DeleteSymmetricKeyRequest{
          Id: "kmssymkey-e0***",
      },
  )
  if err != nil {
      return fmt.Errorf("delete symmetric key: %w", err)
  }
  symDeleteOperation, err = symDeleteOperation.Wait(ctx)
  if err != nil {
      return fmt.Errorf("wait for operation: %w", err)
  }
  ```

* Asymmetric key:

  ```go theme={null}
  asymDeleteService := sdk.Services().KMS().V1().
      AsymmetricKey()
  asymDeleteOperation, err := asymDeleteService.Delete(
      ctx,
      &kms.DeleteAsymmetricKeyRequest{
          Id: "kmsasymkey-e0***",
      },
  )
  if err != nil {
      return fmt.Errorf("delete asymmetric key: %w", err)
  }
  asymDeleteOperation, err = asymDeleteOperation.Wait(ctx)
  if err != nil {
      return fmt.Errorf("wait for operation: %w", err)
  }
  ```

In the code, set `Id` to the ID of the key.

> **How to get the key ID**
>
> * Symmetric key:
>
>   ```go theme={null}
>   symListService := sdk.Services().KMS().V1().
>       SymmetricKey()
>   symListResponse, err := symListService.List(
>       ctx,
>       &kms.ListSymmetricKeysRequest{},
>   )
>   if err != nil {
>       return fmt.Errorf("list symmetric keys: %w", err)
>   }
>   fmt.Println(symListResponse)
>   ```
>
> * Asymmetric key:
>
>   ```go theme={null}
>   asymListService := sdk.Services().KMS().V1().
>       AsymmetricKey()
>   asymListResponse, err := asymListService.List(
>       ctx,
>       &kms.ListAsymmetricKeysRequest{},
>   )
>   if err != nil {
>       return fmt.Errorf("list asymmetric keys: %w", err)
>   }
>   fmt.Println(asymListResponse)
>   ```

**Python SDK**

To delete a key, call `delete` for your key type:

* Symmetric key:

  ```python theme={null}
  service = kms.SymmetricKeyServiceClient(sdk)
  operation = await service.delete(
      kms.DeleteSymmetricKeyRequest(
          id="kmssymkey-e0***",
      ),
  )
  await operation.wait()
  ```

* Asymmetric key:

  ```python theme={null}
  service = kms.AsymmetricKeyServiceClient(sdk)
  operation = await service.delete(
      kms.DeleteAsymmetricKeyRequest(
          id="kmsasymkey-e0***",
      ),
  )
  await operation.wait()
  ```

In the code, set `id` to the ID of the key.

> **How to get the key ID**
>
> * Symmetric key:
>
>   ```python theme={null}
>   service = kms.SymmetricKeyServiceClient(sdk)
>   response = await service.list(
>       kms.ListSymmetricKeysRequest(),
>   )
>   print(response)
>   ```
>
> * Asymmetric key:
>
>   ```python theme={null}
>   service = kms.AsymmetricKeyServiceClient(sdk)
>   response = await service.list(
>       kms.ListAsymmetricKeysRequest(),
>   )
>   print(response)
>   ```

**JavaScript SDK**

To delete a key, call `delete` for your key type:

* Symmetric key:

  ```ts theme={null}
  const symDeleteService = new kms.SymmetricKeyService(sdk);
  const symDeleteOperation = await symDeleteService.delete(
    kms.DeleteSymmetricKeyRequest.create({
      id: "kmssymkey-e0***",
    }),
  ).result;
  await symDeleteOperation.wait();
  ```

* Asymmetric key:

  ```ts theme={null}
  const asymDeleteService = new kms.AsymmetricKeyService(sdk);
  const asymDeleteOperation = await asymDeleteService.delete(
    kms.DeleteAsymmetricKeyRequest.create({
      id: "kmsasymkey-e0***",
    }),
  ).result;
  await asymDeleteOperation.wait();
  ```

In the code, set `id` to the ID of the key.

> **How to get the key ID**
>
> * Symmetric key:
>
>   ```ts theme={null}
>   const symListService = new kms.SymmetricKeyService(sdk);
>   const symListResponse = await symListService.list(
>     kms.ListSymmetricKeysRequest.create({}),
>   ).result;
>   console.log(symListResponse);
>   ```
>
> * Asymmetric key:
>
>   ```ts theme={null}
>   const asymListService = new kms.AsymmetricKeyService(sdk);
>   const asymListResponse = await asymListService.list(
>     kms.ListAsymmetricKeysRequest.create({}),
>   ).result;
>   console.log(asymListResponse);
>   ```

## How to restore a key

You can restore keys up to 30 days after their deletion.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Select filters:

   * **Deleted**
   * **Symmetric keys** or **Asymmetric keys**

3. In the line of the required key, click **Restore**.

4. In the window that opens, confirm the restoration.

The key appears in the list of active keys and becomes available for cryptographic operations.

**CLI**

To restore a key, run the `undelete` command for your key type:

* Symmetric key:

  ```bash theme={null}
  nebius kms symmetric-key undelete --id kmssymkey-e0*** --name <new_key_name>
  ```

* Asymmetric key:

  ```bash theme={null}
  nebius kms asymmetric-key undelete --id kmsasymkey-e0*** --name <new_key_name>
  ```

> **How to get the key ID**
>
> Use the `--show-scheduled-for-deletion` parameter in the `list` command to see keys scheduled for deletion:
>
> * Symmetric key:
>
>   ```bash theme={null}
>   nebius kms symmetric-key list --show-scheduled-for-deletion
>   ```
>
> * Asymmetric key:
>
>   ```bash theme={null}
>   nebius kms asymmetric-key list --show-scheduled-for-deletion
>   ```

In the `undelete` command, use the `--name` parameter to restore the key with a new name. This is needed when you have another key that reserves the original name. The parameter allows you to have different keys with unique names.

The command output shows that the key is active again: `status.state: ACTIVE`.

**Go SDK**

To restore a key, call `Undelete` for your key type:

* Symmetric key:

  ```go theme={null}
  symUndeleteService := sdk.Services().KMS().V1().
      SymmetricKey()
  symUndeleteOperation, err := symUndeleteService.Undelete(
      ctx,
      &kms.UndeleteSymmetricKeyRequest{
          Id: "kmssymkey-e0***",
          Name: "<new_key_name>",
      },
  )
  if err != nil {
      return fmt.Errorf("undelete symmetric key: %w", err)
  }
  symUndeleteOperation, err = symUndeleteOperation.Wait(ctx)
  if err != nil {
      return fmt.Errorf("wait for operation: %w", err)
  }
  symUndeleteResult, err := symUndeleteService.Get(
      ctx,
      &kms.GetSymmetricKeyRequest{
          Id: symUndeleteOperation.ResourceID(),
      },
  )
  if err != nil {
      return fmt.Errorf("get key: %w", err)
  }
  fmt.Println(symUndeleteResult)
  ```

* Asymmetric key:

  ```go theme={null}
  asymUndeleteService := sdk.Services().KMS().V1().
      AsymmetricKey()
  asymUndeleteOperation, err := asymUndeleteService.Undelete(
      ctx,
      &kms.UndeleteAsymmetricKeyRequest{
          Id: "kmsasymkey-e0***",
          Name: "<new_key_name>",
      },
  )
  if err != nil {
      return fmt.Errorf("undelete asymmetric key: %w", err)
  }
  asymUndeleteOperation, err = asymUndeleteOperation.Wait(ctx)
  if err != nil {
      return fmt.Errorf("wait for operation: %w", err)
  }
  asymUndeleteResult, err := asymUndeleteService.Get(
      ctx,
      &kms.GetAsymmetricKeyRequest{
          Id: asymUndeleteOperation.ResourceID(),
      },
  )
  if err != nil {
      return fmt.Errorf("get key: %w", err)
  }
  fmt.Println(asymUndeleteResult)
  ```

In the code, specify:

* `Id`: ID of the deleted key.
* `Name` (optional): New name of the key. This is needed when you have another key that reserves the original name. To keep the original name, omit `Name`.

> **How to get the key ID**
>
> Set `ShowScheduledForDeletion` to `true` in the list request to see keys scheduled for deletion:
>
> * Symmetric key:
>
>   ```go theme={null}
>   symScheduledListService := sdk.Services().KMS().V1().
>       SymmetricKey()
>   symScheduledListResponse, err := symScheduledListService.List(
>       ctx,
>       &kms.ListSymmetricKeysRequest{
>           ShowScheduledForDeletion: true,
>       },
>   )
>   if err != nil {
>       return fmt.Errorf("list symmetric keys: %w", err)
>   }
>   fmt.Println(symScheduledListResponse)
>   ```
>
> * Asymmetric key:
>
>   ```go theme={null}
>   asymScheduledListService := sdk.Services().KMS().V1().
>       AsymmetricKey()
>   asymScheduledListResponse, err := asymScheduledListService.List(
>       ctx,
>       &kms.ListAsymmetricKeysRequest{
>           ShowScheduledForDeletion: true,
>       },
>   )
>   if err != nil {
>       return fmt.Errorf("list asymmetric keys: %w", err)
>   }
>   fmt.Println(asymScheduledListResponse)
>   ```

**Python SDK**

To restore a key, call `undelete` for your key type:

* Symmetric key:

  ```python theme={null}
  service = kms.SymmetricKeyServiceClient(sdk)
  operation = await service.undelete(
      kms.UndeleteSymmetricKeyRequest(
          id="kmssymkey-e0***",
          name="<new_key_name>",
      ),
  )
  await operation.wait()
  result = await service.get(
      kms.GetSymmetricKeyRequest(id=operation.resource_id),
  )
  print(result)
  ```

* Asymmetric key:

  ```python theme={null}
  service = kms.AsymmetricKeyServiceClient(sdk)
  operation = await service.undelete(
      kms.UndeleteAsymmetricKeyRequest(
          id="kmsasymkey-e0***",
          name="<new_key_name>",
      ),
  )
  await operation.wait()
  result = await service.get(
      kms.GetAsymmetricKeyRequest(id=operation.resource_id),
  )
  print(result)
  ```

In the code, specify:

* `id`: ID of the deleted key.
* `name` (optional): New name of the key. This is needed when you have another key that reserves the original name. To keep the original name, omit `name`.

> **How to get the key ID**
>
> Set `show_scheduled_for_deletion` to `True` in the list request to see keys scheduled for deletion:
>
> * Symmetric key:
>
>   ```python theme={null}
>   service = kms.SymmetricKeyServiceClient(sdk)
>   response = await service.list(
>       kms.ListSymmetricKeysRequest(
>           show_scheduled_for_deletion=True,
>       ),
>   )
>   print(response)
>   ```
>
> * Asymmetric key:
>
>   ```python theme={null}
>   service = kms.AsymmetricKeyServiceClient(sdk)
>   response = await service.list(
>       kms.ListAsymmetricKeysRequest(
>           show_scheduled_for_deletion=True,
>       ),
>   )
>   print(response)
>   ```

**JavaScript SDK**

To restore a key, call `undelete` for your key type:

* Symmetric key:

  ```ts theme={null}
  const symUndeleteService = new kms.SymmetricKeyService(sdk);
  const symUndeleteOperation = await symUndeleteService.undelete(
    kms.UndeleteSymmetricKeyRequest.create({
      id: "kmssymkey-e0***",
      name: "<new_key_name>",
    }),
  ).result;
  await symUndeleteOperation.wait();
  const symUndeleteResult = await symUndeleteService.get(
    kms.GetSymmetricKeyRequest.create({
      id: symUndeleteOperation.resourceId(),
    }),
  ).result;
  console.log(symUndeleteResult);
  ```

* Asymmetric key:

  ```ts theme={null}
  const asymUndeleteService =
    new kms.AsymmetricKeyService(sdk);
  const asymUndeleteOperation = await asymUndeleteService.undelete(
    kms.UndeleteAsymmetricKeyRequest.create({
      id: "kmsasymkey-e0***",
      name: "<new_key_name>",
    }),
  ).result;
  await asymUndeleteOperation.wait();
  const asymUndeleteResult = await asymUndeleteService.get(
    kms.GetAsymmetricKeyRequest.create({
      id: asymUndeleteOperation.resourceId(),
    }),
  ).result;
  console.log(asymUndeleteResult);
  ```

In the code, specify:

* `id`: ID of the deleted key.
* `name` (optional): New name of the key. This is needed when you have another key that reserves the original name. To keep the original name, omit `name`.

> **How to get the key ID**
>
> Set `showScheduledForDeletion` to `true` in the list request to see keys scheduled for deletion:
>
> * Symmetric key:
>
>   ```ts theme={null}
>   const symScheduledListService =
>     new kms.SymmetricKeyService(sdk);
>   const symScheduledListResponse = await symScheduledListService.list(
>     kms.ListSymmetricKeysRequest.create({
>       showScheduledForDeletion: true,
>     }),
>   ).result;
>   console.log(symScheduledListResponse);
>   ```
>
> * Asymmetric key:
>
>   ```ts theme={null}
>   const asymScheduledListService =
>     new kms.AsymmetricKeyService(sdk);
>   const asymScheduledListResponse = await asymScheduledListService.list(
>     kms.ListAsymmetricKeysRequest.create({
>       showScheduledForDeletion: true,
>     }),
>   ).result;
>   console.log(asymScheduledListResponse);
>   ```
