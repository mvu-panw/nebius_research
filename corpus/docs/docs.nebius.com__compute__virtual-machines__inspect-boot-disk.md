# How to inspect a VM and attach its boot disk to another VM

Source: https://docs.nebius.com/compute/virtual-machines/inspect-boot-disk

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to inspect a VM and attach its boot disk to another VM

If a virtual machine (VM) does not start or you cannot connect to it, you can attach its boot disk to another VM as a secondary disk and inspect the boot disk from there. To do this:

1. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md) for debugging in the same project as the boot disk you want to inspect. [Set up the SSH connection](https://docs.nebius.com/compute/virtual-machines/connect.md#set-up-the-vm) to your new VM.

2. [Stop the original VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) that you want to inspect. Otherwise, you can't attach its boot disk to another VM.

3. Get the ID of the original VM's boot disk:

   **CLI**

   ```bash theme={null}
   nebius compute instance get --id <original_VM_ID> \
     --format jsonpath='.spec.boot_disk.existing_disk.id'
   ```

   **Go SDK**

   ```go theme={null}
   originalInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<original_VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if originalInstance.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   bootDisk := originalInstance.GetSpec().GetBootDisk()
   if bootDisk == nil || bootDisk.GetExistingDisk() == nil {
       return errors.New("boot disk is missing")
   }
   fmt.Println(bootDisk.GetExistingDisk().GetId())
   ```

   Save the boot disk ID from the output as `originalBootDiskID`.

   **Python SDK**

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   original_instance = await instance_service.get(
       GetInstanceRequest(id="<original_VM_ID>"),
   )
   if original_instance.spec is None:
       raise ValueError("instance spec is missing")
   boot_disk = original_instance.spec.boot_disk
   if boot_disk is None or boot_disk.existing_disk is None:
       raise ValueError("boot disk is missing")
   print(boot_disk.existing_disk.id)
   ```

   Save the boot disk ID from the output as `original_boot_disk_id`.

   **JavaScript SDK**

   ```ts theme={null}
   const getOriginalInstanceService = new InstanceService(sdk);
   const originalInstance = await getOriginalInstanceService.get(
     GetInstanceRequest.create({
       id: "<original_VM_ID>",
     }),
   );
   const originalBootDisk = originalInstance.spec?.bootDisk;
   const bootDiskId = originalBootDisk?.type?.$case === "existingDisk"
     ? originalBootDisk.type.existingDisk.id
     : undefined;
   if (!bootDiskId) {
     throw new Error("boot disk is missing");
   }
   console.log(bootDiskId);
   ```

   Save the boot disk ID from the output as `originalBootDiskId`.

4. Attach the boot disk to the debug VM as a secondary disk:

   **CLI**

   ```bash theme={null}
   nebius compute instance update <debug_VM_ID> \
     --patch \
     --secondary-disks '[{"existing_disk": {"id": "<boot_disk_ID>"}, "attach_mode": "READ_WRITE", "device_id": "original-boot-disk"}]'
   ```

   **Go SDK**

   In the code, specify the debug VM ID and use the `originalBootDiskID` value from the previous step:

   ```go theme={null}
   instance, err = sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<debug_VM_ID>",
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
                   Id: originalBootDiskID,
               },
           },
           DeviceId: "original-boot-disk",
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

   **Python SDK**

   In the code, specify the debug VM ID and use the `original_boot_disk_id` value from the previous step:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   instance = await instance_service.get(
       GetInstanceRequest(id="<debug_VM_ID>"),
   )
   if instance.spec is None:
       raise ValueError("instance spec is missing")
   instance.spec.secondary_disks = [
       AttachedDiskSpec(
           attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
           existing_disk=ExistingDisk(id=original_boot_disk_id),
           device_id="original-boot-disk",
       ),
   ]
   attach_boot_disk_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=instance.metadata,
           spec=instance.spec,
       ),
   )
   await attach_boot_disk_operation.wait()
   ```

   **JavaScript SDK**

   In the code, specify the debug VM ID and use the `originalBootDiskId` value from the previous step:

   ```ts theme={null}
   const attachBootDiskService = new InstanceService(sdk);
   const instanceForBootDiskAttach =
     await attachBootDiskService.get(
       GetInstanceRequest.create({
         id: "<debug_VM_ID>",
       }),
     );
   if (!instanceForBootDiskAttach.spec) {
     throw new Error("instance spec is missing");
   }
   instanceForBootDiskAttach.spec.secondaryDisks = [
     AttachedDiskSpec.create({
       attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
       deviceId: "original-boot-disk",
       type: {
         $case: "existingDisk",
         existingDisk: ExistingDisk.create({
           id: originalBootDiskId,
         }),
       },
     }),
   ];
   const attachBootDiskOperation =
     await attachBootDiskService.update(
       UpdateInstanceRequest.create({
         metadata: instanceForBootDiskAttach.metadata,
         spec: instanceForBootDiskAttach.spec,
       }),
     ).result;
   await attachBootDiskOperation.wait();
   ```

5. [Connect to the debug VM by using SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

6. List the partitions and filesystems on the boot disk:

   ```bash theme={null}
   lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS /dev/disk/by-id/virtio-original-boot-disk
   ```

7. Mount the filesystem you need to inspect. The root filesystem is on the largest ext4 (or xfs) partition — usually `-part1`. To mount it:

   ```bash theme={null}
   sudo mkdir -p /mnt/original-boot-disk
   sudo mount -o ro /dev/disk/by-id/virtio-original-boot-disk-part1 /mnt/original-boot-disk
   ```

   For safety, use the `-o ro` parameter to mount the filesystem in read-only mode. This prevents any accidental changes to the boot disk you are inspecting.

8. (Optional) If you need to repair the filesystem by writing to it, remount it in read-write mode:

   ```bash theme={null}
   sudo mount -o remount,rw /mnt/original-boot-disk
   ```

9. When done inspecting, unmount the filesystem:

   ```bash theme={null}
   sudo umount /mnt/original-boot-disk
   ```

10. [Detach](https://docs.nebius.com/compute/storage/detach-volume.md#remove-the-volume-from-the-vm's-specification) the boot disk of the original VM from the debug VM.

11. After the disk is detached, [start the original VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually). You can't start the VM if its boot disk is attached to another running VM.

## See also

* [How to collect diagnostic logs from Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/logs.md)
* [Viewing serial logs of virtual machines](https://docs.nebius.com/compute/monitoring/serial-logs.md)
* [How to detach additional volumes from virtual machines](https://docs.nebius.com/compute/storage/detach-volume.md)
* [Attaching and mounting Compute volumes to VMs](https://docs.nebius.com/compute/storage/use.md)
