# Moving workload from the existing node group

Source: https://docs.nebius.com/kubernetes/node-groups/moving-workload

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Moving workload from the existing node group

The workload is moved automatically after you evict it from the existing node group.

Before moving your workload, you need to:

1. Install [jq](https://jqlang.github.io/jq/download/) if you don't have it on your system:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

2. [Get your cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) which is returned in the `.metadata.id` field of the cluster resource.

The examples in this guide assume that the cluster ID is saved to the `K8S_CLUSTER_ID` environment variable for the CLI or to the `k8sClusterID`, `k8s_cluster_id` or `k8sClusterId` variable for the Go, Python or JavaScript SDK.

To move your workload:

1. [Create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups).

   > For example, the following command creates a group of two nodes, each with one NVIDIA H100 GPU, and all drivers and components required for the GPU:
   >
   > ```bash theme={null}
   > nebius mk8s node-group create \
   >   --parent-id $K8S_CLUSTER_ID \
   >   --name mk8s-node-group-test \
   >   --fixed-node-count 2 \
   >   --template-resources-platform gpu-h100-sxm \
   >   --template-resources-preset 1gpu-16vcpu-200gb \
   >   --template-gpu-settings-drivers-preset cuda12
   > ```

2. Save the ID of the node group from which you want to move the workload. For example, you can get it by the node group's name (if you have set and know it) and the parent cluster's ID:

   **CLI**

   ```bash theme={null}
   export K8S_NODE_GROUP_ID=$(nebius mk8s node-group get-by-name \
     --parent-id $K8S_CLUSTER_ID \
     --name node-group-name \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   lookupService := sdk.Services().MK8S().V1().NodeGroup()
   oldNodeGroup, err := lookupService.GetByName(
       ctx,
       &common.GetByNameRequest{
           ParentId: k8sClusterID,
           Name:     oldNodeGroupName,
       },
   )
   if err != nil {
       return err
   }
   oldNodeGroupID := oldNodeGroup.GetMetadata().GetId()
   if oldNodeGroupID == "" {
       return errors.New("node group ID is missing")
   }
   ```

   Assign the node group name to the `oldNodeGroupName` variable before you run the code.

   **Python SDK**

   ```python theme={null}
   lookup_service = NodeGroupServiceClient(sdk)
   old_node_group = await lookup_service.get_by_name(
       GetByNameRequest(
           parent_id=k8s_cluster_id,
           name=old_node_group_name,
       ),
   )
   old_node_group_id = old_node_group.metadata.id
   if not old_node_group_id:
       raise ValueError("node group ID is missing")
   ```

   Assign the node group name to the `old_node_group_name` variable before you run the code.

   **JavaScript SDK**

   ```ts theme={null}
   const lookupService = new NodeGroupService(sdk);
   const oldNodeGroup = await lookupService.getByName(
     GetByNameRequest.create({
       parentId: k8sClusterId,
       name: oldNodeGroupName,
     }),
   );
   const oldNodeGroupId = oldNodeGroup.metadata?.id;
   if (!oldNodeGroupId) {
     throw new Error("node group ID is missing");
   }
   ```

   Assign the node group name to the `oldNodeGroupName` variable before you run the code.

3. Get the list of node names in the node group from which you want to move the workload:

   ```sh theme={null}
   export OLD_NODES=$(kubectl get nodes -o json \
     | jq '.items[].metadata
       | select(.annotations."cluster.x-k8s.io/owner-name" = "$K8S_NODE_GROUP_ID")
       | .name')
   ```

4. Cordon off the old nodes so that no new Pods are scheduled on them:

   ```sh theme={null}
   for node in $OLD_NODES; do
     kubectl cordon $node;
   done
   ```

5. Drain the old nodes so that the existing Pods can be evicted from them:

   ```sh theme={null}
   for node in $OLD_NODES; do
     kubectl drain --force --ignore-daemonsets --delete-emptydir-data $node;
   done
   ```

   Kubernetes will automatically move evicted Pods to suitable nodes.

6. Delete the old node group:

   **CLI**

   ```bash theme={null}
   nebius mk8s node-group delete --id $K8S_NODE_GROUP_ID
   ```

   **Go SDK**

   ```go theme={null}
   deleteService := sdk.Services().MK8S().V1().NodeGroup()
   deleteOperation, err := deleteService.Delete(
       ctx,
       &mk8s.DeleteNodeGroupRequest{Id: oldNodeGroupID},
   )
   if err != nil {
       return err
   }
   if _, err = deleteOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   **Python SDK**

   ```python theme={null}
   delete_service = NodeGroupServiceClient(sdk)
   delete_operation = await delete_service.delete(
       DeleteNodeGroupRequest(id=old_node_group_id),
   )
   await delete_operation.wait()
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const deleteService = new NodeGroupService(sdk);
   const deleteOperation = await deleteService.delete(
     DeleteNodeGroupRequest.create({
       id: oldNodeGroupId,
     }),
   ).result;
   await deleteOperation.wait();
   ```
