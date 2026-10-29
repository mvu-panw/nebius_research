# Getting a tenant ID in Nebius AI Cloud

Source: https://docs.nebius.com/iam/get-tenants

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting a tenant ID in Nebius AI Cloud

A [tenant](https://docs.nebius.com/iam/overview.md#tenants) in Nebius AI Cloud has a name and ID. For some actions, you need to provide your tenant ID.

## Prerequisites

> [!TIP]
>
> You do not need to complete any prerequisites if you use the web console.

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to get a tenant ID

**Web console**

1. In the [web console](https://console.nebius.com), expand the list of tenants.
2. Next to the tenant name, click  →  **Copy tenant ID**.

**CLI**

Run the following command:

```bash theme={null}
nebius iam whoami --format json \
  | jq -r '.user_profile.tenants[0].tenant_id'
```

The output contains the tenant ID. If you have multiple tenants, the command will return the ID of your first tenant as shown in the [web console](https://console.nebius.com) when you expand the list of tenants. To get the ID of another tenant, change the array index. For example, to get the second tenant:

```bash theme={null}
nebius iam whoami --format json \
  | jq -r '.user_profile.tenants[1].tenant_id'
```

Alternatively, list all tenants that you have access to:

```bash theme={null}
nebius iam tenant list
```

In the output, find the `metadata.id` value to get the tenant ID.

**Go SDK**

```go theme={null}
profile, err := sdk.Services().IAM().V1().Profile().Get(
    ctx,
    &iam.GetProfileRequest{},
)
if err != nil {
    return err
}
tenants := profile.GetUserProfile().GetTenants()
if len(tenants) == 0 {
    fmt.Println("null")
} else {
    fmt.Println(tenants[0].GetTenantId())
}
```

The code prints the ID of your first tenant, as shown in the [web console](https://console.nebius.com) when you expand the top-left list of tenants. To get the ID of another tenant, change the index in `tenants[0]`.

**Python SDK**

```python theme={null}
profile_service = ProfileServiceClient(sdk)
profile = await profile_service.get(GetProfileRequest())
tenants = profile.user_profile.tenants if profile.user_profile else []
if tenants:
    print(tenants[0].tenant_id)
else:
    print("null")
```

The code prints the ID of your first tenant, as shown in the [web console](https://console.nebius.com) when you expand the top-left list of tenants. To get the ID of another tenant, change the index in `tenants[0]`.

**JavaScript SDK**

```ts theme={null}
const profileService = new ProfileService(sdk);
const profile = await profileService.get(
  GetProfileRequest.create({}),
);
const currentTenantId =
  profile?.userProfile?.tenants?.[0]?.tenantId;
console.log(currentTenantId ?? null);
```

The code prints the ID of your first tenant, as shown in the [web console](https://console.nebius.com) when you expand the top-left list of tenants. To get the ID of another tenant, change the index in `tenants?.[0]`.
