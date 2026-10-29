# How to create versions of secrets in SecretStash

Source: https://docs.nebius.com/mysterybox/secrets/create-version

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create versions of secrets in SecretStash

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

Each secret can have multiple versions. Versions are useful when you need to change credentials or update a secret payload without modifying existing references, such as configurations, scripts or services that point to the specific secret.

For more information, see [About SecretStash](https://docs.nebius.com/mysterybox/overview.md).

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

## How to create a version

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.

2. Locate the required secret and then click  → **Create version**.

3. (Optional) On the page that opens, add a version description. For example, "New database password."

4. Update **Key** and **Value**. These fields display the key-value pair created in the original version. You can reuse an existing key and value, or you can update them.

   If you update **Value**, select a data type for it:

   * **Text**: Specify a plain string. Commonly used for passwords, tokens and API keys.
   * **File**: Upload a binary file. Convenient for certificates, private keys and configuration files.

5. (Optional) To store multiple key-value pairs in a single version, click  **Add pair**. Then, specify additional key-value pairs.

6. If you want this version to become primary (it will be returned by default when the secret is referenced), keep the **Make this version primary** option enabled.

7. Click **Create version**.

**CLI**

1. List all secrets:

   ```bash theme={null}
   nebius mysterybox secret list
   ```

   In the output, copy the ID of the required secret.

2. Create a new version for the secret.

   * Ubuntu:

     ```bash theme={null}
     nebius mysterybox secret-version create \
       --parent-id <secret_ID> \
       --description "<description>" \
       --payload "[
         {\"key\": \"<key_name>\", \"string_value\": \"<value>\"},
         {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -w 0 <path/to/file>)\"},
         ...
       ]"
     ```

   * macOS:

     ```bash theme={null}
     nebius mysterybox secret-version create \
       --parent-id <secret_ID> \
       --description "<description>" \
       --payload "[
         {\"key\": \"<key_name>\", \"string_value\": \"<value>\"},
         {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -i <path/to/file>)\"},
         ...
       ]"
     ```

   In the command, specify the following parameters:

   * `parent-id`: ID that you copied earlier.
   * `description` (optional): Version description.
   * `key`: Name of the key.
   * `string_value`: For each key with a string value, a sensitive secret value.
   * `path/to/file`: For each key with a binary value, a local path to the file whose contents you want to store as binary data in the secret.

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

2. Create a new version for the secret:

   ```go theme={null}
   versionUbuntuService := sdk.Services().Mysterybox().V1().
     SecretVersion()
   versionUbuntuData, err := os.ReadFile("<path/to/file>")
   if err != nil {
     return fmt.Errorf("read payload file: %w", err)
   }
   versionUbuntuPayload := []*mb.Payload{
     {
       Key: "<key_name>",
       Payload: &mb.Payload_StringValue{
         StringValue: "<value>",
       },
     },
     {
       Key: "<key_name>",
       Payload: &mb.Payload_BinaryValue{
         BinaryValue: versionUbuntuData,
       },
     },
   }
   versionUbuntuOperation, err := versionUbuntuService.Create(
     ctx,
     &mb.CreateSecretVersionRequest{
       Metadata: &common.ResourceMetadata{
         ParentId: "<secret_ID>",
       },
       Spec: &mb.SecretVersionSpec{
         Description: "<description>",
         Payload: versionUbuntuPayload,
       },
     },
   )
   if err != nil {
     return fmt.Errorf("create secret version: %w", err)
   }
   versionUbuntuOperation, err = versionUbuntuOperation.Wait(ctx)
   if err != nil {
     return fmt.Errorf("wait for creation: %w", err)
   }
   versionUbuntu, err := versionUbuntuService.Get(
     ctx,
     &mb.GetSecretVersionRequest{
       Id: versionUbuntuOperation.ResourceID(),
     },
   )
   if err != nil {
     return fmt.Errorf("get created resource: %w", err)
   }
   fmt.Println(versionUbuntu)
   ```

   In the code, specify the following parameters:

   * `Key`: Name of the key.
   * `StringValue`: For each key with a string value, a sensitive secret value.
   * `BinaryValue`: For each key with a binary value, the file contents to store as binary data in the secret. In the example, `os.ReadFile` reads them from a local path.
   * `Metadata.ParentId`: ID that you copied earlier.
   * `Spec.Description` (optional): Version description.

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

2. Create a new version for the secret:

   ```python theme={null}
   service = SecretVersionServiceClient(sdk)
   file_data = Path("<path/to/file>").read_bytes()
   payload = [
       Payload(
           key="<key_name>",
           string_value="<value>",
       ),
       Payload(
           key="<key_name>",
           binary_value=file_data,
       ),
   ]
   operation = await service.create(
       CreateSecretVersionRequest(
           metadata=ResourceMetadata(parent_id="<secret_ID>"),
           spec=SecretVersionSpec(
               description="<description>",
               payload=payload,
           ),
       ),
   )
   await operation.wait()
   resource = await service.get(
       GetSecretVersionRequest(id=operation.resource_id),
   )
   print(resource)
   ```

   In the code, specify the following parameters:

   * `key`: Name of the key.
   * `string_value`: For each key with a string value, a sensitive secret value.
   * `binary_value`: For each key with a binary value, the file contents to store as binary data in the secret. In the example, `Path.read_bytes` reads them from a local path.
   * `metadata.parent_id`: ID that you copied earlier.
   * `spec.description` (optional): Version description.

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

2. Create a new version for the secret:

   ```ts theme={null}
   const versionUbuntuService = new SecretVersionService(sdk);
   const versionUbuntuData = await readFile("<path/to/file>");
   const versionUbuntuPayload = [
     {
       key: "<key_name>",
       payload: {
         $case: "stringValue",
         stringValue: "<value>",
       },
     },
     {
       key: "<key_name>",
       payload: {
         $case: "binaryValue",
         binaryValue: versionUbuntuData,
       },
     },
   ];
   const versionUbuntuOperation = await versionUbuntuService.create(
     CreateSecretVersionRequest.create({
       metadata: { parentId: "<secret_ID>" },
       spec: {
         description: "<description>",
         payload: versionUbuntuPayload,
       },
     }),
   ).result;
   await versionUbuntuOperation.wait();
   const versionUbuntu = await versionUbuntuService.get(
     GetSecretVersionRequest.create({
       id: versionUbuntuOperation.resourceId(),
     }),
   ).result;
   console.log(versionUbuntu);
   ```

   In the code, specify the following parameters:

   * `key`: Name of the key.
   * `payload.$case`: Type of the value: `stringValue` for a string or `binaryValue` for binary data.
   * `stringValue`: For each key with a string value, a sensitive secret value.
   * `binaryValue`: For each key with a binary value, the file contents to store as binary data in the secret. In the example, `readFile` reads them from a local path.
   * `metadata.parentId`: ID that you copied earlier.
   * `spec.description` (optional): Version description.

> [!TIP]
>
> You can [make a new version primary](https://docs.nebius.com/mysterybox/secrets/make-version-primary.md) if you want to get its payload by default. When you create a version by using the CLI or an SDK, it does not become primary automatically.

After the version is created, you can pin requests to it.
