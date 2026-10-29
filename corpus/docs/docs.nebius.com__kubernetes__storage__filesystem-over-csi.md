# Mounting shared filesystems to Pods in a Managed Service for Kubernetes® cluster

Source: https://docs.nebius.com/kubernetes/storage/filesystem-over-csi

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Mounting shared filesystems to Pods in a Managed Service for Kubernetes® cluster

In this tutorial, you will use a Container Storage Interface (CSI) driver offered by Nebius AI Cloud to mount a Compute shared filesystem to nodes in a Managed Service for Kubernetes and use it as a persistent volume shared between Pods running on the nodes.

To work with disks that can be mounted to a single node instead of shared filesystems, see [Mounting disks to Pods in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/storage/disk-over-csi.md).

## Costs

The tutorial includes the following chargeable resources:

* [Compute shared filesystem](https://docs.nebius.com/compute/resources/pricing.md#shared-filesystems)
* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md) that make up a node group

## Prerequisites

1. Set up the interface that you are going to use:

   **CLI**

   [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI. The CLI commands in this article assume that the CLI is properly configured. For example, they omit the ID of the parent project, as it is assumed to be set in the CLI profile.

   **Go SDK**

   [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

   **Python SDK**

   [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

   **JavaScript SDK**

   [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

3. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [Helm](https://helm.sh/docs/intro/install/).

4. Install `jq`:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

5. [Create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) or use an existing one.

## Steps

### Create a shared filesystem

Create a 256 GiB SSD shared filesystem:

**CLI**

```bash theme={null}
nebius compute filesystem create \
  --name mk8s-csi-storage \
  --size-gibibytes 256 \
  --type network_ssd \
  --block-size-bytes 4096
```

When setting the filesystem size (`size-gibibytes`), make sure it is enough for all your Pods to store their data.

**Go SDK**

```go theme={null}
filesystemOperation, err := sdk.Services().Compute().V1().
    Filesystem().Create(
        ctx,
        &compute.CreateFilesystemRequest{
            Metadata: &common.ResourceMetadata{
                Name: "mk8s-csi-storage",
            },
            Spec: &compute.FilesystemSpec{
                Size: &compute.FilesystemSpec_SizeGibibytes{
                    SizeGibibytes: 256,
                },
                BlockSizeBytes: 4096,
                Type: compute.FilesystemSpec_NETWORK_SSD,
            },
        },
    )
if err != nil {
    return err
}
if _, err = filesystemOperation.Wait(ctx); err != nil {
    return err
}
filesystemID := filesystemOperation.ResourceID()
if filesystemID == "" {
    return fmt.Errorf("filesystem ID is missing")
}
```

When setting the filesystem size (`SizeGibibytes`), make sure it is enough for all your Pods to store their data. The code saves the new filesystem's ID to `filesystemID`.

**Python SDK**

```python theme={null}
filesystem_service = FilesystemServiceClient(sdk)
filesystem_operation = await filesystem_service.create(
    CreateFilesystemRequest(
        metadata=ResourceMetadata(name="mk8s-csi-storage"),
        spec=FilesystemSpec(
            block_size_bytes=4096,
            type=FilesystemSpec.FilesystemType.NETWORK_SSD,
            size_gibibytes=256,
        ),
    ),
)
await filesystem_operation.wait()
filesystem_id = filesystem_operation.resource_id
if not filesystem_id:
    raise ValueError("filesystem ID is missing")
```

When setting the filesystem size (`size_gibibytes`), make sure it is enough for all your Pods to store their data. The code saves the new filesystem's ID to `filesystem_id`.

**JavaScript SDK**

```ts theme={null}
const filesystemService = new FilesystemService(sdk);
const filesystemOperation =
  await filesystemService.create(
    CreateFilesystemRequest.create({
      metadata: ResourceMetadata.create({
        name: "mk8s-csi-storage",
      }),
      spec: FilesystemSpec.create({
        blockSizeBytes: 4096,
        type: FilesystemSpec_FilesystemType.NETWORK_SSD,
        size: {
          $case: "sizeGibibytes",
          sizeGibibytes: 256,
        },
      }),
    }),
  ).result;
await filesystemOperation.wait();
const filesystemId = filesystemOperation.resourceId();
if (!filesystemId) {
  throw new Error("filesystem ID is missing");
}
```

When setting the filesystem size (`sizeGibibytes`), make sure it is enough for all your Pods to store their data. The code saves the new filesystem's ID to `filesystemId`.

> [!WARNING]
>
> The filesystem that you are adding to a node group must be located in the same project as the node group's parent cluster. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

### Create a node group and mount the filesystem to nodes

> [!WARNING]
>
> Do not omit `nofail` in the cloud-init user data. If it is not specified and a node cannot find the filesystem on restart (for example, it has been deleted), the node will not boot.

**CLI**

1. Create the cloud-init user data that will mount the shared filesystem to nodes:

   ```bash theme={null}
   export MOUNT_POINT=/mnt/data
   export MOUNT_TAG=csi-storage
   export USER_DATA=$(jq -Rrs '.' <<EOF
   runcmd:
     - sudo mkdir -p $MOUNT_POINT
     - sudo mount -t virtiofs $MOUNT_TAG $MOUNT_POINT
     - printf "%s %s virtiofs defaults,nofail 0 2\n" "$MOUNT_TAG" "$MOUNT_POINT" | sudo tee -a /etc/fstab
   EOF
   )
   ```

   This will mount the filesystem to nodes at `/mnt/data` as `csi-storage`. To use another mount point or mount tag, modify the variables.

2. Create the node group:

   ```bash theme={null}
   nebius mk8s node-group create \
     --parent-id <cluster_ID> \
     --name "ng-1" \
     --fixed-node-count 2 \
     --template-resources-platform "cpu-e2" \
     --template-resources-preset "2vcpu-8gb" \
     --template-filesystems "[{\"existing_filesystem\": {\"id\": \"<filesystem_ID>\"}, \"attach_mode\": \"READ_WRITE\", \"mount_tag\": \"$MOUNT_TAG\"}]" \
     --template-cloud-init-user-data "$USER_DATA"
   ```

**Go SDK**

Create the node group. `CloudInitUserData` carries the commands that mount the shared filesystem to nodes, and `Filesystems` attaches the filesystem itself:

```go theme={null}
fsAttachMode := mk8s.AttachedFilesystemSpec_READ_WRITE
existingFilesystem := &mk8s.ExistingFilesystem{
    Id: "<filesystem_ID>",
}
filesystemType := &mk8s.AttachedFilesystemSpec_ExistingFilesystem{
    ExistingFilesystem: existingFilesystem,
}
userData := strings.Join([]string{
    "runcmd:",
    "  - sudo mkdir -p /mnt/data",
    "  - sudo mount -t virtiofs csi-storage /mnt/data",
    `  - printf "%s %s virtiofs defaults,nofail 0 2\n" ` +
        `"csi-storage" "/mnt/data" | sudo tee -a /etc/fstab`,
}, "\n")
nodeGroupOperation, err := sdk.Services().MK8S().V1().
    NodeGroup().Create(
        ctx,
        &mk8s.CreateNodeGroupRequest{
            Metadata: &common.ResourceMetadata{
                ParentId: "<cluster_ID>",
                Name:     "ng-1",
            },
            Spec: &mk8s.NodeGroupSpec{
                Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                    FixedNodeCount: 2,
                },
                Template: &mk8s.NodeTemplate{
                    Resources: &mk8s.ResourcesSpec{
                        Platform: "cpu-d3",
                        Size: &mk8s.ResourcesSpec_Preset{
                            Preset: "4vcpu-16gb",
                        },
                    },
                    Filesystems: []*mk8s.AttachedFilesystemSpec{
                        {
                            AttachMode: fsAttachMode,
                            MountTag:   "csi-storage",
                            Type:       filesystemType,
                        },
                    },
                    CloudInitUserData: userData,
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = nodeGroupOperation.Wait(ctx); err != nil {
    return err
}
```

This mounts the filesystem to nodes at `/mnt/data` as `csi-storage`. To use another mount point or mount tag, modify `userData` and `MountTag`.

**Python SDK**

Create the node group. `cloud_init_user_data` carries the commands that mount the shared filesystem to nodes, and `filesystems` attaches the filesystem itself:

```python theme={null}
filesystem_attach_mode = (
    AttachedFilesystemSpec.AttachMode.READ_WRITE
)
user_data = "\n".join(
    [
        "runcmd:",
        "  - sudo mkdir -p /mnt/data",
        "  - sudo mount -t virtiofs csi-storage /mnt/data",
        '  - printf "%s %s virtiofs defaults,nofail 0 2\\n" '
        '"csi-storage" "/mnt/data" | sudo tee -a /etc/fstab',
    ],
)
node_group_service = NodeGroupServiceClient(sdk)
node_group_operation = await node_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id="<cluster_ID>",
            name="ng-1",
        ),
        spec=NodeGroupSpec(
            fixed_node_count=2,
            template=NodeTemplate(
                resources=ResourcesSpec(
                    platform="cpu-d3",
                    preset="4vcpu-16gb",
                ),
                filesystems=[
                    AttachedFilesystemSpec(
                        attach_mode=filesystem_attach_mode,
                        existing_filesystem=ExistingFilesystem(
                            id="<filesystem_ID>",
                        ),
                        mount_tag="csi-storage",
                    ),
                ],
                cloud_init_user_data=user_data,
            ),
        ),
    ),
)
await node_group_operation.wait()
```

This mounts the filesystem to nodes at `/mnt/data` as `csi-storage`. To use another mount point or mount tag, modify `user_data` and `mount_tag`.

**JavaScript SDK**

Create the node group. `cloudInitUserData` carries the commands that mount the shared filesystem to nodes, and `filesystems` attaches the filesystem itself:

```ts theme={null}
const userData = [
  "runcmd:",
  "  - sudo mkdir -p /mnt/data",
  "  - sudo mount -t virtiofs csi-storage /mnt/data",
  '  - printf "%s %s virtiofs defaults,nofail 0 2\\n" ' +
    '"csi-storage" "/mnt/data" | sudo tee -a /etc/fstab',
].join("\n");
const nodeGroupService = new NodeGroupService(sdk);
const nodeGroupOperation = await nodeGroupService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: "<cluster_ID>",
      name: "ng-1",
    }),
    spec: NodeGroupSpec.create({
      size: {
        $case: "fixedNodeCount",
        fixedNodeCount: 2,
      },
      template: NodeTemplate.create({
        resources: ResourcesSpec.create({
          platform: "cpu-d3",
          size: {
            $case: "preset",
            preset: "4vcpu-16gb",
          },
        }),
        filesystems: [
          AttachedFilesystemSpec.create({
            attachMode: AttachedFilesystemSpec_AttachMode.READ_WRITE,
            mountTag: "csi-storage",
            type: {
              $case: "existingFilesystem",
              existingFilesystem: ExistingFilesystem.create({
                id: "<filesystem_ID>",
              }),
            },
          }),
        ],
        cloudInitUserData: userData,
      }),
    }),
  }),
).result;
await nodeGroupOperation.wait();
```

This mounts the filesystem to nodes at `/mnt/data` as `csi-storage`. To use another mount point or mount tag, modify `userData` and `mountTag`.

### Install the CSI driver

1. Pull the driver's Helm chart:

   ```bash theme={null}
   helm pull \
     oci://cr.eu-north1.nebius.cloud/mk8s/helm/csi-mounted-fs-path \
     --version 0.1.10
   ```

2. Install the chart:

   ```bash theme={null}
   helm upgrade csi-mounted-fs-path ./csi-mounted-fs-path-0.1.10.tgz --install \
     --set dataDir=$MOUNT_POINT/csi-mounted-fs-path-data/
   ```

   `$MOUNT_POINT` is the mount point that you configured for the nodes. If you created the node group with an SDK, substitute the path itself, for example `/mnt/data`.

   The chart creates the `csi-mounted-fs-path-sc` `StorageClass`. By default, this `StorageClass` uses the `WaitForFirstConsumer` [volume binding mode](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode), which delays volume provisioning until a Pod uses the `PersistentVolumeClaim`. To provision a volume as soon as the `PersistentVolumeClaim` is created, add `--set storageClass.volumeBindingMode=Immediate` to the installation command.

### Mount the filesystem to Pods

Here is an example of a `PersistentVolumeClaim` that claims space on the shared filesystem, and a Pod that mounts the filesystem at `/data` through the `PersistentVolumeClaim`:

```yaml theme={null}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: csi-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-mounted-fs-path-sc
---
kind: Pod
apiVersion: v1
metadata:
  name: my-csi-app
spec:
  containers:
  - name: my-csi-app
    image: busybox
    volumeMounts:
      - mountPath: "/data"
        name: my-csi-volume
    command: [ "sleep", "1000000" ]
    securityContext:
      allowPrivilegeEscalation: false
      privileged: false
  volumes:
  - name: my-csi-volume
    persistentVolumeClaim:
      claimName: csi-pvc
```

## How to use several shared filesystems

One CSI driver installation supports multiple shared filesystems, each with its own `StorageClass`. Before configuring the chart, make sure that each filesystem is attached to the node group and mounted on every node that can run the driver.

1. Repeat [Create a shared filesystem](#create-a-shared-filesystem) for each filesystem that you want to use. When [creating the node group](#create-a-node-group-and-mount-the-filesystem-to-nodes), add one filesystem attachment and one mount command for each filesystem. Use distinct mount tags and mount points.

2. Create `values.yaml`. For each additional filesystem, add an entry to both `additionalStoragePools` and `additionalStorageClasses`, following this example:

   ```yaml theme={null}
   dataDir: /mnt/data/csi-mounted-fs-path-data/
   additionalStoragePools:
     - name: fs-2
       hostPath: /mnt/fs-2/csi-mounted-fs-path-data/
   additionalStorageClasses:
     - name: fs-2-sc
       storagePool: fs-2
   ```

   In `hostPath`, specify the filesystem mount point on the nodes, followed by `/csi-mounted-fs-path-data/`. The `storagePool` value must match the corresponding pool `name`. If upgrading, preserve the existing `dataDir` value.

   Renaming a pool or changing its path can make existing volumes inaccessible.

3. Install or upgrade the chart with the values file:

   ```bash theme={null}
   helm upgrade csi-mounted-fs-path ./csi-mounted-fs-path-0.1.10.tgz --install \
     --values values.yaml
   ```

4. In each `PersistentVolumeClaim`, set `storageClassName` to the filesystem's `StorageClass`, such as `fs-2-sc`.

## How to delete the created resources

Some of the created resources are chargeable. If you do not need them, delete these resources, so Nebius AI Cloud does not charge for them:

1. Delete the node group:

   **Web console**

   1. In the sidebar, go to  **Compute** → **Kubernetes**.
   2. Open the page of the required cluster and then go to the **Node groups** tab.
   3. In the row of the required node group, click  → **Delete**.
   4. Confirm the node group deletion.

   **CLI**

   1. Get the ID of the node group that you want to delete:

      ```bash theme={null}
      nebius mk8s node-group list --parent-id <cluster_ID>
      ```

   2. Delete the node group:

      ```bash theme={null}
      nebius mk8s node-group delete --id <node_group_ID>
      ```

   **Go SDK**

   1. Get the ID of the node group that you want to delete:

      ```go theme={null}
      nodeGroupService := sdk.Services().MK8S().V1().NodeGroup()
      nodeGroups, err := nodeGroupService.List(
          ctx,
          &mk8s.ListNodeGroupsRequest{
              ParentId: "<cluster_ID>",
          },
      )
      if err != nil {
          return err
      }
      fmt.Println(nodeGroups)
      ```

   2. Delete the node group:

      ```go theme={null}
      deleteNodeGroupOperation, err := sdk.Services().MK8S().V1().
          NodeGroup().Delete(
              ctx,
              &mk8s.DeleteNodeGroupRequest{
                  Id: "<node_group_ID>",
              },
          )
      if err != nil {
          return err
      }
      if _, err = deleteNodeGroupOperation.Wait(ctx); err != nil {
          return err
      }
      ```

   **Python SDK**

   1. Get the ID of the node group that you want to delete:

      ```python theme={null}
      node_group_service = NodeGroupServiceClient(sdk)
      node_groups = await node_group_service.list(
          ListNodeGroupsRequest(parent_id="<cluster_ID>"),
      )
      print(node_groups)
      ```

   2. Delete the node group:

      ```python theme={null}
      node_group_service = NodeGroupServiceClient(sdk)
      delete_node_group_operation = await node_group_service.delete(
          DeleteNodeGroupRequest(id="<node_group_ID>"),
      )
      await delete_node_group_operation.wait()
      ```

   **JavaScript SDK**

   1. Get the ID of the node group that you want to delete:

      ```ts theme={null}
      const nodeGroupListService = new NodeGroupService(sdk);
      const nodeGroups = await nodeGroupListService.list(
        ListNodeGroupsRequest.create({
          parentId: "<cluster_ID>",
        }),
      );
      console.log(nodeGroups);
      ```

   2. Delete the node group:

      ```ts theme={null}
      const nodeGroupDeleteService = new NodeGroupService(sdk);
      const deleteNodeGroupOperation =
        await nodeGroupDeleteService.delete(
          DeleteNodeGroupRequest.create({
            id: "<node_group_ID>",
          }),
        ).result;
      await deleteNodeGroupOperation.wait();
      ```

2. Delete the Compute shared filesystem:

   **Web console**

   1. In the sidebar, go to  **Storage** → **Shared filesystems**.
   2. Next to the filesystem's name, click  → **Delete**.
   3. Enter the filesystem's name and confirm deletion.

   **CLI**

   ```bash theme={null}
   nebius compute filesystem delete --id <filesystem_ID>
   ```

   **Go SDK**

   ```go theme={null}
   deleteFilesystemOperation, err := sdk.Services().Compute().
       V1().Filesystem().Delete(
           ctx,
           &compute.DeleteFilesystemRequest{
               Id: "<filesystem_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = deleteFilesystemOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   **Python SDK**

   ```python theme={null}
   filesystem_service = FilesystemServiceClient(sdk)
   delete_filesystem_operation = await filesystem_service.delete(
       DeleteFilesystemRequest(id="<filesystem_ID>"),
   )
   await delete_filesystem_operation.wait()
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const filesystemDeleteService = new FilesystemService(sdk);
   const deleteFilesystemOperation =
     await filesystemDeleteService.delete(
       DeleteFilesystemRequest.create({
         id: "<filesystem_ID>",
       }),
     ).result;
   await deleteFilesystemOperation.wait();
   ```

## See also

* [Mounting disks to Pods in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/storage/disk-over-csi.md)
* [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md)
