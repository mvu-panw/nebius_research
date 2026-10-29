# How to rotate symmetric keys in Key Management Service

Source: https://docs.nebius.com/kms/manage/rotate

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to rotate symmetric keys in Key Management Service

When you [create a symmetric key](https://docs.nebius.com/kms/manage/create.md#how-to-create-a-symmetric-key), you can configure a rotation period to [rotate key material](https://docs.nebius.com/kms/types-operations.md#key-rotation) periodically, but you can also rotate a symmetric key manually. Rotation helps you refresh the cryptographic material behind the key and create a new key version while you continue using the same key resource.

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

## How to rotate a symmetric key manually

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.
2. Make sure that **Symmetric keys** and **Active** are selected in the filters.
3. In the line of the required key, click  → **Rotate**.

**CLI**

1. List symmetric keys:

   ```bash theme={null}
   nebius kms symmetric-key list
   ```

   In the output, copy the ID of the required symmetric key.

2. Rotate the key:

   ```bash theme={null}
   nebius kms symmetric-key rotate <key_ID>
   ```

   In the command, specify the ID of the symmetric key.

   The output looks like the following:

   ```yaml theme={null}
   metadata:
     id: kmssymkey-e00***
     parent_id: project-e00***
     name: my-symmetric-key
     resource_version: "2"
     created_at: "2026-05-07T10:18:49.623048Z"
     updated_at: "2026-05-07T10:21:17.384632Z"
   spec:
     description: test-key
     algorithm: AES_256
     rotation_period: 0s
   status:
     state: ACTIVE
   ```

   Each time you rotate a key, the `resource_version` value increases by one.

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

2. Rotate the key:

   ```go theme={null}
   symRotateService := sdk.Services().KMS().V1().
       SymmetricKey()
   symRotateOperation, err := symRotateService.Rotate(
       ctx,
       &kms.RotateSymmetricKeyRequest{
           Id: "<key_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("rotate symmetric key: %w", err)
   }
   symRotateOperation, err = symRotateOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for operation: %w", err)
   }
   symRotateResult, err := symRotateService.Get(
       ctx,
       &kms.GetSymmetricKeyRequest{
           Id: symRotateOperation.ResourceID(),
       },
   )
   if err != nil {
       return fmt.Errorf("get key: %w", err)
   }
   fmt.Println(symRotateResult)
   ```

   In the code, set `Id` to the ID of the symmetric key.

   The code prints the rotated key. Each time you rotate a key, the `resource_version` value in the output increases by one.

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

2. Rotate the key:

   ```python theme={null}
   service = kms.SymmetricKeyServiceClient(sdk)
   operation = await service.rotate(
       kms.RotateSymmetricKeyRequest(
           id="<key_ID>",
       ),
   )
   await operation.wait()
   result = await service.get(
       kms.GetSymmetricKeyRequest(id=operation.resource_id),
   )
   print(result)
   ```

   In the code, set `id` to the ID of the symmetric key.

   The code prints the rotated key. Each time you rotate a key, the `metadata.resource_version` value increases by one.

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

2. Rotate the key:

   ```ts theme={null}
   const symRotateService = new kms.SymmetricKeyService(sdk);
   const symRotateOperation = await symRotateService.rotate(
     kms.RotateSymmetricKeyRequest.create({
       id: "<key_ID>",
     }),
   ).result;
   await symRotateOperation.wait();
   const symRotateResult = await symRotateService.get(
     kms.GetSymmetricKeyRequest.create({
       id: symRotateOperation.resourceId(),
     }),
   ).result;
   console.log(symRotateResult);
   ```

   In the code, set `id` to the ID of the symmetric key.

   The code prints the rotated key. Each time you rotate a key, the `metadata.resourceVersion` value increases by one.
