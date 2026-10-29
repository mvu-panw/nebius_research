# Access tokens in Nebius AI Cloud

Source: https://docs.nebius.com/iam/authorization/access-tokens

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Access tokens in Nebius AI Cloud

Access tokens are used for authentication when you work with Nebius AI Cloud interfaces: [Terraform](https://docs.nebius.com/terraform-provider/index.md) and the [API](https://docs.nebius.com/grpc-api/index.md).

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## Getting an access token

To get an access token:

**CLI**

```bash theme={null}
nebius iam get-access-token
```

**Go SDK**

```go theme={null}
token, err := sdk.BearerToken(ctx)
if err != nil {
    return err
}
fmt.Println(token.Token)
```

**Python SDK**

```python theme={null}
token = await sdk.get_token(timeout=None)
print(token.token)
```

**JavaScript SDK**

```ts theme={null}
const authorization = sdk.getAuthorizationProvider();
if (!authorization) {
  throw new Error("authorization is not configured");
}
const metadata = new Metadata();
await authorization.authenticator().authenticate(metadata);
const header = metadata.get("authorization")[0];
if (typeof header !== "string") {
  throw new Error("authorization token is missing");
}
const token = header.replace(/^Bearer\s+/, "");
console.log(token);
```

An access token is valid for 12 hours. After it expires, create a new one.

## Access keys and access tokens

Do not confuse [access keys](https://docs.nebius.com/iam/service-accounts/access-keys.md) with access tokens.

* Access keys are used to authenticate [service accounts](https://docs.nebius.com/iam/service-accounts/manage.md) in AWS-compatible services, such as Object Storage.
* Access tokens are used to authenticate user accounts in Nebius AI Cloud interfaces.
