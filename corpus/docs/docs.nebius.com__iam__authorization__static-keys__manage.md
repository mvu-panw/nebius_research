# How to manage static keys

Source: https://docs.nebius.com/iam/authorization/static-keys/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage static keys

[Static keys](https://docs.nebius.com/iam/authorization/static-keys.md) provide a method of authentication in Nebius AI Cloud services from third-party tools and systems.

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## Creating a static key

**CLI**

Run the following command:

```bash theme={null}
nebius iam static-key issue \
  --account-service-account-id=<service_account_ID> \
  --service=<CONTAINER_REGISTRY|OBSERVABILITY> \
  --expires-at=<date_in_ISO_8601_format> 
```

In this command, change the following parameters:

* `--account-service-account-id`: The ID of the service account for which the static key is created.

* `--service`: The service for which you create the static key. The following values are possible:

  * `CONTAINER_REGISTRY`: [Container Registry](https://docs.nebius.com/container-registry/index.md)
  * `OBSERVABILITY`: [Observability services](https://docs.nebius.com/observability/index.md)

* `--expires-at` (optional): The date of expiration in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. The default lifetime of a static key is 6 months.

Output example:

```yaml theme={null}
...
    metadata:
      parent_id: project-***
    spec:
      account:
        service_account:
          id: serviceaccount-***
      service: CONTAINER_REGISTRY
  resource_id: statickey-***
token: ********
```

> [!WARNING]
>
> Save the token from the `token` parameter of the output. You will not be able to access it later.

You can also get the ID of the static key from the `resource_id` parameter. The ID can be helpful later if you need to get the information about the static key or revoke it.

**Go SDK**

Issue a static key, then get the resulting operation and read the token from the issue response:

```go theme={null}
issueResponse, err := sdk.Services().IAM().V1().
    StaticKey().Issue(
        ctx,
        &iam.IssueStaticKeyRequest{
            Spec: &iam.StaticKeySpec{
                Account: &iam.Account{
                    Type: &iam.Account_ServiceAccount_{
                        ServiceAccount: &iam.Account_ServiceAccount{
                            Id: "<service_account_ID>",
                        },
                    },
                },
                Service:   iam.StaticKeySpec_CONTAINER_REGISTRY,
                ExpiresAt: timestamppb.New(time.Now().AddDate(0, 1, 0)),
            },
        },
    )
if err != nil {
    return err
}
staticKeyOperation, err := sdk.Services().IAM().V1().
    StaticKey().GetOperation(
        ctx,
        &common.GetOperationRequest{
            Id: issueResponse.GetOperation().GetId(),
        },
    )
if err != nil {
    return err
}
staticKeyToken := issueResponse.GetToken()
```

In the code, set the following parameters:

* `Id` in `Account_ServiceAccount`: The ID of the service account for which the static key is created.

* `Service`: The service for which you create the static key. The following values are possible:

  * `iam.StaticKeySpec_CONTAINER_REGISTRY`: [Container Registry](https://docs.nebius.com/container-registry/index.md)
  * `iam.StaticKeySpec_OBSERVABILITY`: [Observability services](https://docs.nebius.com/observability/index.md)

* `ExpiresAt`: The expiration timestamp for the static key. This example sets it to one month from the current time.

> [!WARNING]
>
> Save the token returned in `issueResponse.GetToken()`. You will not be able to access it later.

You can also get the ID of the static key from the operation returned by `GetOperation`. The ID can be helpful later if you need to get the information about the static key or revoke it.

**Python SDK**

Issue a static key, then get the resulting operation and read the token from the issue response:

```python theme={null}
static_key_service = StaticKeyServiceClient(sdk)
issue_response = await static_key_service.issue(
    IssueStaticKeyRequest(
        spec=StaticKeySpec(
            account=Account(
                service_account=Account__ServiceAccount(
                    id="<service_account_ID>",
                ),
            ),
            service=StaticKeySpec__ClientService.CONTAINER_REGISTRY,
            expiresAt=datetime.now(timezone.utc) + timedelta(days=30),
        ),
    ),
)
operation_service = static_key_service.operation_service()
static_key_operation = await operation_service.get(
    GetOperationRequest(id=issue_response.operation.id),
)
static_key_token = issue_response.token
```

In the code, set the following parameters:

* `id` in `Account__ServiceAccount`: The ID of the service account for which the static key is created.

* `service`: The service for which you create the static key. The following values are possible:

  * `StaticKeySpec__ClientService.CONTAINER_REGISTRY`: [Container Registry](https://docs.nebius.com/container-registry/index.md)
  * `StaticKeySpec__ClientService.OBSERVABILITY`: [Observability services](https://docs.nebius.com/observability/index.md)

* `expiresAt`: The expiration timestamp for the static key. This example sets it to 30 days from the current time.

> [!WARNING]
>
> Save the token returned in `issue_response.token`. You will not be able to access it later.

You can also get the ID of the static key from the operation returned by `operation_service().get()`. The ID can be helpful later if you need to get the information about the static key or revoke it.

**JavaScript SDK**

Issue a static key, then get the resulting operation and read the token from the issue response:

```ts theme={null}
const issueStaticKeyService = new StaticKeyService(sdk);
const issueResponse = await issueStaticKeyService.issue(
  IssueStaticKeyRequest.create({
    metadata: ResourceMetadata.create({
      parentId: "<project_ID>",
    }),
    spec: StaticKeySpec.create({
      account: Account.create({
        type: {$case: "serviceAccount", serviceAccount:
          Account_ServiceAccount.create({id: "<service_account_ID>"})},
      }),
      service: StaticKeySpec_ClientService.CONTAINER_REGISTRY,
      expiresAt: dayjs().add(1, 'month'),
    }),
  }),
);
const staticKeyOperation = await issueStaticKeyService
  .getOperationService()
  .get(
    GetOperationRequest.create({id: issueResponse.operation.id}),
  ).result;
const staticKeyToken = issueResponse.token;
```

In the code, set the following parameters:

* `parentId` in `ResourceMetadata`: The [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3) in which the static key is created.

* `id` in `Account_ServiceAccount`: The ID of the service account for which the static key is created.

* `service`: The service for which you create the static key. The following values are possible:

  * `StaticKeySpec_ClientService.CONTAINER_REGISTRY`: [Container Registry](https://docs.nebius.com/container-registry/index.md)
  * `StaticKeySpec_ClientService.OBSERVABILITY`: [Observability services](https://docs.nebius.com/observability/index.md)

* `expiresAt`: The expiration timestamp for the static key. This example sets it to one month from the current time.

> [!WARNING]
>
> Save the token returned in `issueResponse.token`. You will not be able to access it later.

You can also get the ID of the static key from the operation returned by `getOperationService().get()`. The ID can be helpful later if you need to get the information about the static key or revoke it.

## Listing static keys

**CLI**

To get all static keys in your tenant, run the following command:

```bash theme={null}
nebius iam static-key list
```

To get the details about a static key, run the following command:

```bash theme={null}
nebius iam static-key get --id=<static_key_ID>
```

**Go SDK**

To get all static keys in your tenant:

```go theme={null}
staticKeyList, err := sdk.Services().IAM().V1().StaticKey().
    List(
    ctx,
    &iam.ListStaticKeysRequest{},
)
if err != nil {
    return err
}
fmt.Println(staticKeyList)
```

To get the details about a static key:

```go theme={null}
retrievedStaticKey, err := sdk.Services().IAM().V1().
    StaticKey().Get(
    ctx,
    &iam.GetStaticKeyRequest{Id: "<static_key_ID>"},
)
if err != nil {
    return err
}
fmt.Println(retrievedStaticKey)
```

In the code, set `Id` to the ID of the static key.

**Python SDK**

To get all static keys in your tenant:

```python theme={null}
static_key_service = StaticKeyServiceClient(sdk)
static_keys = await static_key_service.list(
    ListStaticKeysRequest(),
)
print(static_keys)
```

To get the details about a static key:

```python theme={null}
static_key_service = StaticKeyServiceClient(sdk)
static_key = await static_key_service.get(
    GetStaticKeyRequest(id="<static_key_ID>"),
)
print(static_key)
```

In the code, set `id` to the ID of the static key.

**JavaScript SDK**

To get all static keys in your tenant:

```ts theme={null}
const listStaticKeyService = new StaticKeyService(sdk);
const staticKeys = await listStaticKeyService.list(
  ListStaticKeysRequest.create({}),
);
console.log(staticKeys);
```

To get the details about a static key:

```ts theme={null}
const getStaticKeyService = new StaticKeyService(sdk);
const staticKey = await getStaticKeyService.get(
  GetStaticKeyRequest.create({id: "<static_key_ID>"}),
);
console.log(staticKey);
```

In the code, set `id` to the ID of the static key.

## Revoking a static key

**CLI**

You can revoke a static key by using the following command:

```bash theme={null}
nebius iam static-key delete --id=<static_key_ID>
```

If you only know the token value, run the following command to revoke the token:

```bash theme={null}
nebius iam static-key revoke --token=<static_key_token> 
```

**Go SDK**

You can revoke a static key by using the following code:

```go theme={null}
deleteStaticKey, err := sdk.Services().IAM().V1().
    StaticKey().Delete(
        ctx,
        &iam.DeleteStaticKeyRequest{
            Id: "<static_key_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = deleteStaticKey.Wait(ctx); err != nil {
    return err
}
```

In the code, set `Id` to the ID of the static key.

If you only know the token value, use the following code to revoke the token:

```go theme={null}
revokeStaticKey, err := sdk.Services().IAM().V1().
    StaticKey().Revoke(
        ctx,
        &iam.RevokeStaticKeyRequest{
            Token: "<static_key_token>",
        },
    )
if err != nil {
    return err
}
if _, err = revokeStaticKey.Wait(ctx); err != nil {
    return err
}
```

In the code, set `Token` to the static key's token value.

**Python SDK**

You can revoke a static key by using the following code:

```python theme={null}
static_key_service = StaticKeyServiceClient(sdk)
delete_static_key = await static_key_service.delete(
    DeleteStaticKeyRequest(id="<static_key_ID>"),
)
await delete_static_key.wait()
```

In the code, set `id` to the ID of the static key.

If you only know the token value, use the following code to revoke the token:

```python theme={null}
static_key_service = StaticKeyServiceClient(sdk)
revoke_static_key = await static_key_service.revoke(
    RevokeStaticKeyRequest(token="<static_key_token>"),
)
await revoke_static_key.wait()
```

In the code, set `token` to the static key's token value.

**JavaScript SDK**

You can revoke a static key by using the following code:

```ts theme={null}
const deleteStaticKeyService = new StaticKeyService(sdk);
const deleteStaticKey = await deleteStaticKeyService.delete(
  DeleteStaticKeyRequest.create({id: "<static_key_ID>"}),
).result;
await deleteStaticKey.wait();
```

In the code, set `id` to the ID of the static key.

If you only know the token value, use the following code to revoke the token:

```ts theme={null}
const revokeStaticKeyService = new StaticKeyService(sdk);
const revokeStaticKey = await revokeStaticKeyService.revoke(
  RevokeStaticKeyRequest.create({token: "<static_key_token>"}),
).result;
await revokeStaticKey.wait();
```

In the code, set `token` to the static key's token value.
