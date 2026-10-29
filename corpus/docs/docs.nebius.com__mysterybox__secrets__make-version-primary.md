# How to make a secret version primary in SecretStash

Source: https://docs.nebius.com/mysterybox/secrets/make-version-primary

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to make a secret version primary in SecretStash

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

The [primary version](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions) is the version that is returned by default when you get a payload. You can set any version as the primary one.

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

## How to make a version primary

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.
2. Open the page of the required secret.
3. Go to the **Versions** tab.
4. In the line of the version that you want to make primary, click  → **Make primary**.

**CLI**

1. List all secrets:

   ```bash theme={null}
   nebius mysterybox secret list
   ```

   In the output, copy the ID of the required secret.

2. Save the ID to the environment variable:

   ```bash theme={null}
   export SECRET_ID=<secret_ID>
   ```

3. List all versions of the secret:

   ```bash theme={null}
   nebius mysterybox secret-version list --parent-id $SECRET_ID
   ```

   In the output, find the version that you want to make primary and copy its ID.

4. Specify the version ID in the following command:

   ```bash theme={null}
   nebius mysterybox secret update $SECRET_ID --primary-version-id <version_ID>
   ```

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

   In the output, copy the ID of the required secret.

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

   In `ParentId`, specify the ID that you copied earlier.

   In the output, find the version that you want to make primary and copy its ID.

3. Make the version primary:

   ```go theme={null}
   updateService := sdk.Services().Mysterybox().V1().Secret()
   secret, err := updateService.Get(
     ctx,
     &mb.GetSecretRequest{Id: "<secret_ID>"},
   )
   if err != nil {
     return fmt.Errorf("get secret: %w", err)
   }
   primaryVersionID := "<version_ID>"
   secret.Spec.PrimaryVersionId = &primaryVersionID
   updateOperation, err := updateService.Update(
     ctx,
     &mb.UpdateSecretRequest{
       Metadata: secret.Metadata,
       Spec: secret.Spec,
     },
   )
   if err != nil {
     return fmt.Errorf("update secret: %w", err)
   }
   updateOperation, err = updateOperation.Wait(ctx)
   if err != nil {
     return fmt.Errorf("wait for secret update: %w", err)
   }
   updatedSecret, err := updateService.Get(
     ctx,
     &mb.GetSecretRequest{Id: "<secret_ID>"},
   )
   if err != nil {
     return fmt.Errorf("get updated secret: %w", err)
   }
   fmt.Println(updatedSecret)
   ```

   In the code, specify the following parameters:

   * `Id`: ID of the secret that you copied earlier.
   * `Spec.PrimaryVersionId`: ID of the version that you want to make primary.

   The code reads the secret first because the update request replaces the whole secret specification.

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

   In the output, copy the ID of the required secret.

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

   In `parent_id`, specify the ID that you copied earlier.

   In the output, find the version that you want to make primary and copy its ID.

3. Make the version primary:

   ```python theme={null}
   service = SecretServiceClient(sdk)
   secret = await service.get(GetSecretRequest(id="<secret_ID>"))
   secret.spec.primary_version_id = "<version_ID>"
   operation = await service.update(
       UpdateSecretRequest(metadata=secret.metadata, spec=secret.spec),
   )
   await operation.wait()
   updated_secret = await service.get(
       GetSecretRequest(id="<secret_ID>"),
   )
   print(updated_secret)
   ```

   In the code, specify the following parameters:

   * `id`: ID of the secret that you copied earlier.
   * `spec.primary_version_id`: ID of the version that you want to make primary.

   The code reads the secret first because the update request replaces the whole secret specification.

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

   In the output, copy the ID of the required secret.

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

   In `parentId`, specify the ID that you copied earlier.

   In the output, find the version that you want to make primary and copy its ID.

3. Make the version primary:

   ```ts theme={null}
   const updateService = new SecretService(sdk);
   const secret = await updateService.get(
     GetSecretRequest.create({ id: "<secret_ID>" }),
   ).result;
   if (!secret.spec) {
     throw new Error("The secret has no specification.");
   }
   secret.spec.primaryVersionId = "<version_ID>";
   const updateOperation = await updateService.update(
     UpdateSecretRequest.create({
       metadata: secret.metadata,
       spec: secret.spec,
     }),
   ).result;
   await updateOperation.wait();
   const updatedSecret = await updateService.get(
     GetSecretRequest.create({ id: "<secret_ID>" }),
   ).result;
   console.log(updatedSecret);
   ```

   In the code, specify the following parameters:

   * `id`: ID of the secret that you copied earlier.
   * `spec.primaryVersionId`: ID of the version that you want to make primary.

   The code reads the secret first because the update request replaces the whole secret specification.

Now, when you get a payload, this version will be returned by default.
