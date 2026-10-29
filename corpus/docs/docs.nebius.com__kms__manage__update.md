# How to update keys in Key Management Service

Source: https://docs.nebius.com/kms/manage/update

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to update keys in Key Management Service

You can update the name and description of [symmetric and asymmetric keys](https://docs.nebius.com/kms/types-operations.md#symmetric-and-asymmetric-keys) in Key Management Service (KMS). For symmetric keys, you can also update the key rotation period. You can't update the algorithm of an existing key. [Create a new key](https://docs.nebius.com/kms/manage/create.md) if you need to use a different algorithm.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
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

> [!WARNING]
>
> Terraform does not support updating keys. If you use Terraform to update a key, Terraform replaces the key with a new one.

## How to update a symmetric key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Make sure that **Symmetric keys** and **Active** are selected in the filters.

3. In the line of the required key, click  → **Settings**.

4. Update the key settings:

   * **Name**: New key name.
   * **Rotation period**: New period after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). When a key is rotated, KMS generates a new key version and immediately sets it as the default version.
   * **Description**: New key description.

5. Click **Save changes**.

**CLI**

1. List symmetric keys:

   ```bash theme={null}
   nebius kms symmetric-key list
   ```

   In the output, copy the ID of the required symmetric key.

2. Update the key:

   ```bash theme={null}
   nebius kms symmetric-key update \
      --id <symmetric_key_ID> \
      --name <new_key_name> \
      --description "<new_key_description>" \
      --rotation-period <new_period>
   ```

   The command contains the following parameters:

   * `--id`: ID of the symmetric key that you update.
   * `--name` (optional): New name of the key.
   * `--description` (optional): New description of the key.
   * `--rotation-period` (optional): New period after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation).

     When a key is rotated, KMS generates a new key version and immediately sets it as the default version.

     Specify the value in the `NhNmNs` format, for example, `24h` or `48h30m10s`. The minimum value is `86400s` (one day) and the maximum value is `315360000s` (3650 days). The default value is `7776000s` (90 days).

**Go SDK**

1. List symmetric keys:

   ```go theme={null}
   symListService := sdk.Services().KMS().V1().
       SymmetricKey()
   symListResponse, err := symListService.List(
       ctx,
       &kms.ListSymmetricKeysRequest{},
   )
   if err != nil {
       return fmt.Errorf("list symmetric keys: %w", err)
   }
   fmt.Println(symListResponse)
   ```

   In the output, copy the ID of the required symmetric key.

2. Update the key:

   ```go theme={null}
   symUpdateService := sdk.Services().KMS().V1().
       SymmetricKey()
   symUpdateKey, err := symUpdateService.Get(
       ctx,
       &kms.GetSymmetricKeyRequest{Id: "<symmetric_key_ID>"},
   )
   if err != nil {
       return fmt.Errorf("get key: %w", err)
   }
   symUpdateKey.Metadata.Name = "<new_key_name>"
   symUpdateKey.Spec.Description = "<new_key_description>"
   symUpdatePeriod, err := time.ParseDuration("<new_period>")
   if err != nil {
       return fmt.Errorf("parse rotation period: %w", err)
   }
   symUpdateKey.Spec.RotationPeriod = durationpb.New(
       symUpdatePeriod,
   )
   symUpdateOperation, err := symUpdateService.Update(
       ctx,
       &kms.UpdateSymmetricKeyRequest{
           Metadata: symUpdateKey.Metadata,
           Spec: symUpdateKey.Spec,
       },
   )
   if err != nil {
       return fmt.Errorf("update symmetric key: %w", err)
   }
   symUpdateOperation, err = symUpdateOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for operation: %w", err)
   }
   symUpdateResult, err := symUpdateService.Get(
       ctx,
       &kms.GetSymmetricKeyRequest{
           Id: symUpdateOperation.ResourceID(),
       },
   )
   if err != nil {
       return fmt.Errorf("get key: %w", err)
   }
   fmt.Println(symUpdateResult)
   ```

   The code gets the current key settings, replaces the ones that you specify and sends them back to KMS. In the code, specify:

   * `Id` in `GetSymmetricKeyRequest`: ID of the symmetric key that you update.
   * `Metadata.Name` (optional): New name of the key.
   * `Spec.Description` (optional): New description of the key.
   * `Spec.RotationPeriod` (optional): New period after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). The code parses the `<new_period>` value with `time.ParseDuration`. To keep the current period, remove the `time.ParseDuration` call and the `RotationPeriod` assignment.

     When a key is rotated, KMS generates a new key version and immediately sets it as the default version.

     Specify the value in the `NhNmNs` format, for example, `24h` or `48h30m10s`. The minimum value is `86400s` (one day) and the maximum value is `315360000s` (3650 days). The default value is `7776000s` (90 days).

   To keep a setting unchanged, omit it.

