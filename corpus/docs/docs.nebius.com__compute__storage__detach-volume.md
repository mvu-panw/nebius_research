# How to detach additional volumes from virtual machines

Source: https://docs.nebius.com/compute/storage/detach-volume

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to detach additional volumes from virtual machines

You can detach a [secondary disk](https://docs.nebius.com/compute/storage/types.md#disks) or a [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) from a VM. You cannot detach a boot disk.

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

## Steps

### Get the disk device ID or the filesystem mount tag

**Web console**

1. In the sidebar, go to  **Storage** → **Disks** or  **Storage** → **Shared filesystems**.
2. Copy the device ID from the list of disks or the mount tag from the list of filesystems.

**CLI**

Get the VM's specification:

```bash theme={null}
nebius compute instance get <VM_ID>
```

Alternatively, list all VMs:

```bash theme={null}
nebius compute instance list
```

In the output, you can find device IDs of disks and mount tags of filesystems in `.spec.secondary_disks[].device_id` and `.spec.filesystems[].mount_tag`, respectively:

```yaml theme={null}
spec:
  secondary_disks:
    - attach_mode: READ_WRITE
      existing_disk:
        id: computedisk-***
      device_id: newdisk
  filesystems:
    - attach_mode: READ_WRITE
      existing_filesystem:
        id: computefilesystem-***
      mount_tag: shared-fs
```

**Go SDK**

Get the VM's specification:

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
fmt.Println(instance)
```

Alternatively, list all VMs:

```go theme={null}
instances, err := sdk.Services().Compute().V1().
    Instance().List(ctx, &compute.ListInstancesRequest{})
if err != nil {
    return err
}
fmt.Println(instances)
```

In the output, you can find device IDs of disks and mount tags of filesystems in `.spec.secondary_disks[].device_id` and `.spec.filesystems[].mount_tag`, respectively:

```yaml theme={null}
spec:
  secondary_disks:
    - attach_mode: READ_WRITE
      existing_disk:
        id: computedisk-***
      device_id: newdisk
  filesystems:
    - attach_mode: READ_WRITE
      existing_filesystem:
        id: computefilesystem-***
      mount_tag: shared-fs
```

**Python SDK**

Get the VM's specification:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
instance = await instance_service.get(
    GetInstanceRequest(id="<VM_ID>"),
)
print(instance)
```

Alternatively, list all VMs:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
instances = await instance_service.list(
    ListInstancesRequest(),
)
print(instances)
```

In the output, you can find device IDs of disks and mount tags of filesystems in `.spec.secondary_disks[].device_id` and `.spec.filesystems[].mount_tag`, respectively:

```yaml theme={null}
spec:
  secondary_disks:
    - attach_mode: READ_WRITE
      existing_disk:
        id: computedisk-***
      device_id: newdisk
  filesystems:
    - attach_mode: READ_WRITE
      existing_filesystem:
        id: computefilesystem-***
      mount_tag: shared-fs
```

**JavaScript SDK**

Get the VM's specification:

```ts theme={null}
const getInstanceService = new InstanceService(sdk);
const instanceDetails = await getInstanceService.get(
  GetInstanceRequest.create({
    id: "<VM_ID>",
  }),
);
console.log(instanceDetails);
```

Alternatively, list all VMs:

```ts theme={null}
const listInstanceService = new InstanceService(sdk);
const instanceList = await listInstanceService.list(
  ListInstancesRequest.create({}),
);
console.log(instanceList);
```

In the output, you can find device IDs of disks and mount tags of filesystems in `.spec.secondary_disks[].device_id` and `.spec.filesystems[].mount_tag`, respectively:

```yaml theme={null}
spec:
  secondary_disks:
    - attach_mode: READ_WRITE
      existing_disk:
        id: computedisk-***
      device_id: newdisk
  filesystems:
    - attach_mode: READ_WRITE
      existing_filesystem:
        id: computefilesystem-***
      mount_tag: shared-fs
```

### Make sure that the VM does not mount the volume when the VM restarts

1. [Connect to the VM over SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

2. Switch to the `root` user:

   ```bash theme={null}
   sudo su -
   ```

3. If you want to detach a secondary disk, get its UUID:

   ```bash theme={null}
   blkid /dev/disk/by-id/virtio-disk-0-part1 -o export | grep "^UUID"
   ```

   In this example, we assume that you have named the device `disk-0`; for disks, all device IDs are prefixed with `virtio-`.

4. Open `/etc/fstab` with your preferred text editor, for example, `nano /etc/fstab`, and delete the lines that refer to the volumes:

   * The line for a disk should start with its UUID:

     ```text theme={null}
     UUID=<disk_UUID> /mnt/disk-0 ext4 defaults,nofail 0 2
     ```

   * The line for a filesystem should start with the filesystem's mount tag from the VM specification:

     ```text theme={null}
     filesystem-0 /mnt/fs virtiofs rw,nofail 0 0
     ```

     In this example, the filesystem has the mount tag `filesystem-0` and is mounted at `/mnt/fs`.

5. Disconnect from the VM.

### Remove the volume from the VM specification

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. On the **Standalone VMs** tab, open the page of the required VM.

3. Click  **Stop VM** and then confirm it.

   > [!NOTE]
   >
   > You can detach a disk from a running VM, but this can cause data loss or corruption.

4. After the VM's status becomes `Stopped`, switch to the **Disks** or **Filesystems** tab.

5. Next to the disk or filesystem, click  → **Detach**.

6. After the volume is detached, click  **Start VM** and then confirm it.

**CLI**

1. Stop the VM:

   ```bash theme={null}
   nebius compute instance stop --id <VM_ID>
   ```

   > [!NOTE]
   >
   > You can detach a disk from a running VM, but this can cause data loss or corruption.

2. Start editing the VM specification:

   ```bash theme={null}
   nebius compute instance edit <VM_ID>
   ```

3. In the text editor that opens, remove the disk or filesystem from the `.spec.secondary_disks` or `.spec.filesystems` list, respectively. If, after that, a list becomes empty, remove it entirely. For example:

   ```diff theme={null}
     spec:
       boot_disk:
         attach_mode: READ_WRITE
         device_id: ""
         existing_disk:
           id: computedisk-***
   -   secondary_disks:
   -     - attach_mode: READ_WRITE
   -       existing_disk:
   -         id: computedisk-***
   -       device_id: newdisk
       gpu_cluster:
     ...
   ```

4. After making the changes, save the file. The CLI updates the VM automatically.

5. Start the VM:

   ```bash theme={null}
   nebius compute instance start --id <VM_ID>
   ```

**Go SDK**

1. Stop the VM:

   ```go theme={null}
   operation, err := sdk.Services().Compute().V1().
       Instance().Stop(
           ctx,
           &compute.StopInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = operation.Wait(ctx); err != nil {
       return err
   }
   ```

   > [!NOTE]
   >
   > You can detach a disk from a running VM, but this can cause data loss or corruption.

2. Remove the volume from the VM's specification:

   ```go theme={null}
   detachInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if detachInstance.GetSpec() == nil {
       return errors.New("instance spec is missing")
   }
   secondaryDisks := detachInstance.Spec.SecondaryDisks[:0]
   for _, disk := range detachInstance.Spec.SecondaryDisks {
       if disk.GetDeviceId() != "<device_ID>" {
           secondaryDisks = append(secondaryDisks, disk)
       }
   }
   detachInstance.Spec.SecondaryDisks = secondaryDisks
   filesystems := detachInstance.Spec.Filesystems[:0]
   for _, filesystem := range detachInstance.Spec.Filesystems {
       if filesystem.GetMountTag() != "<mount_tag>" {
           filesystems = append(filesystems, filesystem)
       }
   }
   detachInstance.Spec.Filesystems = filesystems
   detachOperation, err := sdk.Services().Compute().V1().
       Instance().Update(
           ctx,
           &compute.UpdateInstanceRequest{
               Metadata: detachInstance.Metadata,
               Spec:     detachInstance.Spec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = detachOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   In the code, specify the VM ID, the disk's `deviceId` or the filesystem's `mountTag`.

3. Start the VM:

   ```go theme={null}
   operation, err = sdk.Services().Compute().V1().
       Instance().Start(
           ctx,
           &compute.StartInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = operation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Stop the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   stop_instance_operation = await instance_service.stop(
       StopInstanceRequest(id="<VM_ID>"),
   )
   await stop_instance_operation.wait()
   ```

   > [!NOTE]
   >
   > You can detach a disk from a running VM, but this can cause data loss or corruption.

2. Remove the volume from the VM's specification:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   detach_instance = await instance_service.get(
       GetInstanceRequest(id="<VM_ID>"),
   )
   if detach_instance.spec is None:
       raise ValueError("instance spec is missing")
   detach_instance.spec.secondary_disks = [
       disk
       for disk in detach_instance.spec.secondary_disks
       if disk.device_id != "<device_ID>"
   ]
   detach_instance.spec.filesystems = [
       filesystem
       for filesystem in detach_instance.spec.filesystems
       if filesystem.mount_tag != "<mount_tag>"
   ]
   detach_operation = await instance_service.update(
       UpdateInstanceRequest(
           metadata=detach_instance.metadata,
           spec=detach_instance.spec,
       ),
   )
   await detach_operation.wait()
   ```

   In the code, specify the VM ID, the disk's `device_id` or the filesystem's `mount_tag`.

3. Start the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   start_instance_operation = await instance_service.start(
       StartInstanceRequest(id="<VM_ID>"),
   )
   await start_instance_operation.wait()
   ```

**JavaScript SDK**

1. Stop the VM:

   ```ts theme={null}
   const stopInstanceService = new InstanceService(sdk);
   const stopInstanceOperation = await stopInstanceService.stop(
     StopInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await stopInstanceOperation.wait();
   ```

   > [!NOTE]
   >
   > You can detach a disk from a running VM, but this can cause data loss or corruption.

2. Remove the volume from the VM's specification:

   ```ts theme={null}
   const detachInstanceService = new InstanceService(sdk);
   const detachInstance = await detachInstanceService.get(
     GetInstanceRequest.create({
       id: "<VM_ID>",
     }),
   );
   if (!detachInstance.spec) {
     throw new Error("instance spec is missing");
   }
   detachInstance.spec.secondaryDisks = (
     detachInstance.spec.secondaryDisks ?? []
   ).filter((disk) => disk.deviceId !== "<device_ID>");
   detachInstance.spec.filesystems = (
     detachInstance.spec.filesystems ?? []
   ).filter((filesystem) => filesystem.mountTag !== "<mount_tag>");
   const detachOperation = await detachInstanceService.update(
     UpdateInstanceRequest.create({
       metadata: detachInstance.metadata,
       spec: detachInstance.spec,
     }),
   ).result;
   await detachOperation.wait();
   ```

   In the code, specify the VM ID, the disk's `deviceId` or the filesystem's `mountTag`.

3. Start the VM:

   ```ts theme={null}
   const startInstanceService = new InstanceService(sdk);
   const startInstanceOperation = await startInstanceService.start(
     StartInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await startInstanceOperation.wait();
   ```

You can [attach and mount](https://docs.nebius.com/compute/storage/use.md) different additional volumes to the VM later.
