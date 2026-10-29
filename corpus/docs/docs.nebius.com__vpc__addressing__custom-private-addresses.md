# Allocating custom private addresses to resources

Source: https://docs.nebius.com/vpc/addressing/custom-private-addresses

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Allocating custom private addresses to resources

By default, Nebius AI Cloud [networks](https://docs.nebius.com/vpc/overview.md#network) and [subnets](https://docs.nebius.com/vpc/overview.md#subnet) provide private IP addresses from specific [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks). These blocks depend on the network's or subnet's region. If you need private addresses outside these blocks, add the required CIDR block to one of the network's [pools](https://docs.nebius.com/vpc/overview.md#pool), or create a new pool and add it to the network. A pool must belong to the network before its addresses can be used in that network's subnets. Next, create a subnet with that CIDR block in the network. As a result, you can allocate random or specific addresses from this block in the required network or subnet.

## Prerequisites

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Install [jq](https://jqlang.github.io/jq/) to extract IDs and tokens from the JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
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

## How to allocate addresses

The CIDR block that you choose must fall within the [RFC 1918](https://datatracker.ietf.org/doc/html/rfc1918#section-3) private address ranges: `10.0.0.0/8`, `172.16.0.0/12` or `192.168.0.0/16`. The block must not overlap with CIDR blocks already used by other pools or subnets in the network, or with external networks the VM reaches over a [Nebius VPN Gateway](https://docs.nebius.com/vpc/nebius-vpn-gateway.md).

> [!NOTE]
>
> When you choose a custom CIDR block, do not use `172.17.0.0/16`. It conflicts with the Docker default bridge network and can make virtual machines unreachable. For more information, see [Virtual machine is unreachable due to a Docker subnet conflict](https://docs.nebius.com/compute/virtual-machines/docker-subnet-conflict.md).

**CLI**

1. Determine what CIDR block you need and save it to an environment variable:

   ```bash theme={null}
   export CUSTOM_SUBNET_CIDR=<CIDR_block>
   ```

2. Get the ID of the required network and save it to an environment variable:

   ```bash theme={null}
   export NETWORK_ID=$(nebius vpc network get-by-name \
     --name <network_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Get the ID of this network's private pool and save it to an environment variable:

   ```bash theme={null}
   export PRIVATE_POOL_ID=$(nebius vpc network get \
     --id $NETWORK_ID \
     --format jsonpath='{.spec.ipv4_private_pools.pools[0].id}')
   ```

   As this command contains `pools[0]`, it saves the ID of the private pool that goes first in the network specification. If you need a different pool, specify its index in `pools[<index>]`. To check the order of pools, run `nebius vpc network list`.

4. Add the `CUSTOM_SUBNET_CIDR` block to the private pool with `PRIVATE_POOL_ID`:

   ```bash theme={null}
   echo $(nebius vpc pool get --id $PRIVATE_POOL_ID --format json | \
     jq '.spec.cidrs += [{"cidr":$ENV.CUSTOM_SUBNET_CIDR}] |
     {metadata: .metadata, spec: .spec}') | \
     nebius vpc pool update -
   ```

5. Create a new subnet with this private pool and save the subnet ID to an environment variable:

   ```bash theme={null}
   export SUBNET_ID=$(nebius vpc subnet create \
     --name private_subnet \
     --network-id $NETWORK_ID \
     --ipv4-private-pools-pools "[{\"cidrs\":[{\"cidr\":\"$CUSTOM_SUBNET_CIDR\"}]}]" \
     --format jsonpath='{.metadata.id}')
   ```

6. (Optional) To assign the VM a specific IP address, create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) within this subnet and save its ID to an environment variable:

   ```bash theme={null}
   export ALLOCATION_ID=$(nebius vpc allocation create \
     --name private_allocation \
     --ipv4-private-subnet-id $SUBNET_ID \
     --ipv4-private-cidr <IP_address> \
     --format jsonpath='{.metadata.id}')
   ```

   The `--ipv4-private-cidr` parameter sets the IP address for the allocation. Make sure that this address is within the subnet's CIDR block. Without this parameter, the command creates an allocation with a random IP address from the subnet.

7. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) in the new subnet:

   ```bash theme={null}
   nebius compute instance create \
     --name <VM_name> \
     --stopped=<true|false> \
     --resources-platform <platform> \
     --resources-preset <preset> \
     --boot-disk-existing-disk-id <boot_disk_ID> \
     --boot-disk-attach-mode READ_WRITE \
     --network-interfaces '[{"name": "<network_interface_name>", "subnet_id": "<subnet_ID>", "ip_address": {}, "public_ip_address": {}}]'
   ```

   The VM is assigned a private IP address from the subnet's pool. To assign the specific address from the allocation instead, set `ip_address` to `{"allocation_id": "$ALLOCATION_ID"}` inside the `--network-interfaces` parameter. If you later delete the VM, you can reuse the allocation for another VM.

**Go SDK**

1. Determine what CIDR block you need. In the following steps, specify it as `<CIDR_block>`.

2. Get the ID of the required network:

   ```go theme={null}
   customNetworkService := sdk.Services().VPC().V1().
       Network()
   customNetwork, err := customNetworkService.GetByName(
       ctx,
       &vpc.GetNetworkByNameRequest{
           ParentId: "<project_ID>",
           Name: "<network_name>",
       },
   )
   if err != nil {
       return err
   }
   networkID := customNetwork.Metadata.Id
   ```

   Set `ParentId` to the project ID and `Name` to the network name. The code saves the network ID from `Metadata.Id` to `networkID`.

3. Get the ID of this network's private pool:

   ```go theme={null}
   poolNetworkService := sdk.Services().VPC().V1().
       Network()
   poolNetwork, err := poolNetworkService.Get(
       ctx,
       &vpc.GetNetworkRequest{
           Id: "<network_ID>",
       },
   )
   if err != nil {
       return err
   }
   privatePoolID := poolNetwork.Spec.Ipv4PrivatePools.Pools[0].Id
   ```

   Set `Id` to the network ID. As the code reads `Spec.Ipv4PrivatePools.Pools[0].Id`, it saves the ID of the private pool that goes first in the network specification to `privatePoolID`. If you need a different pool, specify its index in `Pools[<index>]`.

4. Add the CIDR block to the private pool:

   ```go theme={null}
   customPoolService := sdk.Services().VPC().V1().
       Pool()
   customPool, err := customPoolService.Get(
       ctx,
       &vpc.GetPoolRequest{
           Id: "<pool_ID>",
       },
   )
   if err != nil {
       return err
   }
   customPool.Spec.Cidrs = append(
       customPool.Spec.Cidrs,
       &vpc.PoolCidr{Cidr: "<CIDR_block>"},
   )
   poolUpdateOperation, err := customPoolService.Update(
       ctx,
       &vpc.UpdatePoolRequest{
           Metadata: customPool.Metadata,
           Spec: customPool.Spec,
       },
   )
   if err != nil {
       return err
   }
   if _, err = poolUpdateOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set `Id` to the private pool ID and `Cidr` to the CIDR block. The code appends the block to the pool's `Spec.Cidrs` and updates the pool.

5. Create a new subnet with this private pool:

   ```go theme={null}
   customSubnetService := sdk.Services().VPC().V1().
       Subnet()
   customSubnetOperation, err := customSubnetService.Create(
       ctx,
       &vpc.CreateSubnetRequest{
           Metadata: &common.ResourceMetadata{
               Name: "private_subnet",
               ParentId: "<project_ID>",
           },
           Spec: &vpc.SubnetSpec{
               NetworkId: "<network_ID>",
               Ipv4PrivatePools: &vpc.IPv4PrivateSubnetPools{
                   Pools: []*vpc.SubnetPool{
                       &vpc.SubnetPool{
                           Cidrs: []*vpc.SubnetCidr{
                               &vpc.SubnetCidr{
                                   Cidr: "<CIDR_block>",
                               },
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
   if _, err = customSubnetOperation.Wait(ctx); err != nil {
       return err
   }
   subnetID := customSubnetOperation.ResourceID()
   ```

   Set `Metadata.ParentId` to the project ID, `Spec.NetworkId` to the network ID and `Cidr` under `Spec.Ipv4PrivatePools` to the CIDR block. The code saves the subnet ID to `subnetID`.

6. (Optional) To assign the VM a specific IP address, create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) within this subnet:

   ```go theme={null}
   customIpService := sdk.Services().VPC().V1().
       Allocation()
   customIpOperation, err := customIpService.Create(
       ctx,
       &vpc.CreateAllocationRequest{
           Metadata: &common.ResourceMetadata{
               Name: "private_allocation",
               ParentId: "<project_ID>",
           },
           Spec: &vpc.AllocationSpec{
               IpSpec: &vpc.AllocationSpec_Ipv4Private{
                   Ipv4Private: &vpc.IPv4PrivateAllocationSpec{
                       Pool: &vpc.IPv4PrivateAllocationSpec_SubnetId{
                           SubnetId: "<subnet_ID>",
                       },
                       Cidr: "<IP_address>",
                   },
               },
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = customIpOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Set `Metadata.ParentId` to the project ID and `SubnetId` to the subnet ID. `Cidr` under `Spec.IpSpec` sets the IP address for the allocation. Make sure that this address is within the subnet's CIDR block. Without `Cidr`, the code creates an allocation with a random IP address from the subnet. To get the allocation ID, use `customIpOperation.ResourceID()`.

7. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) in the new subnet:

   ```go theme={null}
   privateInstanceService := sdk.Services().Compute().V1().
       Instance()
   privateInstanceOperation, err := privateInstanceService.Create(
       ctx,
       &compute.CreateInstanceRequest{
           Metadata: &common.ResourceMetadata{
               Name: "<VM_name>",
               ParentId: "<project_ID>",
           },
           Spec: &compute.InstanceSpec{
               Resources: &compute.ResourcesSpec{
                   Platform: "<platform>",
                   Size: &compute.ResourcesSpec_Preset{
                       Preset: "<preset>",
                   },
               },
               BootDisk: &compute.AttachedDiskSpec{
                   AttachMode: compute.AttachedDiskSpec_READ_WRITE,
                   Type: &compute.AttachedDiskSpec_ExistingDisk{
                       ExistingDisk: &compute.ExistingDisk{
                           Id: "<boot_disk_ID>",
                       },
                   },
               },
               NetworkInterfaces: []*compute.NetworkInterfaceSpec{
       &compute.NetworkInterfaceSpec{
           Name: "<network_interface_name>",
           SubnetId: "<subnet_ID>",
           IpAddress: &compute.IPAddress{},
           PublicIpAddress: &compute.PublicIPAddress{},
       },
   },
               Stopped: <true|false>,
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = privateInstanceOperation.Wait(ctx); err != nil {
       return err
   }
   fmt.Println(privateInstanceOperation)
   ```

   In the code, set the following parameters:

   * `Metadata.Name`: Name of the VM.
   * `Metadata.ParentId`: ID of the project.
   * `Spec.Resources.Platform` and `Preset` under `Spec.Resources.Size`: VM [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `Id` under `Spec.BootDisk`: ID of the boot disk.
   * `Name` under `Spec.NetworkInterfaces`: Name of the network interface.
   * `SubnetId`: ID of the new subnet.
   * `Spec.Stopped`: Whether to create the VM in the stopped state, `true` or `false`.

   The VM is assigned a private IP address from the subnet's pool. To assign the specific address from the allocation instead, set `IpAddress` to `&compute.IPAddress{AllocationId: "<allocation_ID>"}`. If you later delete the VM, you can reuse the allocation for another VM.

**Python SDK**

1. Determine what CIDR block you need. In the following steps, specify it as `<CIDR_block>`.

2. Get the ID of the required network:

   ```python theme={null}
   custom_network_service = NetworkServiceClient(sdk)
   custom_network = await custom_network_service.get_by_name(
       GetNetworkByNameRequest(
           parent_id="<project_ID>",
           name="<network_name>",
       ),
   )
   network_id = custom_network.metadata.id
   ```

   Set `parent_id` to the project ID and `name` to the network name. The code saves the network ID from `metadata.id` to `network_id`.

3. Get the ID of this network's private pool:

   ```python theme={null}
   pool_network_service = NetworkServiceClient(sdk)
   pool_network = await pool_network_service.get(
       GetNetworkRequest(
           id="<network_ID>",
       ),
   )
   private_pool_id = pool_network.spec.ipv4_private_pools.pools[0].id
   ```

   Set `id` to the network ID. As the code reads `spec.ipv4_private_pools.pools[0].id`, it saves the ID of the private pool that goes first in the network specification to `private_pool_id`. If you need a different pool, specify its index in `pools[<index>]`.

4. Add the CIDR block to the private pool:

   ```python theme={null}
   custom_pool_service = PoolServiceClient(sdk)
   custom_pool = await custom_pool_service.get(
       GetPoolRequest(
           id="<pool_ID>",
       ),
   )
   custom_pool.spec.cidrs.append(
       PoolCidr(cidr="<CIDR_block>"),
   )
   pool_update_operation = await custom_pool_service.update(
       UpdatePoolRequest(
           metadata=custom_pool.metadata,
           spec=custom_pool.spec,
       ),
   )
   await pool_update_operation.wait()
   ```

   Set `id` to the private pool ID and `cidr` to the CIDR block. The code appends the block to the pool's `spec.cidrs` and updates the pool.

5. Create a new subnet with this private pool:

   ```python theme={null}
   custom_subnet_service = SubnetServiceClient(sdk)
   custom_subnet_operation = await custom_subnet_service.create(
       CreateSubnetRequest(
           metadata=ResourceMetadata(
               name="private_subnet",
               parent_id="<project_ID>",
           ),
           spec=SubnetSpec(
               network_id="<network_ID>",
               ipv4_private_pools=IPv4PrivateSubnetPools(
                   pools=[
                       SubnetPool(
                           cidrs=[
                               SubnetCidr(
                                   cidr="<CIDR_block>",
                               ),
                           ],
                       ),
                   ],
               ),
           ),
       ),
   )
   await custom_subnet_operation.wait()
   subnet_id = custom_subnet_operation.resource_id
   ```

   Set `parent_id` to the project ID, `network_id` to the network ID and `cidr` under `ipv4_private_pools` to the CIDR block. The code saves the subnet ID to `subnet_id`.

6. (Optional) To assign the VM a specific IP address, create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) within this subnet:

   ```python theme={null}
   custom_ip_service = AllocationServiceClient(sdk)
   custom_ip_operation = await custom_ip_service.create(
       CreateAllocationRequest(
           metadata=ResourceMetadata(
               name="private_allocation",
               parent_id="<project_ID>",
           ),
           spec=AllocationSpec(
               ipv4_private=IPv4PrivateAllocationSpec(
                   subnet_id="<subnet_ID>",
                   cidr="<IP_address>",
               ),
           ),
       ),
   )
   await custom_ip_operation.wait()
   ```

   Set `parent_id` to the project ID and `subnet_id` to the subnet ID. `cidr` under `ipv4_private` sets the IP address for the allocation. Make sure that this address is within the subnet's CIDR block. Without `cidr`, the code creates an allocation with a random IP address from the subnet. To get the allocation ID, use `custom_ip_operation.resource_id`.

7. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) in the new subnet:

   ```python theme={null}
   private_instance_service = InstanceServiceClient(sdk)
   private_instance_operation = await private_instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(
               name="<VM_name>",
               parent_id="<project_ID>",
           ),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="<platform>",
                   preset="<preset>",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(
                       id="<boot_disk_ID>",
                   ),
               ),
               network_interfaces=[
       NetworkInterfaceSpec(
           name="<network_interface_name>",
           subnet_id="<subnet_ID>",
           ip_address=IPAddress(),
           public_ip_address=PublicIPAddress(),
       ),
   ],
               stopped=<True|False>,
           ),
       ),
   )
   await private_instance_operation.wait()
   print(private_instance_operation)
   ```

   In the code, set the following parameters:

   * `metadata.name`: Name of the VM.
   * `metadata.parent_id`: ID of the project.
   * `resources.platform` and `resources.preset`: VM [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `existing_disk.id`: ID of the boot disk.
   * `name` under `network_interfaces`: Name of the network interface.
   * `subnet_id`: ID of the new subnet.
   * `stopped`: Whether to create the VM in the stopped state, `True` or `False`.

   The VM is assigned a private IP address from the subnet's pool. To assign the specific address from the allocation instead, set `ip_address` to `IPAddress(allocation_id="<allocation_ID>")`. If you later delete the VM, you can reuse the allocation for another VM.

**JavaScript SDK**

1. Determine what CIDR block you need. In the following steps, specify it as `<CIDR_block>`.

2. Get the ID of the required network:

   ```ts theme={null}
   const customNetworkService = new NetworkService(sdk);
   const customNetwork = await customNetworkService.getByName(
     GetNetworkByNameRequest.create({
       parentId: "<project_ID>",
       name: "<network_name>",
     }),
   ).result;
   const networkId = customNetwork.metadata.id;
   ```

   Set `parentId` to the project ID and `name` to the network name. The code saves the network ID from `metadata.id` to `networkId`.

3. Get the ID of this network's private pool:

   ```ts theme={null}
   const poolNetworkService = new NetworkService(sdk);
   const poolNetwork = await poolNetworkService.get(
     GetNetworkRequest.create({
       id: "<network_ID>",
     }),
   ).result;
   const privatePoolId = poolNetwork.spec.ipv4PrivatePools.pools[0].id;
   ```

   Set `id` to the network ID. As the code reads `spec.ipv4PrivatePools.pools[0].id`, it saves the ID of the private pool that goes first in the network specification to `privatePoolId`. If you need a different pool, specify its index in `pools[<index>]`.

4. Add the CIDR block to the private pool:

   ```ts theme={null}
   const customPoolService = new PoolService(sdk);
   const customPool = await customPoolService.get(
     GetPoolRequest.create({
       id: "<pool_ID>",
     }),
   ).result;
   customPool.spec.cidrs.push(
     PoolCidr.create({ cidr: "<CIDR_block>" }),
   );
   const poolUpdateOperation = await customPoolService.update(
     UpdatePoolRequest.create({
       metadata: customPool.metadata,
       spec: customPool.spec,
     }),
   ).result;
   await poolUpdateOperation.wait();
   ```

   Set `id` to the private pool ID and `cidr` to the CIDR block. The code appends the block to the pool's `spec.cidrs` and updates the pool.

5. Create a new subnet with this private pool:

   ```ts theme={null}
   const customSubnetService = new SubnetService(sdk);
   const customSubnetOperation = await customSubnetService.create(
     CreateSubnetRequest.create({
       metadata: {
         name: "private_subnet",
         parentId: "<project_ID>",
       },
       spec: {
         networkId: "<network_ID>",
         ipv4PrivatePools: {
           pools: [
             {
               cidrs: [
                 {
                   cidr: "<CIDR_block>",
                 },
               ],
             },
           ],
         },
       },
     }),
   ).result;
   await customSubnetOperation.wait();
   const subnetId = customSubnetOperation.resourceId();
   ```

   Set `parentId` to the project ID, `networkId` to the network ID and `cidr` under `ipv4PrivatePools` to the CIDR block. The code saves the subnet ID to `subnetId`.

6. (Optional) To assign the VM a specific IP address, create an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) within this subnet:

   ```ts theme={null}
   const customIpService = new AllocationService(sdk);
   const customIpOperation = await customIpService.create(
     CreateAllocationRequest.create({
       metadata: {
         name: "private_allocation",
         parentId: "<project_ID>",
       },
       spec: {
         ipSpec: {
           "$case": "ipv4Private",
           "ipv4Private": {
             pool: {
               "$case": "subnetId",
               "subnetId": "<subnet_ID>",
             },
             cidr: "<IP_address>",
           },
         },
       },
     }),
   ).result;
   await customIpOperation.wait();
   ```

   Set `parentId` to the project ID and `subnetId` to the subnet ID. `cidr` under `ipv4Private` sets the IP address for the allocation. Make sure that this address is within the subnet's CIDR block. Without `cidr`, the code creates an allocation with a random IP address from the subnet. To get the allocation ID, use `customIpOperation.resourceId()`.

7. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) in the new subnet:

   ```ts theme={null}
   const privateInstanceService = new InstanceService(sdk);
   const privateInstanceOperation = await privateInstanceService.create(
     CreateInstanceRequest.create({
       metadata: {
         name: "<VM_name>",
         parentId: "<project_ID>",
       },
       spec: {
         resources: {
           platform: "<platform>",
           size: {
             "$case": "preset",
             "preset": "<preset>",
           },
         },
         bootDisk: {
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             "$case": "existingDisk",
             "existingDisk": {
               id: "<boot_disk_ID>",
             },
           },
         },
         networkInterfaces: [
     {
       name: "<network_interface_name>",
       subnetId: "<subnet_ID>",
       ipAddress: {},
       publicIpAddress: {},
     },
   ],
         stopped: <true|false>,
       },
     }),
   ).result;
   await privateInstanceOperation.wait();
   console.log(privateInstanceOperation);
   ```

   In the code, set the following parameters:

   * `metadata.name`: Name of the VM.
   * `metadata.parentId`: ID of the project.
   * `resources.platform` and `preset` under `resources.size`: VM [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `existingDisk.id`: ID of the boot disk.
   * `name` under `networkInterfaces`: Name of the network interface.
   * `subnetId`: ID of the new subnet.
   * `stopped`: Whether to create the VM in the stopped state, `true` or `false`.

   The VM is assigned a private IP address from the subnet's pool. To assign the specific address from the allocation instead, set `ipAddress` to `{ allocationId: "<allocation_ID>" }`. If you later delete the VM, you can reuse the allocation for another VM.
