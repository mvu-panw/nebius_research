# Attaching and mounting Compute volumes to VMs

Source: https://docs.nebius.com/compute/storage/use

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Attaching and mounting Compute volumes to VMs

In this article, you will learn how to use [Compute disks and shared filesystems](https://docs.nebius.com/compute/storage/types.md) on virtual machines (VMs).

> [!NOTE]
>
> This article only covers additional volumes: non-boot disks and shared filesystems. You add a boot disk when you create a VM.

After [creating a disk](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk) or a [shared filesystem](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-shared-filesystem), you need to do the following to use it on a VM:

1. [Attach it to the VM](#how-to-attach-volumes-to-vms) by using Nebius AI Cloud interfaces.
2. [Mount it to the VM](#how-to-mount-volumes-to-vms) inside the VM's operating system.

A VM and its volumes must be located in the same project. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to attach volumes to VMs

To attach disks or shared filesystems to a VM:

**Web console**

* **New VM**

  In the VM creation wizard ( **Compute** → **Virtual machines** → **Create resource** → **Virtual machine**), on the **Storage** step, do the following:

  1. Click **Attach disk** or **Attach shared filesystem**.

  2. Set up the volume:

     1. Select whether you want to add a new or existing volume.

        If an existing disk is already added to another VM, you cannot add it to the new VM. A filesystem can be shared by multiple VMs.

     2. For a new volume, set its [parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

     3. Set a device ID if you are adding a disk, or a mount tag if you are attaching a filesystem. Device IDs and mount tags are used to [mount volumes to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms).

  3. Click the attach-volume button at the end of the window.

     > [!WARNING]
     >
     > When you click **Create and add disk** or **Create and attach filesystem**, the disk or filesystem is created immediately and [charged](https://docs.nebius.com/compute/resources/pricing.md#volumes) separately even if you remove it from the VM later or do not proceed with creating the VM.

  4. If you want to [manually mount the filesystem](#shared-filesystems) that you added to the VM, turn off the **Auto mount** option for the filesystem.

     By default, Compute automatically mounts filesystems that you add to VMs via the web console.

     If you add a disk, you always need to [mount it manually](#disks).

* **Existing VM**

  **Disks**

  1. In the sidebar, go to  **Compute** → **Virtual machines**.

  2. On the **Standalone VMs** tab, open the page of the required VM.

  3. Switch to the **Disks** tab.

  4. Click **Attach resource** → **Disk**.

  5. Select whether you want to attach a new or existing disk.

     If an existing disk is already attached to another VM, you cannot attach it to a new VM until you [detach](https://docs.nebius.com/compute/storage/detach-volume.md) it from the current VM.

  6. For a new disk, set its [parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

  7. Set a device ID for the disk. Device IDs are used to [mount disks to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms).

  8. Click the attach-volume button at the end of the window.

  **Shared filesystems**

  1. In the sidebar, go to  **Compute** → **Virtual machines**.

  2. On the **Standalone VMs** tab, open the page of the required VM.

  3. If the VM is not in the `Stopped` status, click **Stop VM** and then confirm the action.

  4. After the VM has the `Stopped` status, switch to the **Filesystems** tab.

  5. Click **Attach resource** → **Filesystem**.

  6. Select whether you want to attach a new or existing filesystem.

     A filesystem can be shared by multiple VMs.

  7. For a new filesystem, set its [parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

  8. Set a mount tag for the filesystem. Mount tags are used to [mount filesystems to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms).

  9. Click the attach-volume button at the end of the window.

**CLI**

1. [Create the volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Create the following files locally:

   * `secondary_disk.json` to attach disks:

     ```json theme={null}
     [
       {
         "attach_mode": "READ_WRITE",
         "existing_disk": {
           "id": "<disk_ID>"
         },
         "device_id": "<device_ID>"
       }
     ]
     ```

     Where:

     * Write permission. The only supported value is `READ_WRITE`.
     * `existing_disk.id`: Disk ID to be added. To get the ID, run `nebius compute disk list`.
     * `device_id`: Disk device ID. This parameter is different from `existing_disk.id`, as `device_id` is used for [mounting a disk to a VM](https://docs.nebius.com/compute/storage/use.md#disks).

       Create your own device ID, such as `my-disk`. Make sure that it is unique within a VM.

       If you do not specify the device ID, it takes the `disk-N` default value where `N` is an integer. For example, `disk-0`.

   * `filesystem.json` to attach shared filesystems:

     ```json theme={null}
     [
       {
         "attach_mode": "READ_WRITE",
         "existing_filesystem": {
           "id": "<filesystem_ID>"
         },
         "mount_tag": "<filesystem_tag>"
       }
     ]
     ```

     Where:

     * Write permission. The only supported value is `READ_WRITE`.
     * `existing_filesystem.id`: Filesystem ID to be attached. To get the ID, run `nebius compute filesystem list`.
     * `mount_tag`: Tag for [mounting a filesystem to a VM](#shared-filesystems).

       Create your own tag, such as `my-filesystem`. Make sure that it is unique within a VM.

       If you do not specify the tag, it takes the `filesystem-N` default value where `N` is an integer. For example, `filesystem-0`.

3. Create or update a VM with the volumes configured:

   * To **create a VM**, run the following command:

     ```bash theme={null}
     nebius compute instance create \
       --secondary-disks "$(cat secondary_disk.json)" \
       --filesystems "$(cat filesystem.json)" \
       <other_parameters>
     ```

   * To **attach disks to an existing VM**, run the following command:

     ```bash theme={null}
     nebius compute instance update <VM_ID> \
       --patch \
       --secondary-disks "$(cat secondary_disk.json)"
     ```

     To get the ID of an existing VM, run `nebius compute instance list`.

     The `--patch` parameter allows you to only update the specified parameters. Without it, the command resets the VM settings to their default values.

   * To **attach shared filesystems to an existing VM**, stop the VM first:

     ```bash theme={null}
     nebius compute instance stop --id <VM_ID>
     ```

     Then update the VM:

     ```bash theme={null}
     nebius compute instance update <VM_ID> \
       --patch \
       --filesystems "$(cat filesystem.json)"
     ```

     After the update, start the VM:

     ```bash theme={null}
     nebius compute instance start --id <VM_ID>
     ```

**Go SDK**

1. [Create the volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Set the attachment parameters in the code examples:

   In the code examples, set the attachment parameters:

   * For disks, set the attach mode, existing disk ID and device ID.
   * For shared filesystems, set the attach mode, existing filesystem ID and mount tag.

   Create your own mount tag, such as `my-filesystem`. Make sure that it is unique within a VM. If you do not specify the tag, it takes the `filesystem-N` default value where `N` is an integer. For example, `filesystem-0`.

3. Create or update a VM with the volumes configured:

   * **Create a VM**:

     ```go theme={null}
     diskAttachMode := compute.AttachedDiskSpec_READ_WRITE
     filesystemAttachMode := compute.AttachedFilesystemSpec_READ_WRITE
     existingFS := &compute.ExistingFilesystem{
         Id: filesystemID,
     }
     fsType := &compute.AttachedFilesystemSpec_ExistingFilesystem{
         ExistingFilesystem: existingFS,
     }
     instanceOperation, err := sdk.Services().Compute().V1().
         Instance().Create(
             ctx,
             &compute.CreateInstanceRequest{
                 Metadata: &common.ResourceMetadata{
                     Name: "vm-name",
                 },
                 Spec: &compute.InstanceSpec{
                     Stopped: false,
                     Resources: &compute.ResourcesSpec{
                         Platform: "cpu-e2",
                         Size: &compute.ResourcesSpec_Preset{
                             Preset: "2vcpu-8gb",
                         },
                     },
                     BootDisk: &compute.AttachedDiskSpec{
                         AttachMode: diskAttachMode,
                         Type: &compute.AttachedDiskSpec_ExistingDisk{
                             ExistingDisk: &compute.ExistingDisk{
                                 Id: bootDiskID1,
                             },
                         },
                     },
                     SecondaryDisks: []*compute.AttachedDiskSpec{
                         {
                             AttachMode: diskAttachMode,
                             Type: &compute.AttachedDiskSpec_ExistingDisk{
                                 ExistingDisk: &compute.ExistingDisk{
                                     Id: additionalDiskID,
                                 },
                             },
                             DeviceId: "device-0",
                         },
                     },
                     Filesystems: []*compute.AttachedFilesystemSpec{
                         {
                             AttachMode: filesystemAttachMode,
                             MountTag:   "mount-tag-1",
                             Type: fsType,
                         },
                     },
                     NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                         {
                             Name:           "ni",
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
     if _, err = instanceOperation.Wait(ctx); err != nil {
         return err
     }
     vmID := instanceOperation.ResourceID()
     ```

   * **Attach disks to an existing VM**:

     ```go theme={null}
     instance, err := sdk.Services().Compute().V1().
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
     instance.Spec.SecondaryDisks = []*compute.AttachedDiskSpec{
         {
             AttachMode: compute.AttachedDiskSpec_READ_WRITE,
             Type: &compute.AttachedDiskSpec_ExistingDisk{
                 ExistingDisk: &compute.ExistingDisk{
                     Id: additionalDiskID,
                 },
             },
             DeviceId: "device-0",
         },
     }
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

     To get the ID of an existing VM:

     ```go theme={null}
     instances, err := sdk.Services().Compute().V1().
         Instance().List(ctx, &compute.ListInstancesRequest{})
     if err != nil {
         return err
     }
     fmt.Println(instances)
     ```

     When updating an existing VM, preserve the disks or shared filesystems that must stay attached. The examples replace the corresponding attachment list in the VM specification.

   * To **attach shared filesystems to an existing VM**, stop the VM first:

     ```go theme={null}
     instanceOperation, err = sdk.Services().Compute().V1().
         Instance().Stop(
             ctx,
             &compute.StopInstanceRequest{
                 Id: "<VM_ID>",
             },
         )
     if err != nil {
         return err
     }
     if _, err = instanceOperation.Wait(ctx); err != nil {
         return err
     }
     ```

     Then update the VM:

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
     instance.Spec.Filesystems = []*compute.AttachedFilesystemSpec{
         {
             AttachMode: compute.AttachedFilesystemSpec_READ_WRITE,
             MountTag:   "mount-tag-1",
             Type: &compute.AttachedFilesystemSpec_ExistingFilesystem{
                 ExistingFilesystem: &compute.ExistingFilesystem{
                     Id: filesystemID,
                 },
             },
         },
     }
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

     When updating an existing VM, preserve the disks or shared filesystems that must stay attached. The examples replace the corresponding attachment list in the VM specification.

     After the update, start the VM:

     ```go theme={null}
     instanceOperation, err = sdk.Services().Compute().V1().
         Instance().Start(
             ctx,
             &compute.StartInstanceRequest{
                 Id: "<VM_ID>",
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

1. [Create the volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Set the attachment parameters in the code examples:

   In the code examples, set the attachment parameters:

   * For disks, set the attach mode, existing disk ID and device ID.
   * For shared filesystems, set the attach mode, existing filesystem ID and mount tag.

   Create your own mount tag, such as `my-filesystem`. Make sure that it is unique within a VM. If you do not specify the tag, it takes the `filesystem-N` default value where `N` is an integer. For example, `filesystem-0`.

3. Create or update a VM with the volumes configured:

   * **Create a VM**:

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     create_instance_operation = await instance_service.create(
         CreateInstanceRequest(
             metadata=ResourceMetadata(
                 name="vm-name",
             ),
             spec=InstanceSpec(
                 stopped=False,
                 resources=ResourcesSpec(
                     platform="cpu-e2",
                     preset="2vcpu-8gb",
                 ),
                 boot_disk=AttachedDiskSpec(
                     attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                     existing_disk=ExistingDisk(id=boot_disk_id_1),
                 ),
                 secondary_disks=[
                     AttachedDiskSpec(
                         attach_mode=(
                             AttachedDiskSpec.AttachMode.READ_WRITE
                         ),
                         existing_disk=ExistingDisk(id=additional_disk_id),
                         device_id="device-0",
                     ),
                 ],
                 filesystems=[
                     AttachedFilesystemSpec(
                         attach_mode=(
                             AttachedFilesystemSpec.AttachMode.READ_WRITE
                         ),
                         existing_filesystem=ExistingFilesystem(
                             id=filesystem_id,
                         ),
                         mount_tag="mount-tag-1",
                     ),
                 ],
                 network_interfaces=[
                     NetworkInterfaceSpec(
                         name="ni",
                         subnet_id=subnet_id,
                         ip_address=IPAddress(),
                         public_ip_address=PublicIPAddress(),
                     ),
                 ],
             ),
         ),
     )
     await create_instance_operation.wait()
     vm_id = create_instance_operation.resource_id
     ```

   * **Attach disks to an existing VM**:

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     instance = await instance_service.get(
         GetInstanceRequest(id="<VM_ID>"),
     )
     if instance.spec is None:
         raise ValueError("instance spec is missing")
     instance.spec.secondary_disks = [
         AttachedDiskSpec(
             attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
             existing_disk=ExistingDisk(id=additional_disk_id),
             device_id="device-0",
         ),
     ]
     attach_disk_operation = await instance_service.update(
         UpdateInstanceRequest(
             metadata=instance.metadata,
             spec=instance.spec,
         ),
     )
     await attach_disk_operation.wait()
     ```

     To get the ID of an existing VM:

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     instances = await instance_service.list(
         ListInstancesRequest(),
     )
     print(instances)
     ```

     When updating an existing VM, preserve the disks or shared filesystems that must stay attached. The examples replace the corresponding attachment list in the VM specification.

   * To **attach shared filesystems to an existing VM**, stop the VM first:

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     stop_instance_operation = await instance_service.stop(
         StopInstanceRequest(id="<VM_ID>"),
     )
     await stop_instance_operation.wait()
     ```

     Then update the VM:

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     instance = await instance_service.get(
         GetInstanceRequest(id="<VM_ID>"),
     )
     if instance.spec is None:
         raise ValueError("instance spec is missing")
     instance.spec.filesystems = [
         AttachedFilesystemSpec(
             attach_mode=AttachedFilesystemSpec.AttachMode.READ_WRITE,
             existing_filesystem=ExistingFilesystem(id=filesystem_id),
             mount_tag="mount-tag-1",
         ),
     ]
     attach_filesystem_operation = await instance_service.update(
         UpdateInstanceRequest(
             metadata=instance.metadata,
             spec=instance.spec,
         ),
     )
     await attach_filesystem_operation.wait()
     ```

     When updating an existing VM, preserve the disks or shared filesystems that must stay attached. The examples replace the corresponding attachment list in the VM specification.

     After the update, start the VM:

     ```python theme={null}
     instance_service = InstanceServiceClient(sdk)
     start_instance_operation = await instance_service.start(
         StartInstanceRequest(id="<VM_ID>"),
     )
     await start_instance_operation.wait()
     ```

**JavaScript SDK**

1. [Create the volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Set the attachment parameters in the code examples:

   In the code examples, set the attachment parameters:

   * For disks, set the attach mode, existing disk ID and device ID.
   * For shared filesystems, set the attach mode, existing filesystem ID and mount tag.

   Create your own mount tag, such as `my-filesystem`. Make sure that it is unique within a VM. If you do not specify the tag, it takes the `filesystem-N` default value where `N` is an integer. For example, `filesystem-0`.

3. Create or update a VM with the volumes configured:

   * **Create a VM**:

     ```ts theme={null}
     const createInstanceService = new InstanceService(sdk);
     const createInstanceOperation = await createInstanceService.create(
       CreateInstanceRequest.create({
         metadata: ResourceMetadata.create({
           name: "vm-name",
         }),
         spec: InstanceSpec.create({
           stopped: false,
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
                 id: bootDiskId1,
               }),
             },
           }),
           secondaryDisks: [
             AttachedDiskSpec.create({
               attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
               deviceId: "device-0",
               type: {
                 $case: "existingDisk",
                 existingDisk: ExistingDisk.create({
                   id: additionalDiskId,
                 }),
               },
             }),
           ],
           filesystems: [
             AttachedFilesystemSpec.create({
               attachMode: AttachedFilesystemSpec_AttachMode.READ_WRITE,
               mountTag: "mount-tag-1",
               type: {
                 $case: "existingFilesystem",
                 existingFilesystem: ExistingFilesystem.create({
                   id: filesystemId,
                 }),
               },
             }),
           ],
           networkInterfaces: [
             NetworkInterfaceSpec.create({
               name: "ni",
               subnetId: subnetId,
               ipAddress: IPAddress.create({}),
               publicIpAddress: PublicIPAddress.create({}),
             }),
           ],
         }),
       }),
     ).result;
     await createInstanceOperation.wait();
     const vmId = createInstanceOperation.resourceId();
     ```

   * **Attach disks to an existing VM**:

     ```ts theme={null}
     const attachDiskService = new InstanceService(sdk);
     const instanceForDiskAttach = await attachDiskService.get(
       GetInstanceRequest.create({
         id: "<VM_ID>",
       }),
     );
     if (!instanceForDiskAttach.spec) {
       throw new Error("instance spec is missing");
     }
     instanceForDiskAttach.spec.secondaryDisks = [
       AttachedDiskSpec.create({
         attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
         deviceId: "device-0",
         type: {
           $case: "existingDisk",
           existingDisk: ExistingDisk.create({
             id: additionalDiskId,
           }),
         },
       }),
     ];
     const attachDiskOperation = await attachDiskService.update(
       UpdateInstanceRequest.create({
         metadata: instanceForDiskAttach.metadata,
         spec: instanceForDiskAttach.spec,
       }),
     ).result;
     await attachDiskOperation.wait();
     ```

     To get the ID of an existing VM:

     ```ts theme={null}
     const listInstanceService = new InstanceService(sdk);
     const instanceList = await listInstanceService.list(
       ListInstancesRequest.create({}),
     );
     console.log(instanceList);
     ```

     When updating an existing VM, preserve the disks or shared filesystems that must stay attached. The examples replace the corresponding attachment list in the VM specification.

   * To **attach shared filesystems to an existing VM**, stop the VM first:

     ```ts theme={null}
     const stopInstanceService = new InstanceService(sdk);
     const stopInstanceOperation = await stopInstanceService.stop(
       StopInstanceRequest.create({
         id: "<VM_ID>",
       }),
     ).result;
     await stopInstanceOperation.wait();
     ```

     Then update the VM:

     ```ts theme={null}
     const attachFilesystemService = new InstanceService(sdk);
     const instanceForFilesystemAttach = await attachFilesystemService.get(
       GetInstanceRequest.create({
         id: "<VM_ID>",
       }),
     );
     if (!instanceForFilesystemAttach.spec) {
       throw new Error("instance spec is missing");
     }
     instanceForFilesystemAttach.spec.filesystems = [
       AttachedFilesystemSpec.create({
         attachMode: AttachedFilesystemSpec_AttachMode.READ_WRITE,
         mountTag: "mount-tag-1",
         type: {
           $case: "existingFilesystem",
           existingFilesystem: ExistingFilesystem.create({
             id: filesystemId,
           }),
         },
       }),
     ];
     const attachFilesystemOperation = await attachFilesystemService.update(
       UpdateInstanceRequest.create({
         metadata: instanceForFilesystemAttach.metadata,
         spec: instanceForFilesystemAttach.spec,
       }),
     ).result;
     await attachFilesystemOperation.wait();
     ```

     When updating an existing VM, preserve the disks or shared filesystems that must stay attached. The examples replace the corresponding attachment list in the VM specification.

     After the update, start the VM:

     ```ts theme={null}
     const startInstanceService = new InstanceService(sdk);
     const startInstanceOperation = await startInstanceService.start(
       StartInstanceRequest.create({
         id: "<VM_ID>",
       }),
     ).result;
     await startInstanceOperation.wait();
     ```

You can also attach a VM-managed boot disk to another VM, so you can investigate and troubleshoot this boot disk. For more information, see [How to inspect a VM and attach its boot disk to another VM](https://docs.nebius.com/compute/virtual-machines/inspect-boot-disk.md).

## How to mount volumes to VMs

### Disks

1. [Attach the disk to a VM](#how-to-attach-volumes-to-vms).

2. If you have not saved the disk's device ID, for example, when adding it to the VM, get it from the information about the VM:

   **CLI**

   ```bash theme={null}
   nebius compute instance get --id <VM_ID> --format json \
     | jq -r --arg disk_id <disk_ID> \
       '.spec.secondary_disks[]
       | select(.existing_disk.id == $disk_id)
       | .device_id'
   ```

   To get the VM ID, run `nebius compute instance list`. To get the disk ID, run `nebius compute disk list`.

   **Go SDK**

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
   deviceID := ""
   for _, secondaryDisk := range instance.GetSpec().GetSecondaryDisks() {
       existingDisk := secondaryDisk.GetExistingDisk()
       if existingDisk != nil && existingDisk.GetId() == "<disk_ID>" {
           deviceID = secondaryDisk.GetDeviceId()
           break
       }
   }
   if deviceID == "" {
       return errors.New("device ID is missing")
   }
   fmt.Println(deviceID)
   ```

   To get the VM ID, run:

   ```go theme={null}
   instances, err := sdk.Services().Compute().V1().
       Instance().List(ctx, &compute.ListInstancesRequest{})
   if err != nil {
       return err
   }
   fmt.Println(instances)
   ```

   For the disk ID, use the ID of the disk that you attached.

   **Python SDK**

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if instance.spec is None:
       raise ValueError("instance spec is missing")
   device_id = next(
       secondary_disk.device_id
       for secondary_disk in instance.spec.secondary_disks
       if secondary_disk.existing_disk is not None
       and secondary_disk.existing_disk.id == "<disk_ID>"
   )
   print(device_id)
   ```

   To get the VM ID, run:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instances = await instance_service.list(
       ListInstancesRequest(),
   )
   print(instances)
   ```

   For the disk ID, use the ID of the disk that you attached.

   **JavaScript SDK**

   ```ts theme={null}
   const getDeviceIdService = new InstanceService(sdk);
   const instanceForDeviceLookup = await getDeviceIdService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   const deviceId = instanceForDeviceLookup.spec?.secondaryDisks.find(
     (secondaryDisk) =>
       secondaryDisk.type?.$case === "existingDisk" &&
       secondaryDisk.type.existingDisk.id === "<disk_ID>",
   )?.deviceId;
   if (!deviceId) {
     throw new Error("device ID is missing");
   }
   console.log(deviceId);
   ```

   To get the VM ID, run:

   ```ts theme={null}
   const listInstanceService = new InstanceService(sdk);
   const instanceList = await listInstanceService.list(
     ListInstancesRequest.create({}),
   );
   console.log(instanceList);
   ```

   For the disk ID, use the ID of the disk that you attached.

3. [Connect to the VM over SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

4. Switch to the `root` user:

   ```bash theme={null}
   sudo su -
   ```

5. Partition the device. For example, you can use `cfdisk`. In the example below, we assume that you have named the device `disk-0`; for disks, all device IDs are prefixed with `virtio-`:

   1. Run `cfdisk`:

      ```bash theme={null}
      cfdisk /dev/disk/by-id/virtio-disk-0
      ```

      > [!NOTE]
      >
      > Referring to a device by its name, e.g., `/dev/vdb`, does not guarantee it will function properly. Use the device ID instead, e.g., `/dev/disk/by-id/virtio-disk-0`.

   2. Under **Select label type**, select **gpt** and press **Enter**.

   3. Select **New** (partition) and press **Enter**.

   4. Enter the partition size and press **Enter**. This will create a `/dev/disk/by-id/virtio-disk-0-part1` partition.

   5. Select **Write** (the partition table to the device) and press **Enter**, then type `yes` and press **Enter**.

   6. Select **Quit** and press **Enter**.

6. Format the partition:

   ```bash theme={null}
   mkfs.ext4 /dev/disk/by-id/virtio-disk-0-part1
   ```

7. Mount the partition and configure permissions for it by using `chmod`. In the example below, the partition is mounted at `/mnt/disk-0`, and all VM users are granted write access to it:

   ```bash theme={null}
   mkdir /mnt/disk-0
   mount /dev/disk/by-id/virtio-disk-0-part1 /mnt/disk-0
   chmod a+w /mnt/disk-0
   ```

8. If you want the partition to be mounted automatically after every VM restart, add it to `/etc/fstab` by its UUID:

   ```bash theme={null}
   echo "UUID=$(blkid -s UUID -o value /dev/disk/by-id/virtio-disk-0-part1) /mnt/disk-0 ext4 defaults,nofail 0 2" >> /etc/fstab
   ```

   > [!WARNING]
   >
   > Do not omit `nofail`. If it is not specified and the VM cannot find the partition on restart (for example, the disk has been repartitioned), the VM will not boot.

9. Exit the `root` user shell:

   ```bash theme={null}
   exit
   ```

### Shared filesystems

If you create a VM in the web console, you can automatically attach and mount a shared filesystem to the VM by using the **Auto mount** option. If you do not use it, mount the filesystem manually. To do this:

1. [Attach the shared filesystem to a VM](#how-to-attach-volumes-to-vms).

2. If you have not saved the filesystem's mount tag, for example, when adding it to the VM, get the mount tag from the information about the VM:

   **CLI**

   ```bash theme={null}
   nebius compute instance get --id <VM_ID> --format json \
     | jq -r --arg fs_id <filesystem_ID> \
       '.spec.filesystems[]
       | select(.existing_filesystem.id == $fs_id)
       | .mount_tag'
   ```

   To get the VM ID, run `nebius compute instance list`. To get the filesystem ID, run `nebius compute filesystem list`.

   **Go SDK**

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
   mountTag := ""
   for _, filesystem := range instance.GetSpec().GetFilesystems() {
       existingFilesystem := filesystem.GetExistingFilesystem()
       if existingFilesystem != nil &&
           existingFilesystem.GetId() == "<filesystem_ID>" {
           mountTag = filesystem.GetMountTag()
           break
       }
   }
   if mountTag == "" {
       return errors.New("mount tag is missing")
   }
   fmt.Println(mountTag)
   ```

   To get the VM ID, run:

   ```go theme={null}
   instances, err := sdk.Services().Compute().V1().
       Instance().List(ctx, &compute.ListInstancesRequest{})
   if err != nil {
       return err
   }
   fmt.Println(instances)
   ```

   For the filesystem ID, use the ID of the filesystem that you attached.

   **Python SDK**

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if instance.spec is None:
       raise ValueError("instance spec is missing")
   mount_tag = next(
       filesystem.mount_tag
       for filesystem in instance.spec.filesystems
       if filesystem.existing_filesystem is not None
       and filesystem.existing_filesystem.id == "<filesystem_ID>"
   )
   print(mount_tag)
   ```

   To get the VM ID, run:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instances = await instance_service.list(
       ListInstancesRequest(),
   )
   print(instances)
   ```

   For the filesystem ID, use the ID of the filesystem that you attached.

   **JavaScript SDK**

   ```ts theme={null}
   const getMountTagService = new InstanceService(sdk);
   const instanceForMountLookup = await getMountTagService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   const mountTag = instanceForMountLookup.spec?.filesystems.find(
     (filesystem) =>
       filesystem.type?.$case === "existingFilesystem" &&
       filesystem.type.existingFilesystem.id === "<filesystem_ID>",
   )?.mountTag;
   if (!mountTag) {
     throw new Error("mount tag is missing");
   }
   console.log(mountTag);
   ```

   To get the VM ID, run:

   ```ts theme={null}
   const listInstanceService = new InstanceService(sdk);
   const instanceList = await listInstanceService.list(
     ListInstancesRequest.create({}),
   );
   console.log(instanceList);
   ```

   For the filesystem ID, use the ID of the filesystem that you attached.

3. [Connect to the VM over SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

4. Switch to the `root` user:

   ```bash theme={null}
   sudo su -
   ```

5. Mount the filesystem as a `virtiofs` device and configure permissions for it by using `chmod`. In the example below, a filesystem has the mount tag `filesystem-0` and is mounted at `/mnt/fs`. All VM users are granted write access to it:

   ```bash theme={null}
   mkdir /mnt/fs
   mount -t virtiofs filesystem-0 /mnt/fs
   chmod a+w /mnt/fs
   ```

6. If you want the filesystem to be mounted automatically after every VM restart, add it to `/etc/fstab`:

   ```bash theme={null}
   echo "filesystem-0 /mnt/fs virtiofs rw,nofail 0 0" >> /etc/fstab
   ```

   > [!WARNING]
   >
   > Do not omit `nofail`. If it is not specified and the VM cannot find the filesystem on restart (for example, it has been deleted), the VM will not boot.

7. Exit the `root` user shell:

   ```bash theme={null}
   exit
   ```

## See also

* [How to detach additional volumes from virtual machines](https://docs.nebius.com/compute/storage/detach-volume.md)
* [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md)
* [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md)
* [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md)
