# How to update settings of a virtual machine in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/update

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to update settings of a virtual machine in Nebius AI Cloud

You can update settings of an existing Compute virtual machine (VM) by using any Nebius AI Cloud interface. For a description of all VM settings, see [Parameters of a virtual machine configuration](https://docs.nebius.com/compute/virtual-machines/params.md).

## Preset

A preset defines the resources, the number of vCPUs and the amount of RAM, allocated to a VM on its [platform](https://docs.nebius.com/compute/virtual-machines/types.md). Change a VM's preset when its workload is constrained by its current resources or it has too many of them.

Regular and preemptible VMs use the same settings to change their presets.

This action requires you to stop the VM.

See available presets for [GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms) and [non-GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-non-gpu-platforms).

To update a preset:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. Select the VM for which you want to change the preset.

3. Click  **Stop** and confirm the action.

   Wait for the VM's status to change to `Stopped`.

4. On the VM's page, select the **Settings** tab.

5. Under **Computing resources**, select the **Preset** you want and click **Save changes**.

6. Click  **Start VM** and confirm the action.

   Wait for the VM's status to change to `Running`.

**CLI**

1. Get the ID of the VM for which you want to change the preset:

   ```bash theme={null}
   nebius compute instance list
   ```

2. Stop the VM:

   ```bash theme={null}
   nebius compute instance stop --id <VM_ID>
   ```

3. Update the resource preset:

   ```bash theme={null}
   nebius compute instance update \
     --id <VM_ID> \
     --parent-id <project_ID> \
     --resources-preset <preset_ID>
   ```

4. Start the VM:

   ```bash theme={null}
   nebius compute instance start --id <VM_ID>
   ```

**Terraform**

1. Stop the VM:

   1. Add `stopped = true` to the resource configuration:

      ```hcl theme={null}
      resource "nebius_compute_v1_instance" "my_vm" {
        # ...
        stopped = true
      }
      ```

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

2. With the VM stopped, update the resource preset:

   1. Change the `preset` value in the `resources` section:

      ```hcl theme={null}
      resource "nebius_compute_v1_instance" "my_vm" {
        # ...
        resources = {
          platform = "<current_platform_ID>"  # Keep the current platform ID.
          preset   = "<new_preset_ID>" # Update the preset value only.
        }
        stopped = true
      }
      ```

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

3. Start the VM:

   1. Change the `stopped` parameter to `false`:

      ```hcl theme={null}
      resource "nebius_compute_v1_instance" "my_vm" {
        # ...
        stopped = false
      }
      ```

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

**Go SDK**

1. Get the ID of the VM for which you want to change the preset:

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

2. Stop the VM:

   ```go theme={null}
   stopInstanceOperation, err := sdk.Services().Compute().V1().
       Instance().Stop(
           ctx,
           &compute.StopInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = stopInstanceOperation.Wait(ctx); err != nil {
       return err
   }
   ```

3. Update the resource preset:

   ```go theme={null}
   instanceToResize, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if instanceToResize.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   instanceToResize.Spec.Resources.
       Size = &compute.ResourcesSpec_Preset{
       Preset: "<preset_ID>",
   }
   updatePresetOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: instanceToResize.Metadata,
               Spec:     instanceToResize.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = updatePresetOperation.Wait(ctx); err != nil {
       return err
   }
   ```

4. Start the VM:

   ```go theme={null}
   startOperation, err := sdk.Services().Compute().V1().
       Instance().Start(
           ctx,
           &compute.StartInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = startOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the ID of the VM for which you want to change the preset:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instances = await instance_service.list(ListInstancesRequest())
   print(instances)
   ```

2. Stop the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   stop_instance_operation = await instance_service.stop(
       StopInstanceRequest(id="<VM_ID>"),
   )
   await stop_instance_operation.wait()
   ```

3. Update the resource preset:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance_to_resize = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if instance_to_resize.spec is None:
       raise ValueError("instance spec is missing")
   instance_to_resize.spec.resources.preset = "<preset_ID>"
   update_preset_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=instance_to_resize.metadata,
           spec=instance_to_resize.spec,
       ),
   )
   await update_preset_operation.wait()
   ```

4. Start the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   start_instance_operation = await instance_service.start(
       StartInstanceRequest(id="<VM_ID>"),
   )
   await start_instance_operation.wait()
   ```

**JavaScript SDK**

1. Get the ID of the VM for which you want to change the preset:

   ```ts theme={null}
   const manageListInstanceService = new InstanceService(sdk);
   const listedInstances = await manageListInstanceService.list(
     ListInstancesRequest.create({}),
   );
   console.log(listedInstances);
   ```

2. Stop the VM:

   ```ts theme={null}
   const stopInstanceService = new InstanceService(sdk);
   const stopInstanceOperation = await stopInstanceService.stop(
     StopInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await stopInstanceOperation.wait();
   ```

3. Update the resource preset:

   ```ts theme={null}
   const instanceService = new InstanceService(sdk);
   const instanceToResize = await instanceService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   if (!instanceToResize.spec) {
     throw new Error("instance spec is missing");
   }
   instanceToResize.spec.resources.size = {
     $case: "preset",
     preset: "<preset_ID>",
   };
   const updatePresetOperation = await instanceService.update(
     UpdateInstanceRequest.create({
       metadata: instanceToResize.metadata,
       spec: instanceToResize.spec,
     }),
   ).result;
   await updatePresetOperation.wait();
   ```

4. Start the VM:

   ```ts theme={null}
   const startInstanceService = new InstanceService(sdk);
   const startInstanceOperation = await startInstanceService.start(
     StartInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await startInstanceOperation.wait();
   ```

## Hostname

A VM's hostname is used to generate its [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md). Change the hostname if you want the VM to be reachable by a custom internal DNS name instead of an autogenerated one.

You do not need to stop the VM to change its hostname.

To set the hostname:

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

## Reservation policy

If you apply the reservation policy, the VM's resources are allocated from reservations, which represent [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md). For more information, see [Capacity reservations for Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/reservations.md).

Change the reservation policy in the following cases:

* You got reservations after creating the VM and you want the VM to use them.
* A reservation is about to expire or has run out of capacity and you want the VM to use another one.
* You want to move the VM out of reservations.

VMs of a regular type and with GPUs support reservations. [Preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) and VMs without GPUs do not support them.

**Web console**

If you want to [create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) and you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), on the **General** step, select **Reserved VM**. On the **Compute** step, select a platform and configure the **Reservation** settings. If you do not have capacity block groups, the wizard skips the **General** step and opens **Compute** instead.

If you want to modify an existing VM, [stop it](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) first and then go to its **Settings** tab on the VM page. Next, update the reservation settings.

The **Reservation** section is only displayed if you have capacity block groups.

In the **Reservation** section, you can configure the following options:

* **Any (existing and future)** (default): Compute selects among your matching capacity block groups automatically.
* **Specific capacity block groups**: Select one or more capacity block groups. Each option shows the capacity block group ID, reservation period and GPU usage. Make sure the selected groups have enough capacity and do not expire soon.
* **Switch to PAYG**: Choose whether the VM can start after you create or restart it without active intervals in selected capacity block groups:

  * **When reservation is exhausted** (default): The VM can start as a pay-as-you-go VM when no capacity is available in the selected capacity block groups.
  * **Never**: The VM cannot start without available capacity in the selected capacity block groups.

  This does not affect the VM when it is running. If an interval in a selected capacity block group expires while the VM is running, the VM always continues as a pay-as-you-go VM, regardless of this setting.

If you have capacity block groups in multiple regions, select a **Region** first.

**CLI**

Use the `--reservation-policy-*` parameters when creating or updating a VM:

* To create a VM, use the following command:

  ```bash theme={null}
  nebius compute instance create \
    ... \
    --reservation-policy-policy <auto|forbid|strict> \
    --reservation-policy-reservation-ids <reservations>
  ```

* To update a VM, [stop it](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) first and then use the following command:

  ```bash theme={null}
  nebius compute instance update \
    ... \
    --reservation-policy-policy <auto|forbid|strict> \
    --reservation-policy-reservation-ids <reservations>
  ```

Description of the parameters:

* `--reservation-policy-policy`: Policy for reservation usage. Supports the following values:

  * `auto`: VM resources are allocated from reservations. If no reservations are currently available, the VM runs without them. In this case, resources for the VM are provided from the common pool.

    > [!NOTE]
    >
    > The `auto` value is the default. If you don't have any reservations and you don't set the `--reservation-policy-policy` parameter, the `auto` value applies and the VM runs without reservations.
  * `forbid`: VM resources are provided from the common pool, and no reservations are used.
  * `strict`: VM resources are exclusively allocated from reservations. The VM doesn't run without the reservations.

* `--reservation-policy-reservation-ids` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation-ids` | **Behavior** |
| - | - | - |
| `auto` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `auto` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `forbid` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `forbid` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `strict` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `strict` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**Terraform**

Use the `reservation_policy` parameter in the VM configuration:

```hcl theme={null}
resource "nebius_compute_v1_instance" "my_vm" {
  ...
  reservation_policy = {
    policy          = "<AUTO|FORBID|STRICT>"
    reservation_ids = "<reservations>"
  }
  ...
}
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the following values:

  * `AUTO`: VM resources are allocated from reservations. If no reservations are currently available, the VM runs without them. In this case, resources for the VM are provided from the common pool.

    > [!NOTE]
    >
    > The `AUTO` value is the default. If you don't have any reservations and you don't set the `policy` parameter, the `AUTO` value applies and the VM runs without reservations.
  * `FORBID`: VM resources are provided from the common pool, and no reservations are used.
  * `STRICT`: VM resources are exclusively allocated from reservations. The VM doesn't run without the reservations.

* `reservation_ids`: IDs of specific reservations (capacity block groups). You can use this parameter with the `AUTO` and `STRICT` reservation usages:

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation_ids` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**Go SDK**

Use `ReservationPolicy` in `InstanceSpec` when creating or updating a VM:

```go theme={null}
reservationPolicy := &compute.ReservationPolicy{
    Policy: compute.ReservationPolicy_STRICT,
    ReservationIds: []string{
        "<reservation_ID>",
    },
}
```

Description of the parameters:

* `Policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `ReservationIds` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `Policy` | `ReservationIds` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**Python SDK**

Use `reservation_policy` in `InstanceSpec` when creating or updating a VM:

```python theme={null}
reservation_policy = ReservationPolicy(
    policy=ReservationPolicy.Policy.STRICT,
    reservation_ids=["<reservation_ID>"],
)
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `reservation_ids` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation_ids` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**JavaScript SDK**

Use `reservationPolicy` in `InstanceSpec` when creating or updating a VM:

```ts theme={null}
const reservationPolicy = ReservationPolicy.create({
  policy: ReservationPolicy_Policy.STRICT,
  reservationIds: ["<reservation_ID>"],
});
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `reservationIds` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservationIds` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

## Network interfaces

You can change the following parts of a VM's network configuration without recreating the VM:

* [Enable a public IP address for an existing VM](https://docs.nebius.com/compute/virtual-machines/network.md#how-to-enable-a-public-ip-address-for-an-existing-vm)
* [Migrate a static public IP address from one VM to another](https://docs.nebius.com/compute/virtual-machines/network.md#how-to-migrate-a-public-static-ip-address-from-one-vm-to-another)
* [Detach an IP address from a VM](https://docs.nebius.com/compute/virtual-machines/network.md#how-to-detach-an-ip-address-from-a-vm)
* [Assign a secondary private IP address to a VM](https://docs.nebius.com/compute/virtual-machines/network.md#how-to-assign-a-secondary-private-ip-address-to-a-vm)
