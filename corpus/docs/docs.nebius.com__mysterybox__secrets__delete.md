# How to delete secrets and their versions in SecretStash

Source: https://docs.nebius.com/mysterybox/secrets/delete

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to delete secrets and their versions in SecretStash

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

You can delete individual versions or entire secrets. Deleted items can be restored within 30 days. After 30 days, deleted secrets and versions are permanently removed.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Deleting versions and secrets

### How to delete a version

You can delete any version, even a primary one. However, if you delete a primary version and do not [assign another version as primary](https://docs.nebius.com/mysterybox/secrets/make-version-primary.md), you will receive an error when requesting the secret payload without specifying a version. You can only retrieve a payload without specifying a version if the secret has a primary version.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.
2. Open the page of the required secret.
3. Go to the **Versions** tab.
4. In the line of the version that you want to delete, click  → **Delete**.
5. Confirm the version deletion.

**CLI**

1. List all secrets:

   ```bash theme={null}
   nebius mysterybox secret list
   ```

   In the output, copy the ID of the secret whose version you want to delete.

2. List all versions of the secret:

   ```bash theme={null}
   nebius mysterybox secret-version list --parent-id <secret_ID>
   ```

   In the command, specify the copied ID.

   In the output, find the version that you want to delete and copy its ID.

3. Delete the version:

   ```bash theme={null}
   nebius mysterybox secret-version delete <version_ID>
   ```

   To make sure that the version is deleted, check its status in the output. It should be empty (`status: {}`).

**Go SDK**

1. List all secrets. The code requests the pages of results one by one, using the next page token from each response, until all secrets are returned:

   ```go theme={null}
   secretsService := sdk.Services().Mysterybox().V1().
     Secret()
   secretsPageToken := ""
   for {
     secrets, err := secretsService.List(
       ctx,
       &mb.ListSecretsRequest{
         PageToken: secretsPageToken,
       },
     )
     if err != nil {
       return fmt.Errorf("get secrets: %w", err)
     }
     fmt.Println(secrets.GetItems())
     secretsPageToken = secrets.GetNextPageToken()
     if secretsPageToken == "" {
       break
     }
   }
   ```

   In the output, copy the ID of the secret whose version you want to delete.

2. List all versions of the secret:

   ```go theme={null}
   versionsService := sdk.Services().Mysterybox().V1().
     SecretVersion()
   versionsPageToken := ""
   for {
     versions, err := versionsService.List(
       ctx,
       &mb.ListSecretVersionsRequest{
         ParentId: "<secret_ID>",
         PageToken: versionsPageToken,
       },
     )
     if err != nil {
       return fmt.Errorf("get versions: %w", err)
     }
     fmt.Println(versions.GetItems())
     versionsPageToken = versions.GetNextPageToken()
     if versionsPageToken == "" {
       break
     }
   }
   ```

   In `ParentId`, specify the copied ID.

   In the output, find the version that you want to delete and copy its ID.

3. Delete the version:

   ```go theme={null}
   deleteVersionService := sdk.Services().Mysterybox().V1().
     SecretVersion()
   deleteVersionOperation, err := deleteVersionService.Delete(
     ctx,
     &mb.DeleteSecretVersionRequest{Id: "<version_ID>"},
   )
   if err != nil {
     return fmt.Errorf("delete resource: %w", err)
   }
   deleteVersionOperation, err = deleteVersionOperation.Wait(ctx)
   if err != nil {
     return fmt.Errorf("wait for delete: %w", err)
   }
   ```

   In `Id`, specify the ID of the version. The code waits until the deletion operation completes.

**Python SDK**

1. List all secrets. The code requests the pages of results one by one, using the next page token from each response, until all secrets are returned:

   ```python theme={null}
   service = SecretServiceClient(sdk)
   page_token = ""
   while True:
       response = await service.list(
           ListSecretsRequest(
               page_token=page_token,
           ),
       )
       print(response.items)
       page_token = response.next_page_token
       if not page_token:
           break
   ```

   In the output, copy the ID of the secret whose version you want to delete.

2. List all versions of the secret:

   ```python theme={null}
   service = SecretVersionServiceClient(sdk)
   page_token = ""
   while True:
       response = await service.list(
           ListSecretVersionsRequest(
               parent_id="<secret_ID>",
               page_token=page_token,
           ),
       )
       print(response.items)
       page_token = response.next_page_token
       if not page_token:
           break
   ```

   In `parent_id`, specify the copied ID.

   In the output, find the version that you want to delete and copy its ID.

3. Delete the version:

   ```python theme={null}
   service = SecretVersionServiceClient(sdk)
   operation = await service.delete(
       DeleteSecretVersionRequest(id="<version_ID>"),
   )
   await operation.wait()
   ```

   In `id`, specify the ID of the version. The code waits until the deletion operation completes.

**JavaScript SDK**

1. List all secrets. The code requests the pages of results one by one, using the next page token from each response, until all secrets are returned:

   ```ts theme={null}
   const secretsService = new SecretService(sdk);
   let secretsPageToken = "";
   do {
     const secrets = await secretsService.list(
       ListSecretsRequest.create({
         pageToken: secretsPageToken,
       }),
     ).result;
     console.log(secrets.items);
     secretsPageToken = secrets.nextPageToken;
   } while (secretsPageToken);
   ```

   In the output, copy the ID of the secret whose version you want to delete.

2. List all versions of the secret:

   ```ts theme={null}
   const versionsService = new SecretVersionService(sdk);
   let versionsPageToken = "";
   do {
     const versions = await versionsService.list(
       ListSecretVersionsRequest.create({
         parentId: "<secret_ID>",
         pageToken: versionsPageToken,
       }),
     ).result;
     console.log(versions.items);
     versionsPageToken = versions.nextPageToken;
   } while (versionsPageToken);
   ```

   In `parentId`, specify the copied ID.

   In the output, find the version that you want to delete and copy its ID.

3. Delete the version:

   ```ts theme={null}
   const deleteVersionService = new SecretVersionService(sdk);
   const deleteVersionOperation = await deleteVersionService.delete(
     DeleteSecretVersionRequest.create({ id: "<version_ID>" }),
   ).result;
   await deleteVersionOperation.wait();
   ```

   In `id`, specify the ID of the version. The code waits until the deletion operation completes.

### How to delete a secret

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.
2. Locate the required secret and then click  → **Delete**.
3. Confirm the deletion of the secret.

**CLI**

1. List all secrets:

   ```bash theme={null}
   nebius mysterybox secret list
   ```

   In the output, copy the ID of the secret that you want to delete.

2. Delete the secret:

   ```bash theme={null}
   nebius mysterybox secret delete <secret_ID>
   ```

   To make sure that the secret is deleted, check its status in the output. It should be empty (`status: {}`).

**Go SDK**

1. List all secrets. The code requests the pages of results one by one, using the next page token from each response, until all secrets are returned:

   ```go theme={null}
   secretsService := sdk.Services().Mysterybox().V1().
     Secret()
   secretsPageToken := ""
   for {
     secrets, err := secretsService.List(
       ctx,
       &mb.ListSecretsRequest{
         PageToken: secretsPageToken,
       },
     )
     if err != nil {
       return fmt.Errorf("get secrets: %w", err)
     }
     fmt.Println(secrets.GetItems())
     secretsPageToken = secrets.GetNextPageToken()
     if secretsPageToken == "" {
       break
     }
   }
   ```

   In the output, copy the ID of the secret that you want to delete.

2. Delete the secret:

   ```go theme={null}
   deleteSecretService := sdk.Services().Mysterybox().V1().
     Secret()
   deleteSecretOperation, err := deleteSecretService.Delete(
     ctx,
     &mb.DeleteSecretRequest{Id: "<secret_ID>"},
   )
   if err != nil {
     return fmt.Errorf("delete resource: %w", err)
   }
   deleteSecretOperation, err = deleteSecretOperation.Wait(ctx)
   if err != nil {
     return fmt.Errorf("wait for delete: %w", err)
   }
   ```

   In `Id`, specify the copied ID. The code waits until the deletion operation completes.

**Python SDK**

1. List all secrets. The code requests the pages of results one by one, using the next page token from each response, until all secrets are returned:

   ```python theme={null}
   service = SecretServiceClient(sdk)
   page_token = ""
   while True:
       response = await service.list(
           ListSecretsRequest(
               page_token=page_token,
           ),
       )
       print(response.items)
       page_token = response.next_page_token
       if not page_token:
           break
   ```

   In the output, copy the ID of the secret that you want to delete.

2. Delete the secret:

   ```python theme={null}
   service = SecretServiceClient(sdk)
   operation = await service.delete(
       DeleteSecretRequest(id="<secret_ID>"),
   )
   await operation.wait()
   ```

   In `id`, specify the copied ID. The code waits until the deletion operation completes.

**JavaScript SDK**

1. List all secrets. The code requests the pages of results one by one, using the next page token from each response, until all secrets are returned:

   ```ts theme={null}
   const secretsService = new SecretService(sdk);
   let secretsPageToken = "";
   do {
     const secrets = await secretsService.list(
       ListSecretsRequest.create({
         pageToken: secretsPageToken,
       }),
     ).result;
     console.log(secrets.items);
     secretsPageToken = secrets.nextPageToken;
   } while (secretsPageToken);
   ```

   In the output, copy the ID of the secret that you want to delete.

2. Delete the secret:

   ```ts theme={null}
   const deleteSecretService = new SecretService(sdk);
   const deleteSecretOperation = await deleteSecretService.delete(
     DeleteSecretRequest.create({ id: "<secret_ID>" }),
   ).result;
   await deleteSecretOperation.wait();
   ```

   In `id`, specify the copied ID. The code waits until the deletion operation completes.

> [!NOTE]
>
> A deleted secret counts toward the [quota on the number of secrets](https://docs.nebius.com/mysterybox/resources/quotas-limits.md) for 30 days after you delete it. If you hit the quota, you can [request to increase it](https://docs.nebius.com/overview/quotas.md#change-quotas).

## Restoring versions and secrets

You can restore deleted items within 30 days after deletion.

### How to restore a version

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.
2. Open the page of the required secret.
3. Go to the **Versions** tab.
4. To view versions scheduled for deletion, switch to the **Inactive** tab.
5. In the line of the required version, click **Restore**.
6. Confirm the version restoration.

**CLI**

Run the following command:

```bash theme={null}
nebius mysterybox secret-version undelete --id <version_ID>
```

To make sure that the version is restored, check its status in the output. It should be `ACTIVE`.

**Go SDK**

Restore the version:

```go theme={null}
undeleteVersionService := sdk.Services().Mysterybox().V1().
  SecretVersion()
undeleteVersionOperation, err := undeleteVersionService.Undelete(
  ctx,
  &mb.UndeleteSecretVersionRequest{Id: "<version_ID>"},
)
if err != nil {
  return fmt.Errorf("undelete resource: %w", err)
}
undeleteVersionOperation, err = undeleteVersionOperation.Wait(ctx)
if err != nil {
  return fmt.Errorf("wait for undelete: %w", err)
}
```

In `Id`, specify the ID of the version. The code waits until the restoration operation completes.

**Python SDK**

Restore the version:

```python theme={null}
service = SecretVersionServiceClient(sdk)
operation = await service.undelete(
    UndeleteSecretVersionRequest(id="<version_ID>"),
)
await operation.wait()
```

In `id`, specify the ID of the version. The code waits until the restoration operation completes.

**JavaScript SDK**

Restore the version:

```ts theme={null}
const undeleteVersionService =
  new SecretVersionService(sdk);
const undeleteVersionOperation =
  await undeleteVersionService.undelete(
  UndeleteSecretVersionRequest.create({ id: "<version_ID>" }),
).result;
await undeleteVersionOperation.wait();
```

In `id`, specify the ID of the version. The code waits until the restoration operation completes.

### How to restore a secret

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.
2. To view secrets scheduled for deletion, switch to the **Inactive** tab.
3. Locate the required secret and then click **Restore**.
4. Confirm the restoration of the secret.

**CLI**

Run the following command:

```bash theme={null}
nebius mysterybox secret undelete --id <secret_ID>
```

To make sure that the secret is restored, check its status in the output. It should be `ACTIVE`.

**Go SDK**

Restore the secret:

```go theme={null}
undeleteSecretService := sdk.Services().Mysterybox().V1().
  Secret()
undeleteSecretOperation, err := undeleteSecretService.Undelete(
  ctx,
  &mb.UndeleteSecretRequest{Id: "<secret_ID>"},
)
if err != nil {
  return fmt.Errorf("undelete resource: %w", err)
}
undeleteSecretOperation, err = undeleteSecretOperation.Wait(ctx)
if err != nil {
  return fmt.Errorf("wait for undelete: %w", err)
}
```

In `Id`, specify the ID of the secret. The code waits until the restoration operation completes.

**Python SDK**

Restore the secret:

```python theme={null}
service = SecretServiceClient(sdk)
operation = await service.undelete(
    UndeleteSecretRequest(id="<secret_ID>"),
)
await operation.wait()
```

In `id`, specify the ID of the secret. The code waits until the restoration operation completes.

**JavaScript SDK**

Restore the secret:

```ts theme={null}
const undeleteSecretService = new SecretService(sdk);
const undeleteSecretOperation = await undeleteSecretService.undelete(
  UndeleteSecretRequest.create({ id: "<secret_ID>" }),
).result;
await undeleteSecretOperation.wait();
```

In `id`, specify the ID of the secret. The code waits until the restoration operation completes.
