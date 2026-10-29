# Setting and upgrading Kubernetes® versions in Managed Service for Kubernetes

Source: https://docs.nebius.com/kubernetes/manage-versions

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Setting and upgrading Kubernetes® versions in Managed Service for Kubernetes

You can set the [Kubernetes version](https://kubernetes.io/releases/) that is used on your Managed Kubernetes clusters and node groups during creation. For existing clusters and node groups, you can upgrade the version.

For more information about available versions and the upgrade, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

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

## How to set a Kubernetes version

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.
2. Click  **Create cluster**.
3. In the **Control plane** section, select the Kubernetes version from the drop-down list.

> [!NOTE]
>
> It is not currently possible to set a Kubernetes version for a node group in the web console.

**CLI**

Use the following parameters:

* For clusters ([nebius mk8s cluster create](https://docs.nebius.com/cli/reference/mk8s/cluster/create.md)):

  ```sh theme={null}
  --control-plane-version <major.minor>
  ```

* For node groups ([nebius mk8s node-group create](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md)):

  ```sh theme={null}
  --version <major.minor>
  ```

  > [!WARNING]
  >
  > The Kubernetes version for a node group must not be higher than for the control plane.

**Go SDK**

Set the following parameters when creating a [cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) or [node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

* For clusters, in `mk8s.CreateClusterRequest`, set `Spec.ControlPlane.Version` to `<major.minor>`.
* For node groups, in `mk8s.CreateNodeGroupRequest`, set `Spec.Version` to `<major.minor>`.

  > [!WARNING]
  >
  > The Kubernetes version for a node group must not be higher than for the control plane.

**Python SDK**

Set the following parameters when creating a [cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) or [node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

* For clusters, in `CreateClusterRequest`, set `spec.control_plane.version` to `<major.minor>`.
* For node groups, in `CreateNodeGroupRequest`, set `spec.version` to `<major.minor>`.

  > [!WARNING]
  >
  > The Kubernetes version for a node group must not be higher than for the control plane.

**JavaScript SDK**

Set the following parameters when creating a [cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) or [node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

* For clusters, in `CreateClusterRequest`, set `spec.controlPlane.version` to `<major.minor>`.
* For node groups, in `CreateNodeGroupRequest`, set `spec.version` to `<major.minor>`.

  > [!WARNING]
  >
  > The Kubernetes version for a node group must not be higher than for the control plane.

## How to upgrade a Kubernetes version

To upgrade a Managed Kubernetes cluster to a new version, upgrade the control plane first and then the node groups.

> [!NOTE]
>
> The Kubernetes version for a node group must not be higher than for the control plane.

**CLI**

1. Get the ID of the cluster:

   ```bash theme={null}
   nebius mk8s cluster get-by-name \
     --name <cluster_name> --format jsonpath='{.metadata.id}'
   ```

2. Upgrade the control plane:

   ```bash theme={null}
   nebius mk8s cluster update \
     --id <cluster_ID> \
     --control-plane-version <major.minor>
   ```

3. After the upgrade is completed, get the ID of the node group:

   ```bash theme={null}
   nebius mk8s node-group get-by-name \
     --parent-id <cluster_ID> \
     --name <node_group_name> --format jsonpath='{.metadata.id}'
   ```

4. Upgrade the node group:

   ```bash theme={null}
   nebius mk8s node-group update \
     --id <node_group_ID> \
     --auto-approve \
     --version <major.minor>
   ```

**Go SDK**

1. Get the ID of the cluster:

   ```go theme={null}
   clusterByName, err := sdk.Services().MK8S().V1().
       Cluster().GetByName(
           ctx,
           &common.GetByNameRequest{
               Name: "<cluster_name>",
           },
       )
   if err != nil {
       return err
   }
   clusterByNameID := clusterByName.GetMetadata().GetId()
   if clusterByNameID == "" {
       return errors.New("cluster ID is missing")
   }
   fmt.Println(clusterByNameID)
   ```

2. Upgrade the control plane. Set the new version in `Spec.ControlPlane.Version`:

   ```go theme={null}
   cluster, err := sdk.Services().MK8S().V1().
       Cluster().Get(
           ctx,
           &mk8s.GetClusterRequest{
               Id: "<cluster_ID>",
           },
       )
   if err != nil {
       return err
   }
   clusterSpec := cluster.GetSpec()
   if clusterSpec == nil || clusterSpec.GetControlPlane() == nil {
       return errors.New("cluster control plane spec is missing")
   }
   clusterSpec.GetControlPlane().Version = "<major.minor>"
   clusterOperation, err := sdk.Services().MK8S().V1().
       Cluster().Update(
           ctx,
           &mk8s.UpdateClusterRequest{
               Metadata: cluster.GetMetadata(),
               Spec:     clusterSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = clusterOperation.Wait(ctx); err != nil {
       return err
   }
   ```

3. After the upgrade is completed, get the ID of the node group:

   ```go theme={null}
   nodeGroupByName, err := sdk.Services().MK8S().V1().
       NodeGroup().GetByName(
           ctx,
           &common.GetByNameRequest{
               ParentId: "<cluster_ID>",
               Name:     "<node_group_name>",
           },
       )
   if err != nil {
       return err
   }
   nodeGroupByNameID := nodeGroupByName.GetMetadata().GetId()
   if nodeGroupByNameID == "" {
       return errors.New("node group ID is missing")
   }
   fmt.Println(nodeGroupByNameID)
   ```

4. Upgrade the node group. Set the new version in `Spec.Version`:

   ```go theme={null}
   nodeGroup, err := sdk.Services().MK8S().V1().
       NodeGroup().Get(
           ctx,
           &mk8s.GetNodeGroupRequest{
               Id: "<node_group_ID>",
           },
       )
   if err != nil {
       return err
   }
   nodeGroupSpec := nodeGroup.GetSpec()
   if nodeGroupSpec == nil {
       return errors.New("node group spec is missing")
   }
   nodeGroupSpec.Version = "<major.minor>"
   nodeGroupOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Update(
           ctx,
           &mk8s.UpdateNodeGroupRequest{
               Metadata: nodeGroup.GetMetadata(),
               Spec:     nodeGroupSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = nodeGroupOperation.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the ID of the cluster:

   ```python theme={null}
   cluster_service = ClusterServiceClient(sdk)
   cluster_by_name = await cluster_service.get_by_name(
       GetByNameRequest(name="<cluster_name>"),
   )
   cluster_by_name_id = cluster_by_name.metadata.id
   print(cluster_by_name_id)
   ```

2. Upgrade the control plane. Set the new version in `spec.control_plane.version`:

   ```python theme={null}
   cluster_service = ClusterServiceClient(sdk)
   cluster = await cluster_service.get(
       GetClusterRequest(id="<cluster_ID>"),
   )
   if cluster.spec is None or cluster.spec.control_plane is None:
       raise ValueError("cluster control plane spec is missing")
   cluster.spec.control_plane.version = "<major.minor>"
   cluster_operation = await cluster_service.update(
       UpdateClusterRequest(
           metadata=cluster.metadata,
           spec=cluster.spec,
       ),
   )
   await cluster_operation.wait()
   ```

3. After the upgrade is completed, get the ID of the node group:

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group_by_name = await node_group_service.get_by_name(
       GetByNameRequest(
           parent_id="<cluster_ID>",
           name="<node_group_name>",
       ),
   )
   node_group_by_name_id = node_group_by_name.metadata.id
   print(node_group_by_name_id)
   ```

4. Upgrade the node group. Set the new version in `spec.version`:

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group = await node_group_service.get(
       GetNodeGroupRequest(id="<node_group_ID>"),
   )
   if node_group.spec is None:
       raise ValueError("node group spec is missing")
   node_group.spec.version = "<major.minor>"
   node_group_operation = await node_group_service.update(
       UpdateNodeGroupRequest(
           metadata=node_group.metadata,
           spec=node_group.spec,
       ),
   )
   await node_group_operation.wait()
   ```

**JavaScript SDK**

1. Get the ID of the cluster:

   ```ts theme={null}
   const clusterLookupService = new ClusterService(sdk);
   const clusterByName = await clusterLookupService.getByName(
     GetByNameRequest.create({
       name: "<cluster_name>",
     }),
   );
   const clusterByNameId = clusterByName.metadata?.id;
   if (!clusterByNameId) {
     throw new Error("cluster ID is missing");
   }
   console.log(clusterByNameId);
   ```

2. Upgrade the control plane. Set the new version in `spec.controlPlane.version`:

   ```ts theme={null}
   const clusterService = new ClusterService(sdk);
   const cluster = await clusterService.get(
     GetClusterRequest.create({
       id: "<cluster_ID>",
     }),
   );
   if (!cluster.spec?.controlPlane) {
     throw new Error("cluster control plane spec is missing");
   }
   cluster.spec.controlPlane.version = "<major.minor>";
   const clusterOperation = await clusterService.update(
     UpdateClusterRequest.create({
       metadata: cluster.metadata,
       spec: cluster.spec,
     }),
   ).result;
   await clusterOperation.wait();
   ```

3. After the upgrade is completed, get the ID of the node group:

   ```ts theme={null}
   const nodeGroupLookupService = new NodeGroupService(sdk);
   const nodeGroupByName = await nodeGroupLookupService.getByName(
     GetByNameRequest.create({
       parentId: "<cluster_ID>",
       name: "<node_group_name>",
     }),
   );
   const nodeGroupByNameId = nodeGroupByName.metadata?.id;
   if (!nodeGroupByNameId) {
     throw new Error("node group ID is missing");
   }
   console.log(nodeGroupByNameId);
   ```

4. Upgrade the node group. Set the new version in `spec.version`:

   ```ts theme={null}
   const nodeGroupService = new NodeGroupService(sdk);
   const nodeGroup = await nodeGroupService.get(
     GetNodeGroupRequest.create({
       id: "<node_group_ID>",
     }),
   );
   if (!nodeGroup.spec) {
     throw new Error("node group spec is missing");
   }
   nodeGroup.spec.version = "<major.minor>";
   const nodeGroupOperation = await nodeGroupService.update(
     UpdateNodeGroupRequest.create({
       metadata: nodeGroup.metadata,
       spec: nodeGroup.spec,
     }),
   ).result;
   await nodeGroupOperation.wait();
   ```
