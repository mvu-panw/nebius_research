# Renaming tenants in Nebius AI Cloud

Source: https://docs.nebius.com/iam/rename-tenants

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Renaming tenants in Nebius AI Cloud

A [tenant](https://docs.nebius.com/iam/overview.md#tenants) in Nebius AI Cloud has a name and ID. You can change the tenant name; the tenant ID remains the same.

## Prerequisites

The preparations for this guide depend on your preferred interface.

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to rename a tenant

**Web console**

1. Go to the [web console](https://console.nebius.com) and expand the list of tenants.
2. In the line of the required tenant, click  → **Rename tenant**.
3. In the window that opens, specify the new name.
4. Click **Rename tenant**.

A random suffix is appended to the name you specify, to ensure that the new name is unique. For example, if you entered `my-main-tenant`, the new name can be `my-main-tenant-jf3`.

**CLI**

Run the following command:

```bash theme={null}
nebius iam v2 tenant update --id <tenant_ID> \
  --name-prefix <new_tenant_name>
```

In this command, specify the following:

* `--id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
* `--name-prefix`: Desired name. A random suffix is appended to the name you specify, to ensure that the new name is unique. For example, if you entered `my-main-tenant`, the new name can be `my-main-tenant-jf3`.

**Go SDK**

Get the tenant, then update it with a new name prefix:

```go theme={null}
tenantService := sdk.Services().IAM().V2().
    Tenant()
tenant, err := tenantService.Get(
    ctx,
    &iamv2.GetTenantRequest{Id: "<tenant_ID>"},
)
if err != nil {
    return err
}
renameTenantOperation, err := tenantService.
    Update(
        ctx,
        &iamv2.UpdateTenantRequest{
            Metadata:   tenant.GetMetadata(),
            Spec:       tenant.GetSpec(),
            NamePrefix: "<new_tenant_name>",
        },
    )
if err != nil {
    return err
}
if _, err = renameTenantOperation.Wait(ctx); err != nil {
    return err
}
```

In the code, set the following parameters:

* `Id` in `GetTenantRequest`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).
* `NamePrefix`: Desired name. A random suffix is appended to the name you specify, to ensure that the new name is unique. For example, if you entered `my-main-tenant`, the new name can be `my-main-tenant-jf3`.

**Python SDK**

Get the tenant, then update it with a new name prefix:

```python theme={null}
tenant_service = TenantServiceClient(sdk)
tenant = await tenant_service.get(
    GetTenantRequest(id="<tenant_ID>"),
)
rename_tenant_operation = (
    await tenant_service.update(
        UpdateTenantRequest(
            metadata=tenant.metadata,
            spec=tenant.spec,
            name_prefix="<new_tenant_name>",
        ),
    )
)
await rename_tenant_operation.wait()
```

In the code, set the following parameters:

* `id` in `GetTenantRequest`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).
* `name_prefix`: Desired name. A random suffix is appended to the name you specify, to ensure that the new name is unique. For example, if you entered `my-main-tenant`, the new name can be `my-main-tenant-jf3`.

**JavaScript SDK**

Get the tenant, then update it with a new name prefix:

```ts theme={null}
const tenantService = new TenantService(sdk);
const tenant = await tenantService.get(
  GetTenantRequest.create({id: "<tenant_ID>"}),
);
const renameTenantOperation =
  await tenantService.update(
    UpdateTenantRequest.create({
      metadata: tenant.metadata,
      spec: tenant.spec,
      namePrefix: "<new_tenant_name>",
    }),
  ).result;
await renameTenantOperation.wait();
```

In the code, set the following parameters:

* `id` in `GetTenantRequest`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).
* `namePrefix`: Desired name. A random suffix is appended to the name you specify, to ensure that the new name is unique. For example, if you entered `my-main-tenant`, the new name can be `my-main-tenant-jf3`.
