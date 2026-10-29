# Managing routing tables and routes

Source: https://docs.nebius.com/vpc/routing/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing routing tables and routes

By default, Nebius AI Cloud routes egress traffic from your resources according to the [default routing rules](https://docs.nebius.com/vpc/routing/overview.md#default-routing-rules). You can configure routing by creating and managing routing tables (route tables) and routes. For more details on how routing works, see [Routing in Nebius AI Cloud](https://docs.nebius.com/vpc/routing/overview.md).

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Creating routing tables

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.

2. Select the network for which you want to create a routing table.

   You can only assign a routing table to subnets within this network.

3. Click **Create** and select **Routing table**.

4. In the window that opens:

   1. Enter a name for the routing table.
   2. (Optional) Select the subnets within this network that you want to assign to the routing table. You can also [assign a routing table to subnets](#assigning-routing-tables-to-subnets) later.

5. Click **Create**.
   The new routing table should appear on the **Routing tables** tab.

**CLI**

To create a routing table, run the following command:

```bash theme={null}
nebius vpc route-table create \
  --name <name> \
  --network-id <network_ID>
```

In the command, specify the following parameters:

* `--name`: Name of the routing table.
* `--network-id`: [ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) for which you are creating the routing table. You can only assign a routing table to subnets within this network.

Routing tables are created empty. After creating a routing table, [add routes to it](#adding-routes-to-routing-tables) and then [assign it to subnets](#assigning-routing-tables-to-subnets).

**Go SDK**

Create a routing table:

```go theme={null}
routingTableService := sdk.Services().VPC().V1().
    RouteTable()
routingTableOperation, err := routingTableService.Create(
    ctx,
    &vpc.CreateRouteTableRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<name>",
            ParentId: "<project_ID>",
        },
        Spec: &vpc.RouteTableSpec{
            NetworkId: "<network_ID>",
        },
    },
)
if err != nil {
    return err
}
if _, err = routingTableOperation.Wait(ctx); err != nil {
    return err
}
routeTableID := routingTableOperation.ResourceID()
fmt.Println(routingTableOperation)
```

In the code, set the following parameters:

* `Metadata.Name`: Name of the routing table.
* `Metadata.ParentId`: ID of the project.
* `Spec.NetworkId`: [ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) for which you are creating the routing table. You can only assign a routing table to subnets within this network.

The code saves the routing table ID to `routeTableID`. Routing tables are created empty. After creating a routing table, [add routes to it](#adding-routes-to-routing-tables) and then [assign it to subnets](#assigning-routing-tables-to-subnets).

**Python SDK**

Create a routing table:

```python theme={null}
routing_table_service = RouteTableServiceClient(sdk)
routing_table_operation = await routing_table_service.create(
    CreateRouteTableRequest(
        metadata=ResourceMetadata(
            name="<name>",
            parent_id="<project_ID>",
        ),
        spec=RouteTableSpec(
            network_id="<network_ID>",
        ),
    ),
)
await routing_table_operation.wait()
route_table_id = routing_table_operation.resource_id
print(routing_table_operation)
```

In the code, set the following parameters:

* `name`: Name of the routing table.
* `parent_id`: ID of the project.
* `network_id`: [ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) for which you are creating the routing table. You can only assign a routing table to subnets within this network.

The code saves the routing table ID to `route_table_id`. Routing tables are created empty. After creating a routing table, [add routes to it](#adding-routes-to-routing-tables) and then [assign it to subnets](#assigning-routing-tables-to-subnets).

**JavaScript SDK**

Create a routing table:

```ts theme={null}
const routingTableService = new RouteTableService(sdk);
const routingTableOperation = await routingTableService.create(
  CreateRouteTableRequest.create({
    metadata: {
      name: "<name>",
      parentId: "<project_ID>",
    },
    spec: {
      networkId: "<network_ID>",
    },
  }),
).result;
await routingTableOperation.wait();
const routeTableId = routingTableOperation.resourceId();
console.log(routingTableOperation);
```

In the code, set the following parameters:

* `name`: Name of the routing table.
* `parentId`: ID of the project.
* `networkId`: [ID of the network](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) for which you are creating the routing table. You can only assign a routing table to subnets within this network.

The code saves the routing table ID to `routeTableId`. Routing tables are created empty. After creating a routing table, [add routes to it](#adding-routes-to-routing-tables) and then [assign it to subnets](#assigning-routing-tables-to-subnets).

## Adding routes to routing tables

Routes support different next hop options. You can set the next hop to an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) or to the [internet through the default egress gateway](https://docs.nebius.com/vpc/routing/overview.md#default-egress-gateway). For more information, see [Routing in Nebius AI Cloud](https://docs.nebius.com/vpc/routing/overview.md).

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.

2. Select the network that contains the routing table and switch to the **Routing tables** tab.

3. Select the routing table to which you want to add a route.

4. Click **Add route**.

5. In the window that opens:

   1. Enter a name for the route.

   2. In **Destination CIDR**, do one of the following:

      * To route traffic to an [allocation](https://docs.nebius.com/vpc/overview.md#allocation), specify the CIDR block of destination IP addresses to which the route applies.
      * To route traffic to the internet through the [default egress gateway](https://docs.nebius.com/vpc/routing/overview.md#default-egress-gateway), specify `0.0.0.0/0`.

   3. Under **Next hop**, do one of the following:

      * To route traffic to an allocation, select **Allocation**.
      * To route traffic to the internet, select **Default egress gateway**.

   4. Only if you selected **Allocation** under **Next hop**, select the allocation to route traffic through.

6. Click **Add route**.

**CLI**

* **Routing traffic to an allocation**

  To route traffic to an allocation, run the following command:

  ```bash theme={null}
  nebius vpc route create \
    --name <route_name> \
    --parent-id <routing_table_ID> \
    --destination-cidr <destination_CIDR_block> \
    --next-hop-allocation-id <allocation_ID>
  ```

  In the command, specify the following parameters:

  * `--name`: Name of the route.

  * `--parent-id`: ID of the routing table to add the route to. To get it, run:

    ```bash theme={null}
    nebius vpc route-table list
    ```

    The output contains the routing table ID in the `.metadata.id` parameter.

  * `--destination-cidr`: Specify the CIDR block of destination IP addresses to which the route applies.

  * `--next-hop-allocation-id`: ID of the allocation to route traffic through. To get it, run:

    ```bash theme={null}
    nebius vpc allocation list
    ```

    The output contains the allocation ID in the `.metadata.id` parameter.

* **Routing traffic to the internet**

  To route traffic to the internet through the default egress gateway, run the following command:

  ```bash theme={null}
  nebius vpc route create \
    --name "default-egress" \
    --parent-id <routing_table_ID> \
    --destination-cidr "0.0.0.0/0" \
    --next-hop-default-egress-gateway=true
  ```

  In the command, specify the following parameters:

  * `--name`: Name of the route.

  * `--parent-id`: ID of the routing table to add the route to. To get it, run:

    ```bash theme={null}
    nebius vpc route-table list
    ```

    The output contains the routing table ID in the `.metadata.id` parameter.

  * `--destination-cidr`: Set to `0.0.0.0/0` to route traffic to the internet through the default egress gateway.

  * `--next-hop-default-egress-gateway`: Set to `true` to route traffic through the default egress gateway.

**Go SDK**

* **Routing traffic to an allocation**

  To route traffic to an allocation, create a route:

  ```go theme={null}
  allocationRouteService := sdk.Services().VPC().V1().
      Route()
  allocationRouteOperation, err := allocationRouteService.Create(
      ctx,
      &vpc.CreateRouteRequest{
          Metadata: &common.ResourceMetadata{
              Name: "<route_name>",
              ParentId: "<routing_table_ID>",
          },
          Spec: &vpc.RouteSpec{
              Destination: &vpc.DestinationMatch{
                  Cidr: "<destination_CIDR_block>",
              },
              NextHop: &vpc.NextHop{
                  NextHop: &vpc.NextHop_Allocation{
                      Allocation: &vpc.AllocationNextHop{
                          Id: "<allocation_ID>",
                      },
                  },
              },
          },
      },
  )
  if err != nil {
      return err
  }
  if _, err = allocationRouteOperation.Wait(ctx); err != nil {
      return err
  }
  routeID := allocationRouteOperation.ResourceID()
  fmt.Println(allocationRouteOperation)
  ```

  In the code, set the following parameters:

  * `Metadata.Name`: Name of the route.
  * `Metadata.ParentId`: ID of the routing table to add the route to.
  * `Spec.Destination.Cidr`: CIDR block of destination IP addresses to which the route applies.
  * `Id` under `Spec.NextHop.Allocation`: ID of the allocation to route traffic through.

  The code saves the route ID to `routeID`.

* **Routing traffic to the internet**

  To route traffic to the internet through the default egress gateway, create a route:

  ```go theme={null}
  egressRouteService := sdk.Services().VPC().V1().
      Route()
  egressRouteOperation, err := egressRouteService.Create(
      ctx,
      &vpc.CreateRouteRequest{
          Metadata: &common.ResourceMetadata{
              Name: "default-egress",
              ParentId: "<routing_table_ID>",
          },
          Spec: &vpc.RouteSpec{
              Destination: &vpc.DestinationMatch{
                  Cidr: "0.0.0.0/0",
              },
              NextHop: &vpc.NextHop{
                  NextHop: &vpc.NextHop_DefaultEgressGateway{
                      DefaultEgressGateway: true,
                  },
              },
          },
      },
  )
  if err != nil {
      return err
  }
  if _, err = egressRouteOperation.Wait(ctx); err != nil {
      return err
  }
  fmt.Println(egressRouteOperation)
  ```

  In the code, set the following parameters:

  * `Metadata.Name`: Name of the route.
  * `Metadata.ParentId`: ID of the routing table to add the route to.
  * `Spec.Destination.Cidr`: Set to `0.0.0.0/0` to route traffic to the internet through the default egress gateway.
  * `DefaultEgressGateway` under `Spec.NextHop`: Set to `true` to route traffic through the default egress gateway.

**Python SDK**

* **Routing traffic to an allocation**

  To route traffic to an allocation, create a route:

  ```python theme={null}
  allocation_route_service = RouteServiceClient(sdk)
  allocation_route_operation = await allocation_route_service.create(
      CreateRouteRequest(
          metadata=ResourceMetadata(
              name="<route_name>",
              parent_id="<routing_table_ID>",
          ),
          spec=RouteSpec(
              destination=DestinationMatch(
                  cidr="<destination_CIDR_block>",
              ),
              next_hop=NextHop(
                  allocation=AllocationNextHop(
                      id="<allocation_ID>",
                  ),
              ),
          ),
      ),
  )
  await allocation_route_operation.wait()
  route_id = allocation_route_operation.resource_id
  print(allocation_route_operation)
  ```

  In the code, set the following parameters:

  * `name`: Name of the route.
  * `parent_id`: ID of the routing table to add the route to.
  * `destination.cidr`: CIDR block of destination IP addresses to which the route applies.
  * `next_hop.allocation.id`: ID of the allocation to route traffic through.

  The code saves the route ID to `route_id`.

* **Routing traffic to the internet**

  To route traffic to the internet through the default egress gateway, create a route:

  ```python theme={null}
  egress_route_service = RouteServiceClient(sdk)
  egress_route_operation = await egress_route_service.create(
      CreateRouteRequest(
          metadata=ResourceMetadata(
              name="default-egress",
              parent_id="<routing_table_ID>",
          ),
          spec=RouteSpec(
              destination=DestinationMatch(
                  cidr="0.0.0.0/0",
              ),
              next_hop=NextHop(
                  default_egress_gateway=True,
              ),
          ),
      ),
  )
  await egress_route_operation.wait()
  print(egress_route_operation)
  ```

  In the code, set the following parameters:

  * `name`: Name of the route.
  * `parent_id`: ID of the routing table to add the route to.
  * `destination.cidr`: Set to `0.0.0.0/0` to route traffic to the internet through the default egress gateway.
  * `next_hop.default_egress_gateway`: Set to `True` to route traffic through the default egress gateway.

**JavaScript SDK**

* **Routing traffic to an allocation**

  To route traffic to an allocation, create a route:

  ```ts theme={null}
  const allocationRouteService = new RouteService(sdk);
  const allocationRouteOperation = await allocationRouteService.create(
    CreateRouteRequest.create({
      metadata: {
        name: "<route_name>",
        parentId: "<routing_table_ID>",
      },
      spec: {
        destination: {
          cidr: "<destination_CIDR_block>",
        },
        nextHop: {
          nextHop: {
            "$case": "allocation",
            "allocation": {
              id: "<allocation_ID>",
            },
          },
        },
      },
    }),
  ).result;
  await allocationRouteOperation.wait();
  const routeId = allocationRouteOperation.resourceId();
  console.log(allocationRouteOperation);
  ```

  In the code, set the following parameters:

  * `name`: Name of the route.
  * `parentId`: ID of the routing table to add the route to.
  * `destination.cidr`: CIDR block of destination IP addresses to which the route applies.
  * `id` under `nextHop.allocation`: ID of the allocation to route traffic through.

  The code saves the route ID to `routeId`.

* **Routing traffic to the internet**

  To route traffic to the internet through the default egress gateway, create a route:

  ```ts theme={null}
  const egressRouteService = new RouteService(sdk);
  const egressRouteOperation = await egressRouteService.create(
    CreateRouteRequest.create({
      metadata: {
        name: "default-egress",
        parentId: "<routing_table_ID>",
      },
      spec: {
        destination: {
          cidr: "0.0.0.0/0",
        },
        nextHop: {
          nextHop: {
            "$case": "defaultEgressGateway",
            "defaultEgressGateway": true,
          },
        },
      },
    }),
  ).result;
  await egressRouteOperation.wait();
  console.log(egressRouteOperation);
  ```

  In the code, set the following parameters:

  * `name`: Name of the route.
  * `parentId`: ID of the routing table to add the route to.
  * `destination.cidr`: Set to `0.0.0.0/0` to route traffic to the internet through the default egress gateway.
  * `defaultEgressGateway` under `nextHop`: Set to `true` to route traffic through the default egress gateway.

## Deleting routes

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Select the network that contains the routing table and switch to the **Routing tables** tab.
3. Select the routing table from which you want to delete a route.
4. Do one of the following:

   * To delete one route, click  next to the route and select **Delete**.
   * To delete multiple routes at once, select the checkboxes next to the required routes and click **Delete** in the banner that appears.

**CLI**

To delete a route from a routing table, run the following command:

```bash theme={null}
nebius vpc route delete <route_ID>
```

In the command, specify the route ID to delete. To get it, do the following:

1. Get the ID of the routing table:

   ```bash theme={null}
   nebius vpc route-table list
   ```

   The output contains the routing table ID in the `.metadata.id` parameter.

2. Use this ID to list all the routes in that routing table:

   ```bash theme={null}
   nebius vpc route list --parent-id <routing_table_ID>
   ```

   The output contains the route ID in the `.metadata.id` parameter.

**Go SDK**

Delete a route from a routing table:

```go theme={null}
deletedRouteService := sdk.Services().VPC().V1().
    Route()
deletedRouteOperation, err := deletedRouteService.Delete(
    ctx,
    &vpc.DeleteRouteRequest{
        Id: "<route_ID>",
    },
)
if err != nil {
    return err
}
if _, err = deletedRouteOperation.Wait(ctx); err != nil {
    return err
}
```

Set `Id` to the ID of the route that you want to delete.

**Python SDK**

Delete a route from a routing table:

```python theme={null}
deleted_route_service = RouteServiceClient(sdk)
deleted_route_operation = await deleted_route_service.delete(
    DeleteRouteRequest(
        id="<route_ID>",
    ),
)
await deleted_route_operation.wait()
```

Set `id` to the ID of the route that you want to delete.

**JavaScript SDK**

Delete a route from a routing table:

```ts theme={null}
const deletedRouteService = new RouteService(sdk);
const deletedRouteOperation = await deletedRouteService.delete(
  DeleteRouteRequest.create({
    id: "<route_ID>",
  }),
).result;
await deletedRouteOperation.wait();
```

Set `id` to the ID of the route that you want to delete.

If you delete all routes in a routing table, resources in subnets that have this routing table assigned can only communicate with other resources within their network. All traffic to private IP addresses outside the network and to public IP addresses is discarded.

## Assigning routing tables to subnets

You can only assign a routing table to subnets within the network that the routing table is associated with. After you assign a routing table to a subnet, egress traffic from all resources in the subnet is routed according to the routing table.

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Switch to the **Subnets** tab.
3. Select the subnet to which you want to assign a routing table.
4. On the **Settings** tab, select a routing table from the **Routing table** drop-down list.
5. Click **Save changes**.

**CLI**

To assign a routing table to a subnet, run the following command:

```bash theme={null}
nebius vpc subnet update <subnet_ID> \
  --route-table-id <routing_table_ID>
```

In the command, specify the following parameters:

* `<subnet_ID>`: ID of the subnet to assign the routing table to. To get it, run:

  ```bash theme={null}
  nebius vpc subnet list
  ```

  The output contains the subnet ID in the `.metadata.id` parameter.

* `--route-table-id`: ID of the routing table to assign to the subnet. To get it, run:

  ```bash theme={null}
  nebius vpc route-table list
  ```

  The output contains the routing table ID in the `.metadata.id` parameter.

**Go SDK**

Assign a routing table to a subnet:

```go theme={null}
assignedSubnetService := sdk.Services().VPC().V1().
    Subnet()
assignedSubnet, err := assignedSubnetService.Get(
    ctx,
    &vpc.GetSubnetRequest{
        Id: "<subnet_ID>",
    },
)
if err != nil {
    return err
}
assignedSubnet.Spec.RouteTableId = "<routing_table_ID>"
assignedSubnetOperation, err := assignedSubnetService.Update(
    ctx,
    &vpc.UpdateSubnetRequest{
        Metadata: assignedSubnet.Metadata,
        Spec: assignedSubnet.Spec,
    },
)
if err != nil {
    return err
}
if _, err = assignedSubnetOperation.Wait(ctx); err != nil {
    return err
}
```

In the code, set the following parameters:

* `Id`: ID of the subnet to assign the routing table to.
* `Spec.RouteTableId`: ID of the routing table to assign to the subnet.

The code gets the subnet, sets the routing table in its specification and updates the subnet.

**Python SDK**

Assign a routing table to a subnet:

```python theme={null}
assigned_subnet_service = SubnetServiceClient(sdk)
assigned_subnet = await assigned_subnet_service.get(
    GetSubnetRequest(
        id="<subnet_ID>",
    ),
)
assigned_subnet.spec.route_table_id = "<routing_table_ID>"
assigned_subnet_operation = await assigned_subnet_service.update(
    UpdateSubnetRequest(
        metadata=assigned_subnet.metadata,
        spec=assigned_subnet.spec,
    ),
)
await assigned_subnet_operation.wait()
```

In the code, set the following parameters:

* `id`: ID of the subnet to assign the routing table to.
* `spec.route_table_id`: ID of the routing table to assign to the subnet.

The code gets the subnet, sets the routing table in its specification and updates the subnet.

**JavaScript SDK**

Assign a routing table to a subnet:

```ts theme={null}
const assignedSubnetService = new SubnetService(sdk);
const assignedSubnet = await assignedSubnetService.get(
  GetSubnetRequest.create({
    id: "<subnet_ID>",
  }),
).result;
assignedSubnet.spec.routeTableId = "<routing_table_ID>";
const assignedSubnetOperation = await assignedSubnetService.update(
  UpdateSubnetRequest.create({
    metadata: assignedSubnet.metadata,
    spec: assignedSubnet.spec,
  }),
).result;
await assignedSubnetOperation.wait();
```

In the code, set the following parameters:

* `id`: ID of the subnet to assign the routing table to.
* `spec.routeTableId`: ID of the routing table to assign to the subnet.

The code gets the subnet, sets the routing table in its specification and updates the subnet.

## Reverting subnets to the parent network's default routing table

If you no longer want to apply custom routing to a subnet, you can unassign its custom routing table. After this, the subnet uses its parent network's default routing table.

**Web console**

To assign the subnet to its parent network's default routing table:

1. Find the parent network's default routing table:
   1. In the sidebar, go to  **Networking** → **Virtual Networks**.
   2. In the list of networks, select the network to which the subnet belongs.
   3. Switch to the **Routing tables** tab. The default routing table has a **Default** label next to its name.
2. Assign the default routing table to the subnet:
   1. Switch to the **Subnets** tab.
   2. Select the subnet that you want to revert to the default routing table.
   3. On the **Settings** tab, select the default routing table from the **Routing table** drop-down list.
   4. Click **Save changes**.

Alternatively, you can [delete](#deleting-routing-tables) the custom routing table if you no longer need it. When you delete the routing table, you can choose the option to use the default routing table for the subnet.

**CLI**

To revert a subnet to its parent network's default routing table, run the following command:

```bash theme={null}
nebius vpc subnet update <subnet_ID> \
  --route-table-id ""
```

In the command, specify the subnet ID. To get it, run:

```bash theme={null}
nebius vpc subnet list
```

After you run this command, the subnet uses its parent network's default routing table.

**Go SDK**

Revert a subnet to its parent network's default routing table:

```go theme={null}
revertedSubnetService := sdk.Services().VPC().V1().
    Subnet()
revertedSubnet, err := revertedSubnetService.Get(
    ctx,
    &vpc.GetSubnetRequest{
        Id: "<subnet_ID>",
    },
)
if err != nil {
    return err
}
revertedSubnet.Spec.RouteTableId = ""
revertedSubnetOperation, err := revertedSubnetService.Update(
    ctx,
    &vpc.UpdateSubnetRequest{
        Metadata: revertedSubnet.Metadata,
        Spec: revertedSubnet.Spec,
    },
)
if err != nil {
    return err
}
if _, err = revertedSubnetOperation.Wait(ctx); err != nil {
    return err
}
```

Set `Id` to the subnet ID. The code sets `Spec.RouteTableId` to an empty string and updates the subnet. After this, the subnet uses its parent network's default routing table.

**Python SDK**

Revert a subnet to its parent network's default routing table:

```python theme={null}
reverted_subnet_service = SubnetServiceClient(sdk)
reverted_subnet = await reverted_subnet_service.get(
    GetSubnetRequest(
        id="<subnet_ID>",
    ),
)
reverted_subnet.spec.route_table_id = ""
reverted_subnet_operation = await reverted_subnet_service.update(
    UpdateSubnetRequest(
        metadata=reverted_subnet.metadata,
        spec=reverted_subnet.spec,
    ),
)
await reverted_subnet_operation.wait()
```

Set `id` to the subnet ID. The code sets `spec.route_table_id` to an empty string and updates the subnet. After this, the subnet uses its parent network's default routing table.

**JavaScript SDK**

Revert a subnet to its parent network's default routing table:

```ts theme={null}
const revertedSubnetService = new SubnetService(sdk);
const revertedSubnet = await revertedSubnetService.get(
  GetSubnetRequest.create({
    id: "<subnet_ID>",
  }),
).result;
revertedSubnet.spec.routeTableId = "";
const revertedSubnetOperation = await revertedSubnetService.update(
  UpdateSubnetRequest.create({
    metadata: revertedSubnet.metadata,
    spec: revertedSubnet.spec,
  }),
).result;
await revertedSubnetOperation.wait();
```

Set `id` to the subnet ID. The code sets `spec.routeTableId` to an empty string and updates the subnet. After this, the subnet uses its parent network's default routing table.

## Resetting default routing tables of networks

[Reverting to the default routing table](#reverting-subnets-to-the-parent-networks-default-routing-table) means that the [default routing rules](https://docs.nebius.com/vpc/routing/overview.md#default-routing-rules) apply to the subnet again, unless you have modified the default routing table. If you modified it, you can make the default routing table implement the default routing rules again. To do this, bring it to the state described in [Default routing tables](https://docs.nebius.com/vpc/routing/overview.md#default-routing-tables):

**Web console**

If you added new routes to the default routing table, you can delete them to reset the default routing table.

1. In the sidebar, go to  **Networking** → **Virtual Networks**.

2. Select the network whose default routing table you want to reset.

3. Switch to the **Routing tables** tab.

4. Select the routing table that is labeled **Default**.

5. In the routes list, check whether there is a route whose **Destination CIDR** value is `0.0.0.0/0`.

6. If there is no such route:

   1. Click **Add route**.

   2. In the window that opens:

      1. Specify a name for the route.
      2. In **Destination CIDR**, enter `0.0.0.0/0`.
      3. Under **Next hop**, select **Default egress gateway**.

   3. Click **Add route**.

7. [Delete](#deleting-routes) all other routes from the default routing table.

**CLI**

1. Get the ID of the default routing table:

   ```bash theme={null}
   nebius vpc network list
   ```

   The output contains the ID in the `.status.default_route_table_id` parameter.

2. List the table's routes:

   ```bash theme={null}
   nebius vpc route list --parent-id <default_routing_table_ID>
   ```

3. If the table doesn't contain a route to the internet through the default egress gateway for all egress traffic (CIDR block `0.0.0.0/0`) as described in [Default routing tables](https://docs.nebius.com/vpc/routing/overview.md#default-routing-tables), add it:

   ```bash theme={null}
   nebius vpc route create \
     --name <route_name> \
     --parent-id <routing_table_ID> \
     --destination-cidr "0.0.0.0/0" \
     --next-hop-default-egress-gateway=true
   ```

4. [Delete](#deleting-routes) all other routes from the default routing table.

**Go SDK**

1. Get the ID of the default routing table. List the networks in the project, with `ParentId` set to the project ID:

   ```go theme={null}
   routingNetworksService := sdk.Services().VPC().V1().
       Network()
   routingNetworksResponse, err := routingNetworksService.List(
       ctx,
       &vpc.ListNetworksRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(routingNetworksResponse)
   ```

   The response contains the ID in `Status.DefaultRouteTableId` of each network.

2. List the table's routes. Set `ParentId` to the default routing table ID:

   ```go theme={null}
   defaultRoutesService := sdk.Services().VPC().V1().
       Route()
   defaultRoutesResponse, err := defaultRoutesService.List(
       ctx,
       &vpc.ListRoutesRequest{
           ParentId: "<default_routing_table_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(defaultRoutesResponse)
   ```

3. If the table doesn't contain a route to the internet through the default egress gateway for all egress traffic (CIDR block `0.0.0.0/0`) as described in [Default routing tables](https://docs.nebius.com/vpc/routing/overview.md#default-routing-tables), add it. Set `Metadata.Name` to the route name and `Metadata.ParentId` to the default routing table ID:

   ```go theme={null}
   defaultRouteService := sdk.Services().VPC().V1().
       Route()
   defaultRouteOperation, err := defaultRouteService.Create(
       ctx,
       &vpc.CreateRouteRequest{
           Metadata: &common.ResourceMetadata{
               Name: "<route_name>",
               ParentId: "<routing_table_ID>",
           },
           Spec: &vpc.RouteSpec{
               Destination: &vpc.DestinationMatch{
                   Cidr: "0.0.0.0/0",
               },
               NextHop: &vpc.NextHop{
                   NextHop: &vpc.NextHop_DefaultEgressGateway{
                       DefaultEgressGateway: true,
                   },
               },
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = defaultRouteOperation.Wait(ctx); err != nil {
       return err
   }
   fmt.Println(defaultRouteOperation)
   ```

4. [Delete](#deleting-routes) all other routes from the default routing table.

**Python SDK**

1. Get the ID of the default routing table. List the networks in the project, with `parent_id` set to the project ID:

   ```python theme={null}
   routing_networks_service = NetworkServiceClient(sdk)
   routing_networks_response = await routing_networks_service.list(
       ListNetworksRequest(
           parent_id="<project_ID>",
       ),
   )
   print(routing_networks_response)
   ```

   The response contains the ID in `status.default_route_table_id` of each network.

2. List the table's routes. Set `parent_id` to the default routing table ID:

   ```python theme={null}
   default_routes_service = RouteServiceClient(sdk)
   default_routes_response = await default_routes_service.list(
       ListRoutesRequest(
           parent_id="<default_routing_table_ID>",
       ),
   )
   print(default_routes_response)
   ```

3. If the table doesn't contain a route to the internet through the default egress gateway for all egress traffic (CIDR block `0.0.0.0/0`) as described in [Default routing tables](https://docs.nebius.com/vpc/routing/overview.md#default-routing-tables), add it. Set `name` to the route name and `parent_id` to the default routing table ID:

   ```python theme={null}
   default_route_service = RouteServiceClient(sdk)
   default_route_operation = await default_route_service.create(
       CreateRouteRequest(
           metadata=ResourceMetadata(
               name="<route_name>",
               parent_id="<routing_table_ID>",
           ),
           spec=RouteSpec(
               destination=DestinationMatch(
                   cidr="0.0.0.0/0",
               ),
               next_hop=NextHop(
                   default_egress_gateway=True,
               ),
           ),
       ),
   )
   await default_route_operation.wait()
   print(default_route_operation)
   ```

4. [Delete](#deleting-routes) all other routes from the default routing table.

**JavaScript SDK**

1. Get the ID of the default routing table. List the networks in the project, with `parentId` set to the project ID:

   ```ts theme={null}
   const routingNetworksService = new NetworkService(sdk);
   const routingNetworksResponse = await routingNetworksService.list(
     ListNetworksRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(routingNetworksResponse);
   ```

   The response contains the ID in `status.defaultRouteTableId` of each network.

2. List the table's routes. Set `parentId` to the default routing table ID:

   ```ts theme={null}
   const defaultRoutesService = new RouteService(sdk);
   const defaultRoutesResponse = await defaultRoutesService.list(
     ListRoutesRequest.create({
       parentId: "<default_routing_table_ID>",
     }),
   ).result;
   console.log(defaultRoutesResponse);
   ```

3. If the table doesn't contain a route to the internet through the default egress gateway for all egress traffic (CIDR block `0.0.0.0/0`) as described in [Default routing tables](https://docs.nebius.com/vpc/routing/overview.md#default-routing-tables), add it. Set `name` to the route name and `parentId` to the default routing table ID:

   ```ts theme={null}
   const defaultRouteService = new RouteService(sdk);
   const defaultRouteOperation = await defaultRouteService.create(
     CreateRouteRequest.create({
       metadata: {
         name: "<route_name>",
         parentId: "<routing_table_ID>",
       },
       spec: {
         destination: {
           cidr: "0.0.0.0/0",
         },
         nextHop: {
           nextHop: {
             "$case": "defaultEgressGateway",
             "defaultEgressGateway": true,
           },
         },
       },
     }),
   ).result;
   await defaultRouteOperation.wait();
   console.log(defaultRouteOperation);
   ```

4. [Delete](#deleting-routes) all other routes from the default routing table.

## Deleting routing tables

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Select the network from which you want to delete the routing table and switch to the **Routing tables** tab.
3. Click  next to the routing table you want to delete.
4. In the window that opens:
   * If the routing table is not assigned to any subnets, confirm the deletion.
   * If the routing table is assigned to a subnet, select a new routing table for the subnet or choose the option to use the default routing table, then confirm the deletion.

**CLI**

> [!WARNING]
>
> You can only delete custom routing tables that are not assigned to any subnet. Before deleting a routing table, [assign other routing tables](#assigning-routing-tables-to-subnets) to this table's subnets or [revert these subnets to defaults](#reverting-subnets-to-the-parent-networks-default-routing-table).

To delete a routing table, run the following command:

```bash theme={null}
nebius vpc route-table delete <routing_table_ID>
```

In the command, specify the ID of the routing table. To get it, run:

```bash theme={null}
nebius vpc route-table list
```

**Go SDK**

> [!WARNING]
>
> You can only delete custom routing tables that are not assigned to any subnet. Before deleting a routing table, [assign other routing tables](#assigning-routing-tables-to-subnets) to this table's subnets or [revert these subnets to defaults](#reverting-subnets-to-the-parent-networks-default-routing-table).

Delete a routing table:

```go theme={null}
deletedTableService := sdk.Services().VPC().V1().
    RouteTable()
deletedTableOperation, err := deletedTableService.Delete(
    ctx,
    &vpc.DeleteRouteTableRequest{
        Id: "<routing_table_ID>",
    },
)
if err != nil {
    return err
}
if _, err = deletedTableOperation.Wait(ctx); err != nil {
    return err
}
```

Set `Id` to the ID of the routing table.

**Python SDK**

> [!WARNING]
>
> You can only delete custom routing tables that are not assigned to any subnet. Before deleting a routing table, [assign other routing tables](#assigning-routing-tables-to-subnets) to this table's subnets or [revert these subnets to defaults](#reverting-subnets-to-the-parent-networks-default-routing-table).

Delete a routing table:

```python theme={null}
deleted_table_service = RouteTableServiceClient(sdk)
deleted_table_operation = await deleted_table_service.delete(
    DeleteRouteTableRequest(
        id="<routing_table_ID>",
    ),
)
await deleted_table_operation.wait()
```

Set `id` to the ID of the routing table.

**JavaScript SDK**

> [!WARNING]
>
> You can only delete custom routing tables that are not assigned to any subnet. Before deleting a routing table, [assign other routing tables](#assigning-routing-tables-to-subnets) to this table's subnets or [revert these subnets to defaults](#reverting-subnets-to-the-parent-networks-default-routing-table).

Delete a routing table:

```ts theme={null}
const deletedTableService = new RouteTableService(sdk);
const deletedTableOperation = await deletedTableService.delete(
  DeleteRouteTableRequest.create({
    id: "<routing_table_ID>",
  }),
).result;
await deletedTableOperation.wait();
```

Set `id` to the ID of the routing table.
