# Getting network and subnet IDs for Nebius AI Cloud resources

Source: https://docs.nebius.com/vpc/networking/resources

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting network and subnet IDs for Nebius AI Cloud resources

When you create Nebius AI Cloud resources by using the [Nebius AI Cloud CLI](https://docs.nebius.com/cli/index.md), the [Terraform provider](https://docs.nebius.com/terraform-provider/index.md) or the [API](https://docs.nebius.com/grpc-api/index.md), you need to specify the ID of the [network](https://docs.nebius.com/vpc/overview.md#network) or [subnet](https://docs.nebius.com/vpc/overview.md#subnet).

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

> [!NOTE]
>
> If you are in a group with the `viewer` role, you can get the IDs but cannot create any Nebius AI Cloud resources.

## How to get a network ID

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. To copy the network ID, click the  icon next to the required ID.

**CLI**

* If you know the name of the network, use the `get-by-name` command:

  ```bash theme={null}
  nebius vpc network get-by-name --name <network_name>
  ```

* If you do not know the exact name of the network, use the `list` command to view a list of available networks:

  ```bash theme={null}
  nebius vpc network list
  ```

You can find the ID in the `metadata.id` parameter of the output.

**Go SDK**

In the code, set `ParentId` to the ID of the project that contains the network.

* If you know the name of the network, get it by name. Set `Name` to the network name:

  ```go theme={null}
  namedNetworkService := sdk.Services().VPC().V1().
      Network()
  namedNetwork, err := namedNetworkService.GetByName(
      ctx,
      &vpc.GetNetworkByNameRequest{
          ParentId: "<project_ID>",
          Name: "<network_name>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(namedNetwork)
  ```

* If you do not know the exact name of the network, list the available networks:

  ```go theme={null}
  networksService := sdk.Services().VPC().V1().
      Network()
  networksResponse, err := networksService.List(
      ctx,
      &vpc.ListNetworksRequest{
          ParentId: "<project_ID>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(networksResponse)
  ```

The response contains the network ID in `Metadata.Id`. In a list response, each network in `Items` has its ID in `Metadata.Id`.

**Python SDK**

In the code, set `parent_id` to the ID of the project that contains the network.

* If you know the name of the network, get it by name. Set `name` to the network name:

  ```python theme={null}
  named_network_service = NetworkServiceClient(sdk)
  named_network = await named_network_service.get_by_name(
      GetNetworkByNameRequest(
          parent_id="<project_ID>",
          name="<network_name>",
      ),
  )
  print(named_network)
  ```

* If you do not know the exact name of the network, list the available networks:

  ```python theme={null}
  networks_service = NetworkServiceClient(sdk)
  networks_response = await networks_service.list(
      ListNetworksRequest(
          parent_id="<project_ID>",
      ),
  )
  print(networks_response)
  ```

The response contains the network ID in `metadata.id`. In a list response, each network in `items` has its ID in `metadata.id`.

**JavaScript SDK**

In the code, set `parentId` to the ID of the project that contains the network.

* If you know the name of the network, get it by name. Set `name` to the network name:

  ```ts theme={null}
  const namedNetworkService = new NetworkService(sdk);
  const namedNetwork = await namedNetworkService.getByName(
    GetNetworkByNameRequest.create({
      parentId: "<project_ID>",
      name: "<network_name>",
    }),
  ).result;
  console.log(namedNetwork);
  ```

* If you do not know the exact name of the network, list the available networks:

  ```ts theme={null}
  const networksService = new NetworkService(sdk);
  const networksResponse = await networksService.list(
    ListNetworksRequest.create({
      parentId: "<project_ID>",
    }),
  ).result;
  console.log(networksResponse);
  ```

The response contains the network ID in `metadata.id`. In a list response, each network in `items` has its ID in `metadata.id`.

## How to get a subnet ID

**Web console**

1. In the sidebar, go to  **Networking** → **Virtual Networks**.
2. Switch to the **Subnets** tab.
3. To copy the subnet ID, click the  icon next to the required ID.

**CLI**

* If you know the name of the subnet, use the `get-by-name` command:

  ```bash theme={null}
  nebius vpc subnet get-by-name --name <subnet_name>
  ```

* If you do not know the exact name of the subnet, use the `list` command to view a list of available subnets:

  ```bash theme={null}
  nebius vpc subnet list
  ```

You can find the ID in the `metadata.id` parameter of the output.

**Go SDK**

In the code, set `ParentId` to the ID of the project that contains the subnet.

* If you know the name of the subnet, get it by name. Set `Name` to the subnet name:

  ```go theme={null}
  namedSubnetService := sdk.Services().VPC().V1().
      Subnet()
  namedSubnet, err := namedSubnetService.GetByName(
      ctx,
      &vpc.GetSubnetByNameRequest{
          ParentId: "<project_ID>",
          Name: "<subnet_name>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(namedSubnet)
  ```

* If you do not know the exact name of the subnet, list the available subnets:

  ```go theme={null}
  subnetsService := sdk.Services().VPC().V1().
      Subnet()
  subnetsResponse, err := subnetsService.List(
      ctx,
      &vpc.ListSubnetsRequest{
          ParentId: "<project_ID>",
      },
  )
  if err != nil {
      return err
  }
  fmt.Println(subnetsResponse)
  ```

The response contains the subnet ID in `Metadata.Id`. In a list response, each subnet in `Items` has its ID in `Metadata.Id`.

**Python SDK**

In the code, set `parent_id` to the ID of the project that contains the subnet.

* If you know the name of the subnet, get it by name. Set `name` to the subnet name:

  ```python theme={null}
  named_subnet_service = SubnetServiceClient(sdk)
  named_subnet = await named_subnet_service.get_by_name(
      GetSubnetByNameRequest(
          parent_id="<project_ID>",
          name="<subnet_name>",
      ),
  )
  print(named_subnet)
  ```

* If you do not know the exact name of the subnet, list the available subnets:

  ```python theme={null}
  subnets_service = SubnetServiceClient(sdk)
  subnets_response = await subnets_service.list(
      ListSubnetsRequest(
          parent_id="<project_ID>",
      ),
  )
  print(subnets_response)
  ```

The response contains the subnet ID in `metadata.id`. In a list response, each subnet in `items` has its ID in `metadata.id`.

**JavaScript SDK**

In the code, set `parentId` to the ID of the project that contains the subnet.

* If you know the name of the subnet, get it by name. Set `name` to the subnet name:

  ```ts theme={null}
  const namedSubnetService = new SubnetService(sdk);
  const namedSubnet = await namedSubnetService.getByName(
    GetSubnetByNameRequest.create({
      parentId: "<project_ID>",
      name: "<subnet_name>",
    }),
  ).result;
  console.log(namedSubnet);
  ```

* If you do not know the exact name of the subnet, list the available subnets:

  ```ts theme={null}
  const subnetsService = new SubnetService(sdk);
  const subnetsResponse = await subnetsService.list(
    ListSubnetsRequest.create({
      parentId: "<project_ID>",
    }),
  ).result;
  console.log(subnetsResponse);
  ```

The response contains the subnet ID in `metadata.id`. In a list response, each subnet in `items` has its ID in `metadata.id`.
