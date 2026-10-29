# Exporting data from Compute disks and shared filesystems

Source: https://docs.nebius.com/compute/storage/export

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Exporting data from Compute disks and shared filesystems

You can export data that you store on [Compute volumes](https://docs.nebius.com/compute/storage/types.md) (boot disks, additional disks and shared filesystems) to local or virtual machines:

1. Check whether the disk or filesystem is used on any VMs:

   **Web console**

   1. In the [web console](https://console.nebius.com), go to  **Storage** → **Disks** or  **Storage** → **Shared filesystems**.
   2. Click on the volume.
   3. Under **General**, check the **Virtual machine** value. It lists the VMs that use the volume.

   **CLI**

   * For a disk, run `nebius compute disk list` or `nebius compute disk get <disk_ID>`. If the disk is used on a VM, the output contains the VM's ID in the `.status.read_write_attachment` field:

     ```yaml theme={null}
     status:
       read_write_attachment: computeinstance-e00***
     ```

     For more details about the commands, see the references for [nebius compute disk list](https://docs.nebius.com/cli/reference/compute/disk/list.md) and [nebius compute disk get](https://docs.nebius.com/cli/reference/compute/disk/get.md).

   * For a filesystem, run `nebius compute filesystem list` or `nebius compute filesystem get <filesystem_ID>`. If the filesystem is used on any VMs, the output lists their IDs in the `.status.read_write_attachments` field:

     ```yaml theme={null}
     status:
       read_write_attachments:
         - computeinstance-e00***
         - computeinstance-e00***
     ```

     For more details about the commands, see the references for [nebius compute filesystem list](https://docs.nebius.com/cli/reference/compute/filesystem/list.md) and [nebius compute filesystem get](https://docs.nebius.com/cli/reference/compute/filesystem/get.md).

   **Go SDK**

   * For a disk, get or list disks and check `disk.GetStatus().GetReadWriteAttachment()`. If the disk is used on a VM, the response contains this VM's ID.
   * For a filesystem, get or list filesystems and check `filesystem.GetStatus().GetReadWriteAttachments()`. If the filesystem is used on any VMs, the response contains a list of their IDs.

   **Python SDK**

   * For a disk, get or list disks and check `disk.status.read_write_attachment`. If the disk is used on a VM, the response contains this VM's ID.
   * For a filesystem, get or list filesystems and check `filesystem.status.read_write_attachments`. If the filesystem is used on any VMs, the response contains a list of their IDs.

   **JavaScript SDK**

   * For a disk, get or list disks and check `disk.status?.readWriteAttachment`. If the disk is used on a VM, the response contains this VM's ID.
   * For a filesystem, get or list filesystems and check `filesystem.status?.readWriteAttachments`. If the filesystem is used on any VMs, the response contains a list of their IDs.

2. If the disk or filesystem is not used on any VM, [attach and mount it to a VM](https://docs.nebius.com/compute/storage/use.md).

3. Check that you can [connect to the VM over SSH](https://docs.nebius.com/compute/virtual-machines/connect.md).

   > **What to do if I cannot connect to the VM**
   >
   > * If the VM does not have a public IP address, you have the following options:
   >
   >   * Connect to the VM's private address from another VM in the same [network](https://docs.nebius.com/vpc/overview.md#network).
   >   * Run `nebius compute instance update` with the `--network-interfaces` parameter to add a public address to the VM. For the command reference, see [nebius compute instance update](https://docs.nebius.com/cli/reference/compute/instance/update.md).
   >   * Create another VM with a public address and add the volume to it. For details and examples, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).
   >
   >     > [!WARNING]
   >     >
   >     > A disk can be attached to only one running VM at a time; shared filesystems can be used by several VMs at once. To add a disk to a new VM, [detach the disk](https://docs.nebius.com/compute/storage/detach-volume.md) from the original VM if it's a secondary disk, or [attach it to another VM for troubleshooting](https://docs.nebius.com/compute/virtual-machines/inspect-boot-disk.md) if it's the boot disk.
   >
   > * If you have not created this VM, ask its owner to perform the following steps themselves or add you to the VM as a user.
   >
   > * For other connection issues, [contact support](https://console.nebius.com/support/create-ticket).

4. On your local machine, run a tool for copying files, for example, `rsync` or `scp`:

   **rsync**

   ```bash theme={null}
   rsync <username>@<public_IP_address>:</path/to/file(s)/on/VM> </path/to/destination/on/local/machine>
   ```

   > For example, if a VM has the public IP address `195.242.11.11` and you work with it as `alice`, run the following command to recursively copy the contents of your home directory:
   >
   > ```bash theme={null}
   > rsync -r alice@195.242.11.11:/home/alice ~/vm-home
   > ```

   For more `rsync` details and parameters, run `man rsync`.

   **scp**

   ```bash theme={null}
   scp <username>@<public_IP_address>:</path/to/file(s)/on/VM> </path/to/destination/on/local/machine>
   ```

   > For example, if a VM has the public IP address `195.242.11.11` and you work with it as `alice`, run the following command to recursively copy the contents of your home directory:
   >
   > ```bash theme={null}
   > scp -r alice@195.242.11.11:/home/alice ~/vm-home
   > ```

   For more `scp` details and parameters, see its [manpage](https://man.openbsd.org/scp.1) or run `man scp`.
