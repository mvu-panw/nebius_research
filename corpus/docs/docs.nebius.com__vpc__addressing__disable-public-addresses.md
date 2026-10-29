# Disabling public addresses for a subnet

Source: https://docs.nebius.com/vpc/addressing/disable-public-addresses

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Disabling public addresses for a subnet

In some scenarios, you may need to ensure that some of your Nebius AI Cloud resources cannot be reached from the internet. For example, you may want to set up a secure zone and connect to it from a demilitarized zone (DMZ) via a [jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md). To do so, you can [create a subnet](#creating-a-subnet-without-public-ip-addresses) that cannot allocate public IP addresses. Resources in such a subnet can only have private IP addresses.

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

## Creating a subnet without public IP addresses

**CLI**

1. Choose a network that has at least one private [pool](https://docs.nebius.com/vpc/overview.md#pool). You can get information about available networks by using the following command:

   ```bash theme={null}
   nebius vpc network list
   ```

   In the output, check the `metadata.spec.ipv4_private_pools` parameter to determine whether a network has private pools. Save the ID of the required network for the next command.

2. Create a subnet that doesn't use the network's public pools, and save the subnet's ID to an environment variable:

   ```bash theme={null}
   export PRIVATE_SUBNET_ID=$(nebius vpc subnet create \
     --name <private_subnet> \
     --network-id <network_ID> \
     --ipv4-public-pools-use-network-pools=False \
     --format jsonpath='{.metadata.id}')
   ```

   In this command, specify the subnet name and the copied network ID.

3. To check that public addresses are disabled in this subnet, try to create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) of a public IP address in this subnet:

   ```bash theme={null}
   nebius vpc allocation create \
     --name <public_allocation> \
     --ipv4-public-subnet-id $PRIVATE_SUBNET_ID
   ```

   This command returns an error, indicating that the subnet doesn't support public allocations. This is expected and confirms that the subnet is configured correctly.

**Go SDK**

1. Choose a network that has at least one private [pool](https://docs.nebius.com/vpc/overview.md#pool). List the available networks in the project, with `ParentId` set to the project ID:

   ```go theme={null}
   availableNetworksService := sdk.Services().VPC().V1().
       Network()
   availableNetworksResponse, err := availableNetworksService.List(
       ctx,
       &vpc.ListNetworksRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(availableNetworksResponse)
   ```

   In the response, check `Spec.Ipv4PrivatePools` of each network to determine whether it has private pools. Save the ID of the required network from `Metadata.Id`.

2. Create a subnet that doesn't use the network's public pools:

   ```go theme={null}
   privateSubnetService := sdk.Services().VPC().V1().
       Subnet()
   privateSubnetOperation, err := privateSubnetService.Create(
       ctx,
       &vpc.CreateSubnetRequest{
           Metadata: &common.ResourceMetadata{
               Name: "<private_subnet>",
               ParentId: "<project_ID>",
           },
           Spec: &vpc.SubnetSpec{
               NetworkId: "<network_ID>",
               Ipv4PublicPools: &vpc.IPv4PublicSubnetPools{
                   UseNetworkPools: false,
               },
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = privateSubnetOperation.Wait(ctx); err != nil {
       return err
   }
   privateSubnetID := privateSubnetOperation.ResourceID()
   ```

   In the code, set the following parameters:

   * `Metadata.Name`: Name of the subnet.
   * `Metadata.ParentId`: ID of the project.
   * `Spec.NetworkId`: Network ID that you saved in the previous step.

   `Spec.Ipv4PublicPools.UseNetworkPools` is set to `false`, so the subnet doesn't use the network's public pools. The code saves the subnet ID to `privateSubnetID`.

3. To check that public addresses are disabled in this subnet, try to create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) of a public IP address in this subnet:

   ```go theme={null}
   publicAllocationService := sdk.Services().VPC().V1().
       Allocation()
   publicOperation, err := publicAllocationService.Create(
       ctx,
       &vpc.CreateAllocationRequest{
           Metadata: &common.ResourceMetadata{
               Name: "<public_allocation>",
               ParentId: "<project_ID>",
           },
           Spec: &vpc.AllocationSpec{
               IpSpec: &vpc.AllocationSpec_Ipv4Public{
                   Ipv4Public: &vpc.IPv4PublicAllocationSpec{
                       Pool: &vpc.IPv4PublicAllocationSpec_SubnetId{
                           SubnetId: "<private_subnet_ID>",
                       },
                   },
               },
           },
       },
   )
   if err != nil {
       return err
   }
   _, err = publicOperation.Wait(ctx)
   return err
   ```

   Set `SubnetId` to the ID of the new subnet. The code returns an error, indicating that the subnet doesn't support public allocations. This is expected and confirms that the subnet is configured correctly.

**Python SDK**

1. Choose a network that has at least one private [pool](https://docs.nebius.com/vpc/overview.md#pool). List the available networks in the project, with `parent_id` set to the project ID:

   ```python theme={null}
   available_networks_service = NetworkServiceClient(sdk)
   available_networks_response = await available_networks_service.list(
       ListNetworksRequest(
           parent_id="<project_ID>",
       ),
   )
   print(available_networks_response)
   ```

   In the response, check `spec.ipv4_private_pools` of each network to determine whether it has private pools. Save the ID of the required network from `metadata.id`.

2. Create a subnet that doesn't use the network's public pools:

   ```python theme={null}
   private_subnet_service = SubnetServiceClient(sdk)
   private_subnet_operation = await private_subnet_service.create(
       CreateSubnetRequest(
           metadata=ResourceMetadata(
               name="<private_subnet>",
               parent_id="<project_ID>",
           ),
           spec=SubnetSpec(
               network_id="<network_ID>",
               ipv4_public_pools=IPv4PublicSubnetPools(
                   use_network_pools=False,
               ),
           ),
       ),
   )
   await private_subnet_operation.wait()
   private_subnet_id = private_subnet_operation.resource_id
   ```

   In the code, set the following parameters:

   * `name`: Name of the subnet.
   * `parent_id`: ID of the project.
   * `network_id`: Network ID that you saved in the previous step.

   `ipv4_public_pools.use_network_pools` is set to `False`, so the subnet doesn't use the network's public pools. The code saves the subnet ID to `private_subnet_id`.

3. To check that public addresses are disabled in this subnet, try to create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) of a public IP address in this subnet:

   ```python theme={null}
   public_allocation_service = AllocationServiceClient(sdk)
   try:
       public_operation = await public_allocation_service.create(
           CreateAllocationRequest(
               metadata=ResourceMetadata(
                   name="<public_allocation>",
                   parent_id="<project_ID>",
               ),
               spec=AllocationSpec(
                   ipv4_public=IPv4PublicAllocationSpec(
                       subnet_id="<private_subnet_ID>",
                   ),
               ),
           ),
       )
       await public_operation.wait()
   except RequestError as error:
       print(error)

   ```

   Set `subnet_id` to the ID of the new subnet. The code prints an error, indicating that the subnet doesn't support public allocations. This is expected and confirms that the subnet is configured correctly.

**JavaScript SDK**

1. Choose a network that has at least one private [pool](https://docs.nebius.com/vpc/overview.md#pool). List the available networks in the project, with `parentId` set to the project ID:

   ```ts theme={null}
   const availableNetworksService = new NetworkService(sdk);
   const availableNetworksResponse = await availableNetworksService.list(
     ListNetworksRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(availableNetworksResponse);
   ```

   In the response, check `spec.ipv4PrivatePools` of each network to determine whether it has private pools. Save the ID of the required network from `metadata.id`.

2. Create a subnet that doesn't use the network's public pools:

   ```ts theme={null}
   const privateSubnetService = new SubnetService(sdk);
   const privateSubnetOperation = await privateSubnetService.create(
     CreateSubnetRequest.create({
       metadata: {
         name: "<private_subnet>",
         parentId: "<project_ID>",
       },
       spec: {
         networkId: "<network_ID>",
         ipv4PublicPools: {
           useNetworkPools: false,
         },
       },
     }),
   ).result;
   await privateSubnetOperation.wait();
   const privateSubnetId = privateSubnetOperation.resourceId();
   ```

   In the code, set the following parameters:

   * `name`: Name of the subnet.
   * `parentId`: ID of the project.
   * `networkId`: Network ID that you saved in the previous step.

   `ipv4PublicPools.useNetworkPools` is set to `false`, so the subnet doesn't use the network's public pools. The code saves the subnet ID to `privateSubnetId`.

3. To check that public addresses are disabled in this subnet, try to create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) of a public IP address in this subnet:

   ```ts theme={null}
   const publicAllocationService = new AllocationService(sdk);
   try {
     const publicOperation = await publicAllocationService.create(
       CreateAllocationRequest.create({
         metadata: {
           name: "<public_allocation>",
           parentId: "<project_ID>",
         },
         spec: {
           ipSpec: {
             "$case": "ipv4Public",
             "ipv4Public": {
               pool: {
                 "$case": "subnetId",
                 "subnetId": "<private_subnet_ID>",
               },
             },
           },
         },
       }),
     ).result;
     await publicOperation.wait();
   } catch (error) {
     console.error(error);
   }
   ```

   Set `subnetId` to the ID of the new subnet. The code logs an error, indicating that the subnet doesn't support public allocations. This is expected and confirms that the subnet is configured correctly.

Use this subnet to create resources that should not be reachable from the internet. These resources have only private IP addresses that can be accessed from within the same network. You can create a virtual machine with a public IP address within the same network, but outside the private subnet, and use this virtual machine as a jump server for external connections.

> [!NOTE]
>
> Disabling public addresses only blocks inbound traffic from the internet. Resources in the subnet can still send outbound (egress) traffic to the internet through the [default egress gateway](https://docs.nebius.com/vpc/routing/overview.md#default-egress-gateway).
