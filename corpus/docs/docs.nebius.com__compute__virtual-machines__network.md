# Private and public IP addresses of Compute virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/network

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Private and public IP addresses of Compute virtual machines

Virtual machines (VMs) in Compute can be reached at their private and public IP addresses. Assign them to manage access to the VM in a network.

In addition, you can also configure [security groups](https://docs.nebius.com/vpc/security-groups/overview.md) to enable a firewall for your VMs and control ingress and egress traffic. For more information, see [Managing security groups and security rules](https://docs.nebius.com/vpc/security-groups/manage.md).

## Private IP addresses

Each VM is created with a network interface that has a private IPv4 address. VMs can communicate with each other without internet access by using their private addresses.

Private address ranges are randomly allocated from subnets within the `10.0.0.0/8` and `192.168.0.0/16` IPv4 CIDR blocks. To reach a VM by a stable name rather than by an allocated address, use its fully qualified domain name ([FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md)), which Nebius AI Cloud registers in the [DNS zone](https://docs.nebius.com/vpc/dns/overview.md) of the VM's network.

> [!NOTE]
>
> Don't assign a private IPv4 address within the `172.17.0.0/16` CIDR block to a VM. The VMs running Docker cannot reach this address because the default boot disk images come with Docker preinstalled. As a result, this affects most VMs in the network. For more information, see [Virtual machine is unreachable due to a Docker subnet conflict](https://docs.nebius.com/compute/virtual-machines/docker-subnet-conflict.md).

## Prerequisites

If you use the web console, you don't need to complete any prerequisites.

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

### How to get a VM's private IP address

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, open the page of the required VM.
3. Copy the **Private IPv4** value from the **Network** block.

**CLI**

```bash theme={null}
export PRIVATE_IP_ADDRESS=$(nebius compute instance get-by-name \
  --name <VM_name> \
  --format json \
  | jq -r '.status.network_interfaces[0].ip_address.address | split("/")[0]')
echo $PRIVATE_IP_ADDRESS
```

**Go SDK**

```go theme={null}
privateIPInstance, err := sdk.Services().Compute().V1().
    Instance().GetByName(
        ctx,
        &common.GetByNameRequest{
            Name: "<VM_name>",
        },
    )
if err != nil {
    return err
}
privateAddress := privateIPInstance.GetStatus().
    GetNetworkInterfaces()[0].GetIpAddress().GetAddress()
privateIPAddress := strings.Split(privateAddress, "/")[0]
fmt.Println(privateIPAddress)
```

**Python SDK**

```python theme={null}
instance_service = InstanceServiceClient(sdk)
private_ip_instance = await instance_service.get_by_name(
    GetByNameRequest(name="<VM_name>"),
)
private_address = (
    private_ip_instance.status.network_interfaces[0]
    .ip_address.address
)
private_ip_address = private_address.split("/")[0]
print(private_ip_address)
```

**JavaScript SDK**

```ts theme={null}
const privateIpService = new InstanceService(sdk);
const privateIpInstance = await privateIpService.getByName(
  GetByNameRequest.create({
    name: "<VM_name>",
  }),
);
const privateAddress = privateIpInstance.status
  ?.networkInterfaces[0]?.ipAddress?.address;
const privateIpAddress = privateAddress?.split("/")[0];
console.log(privateIpAddress);
```

### How to assign a secondary private IP address to a VM

You can use secondary private IP addresses as a backup option in case of incidents. For example, a backup node can take a secondary address of the main node when the main one fails. As a result, routing to this address can be preserved.

**Web console**

To assign a secondary private address to a VM:

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, open the page of the required VM.
3. Click **Attach resource** → **Secondary private IP**.
4. In the window that opens, select whether you want to reuse an existing IP address as a secondary one or create a new address.
5. For an existing IP address, select an allocation and then click **Assign address**.
6. For a new address, specify the allocation name and address. After that, click **Create and assign address**.

**CLI**

To assign a secondary private address to a VM, first create a private allocation with the required address. After that, add this allocation to the VM specification.

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the allocation.

2. Check what private CIDR blocks this subnet includes:

   ```bash theme={null}
   nebius vpc subnet get --id <subnet_ID>
   ```

   The available CIDR blocks are specified in the `status.ipv4_private_cidrs` parameter in the output.

3. Create an allocation that reserves a private address. Use the address that belongs to one of the received private CIDR blocks.

   ```bash theme={null}
   nebius vpc allocation create \
     --name private_allocation \
     --ipv4-private-subnet-id <subnet_ID> \
     --ipv4-private-cidr <IP_address>
   ```

   Copy the allocation ID from the output.

4. Assign the allocation to the required VM:

   ```bash theme={null}
   nebius compute instance update \
     --id <VM_ID> \
     --network-interfaces "[{\"aliases\": [{\"allocation_id\": \"<allocation_ID>\"}] }]"
   ```

For more information, see [Allocating custom private addresses to resources](https://docs.nebius.com/vpc/addressing/custom-private-addresses.md).

**Go SDK**

To assign a secondary private address to a VM, first create a private allocation with the required address. After that, add this allocation to the VM specification.

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the allocation.

2. Check what private CIDR blocks this subnet includes:

   ```go theme={null}
   subnet, err := sdk.Services().VPC().V1().
       Subnet().Get(
           ctx,
           &vpc.GetSubnetRequest{
               Id: "<subnet_ID>",
           },
       )
   if err != nil {
       return err
   }
   fmt.Println(subnet)
   ```

   The response includes the available CIDR blocks.

3. Create an allocation that reserves a private address. Use the address that belongs to one of the received private CIDR blocks.

   ```go theme={null}
   privAllocOperation, err := sdk.Services().VPC().V1().
       Allocation().Create(
           ctx,
           &vpc.CreateAllocationRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "private_allocation",
               },
               Spec: &vpc.AllocationSpec{
                   IpSpec: &vpc.AllocationSpec_Ipv4Private{
                       Ipv4Private: &vpc.IPv4PrivateAllocationSpec{
                           Cidr: "<IP_address>",
                           Pool: &vpc.IPv4PrivateAllocationSpec_SubnetId{
                               SubnetId: "<subnet_ID>",
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = privAllocOperation.Wait(ctx); err != nil {
       return err
   }
   allocationID1 := privAllocOperation.ResourceID()
   ```

   Copy the allocation ID from the response.

4. Assign the allocation to the required VM:

   ```go theme={null}
   instanceForAlias, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if instanceForAlias.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   networkInterfaces := instanceForAlias.Spec.NetworkInterfaces
   networkInterfaces[0].Aliases = []*compute.IPAlias{
       {
           AllocationId: "<allocation_ID>",
       },
   }
   aliasOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: instanceForAlias.Metadata,
               Spec:     instanceForAlias.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = aliasOperation.Wait(ctx); err != nil {
       return err
   }
   ```

For more information, see [Allocating custom private addresses to resources](https://docs.nebius.com/vpc/addressing/custom-private-addresses.md).

**Python SDK**

To assign a secondary private address to a VM, first create a private allocation with the required address. After that, add this allocation to the VM specification.

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the allocation.

2. Check what private CIDR blocks this subnet includes:

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnet = await subnet_service.get(
       GetSubnetRequest(id="<subnet_ID>"),
   )
   print(subnet)
   ```

   The response includes the available CIDR blocks.

3. Create an allocation that reserves a private address. Use the address that belongs to one of the received private CIDR blocks.

   ```python theme={null}
   allocation_service = AllocationServiceClient(sdk)
   private_allocation_operation = await allocation_service.create(
       CreateAllocationRequest(
           metadata=ResourceMetadata(name="private_allocation"),
           spec=AllocationSpec(
               ipv4_private=IPv4PrivateAllocationSpec(
                   cidr="<IP_address>",
                   subnet_id="<subnet_ID>",
               ),
           ),
       ),
   )
   await private_allocation_operation.wait()
   allocation_id_1 = private_allocation_operation.resource_id
   ```

   Copy the allocation ID from the response.

4. Assign the allocation to the required VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if instance.spec is None:
       raise ValueError("instance spec is missing")
   instance.spec.network_interfaces[0].aliases = [
       IPAlias(allocation_id="<allocation_ID>"),
   ]
   alias_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=instance.metadata,
           spec=instance.spec,
       ),
   )
   await alias_operation.wait()
   ```

For more information, see [Allocating custom private addresses to resources](https://docs.nebius.com/vpc/addressing/custom-private-addresses.md).

**JavaScript SDK**

To assign a secondary private address to a VM, first create a private allocation with the required address. After that, add this allocation to the VM specification.

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the allocation.

2. Check what private CIDR blocks this subnet includes:

   ```ts theme={null}
   const getSubnetService = new SubnetService(sdk);
   const subnet = await getSubnetService.get(
     GetSubnetRequest.create({
       id: "<subnet_ID>",
     }),
   );
   console.log(subnet);
   ```

   The response includes the available CIDR blocks.

3. Create an allocation that reserves a private address. Use the address that belongs to one of the received private CIDR blocks.

   ```ts theme={null}
   const privateAllocationService = new AllocationService(sdk);
   const privateAllocationOperation =
     await privateAllocationService.create(
       CreateAllocationRequest.create({
         metadata: ResourceMetadata.create({
           name: "private_allocation",
         }),
         spec: AllocationSpec.create({
           ipSpec: {
             $case: "ipv4Private",
             ipv4Private: IPv4PrivateAllocationSpec.create({
               cidr: "<IP_address>",
               pool: {
                 $case: "subnetId",
                 subnetId: "<subnet_ID>",
               },
             }),
           },
         }),
       }),
     ).result;
   await privateAllocationOperation.wait();
   const allocationId1 = privateAllocationOperation.resourceId();
   ```

   Copy the allocation ID from the response.

4. Assign the allocation to the required VM:

   ```ts theme={null}
   const aliasInstanceService = new InstanceService(sdk);
   const instanceForAlias = await aliasInstanceService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   if (!instanceForAlias.spec) {
     throw new Error("instance spec is missing");
   }
   instanceForAlias.spec.networkInterfaces[0].aliases = [
     IPAlias.create({
       allocationId: "<allocation_ID>",
     }),
   ];
   const aliasOperation = await aliasInstanceService.update(
     UpdateInstanceRequest.create({
       metadata: instanceForAlias.metadata,
       spec: instanceForAlias.spec,
     }),
   ).result;
   await aliasOperation.wait();
   ```

For more information, see [Allocating custom private addresses to resources](https://docs.nebius.com/vpc/addressing/custom-private-addresses.md).

## Public IP addresses

When creating a VM, you can enable public IPv4 addressing for it. A VM's public address is mapped to its private address by using one-to-one NAT.

All IP addresses assigned to a VM are [allocations](https://docs.nebius.com/vpc/overview.md#allocation). When you create a VM and automatically assign a static or dynamic public address, Compute creates an allocation for it and assigns this address to this VM. After that, Compute manages the lifecycle of this allocation. In particular, Compute deletes the allocation when the VM is deleted.

Public IP addresses are allocated from the public IPv4 ranges available for a given project. The available range depends on the [region](https://docs.nebius.com/overview/regions.md) where you create a VM. For instructions on how to get these ranges, see [Getting public IPv4 ranges for projects](https://docs.nebius.com/vpc/addressing/public-address-ranges.md).

If you assign an already existing allocation when you create a VM, Virtual Networks manages the lifecycle of this allocation. In this case, the allocation is preserved even if you delete the VM.

If you need to secure your VM and make it isolated, you can create a VM without a public IP address. If you need to connect to this VM from the internet, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md). It has an IP address in the internet and an IP address in the VM's network. As a result, you can access the VM via the jump server from the internet. This approach enhances security and still provides access to the VM.

### How to enable a public IP address for a VM

To enable a public address, either [create a VM](#how-to-create-a-vm-with-a-public-ip-address) with it or [assign a public address to an existing VM](#how-to-enable-a-public-ip-address-for-an-existing-vm).

A VM must be in the same [region](https://docs.nebius.com/overview/regions.md) as the VM's subnet. An allocation assigned to a VM must belong to the VM's subnet. For more information, see [Virtual Networks documentation](https://docs.nebius.com/vpc/overview.md).

#### How to create a VM with a public IP address

**Web console**

On the **Network** step of the [VM creation wizard](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), in the **Public IP address** field, select one of the following options:

* **Auto assign dynamic IP** (default): A dynamic public IP address is randomly allocated from the [public IPv4 ranges available for the project](https://docs.nebius.com/vpc/addressing/public-address-ranges.md).

  Dynamic public IP addresses are not persistent. If a VM with a dynamic address has the `Stopped` status for more than one hour, the address automatically returns to the IPv4 public range of Nebius AI Cloud. After that, Compute may allocate this address to a different VM.

  If you want to preserve the address, assign a static address or an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) to the VM.

* **Auto assign static IP**: A static public IP address is randomly allocated from the public IPv4 ranges available for the project.

  If you stop a VM that has a static IP address, the address will not return to the range. However, if you delete this VM, the address will return.

* **Select from already allocated**: A preliminarily created allocation is assigned to a VM.

  If you use an allocation, its address will not return to the IPv4 range even if you delete the VM.

If you want to create a VM with a private address only, select the **No public IP** option.

**CLI**

You can [create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) with a public IP address. This can be either a dynamic address, a static address or an [allocation](https://docs.nebius.com/vpc/overview.md#allocation):

* A dynamic public IP address is randomly allocated from the [IPv4 public range](#get-public-ip-range) of Nebius AI Cloud and is not persistent. If a VM with a dynamic address has the `Stopped` status for more than one hour, the address is automatically returned to the IPv4 public range. After that, Compute may allocate this address to a different VM.
* A static public IP address is also randomly allocated from the IPv4 public range of Nebius AI Cloud. If you stop a VM that has a static IP address, the address will not return to the range. However, if you delete this VM, the address will return.
* An allocation allows you to use a reserved static public address for the VM. This address will not return to the IPv4 range even if you delete the VM.

To create a VM with a **dynamic public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Run the following command and specify the subnet ID in it:

   ```bash theme={null}
   nebius compute instance create \
     ... \
     --network-interfaces "[{\"name\": \"eth0\", \"ip_address\": {}, \"public_ip_address\": {}, \"subnet_id\": \"<subnet_ID>\"}]"
   ```

To create a VM with a **static public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Run the following command and specify the subnet ID in it:

   ```bash theme={null}
   nebius compute instance create \
     ... \
     --network-interfaces "[{\"name\": \"eth0\", \"ip_address\": {}, \"public_ip_address\": {\"static\": true}, \"subnet_id\": \"<subnet_ID>\"}]"
   ```

To create a VM with an **already allocated public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```bash theme={null}
   nebius vpc allocation create \
     --ipv4-public-subnet-id <subnet_ID> \
     --name <allocation_name>
   ```

3. Create the VM. Specify the subnet ID and the allocation ID in the command:

   ```bash theme={null}
   nebius compute instance create \
     ... \
     --network-interfaces "[{\"name\": \"eth0\", \"ip_address\": {}, \"public_ip_address\": {\"allocation_id\": \"<allocation_ID>\"}, \"subnet_id\": \"<subnet_ID>\"}]"
   ```

If you want to create a VM with a private address only, omit the `public_ip_address` parameter in the `nebius compute instance create` command.

**Go SDK**

You can [create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) with a public IP address. This can be either a dynamic address, a static address or an [allocation](https://docs.nebius.com/vpc/overview.md#allocation).

To create a VM with a **dynamic public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Use the following code:

   ```go theme={null}
   publicVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<VM_name>",
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
                               Id: publicBootDiskID,
                           },
                       },
                   },
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       {
                           Name:           "eth0",
                           SubnetId:       subnetID,
                           IpAddress:      &compute.IPAddress{},
                           PublicIpAddress: &compute.PublicIPAddress{},
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = publicVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

To create a VM with a **static public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Use the following code:

   ```go theme={null}
   staticVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<static_VM_name>",
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
                               Id: staticBootDiskID,
                           },
                       },
                   },
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       {
                           Name:      "eth0",
                           SubnetId:  subnetID,
                           IpAddress: &compute.IPAddress{},
                           PublicIpAddress: &compute.PublicIPAddress{
                               Static: true,
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = staticVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

To create a VM with an **already allocated public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```go theme={null}
   publicAllocationOperation, err := sdk.Services().VPC().V1().
       Allocation().Create(
           ctx,
           &vpc.CreateAllocationRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<allocation_name>",
               },
               Spec: &vpc.AllocationSpec{
                   IpSpec: &vpc.AllocationSpec_Ipv4Public{
                       Ipv4Public: &vpc.IPv4PublicAllocationSpec{
                           Pool: &vpc.IPv4PublicAllocationSpec_SubnetId{
                               SubnetId: "<subnet_ID>",
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = publicAllocationOperation.Wait(ctx); err != nil {
       return err
   }
   allocationID := publicAllocationOperation.ResourceID()
   ```

3. Create the VM:

   ```go theme={null}
   allocationIP := &compute.PublicIPAddress_AllocationId{
       AllocationId: "<allocation_ID>",
   }
   allocationVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<allocation_VM_name>",
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
                               Id: allocationBootDiskID,
                           },
                       },
                   },
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       {
                           Name:      "eth0",
                           SubnetId:  subnetID,
                           IpAddress: &compute.IPAddress{},
                           PublicIpAddress: &compute.PublicIPAddress{
                               Allocation: allocationIP,
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = allocationVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

Create a VM with a private address only:

```go theme={null}
privateOnlyOperation, err := sdk.Services().Compute().V1().
    Instance().Create(
        ctx,
        &compute.CreateInstanceRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<private_VM_name>",
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
                            Id: privateBootDiskID,
                        },
                    },
                },
                NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                    {
                        Name:      "eth0",
                        SubnetId:  subnetID,
                        IpAddress: &compute.IPAddress{},
                    },
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = privateOnlyOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

You can [create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) with a public IP address. This can be either a dynamic address, a static address or an [allocation](https://docs.nebius.com/vpc/overview.md#allocation).

To create a VM with a **dynamic public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Use the following code:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   public_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<VM_name>"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-e2",
                   preset="2vcpu-8gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(id=public_boot_disk_id),
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await public_vm_operation.wait()
   ```

To create a VM with a **static public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Use the following code:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   static_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<static_VM_name>"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-e2",
                   preset="2vcpu-8gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(id=static_boot_disk_id),
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(static=True),
                   ),
               ],
           ),
       ),
   )
   await static_vm_operation.wait()
   ```

To create a VM with an **already allocated public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```python theme={null}
   allocation_service = AllocationServiceClient(sdk)
   public_allocation_operation = await allocation_service.create(
       CreateAllocationRequest(
           metadata=ResourceMetadata(name="<allocation_name>"),
           spec=AllocationSpec(
               ipv4_public=IPv4PublicAllocationSpec(
                   subnet_id="<subnet_ID>",
               ),
           ),
       ),
   )
   await public_allocation_operation.wait()
   allocation_id = public_allocation_operation.resource_id
   ```

3. Create the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   allocation_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<allocation_VM_name>"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-e2",
                   preset="2vcpu-8gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(
                       id=allocation_boot_disk_id,
                   ),
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(
                           allocation_id="<allocation_ID>",
                       ),
                   ),
               ],
           ),
       ),
   )
   await allocation_vm_operation.wait()
   ```

Create a VM with a private address only:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
private_only_operation = await instance_service.create(
    CreateInstanceRequest(
        metadata=ResourceMetadata(name="<private_VM_name>"),
        spec=InstanceSpec(
            resources=ResourcesSpec(
                platform="cpu-e2",
                preset="2vcpu-8gb",
            ),
            boot_disk=AttachedDiskSpec(
                attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                existing_disk=ExistingDisk(id=private_boot_disk_id),
            ),
            network_interfaces=[
                NetworkInterfaceSpec(
                    name="eth0",
                    subnet_id=subnet_id,
                    ip_address=IPAddress(),
                ),
            ],
        ),
    ),
)
await private_only_operation.wait()
```

**JavaScript SDK**

You can [create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) with a public IP address. This can be either a dynamic address, a static address or an [allocation](https://docs.nebius.com/vpc/overview.md#allocation).

To create a VM with a **dynamic public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Use the following code:

   ```ts theme={null}
   const publicVmService = new InstanceService(sdk);
   const publicVmOperation = await publicVmService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "<VM_name>",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "cpu-e2",
           size: {
             $case: "preset",
             preset: "2vcpu-8gb",
           },
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: publicBootDiskId,
             }),
           },
         }),
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
       }),
     }),
   ).result;
   await publicVmOperation.wait();
   ```

To create a VM with a **static public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.
2. Use the following code:

   ```ts theme={null}
   const staticVmService = new InstanceService(sdk);
   const staticVmOperation = await staticVmService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "<static_VM_name>",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "cpu-e2",
           size: {
             $case: "preset",
             preset: "2vcpu-8gb",
           },
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: staticBootDiskId,
             }),
           },
         }),
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({
               static: true,
             }),
           }),
         ],
       }),
     }),
   ).result;
   await staticVmOperation.wait();
   ```

To create a VM with an **already allocated public IP address**:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```ts theme={null}
   const publicAllocationService = new AllocationService(sdk);
   const publicAllocationOperation =
     await publicAllocationService.create(
       CreateAllocationRequest.create({
         metadata: ResourceMetadata.create({
           name: "<allocation_name>",
         }),
         spec: AllocationSpec.create({
           ipSpec: {
             $case: "ipv4Public",
             ipv4Public: IPv4PublicAllocationSpec.create({
               pool: {
                 $case: "subnetId",
                 subnetId: "<subnet_ID>",
               },
             }),
           },
         }),
       }),
     ).result;
   await publicAllocationOperation.wait();
   const allocationId = publicAllocationOperation.resourceId();
   ```

3. Create the VM:

   ```ts theme={null}
   const allocationVmService = new InstanceService(sdk);
   const allocationVmOperation = await allocationVmService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "<allocation_VM_name>",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "cpu-e2",
           size: {
             $case: "preset",
             preset: "2vcpu-8gb",
           },
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: allocationBootDiskId,
             }),
           },
         }),
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({
               allocation: {
                 $case: "allocationId",
                 allocationId: "<allocation_ID>",
               },
             }),
           }),
         ],
       }),
     }),
   ).result;
   await allocationVmOperation.wait();
   ```

Create a VM with a private address only:

```ts theme={null}
const privateOnlyService = new InstanceService(sdk);
const privateOnlyOperation = await privateOnlyService.create(
  CreateInstanceRequest.create({
    metadata: ResourceMetadata.create({
      name: "<private_VM_name>",
    }),
    spec: InstanceSpec.create({
      resources: ResourcesSpec.create({
        platform: "cpu-e2",
        size: {
          $case: "preset",
          preset: "2vcpu-8gb",
        },
      }),
      bootDisk: AttachedDiskSpec.create({
        attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
        type: {
          $case: "existingDisk",
          existingDisk: ExistingDisk.create({
            id: privateBootDiskId,
          }),
        },
      }),
      networkInterfaces: [
        NetworkInterfaceSpec.create({
          name: "eth0",
          subnetId,
          ipAddress: IPAddress.create({}),
        }),
      ],
    }),
  }),
).result;
await privateOnlyOperation.wait();
```

> [!NOTE]
>
> If an allocation with a public address has not been assigned to any resource for 30 days, Nebius AI Cloud can delete this allocation and release its address. If you want to preserve the address, assign its allocation to a Nebius AI Cloud resource.

#### How to enable a public IP address for an existing VM

You can only assign one public IP address to a VM. If the VM already has a public address, you cannot assign one more.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, open the page of the required VM.
3. Click **Attach resource** → **Public IP address**.
4. In the window that opens, select whether you want to assign an existing IP address or create a new one.
5. For an existing IP address, select the required one and then click **Assign address**.
6. For a new address, specify the address type: dynamic or static. After that, click **Create and assign address**.

After you enable an IP address for a VM, you can change the type of this address: make it static or dynamic. To do so, go to the VM page, open the **Network interface** tab and then click  → **Edit type** in the line of the required address.

**CLI**

To enable a **dynamic public IP address** for a VM, run the following command:

```bash theme={null}
nebius compute instance update \
  --id <VM_ID> \
  --network-interfaces "[{\"public_ip_address\": {} }]"
```

To enable a **static public IP address** for a VM, run the following command:

```bash theme={null}
nebius compute instance update \
  --id <VM_ID> \
  --network-interfaces "[{\"public_ip_address\": {\"static\": true}}]"
```

To assign an **already allocated public IP address** to a VM:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```bash theme={null}
   nebius vpc allocation create \
     --ipv4-public-subnet-id <subnet_ID> \
     --name <allocation_name>
   ```

3. Assign this allocation to the VM:

   ```bash theme={null}
   nebius compute instance update \
     --id <VM_ID> \
     --network-interfaces "[{\"public_ip_address\": {\"allocation_id\": \"<allocation_ID>\"}}]"
   ```

**Go SDK**

Enable a **dynamic public IP address** for a VM:

```go theme={null}
privateInstance1, err := sdk.Services().Compute().V1().
    Instance().Get(
        ctx,
        &compute.GetInstanceRequest{
            Id: "<VM_ID>",
        },
    )
if err != nil {
    return err
}
if privateInstance1.GetSpec() == nil {
    return errors.New("instance spec is missing")
}
privateInstance1.Spec.NetworkInterfaces[0].
    PublicIpAddress = &compute.PublicIPAddress{}
dynamicIPOperation, err := sdk.Services().Compute().V1().
    Instance().Update(
        ctx,
        &compute.UpdateInstanceRequest{
            Metadata: privateInstance1.Metadata,
            Spec:     privateInstance1.Spec,
        },
    )
if err != nil {
    return err
}
if _, err = dynamicIPOperation.Wait(ctx); err != nil {
    return err
}
```

Enable a **static public IP address** for a VM:

```go theme={null}
privateInstance2, err := sdk.Services().Compute().V1().
    Instance().Get(
        ctx,
        &compute.GetInstanceRequest{
            Id: "<VM_ID>",
        },
    )
if err != nil {
    return err
}
if privateInstance2.GetSpec() == nil {
    return errors.New("instance spec is missing")
}
privateInstance2.Spec.NetworkInterfaces[0].
    PublicIpAddress = &compute.PublicIPAddress{Static: true}
staticIPOperation, err := sdk.Services().Compute().V1().
    Instance().Update(
        ctx,
        &compute.UpdateInstanceRequest{
            Metadata: privateInstance2.Metadata,
            Spec:     privateInstance2.Spec,
        },
    )
if err != nil {
    return err
}
if _, err = staticIPOperation.Wait(ctx); err != nil {
    return err
}
```

To assign an **already allocated public IP address** to a VM:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```go theme={null}
   publicAllocationOperation, err := sdk.Services().VPC().V1().
       Allocation().Create(
           ctx,
           &vpc.CreateAllocationRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<allocation_name>",
               },
               Spec: &vpc.AllocationSpec{
                   IpSpec: &vpc.AllocationSpec_Ipv4Public{
                       Ipv4Public: &vpc.IPv4PublicAllocationSpec{
                           Pool: &vpc.IPv4PublicAllocationSpec_SubnetId{
                               SubnetId: "<subnet_ID>",
                           },
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = publicAllocationOperation.Wait(ctx); err != nil {
       return err
   }
   allocationID := publicAllocationOperation.ResourceID()
   ```

3. Assign this allocation to the VM:

   ```go theme={null}
   privateInstance3, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if privateInstance3.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   privateInstance3.Spec.NetworkInterfaces[0].
       PublicIpAddress = &compute.PublicIPAddress{
       Allocation: &compute.PublicIPAddress_AllocationId{
           AllocationId: "<allocation_ID>",
       },
   }
   allocationIPOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: privateInstance3.Metadata,
               Spec:     privateInstance3.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = allocationIPOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

Enable a **dynamic public IP address** for a VM:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
private_instance_1 = await instance_service.get(
    GetInstanceRequest(id="<VM_ID>"),
)
if private_instance_1.spec is None:
    raise ValueError("instance spec is missing")
private_instance_1.spec.network_interfaces[0].public_ip_address = (
    PublicIPAddress()
)
dynamic_ip_operation = await instance_service.update(
    UpdateInstanceRequest(
        metadata=private_instance_1.metadata,
        spec=private_instance_1.spec,
    ),
)
await dynamic_ip_operation.wait()
```

Enable a **static public IP address** for a VM:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
private_instance_2 = await instance_service.get(
    GetInstanceRequest(id="<VM_ID>"),
)
if private_instance_2.spec is None:
    raise ValueError("instance spec is missing")
private_instance_2.spec.network_interfaces[0].public_ip_address = (
    PublicIPAddress(static=True)
)
static_ip_operation = await instance_service.update(
    UpdateInstanceRequest(
        metadata=private_instance_2.metadata,
        spec=private_instance_2.spec,
    ),
)
await static_ip_operation.wait()
```

To assign an **already allocated public IP address** to a VM:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```python theme={null}
   allocation_service = AllocationServiceClient(sdk)
   public_allocation_operation = await allocation_service.create(
       CreateAllocationRequest(
           metadata=ResourceMetadata(name="<allocation_name>"),
           spec=AllocationSpec(
               ipv4_public=IPv4PublicAllocationSpec(
                   subnet_id="<subnet_ID>",
               ),
           ),
       ),
   )
   await public_allocation_operation.wait()
   allocation_id = public_allocation_operation.resource_id
   ```

3. Assign this allocation to the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   private_instance_3 = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if private_instance_3.spec is None:
       raise ValueError("instance spec is missing")
   private_instance_3.spec.network_interfaces[0].public_ip_address = (
       PublicIPAddress(allocation_id="<allocation_ID>")
   )
   allocation_ip_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=private_instance_3.metadata,
           spec=private_instance_3.spec,
       ),
   )
   await allocation_ip_operation.wait()
   ```

**JavaScript SDK**

Enable a **dynamic public IP address** for a VM:

```ts theme={null}
const dynamicIpService = new InstanceService(sdk);
const privateInstance1 = await dynamicIpService.get(
  GetInstanceRequest.create({
    id: "<VM_ID>",
  }),
);
if (!privateInstance1.spec) {
  throw new Error("instance spec is missing");
}
privateInstance1.spec.networkInterfaces[0].publicIpAddress =
  PublicIPAddress.create({});
const dynamicIpOperation = await dynamicIpService.update(
  UpdateInstanceRequest.create({
    metadata: privateInstance1.metadata,
    spec: privateInstance1.spec,
  }),
).result;
await dynamicIpOperation.wait();
```

Enable a **static public IP address** for a VM:

```ts theme={null}
const staticIpService = new InstanceService(sdk);
const privateInstance2 = await staticIpService.get(
  GetInstanceRequest.create({
    id: "<VM_ID>",
  }),
);
if (!privateInstance2.spec) {
  throw new Error("instance spec is missing");
}
privateInstance2.spec.networkInterfaces[0].publicIpAddress =
  PublicIPAddress.create({
    static: true,
  });
const staticIpOperation = await staticIpService.update(
  UpdateInstanceRequest.create({
    metadata: privateInstance2.metadata,
    spec: privateInstance2.spec,
  }),
).result;
await staticIpOperation.wait();
```

To assign an **already allocated public IP address** to a VM:

1. Get the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM.

2. Create an allocation that reserves a static public address:

   ```ts theme={null}
   const publicAllocationService = new AllocationService(sdk);
   const publicAllocationOperation =
     await publicAllocationService.create(
       CreateAllocationRequest.create({
         metadata: ResourceMetadata.create({
           name: "<allocation_name>",
         }),
         spec: AllocationSpec.create({
           ipSpec: {
             $case: "ipv4Public",
             ipv4Public: IPv4PublicAllocationSpec.create({
               pool: {
                 $case: "subnetId",
                 subnetId: "<subnet_ID>",
               },
             }),
           },
         }),
       }),
     ).result;
   await publicAllocationOperation.wait();
   const allocationId = publicAllocationOperation.resourceId();
   ```

3. Assign this allocation to the VM:

   ```ts theme={null}
   const allocationIpService = new InstanceService(sdk);
   const privateInstance3 = await allocationIpService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   if (!privateInstance3.spec) {
     throw new Error("instance spec is missing");
   }
   privateInstance3.spec.networkInterfaces[0].publicIpAddress =
     PublicIPAddress.create({
       allocation: {
         $case: "allocationId",
         allocationId: "<allocation_ID>",
       },
     });
   const allocationIpOperation = await allocationIpService.update(
     UpdateInstanceRequest.create({
       metadata: privateInstance3.metadata,
       spec: privateInstance3.spec,
     }),
   ).result;
   await allocationIpOperation.wait();
   ```

### How to get a VM's public IP address

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, open the page of the required VM.
3. Copy the **Public IPv4** value from the **Network** block.

**CLI**

```bash theme={null}
export PUBLIC_IP_ADDRESS=$(nebius compute instance get-by-name \
  --name <VM_name> \
  --format json \
  | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
echo $PUBLIC_IP_ADDRESS
```

**Go SDK**

```go theme={null}
publicIPInstance, err := sdk.Services().Compute().V1().
    Instance().GetByName(
        ctx,
        &common.GetByNameRequest{
            Name: "<VM_name>",
        },
    )
if err != nil {
    return err
}
publicAddress := publicIPInstance.GetStatus().
    GetNetworkInterfaces()[0].GetPublicIpAddress().GetAddress()
publicIPAddress := strings.Split(publicAddress, "/")[0]
fmt.Println(publicIPAddress)
```

**Python SDK**

```python theme={null}
instance_service = InstanceServiceClient(sdk)
public_ip_instance = await instance_service.get_by_name(
    GetByNameRequest(name="<VM_name>"),
)
public_address = (
    public_ip_instance.status.network_interfaces[0]
    .public_ip_address.address
)
public_ip_address = public_address.split("/")[0]
print(public_ip_address)
```

**JavaScript SDK**

```ts theme={null}
const publicIpLookupService = new InstanceService(sdk);
const publicIpInstance = await publicIpLookupService.getByName(
  GetByNameRequest.create({
    name: "<VM_name>",
  }),
);
const publicAddress = publicIpInstance.status
  ?.networkInterfaces[0]?.publicIpAddress?.address;
const publicIpAddress = publicAddress?.split("/")[0];
console.log(publicIpAddress);
```

### How to migrate a public static IP address from one VM to another

To reassign a public static IP address from one VM to another, detach this address from the source VM and attach it to the target VM.

Before you begin, make sure that you have a VM with a public static IP address (the source VM) and a VM without a public address (the target VM). For information about creating VMs, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

To migrate the address, do the following:

**CLI**

1. To get IDs of the source and target VMs, list all VMs:

   ```bash theme={null}
   nebius compute instance list
   ```

2. Store the VMs' IDs in environment variables:

   ```bash theme={null}
   SOURCE_VM="<source_VM_ID>"
   TARGET_VM="<target_VM_ID>"
   ```

3. Extract the allocation ID of the public static IP address currently attached to the source VM. This value is required to reassign the IP address to another VM.

   ```bash theme={null}
   ALLOC_ID=$(nebius compute instance get \
     --id "$SOURCE_VM" \
     --format json | jq -r '.status.network_interfaces[] | select(.name=="eth0")
     | .public_ip_address.allocation_id')
   ```

4. Pin the allocation in the source VM specification. This prevents the allocation from being deleted when you detach it in the next step.

   ```bash theme={null}
   nebius compute instance update --patch \
     --id "$SOURCE_VM" \
     "$(jq -n --arg alloc "$ALLOC_ID" '{"spec":{"network_interfaces":[{"name":"eth0","public_ip_address":{"static":true,"allocation_id":$alloc}}]}}')"
   ```

5. Remove the public IP address from the source VM. This makes the allocation available for reuse.

   ```bash theme={null}
   nebius compute instance update --patch \
     --id "$SOURCE_VM" \
     '{"spec":{"network_interfaces":
     [{"name":"eth0","public_ip_address":null}]}}'
   ```

6. Assign the same allocation ID to the target VM:

   ```bash theme={null}
   nebius compute instance update --patch \
     --id "$TARGET_VM" \
     "$(jq -n --arg alloc "$ALLOC_ID" '{"spec":{"network_interfaces":
     [{"name":"eth0","public_ip_address":{"static":true,"allocation_id":$alloc}}]}}')"
   ```

   The output of this command shows that the allocation is attached to the target VM.

**Go SDK**

1. To get IDs of the source and target VMs, list all VMs:

   ```go theme={null}
   instances, err := sdk.Services().Compute().V1().
       Instance().List(
           ctx,
           &compute.ListInstancesRequest{},
       )
   if err != nil {
       return err
   }
   fmt.Println(instances)
   ```

2. Set `sourceVM` to the ID of the source VM and `targetVM` to the ID of the target VM.

3. Extract the allocation ID of the public static IP address currently attached to the source VM. This value is required to reassign the IP address to another VM.

   ```go theme={null}
   sourceInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: sourceVM,
           },
       )
   if err != nil {
       return err
   }
   allocID := sourceInstance.GetStatus().
       GetNetworkInterfaces()[0].GetPublicIpAddress().GetAllocationId()
   if allocID == "" {
       return errors.New("allocation ID is missing")
   }
   ```

4. Pin the allocation in the source VM specification. This prevents the allocation from being deleted when you detach it in the next step.

   ```go theme={null}
   sourceInstanceForPin, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: sourceVM,
           },
       )
   if err != nil {
       return err
   }
   if sourceInstanceForPin.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   sourceInstanceForPin.Spec.NetworkInterfaces[0].
       PublicIpAddress = &compute.PublicIPAddress{
       Static: true,
       Allocation: &compute.PublicIPAddress_AllocationId{
           AllocationId: allocID,
       },
   }
   pinAllocationOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: sourceInstanceForPin.Metadata,
               Spec:     sourceInstanceForPin.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = pinAllocationOperation.Wait(ctx); err != nil {
       return err
   }
   ```

5. Remove the public IP address from the source VM. This makes the allocation available for reuse.

   ```go theme={null}
   removeInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: sourceVM,
           },
       )
   if err != nil {
       return err
   }
   if removeInstance.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   removeInstance.Spec.NetworkInterfaces[0].
       PublicIpAddress = nil
   removeAddressOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: removeInstance.Metadata,
               Spec:     removeInstance.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = removeAddressOperation.Wait(ctx); err != nil {
       return err
   }
   ```

6. Assign the same allocation ID to the target VM:

   ```go theme={null}
   assignInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: targetVM,
           },
       )
   if err != nil {
       return err
   }
   if assignInstance.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   assignInstance.Spec.NetworkInterfaces[0].
       PublicIpAddress = &compute.PublicIPAddress{
       Static: true,
       Allocation: &compute.PublicIPAddress_AllocationId{
           AllocationId: allocID,
       },
   }
   assignAddressOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: assignInstance.Metadata,
               Spec:     assignInstance.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = assignAddressOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. To get IDs of the source and target VMs, list all VMs:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instances = await instance_service.list(ListInstancesRequest())
   print(instances)
   ```

2. Set `source_vm` to the ID of the source VM and `target_vm` to the ID of the target VM.

3. Extract the allocation ID of the public static IP address currently attached to the source VM. This value is required to reassign the IP address to another VM.

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   source_instance = await instance_service.get(
       GetInstanceRequest(id=source_vm),
   )
   alloc_id = (
       source_instance.status.network_interfaces[0]
       .public_ip_address.allocation_id
   )
   if not alloc_id:
       raise ValueError("allocation ID is missing")
   ```

4. Pin the allocation in the source VM specification. This prevents the allocation from being deleted when you detach it in the next step.

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   source_instance_for_pin = await instance_service.get(
       GetInstanceRequest(id=source_vm),
   )
   if source_instance_for_pin.spec is None:
       raise ValueError("instance spec is missing")
   source_interfaces = source_instance_for_pin.spec.network_interfaces
   source_interfaces[0].public_ip_address = (
       PublicIPAddress(static=True, allocation_id=alloc_id)
   )
   pin_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=source_instance_for_pin.metadata,
           spec=source_instance_for_pin.spec,
       ),
   )
   await pin_operation.wait()
   ```

5. Remove the public IP address from the source VM. This makes the allocation available for reuse.

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   source_instance_for_removal = await instance_service.get(
       GetInstanceRequest(id=source_vm),
   )
   if source_instance_for_removal.spec is None:
       raise ValueError("instance spec is missing")
   source_instance_for_removal.spec.network_interfaces[
       0
   ].public_ip_address = None
   remove_address_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=source_instance_for_removal.metadata,
           spec=source_instance_for_removal.spec,
       ),
   )
   await remove_address_operation.wait()
   ```

6. Assign the same allocation ID to the target VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   target_instance = await instance_service.get(
       GetInstanceRequest(id=target_vm),
   )
   if target_instance.spec is None:
       raise ValueError("instance spec is missing")
   target_instance.spec.network_interfaces[0].public_ip_address = (
       PublicIPAddress(static=True, allocation_id=alloc_id)
   )
   assign_address_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=target_instance.metadata,
           spec=target_instance.spec,
       ),
   )
   await assign_address_operation.wait()
   ```

**JavaScript SDK**

1. To get IDs of the source and target VMs, list all VMs:

   ```ts theme={null}
   const listInstanceService = new InstanceService(sdk);
   const instances = await listInstanceService.list(
     ListInstancesRequest.create({}),
   );
   console.log(instances);
   ```

2. Set `sourceVm` to the ID of the source VM and `targetVm` to the ID of the target VM.

3. Extract the allocation ID of the public static IP address currently attached to the source VM. This value is required to reassign the IP address to another VM.

   ```ts theme={null}
   const sourceInstanceService = new InstanceService(sdk);
   const sourceInstance = await sourceInstanceService.get(
     GetInstanceRequest.create({
       id: sourceVm,
     }),
   );
   const allocId = sourceInstance.status
     ?.networkInterfaces[0]?.publicIpAddress?.allocationId;
   if (!allocId) {
     throw new Error("allocation ID is missing");
   }
   ```

4. Pin the allocation in the source VM specification. This prevents the allocation from being deleted when you detach it in the next step.

   ```ts theme={null}
   const pinAllocationService = new InstanceService(sdk);
   const sourceInstanceForPin = await pinAllocationService.get(
     GetInstanceRequest.create({
       id: sourceVm,
     }),
   );
   if (!sourceInstanceForPin.spec) {
     throw new Error("instance spec is missing");
   }
   sourceInstanceForPin.spec.networkInterfaces[0].publicIpAddress =
     PublicIPAddress.create({
       static: true,
       allocation: {
         $case: "allocationId",
         allocationId: allocId,
       },
     });
   const pinAllocationOperation = await pinAllocationService.update(
     UpdateInstanceRequest.create({
       metadata: sourceInstanceForPin.metadata,
       spec: sourceInstanceForPin.spec,
     }),
   ).result;
   await pinAllocationOperation.wait();
   ```

5. Remove the public IP address from the source VM. This makes the allocation available for reuse.

   ```ts theme={null}
   const removeAddressService = new InstanceService(sdk);
   const sourceInstanceForRemoval = await removeAddressService.get(
     GetInstanceRequest.create({
       id: sourceVm,
     }),
   );
   if (!sourceInstanceForRemoval.spec) {
     throw new Error("instance spec is missing");
   }
   sourceInstanceForRemoval.spec.networkInterfaces[0].publicIpAddress =
     undefined;
   const removeAddressOperation = await removeAddressService.update(
     UpdateInstanceRequest.create({
       metadata: sourceInstanceForRemoval.metadata,
       spec: sourceInstanceForRemoval.spec,
     }),
   ).result;
   await removeAddressOperation.wait();
   ```

6. Assign the same allocation ID to the target VM:

   ```ts theme={null}
   const assignAddressService = new InstanceService(sdk);
   const targetInstance = await assignAddressService.get(
     GetInstanceRequest.create({
       id: targetVm,
     }),
   );
   if (!targetInstance.spec) {
     throw new Error("instance spec is missing");
   }
   targetInstance.spec.networkInterfaces[0].publicIpAddress =
     PublicIPAddress.create({
       static: true,
       allocation: {
         $case: "allocationId",
         allocationId: allocId,
       },
     });
   const assignAddressOperation = await assignAddressService.update(
     UpdateInstanceRequest.create({
       metadata: targetInstance.metadata,
       spec: targetInstance.spec,
     }),
   ).result;
   await assignAddressOperation.wait();
   ```

## How to detach an IP address from a VM

To detach a public address or a secondary private address from a VM:

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, open the page of the required VM and then go to the **Network interface** tab.
3. In the line of the allocation that you want to detach from a VM, click  → **Detach**.
4. In the window that opens, confirm the action.

**CLI**

To detach a public IP address, set the `SOURCE_VM` environment variable to the VM ID and run the following command:

```bash theme={null}
nebius compute instance update --patch \
  --id "$SOURCE_VM" \
  '{"spec":{"network_interfaces":
  [{"name":"eth0","public_ip_address":null}]}}'
```

To detach a secondary private IP address, run the following command:

```bash theme={null}
nebius compute instance update \
  --id <VM_ID> \
  --network-interfaces "[{\"aliases\": []}]"
```

If the VM has several secondary private IP addresses, keep the aliases that you do not want to detach in the `aliases` list.

**Go SDK**

To detach a public IP address, set `sourceVM` to the VM ID:

```go theme={null}
removeInstance, err := sdk.Services().Compute().V1().
    Instance().Get(
        ctx,
        &compute.GetInstanceRequest{
            Id: sourceVM,
        },
    )
if err != nil {
    return err
}
if removeInstance.GetSpec() == nil {
    return errors.New("instance spec is missing")
}
removeInstance.Spec.NetworkInterfaces[0].
    PublicIpAddress = nil
removeAddressOperation, err := sdk.Services().Compute().V1().
    Instance().Update(
        ctx,
        &compute.UpdateInstanceRequest{
            Metadata: removeInstance.Metadata,
            Spec:     removeInstance.Spec,
        },
    )
if err != nil {
    return err
}
if _, err = removeAddressOperation.Wait(ctx); err != nil {
    return err
}
```

Detach a secondary private IP address:

```go theme={null}
detachAliasInstance, err := sdk.Services().Compute().V1().
    Instance().Get(
        ctx,
        &compute.GetInstanceRequest{
            Id: "<VM_ID>",
        },
    )
if err != nil {
    return err
}
if detachAliasInstance.GetSpec() == nil {
    return errors.New("instance spec is missing")
}
detachNetworkInterfaces := detachAliasInstance.Spec.NetworkInterfaces
aliases := detachNetworkInterfaces[0].Aliases[:0]
for _, alias := range detachNetworkInterfaces[0].Aliases {
    if alias.GetAllocationId() != "<allocation_ID>" {
        aliases = append(aliases, alias)
    }
}
detachNetworkInterfaces[0].Aliases = aliases
detachAliasOperation, err := sdk.Services().Compute().V1().
    Instance().Update(
        ctx,
        &compute.UpdateInstanceRequest{
            Metadata: detachAliasInstance.Metadata,
            Spec:     detachAliasInstance.Spec,
        },
    )
if err != nil {
    return err
}
if _, err = detachAliasOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

To detach a public IP address, set `source_vm` to the VM ID:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
source_instance_for_removal = await instance_service.get(
    GetInstanceRequest(id=source_vm),
)
if source_instance_for_removal.spec is None:
    raise ValueError("instance spec is missing")
source_instance_for_removal.spec.network_interfaces[
    0
].public_ip_address = None
remove_address_operation = await instance_service.update(
    UpdateInstanceRequest(
        metadata=source_instance_for_removal.metadata,
        spec=source_instance_for_removal.spec,
    ),
)
await remove_address_operation.wait()
```

Detach a secondary private IP address:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
detach_alias_instance = await instance_service.get(
    GetInstanceRequest(id="<VM_ID>"),
)
if detach_alias_instance.spec is None:
    raise ValueError("instance spec is missing")
aliases = detach_alias_instance.spec.network_interfaces[0].aliases
detach_alias_instance.spec.network_interfaces[0].aliases = [
    alias
    for alias in aliases
    if alias.allocation_id != "<allocation_ID>"
]
detach_alias_operation = await instance_service.update(
    UpdateInstanceRequest(
        metadata=detach_alias_instance.metadata,
        spec=detach_alias_instance.spec,
    ),
)
await detach_alias_operation.wait()
```

**JavaScript SDK**

To detach a public IP address, set `sourceVm` to the VM ID:

```ts theme={null}
const removeAddressService = new InstanceService(sdk);
const sourceInstanceForRemoval = await removeAddressService.get(
  GetInstanceRequest.create({
    id: sourceVm,
  }),
);
if (!sourceInstanceForRemoval.spec) {
  throw new Error("instance spec is missing");
}
sourceInstanceForRemoval.spec.networkInterfaces[0].publicIpAddress =
  undefined;
const removeAddressOperation = await removeAddressService.update(
  UpdateInstanceRequest.create({
    metadata: sourceInstanceForRemoval.metadata,
    spec: sourceInstanceForRemoval.spec,
  }),
).result;
await removeAddressOperation.wait();
```

Detach a secondary private IP address:

```ts theme={null}
const detachAliasService = new InstanceService(sdk);
const detachAliasInstance = await detachAliasService.get(
  GetInstanceRequest.create({
    id: "<VM_ID>",
  }),
);
if (!detachAliasInstance.spec) {
  throw new Error("instance spec is missing");
}
const aliases =
  detachAliasInstance.spec.networkInterfaces[0].aliases ?? [];
detachAliasInstance.spec.networkInterfaces[0].aliases =
  aliases.filter(
    (alias) => alias.allocationId !== "<allocation_ID>",
  );
const detachAliasOperation = await detachAliasService.update(
  UpdateInstanceRequest.create({
    metadata: detachAliasInstance.metadata,
    spec: detachAliasInstance.spec,
  }),
).result;
await detachAliasOperation.wait();
```
