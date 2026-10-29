# How to find out platforms and presets available in a project

Source: https://docs.nebius.com/compute/virtual-machines/list-platforms

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to find out platforms and presets available in a project

Different virtual machine platforms and presets are available for different regions and projects. All supported platforms and presets are listed in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to find out available platforms and presets

To find out what platforms and presets are available in a given project:

**CLI**

Run the following command:

```bash theme={null}
nebius compute platform list --parent-id <project_ID>
```

In the `--parent-id` parameter, specify the ID of the project for which you want to see the list.

**Go SDK**

```go theme={null}
platforms, err := sdk.Services().Compute().V1().
    Platform().List(
        ctx,
        &compute.ListPlatformsRequest{
            ParentId: "<project_ID>",
        },
    )
if err != nil {
    return err
}
fmt.Println(platforms)
```

In the `ParentId` parameter, specify the ID of the project for which you want to see the list.

**Python SDK**

```python theme={null}
platform_service = PlatformServiceClient(sdk)
platforms = await platform_service.list(
    ListPlatformsRequest(parent_id="<project_ID>"),
)
print(platforms)
```

In the `parent_id` parameter, specify the ID of the project for which you want to see the list.

**JavaScript SDK**

```ts theme={null}
const platformService = new PlatformService(sdk);
const platforms = await platformService.list(
  ListPlatformsRequest.create({
    parentId: "<project_ID>",
  }),
);
console.log(platforms);
```

In the `parentId` parameter, specify the ID of the project for which you want to see the list.
