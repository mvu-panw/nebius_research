# Mounting disks to Pods in a Managed Service for Kubernetes® cluster

Source: https://docs.nebius.com/kubernetes/storage/disk-over-csi

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Mounting disks to Pods in a Managed Service for Kubernetes® cluster

Nebius AI Cloud offers persistent storage for Pods in Managed Service for Kubernetes clusters. In this tutorial, you will mount a Compute disk as a persistent volume to a Pod in your cluster.

## Background

By default, files created or modified by a container in a Kubernetes Pod are lost when the container crashes, or is stopped or restarted. [Persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) help you avoid this: they keep the files for the lifetime of the Pod, regardless of the states of its individual containers to the Pod. These volumes are mounted to a node that is running the Pod.

In Nebius AI Cloud, Managed Service for Kubernetes offers a native solution for persistent volumes in your clusters. You can mount disks from another Nebius AI Cloud service, Compute, to your Pods as persistent volumes. Compute provides multiple disk types that vary in performance, reliability and price, and you can choose between them depending on your use case. For more details, see the [Compute documentation](https://docs.nebius.com/compute/storage/types.md#disks).

Mounting disks to Pods relies on support for Container Storage Interface (CSI), which is enabled on newer Managed Kubernetes clusters and can be enabled for older clusters (see prerequisites below).

A disk can be used on one node at a time. If you need to share data between Pods and nodes, use Compute shared filesystems instead of disks. See [Mounting shared filesystems to Pods in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md) for details.

## Costs

Nebius AI Cloud only charges for a Compute disk. For more details, see the [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md#disks).

## Prerequisites

1. [Create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) or choose an existing one.
2. If you are working with an existing cluster, [verify that it supports CSI](#verify-that-your-cluster-supports-csi).
3. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [connect to the cluster](https://docs.nebius.com/kubernetes/connect.md).

[Nebius AI Cloud disks](https://docs.nebius.com/compute/storage/types.md#disks) are created automatically; you do not need to create them beforehand.

### Verify that your cluster supports CSI

If your Managed Kubernetes cluster was created on or after January 7, 2025, it already supports CSI and no additional configuration is required. Proceed to the tutorial's [steps](#steps).

If your cluster was created before January 7, 2025, enable CSI support in it:

> **How to enable CSI support**
>
> 1. Get IDs of the node groups in the cluster:
>
>    **Web console**
>
>    1. In [Managed Kubernetes](https://console.nebius.com/mk8s), open your cluster.
>    2. Switch to the **Node groups** tab.
>    3. For each node group, find its ID under its name and click  to copy it.
>
>    **CLI**
>
>    1. Get the cluster ID. List all clusters:
>
>       ```bash theme={null}
>       nebius mk8s cluster list
>       ```
>
>       Alternatively, look the cluster up by name:
>
>       ```bash theme={null}
>       nebius mk8s cluster get-by-name --name <cluster_name>
>       ```
>
>       The cluster ID is returned in `.metadata.id`.
>
>    2. Get the list of the cluster's node groups, by using the cluster ID as parent ID:
>
>       ```bash theme={null}
>       nebius mk8s node-group list --parent-id <cluster_ID>
>       ```
>
>       The IDs of the node groups are returned in the `.metadata.id` fields.
>
>    **Go SDK**
>
>    1. Get the cluster ID. List all clusters:
>
>       ```go theme={null}
>       clusterService := sdk.Services().MK8S().V1().Cluster()
>       clusters, err := clusterService.List(
>           ctx,
>           &mk8s.ListClustersRequest{},
>       )
>       if err != nil {
>           return err
>       }
>       fmt.Println(clusters)
>       ```
>
>       Alternatively, look the cluster up by name:
>
>       ```go theme={null}
>       clusterLookupService := sdk.Services().MK8S().V1().Cluster()
>       cluster, err := clusterLookupService.GetByName(
>           ctx,
>           &common.GetByNameRequest{
>               Name: "<cluster_name>",
>           },
>       )
>       if err != nil {
>           return err
>       }
>       fmt.Println(cluster)
>       ```
>
>       The cluster ID is returned in `Metadata.Id`.
>
>    2. Get the list of the cluster's node groups, by using the cluster ID as `ParentId`:
>
>       ```go theme={null}
>       nodeGroupService := sdk.Services().MK8S().V1().NodeGroup()
>       nodeGroups, err := nodeGroupService.List(
>           ctx,
>           &mk8s.ListNodeGroupsRequest{
>               ParentId: "<cluster_ID>",
>           },
>       )
>       if err != nil {
>           return err
>       }
>       fmt.Println(nodeGroups)
>       ```
>
>       The IDs of the node groups are returned in `Metadata.Id`.
>
>    **Python SDK**
>
>    1. Get the cluster ID. List all clusters:
>
>       ```python theme={null}
>       cluster_service = ClusterServiceClient(sdk)
>       clusters = await cluster_service.list(ListClustersRequest())
>       print(clusters)
>       ```
>
>       Alternatively, look the cluster up by name:
>
>       ```python theme={null}
>       cluster_service = ClusterServiceClient(sdk)
>       cluster = await cluster_service.get_by_name(
>           GetByNameRequest(name="<cluster_name>"),
>       )
>       print(cluster)
>       ```
>
>       The cluster ID is returned in `metadata.id`.
>
>    2. Get the list of the cluster's node groups, by using the cluster ID as `parent_id`:
>
>       ```python theme={null}
>       node_group_service = NodeGroupServiceClient(sdk)
>       node_groups = await node_group_service.list(
>           ListNodeGroupsRequest(parent_id="<cluster_ID>"),
>       )
>       print(node_groups)
>       ```
>
>       The IDs of the node groups are returned in `metadata.id`.
>
>    **JavaScript SDK**
>
>    1. Get the cluster ID. List all clusters:
>
>       ```ts theme={null}
>       const clusterService = new ClusterService(sdk);
>       const clusters = await clusterService.list(
>         ListClustersRequest.create({}),
>       );
>       console.log(clusters);
>       ```
>
>       Alternatively, look the cluster up by name:
>
>       ```ts theme={null}
>       const clusterLookupService = new ClusterService(sdk);
>       const cluster = await clusterLookupService.getByName(
>         GetByNameRequest.create({
>           name: "<cluster_name>",
>         }),
>       );
>       console.log(cluster);
>       ```
>
>       The cluster ID is returned in `metadata.id`.
>
>    2. Get the list of the cluster's node groups, by using the cluster ID as `parentId`:
>
>       ```ts theme={null}
>       const nodeGroupService = new NodeGroupService(sdk);
>       const nodeGroups = await nodeGroupService.list(
>         ListNodeGroupsRequest.create({
>           parentId: "<cluster_ID>",
>         }),
>       );
>       console.log(nodeGroups);
>       ```
>
>       The IDs of the node groups are returned in `metadata.id`.
>
> 2. Upgrade each node group:
>
>    **CLI**
>
>    ```bash theme={null}
>    nebius mk8s node-group upgrade --id <node_group_ID> --latest-infra-version
>    ```
>
>    **Go SDK**
>
>    ```go theme={null}
>    upgradeOperation, err := sdk.Services().MK8S().V1().
>        NodeGroup().Upgrade(
>            ctx,
>            &mk8s.UpgradeNodeGroupRequest{
>                Id:                 "<node_group_ID>",
>                LatestInfraVersion: &emptypb.Empty{},
>            },
>        )
>    if err != nil {
>        return err
>    }
>    if _, err = upgradeOperation.Wait(ctx); err != nil {
>        return err
>    }
>    ```
>
>    **Python SDK**
>
>    ```python theme={null}
>    node_group_service = NodeGroupServiceClient(sdk)
>    upgrade_operation = await node_group_service.upgrade(
>        UpgradeNodeGroupRequest(
>            id="<node_group_ID>",
>            latest_infra_version=Empty(),
>        ),
>    )
>    await upgrade_operation.wait()
>    ```
>
>    **JavaScript SDK**
>
>    ```ts theme={null}
>    const nodeGroupUpgradeService = new NodeGroupService(sdk);
>    const upgradeOperation = await nodeGroupUpgradeService.upgrade(
>      UpgradeNodeGroupRequest.create({
>        id: "<node_group_ID>",
>        latestInfraVersion: {},
>      }),
>    ).result;
>    await upgradeOperation.wait();
>    ```
>
> 3. [Contact support](https://console.nebius.com/support) or your solution architect to enable CSI support.

## Steps

### Create a storage class for custom provisioning (optional)

Before using Compute disks as persistent volumes, you can choose how disks are provisioned: the [disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks), the filesystem type (ext4 or xfs) and when a disk should be created (together with a persistent volume claim or when the claim is used by a Pod). To do this, define a custom Kubernetes storage class.

> [!NOTE]
>
> The default storage class offered by Managed Kubernetes, `compute-csi-default-sc`, creates a [Network SSD disk](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks) with an ext4 filesystem, and does so when a Pod that uses a persistent volume claim with this storage class is created. If this configuration suits you, you can skip this step and proceed to [creating a persistent volume claim](#create-a-persistent-volume-claim).

To create a custom storage class:

1. Create a manifest, for example `storage-class.yaml`, that defines the storage class. For example:

   ```yaml theme={null}
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: storage-test-class
   provisioner: compute.csi.nebius.com
   volumeBindingMode: WaitForFirstConsumer
   parameters:
     csi.storage.k8s.io/fstype: xfs
     type: "NETWORK_SSD_IO_M3"
     disk_block_size_bytes: "4096"
     encrypted: "true"
   ```

   * `.metadata.name` — The name of the storage class. Use it when referring to the class in [persistent volume claims](#create-a-persistent-volume-claim) (`.spec.storageClassName`).

   * `.provisioner` — The volume [provisioner](https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner). For Nebius AI Cloud disks, the provisioner is `compute.csi.nebius.com`.

   * `.volumeBindingMode` — The [volume binding mode](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) that determines when a Nebius AI Cloud disk is created for a persistent volume claim of this storage class. Supported values are `WaitForFirstConsumer` (the disk is created together with a Pod that uses the claim) or `Immediate` (the disk is created together with the claim, even if no Pods use it yet).

     > [!TIP]
     >
     > Disks created in the `Immediate` binding mode may start to be [charged](https://docs.nebius.com/compute/resources/pricing.md#disks) and to count towards [quotas](https://docs.nebius.com/compute/resources/quotas-limits.md#storage) before being actually used in Pods. To avoid this, use the `WaitForFirstConsumer` binding mode.

   * `.parameters."csi.storage.k8s.io/fstype"` — The filesystem for disks: `ext4` or `xfs`.

   * `.parameters.type` — The Nebius AI Cloud disk type. See the [list of network disk types and their IDs](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks). Write IDs in uppercase, for example, `NETWORK_SSD`, `NETWORK_SSD_IO_M3`.

   * `.parameters.disk_block_size_bytes` — The [block size](https://docs.nebius.com/compute/storage/manage.md#type-encryption-and-size) of disks, in bytes. The value must be a power of two between `"4096"` (default) and `"131072"`. The block size cannot be changed after the disk is created. With the default block size, a disk cannot exceed 16 TiB. For larger disks, set a larger block size.

   * `.parameters.encrypted` — Whether to enable [encryption](https://docs.nebius.com/compute/storage/types.md#encryption-of-disks) for disks: `"true"` or `"false"` (default). Set this parameter to `"true"` only for `NETWORK_SSD_NON_REPLICATED` and `NETWORK_SSD_IO_M3` disks. `NETWORK_SSD` disks are always encrypted, and setting `encrypted: "true"` for them causes disk provisioning to fail.

2. Apply the manifest to your cluster:

   ```bash theme={null}
   kubectl apply -f storage-class.yaml
   ```

### Create a persistent volume claim

Persistent volume claims are requests that Pods make for persistent volumes. These requests include what kind of storage should be provided (in our case, a Compute disk with the default or a custom storage class) and how large it should be.

To create a persistent volume claim:

1. Create a manifest, for example `pvc.yaml`, that defines the claim. For example:

   ```yaml theme={null}
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: storage-test-claim
   spec:
     accessModes:
       - ReadWriteOnce
     storageClassName: compute-csi-default-sc
     resources:
       requests:
         storage: 4Gi
   ```

   * `.metadata.name` — The name of your claim. Use it when referring to the claim in Pod configurations.
   * `.spec.accessModes` — An array of [access modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) that determine how the persistent volume can be mounted to nodes. The only mode supported for Nebius AI Cloud block storage is `ReadWriteOnce`; the volume can be mounted as read-write by a single node. For storage that can be mounted to multiple nodes (`ReadWriteMany`), see [Mounting shared filesystems to Pods in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md).
   * `.spec.storageClassName` — The [storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) of the volume. The default storage class for Nebius AI Cloud block storage, `compute-csi-default-sc`, creates a [Network SSD disk](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks) with an ext4 filesystem. To use another disk type or filesystem, [create a custom storage class](#create-a-storage-class-for-custom-provisioning-optional) by using the Nebius AI Cloud provisioner and specify its name here.
   * `.spec.resources.requests.storage` — The volume size.

2. Apply the manifest to your cluster:

   ```bash theme={null}
   kubectl apply -f pvc.yaml
   ```

### Mount a volume to a Pod and test it

When a persistent volume claim is used in a Pod's specification, the Compute disk created for the claim is mounted to the Pod as a persistent volume.

> [!WARNING]
>
> A disk created for a claim is mounted to each Pod that uses the claim, and is deleted together with the claim. Do not use a claim on multiple Pods at one time, as a disk can only be mounted to a single node. For a solution that shares storage between nodes, see [Mounting shared filesystems to Pods in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md).

To create a Pod with a volume and test it:

1. Create a manifest, for example `pod.yaml`, that defines the Pod. For example, in the manifest below, a volume named `persistent-storage`, created from the `test-claim` persistent volume claim, is mounted to the Pod's container at `/data`:

   ```yaml theme={null}
   apiVersion: v1
   kind: Pod
   metadata:
     name: storage-test-app
   spec:
     volumes:
       - name: persistent-storage
         persistentVolumeClaim:
           claimName: storage-test-claim
     containers:
       - name: app
         image: centos
         command: ["/bin/sh"]
         args: ["-c", "while true; do echo $(date -u) >> /data/out.txt; sleep 5; done"]
         volumeMounts:
           - name: persistent-storage
             mountPath: /data
   ```

   * `.spec.volumes[0].name`: The name of the volume that is created for the Pod.
   * `.spec.volumes[0].persistentVolumeClaim.claimName`: The name of the persistent volume claim that is used to create a volume.
   * `.spec.containers[0].volumeMounts[0].name`: The same volume name as in `.spec.volumes[0].name`.
   * `.spec.containers[0].volumeMounts[0].mountPath`: The mount point for the volume.

   > [!NOTE]
   >
   > You can configure volumes in Kubernetes resources that manage Pods, like [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) or [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/), in the same way, by using sub-fields of `.spec.template.spec.volumes` and `.spec.template.spec.containers`.

2. Apply the manifest to your cluster:

   ```bash theme={null}
   kubectl apply -f pod.yaml
   ```

3. Wait until the Pod is ready:

   ```bash theme={null}
   kubectl wait --for condition=Ready=true pod/storage-test-app
   ```

4. Test that the container has written into `/data/out.txt`:

   ```bash theme={null}
   kubectl exec storage-test-app -- cat /data/out.txt
   ```

## How to delete the created resources

The created Compute disk is chargeable. If you do not need it, delete the Pod and the persistent volume claim, so that the disk is deleted and Nebius AI Cloud does not charge for it:

```bash theme={null}
kubectl delete pod/storage-test-app pvc/storage-test-claim
```

## See also

* [Mounting shared filesystems to Pods in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md)
* [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md)