**Python SDK**

1. List symmetric keys:

   ```python theme={null}
   service = kms.SymmetricKeyServiceClient(sdk)
   response = await service.list(
       kms.ListSymmetricKeysRequest(),
   )
   print(response)
   ```

   In the output, copy the ID of the required symmetric key.

2. Update the key:

   ```python theme={null}
   service = kms.SymmetricKeyServiceClient(sdk)
   key = await service.get(
       kms.GetSymmetricKeyRequest(id="<symmetric_key_ID>"),
   )
   key.metadata.name = "<new_key_name>"
   key.spec.description = "<new_key_description>"
   key.spec.rotation_period = timedelta(hours=8760)
   operation = await service.update(
       kms.UpdateSymmetricKeyRequest(
           metadata=key.metadata,
           spec=key.spec,
       ),
   )
   await operation.wait()
   result = await service.get(
       kms.GetSymmetricKeyRequest(id=operation.resource_id),
   )
   print(result)
   ```

   The code gets the current key settings, replaces the ones that you specify and sends them back to KMS. In the code, specify:

   * `id` in `GetSymmetricKeyRequest`: ID of the symmetric key that you update.
   * `metadata.name` (optional): New name of the key.
   * `spec.description` (optional): New description of the key.
   * `spec.rotation_period` (optional): New period, as a `timedelta`, after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). The example sets 8760 hours. When a key is rotated, KMS generates a new key version and immediately sets it as the default version. The minimum value is one day and the maximum value is 3650 days.

   To keep a setting unchanged, omit it.

**JavaScript SDK**

1. List symmetric keys:

   ```ts theme={null}
   const symListService = new kms.SymmetricKeyService(sdk);
   const symListResponse = await symListService.list(
     kms.ListSymmetricKeysRequest.create({}),
   ).result;
   console.log(symListResponse);
   ```

   In the output, copy the ID of the required symmetric key.

2. Update the key:

   ```ts theme={null}
   const symUpdateService = new kms.SymmetricKeyService(sdk);
   const symUpdateKey = await symUpdateService.get(
     kms.GetSymmetricKeyRequest.create({ id: "<symmetric_key_ID>" }),
   ).result;
   symUpdateKey.metadata.name = "<new_key_name>";
   symUpdateKey.spec.description = "<new_key_description>";
   dayjs.extend(duration);
   symUpdateKey.spec.rotationPeriod = dayjs.duration(
     8760, "hours",
   );
   const symUpdateOperation = await symUpdateService.update(
     kms.UpdateSymmetricKeyRequest.create({
       metadata: symUpdateKey.metadata,
       spec: symUpdateKey.spec,
     }),
   ).result;
   await symUpdateOperation.wait();
   const symUpdateResult = await symUpdateService.get(
     kms.GetSymmetricKeyRequest.create({
       id: symUpdateOperation.resourceId(),
     }),
   ).result;
   console.log(symUpdateResult);
   ```

   The code gets the current key settings, replaces the ones that you specify and sends them back to KMS. In the code, specify:

   * `id` in `GetSymmetricKeyRequest`: ID of the symmetric key that you update.
   * `metadata.name` (optional): New name of the key.
   * `spec.description` (optional): New description of the key.
   * `spec.rotationPeriod` (optional): New period, as a Day.js duration, after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). The example sets 8760 hours. When a key is rotated, KMS generates a new key version and immediately sets it as the default version. The minimum value is one day and the maximum value is 3650 days.

   To keep a setting unchanged, omit it.

## How to update an asymmetric key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Make sure that **Asymmetric keys** and **Active** are selected in the filters.

3. In the line of the required key, click  → **Settings**.

4. Update the key settings:

   * **Name**: New key name.
   * **Description**: New key description.

5. Click **Save changes**.

**CLI**

1. List asymmetric keys:

   ```bash theme={null}
   nebius kms asymmetric-key list
   ```

   In the output, copy the ID of the required asymmetric key.

2. Update the key:

   ```bash theme={null}
   nebius kms asymmetric-key update \
      --id <asymmetric_key_ID> \
      --name <new_key_name> \
      --description "<new_key_description>"
   ```

   The command contains the following parameters:

   * `--id`: ID of the asymmetric key that you update.
   * `--name` (optional): New name of the key.
   * `--description` (optional): New description of the key.

**Go SDK**

1. List asymmetric keys:

   ```go theme={null}
   asymListService := sdk.Services().KMS().V1().
       AsymmetricKey()
   asymListResponse, err := asymListService.List(
       ctx,
       &kms.ListAsymmetricKeysRequest{},
   )
   if err != nil {
       return fmt.Errorf("list asymmetric keys: %w", err)
   }
   fmt.Println(asymListResponse)
   ```

   In the output, copy the ID of the required asymmetric key.

