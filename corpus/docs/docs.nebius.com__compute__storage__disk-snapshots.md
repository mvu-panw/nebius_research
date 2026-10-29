# Managing disk snapshots in Compute

Source: https://docs.nebius.com/compute/storage/disk-snapshots

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing disk snapshots in Compute

A *disk snapshot* captures a point-in-time copy of a disk. This is an instant disk backup that allows you to:

* Clone and recover a certain state of the disk.
* Eliminate data loss risks.
* Prevent accidental deletion, corruption and security incidents.
* Make a copy of a disk before risky operations, such as software upgrades, patches or configuration changes, so you can roll back in case of issues.
* Fulfill compliance requirements for immutable system versions, if applicable.

To clone a disk state, [create a snapshot](#how-to-create-a-snapshot). To restore a disk state, [create a new disk from a snapshot](#how-to-create-a-disk-from-a-snapshot).

Snapshots support both boot and additional disks. They also support all [disk types](https://docs.nebius.com/compute/storage/types.md#disk-types): SSD, SSD Non-replicated and SSD IO M3.

Every snapshot is only available in the project where it was created. Therefore, you can only work with snapshots and disks within the project.

Nebius AI Cloud charges for a complete copy of a disk and applies separate pricing for snapshots. For more information, see [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md#disk-snapshots).

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

* [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create a snapshot

To create a snapshot, you don't need to stop a virtual machine.

**Web console**

1. In the sidebar, go to  **Storage** → **Disks**.

2. In the list of disks, find the disk that you want to create a snapshot for.

3. In the line of the required disk, click  → **Create snapshot**.

4. In the window that opens, specify the name and optionally the description of the snapshot.

   The ID of the selected disk is prefilled in the **Source disk** field.

5. Click **Create snapshot**.

Once you create a snapshot, it appears on the disk page. There, you can find all snapshots created for a given disk.

**CLI**

Run the following command:

```bash theme={null}
nebius compute disk-snapshot create \
   --name <snapshot_name> \
   --description "<snapshot_description>" \
   --source-disk-id <disk_ID>
```

The command contains the following parameters:

* `--name`: Snapshot name.
* `--description` (optional): Snapshot description.
* `--source-disk-id`: ID of the disk that you want to create a snapshot for. To get the disk ID, run `nebius compute disk list`.

**Terraform**

1. Create the following configuration:

   ```hcl theme={null}
   resource "nebius_compute_v1_disk_snapshot" "<snapshot_name>" {
     name           = "<snapshot_name>"
     parent_id      = "<project_ID>"
     description    = "<snapshot_description>"
     source_disk_id = "<disk_ID>"
   }
   ```

   The file contains the following parameters:

   * `name`: Snapshot name.
   * `parent_id`: [ID of the project](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) where the snapshot is created. Use the project that contains the source disk.
   * `description` (optional): Snapshot description.
   * `source_disk_id`: ID of the disk that you want to create a snapshot for.

   For the full resource reference, see [nebius\_compute\_v1\_disk\_snapshot](https://docs.nebius.com/terraform-provider/reference/resources/compute_v1_disk_snapshot.md).

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
snapshotOperation, err := sdk.Services().Compute().V1().
    DiskSnapshot().Create(
        ctx,
        &compute.CreateDiskSnapshotRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<snapshot_name>",
            },
            Spec: &compute.DiskSnapshotSpec{
                SourceDiskId: "<disk_ID>",
                Description:  "<snapshot_description>",
            },
        },
    )
if err != nil {
    return err
}
if _, err = snapshotOperation.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameters:

* `Metadata.Name`: Snapshot name.
* `Spec.SourceDiskId`: ID of the disk that you want to create a snapshot for.
* `Spec.Description` (optional): Snapshot description.

**Python SDK**

```python theme={null}
snapshot_service = DiskSnapshotServiceClient(sdk)
create_snapshot_operation = await snapshot_service.create(
    CreateDiskSnapshotRequest(
        metadata=ResourceMetadata(
            name="<snapshot_name>",
        ),
        spec=DiskSnapshotSpec(
            source_disk_id="<disk_ID>",
            description="<snapshot_description>",
        ),
    ),
)
await create_snapshot_operation.wait()
```

The code contains the following parameters:

* `metadata.name`: Snapshot name.
* `spec.source_disk_id`: ID of the disk that you want to create a snapshot for.
* `spec.description` (optional): Snapshot description.

**JavaScript SDK**

```ts theme={null}
const snapshotService = new DiskSnapshotService(sdk);
const createSnapshotOperation = await snapshotService.create(
  CreateDiskSnapshotRequest.create({
    metadata: ResourceMetadata.create({
      name: "<snapshot_name>",
    }),
    spec: DiskSnapshotSpec.create({
      sourceDiskId: "<disk_ID>",
      description: "<snapshot_description>",
    }),
  }),
).result;
await createSnapshotOperation.wait();
```

The code contains the following parameters:

* `metadata.name`: Snapshot name.
* `spec.sourceDiskId`: ID of the disk that you want to create a snapshot for.
* `spec.description` (optional): Snapshot description.

## How to create a disk from a snapshot

After you [prepare a snapshot](#how-to-create-a-snapshot), you can create a disk based on this snapshot. Thus, you restore the needed disk state with data integrity verified.

To create a disk from a snapshot:

**Web console**

1. In the sidebar, go to  **Storage** → **Disks** → **Snapshots**.

2. In the line of the required snapshot, click  → **Create disk**.

3. On the disk creation page that opens, check the **Disk source type** and **Snapshot** fields. They are prefilled:

   * **Disk source type**: Snapshot.
   * **Snapshot**: ID of the selected snapshot.

4. Set other needed [fields for the disk](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk) and click **Create disk**.

**CLI**

Run the following command:

```bash theme={null}
nebius compute disk create \
   --name <disk_name> \
   --type network_<ssd|ssd_non_replicated|ssd_io_m3> \
   --size-gibibytes <size> \
   --block-size-bytes <block_size> \
   --source-snapshot-id <snapshot_ID>
```

To get the snapshot ID, run `nebius compute disk-snapshot list`.

**Terraform**

1. Create the following configuration:

   ```hcl theme={null}
   resource "nebius_compute_v1_disk" "<disk_name>" {
     name               = "<disk_name>"
     parent_id          = "<project_ID>"
     type               = "NETWORK_<SSD|SSD_NON_REPLICATED|SSD_IO_M3>"
     size_gibibytes     = <size>
     block_size_bytes   = <block_size>
     source_snapshot_id = "<snapshot_ID>"
   }
   ```

   For `parent_id`, use the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). For more information about other parameters, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters). For the full reference on the disk resource, see [nebius\_compute\_v1\_disk](https://docs.nebius.com/terraform-provider/reference/resources/compute_v1_disk.md).

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
diskType := compute.DiskSpec_NETWORK_SSD
diskOperation, err := sdk.Services().Compute().V1().
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
                Source: &compute.DiskSpec_SourceSnapshotId{
                    SourceSnapshotId: "<snapshot_ID>",
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = diskOperation.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameters:

* `diskType`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
* `Metadata.Name`: Disk name.
* `Spec.Size.SizeGibibytes`: Disk size in gibibytes.
* `Spec.BlockSizeBytes`: Block size in bytes.
* `Spec.Type`: Disk type set by `diskType`.
* `Spec.Source.SourceSnapshotId`: ID of the snapshot to create the disk from.

**Python SDK**

```python theme={null}
# One of DiskSpec.DiskType.NETWORK_SSD,
# DiskSpec.DiskType.NETWORK_SSD_NON_REPLICATED,
# or DiskSpec.DiskType.NETWORK_SSD_IO_M3.
disk_type = DiskSpec.DiskType.NETWORK_SSD

disk_service = DiskServiceClient(sdk)
create_disk_operation = await disk_service.create(
    CreateDiskRequest(
        metadata=ResourceMetadata(
            name="<disk_name>",
        ),
        spec=DiskSpec(
            block_size_bytes=<block_size>,
            type=disk_type,
            source_snapshot_id="<snapshot_ID>",
            size_gibibytes=<size>,
        ),
    ),
)
await create_disk_operation.wait()
```

The code contains the following parameters:

* `disk_type`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
* `metadata.name`: Disk name.
* `spec.block_size_bytes`: Block size in bytes.
* `spec.type`: Disk type set by `disk_type`.
* `spec.source_snapshot_id`: ID of the snapshot to create the disk from.
* `spec.size_gibibytes`: Disk size in gibibytes.

**JavaScript SDK**

```ts theme={null}
// One of DiskSpec_DiskType.NETWORK_SSD,
// DiskSpec_DiskType.NETWORK_SSD_NON_REPLICATED,
// or DiskSpec_DiskType.NETWORK_SSD_IO_M3.
const diskType = DiskSpec_DiskType.NETWORK_SSD;

const diskService = new DiskService(sdk);
const createDiskOperation = await diskService.create(
  CreateDiskRequest.create({
    metadata: ResourceMetadata.create({
      name: "<disk_name>",
    }),
    spec: DiskSpec.create({
      blockSizeBytes: <block_size>,
      type: diskType,
      source: {
        $case: "sourceSnapshotId",
        sourceSnapshotId: "<snapshot_ID>",
      },
      size: {
        $case: "sizeGibibytes",
        sizeGibibytes: <size>,
      },
    }),
  }),
).result;
await createDiskOperation.wait();
```

The code contains the following parameters:

* `diskType`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
* `metadata.name`: Disk name.
* `spec.blockSizeBytes`: Block size in bytes.
* `spec.type`: Disk type set by `diskType`.
* `spec.source.sourceSnapshotId`: ID of the snapshot to create the disk from.
* `spec.size.sizeGibibytes`: Disk size in gibibytes.

After you create the disk, you can [create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with it.

## How to update a snapshot

**Web console**

In the web console, you can only change the snapshot name.

1. In the sidebar, go to  **Storage** → **Disks** → **Snapshots**.
2. In the line of the required snapshot, click  → **Settings**.
3. On the page of the snapshot settings that opens, update the snapshot name and click **Save changes**.

**CLI**

In the CLI, you can change the snapshot name and description.

Run the following command:

```bash theme={null}
nebius compute disk-snapshot update \
   --id <snapshot_ID> \
   --name <new_snapshot_name> \
   --description "<new_snapshot_description>"
```

In the command, specify the ID of the snapshot that you want to update. To get the snapshot ID, run `nebius compute disk-snapshot list`.

**Terraform**

1. In the configuration file, update the `nebius_compute_v1_disk_snapshot` resource:

   ```hcl theme={null}
   resource "nebius_compute_v1_disk_snapshot" "<snapshot_name>" {
     name           = "<new_snapshot_name>"
     description    = "<new_snapshot_description>"

     # ...
   }
   ```

   You can update the following parameters:

   * `name`: Snapshot name.
   * `description`: Snapshot description.

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
snapshotForUpdate, err := sdk.Services().Compute().V1().
    DiskSnapshot().Get(
        ctx,
        &compute.GetDiskSnapshotRequest{
            Id: "<snapshot_ID>",
        },
    )
if err != nil {
    return err
}
if snapshotForUpdate.GetMetadata() == nil ||
    snapshotForUpdate.GetSpec() == nil {
    return errors.New("snapshot metadata or spec is missing")
}
snapshotForUpdate.Metadata.Name = "<new_snapshot_name>"
snapshotForUpdate.Spec.Description = "<new_snapshot_description>"
snapshotOperation, err = sdk.Services().Compute().V1().
    DiskSnapshot().Update(
        ctx,
        &compute.UpdateDiskSnapshotRequest{
            Metadata: snapshotForUpdate.Metadata,
            Spec:     snapshotForUpdate.Spec,
        },
    )
if err != nil {
    return err
}
if _, err = snapshotOperation.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameters:

* `GetDiskSnapshotRequest.Id`: ID of the snapshot that you want to update.
* `Metadata.Name`: New snapshot name.
* `Spec.Description`: New snapshot description.

**Python SDK**

```python theme={null}
snapshot_service = DiskSnapshotServiceClient(sdk)
snapshot = await snapshot_service.get(
    GetDiskSnapshotRequest(id="<snapshot_ID>"),
)
if snapshot.metadata is None or snapshot.spec is None:
    raise ValueError("snapshot metadata or spec is missing")
snapshot.metadata.name = "<new_snapshot_name>"
snapshot.spec.description = "<new_snapshot_description>"
update_snapshot_operation = await snapshot_service.update(
    UpdateDiskSnapshotRequest(
        metadata=snapshot.metadata,
        spec=snapshot.spec,
    ),
)
await update_snapshot_operation.wait()
```

The code contains the following parameters:

* `GetDiskSnapshotRequest.id`: ID of the snapshot that you want to update.
* `metadata.name`: New snapshot name.
* `spec.description`: New snapshot description.

**JavaScript SDK**

```ts theme={null}
const updateSnapshotService = new DiskSnapshotService(sdk);
const snapshotForUpdate = await updateSnapshotService.get(
  GetDiskSnapshotRequest.create({
    id: "<snapshot_ID>",
  }),
);
if (!snapshotForUpdate.metadata || !snapshotForUpdate.spec) {
  throw new Error("snapshot metadata or spec is missing");
}
snapshotForUpdate.metadata.name = "<new_snapshot_name>";
snapshotForUpdate.spec.description = "<new_snapshot_description>";
const updateSnapshotOperation = await updateSnapshotService.update(
  UpdateDiskSnapshotRequest.create({
    metadata: snapshotForUpdate.metadata,
    spec: snapshotForUpdate.spec,
  }),
).result;
await updateSnapshotOperation.wait();
```

The code contains the following parameters:

* `GetDiskSnapshotRequest.id`: ID of the snapshot that you want to update.
* `metadata.name`: New snapshot name.
* `spec.description`: New snapshot description.

## How to delete a snapshot

**Web console**

1. In the sidebar, go to  **Storage** → **Disks** → **Snapshots**.
2. In the line of the required snapshot, click  → **Delete**.
3. In the window that opens, confirm the deletion.

**CLI**

Run the following command:

```bash theme={null}
nebius compute disk-snapshot delete <snapshot_ID>
```

To get the snapshot ID, run `nebius compute disk-snapshot list`.

**Terraform**

1. In your Terraform configuration, remove the `nebius_compute_v1_disk_snapshot` resource for the snapshot that you want to delete.
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
snapshotOperation, err = sdk.Services().Compute().V1().
    DiskSnapshot().Delete(
        ctx,
        &compute.DeleteDiskSnapshotRequest{
            Id: "<snapshot_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = snapshotOperation.Wait(ctx); err != nil {
    return err
}
```

In `DeleteDiskSnapshotRequest.Id`, specify the ID of the snapshot that you want to delete.

**Python SDK**

```python theme={null}
snapshot_service = DiskSnapshotServiceClient(sdk)
delete_snapshot_operation = await snapshot_service.delete(
    DeleteDiskSnapshotRequest(id="<snapshot_ID>"),
)
await delete_snapshot_operation.wait()
```

In `DeleteDiskSnapshotRequest.id`, specify the ID of the snapshot that you want to delete.

**JavaScript SDK**

```ts theme={null}
const deleteSnapshotService = new DiskSnapshotService(sdk);
const deleteSnapshotOperation = await deleteSnapshotService.delete(
  DeleteDiskSnapshotRequest.create({
    id: "<snapshot_ID>",
  }),
).result;
await deleteSnapshotOperation.wait();
```

In `DeleteDiskSnapshotRequest.id`, specify the ID of the snapshot that you want to delete.
