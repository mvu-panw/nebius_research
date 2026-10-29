# Setting up a custom NAT gateway for subnets

Source: https://docs.nebius.com/vpc/routing/custom-nat-gateway

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Setting up a custom NAT gateway for subnets

By default, traffic from your Nebius AI Cloud resources to public IP addresses is routed to the internet through the [default egress gateway](https://docs.nebius.com/vpc/routing/overview.md#default-egress-gateway). You can set up a Compute virtual machine (VM) as a custom gateway for traffic from specific subnets to the internet. The gateway is called a NAT gateway because it uses [network address translation](https://en.wikipedia.org/wiki/Network_address_translation) (NAT) to change the egress traffic's source IP address. This change causes the traffic to appear as if it were sent from the public IP address of the gateway VM rather than the private IP address of the originating resource.

## Costs

Nebius AI Cloud charges you for running Compute virtual machines. For more details, see [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md).

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

## Steps

### Create a gateway virtual machine

> [!WARNING]
>
> The subnet for the gateway VM must be a separate subnet. In later steps, you create a routing table (route table) and assign it to subnets to which the new routing should apply; assigning this routing table to the gateway VM's subnet leads to routing loops.

**CLI**

1. Get the ID of the network that contains the subnets for which you want to set up routing:

   ```bash theme={null}
   nebius vpc network list
   ```

   Save the network's ID from the `.metadata.id` parameter.

2. Create a subnet for the gateway VM:

   ```bash theme={null}
   nebius vpc subnet create --name gateway-subnet --network-id <network_ID>
   ```

   Save the subnet's ID from the `.metadata.id` parameter.

3. Create a private allocation for the gateway VM:

   ```bash theme={null}
   nebius vpc allocation create \
      --name gateway-allocation \
      --ipv4-private-subnet-id <gateway_subnet_ID>
   ```

   Save the allocation's ID from the `.metadata.id` parameter.

4. Create the gateway VM. It must have a network interface that is located in the created subnet, has the allocated private IP address and a public IP address:

   ```bash theme={null}
   nebius compute instance create \
      --name gateway-vm \
      --network-interfaces "[{
        \"name\": \"eth0\",
        \"ip_address\": {
          \"allocation_id\": \"<gateway_allocation_ID>\"
        },
        \"subnet_id\": \"<gateway_subnet_ID>\",
        \"public_ip_address\": {}
      }]" \
      <other_parameters>
   ```

   > **Full example**
   >
   > ```bash theme={null}
   > VM_BOOT_DISK_ID=$(nebius compute disk create \
   >    --name gateway-boot-disk \
   >    --size-gibibytes 50 \
   >    --type network_ssd \
   >    --source-image-family-image-family ubuntu24.04-cuda13.0 \
   >    --block-size-bytes 4096 \
   >    --format jsonpath='{.metadata.id}')
   >
   > nebius compute instance create \
   >    --name gateway-vm-example \
   >    --resources-platform cpu-d3 \
   >    --resources-preset 4vcpu-16gb \
   >    --boot-disk-existing-disk-id $VM_BOOT_DISK_ID \
   >    --boot-disk-attach-mode read_write \
   >    --boot-disk-device-id boot-disk \
   >    --network-interfaces "[{
   >      \"name\": \"eth0\",
   >      \"ip_address\": {
   >        \"allocation_id\": \"<gateway_allocation_ID>\"
   >      },
   >      \"subnet_id\": \"<gateway_subnet_ID>\",
   >      \"public_ip_address\": {}
   >    }]" \
   >    --cloud-init-user-data "users:
   >      - name: $USER
   >        sudo: ALL=(ALL) NOPASSWD:ALL
   >        shell: /bin/bash
   >        ssh_authorized_keys:
   >         - $(cat ~/.ssh/id_ed25519.pub)"
   > ```

   For more details about VM parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**Go SDK**

1. Get the ID of the network that contains the subnets for which you want to set up routing. List the networks in the project, with `ParentId` set to the project ID:

   ```go theme={null}
   natNetworksService := sdk.Services().VPC().V1().
       Network()
   natNetworksResponse, err := natNetworksService.List(
       ctx,
       &vpc.ListNetworksRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return err
   }
   fmt.Println(natNetworksResponse)
   ```

   Save the network's ID from `Metadata.Id`.

2. Create a subnet for the gateway VM. Set `Metadata.ParentId` to the project ID and `Spec.NetworkId` to the network ID:

   ```go theme={null}
   gatewaySubnetService := sdk.Services().VPC().V1().
       Subnet()
   gatewaySubnetOperation, err := gatewaySubnetService.Create(
       ctx,
       &vpc.CreateSubnetRequest{
           Metadata: &common.ResourceMetadata{
               Name: "gateway-subnet",
               ParentId: "<project_ID>",
           },
           Spec: &vpc.SubnetSpec{
               NetworkId: "<network_ID>",
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = gatewaySubnetOperation.Wait(ctx); err != nil {
       return err
   }
   gatewaySubnetID := gatewaySubnetOperation.ResourceID()
   fmt.Println(gatewaySubnetOperation)
   ```

   The code saves the subnet ID to `gatewaySubnetID`.

3. Create a private allocation for the gateway VM. Set `Metadata.ParentId` to the project ID and `SubnetId` to the gateway subnet ID:

   ```go theme={null}
   gatewayIpService := sdk.Services().VPC().V1().
       Allocation()
   gatewayIpOperation, err := gatewayIpService.Create(
       ctx,
       &vpc.CreateAllocationRequest{
           Metadata: &common.ResourceMetadata{
               Name: "gateway-allocation",
               ParentId: "<project_ID>",
           },
           Spec: &vpc.AllocationSpec{
               IpSpec: &vpc.AllocationSpec_Ipv4Private{
                   Ipv4Private: &vpc.IPv4PrivateAllocationSpec{
                       Pool: &vpc.IPv4PrivateAllocationSpec_SubnetId{
                           SubnetId: "<gateway_subnet_ID>",
                       },
                   },
               },
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = gatewayIpOperation.Wait(ctx); err != nil {
       return err
   }
   allocationID := gatewayIpOperation.ResourceID()
   fmt.Println(gatewayIpOperation)
   ```

   The code saves the allocation ID to `allocationID`.

4. Create the gateway VM. It must have a network interface that is located in the created subnet, has the allocated private IP address and a public IP address:

   ```go theme={null}
   gatewayInstanceService := sdk.Services().Compute().V1().
       Instance()
   gatewayInstanceOperation, err := gatewayInstanceService.Create(
       ctx,
       &compute.CreateInstanceRequest{
           Metadata: &common.ResourceMetadata{
               Name: "gateway-vm",
               ParentId: "<project_ID>",
           },
           Spec: &compute.InstanceSpec{
               Resources: &compute.ResourcesSpec{
                   Platform: "cpu-e2",
                   Size: &compute.ResourcesSpec_Preset{
                       Preset: "2vcpu-8gb",
                   },
               },
               BootDisk: &compute.AttachedDiskSpec{
                   AttachMode: compute.AttachedDiskSpec_READ_WRITE,
                   Type: &compute.AttachedDiskSpec_ExistingDisk{
                       ExistingDisk: &compute.ExistingDisk{
                           Id: "<boot_disk_ID>",
                       },
                   },
                   DeviceId: "boot-device-id",
               },
               NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                   &compute.NetworkInterfaceSpec{
                       Name: "eth0",
                       SubnetId: "<gateway_subnet_ID>",
                       IpAddress: &compute.IPAddress{
                           AllocationId: "<gateway_allocation_ID>",
                       },
                       PublicIpAddress: &compute.PublicIPAddress{},
                   },
               },
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = gatewayInstanceOperation.Wait(ctx); err != nil {
       return err
   }
   fmt.Println(gatewayInstanceOperation)
   ```

   In the code, set the following parameters:

   * `Metadata.ParentId`: ID of the project.
   * `Id` under `Spec.BootDisk`: ID of the boot disk.
   * `SubnetId`: ID of the gateway subnet.
   * `AllocationId`: ID of the gateway allocation.

   `PublicIpAddress` gives the VM a public IP address. `Spec.Resources.Platform` and `Preset` under `Spec.Resources.Size` are example values; change them if needed.

   > **Full example**
   >
   > The full example also creates a boot disk and adds a user through cloud-init. Set `<username>` and `<SSH_public_key>` to the username and the public SSH key for connecting to the VM.
   >
   > ```go theme={null}
   > exampleDiskService := sdk.Services().Compute().V1().
   >     Disk()
   > exampleDiskOperation, err := exampleDiskService.Create(
   >     ctx,
   >     &compute.CreateDiskRequest{
   >         Metadata: &common.ResourceMetadata{
   >             Name: "gateway-boot-disk",
   >             ParentId: "<project_ID>",
   >         },
   >         Spec: &compute.DiskSpec{
   >             Size: &compute.DiskSpec_SizeGibibytes{
   >                 SizeGibibytes: 50,
   >             },
   >             BlockSizeBytes: 4096,
   >             Type: compute.DiskSpec_NETWORK_SSD,
   >             Source: &compute.DiskSpec_SourceImageFamily{
   >                 SourceImageFamily: &compute.SourceImageFamily{
   >                     ImageFamily: "ubuntu24.04-cuda13.0",
   >                 },
   >             },
   >         },
   >     },
   > )
   > if err != nil {
   >     return err
   > }
   > if _, err = exampleDiskOperation.Wait(ctx); err != nil {
   >     return err
   > }
   > exampleCloudInit := fmt.Sprintf(
   >     "users:\n"+
   >         "  - name: %s\n"+
   >         "    sudo: ALL=(ALL) NOPASSWD:ALL\n"+
   >         "    shell: /bin/bash\n"+
   >         "    ssh_authorized_keys:\n"+
   >         "      - %s\n",
   >     "<username>",
   >     "<SSH_public_key>",
   > )
   > exampleInstanceService := sdk.Services().Compute().V1().
   >     Instance()
   > exampleInstanceOperation, err := exampleInstanceService.Create(
   >     ctx,
   >     &compute.CreateInstanceRequest{
   >         Metadata: &common.ResourceMetadata{
   >             Name: "gateway-vm-example",
   >             ParentId: "<project_ID>",
   >         },
   >         Spec: &compute.InstanceSpec{
   >             Resources: &compute.ResourcesSpec{
   >                 Platform: "cpu-d3",
   >                 Size: &compute.ResourcesSpec_Preset{
   >                     Preset: "4vcpu-16gb",
   >                 },
   >             },
   >             BootDisk: &compute.AttachedDiskSpec{
   >                 AttachMode: compute.AttachedDiskSpec_READ_WRITE,
   >                 Type: &compute.AttachedDiskSpec_ExistingDisk{
   >                     ExistingDisk: &compute.ExistingDisk{
   >                         Id: exampleDiskOperation.ResourceID(),
   >                     },
   >                 },
   >                 DeviceId: "boot-disk",
   >             },
   >             NetworkInterfaces: []*compute.NetworkInterfaceSpec{
   >                 &compute.NetworkInterfaceSpec{
   >                     Name: "eth0",
   >                     SubnetId: "<gateway_subnet_ID>",
   >                     IpAddress: &compute.IPAddress{
   >                         AllocationId: "<gateway_allocation_ID>",
   >                     },
   >                     PublicIpAddress: &compute.PublicIPAddress{},
   >                 },
   >             },
   >             CloudInitUserData: exampleCloudInit,
   >         },
   >     },
   > )
   > if err != nil {
   >     return err
   > }
   > if _, err = exampleInstanceOperation.Wait(ctx); err != nil {
   >     return err
   > }
   > fmt.Println(exampleInstanceOperation)
   > ```

   For more details about VM parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**Python SDK**

1. Get the ID of the network that contains the subnets for which you want to set up routing. List the networks in the project, with `parent_id` set to the project ID:

   ```python theme={null}
   nat_networks_service = NetworkServiceClient(sdk)
   nat_networks_response = await nat_networks_service.list(
       ListNetworksRequest(
           parent_id="<project_ID>",
       ),
   )
   print(nat_networks_response)
   ```

   Save the network's ID from `metadata.id`.

2. Create a subnet for the gateway VM. Set `parent_id` to the project ID and `network_id` to the network ID:

   ```python theme={null}
   gateway_subnet_service = SubnetServiceClient(sdk)
   gateway_subnet_operation = await gateway_subnet_service.create(
       CreateSubnetRequest(
           metadata=ResourceMetadata(
               name="gateway-subnet",
               parent_id="<project_ID>",
           ),
           spec=SubnetSpec(
               network_id="<network_ID>",
           ),
       ),
   )
   await gateway_subnet_operation.wait()
   gateway_subnet_id = gateway_subnet_operation.resource_id
   print(gateway_subnet_operation)
   ```

   The code saves the subnet ID to `gateway_subnet_id`.

3. Create a private allocation for the gateway VM. Set `parent_id` to the project ID and `subnet_id` to the gateway subnet ID:

   ```python theme={null}
   gateway_ip_service = AllocationServiceClient(sdk)
   gateway_ip_operation = await gateway_ip_service.create(
       CreateAllocationRequest(
           metadata=ResourceMetadata(
               name="gateway-allocation",
               parent_id="<project_ID>",
           ),
           spec=AllocationSpec(
               ipv4_private=IPv4PrivateAllocationSpec(
                   subnet_id="<gateway_subnet_ID>",
               ),
           ),
       ),
   )
   await gateway_ip_operation.wait()
   allocation_id = gateway_ip_operation.resource_id
   print(gateway_ip_operation)
   ```

   The code saves the allocation ID to `allocation_id`.

4. Create the gateway VM. It must have a network interface that is located in the created subnet, has the allocated private IP address and a public IP address:

   ```python theme={null}
   gateway_instance_service = InstanceServiceClient(sdk)
   gateway_instance_operation = await gateway_instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(
               name="gateway-vm",
               parent_id="<project_ID>",
           ),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-e2",
                   preset="2vcpu-8gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(
                       id="<boot_disk_ID>",
                   ),
                   device_id="boot-device-id",
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id="<gateway_subnet_ID>",
                       ip_address=IPAddress(
                           allocation_id="<gateway_allocation_ID>",
                       ),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await gateway_instance_operation.wait()
   print(gateway_instance_operation)
   ```

   In the code, set the following parameters:

   * `parent_id`: ID of the project.
   * `existing_disk.id`: ID of the boot disk.
   * `subnet_id`: ID of the gateway subnet.
   * `allocation_id`: ID of the gateway allocation.

   `public_ip_address` gives the VM a public IP address. `resources.platform` and `resources.preset` are example values; change them if needed.

   > **Full example**
   >
   > The full example also creates a boot disk and adds a user through cloud-init. Set `<username>` and `<SSH_public_key>` to the username and the public SSH key for connecting to the VM.
   >
   > ```python theme={null}
   > example_disk_service = DiskServiceClient(sdk)
   > example_disk_operation = await example_disk_service.create(
   >     CreateDiskRequest(
   >         metadata=ResourceMetadata(
   >             name="gateway-boot-disk",
   >             parent_id="<project_ID>",
   >         ),
   >         spec=DiskSpec(
   >             size_gibibytes=50,
   >             block_size_bytes=4096,
   >             type=DiskSpec.DiskType.NETWORK_SSD,
   >             source_image_family=SourceImageFamily(
   >                 image_family="ubuntu24.04-cuda13.0",
   >             ),
   >         ),
   >     ),
   > )
   > await example_disk_operation.wait()
   > example_cloud_init = (
   >     "users:\n"
   >     "  - name: {}\n"
   >     "    sudo: ALL=(ALL) NOPASSWD:ALL\n"
   >     "    shell: /bin/bash\n"
   >     "    ssh_authorized_keys:\n"
   >     "      - {}\n"
   > ).format("<username>", "<SSH_public_key>")
   > example_instance_service = InstanceServiceClient(sdk)
   > example_instance_operation = await example_instance_service.create(
   >     CreateInstanceRequest(
   >         metadata=ResourceMetadata(
   >             name="gateway-vm-example",
   >             parent_id="<project_ID>",
   >         ),
   >         spec=InstanceSpec(
   >             resources=ResourcesSpec(
   >                 platform="cpu-d3",
   >                 preset="4vcpu-16gb",
   >             ),
   >             boot_disk=AttachedDiskSpec(
   >                 attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
   >                 existing_disk=ExistingDisk(
   >                     id=example_disk_operation.resource_id,
   >                 ),
   >                 device_id="boot-disk",
   >             ),
   >             network_interfaces=[
   >                 NetworkInterfaceSpec(
   >                     name="eth0",
   >                     subnet_id="<gateway_subnet_ID>",
   >                     ip_address=IPAddress(
   >                         allocation_id="<gateway_allocation_ID>",
   >                     ),
   >                     public_ip_address=PublicIPAddress(),
   >                 ),
   >             ],
   >             cloud_init_user_data=example_cloud_init,
   >         ),
   >     ),
   > )
   > await example_instance_operation.wait()
   > print(example_instance_operation)
   > ```

   For more details about VM parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**JavaScript SDK**

1. Get the ID of the network that contains the subnets for which you want to set up routing. List the networks in the project, with `parentId` set to the project ID:

   ```ts theme={null}
   const natNetworksService = new NetworkService(sdk);
   const natNetworksResponse = await natNetworksService.list(
     ListNetworksRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(natNetworksResponse);
   ```

   Save the network's ID from `metadata.id`.

2. Create a subnet for the gateway VM. Set `parentId` to the project ID and `networkId` to the network ID:

   ```ts theme={null}
   const gatewaySubnetService = new SubnetService(sdk);
   const gatewaySubnetOperation = await gatewaySubnetService.create(
     CreateSubnetRequest.create({
       metadata: {
         name: "gateway-subnet",
         parentId: "<project_ID>",
       },
       spec: {
         networkId: "<network_ID>",
       },
     }),
   ).result;
   await gatewaySubnetOperation.wait();
   const gatewaySubnetId = gatewaySubnetOperation.resourceId();
   console.log(gatewaySubnetOperation);
   ```

   The code saves the subnet ID to `gatewaySubnetId`.

3. Create a private allocation for the gateway VM. Set `parentId` to the project ID and `subnetId` to the gateway subnet ID:

   ```ts theme={null}
   const gatewayIpService = new AllocationService(sdk);
   const gatewayIpOperation = await gatewayIpService.create(
     CreateAllocationRequest.create({
       metadata: {
         name: "gateway-allocation",
         parentId: "<project_ID>",
       },
       spec: {
         ipSpec: {
           "$case": "ipv4Private",
           "ipv4Private": {
             pool: {
               "$case": "subnetId",
               "subnetId": "<gateway_subnet_ID>",
             },
           },
         },
       },
     }),
   ).result;
   await gatewayIpOperation.wait();
   const allocationId = gatewayIpOperation.resourceId();
   console.log(gatewayIpOperation);
   ```

   The code saves the allocation ID to `allocationId`.

4. Create the gateway VM. It must have a network interface that is located in the created subnet, has the allocated private IP address and a public IP address:

   ```ts theme={null}
   const gatewayInstanceService = new InstanceService(sdk);
   const gatewayInstanceOperation = await gatewayInstanceService.create(
     CreateInstanceRequest.create({
       metadata: {
         name: "gateway-vm",
         parentId: "<project_ID>",
       },
       spec: {
         resources: {
           platform: "cpu-e2",
           size: {
             "$case": "preset",
             "preset": "2vcpu-8gb",
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
           deviceId: "boot-device-id",
         },
         networkInterfaces: [
           {
             name: "eth0",
             subnetId: "<gateway_subnet_ID>",
             ipAddress: {
               allocationId: "<gateway_allocation_ID>",
             },
             publicIpAddress: {},
           },
         ],
       },
     }),
   ).result;
   await gatewayInstanceOperation.wait();
   console.log(gatewayInstanceOperation);
   ```

   In the code, set the following parameters:

   * `parentId`: ID of the project.
   * `existingDisk.id`: ID of the boot disk.
   * `subnetId`: ID of the gateway subnet.
   * `allocationId`: ID of the gateway allocation.

   `publicIpAddress` gives the VM a public IP address. `resources.platform` and `preset` under `resources.size` are example values; change them if needed.

   > **Full example**
   >
   > The full example also creates a boot disk and adds a user through cloud-init. Set `<username>` and `<SSH_public_key>` to the username and the public SSH key for connecting to the VM.
   >
   > ```ts theme={null}
   > const exampleDiskService = new DiskService(sdk);
   > const exampleDiskOperation = await exampleDiskService.create(
   >   CreateDiskRequest.create({
   >     metadata: {
   >       name: "gateway-boot-disk",
   >       parentId: "<project_ID>",
   >     },
   >     spec: {
   >       size: {
   >         "$case": "sizeGibibytes",
   >         "sizeGibibytes": 50,
   >       },
   >       blockSizeBytes: 4096,
   >       type: DiskSpec_DiskType.NETWORK_SSD,
   >       source: {
   >         "$case": "sourceImageFamily",
   >         "sourceImageFamily": {
   >           imageFamily: "ubuntu24.04-cuda13.0",
   >         },
   >       },
   >     },
   >   }),
   > ).result;
   > await exampleDiskOperation.wait();
   > const exampleCloudInit = [
   >   "users:",
   >   "  - name: " + "<username>",
   >   "    sudo: ALL=(ALL) NOPASSWD:ALL",
   >   "    shell: /bin/bash",
   >   "    ssh_authorized_keys:",
   >   "      - " + "<SSH_public_key>",
   > ].join("\n");
   > const exampleInstanceService = new InstanceService(sdk);
   > const exampleInstanceOperation = await exampleInstanceService.create(
   >   CreateInstanceRequest.create({
   >     metadata: {
   >       name: "gateway-vm-example",
   >       parentId: "<project_ID>",
   >     },
   >     spec: {
   >       resources: {
   >         platform: "cpu-d3",
   >         size: {
   >           "$case": "preset",
   >           "preset": "4vcpu-16gb",
   >         },
   >       },
   >       bootDisk: {
   >         attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
   >         type: {
   >           "$case": "existingDisk",
   >           "existingDisk": {
   >             id: exampleDiskOperation.resourceId(),
   >           },
   >         },
   >         deviceId: "boot-disk",
   >       },
   >       networkInterfaces: [
   >         {
   >           name: "eth0",
   >           subnetId: "<gateway_subnet_ID>",
   >           ipAddress: {
   >             allocationId: "<gateway_allocation_ID>",
   >           },
   >           publicIpAddress: {},
   >         },
   >       ],
   >       cloudInitUserData: exampleCloudInit,
   >     },
   >   }),
   > ).result;
   > await exampleInstanceOperation.wait();
   > console.log(exampleInstanceOperation);
   > ```

   For more details about VM parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

### Set up the gateway VM

1. Connect to the gateway VM by using SSH:

   ```bash theme={null}
   ssh <username>@<public_IP_address>
   ```

   For more details, see [How to connect to virtual machines in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/connect.md).

2. Enable IPv4 routing and make this change persistent:

   ```bash theme={null}
   sudo sysctl -w net.ipv4.ip_forward=1
   sudo sed -i -E 's/^(#\s?)?net.ipv4.ip_forward.*/net.ipv4.ip_forward=1/' /etc/sysctl.conf
   ```

3. Enable egress NAT and make this change persistent:

   ```bash theme={null}
   sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   sudo apt-get install iptables-persistent
   ```

   The latter command asks you whether to save your current `iptables` IPv4 and IPv6 rules to files. Answer "yes" to both.

4. Disconnect from the gateway VM:

   ```bash theme={null}
   exit
   ```

### Set up routing

**CLI**

1. Create a routing table in the network:

   ```bash theme={null}
   nebius vpc route-table create \
      --name gateway-table \
      --network-id <network_ID>
   ```

   Save the routing table's ID from the `.metadata.id` parameter.

2. Create a route in the routing table to send egress traffic to the gateway private allocation:

   ```bash theme={null}
   nebius vpc route create \
      --name route-to-allocation \
      --parent-id <routing_table_ID> \
      --destination-cidr 0.0.0.0/0 \
      --next-hop-allocation-id <gateway_allocation_ID>
   ```

3. Assign the routing table to the subnets that should use the NAT gateway:

   ```bash theme={null}
   nebius vpc subnet update <subnet_ID> \
      --route-table-id <routing_table_ID>
   ```

   Repeat for each subnet as needed. Do not assign the routing table to the subnet of the gateway VM (`gateway-subnet`).

**Go SDK**

1. Create a routing table in the network. Set `Metadata.ParentId` to the project ID and `Spec.NetworkId` to the network ID:

   ```go theme={null}
   gatewayTableService := sdk.Services().VPC().V1().
       RouteTable()
   gatewayTableOperation, err := gatewayTableService.Create(
       ctx,
       &vpc.CreateRouteTableRequest{
           Metadata: &common.ResourceMetadata{
               Name: "gateway-table",
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
   if _, err = gatewayTableOperation.Wait(ctx); err != nil {
       return err
   }
   routingTableID := gatewayTableOperation.ResourceID()
   fmt.Println(gatewayTableOperation)
   ```

   The code saves the routing table ID to `routingTableID`.

2. Create a route in the routing table to send egress traffic to the gateway private allocation. Set `Metadata.ParentId` to the routing table ID and `Id` under `Spec.NextHop.Allocation` to the gateway allocation ID:

   ```go theme={null}
   gatewayRouteService := sdk.Services().VPC().V1().
       Route()
   gatewayRouteOperation, err := gatewayRouteService.Create(
       ctx,
       &vpc.CreateRouteRequest{
           Metadata: &common.ResourceMetadata{
               Name: "route-to-allocation",
               ParentId: "<routing_table_ID>",
           },
           Spec: &vpc.RouteSpec{
               Destination: &vpc.DestinationMatch{
                   Cidr: "0.0.0.0/0",
               },
               NextHop: &vpc.NextHop{
                   NextHop: &vpc.NextHop_Allocation{
                       Allocation: &vpc.AllocationNextHop{
                           Id: "<gateway_allocation_ID>",
                       },
                   },
               },
           },
       },
   )
   if err != nil {
       return err
   }
   if _, err = gatewayRouteOperation.Wait(ctx); err != nil {
       return err
   }
   fmt.Println(gatewayRouteOperation)
   ```

3. Assign the routing table to the subnets that should use the NAT gateway. Set `Id` to the subnet ID and `Spec.RouteTableId` to the routing table ID:

   ```go theme={null}
   clientSubnetService := sdk.Services().VPC().V1().
       Subnet()
   clientSubnet, err := clientSubnetService.Get(
       ctx,
       &vpc.GetSubnetRequest{
           Id: "<subnet_ID>",
       },
   )
   if err != nil {
       return err
   }
   clientSubnet.Spec.RouteTableId = "<routing_table_ID>"
   clientSubnetOperation, err := clientSubnetService.Update(
       ctx,
       &vpc.UpdateSubnetRequest{
           Metadata: clientSubnet.Metadata,
           Spec: clientSubnet.Spec,
       },
   )
   if err != nil {
       return err
   }
   if _, err = clientSubnetOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Repeat for each subnet as needed. Do not assign the routing table to the subnet of the gateway VM (`gateway-subnet`).

**Python SDK**

1. Create a routing table in the network. Set `parent_id` to the project ID and `network_id` to the network ID:

   ```python theme={null}
   gateway_table_service = RouteTableServiceClient(sdk)
   gateway_table_operation = await gateway_table_service.create(
       CreateRouteTableRequest(
           metadata=ResourceMetadata(
               name="gateway-table",
               parent_id="<project_ID>",
           ),
           spec=RouteTableSpec(
               network_id="<network_ID>",
           ),
       ),
   )
   await gateway_table_operation.wait()
   routing_table_id = gateway_table_operation.resource_id
   print(gateway_table_operation)
   ```

   The code saves the routing table ID to `routing_table_id`.

2. Create a route in the routing table to send egress traffic to the gateway private allocation. Set `parent_id` to the routing table ID and `next_hop.allocation.id` to the gateway allocation ID:

   ```python theme={null}
   gateway_route_service = RouteServiceClient(sdk)
   gateway_route_operation = await gateway_route_service.create(
       CreateRouteRequest(
           metadata=ResourceMetadata(
               name="route-to-allocation",
               parent_id="<routing_table_ID>",
           ),
           spec=RouteSpec(
               destination=DestinationMatch(
                   cidr="0.0.0.0/0",
               ),
               next_hop=NextHop(
                   allocation=AllocationNextHop(
                       id="<gateway_allocation_ID>",
                   ),
               ),
           ),
       ),
   )
   await gateway_route_operation.wait()
   print(gateway_route_operation)
   ```

3. Assign the routing table to the subnets that should use the NAT gateway. Set `id` to the subnet ID and `spec.route_table_id` to the routing table ID:

   ```python theme={null}
   client_subnet_service = SubnetServiceClient(sdk)
   client_subnet = await client_subnet_service.get(
       GetSubnetRequest(
           id="<subnet_ID>",
       ),
   )
   client_subnet.spec.route_table_id = "<routing_table_ID>"
   client_subnet_operation = await client_subnet_service.update(
       UpdateSubnetRequest(
           metadata=client_subnet.metadata,
           spec=client_subnet.spec,
       ),
   )
   await client_subnet_operation.wait()
   ```

   Repeat for each subnet as needed. Do not assign the routing table to the subnet of the gateway VM (`gateway-subnet`).

**JavaScript SDK**

1. Create a routing table in the network. Set `parentId` to the project ID and `networkId` to the network ID:

   ```ts theme={null}
   const gatewayTableService = new RouteTableService(sdk);
   const gatewayTableOperation = await gatewayTableService.create(
     CreateRouteTableRequest.create({
       metadata: {
         name: "gateway-table",
         parentId: "<project_ID>",
       },
       spec: {
         networkId: "<network_ID>",
       },
     }),
   ).result;
   await gatewayTableOperation.wait();
   const routingTableId = gatewayTableOperation.resourceId();
   console.log(gatewayTableOperation);
   ```

   The code saves the routing table ID to `routingTableId`.

2. Create a route in the routing table to send egress traffic to the gateway private allocation. Set `parentId` to the routing table ID and `id` under `nextHop.allocation` to the gateway allocation ID:

   ```ts theme={null}
   const gatewayRouteService = new RouteService(sdk);
   const gatewayRouteOperation = await gatewayRouteService.create(
     CreateRouteRequest.create({
       metadata: {
         name: "route-to-allocation",
         parentId: "<routing_table_ID>",
       },
       spec: {
         destination: {
           cidr: "0.0.0.0/0",
         },
         nextHop: {
           nextHop: {
             "$case": "allocation",
             "allocation": {
               id: "<gateway_allocation_ID>",
             },
           },
         },
       },
     }),
   ).result;
   await gatewayRouteOperation.wait();
   console.log(gatewayRouteOperation);
   ```

3. Assign the routing table to the subnets that should use the NAT gateway. Set `id` to the subnet ID and `spec.routeTableId` to the routing table ID:

   ```ts theme={null}
   const clientSubnetService = new SubnetService(sdk);
   const clientSubnet = await clientSubnetService.get(
     GetSubnetRequest.create({
       id: "<subnet_ID>",
     }),
   ).result;
   clientSubnet.spec.routeTableId = "<routing_table_ID>";
   const clientSubnetOperation = await clientSubnetService.update(
     UpdateSubnetRequest.create({
       metadata: clientSubnet.metadata,
       spec: clientSubnet.spec,
     }),
   ).result;
   await clientSubnetOperation.wait();
   ```

   Repeat for each subnet as needed. Do not assign the routing table to the subnet of the gateway VM (`gateway-subnet`).

### Test routing

To test that the routing table works, send traffic from a VM in a subnet to which you assigned the routing table (a test VM) and check its source IP address:

1. Connect to the test VM by using the gateway VM as the jump host:

   ```bash theme={null}
   ssh -J <username>@<gateway_public_IP_address> <username>@<VM_private_IP_address>
   ```

2. Verify that egress traffic from the test VM to the internet is routed through the gateway VM, by using a public service that looks up the traffic's source IP address:

   ```bash theme={null}
   curl ifconfig.me
   ```

   The command should return the public IP address of the gateway VM. If it returns the private address of the test VM instead:

   * Check that you assigned the routing table to the subnet: run `nebius vpc route-table get <routing_table_ID>` and then find the subnet in the `.status.assignment.subnets` parameter.
   * Check that the test VM belongs to this subnet: run `nebius compute instance get <VM_ID>` and then find the subnet in the `.spec.network_interfaces[0].subnet_id` parameter.
   * Check that you specified the gateway VM's private allocation as the next hop in the route: run `nebius vpc route list --parent-id <routing_table_ID>` and then find the allocation in the `.spec.next_hop.allocation.id` parameter.

## How to delete the created resources

The created Compute virtual machines are chargeable. If you don't need them, [delete these VMs](https://docs.nebius.com/compute/virtual-machines/delete.md), so Nebius AI Cloud doesn't charge for them.

You can also delete the [routing tables](https://docs.nebius.com/vpc/routing/manage.md#deleting-routing-tables) and [allocations](https://docs.nebius.com/cli/reference/vpc/allocation/delete.md) if you no longer need them.
