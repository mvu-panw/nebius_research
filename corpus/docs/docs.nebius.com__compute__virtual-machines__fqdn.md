# FQDN and hostname of a virtual machine

Source: https://docs.nebius.com/compute/virtual-machines/fqdn

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# FQDN and hostname of a virtual machine

When you create a virtual machine (VM), the service assigns an [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) to this VM. By using this FQDN, other VMs can access your VM within a single [network](https://docs.nebius.com/vpc/overview.md#network). The FQDN is registered in the [DNS zone](https://docs.nebius.com/vpc/dns/overview.md) that Nebius AI Cloud creates for this network.

You can configure the FQDN on your own or you can use the default FQDN:

* The format of the default FQDN is the following:

  ```text theme={null}
  <VM_ID>.<VM_network_ID>.compute.internal.
  ```

  In this case, the FQDN (as well as the VM's ID) is only known after the VM is created.

* The format of a custom FQDN is the following:

  ```text theme={null}
  <hostname>.<VM_network_ID>.compute.internal.
  ```

  You can [set the hostname](#how-to-customize-an-fqdn) when you create or update a VM.

You can configure an FQDN, but you cannot delete it.

The guest OS hostname of the VM is set up during the VM creation; it matches the FQDN. If the FQDN is changed later, the guest OS hostname does not change; and it remains the same as the FQDN was when the VM was created.

## Prerequisites

> [!TIP]
>
> You do not need to complete any prerequisites if you use the web console.

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Terraform**

[Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to get an FQDN

**Web console**

To get an FQDN of a VM:

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. Select either the **Standalone VMs** or **Kubernetes nodes** tab.
3. Open the page of the required VM.
4. On the **Overview** tab, from the **Network** section, copy the FQDN value.

**CLI**

To get an FQDN of a VM, run the following command:

```bash theme={null}
nebius compute instance get-by-name \
  --name <VM_name> \
  --format json \
  | jq -r '.status.network_interfaces[0].fqdn | split("/")[0]'
```

The FQDN is specified in the `status.network_interfaces.fqdn` field of the output.

**Go SDK**

Get an FQDN of a VM:

```go theme={null}
fqdnInstance, err := sdk.Services().Compute().V1().
    Instance().GetByName(
        ctx,
        &common.GetByNameRequest{
            Name: "<VM_name>",
        },
    )
if err != nil {
    return err
}
fqdn := fqdnInstance.GetStatus().GetNetworkInterfaces()[0].GetFqdn()
fmt.Println(strings.Split(fqdn, "/")[0])
```

**Python SDK**

Get an FQDN of a VM:

```python theme={null}
fqdn_service = InstanceServiceClient(sdk)
fqdn_instance = await fqdn_service.get_by_name(
    GetByNameRequest(name="<VM_name>"),
)
fqdn = fqdn_instance.status.network_interfaces[0].fqdn
print(fqdn.split("/")[0])
```

**JavaScript SDK**

Get an FQDN of a VM:

```ts theme={null}
const fqdnInstanceService = new InstanceService(sdk);
const fqdnInstance = await fqdnInstanceService.getByName(
  GetByNameRequest.create({
    name: "<VM_name>",
  }),
);
const fqdn = fqdnInstance.status?.networkInterfaces[0]?.fqdn;
console.log(fqdn?.split("/")[0]);
```

## How to customize an FQDN

If you do not want to use the default FQDN, you can use your own hostname instead of the VM's ID. To customize an FQDN, use the `hostname` parameter:

**Web console**

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) with a customized FQDN:

   In the VM creation wizard, on the **Network** step, in the **Hostname** field, select **Custom** and specify the hostname for the VM's FQDN.

2. Change the FQDN of the created VM:

   1. In the sidebar, go to  **Compute** → **Virtual machines**.
   2. Select either the **Standalone VMs** or **Kubernetes nodes** tab.
   3. Open the page of the required VM.
   4. Go to the **Settings** tab.
   5. Modify the **Hostname** field.
   6. Click **Save changes**.

**CLI**

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) with a customized FQDN:

   ```bash theme={null}
   nebius compute instance create \
      ... \
      --hostname <FQDN_prefix>
   ```

2. Change an FQDN of an existing VM:

   ```bash theme={null}
   nebius compute instance update --id <VM_ID> --hostname <FQDN_prefix>
   ```

**Terraform**

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) with a customized FQDN:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     ...
     hostname = "<FQDN_prefix>"
     ...
   }
   ```

2. Change the FQDN of the created VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     # ...
     hostname = "<FQDN_prefix>"
   }
   ```

3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) with a customized FQDN:

   ```go theme={null}
   instanceOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "vm-for-scenario",
               },
               Spec: &compute.InstanceSpec{
                   Resources: &compute.ResourcesSpec{
                       Platform: "cpu-d3",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "4vcpu-16gb",
                       },
                   },
                   BootDisk: &compute.AttachedDiskSpec{
                       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
                       DeviceId:   "my-device",
                       Type: &compute.AttachedDiskSpec_ExistingDisk{
                           ExistingDisk: &compute.ExistingDisk{
                               Id: bootDiskID,
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
                   Hostname: "<FQDN_prefix>",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = instanceOperation.Wait(ctx); err != nil {
       return err
   }
   vmID := instanceOperation.ResourceID()
   ```

2. Change the FQDN of the created VM:

   ```go theme={null}
   instance, err = sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if instance.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   instance.Spec.Hostname = "<FQDN_prefix>"
   instanceOperation, err = sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: instance.Metadata,
               Spec:     instance.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = instanceOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) with a customized FQDN:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   create_instance_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="vm-for-scenario"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-d3",
                   preset="4vcpu-16gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(id=boot_disk_id),
                   device_id="my-device",
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
               hostname="<FQDN_prefix>",
           ),
       ),
   )
   await create_instance_operation.wait()
   vm_id = create_instance_operation.resource_id
   ```

2. Change the FQDN of the created VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if instance.spec is None:
       raise ValueError("instance spec is missing")
   instance.spec.hostname = "<FQDN_prefix>"
   update_instance_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=instance.metadata,
           spec=instance.spec,
       ),
   )
   await update_instance_operation.wait()
   ```

**JavaScript SDK**

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) with a customized FQDN:

   ```ts theme={null}
   const instanceService = new InstanceService(sdk);
   const createInstanceOperation = await instanceService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "vm-for-scenario",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "cpu-d3",
           size: {
             $case: "preset",
             preset: "4vcpu-16gb",
           },
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           deviceId: "my-device",
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: bootDiskId,
             }),
           },
         }),
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId: subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
         hostname: "<FQDN_prefix>",
       }),
     }),
   ).result;
   await createInstanceOperation.wait();
   const vmId = createInstanceOperation.resourceId();
   ```

2. Change the FQDN of the created VM:

   ```ts theme={null}
   const updateInstanceService = new InstanceService(sdk);
   const instanceForHostname = await updateInstanceService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   if (!instanceForHostname.spec) {
     throw new Error("instance spec is missing");
   }
   instanceForHostname.spec.hostname = "<FQDN_prefix>";
   const updateInstanceOperation = await updateInstanceService.update(
     UpdateInstanceRequest.create({
       metadata: instanceForHostname.metadata,
       spec: instanceForHostname.spec,
     }),
   ).result;
   await updateInstanceOperation.wait();
   ```

The hostname must be unique, and it cannot contain a full stop (`.`).

For example, if you set `hostname` to `my-host`, the FQDN is the following:

```text theme={null}
my-host.vpcnetwork-e00***.compute.internal.
```

If you do not set `hostname`, the VM's ID is used instead of the hostname, according to the default FQDN.
