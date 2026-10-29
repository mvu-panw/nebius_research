# How to delete a tunnel in Nebius Tunnels

Source: https://docs.nebius.com/tunnels/delete

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to delete a tunnel in Nebius Tunnels

When you delete a tunnel, its public service URLs stop working. Deleting a tunnel doesn't delete service accounts, groups, authorized keys, tunnel agent configuration files or virtual machines that you created for the agent.

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

## Deleting a tunnel

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Networking** → **Tunnels**.

2. Click  next to the tunnel that you want to delete and click **Delete**.

3. Confirm the deletion.

**CLI**

1. Get the list of tunnels:

   ```bash theme={null}
   nebius tunnel list
   ```

   In the output, find the tunnel by its title and copy its ID from the `metadata.id` field. The ID has the `applicationtunnel-...` format.

2. Delete the tunnel:

   ```bash theme={null}
   nebius tunnel delete --id <tunnel_ID>
   ```

**Go SDK**

1. Get the list of tunnels:

   ```go theme={null}
   listTunnelsService := sdk.Services().Tunnel().V1().
       Tunnel()
   listTunnels, err := listTunnelsService.List(
       ctx,
       &tunnel.ListTunnelRequest{},
   )
   if err != nil {
       return fmt.Errorf("list tunnels: %w", err)
   }
   fmt.Println(listTunnels)
   ```

   In the output, find the tunnel by its title and copy its ID from `Metadata.Id`. The ID has the `applicationtunnel-...` format.

2. Delete the tunnel:

   ```go theme={null}
   deleteTunnelService := sdk.Services().Tunnel().V1().
       Tunnel()
   deleteTunnelOperation, err := deleteTunnelService.Delete(
       ctx,
       &tunnel.DeleteTunnelRequest{
           Id: "<tunnel_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("delete tunnel: %w", err)
   }
   deleteTunnelOperation, err = deleteTunnelOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for delete tunnel: %w", err)
   }
   ```

   In the code, set `Id` in `DeleteTunnelRequest` to the tunnel ID.

**Python SDK**

1. Get the list of tunnels:

   ```python theme={null}
   list_tunnels_service = TunnelServiceClient(sdk)
   list_tunnels = await list_tunnels_service.list(
       ListTunnelRequest(),
   )
   print(list_tunnels)
   ```

   In the output, find the tunnel by its title and copy its ID from `metadata.id`. The ID has the `applicationtunnel-...` format.

2. Delete the tunnel:

   ```python theme={null}
   delete_tunnel_service = TunnelServiceClient(sdk)
   delete_tunnel_operation = await delete_tunnel_service.delete(
       DeleteTunnelRequest(
           id="<tunnel_ID>",
       ),
   )
   await delete_tunnel_operation.wait()
   ```

   In the code, set `id` in `DeleteTunnelRequest` to the tunnel ID.

**JavaScript SDK**

1. Get the list of tunnels:

   ```ts theme={null}
   const listTunnelsService = new TunnelService(sdk);
   const listTunnels = await listTunnelsService.list(
     ListTunnelRequest.create({}),
   ).result;
   console.log(listTunnels);
   ```

   In the output, find the tunnel by its title and copy its ID from `metadata.id`. The ID has the `applicationtunnel-...` format.

2. Delete the tunnel:

   ```ts theme={null}
   const deleteTunnelService = new TunnelService(sdk);
   const deleteTunnelOperation = await deleteTunnelService.delete(
     DeleteTunnelRequest.create({
       id: "<tunnel_ID>",
     }),
   ).result;
   await deleteTunnelOperation.wait();
   ```

   In the code, set `id` in `DeleteTunnelRequest` to the tunnel ID.

If you created a dedicated service account and a group for the tunnel agent, delete them separately when you no longer need them.
