# Isolating Nebius AI Cloud resources in separate networks

Source: https://docs.nebius.com/vpc/networking/isolation

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Isolating Nebius AI Cloud resources in separate networks

Nebius AI Cloud resources within one [network](https://docs.nebius.com/vpc/overview.md#network) can connect directly to each other by using their private IP addresses. If you want to disable connectivity between resources or allocate the same private IP address to multiple different resources, for example, for testing purposes, create separate networks for them.

## Prerequisites

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

## Creating a network and a subnet

Each network must contain at least one [subnet](https://docs.nebius.com/vpc/overview.md#subnet). To create a network and a subnet within it:

**CLI**

Run the following command:

```bash theme={null}
export NETWORK_ID=$(nebius vpc network create \
   --name <network_name> \
   --format jsonpath='{.metadata.id}')
export SUBNET_ID=$(nebius vpc subnet create \
   --name <subnet_name> \
   --network-id $NETWORK_ID \
   --format jsonpath='{.metadata.id}')
```

This command saves the IDs of the created network and subnet to environment variables that you can use to create resources.

**Go SDK**

```go theme={null}
isolatedNetworkService := sdk.Services().VPC().V1().
    Network()
isolatedNetworkOperation, err := isolatedNetworkService.Create(
    ctx,
    &vpc.CreateNetworkRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<network_name>",
            ParentId: "<project_ID>",
        },
        Spec: &vpc.NetworkSpec{},
    },
)
if err != nil {
    return err
}
if _, err = isolatedNetworkOperation.Wait(ctx); err != nil {
    return err
}
isolatedSubnetService := sdk.Services().VPC().V1().
    Subnet()
isolatedSubnetOperation, err := isolatedSubnetService.Create(
    ctx,
    &vpc.CreateSubnetRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<subnet_name>",
            ParentId: "<project_ID>",
        },
        Spec: &vpc.SubnetSpec{
            NetworkId: isolatedNetworkOperation.ResourceID(),
        },
    },
)
if err != nil {
    return err
}
if _, err = isolatedSubnetOperation.Wait(ctx); err != nil {
    return err
}
```

In the code, set the following parameters for both resources:

* `Metadata.Name`: Name of the network or subnet.
* `Metadata.ParentId`: [ID of the project](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3) to create the resources in.

The code creates the network first and passes its ID from `isolatedNetworkOperation.ResourceID()` to the subnet's `Spec.NetworkId`. To get the subnet ID for creating resources, use `isolatedSubnetOperation.ResourceID()`.

**Python SDK**

```python theme={null}
isolated_network_service = NetworkServiceClient(sdk)
isolated_network_operation = await isolated_network_service.create(
    CreateNetworkRequest(
        metadata=ResourceMetadata(
            name="<network_name>",
            parent_id="<project_ID>",
        ),
        spec=NetworkSpec(),
    ),
)
await isolated_network_operation.wait()
isolated_subnet_service = SubnetServiceClient(sdk)
isolated_subnet_operation = await isolated_subnet_service.create(
    CreateSubnetRequest(
        metadata=ResourceMetadata(
            name="<subnet_name>",
            parent_id="<project_ID>",
        ),
        spec=SubnetSpec(
            network_id=isolated_network_operation.resource_id,
        ),
    ),
)
await isolated_subnet_operation.wait()
```

In the code, set the following parameters for both resources:

* `name`: Name of the network or subnet.
* `parent_id`: [ID of the project](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3) to create the resources in.

The code creates the network first and passes its ID from `isolated_network_operation.resource_id` to the subnet's `network_id`. To get the subnet ID for creating resources, use `isolated_subnet_operation.resource_id`.

**JavaScript SDK**

```ts theme={null}
const isolatedNetworkService = new NetworkService(sdk);
const isolatedNetworkOperation = await isolatedNetworkService.create(
  CreateNetworkRequest.create({
    metadata: {
      name: "<network_name>",
      parentId: "<project_ID>",
    },
    spec: {},
  }),
).result;
await isolatedNetworkOperation.wait();
const isolatedSubnetService = new SubnetService(sdk);
const isolatedSubnetOperation = await isolatedSubnetService.create(
  CreateSubnetRequest.create({
    metadata: {
      name: "<subnet_name>",
      parentId: "<project_ID>",
    },
    spec: {
      networkId: isolatedNetworkOperation.resourceId(),
    },
  }),
).result;
await isolatedSubnetOperation.wait();
```

In the code, set the following parameters for both resources:

* `name`: Name of the network or subnet.
* `parentId`: [ID of the project](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3) to create the resources in.

The code creates the network first and passes its ID from `isolatedNetworkOperation.resourceId()` to the subnet's `networkId`. To get the subnet ID for creating resources, use `isolatedSubnetOperation.resourceId()`.

## Adding resources to a network or subnet

> [!WARNING]
>
> Set the required network or subnet when you create Nebius AI Cloud resources. You cannot move a resource to another network or subnet after creation.

When you create resources by using the Nebius AI Cloud CLI, set the network or subnet by using parameters with `network-id` or `subnet-id` in them. For example:

* When you [create a Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), add the `--network-interfaces "[{\"subnet_id\": \"$SUBNET_ID\"}]"` parameter.
* When you [create a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters), add the `--control-plane-subnet-id $SUBNET_ID` parameter.
* When you [create a Managed Service for PostgreSQL® cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-create-clusters), add the `--network-id $NETWORK_ID` parameter.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
