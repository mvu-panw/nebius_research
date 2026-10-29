# How to create secrets in SecretStash

Source: https://docs.nebius.com/mysterybox/secrets/create

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create secrets in SecretStash

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

You can create an empty [secret](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions) and add versions whenever you need them, or you can create a secret together with a version immediately.

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

## How to create a secret without a version

You can create a secret without a version by using the CLI or an SDK. If you want to use the web console, follow [How to create a secret with a version](#how-to-create-a-secret-with-a-version).

**CLI**

Run the following command:

```bash theme={null}
nebius mysterybox secret create \
  --name "<secret_name>" \
  --description "<description>"
```

In the command, specify the following values:

* `name`: Name of the secret.
* `description` (optional): Secret description.

**Go SDK**

Create a secret:

```go theme={null}
emptySecretService := sdk.Services().Mysterybox().V1().
  Secret()
emptySecretOperation, err := emptySecretService.Create(
  ctx,
  &mb.CreateSecretRequest{
    Metadata: &common.ResourceMetadata{
      Name: "<secret_name>",
    },
    Spec: &mb.SecretSpec{
      Description: "<description>",
    },
  },
)
if err != nil {
  return fmt.Errorf("create secret: %w", err)
}
emptySecretOperation, err = emptySecretOperation.Wait(ctx)
if err != nil {
  return fmt.Errorf("wait for creation: %w", err)
}
emptySecret, err := emptySecretService.Get(
  ctx,
  &mb.GetSecretRequest{Id: emptySecretOperation.ResourceID()},
)
if err != nil {
  return fmt.Errorf("get created resource: %w", err)
}
fmt.Println(emptySecret)
```

In the code, specify the following values:

* `Metadata.Name`: Name of the secret.
* `Spec.Description` (optional): Secret description.

**Python SDK**

Create a secret:

```python theme={null}
service = SecretServiceClient(sdk)
operation = await service.create(
    CreateSecretRequest(
        metadata=ResourceMetadata(name="<secret_name>"),
        spec=SecretSpec(
            description="<description>",
        ),
    ),
)
await operation.wait()
resource = await service.get(
    GetSecretRequest(id=operation.resource_id),
)
print(resource)
```

In the code, specify the following values:

* `metadata.name`: Name of the secret.
* `spec.description` (optional): Secret description.

**JavaScript SDK**

Create a secret:

```ts theme={null}
const emptySecretService = new SecretService(sdk);
const emptySecretOperation = await emptySecretService.create(
  CreateSecretRequest.create({
    metadata: { name: "<secret_name>" },
    spec: {
      description: "<description>",
    },
  }),
).result;
await emptySecretOperation.wait();
const emptySecret = await emptySecretService.get(
  GetSecretRequest.create({
    id: emptySecretOperation.resourceId(),
  }),
).result;
console.log(emptySecret);
```

In the code, specify the following values:

* `metadata.name`: Name of the secret.
* `spec.description` (optional): Secret description.

After the secret is created, you can refer to it by its name or ID and [create versions](https://docs.nebius.com/mysterybox/secrets/create-version.md) of the secret.

## How to create a secret with a version

You can specify one or several key-value pairs in the version payload. Every pair contains a string value or binary data.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **SecretStash**.

2. Click  **Create secret**.

3. In the window that opens, specify a unique name for the secret. For example, `db-credentials`.

4. (Optional) Add a description that explains what the secret is used for. For example, "Credentials for the production database."

5. In the **Key** and **Value** fields, specify a key-value pair that the secret should store. This pair will be the [payload](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions) of this secret.

   In the **Value** field, select a data type:

   * **Text**: Specify a plain string. Commonly used for passwords, tokens and API keys.
   * **File**: Upload a binary file. Convenient for certificates, private keys and configuration files.

6. (Optional) To store multiple key-value pairs in a single version, click  **Add pair**. Then, specify additional key-value pairs.

7. Click **Create secret**.

**CLI**

Run the `nebius mysterybox secret create` command.

* Strings:

  ```bash theme={null}
  nebius mysterybox secret create \
    --name "<secret_name>" \
    --description "<description>" \
    --secret-version-payload '[
      {"key": "<key_name>", "string_value": "<value>"},
      {"key": "<key_name>", "string_value": "<value>"},
      ...
    ]'
  ```

* Binary files, Ubuntu:

  ```bash theme={null}
  nebius mysterybox secret create \
    --name "<secret_name>" \
    --description "<description>" \
    --secret-version-payload "[
      {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -w 0 <path/to/file>)\"},
      {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -w 0 <path/to/file>)\"},
      ...
    ]"
  ```

* Binary files, macOS:

  ```bash theme={null}
  nebius mysterybox secret create \
    --name "<secret_name>" \
    --description "<description>" \
    --secret-version-payload "[
      {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -i <path/to/file>)\"},
      {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -i <path/to/file>)\"},
      ...
    ]"
  ```

* Both strings and binary files, Ubuntu:

  ```bash theme={null}
  nebius mysterybox secret create \
    --name "<secret_name>" \
    --description "<description>" \
    --secret-version-payload "[
      {\"key\": \"<key_name>\", \"string_value\": \"<value>\"},
      {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -w 0 <path/to/file>)\"},
      ...
    ]"
  ```

* Both strings and binary files, macOS:

  ```bash theme={null}
  nebius mysterybox secret create \
    --name "<secret_name>" \
    --description "<description>" \
    --secret-version-payload "[
      {\"key\": \"<key_name>\", \"string_value\": \"<value>\"},
      {\"key\": \"<key_name>\", \"binary_value\": \"$(base64 -i <path/to/file>)\"},
      ...
    ]"
  ```

In the command, specify the following values:

* `name`: Name of the secret.
* `description` (optional): Secret description.
* `key`: Name of the key.
* `string_value`: For each key with a string value, a sensitive secret value.
* `path/to/file`: For each key with a binary value, a local path to the file whose contents you want to store as binary data in the secret.

**Go SDK**

Create a secret together with its first version:

* Strings:

  ```go theme={null}
  stringSecretService := sdk.Services().Mysterybox().V1().
    Secret()
  stringSecretPayload := []*mb.Payload{
    {
      Key: "<key_name>",
      Payload: &mb.Payload_StringValue{
        StringValue: "<value>",
      },
    },
    {
      Key: "<key_name>",
      Payload: &mb.Payload_StringValue{
        StringValue: "<value>",
      },
    },
  }
  stringSecretOperation, err := stringSecretService.Create(
    ctx,
    &mb.CreateSecretRequest{
      Metadata: &common.ResourceMetadata{
        Name: "<secret_name>",
      },
      Spec: &mb.SecretSpec{
        Description: "<description>",
        SecretVersion: &mb.SecretVersionSpec{
          Payload: stringSecretPayload,
        },
      },
    },
  )
  if err != nil {
    return fmt.Errorf("create secret: %w", err)
  }
  stringSecretOperation, err = stringSecretOperation.Wait(ctx)
  if err != nil {
    return fmt.Errorf("wait for creation: %w", err)
  }
  stringSecret, err := stringSecretService.Get(
    ctx,
    &mb.GetSecretRequest{Id: stringSecretOperation.ResourceID()},
  )
  if err != nil {
    return fmt.Errorf("get created resource: %w", err)
  }
  fmt.Println(stringSecret)
  ```

* Binary files:

  ```go theme={null}
  binaryUbuntuService := sdk.Services().Mysterybox().V1().
    Secret()
  binaryUbuntuData, err := os.ReadFile("<path/to/file>")
  if err != nil {
    return fmt.Errorf("read payload file: %w", err)
  }
  binaryUbuntuPayload := []*mb.Payload{
    {
      Key: "<key_name>",
      Payload: &mb.Payload_BinaryValue{
        BinaryValue: binaryUbuntuData,
      },
    },
    {
      Key: "<key_name>",
      Payload: &mb.Payload_BinaryValue{
        BinaryValue: binaryUbuntuData,
      },
    },
  }
  binaryUbuntuOperation, err := binaryUbuntuService.Create(
    ctx,
    &mb.CreateSecretRequest{
      Metadata: &common.ResourceMetadata{
        Name: "<secret_name>",
      },
      Spec: &mb.SecretSpec{
        Description: "<description>",
        SecretVersion: &mb.SecretVersionSpec{
          Payload: binaryUbuntuPayload,
        },
      },
    },
  )
  if err != nil {
    return fmt.Errorf("create secret: %w", err)
  }
  binaryUbuntuOperation, err = binaryUbuntuOperation.Wait(ctx)
  if err != nil {
    return fmt.Errorf("wait for creation: %w", err)
  }
  binaryUbuntu, err := binaryUbuntuService.Get(
    ctx,
    &mb.GetSecretRequest{Id: binaryUbuntuOperation.ResourceID()},
  )
  if err != nil {
    return fmt.Errorf("get created resource: %w", err)
  }
  fmt.Println(binaryUbuntu)
  ```

* Both strings and binary files:

  ```go theme={null}
  mixedUbuntuService := sdk.Services().Mysterybox().V1().
    Secret()
  mixedUbuntuData, err := os.ReadFile("<path/to/file>")
  if err != nil {
    return fmt.Errorf("read payload file: %w", err)
  }
  mixedUbuntuPayload := []*mb.Payload{
    {
      Key: "<key_name>",
      Payload: &mb.Payload_StringValue{
        StringValue: "<value>",
      },
    },
    {
      Key: "<key_name>",
      Payload: &mb.Payload_BinaryValue{
        BinaryValue: mixedUbuntuData,
      },
    },
  }
  mixedUbuntuOperation, err := mixedUbuntuService.Create(
    ctx,
    &mb.CreateSecretRequest{
      Metadata: &common.ResourceMetadata{
        Name: "<secret_name>",
      },
      Spec: &mb.SecretSpec{
        Description: "<description>",
        SecretVersion: &mb.SecretVersionSpec{
          Payload: mixedUbuntuPayload,
        },
      },
    },
  )
  if err != nil {
    return fmt.Errorf("create secret: %w", err)
  }
  mixedUbuntuOperation, err = mixedUbuntuOperation.Wait(ctx)
  if err != nil {
    return fmt.Errorf("wait for creation: %w", err)
  }
  mixedUbuntu, err := mixedUbuntuService.Get(
    ctx,
    &mb.GetSecretRequest{Id: mixedUbuntuOperation.ResourceID()},
  )
  if err != nil {
    return fmt.Errorf("get created resource: %w", err)
  }
  fmt.Println(mixedUbuntu)
  ```

In the code, specify the following values:

* `Key`: Name of the key.
* `StringValue`: For each key with a string value, a sensitive secret value.
* `BinaryValue`: For each key with a binary value, the file contents to store as binary data in the secret. In the examples, `os.ReadFile` reads them from a local path.
* `Metadata.Name`: Name of the secret.
* `Spec.Description` (optional): Secret description.

**Python SDK**

Create a secret together with its first version:

* Strings:

  ```python theme={null}
  service = SecretServiceClient(sdk)
  payload = [
      Payload(
          key="<key_name>",
          string_value="<value>",
      ),
      Payload(
          key="<key_name>",
          string_value="<value>",
      ),
  ]
  operation = await service.create(
      CreateSecretRequest(
          metadata=ResourceMetadata(name="<secret_name>"),
          spec=SecretSpec(
              description="<description>",
              secret_version=SecretVersionSpec(payload=payload),
          ),
      ),
  )
  await operation.wait()
  resource = await service.get(
      GetSecretRequest(id=operation.resource_id),
  )
  print(resource)
  ```

* Binary files:

  ```python theme={null}
  service = SecretServiceClient(sdk)
  file_data = Path("<path/to/file>").read_bytes()
  payload = [
      Payload(
          key="<key_name>",
          binary_value=file_data,
      ),
      Payload(
          key="<key_name>",
          binary_value=file_data,
      ),
  ]
  operation = await service.create(
      CreateSecretRequest(
          metadata=ResourceMetadata(name="<secret_name>"),
          spec=SecretSpec(
              description="<description>",
              secret_version=SecretVersionSpec(payload=payload),
          ),
      ),
  )
  await operation.wait()
  resource = await service.get(
      GetSecretRequest(id=operation.resource_id),
  )
  print(resource)
  ```

* Both strings and binary files:

  ```python theme={null}
  service = SecretServiceClient(sdk)
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
      CreateSecretRequest(
          metadata=ResourceMetadata(name="<secret_name>"),
          spec=SecretSpec(
              description="<description>",
              secret_version=SecretVersionSpec(payload=payload),
          ),
      ),
  )
  await operation.wait()
  resource = await service.get(
      GetSecretRequest(id=operation.resource_id),
  )
  print(resource)
  ```

In the code, specify the following values:

* `key`: Name of the key.
* `string_value`: For each key with a string value, a sensitive secret value.
* `binary_value`: For each key with a binary value, the file contents to store as binary data in the secret. In the examples, `Path.read_bytes` reads them from a local path.
* `metadata.name`: Name of the secret.
* `spec.description` (optional): Secret description.

**JavaScript SDK**

Create a secret together with its first version:

* Strings:

  ```ts theme={null}
  const stringSecretService = new SecretService(sdk);
  const stringSecretPayload = [
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
        $case: "stringValue",
        stringValue: "<value>",
      },
    },
  ];
  const stringSecretOperation = await stringSecretService.create(
    CreateSecretRequest.create({
      metadata: { name: "<secret_name>" },
      spec: {
        description: "<description>",
        secretVersion: { payload: stringSecretPayload },
      },
    }),
  ).result;
  await stringSecretOperation.wait();
  const stringSecret = await stringSecretService.get(
    GetSecretRequest.create({
      id: stringSecretOperation.resourceId(),
    }),
  ).result;
  console.log(stringSecret);
  ```

* Binary files:

  ```ts theme={null}
  const binaryUbuntuService = new SecretService(sdk);
  const binaryUbuntuData = await readFile("<path/to/file>");
  const binaryUbuntuPayload = [
    {
      key: "<key_name>",
      payload: {
        $case: "binaryValue",
        binaryValue: binaryUbuntuData,
      },
    },
    {
      key: "<key_name>",
      payload: {
        $case: "binaryValue",
        binaryValue: binaryUbuntuData,
      },
    },
  ];
  const binaryUbuntuOperation = await binaryUbuntuService.create(
    CreateSecretRequest.create({
      metadata: { name: "<secret_name>" },
      spec: {
        description: "<description>",
        secretVersion: { payload: binaryUbuntuPayload },
      },
    }),
  ).result;
  await binaryUbuntuOperation.wait();
  const binaryUbuntu = await binaryUbuntuService.get(
    GetSecretRequest.create({
      id: binaryUbuntuOperation.resourceId(),
    }),
  ).result;
  console.log(binaryUbuntu);
  ```

* Both strings and binary files:

  ```ts theme={null}
  const mixedUbuntuService = new SecretService(sdk);
  const mixedUbuntuData = await readFile("<path/to/file>");
  const mixedUbuntuPayload = [
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
        binaryValue: mixedUbuntuData,
      },
    },
  ];
  const mixedUbuntuOperation = await mixedUbuntuService.create(
    CreateSecretRequest.create({
      metadata: { name: "<secret_name>" },
      spec: {
        description: "<description>",
        secretVersion: { payload: mixedUbuntuPayload },
      },
    }),
  ).result;
  await mixedUbuntuOperation.wait();
  const mixedUbuntu = await mixedUbuntuService.get(
    GetSecretRequest.create({
      id: mixedUbuntuOperation.resourceId(),
    }),
  ).result;
  console.log(mixedUbuntu);
  ```

In the code, specify the following values:

* `key`: Name of the key.
* `payload.$case`: Type of the value: `stringValue` for a string or `binaryValue` for binary data.
* `stringValue`: For each key with a string value, a sensitive secret value.
* `binaryValue`: For each key with a binary value, the file contents to store as binary data in the secret. In the examples, `readFile` reads them from a local path.
* `metadata.name`: Name of the secret.
* `spec.description` (optional): Secret description.

After the secret is created, you can refer to it by its name or ID.
