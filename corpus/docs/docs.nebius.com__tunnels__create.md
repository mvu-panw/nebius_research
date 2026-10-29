# How to create a tunnel in Nebius Tunnels

Source: https://docs.nebius.com/tunnels/create

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create a tunnel in Nebius Tunnels

A *tunnel* is the Nebius AI Cloud resource that receives public traffic and forwards it to a tunnel agent.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Creating a tunnel

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Networking** → **Tunnels**.

2. Click **Create tunnel**.

3. Specify a name for the tunnel.

4. (Optional) Add a description.

5. Click **Create**.

**CLI**

Create a tunnel:

```bash theme={null}
nebius tunnel create \
  --title <tunnel_title>
```

The command uses the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) from your CLI profile configuration.

**Go SDK**

Create a tunnel:

```go theme={null}
createTunnelService := sdk.Services().Tunnel().V1().
    Tunnel()
createTunnelOperation, err := createTunnelService.Create(
    ctx,
    &tunnel.CreateTunnelRequest{
        Spec: &tunnel.TunnelSpec{
            Title: "<tunnel_title>",
        },
    },
)
if err != nil {
    return fmt.Errorf("create tunnel: %w", err)
}
createTunnelOperation, err = createTunnelOperation.Wait(ctx)
if err != nil {
    return fmt.Errorf("wait for create tunnel: %w", err)
}
```

In the code, set `Title` in `TunnelSpec` to the tunnel title. The code uses the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you set with `gosdk.WithParentID` when initializing the SDK.

**Python SDK**

Create a tunnel:

```python theme={null}
create_tunnel_service = TunnelServiceClient(sdk)
create_tunnel_operation = await create_tunnel_service.create(
    CreateTunnelRequest(
        spec=TunnelSpec(
            title="<tunnel_title>",
        ),
    ),
)
await create_tunnel_operation.wait()
```

In the code, set `title` in `TunnelSpec` to the tunnel title. The code uses the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you set in `parent_id` when initializing the SDK.

**JavaScript SDK**

Create a tunnel:

```ts theme={null}
const createTunnelService = new TunnelService(sdk);
const createTunnelOperation = await createTunnelService.create(
  CreateTunnelRequest.create({
    metadata: ResourceMetadata.create({}),
    spec: TunnelSpec.create({
      title: "<tunnel_title>",
    }),
  }),
).result;
await createTunnelOperation.wait();
```

In the code, set `title` in `TunnelSpec` to the tunnel title. The code uses the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) that you set in `parentId` when initializing the SDK.

After you create a tunnel, you can [connect a service to it](https://docs.nebius.com/tunnels/connect.md) by configuring and running a tunnel agent.