2. Update the key:

   ```go theme={null}
   asymUpdateService := sdk.Services().KMS().V1().
       AsymmetricKey()
   asymUpdateKey, err := asymUpdateService.Get(
       ctx,
       &kms.GetAsymmetricKeyRequest{Id: "<asymmetric_key_ID>"},
   )
   if err != nil {
       return fmt.Errorf("get key: %w", err)
   }
   asymUpdateKey.Metadata.Name = "<new_key_name>"
   asymUpdateKey.Spec.Description = "<new_key_description>"
   asymUpdateOperation, err := asymUpdateService.Update(
       ctx,
       &kms.UpdateAsymmetricKeyRequest{
           Metadata: asymUpdateKey.Metadata,
           Spec: asymUpdateKey.Spec,
       },
   )
   if err != nil {
       return fmt.Errorf("update asymmetric key: %w", err)
   }
   asymUpdateOperation, err = asymUpdateOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for operation: %w", err)
   }
   asymUpdateResult, err := asymUpdateService.Get(
       ctx,
       &kms.GetAsymmetricKeyRequest{
           Id: asymUpdateOperation.ResourceID(),
       },
   )
   if err != nil {
       return fmt.Errorf("get key: %w", err)
   }
   fmt.Println(asymUpdateResult)
   ```

   The code gets the current key settings, replaces the ones that you specify and sends them back to KMS. In the code, specify:

   * `Id` in `GetAsymmetricKeyRequest`: ID of the asymmetric key that you update.
   * `Metadata.Name` (optional): New name of the key.
   * `Spec.Description` (optional): New description of the key.

   To keep a setting unchanged, omit it.

**Python SDK**

1. List asymmetric keys:

   ```python theme={null}
   service = kms.AsymmetricKeyServiceClient(sdk)
   response = await service.list(
       kms.ListAsymmetricKeysRequest(),
   )
   print(response)
   ```

   In the output, copy the ID of the required asymmetric key.

2. Update the key:

   ```python theme={null}
   service = kms.AsymmetricKeyServiceClient(sdk)
   key = await service.get(
       kms.GetAsymmetricKeyRequest(id="<asymmetric_key_ID>"),
   )
   key.metadata.name = "<new_key_name>"
   key.spec.description = "<new_key_description>"
   operation = await service.update(
       kms.UpdateAsymmetricKeyRequest(
           metadata=key.metadata,
           spec=key.spec,
       ),
   )
   await operation.wait()
   result = await service.get(
       kms.GetAsymmetricKeyRequest(id=operation.resource_id),
   )
   print(result)
   ```

   The code gets the current key settings, replaces the ones that you specify and sends them back to KMS. In the code, specify:

   * `id` in `GetAsymmetricKeyRequest`: ID of the asymmetric key that you update.
   * `metadata.name` (optional): New name of the key.
   * `spec.description` (optional): New description of the key.

   To keep a setting unchanged, omit it.

**JavaScript SDK**

1. List asymmetric keys:

   ```ts theme={null}
   const asymListService = new kms.AsymmetricKeyService(sdk);
   const asymListResponse = await asymListService.list(
     kms.ListAsymmetricKeysRequest.create({}),
   ).result;
   console.log(asymListResponse);
   ```

   In the output, copy the ID of the required asymmetric key.

2. Update the key:

   ```ts theme={null}
   const asymUpdateService = new kms.AsymmetricKeyService(sdk);
   const asymUpdateKey = await asymUpdateService.get(
     kms.GetAsymmetricKeyRequest.create({ id: "<asymmetric_key_ID>" }),
   ).result;
   asymUpdateKey.metadata.name = "<new_key_name>";
   asymUpdateKey.spec.description = "<new_key_description>";
   const asymUpdateOperation = await asymUpdateService.update(
     kms.UpdateAsymmetricKeyRequest.create({
       metadata: asymUpdateKey.metadata,
       spec: asymUpdateKey.spec,
     }),
   ).result;
   await asymUpdateOperation.wait();
   const asymUpdateResult = await asymUpdateService.get(
     kms.GetAsymmetricKeyRequest.create({
       id: asymUpdateOperation.resourceId(),
     }),
   ).result;
   console.log(asymUpdateResult);
   ```

   The code gets the current key settings, replaces the ones that you specify and sends them back to KMS. In the code, specify:

   * `id` in `GetAsymmetricKeyRequest`: ID of the asymmetric key that you update.
   * `metadata.name` (optional): New name of the key.
   * `spec.description` (optional): New description of the key.

   To keep a setting unchanged, omit it.

## See also

* [Cryptographic operations with symmetric keys](https://docs.nebius.com/kms/cryptography/symmetric.md)
* [Cryptographic operations with asymmetric keys](https://docs.nebius.com/kms/cryptography/asymmetric.md)
