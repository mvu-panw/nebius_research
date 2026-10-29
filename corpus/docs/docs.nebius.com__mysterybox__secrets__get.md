# How to get SecretStash secrets and versions

Source: https://docs.nebius.com/mysterybox/secrets/get

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to get SecretStash secrets and versions

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

You can get information about secrets, their versions and payloads:

* If you want to get general information about secrets (for example, a secret ID), [get a list of secrets](#how-to-get-a-list-of-secrets).
* If you want to find out what versions a secret has, [get a list of its versions](#how-to-get-a-list-of-versions).
* If you want to get sensitive information stored in a version of a secret, [get the version payload](#how-to-get-a-payload).

For more information, see [About SecretStash](https://docs.nebius.com/mysterybox/overview.md).

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to get a list of secrets

**CLI**

Run the following command:

```bash theme={null}
nebius mysterybox secret list
```

To include secrets that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-secret), add `--show-scheduled-for-deletion`:

```bash theme={null}
nebius mysterybox secret list --show-scheduled-for-deletion
```

**Go SDK**

List the secrets:

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

The API returns results in pages. The code requests the pages one by one: it passes the `NextPageToken` value from each response as `PageToken` in the next request, until the value is empty. The same applies to listing versions.

To include secrets that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-secret), set `ShowScheduledForDeletion` to `true`:

```go theme={null}
restorableSecretsService := sdk.Services().Mysterybox().
  V1().Secret()
restorablePageToken := ""
for {
  restorableSecrets, err := restorableSecretsService.List(
    ctx,
    &mb.ListSecretsRequest{
      ShowScheduledForDeletion: true,
      PageToken: restorablePageToken,
    },
  )
  if err != nil {
    return fmt.Errorf("get restorable secrets: %w", err)
  }
  fmt.Println(restorableSecrets.GetItems())
  restorablePageToken = restorableSecrets.GetNextPageToken()
  if restorablePageToken == "" {
    break
  }
}
```

**Python SDK**

List the secrets:

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

The API returns results in pages. The code requests the pages one by one: it passes the `next_page_token` value from each response as `page_token` in the next request, until the value is empty. The same applies to listing versions.

To include secrets that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-secret), set `show_scheduled_for_deletion` to `True`:

```python theme={null}
service = SecretServiceClient(sdk)
page_token = ""
while True:
    response = await service.list(
        ListSecretsRequest(
            show_scheduled_for_deletion=True,
            page_token=page_token,
        ),
    )
    print(response.items)
    page_token = response.next_page_token
    if not page_token:
        break
```

**JavaScript SDK**

List the secrets:

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

The API returns results in pages. The code requests the pages one by one: it passes the `nextPageToken` value from each response as `pageToken` in the next request, until the value is empty. The same applies to listing versions.

To include secrets that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-secret), set `showScheduledForDeletion` to `true`:

```ts theme={null}
const restorableSecretsService = new SecretService(sdk);
let restorablePageToken = "";
do {
  const restorableSecrets = await restorableSecretsService.list(
    ListSecretsRequest.create({
      showScheduledForDeletion: true,
      pageToken: restorablePageToken,
    }),
  ).result;
  console.log(restorableSecrets.items);
  restorablePageToken = restorableSecrets.nextPageToken;
} while (restorablePageToken);
```

## How to get a list of versions

**CLI**

To get versions of a given secret, run the following command:

```bash theme={null}
nebius mysterybox secret-version list --parent-id mbsec-*** --show-scheduled-for-deletion
```

The command contains the following parameters:

* `--parent-id`: ID of the secret. To get the ID, run `nebius mysterybox secret list`.
* `--show-scheduled-for-deletion` (optional): In addition to existing versions, lists versions that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-version).

**Go SDK**

Get versions of a given secret:

```go theme={null}
versionsService := sdk.Services().Mysterybox().V1().
  SecretVersion()
versionsPageToken := ""
for {
  versions, err := versionsService.List(
    ctx,
    &mb.ListSecretVersionsRequest{
      ParentId: "mbsec-***",
      ShowScheduledForDeletion: true,
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

The code contains the following parameters:

* `ParentId`: ID of the secret. To get the ID, [get a list of secrets](#how-to-get-a-list-of-secrets).
* `ShowScheduledForDeletion` (optional): Set it to `true` to also list versions that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-version).

**Python SDK**

Get versions of a given secret:

```python theme={null}
service = SecretVersionServiceClient(sdk)
page_token = ""
while True:
    response = await service.list(
        ListSecretVersionsRequest(
            parent_id="mbsec-***",
            show_scheduled_for_deletion=True,
            page_token=page_token,
        ),
    )
    print(response.items)
    page_token = response.next_page_token
    if not page_token:
        break
