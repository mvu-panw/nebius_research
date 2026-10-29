# How to create a fixed set of public IP addresses for a node group

Source: https://docs.nebius.com/kubernetes/networking/defined-ips

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create a fixed set of public IP addresses for a node group

When you enable public IP addresses for nodes in a node group, the IP addresses are dynamically assigned from the general pool of public IP addresses managed by Nebius AI Cloud. The assigned addresses may change when nodes are recreated or updated.

If you need a fixed set of public IP addresses—for example, to configure firewall rules, define an allowlist, register DNS records or integrate external systems—create a subnet with a dedicated public IP address range. While individual node IP addresses may still change, they will always be selected from the range defined in this subnet.

## Prerequisites

1. Set up the interface that you are going to use:

   **CLI**

   [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   **Go SDK**

   [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

   **Python SDK**

   [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

   **JavaScript SDK**

   [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. Make sure that you have enough quota on IP addresses to support your node group [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters). You can check the quota on the [Administration → Limits → Quotas](https://console.nebius.com/quota) page of the web console.

   By default, no additional public IP addresses are required during an update. If you configure a surge-based strategy, reserve enough extra public IP addresses for the additional nodes that can be created during the update. Otherwise, updates or upgrades can stop when trying to create a new node.

## How to create a fixed set of IP addresses

To create a fixed set of public IP addresses for a node group, create a subnet with a dedicated public IP address pool and configure the node group to use this subnet:

1. Create a subnet with public IP address CIDRs:

   **CLI**

   ```bash theme={null}
   nebius vpc subnet create \
     --name <subnet_name> \
     --network-id <network_ID> \
     --ipv4-public-pools-use-network-pools=false \
     --ipv4-public-pools-pools='[
     {
       "cidrs": [
         {"cidr": "/32"},
         {"cidr": "/32"},
         {"cidr": "/32"}
       ]
     }]'
   ```

   Specify the following parameters:

   * `name`: Name of the subnet with a dedicated set of IP addresses.
   * `network-id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).
   * `ipv4-public-pools-pools.cidrs`: One or more IPv4 [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). The number of these blocks defines how many public IP addresses the subnet has. The nodes in the node group receive these addresses randomly. In the example, three CIDR blocks are defined, each with one public IP address.

   In the output, copy the `metadata.id` value — this is the subnet ID.

   **Go SDK**

   ```go theme={null}
   subnetOperation, err := sdk.Services().VPC().V1().
       Subnet().Create(
           ctx,
           &vpc.CreateSubnetRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<subnet_name>",
               },
               Spec: &vpc.SubnetSpec{
                   NetworkId: "<network_ID>",
                   Ipv4PublicPools: &vpc.IPv4PublicSubnetPools{
                       UseNetworkPools: false,
                       Pools: []*vpc.SubnetPool{
                           {
                               Cidrs: []*vpc.SubnetCidr{
                                   {Cidr: "/32"},
                                   {Cidr: "/32"},
                                   {Cidr: "/32"},
                               },
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = subnetOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Specify the following parameters:

   * `Metadata.Name`: Name of the subnet with a dedicated set of IP addresses.
   * `Spec.NetworkId`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).
   * `Spec.Ipv4PublicPools.Pools.Cidrs`: One or more IPv4 [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). The number of these blocks defines how many public IP addresses the subnet has. The nodes in the node group receive these addresses randomly. In the example, three CIDR blocks are defined, each with one public IP address.

   To get the subnet ID, call `subnetOperation.ResourceID()`.

   **Python SDK**

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnet_operation = await subnet_service.create(
       CreateSubnetRequest(
           metadata=ResourceMetadata(name="<subnet_name>"),
           spec=SubnetSpec(
               network_id="<network_ID>",
               ipv4_public_pools=IPv4PublicSubnetPools(
                   use_network_pools=False,
                   pools=[
                       SubnetPool(
                           cidrs=[
                               SubnetCidr(cidr="/32"),
                               SubnetCidr(cidr="/32"),
                               SubnetCidr(cidr="/32"),
                           ],
                       ),
                   ],
               ),
           ),
       ),
   )
   await subnet_operation.wait()
   ```

   Specify the following parameters:

   * `metadata.name`: Name of the subnet with a dedicated set of IP addresses.
   * `spec.network_id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).
   * `spec.ipv4_public_pools.pools.cidrs`: One or more IPv4 [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). The number of these blocks defines how many public IP addresses the subnet has. The nodes in the node group receive these addresses randomly. In the example, three CIDR blocks are defined, each with one public IP address.

   To get the subnet ID, read `subnet_operation.resource_id`.

   **JavaScript SDK**

   ```ts theme={null}
   const subnetService = new SubnetService(sdk);
   const subnetOperation = await subnetService.create(
     CreateSubnetRequest.create({
       metadata: ResourceMetadata.create({
         name: "<subnet_name>",
       }),
       spec: SubnetSpec.create({
         networkId: "<network_ID>",
         ipv4PublicPools: IPv4PublicSubnetPools.create({
           useNetworkPools: false,
           pools: [
             SubnetPool.create({
               cidrs: [
                 SubnetCidr.create({ cidr: "/32" }),
                 SubnetCidr.create({ cidr: "/32" }),
                 SubnetCidr.create({ cidr: "/32" }),
               ],
             }),
           ],
         }),
       }),
     }),
   ).result;
   await subnetOperation.wait();
   ```

   Specify the following parameters:

   * `metadata.name`: Name of the subnet with a dedicated set of IP addresses.
   * `spec.networkId`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).
   * `spec.ipv4PublicPools.pools.cidrs`: One or more IPv4 [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). The number of these blocks defines how many public IP addresses the subnet has. The nodes in the node group receive these addresses randomly. In the example, three CIDR blocks are defined, each with one public IP address.

   To get the subnet ID, call `subnetOperation.resourceId()`.

2. [Create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) that uses the new subnet and assigns public IP addresses to the nodes:

   **CLI**

   Specify the new subnet ID in the `--template-network-interfaces` parameter:

   ```bash theme={null}
   nebius mk8s node-group create \
     ... \
     --template-network-interfaces "[{\"public_ip_address\": {}, \"subnet_id\": \"<subnet_ID>\"}]"
   ```

   **Go SDK**

   Specify the new subnet ID in `SubnetId` and add `PublicIpAddress` in `Spec.Template.NetworkInterfaces`:

   ```go theme={null}
   nodeGroupOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Create(
           ctx,
           &mk8s.CreateNodeGroupRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: mk8sClusterID,
                   Name:     "defined-ips-test",
               },
               Spec: &mk8s.NodeGroupSpec{
                   Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                       FixedNodeCount: 1,
                   },
                   Template: &mk8s.NodeTemplate{
                       Resources: &mk8s.ResourcesSpec{
                           Platform: "cpu-d3",
                           Size: &mk8s.ResourcesSpec_Preset{
                               Preset: "4vcpu-16gb",
                           },
                       },
                       NetworkInterfaces:
                           []*mk8s.NetworkInterfaceTemplate{
                           {
                               PublicIpAddress: &mk8s.PublicIPAddress{},
                               SubnetId:         "<subnet_ID>",
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = nodeGroupOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   `ParentId` reads the `mk8sClusterID` variable. Assign the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) to it before you run the code.

   **Python SDK**

   Specify the new subnet ID in `subnet_id` and add `public_ip_address` in `spec.template.network_interfaces`:

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group_operation = await node_group_service.create(
       CreateNodeGroupRequest(
           metadata=ResourceMetadata(
               parent_id=mk8s_cluster_id,
               name="defined-ips-test",
           ),
           spec=NodeGroupSpec(
               fixed_node_count=1,
               template=NodeTemplate(
                   resources=ResourcesSpec(
                       platform="cpu-d3",
                       preset="4vcpu-16gb",
                   ),
                   network_interfaces=[
                       NetworkInterfaceTemplate(
                           public_ip_address=PublicIPAddress(),
                           subnet_id="<subnet_ID>",
                       ),
                   ],
               ),
           ),
       ),
   )
   await node_group_operation.wait()
   ```

   `parent_id` reads the `mk8s_cluster_id` variable. Assign the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) to it before you run the code.

   **JavaScript SDK**

   Specify the new subnet ID in `subnetId` and add `publicIpAddress` in `spec.template.networkInterfaces`:

   ```ts theme={null}
   const nodeGroupService = new NodeGroupService(sdk);
   const nodeGroupOperation = await nodeGroupService.create(
     CreateNodeGroupRequest.create({
       metadata: ResourceMetadata.create({
         parentId: mk8sClusterId,
         name: "defined-ips-test",
       }),
       spec: NodeGroupSpec.create({
         size: {
           $case: "fixedNodeCount",
           fixedNodeCount: 1,
         },
         template: NodeTemplate.create({
           resources: ResourcesSpec.create({
             platform: "cpu-d3",
             size: {
               $case: "preset",
               preset: "4vcpu-16gb",
             },
           }),
           networkInterfaces: [
             NetworkInterfaceTemplate.create({
               publicIpAddress: PublicIPAddress.create({}),
               subnetId: "<subnet_ID>",
             }),
           ],
         }),
       }),
     }),
   ).result;
   await nodeGroupOperation.wait();
   ```

   `parentId` reads the `mk8sClusterId` variable. Assign the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) to it before you run the code.

   This configuration assigns random public IP addresses from the CIDR blocks defined in the subnet.

Now, the nodes in the node group get public IP addresses from the dedicated set. This enables you to predefine a fixed range of IP addresses for use in an allowlist or for DNS mapping, even if individual IP addresses are reassigned across nodes.
