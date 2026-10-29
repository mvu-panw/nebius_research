# Managing Compute volumes

Source: https://docs.nebius.com/compute/storage/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing Compute volumes

In this article, you will learn how to manage [Compute volumes](https://docs.nebius.com/compute/storage/types.md): Network SSD disks and shared filesystems.

Boot disks are added to virtual machines (VMs) immediately. To use secondary (additional) disks and shared filesystems on VMs after you create the volumes, you need to [attach and mount them to the VMs](https://docs.nebius.com/compute/storage/use.md). You can [detach these volumes](https://docs.nebius.com/compute/storage/detach-volume.md) later, if necessary.

A VM and its volumes must be located in the same project. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

## Prerequisites

If you use the web console, you don't need to complete any prerequisites.

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

## How to create a disk

**Web console**

1. In the sidebar, go to  **Storage** → **Disks**.

2. Click **Create disk**.

3. On the creation page, specify a disk name.

4. In **Disk source type**, select one of the supported sources for the disk:

   * **Blank disk**: Create a regular, blank disk. Suitable for any boot or additional disk.
   * **Public image**: Create a boot disk from one of [public images](https://docs.nebius.com/compute/storage/boot-disk-images.md) that Nebius AI Cloud provides. An image represents an operating system for the disk.
   * **Custom image**: Create a boot disk based on your [custom image](https://docs.nebius.com/compute/storage/custom-disk-images.md) that includes custom software.
   * **Custom image family**: Create a boot disk based on your custom image family. When you create custom images, you can add them to an arbitrary custom family. If an image family contains several images, the latest one is used.
   * **Snapshot**: Create a boot or additional disk based on a [disk snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md).

5. In **Storage configuration**, select the disk type.

6. (Optional) Enable [data encryption](https://docs.nebius.com/security/encryption.md) if you're creating a Network SSD Non-replicated or Network SSD IO M3 disk.

   Encryption is enabled by default for Network SSD disks.

7. Set the disk size and block size.

8. (Optional) Enable **Deletion protection** to prevent this disk from being accidentally deleted.

9. Click **Create disk**.

**CLI**

Run the following command:

```bash theme={null}
nebius compute disk create \
  --name <disk_name> \
  --source-image-family-image-family <image_family> \
  --source-image-family-parent-id <project_ID_for_image_family> \
  --source-image-id <custom_image_ID> \
  --source-snapshot-id <snapshot_ID> \
  --type network_<ssd|ssd_non_replicated|ssd_io_m3> \
  --disk-encryption-type disk_encryption_managed \
  --size-gibibytes <size> \
  --block-size-bytes <block_size> \
  --forbid-deletion
```

For more information, see [Volume parameters](#volume-parameters).

**Terraform**

1. Create the following configuration:

   ```hcl theme={null}
   resource "nebius_compute_v1_disk" "<disk_name>" {
     name             = "<disk_name>"
     parent_id        = "<project_ID>"
     type             = "NETWORK_<SSD|SSD_NON_REPLICATED|SSD_IO_M3>"
     size_gibibytes   = <size>
     block_size_bytes = <block_size>

     # Only for boot disks. Use one of the supported disk sources.
     source_image_family = {
       image_family = "<image_family>"
       parent_id    = "<project_ID_for_image_family>" # Optional: for custom image families only
     }
     source_image_id = "<custom_image_ID>"

     source_snapshot_id = "<snapshot_ID>"

     # Optional: only for NETWORK_SSD_NON_REPLICATED and NETWORK_SSD_IO_M3
     disk_encryption = {
       type = "DISK_ENCRYPTION_MANAGED"
     }

     # Optional: protect disk from deletion
     forbid_deletion = true
   }
   ```

   For `parent_id`, use the [project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3). For more information about other parameters, see [Volume parameters](#volume-parameters). For the full reference on the disk resource, see [nebius\_compute\_v1\_disk](https://docs.nebius.com/terraform-provider/reference/resources/compute_v1_disk.md).

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

```go theme={null}
// One of compute.DiskSpec_NETWORK_SSD,
// compute.DiskSpec_NETWORK_SSD_NON_REPLICATED,
// or compute.DiskSpec_NETWORK_SSD_IO_M3.
diskType := compute.DiskSpec_NETWORK_SSD_NON_REPLICATED
diskEncryptionType := compute.DiskEncryption_DISK_ENCRYPTION_MANAGED

operation, err := sdk.Services().Compute().V1().
    Disk().Create(
        ctx,
        &compute.CreateDiskRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<disk_name>",
            },
            Spec: &compute.DiskSpec{
                Size: &compute.DiskSpec_SizeGibibytes{
                    SizeGibibytes: <size>,
                },
                BlockSizeBytes: <block_size>,
                Type:           diskType,
                Source: &compute.DiskSpec_SourceImageFamily{
                    SourceImageFamily: &compute.SourceImageFamily{
                        ImageFamily: "<OS_image>",
                    },
                },
                DiskEncryption: &compute.DiskEncryption{
                    Type: diskEncryptionType,
                },
                ForbidDeletion: true,
            },
        },
    )
if err != nil {
    return err
}
if _, err = operation.Wait(ctx); err != nil {
    return err
}
```

For more information, see [Volume parameters](#volume-parameters).

**Python SDK**

```python theme={null}
# One of DiskSpec.DiskType.NETWORK_SSD,
# DiskSpec.DiskType.NETWORK_SSD_NON_REPLICATED,
# or DiskSpec.DiskType.NETWORK_SSD_IO_M3.
disk_type = DiskSpec.DiskType.NETWORK_SSD_NON_REPLICATED
encryption_type = (
    DiskEncryption.DiskEncryptionType.DISK_ENCRYPTION_MANAGED
)

disk_service = DiskServiceClient(sdk)
create_disk_operation = await disk_service.create(
    CreateDiskRequest(
        metadata=ResourceMetadata(
            name="<disk_name>",
        ),
        spec=DiskSpec(
            block_size_bytes=<block_size>,
            type=disk_type,
            source_image_family=SourceImageFamily(
                image_family="<OS_image>",
            ),
            disk_encryption=DiskEncryption(
                type=encryption_type,
            ),
            forbid_deletion=True,
            size_gibibytes=<size>,
        ),
    ),
)
await create_disk_operation.wait()
```

For more information, see [Volume parameters](#volume-parameters).

**JavaScript SDK**

```ts theme={null}
// One of DiskSpec_DiskType.NETWORK_SSD,
// DiskSpec_DiskType.NETWORK_SSD_NON_REPLICATED,
// or DiskSpec_DiskType.NETWORK_SSD_IO_M3.
const diskType = DiskSpec_DiskType.NETWORK_SSD_NON_REPLICATED;

const createDiskService = new DiskService(sdk);
const createDiskOperation = await createDiskService.create(
  CreateDiskRequest.create({
    metadata: ResourceMetadata.create({
      name: "<disk_name>",
    }),
    spec: DiskSpec.create({
      blockSizeBytes: <block_size>,
      type: diskType,
      source: {
        $case: "sourceImageFamily",
        sourceImageFamily: SourceImageFamily.create({
          imageFamily: "<OS_image>",
        }),
      },
      diskEncryption: DiskEncryption.create({
        type: DiskEncryption_DiskEncryptionType.DISK_ENCRYPTION_MANAGED,
      }),
      forbidDeletion: true,
      size: {
        $case: "sizeGibibytes",
        sizeGibibytes: <size>,
      },
    }),
  }),
).result;
await createDiskOperation.wait();
```

For more information, see [Volume parameters](#volume-parameters).

For more information about how to start using secondary disks, see [Attaching and mounting Compute volumes to VMs](https://docs.nebius.com/compute/storage/use.md).

## How to create a shared filesystem

**Web console**

1. In the sidebar, go to  **Storage** → **Shared filesystems**.
2. Click **Create filesystem**.
3. On the creation page, specify a filesystem name.
4. Set the filesystem size and block size.
5. (Optional) Enable **Deletion protection** to prevent this filesystem from being accidentally deleted.
6. Click **Create filesystem**.

**CLI**

Run the following command:

```bash theme={null}
nebius compute filesystem create \
  --name <filesystem_name> \
  --type network_ssd \
  --size-gibibytes <size> \
  --block-size-bytes <block_size> \
  --forbid-deletion
```

For more details about volume parameters, see [Volume parameters](#volume-parameters).

**Terraform**

1. Create the following configuration:

   ```hcl theme={null}
   resource "nebius_compute_v1_filesystem" "<filesystem_name>" {
     name             = "<filesystem_name>"
     parent_id        = "<project_ID>"
     type             = "NETWORK_SSD"
     size_gibibytes   = <size>
     block_size_bytes = <block_size>

     # Optional: protect filesystem from deletion
     forbid_deletion = true
   }
   ```

   For `parent_id`, use [project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3). For more information about other parameters, see [Volume parameters](#volume-parameters). For the full reference on the filesystem resource, see [nebius\_compute\_v1\_filesystem](https://docs.nebius.com/terraform-provider/reference/resources/compute_v1_filesystem.md).

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

```go theme={null}
operation, err = sdk.Services().Compute().V1().
    Filesystem().Create(
        ctx,
        &compute.CreateFilesystemRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<filesystem_name>",
            },
            Spec: &compute.FilesystemSpec{
                Size: &compute.FilesystemSpec_SizeGibibytes{
                    SizeGibibytes: <size>,
                },
                BlockSizeBytes: <block_size>,
                Type:           compute.FilesystemSpec_NETWORK_SSD,
                ForbidDeletion: true,
            },
        },
    )
if err != nil {
    return err
}
if _, err = operation.Wait(ctx); err != nil {
    return err
}
```

For more details about volume parameters, see [Volume parameters](#volume-parameters).

**Python SDK**

```python theme={null}
filesystem_service = FilesystemServiceClient(sdk)
create_filesystem_operation = await filesystem_service.create(
    CreateFilesystemRequest(
        metadata=ResourceMetadata(
            name="<filesystem_name>",
        ),
        spec=FilesystemSpec(
            block_size_bytes=<block_size>,
            type=FilesystemSpec.FilesystemType.NETWORK_SSD,
            forbid_deletion=True,
            size_gibibytes=<size>,
        ),
    ),
)
await create_filesystem_operation.wait()
```

For more details about volume parameters, see [Volume parameters](#volume-parameters).

**JavaScript SDK**

```ts theme={null}
const createFilesystemService = new FilesystemService(sdk);
const createFilesystemOperation = await createFilesystemService.create(
  CreateFilesystemRequest.create({
    metadata: ResourceMetadata.create({
      name: "<filesystem_name>",
    }),
    spec: FilesystemSpec.create({
      blockSizeBytes: <block_size>,
      type: FilesystemSpec_FilesystemType.NETWORK_SSD,
      forbidDeletion: true,
      size: {
        $case: "sizeGibibytes",
        sizeGibibytes: <size>,
      },
    }),
  }),
).result;
await createFilesystemOperation.wait();
```

For more details about volume parameters, see [Volume parameters](#volume-parameters).

For more information about how to start using the created shared filesystem, see [Attaching and mounting Compute volumes to VMs](https://docs.nebius.com/compute/storage/use.md).

To access and transfer data in a shared filesystem through the Object Storage [S3-compatible API](https://docs.nebius.com/object-storage/interfaces/aws-cli.md), create a [filesystem bucket](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md). You can then use the AWS CLI and other S3-compatible tools to work with data in the filesystem.

## Volume parameters

Disks and shared filesystems share almost all of their parameters, except for boot disk image which can only be set for disks.

CLI parameter names are shown in parentheses. Terraform uses the corresponding snake\_case attributes, and SDKs use the corresponding parameter names for each language, such as camelCase in JavaScript, as shown in the examples.

### Metadata

**Name** (`name`): A Nebius AI Cloud resource name. It must be unique inside your tenant. Required at creation, cannot be changed after it.

### Type, encryption and size

* **Type** (`type`): The volume type. See available types of [disks](https://docs.nebius.com/compute/storage/types.md#network-and-local-ssd-disks) and [shared filesystems](https://docs.nebius.com/compute/storage/types.md#filesystem-specifications). Required at creation, and cannot be changed later.

* **Enable data encryption** (`disk-encryption-type`): Whether a volume should support [data encryption](https://docs.nebius.com/security/encryption.md). Encryption allows you to store personal and other sensitive data securely on volumes, and reduce the risk of unauthorized access.

  Use this parameter only for disks of the Network SSD Non-replicated and Network SSD IO M3 types. Filesystems and Network SSD disks support encryption by default, and you cannot disable it. For more information, see [Encryption of disks](https://docs.nebius.com/compute/storage/types.md#encryption-of-disks).

  In the CLI, use `--disk-encryption-type disk_encryption_managed` to enable encryption.

* **Block size** (`block-size-bytes`): The data block size for the volume. The data stored on the volume is divided into blocks of this size on the underlying physical drives. The block size cannot be changed after the volume is created.

  The block size must be a power of two between 4096 bytes (4 KiB) and 131,072 bytes (128 KiB). The default value is 4096 bytes (4 KiB).

  For maximum IOPS, reads and writes to a volume should be close to its block size.

* **Size** (`size-gibibytes`, `size-mebibytes`, `size-kibibytes` or `size-bytes`): The volume size. See requirements for sizes of [disks](https://docs.nebius.com/compute/storage/types.md#disk-types-comparison) and [shared filesystems](https://docs.nebius.com/compute/storage/types.md#filesystem-specifications) in their comparison tables. Required at creation. After creation, size can only be [increased](#how-to-resize-a-volume).

  When using the CLI, you can set the volume size in GiB, MiB, KiB or B using a respective parameter.

  For disks, the size must be a multiple of both 4 MiB and the block size. A disk can contain up to 4,294,967,296 blocks, so the selected block size can further restrict the capacity listed for the disk type. With the default block size of 4 KiB, a disk cannot exceed 16 TiB. Select a larger block size for disks above 16 TiB.

  Boot disks cannot exceed 30,720 GiB (30 TiB).

### Disk sources

Use one of the supported disk sources:

* **Public image** (`source-image-family-image-family`): Create a boot disk from one of the [public images](https://docs.nebius.com/compute/storage/boot-disk-images.md) that Nebius AI Cloud provides. An image represents an operating system for the disk.
* **Custom image** (`source-image-id`): Create a boot disk based on your [custom image](https://docs.nebius.com/compute/storage/custom-disk-images.md) that includes custom software.
* **Custom image family** (both `source-image-family-image-family` and `source-image-family-parent-id`): Create a boot disk based on your custom image family. When you create custom images, you can add them to an arbitrary custom family. If an image family contains several images, the latest one is used.
* **Snapshot** (`source-snapshot-id`): Create a boot or additional disk based on a [disk snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md).

To create a blank additional disk, don't specify any disk source.

### Deletion protection

* **Deletion protection** (`forbid-deletion`): Prevents the volume from being deleted. Use this parameter to protect disks and shared filesystems from accidental deletion, especially in automated environments such as CI/CD pipelines or Terraform configurations.

  Deletion protection can be enabled at creation time or changed at any time after creation. When enabled, any attempt to delete the volume fails with an error. To delete a protected volume, disable deletion protection first.

## How to resize a volume

You can increase the size of an existing disk or shared filesystem. Reducing volume size is not possible.

### How to resize a disk

> [!NOTE]
>
> Compute supports *hot resize*: the resize operation itself does not require stopping the VM. However, you need to restart the VM afterward for the operating system to recognize the new disk size.

To resize a disk:

1. Change the disk size:

   **Web console**

   1. In the sidebar, go to  **Storage** → **Disks**.

      Alternatively, go to the virtual machine where the disk is attached and find it in the **Disks** tab.

   2. Click the disk you want to resize and go to the **Settings** tab.

   3. In the **Parameters** section, enter the new **Size** value or use the slider to set the new size.

   4. Click **Save changes**.

   **CLI**

   1. If you haven't saved the disk's ID when creating it, get its ID:

      ```bash theme={null}
      export DISK_ID=$(nebius compute disk get-by-name \
        --parent-id <project_ID> \
        --name <disk_name> \
        --format jsonpath='{.metadata.id}')
      ```

   2. Run [nebius compute disk update](https://docs.nebius.com/cli/reference/compute/disk/update.md) and set the new size by using one of the `--size-gibibytes`, `--size-mebibytes`, `--size-kibibytes` or `--size-bytes` parameters:

      ```bash theme={null}
      nebius compute disk update \
        --id $DISK_ID \
        --size-gibibytes <size>
      ```

   **Terraform**

   1. In your Terraform configuration, update the `size_gibibytes` value (or `size_mebibytes`, `size_kibibytes`, `size_bytes`) in the disk resource. For example:

      ```hcl highlight={4} theme={null}
      resource "nebius_compute_v1_disk" "<disk_name>" {
        name             = "<disk_name>"
        ...
        size_gibibytes   = <new_size>
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

   1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

      ```go theme={null}
      disk, err := sdk.Services().Compute().V1().
          Disk().GetByName(
              ctx,
              &common.GetByNameRequest{
                  ParentId: "<project_ID>",
                  Name:     "<disk_name>",
              },
          )
      if err != nil {
          return err
      }
      diskID := disk.GetMetadata().GetId()
      ```

      For a filesystem, get its ID by name with the same parameters.

   2. Update the disk or filesystem size. Here is an example for a disk:

      ```go theme={null}
      disk, err = sdk.Services().Compute().V1().
          Disk().Get(
              ctx,
              &compute.GetDiskRequest{
                  Id: diskID,
              },
          )
      if err != nil {
          return err
      }
      if disk.GetSpec() == nil {
          return errors.New("disk spec is missing")
      }
      disk.Spec.Size = &compute.DiskSpec_SizeGibibytes{
          SizeGibibytes: <size>,
      }
      operation, err = sdk.Services().Compute().V1().
          Disk().Update(
              ctx,
              &compute.UpdateDiskRequest{
                  Metadata: disk.Metadata,
                  Spec:     disk.Spec,
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

   1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

      ```python theme={null}
      disk_service = DiskServiceClient(sdk)
      disk = await disk_service.get_by_name(
          GetByNameRequest(
              parent_id="<project_ID>",
              name="<disk_name>",
          ),
      )
      disk_id = disk.metadata.id
      ```

      For a filesystem, get its ID by name with the same parameters.

   2. Update the disk or filesystem size. Here is an example for a disk:

      ```python theme={null}
      disk_service = DiskServiceClient(sdk)
      disk = await disk_service.get(
          GetDiskRequest(id=disk_id),
      )
      if disk.spec is None:
          raise ValueError("disk spec is missing")
      disk.spec.size_gibibytes = <size>
      update_disk_operation = await disk_service.update(
          UpdateDiskRequest(
              metadata=disk.metadata,
              spec=disk.spec,
          ),
      )
      await update_disk_operation.wait()
      ```

   **JavaScript SDK**

   1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

      ```ts theme={null}
      const getDiskByNameService = new DiskService(sdk);
      const diskByName = await getDiskByNameService.getByName(
        GetByNameRequest.create({
          parentId: "<project_ID>",
          name: "<disk_name>",
        }),
      );
      const diskId = diskByName.metadata?.id;
      if (!diskId) {
        throw new Error("disk ID is missing");
      }
      ```

      For a filesystem, get its ID by name with the same parameters.

   2. Update the disk or filesystem size. Here is an example for a disk:

      ```ts theme={null}
      const updateDiskService = new DiskService(sdk);
      const diskForResize = await updateDiskService.get(
        GetDiskRequest.create({
          id: diskId,
        }),
      );
      if (!diskForResize.spec) {
        throw new Error("disk spec is missing");
      }
      diskForResize.spec.size = {
        $case: "sizeGibibytes",
        sizeGibibytes: <size>,
      };
      const updateDiskResizeOperation = await updateDiskService.update(
        UpdateDiskRequest.create({
          metadata: diskForResize.metadata,
          spec: diskForResize.spec,
        }),
      ).result;
      await updateDiskResizeOperation.wait();
      ```

2. If you resized a secondary disk and it is currently attached to a running virtual machine, do the following:

   1. [Restart](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) this VM.

   2. [Connect](https://docs.nebius.com/compute/virtual-machines/connect.md) to this VM.

   3. Install the `cloud-guest-utils` package that manages the disk partitions:

      ```bash theme={null}
      sudo apt-get update && sudo apt-get install -y cloud-guest-utils
      ```

   4. List disks and partitions:

      ```bash theme={null}
      lsblk --paths
      ```

      Output example:

      ```bash theme={null}
      NAME          MAJ:MIN  RM   SIZE  RO  TYPE  MOUNTPOINTS
      /dev/vda      253:0     0    10G   0  disk
      ├─/dev/vda1   253:1     0     9G   0  part  /
      ├─/dev/vda14  253:14    0     4M   0  part
      ├─/dev/vda15  253:15    0   106M   0  part  /boot/efi
      └─/dev/vda16  259:0     0   913M   0  part  /boot
      /dev/vdb      253:16    0     1M   0  disk
      /dev/vdc      253:32    0    20G   0  disk
      └─/dev/vdc1   253:33    0    10G   0  part  /mnt/disk-0
      ```

      Find the device name of the resized disk and get the name of its last partition. The secondary disk is most likely the last one in the list. Also, check the `SIZE` column: it shows that the disk size is increased, but the partition size stays the same. In this example, the required device name is `/dev/vdc`, and the partition is `/dev/vdc1`.

   5. Grow the partition to fill the disk:

      ```bash theme={null}
      sudo growpart /dev/vdc 1
      ```

      If you work with a disk that has a device name other than `/dev/vdc`, change the device name and the partition index `1` in the current command and commands below. You can get the index of the partition from its name. Only the last partition may be grown.

      > [!NOTE]
      >
      > In the commands, you can use the device ID of the disk (`/dev/disk/by-id/virtio-disk-0`) instead of the device name (`/dev/vdc`). Run the `ls /dev/disk/by-id` command to get device IDs for all disks.

   6. Refresh the kernel partition table for the disk and wait for the device information to be updated:

      ```bash theme={null}
      sudo partprobe /dev/vdc && sudo udevadm settle
      ```

   7. Show information about partitions and check that the size of the partition has increased:

      ```bash theme={null}
      lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT /dev/vdc
      ```

      Output example:

      ```bash theme={null}
      NAME    SIZE  TYPE  FSTYPE  MOUNTPOINT
      vdc      25G  disk
      └─vdc1   25G  part  ext4    /mnt/disk-0
      ```

   8. Grow the `ext4` filesystem on the increased partition:

      ```bash theme={null}
      sudo resize2fs /dev/vdc1
      ```

   9. Check that the filesystem size has increased:

      ```bash theme={null}
      df -hT
      ```

      Output example:

      ```bash theme={null}
      Filesystem      Type       Size   Used  Avail  Use%  Mounted on
      tmpfs           tmpfs      795M   1.1M   794M    1%  /run
      /dev/vda1       ext4        38G   3.3G    35G    9%  /
      tmpfs           tmpfs      3.9G      0   3.9G    0%  /dev/shm
      tmpfs           tmpfs      5.0M      0   5.0M    0%  /run/lock
      cloud-metadata  virtiofs   252G    16K   252G    1%  /mnt/cloud-metadata
      /dev/vdc1       ext4        25G    24K    24G    1%  /mnt/disk-0
      /dev/vda16      ext4       881M   174M   645M   22%  /boot
      /dev/vda15      vfat       105M   6.2M    99M    6%  /boot/efi
      tmpfs           tmpfs      795M    12K   795M    1%  /run/user/1001
      ```

### How to resize a shared filesystem

To resize a shared filesystem:

**Web console**

1. In the sidebar, go to  **Storage** → **Shared filesystems**.

   Alternatively, go to the virtual machine where the filesystem is attached and find it in the **Shared filesystems** tab.

2. Click the filesystem you want to resize and go to the **Settings** tab.

3. In the **Parameters** section, enter the new **Size** value or use the slider to set the new size.

4. Click **Save changes**.

**CLI**

1. If you haven't saved the filesystem's ID when creating it, get its ID by using [nebius compute filesystem get-by-name](https://docs.nebius.com/cli/reference/compute/filesystem/get-by-name.md).

2. Run [nebius compute filesystem update](https://docs.nebius.com/cli/reference/compute/filesystem/update.md) and set the new size by using one of the `--size-gibibytes`, `--size-mebibytes`, `--size-kibibytes` or `--size-bytes` parameters.

**Terraform**

1. In your Terraform configuration, update the `size_gibibytes` value (or `size_mebibytes`, `size_kibibytes`, `size_bytes`) in the filesystem resource. For example:

   ```hcl highlight={4} theme={null}
   resource "nebius_compute_v1_filesystem" "<filesystem_name>" {
     name             = "<filesystem_name>"
     ...
     size_gibibytes   = <new_size>
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

## How to enable or disable deletion protection

You can only change deletion protection of a [standalone disk](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). If you need to update a VM-managed disk, [convert it first to standalone](#how-to-make-a-disk-vm-managed-or-standalone).

To enable or disable deletion protection:

**Web console**

1. In the sidebar, go to  **Storage** → **Disks** or  **Storage** → **Shared filesystems**.
2. Click the volume you want to update and go to the **Settings** tab.
3. In the **Parameters** section, enable or disable **Deletion protection**.
4. Click **Save changes**.

**CLI**

1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

   ```bash theme={null}
   export DISK_ID=$(nebius compute disk get-by-name \
     --parent-id <project_ID> \
     --name <disk_name> \
     --format jsonpath='{.metadata.id}')
   ```

   For a filesystem, use [nebius compute filesystem get-by-name](https://docs.nebius.com/cli/reference/compute/filesystem/get-by-name.md) with the same parameters.

2. Run [nebius compute disk update](https://docs.nebius.com/cli/reference/compute/disk/update.md) for a disk, or [nebius compute filesystem update](https://docs.nebius.com/cli/reference/compute/filesystem/update.md) for a filesystem:

   ```bash theme={null}
   nebius compute disk update \
     --id $DISK_ID \
     --forbid-deletion=<true|false>
   ```

**Terraform**

1. In your Terraform configuration, set `forbid_deletion` to `true` or `false` in the disk or filesystem resource. For example, for a disk:

   ```hcl highlight={4} theme={null}
   resource "nebius_compute_v1_disk" "<disk_name>" {
     name             = "<disk_name>"
     ...
     forbid_deletion  = true
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

1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

   ```go theme={null}
   disk, err := sdk.Services().Compute().V1().
       Disk().GetByName(
           ctx,
           &common.GetByNameRequest{
               ParentId: "<project_ID>",
               Name:     "<disk_name>",
           },
       )
   if err != nil {
       return err
   }
   diskID := disk.GetMetadata().GetId()
   ```

   For a filesystem, get its ID by name with the same parameters.

2. Update the disk or filesystem deletion protection. Here is an example for a disk:

   ```go theme={null}
   disk, err = sdk.Services().Compute().V1().
       Disk().Get(
           ctx,
           &compute.GetDiskRequest{
               Id: diskID,
           },
       )
   if err != nil {
       return err
   }
   if disk.GetSpec() == nil {
       return errors.New("disk spec is missing")
   }
   disk.Spec.ForbidDeletion = <true|false>
   operation, err = sdk.Services().Compute().V1().
       Disk().Update(
           ctx,
           &compute.UpdateDiskRequest{
               Metadata: disk.Metadata,
               Spec:     disk.Spec,
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

1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   disk = await disk_service.get_by_name(
       GetByNameRequest(
           parent_id="<project_ID>",
           name="<disk_name>",
       ),
   )
   disk_id = disk.metadata.id
   ```

   For a filesystem, get its ID by name with the same parameters.

2. Update the disk or filesystem deletion protection. Here is an example for a disk:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   disk = await disk_service.get(
       GetDiskRequest(id=disk_id),
   )
   if disk.spec is None:
       raise ValueError("disk spec is missing")
   disk.spec.forbid_deletion = <True|False>
   update_disk_operation = await disk_service.update(
       UpdateDiskRequest(
           metadata=disk.metadata,
           spec=disk.spec,
       ),
   )
   await update_disk_operation.wait()
   ```

**JavaScript SDK**

1. If you haven't saved the disk or filesystem's ID when creating it, get its ID:

   ```ts theme={null}
   const getDiskByNameService = new DiskService(sdk);
   const diskByName = await getDiskByNameService.getByName(
     GetByNameRequest.create({
       parentId: "<project_ID>",
       name: "<disk_name>",
     }),
   );
   const diskId = diskByName.metadata?.id;
   if (!diskId) {
     throw new Error("disk ID is missing");
   }
   ```

   For a filesystem, get its ID by name with the same parameters.

2. Update the disk or filesystem deletion protection. Here is an example for a disk:

   ```ts theme={null}
   const updateDiskDeletionService = new DiskService(sdk);
   const diskForDeletion = await updateDiskDeletionService.get(
     GetDiskRequest.create({
       id: diskId,
     }),
   );
   if (!diskForDeletion.spec) {
     throw new Error("disk spec is missing");
   }
   diskForDeletion.spec.forbidDeletion = <true|false>;
   const updateDiskDeletionOperation =
     await updateDiskDeletionService.update(
       UpdateDiskRequest.create({
         metadata: diskForDeletion.metadata,
         spec: diskForDeletion.spec,
       }),
     ).result;
   await updateDiskDeletionOperation.wait();
   ```

> [!NOTE]
>
> If you try to delete a volume with deletion protection enabled, the operation will fail, and you'll see the following message: `Error: rpc error: code = FailedPrecondition desc = disk cannot be deleted because forbid_deletion is set`. Disable deletion protection first, then delete the volume.

## How to make a disk VM-managed or standalone

Each disk is either [VM-managed or standalone](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). You can convert a disk from one state to another. To do so:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. Open the page of the required VM and then go to the **Disks** tab.
3. In the line of the required disk, click  → **Convert to VM-managed** or  → **Convert to standalone**.

## How to delete a volume

> [!WARNING]
>
> Deleting a volume permanently removes all data stored on it. Before deleting, make sure the volume is [detached](https://docs.nebius.com/compute/storage/detach-volume.md) from any virtual machine.

**Web console**

1. In the sidebar, go to  **Storage** → **Disks** or  **Storage** → **Shared filesystems**.
2. Open the page of the volume that you want to delete.
3. Go to the **Settings** tab.
4. Click **Delete disk** or **Delete filesystem**.
5. In the window that opens, confirm the deletion.

**CLI**

1. Get the ID of the volume you want to delete:

   ```bash theme={null}
   nebius compute <disk|filesystem> list
   ```

2. Delete the disk:

   ```bash theme={null}
   nebius compute disk delete <disk_ID>
   ```

3. Delete the filesystem:

   ```bash theme={null}
   nebius compute filesystem delete <filesystem_ID>
   ```

**Terraform**

1. In your Terraform configuration, remove the `nebius_compute_v1_disk` or `nebius_compute_v1_filesystem` resource block.

   If the resource has `forbid_deletion = true`, set it to `false` before removing the resource, then apply the configuration. Once done, remove the resource.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. If you haven't saved the volume ID, get it as described in [How to resize a volume](#how-to-resize-a-volume).

2. Delete the disk:

   ```go theme={null}
   operation, err = sdk.Services().Compute().V1().
       Disk().Delete(
           ctx,
           &compute.DeleteDiskRequest{
               Id: "<disk_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = operation.Wait(ctx); err != nil {
       return err
   }
   ```

3. Delete the filesystem:

   ```go theme={null}
   operation, err = sdk.Services().Compute().V1().
       Filesystem().Delete(
           ctx,
           &compute.DeleteFilesystemRequest{
               Id: "<filesystem_ID>",
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

1. If you haven't saved the volume ID, get it as described in [How to resize a volume](#how-to-resize-a-volume).

2. Delete the disk:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   delete_disk_operation = await disk_service.delete(
       DeleteDiskRequest(
           id="<disk_ID>",
       ),
   )
   await delete_disk_operation.wait()
   ```

3. Delete the filesystem:

   ```python theme={null}
   filesystem_service = FilesystemServiceClient(sdk)
   delete_filesystem_operation = await filesystem_service.delete(
       DeleteFilesystemRequest(
           id="<filesystem_ID>",
       ),
   )
   await delete_filesystem_operation.wait()
   ```

**JavaScript SDK**

1. If you haven't saved the volume ID, get it as described in [How to resize a volume](#how-to-resize-a-volume).

2. Delete the disk:

   ```ts theme={null}
   const deleteDiskService = new DiskService(sdk);
   const deleteDiskOperation = await deleteDiskService.delete(
     DeleteDiskRequest.create({
       id: "<disk_ID>",
     }),
   ).result;
   await deleteDiskOperation.wait();
   ```

3. Delete the filesystem:

   ```ts theme={null}
   const deleteFilesystemService = new FilesystemService(sdk);
   const deleteFilesystemOperation = await deleteFilesystemService.delete(
     DeleteFilesystemRequest.create({
       id: "<filesystem_ID>",
     }),
   ).result;
   await deleteFilesystemOperation.wait();
   ```

## See also

* [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md)
* [Attaching and mounting Compute volumes to VMs](https://docs.nebius.com/compute/storage/use.md)