```

The code contains the following parameters:

* `parent_id`: ID of the secret. To get the ID, [get a list of secrets](#how-to-get-a-list-of-secrets).
* `show_scheduled_for_deletion` (optional): Set it to `True` to also list versions that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-version).

**JavaScript SDK**

Get versions of a given secret:

```ts theme={null}
const versionsService = new SecretVersionService(sdk);
let versionsPageToken = "";
do {
  const versions = await versionsService.list(
    ListSecretVersionsRequest.create({
      parentId: "mbsec-***",
      showScheduledForDeletion: true,
      pageToken: versionsPageToken,
    }),
  ).result;
  console.log(versions.items);
  versionsPageToken = versions.nextPageToken;
} while (versionsPageToken);
```

The code contains the following parameters:

* `parentId`: ID of the secret. To get the ID, [get a list of secrets](#how-to-get-a-list-of-secrets).
* `showScheduledForDeletion` (optional): Set it to `true` to also list versions that have been deleted in the last 30 days and can still be [restored](https://docs.nebius.com/mysterybox/secrets/delete.md#how-to-restore-a-version).

## How to get a payload

Before you begin, make sure you are in a group that has at least the `mysterybox.payload-viewer` role. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

**CLI**

To get the payload of a given version, run the following command:

```bash theme={null}
nebius mysterybox payload get --secret-id mbsec-*** --version-id mbsecver-***
```

In the command, set the following parameters:

* `--secret-id`: ID of the secret. To get the ID, run `nebius mysterybox secret list`.
* `--version-id` (optional): ID of the version. To get the ID, run `nebius mysterybox secret-version list --parent-id <secret_ID>`.

  If you do not specify `--version-id`, the command returns the payload of the primary version.

**Go SDK**

Get the payload of a given version:

```go theme={null}
payloadService := sdk.Services().Mysterybox().V1().
  Payload()
payload, err := payloadService.Get(
  ctx,
  &mb.GetPayloadRequest{
    SecretId: "mbsec-***",
    VersionId: "mbsecver-***",
  },
)
if err != nil {
  return fmt.Errorf("get payload: %w", err)
}
payloadJSON, err := protojson.Marshal(payload)
if err != nil {
  return fmt.Errorf("encode payload: %w", err)
}
fmt.Println(string(payloadJSON))
```

In the code, set the following parameters:

* `SecretId`: ID of the secret. To get the ID, [get a list of secrets](#how-to-get-a-list-of-secrets).
* `VersionId` (optional): ID of the version. To get the ID, [get a list of versions](#how-to-get-a-list-of-versions).

  If you do not specify `VersionId`, the request returns the payload of the primary version.

**Python SDK**

Get the payload of a given version:

```python theme={null}
service = PayloadServiceClient(sdk)
response = await service.get(
    GetPayloadRequest(
        secret_id="mbsec-***",
        version_id="mbsecver-***",
    ),
)
print(response.to_json())
```

In the code, set the following parameters:

* `secret_id`: ID of the secret. To get the ID, [get a list of secrets](#how-to-get-a-list-of-secrets).
* `version_id` (optional): ID of the version. To get the ID, [get a list of versions](#how-to-get-a-list-of-versions).

  If you do not specify `version_id`, the request returns the payload of the primary version.

**JavaScript SDK**

Get the payload of a given version:

```ts theme={null}
const payloadService = new PayloadService(sdk);
const payload = await payloadService.get(
  GetPayloadRequest.create({
    secretId: "mbsec-***",
    versionId: "mbsecver-***",
  }),
).result;
console.log(SecretPayload.toJSON(payload));
```

In the code, set the following parameters:

* `secretId`: ID of the secret. To get the ID, [get a list of secrets](#how-to-get-a-list-of-secrets).
* `versionId` (optional): ID of the version. To get the ID, [get a list of versions](#how-to-get-a-list-of-versions).

  If you do not specify `versionId`, the request returns the payload of the primary version.
