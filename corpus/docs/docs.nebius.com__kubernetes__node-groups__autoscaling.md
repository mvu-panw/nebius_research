# Autoscaling in Managed Service for Kubernetes

Source: https://docs.nebius.com/kubernetes/node-groups/autoscaling

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Autoscaling in Managed Service for Kubernetes

In Managed Service for Kubernetes, the **cluster autoscaler** integrates with the underlying infrastructure to monitor and manage [node groups](https://docs.nebius.com/kubernetes/components.md#node-group) in your cluster, to add or remove nodes seamlessly as needed. It makes scaling decisions based on the following principles:

* If there are unschedulable Pods in the cluster due to resource constraints, the cluster autoscaler adds new nodes to accommodate these Pods.
* If nodes in the cluster are underutilized, the cluster autoscaler removes these nodes in order to optimize resource usage and reduce costs.

> [!TIP]
>
> If you have a GPU node group with autoscaling, add a CPU node group with at least two nodes (or with autoscaling) to the cluster. In this case, when there are no tasks to perform, [CoreDNS and Cilium networking add-ons](https://docs.nebius.com/kubernetes/networking/add-ons.md) can run on CPU nodes, so that the GPU node group can scale down and reduce your costs.

## Set up autoscaling for new node groups

You can set up autoscaling when creating a new node group:

**Web console**

When [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

1. Under **Size**, select **Enable autoscaling**.

2. Specify the **Min. nodes** and **Max. nodes** numbers in the group.

**CLI**

When [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups), add the following parameters to the [nebius mk8s node-group create](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md) command:

```bash theme={null}
nebius mk8s node-group create \
  ... \
  --autoscaling-min-node-count <minimum_number_of_nodes> \
  --autoscaling-max-node-count <maximum_number_of_nodes>
```

For example, to set the autoscaling from 2 to 4 nodes, add `--autoscaling-min-node-count 2 --autoscaling-max-node-count 4` to the `nebius mk8s node-group create` command.

**Go SDK**

When [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups), set `Spec.Size.Autoscaling` instead of a fixed node count:

```go theme={null}
createService := sdk.Services().MK8S().V1().NodeGroup()
createOperation, err := createService.Create(
    ctx,
    &mk8s.CreateNodeGroupRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: mk8sClusterID,
            Name:     nodeGroupName,
        },
        Spec: &mk8s.NodeGroupSpec{
            Size: &mk8s.NodeGroupSpec_Autoscaling{
                Autoscaling: &mk8s.NodeGroupAutoscalingSpec{
                    MinNodeCount: <minimum_number_of_nodes>,
                    MaxNodeCount: <maximum_number_of_nodes>,
                },
            },
            Template: &mk8s.NodeTemplate{
                Resources: &mk8s.ResourcesSpec{
                    Platform: "cpu-d3",
                    Size: &mk8s.ResourcesSpec_Preset{
                        Preset: "4vcpu-16gb",
                    },
                },
            },
        },
    },
)
if err != nil {
    return err
}
if _, err = createOperation.Wait(ctx); err != nil {
    return err
}
```

For example, to set the autoscaling from 2 to 4 nodes, set `MinNodeCount` to `2` and `MaxNodeCount` to `4`.

**Python SDK**

When [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups), set `spec.autoscaling` instead of a fixed node count:

```python theme={null}
create_service = NodeGroupServiceClient(sdk)
create_operation = await create_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id=mk8s_cluster_id,
            name=node_group_name,
        ),
        spec=NodeGroupSpec(
            autoscaling=NodeGroupAutoscalingSpec(
                min_node_count=<minimum_number_of_nodes>,
                max_node_count=<maximum_number_of_nodes>,
            ),
            template=NodeTemplate(
                resources=ResourcesSpec(
                    platform="cpu-d3",
                    preset="4vcpu-16gb",
                ),
            ),
        ),
    ),
)
await create_operation.wait()
```

For example, to set the autoscaling from 2 to 4 nodes, set `min_node_count` to `2` and `max_node_count` to `4`.

**JavaScript SDK**

When [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups), set `spec.size.autoscaling` instead of a fixed node count:

```ts theme={null}
const createService = new NodeGroupService(sdk);
const createOperation = await createService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: mk8sClusterId,
      name: nodeGroupName,
    }),
    spec: NodeGroupSpec.create({
      size: {
        $case: "autoscaling",
        autoscaling: NodeGroupAutoscalingSpec.create({
          minNodeCount: <minimum_number_of_nodes>,
          maxNodeCount: <maximum_number_of_nodes>,
        }),
      },
      template: NodeTemplate.create({
        resources: ResourcesSpec.create({
          platform: "cpu-d3",
          size: {
            $case: "preset",
            preset: "4vcpu-16gb",
          },
        }),
      }),
    }),
  }),
).result;
await createOperation.wait();
```

For example, to set the autoscaling from 2 to 4 nodes, set `minNodeCount` to `2` and `maxNodeCount` to `4`.

## Set up autoscaling for existing node groups

You cannot manage autoscaling for existing node groups in the web console. Use the CLI or an SDK instead.

**CLI**

To enable autoscaling for an existing node group, add the following parameters to the [nebius mk8s node-group update](https://docs.nebius.com/cli/reference/mk8s/node-group/update.md) command:

```bash theme={null}
nebius mk8s node-group update --id <node_group_ID> \
  --autoscaling-min-node-count <minimum_number_of_nodes> \
  --autoscaling-max-node-count <maximum_number_of_nodes>
```

For example, to set the autoscaling from 2 to 4 nodes, add `--autoscaling-min-node-count 2 --autoscaling-max-node-count 4` to the `nebius mk8s node-group update` command.

**Go SDK**

1. To find the node group ID by name:

   ```go theme={null}
   lookupService := sdk.Services().MK8S().V1().NodeGroup()
   nodeGroup, err := lookupService.GetByName(
       ctx,
       &common.GetByNameRequest{
           ParentId: mk8sClusterID,
           Name:     nodeGroupName,
       },
   )
   if err != nil {
       return err
   }
   nodeGroupID := nodeGroup.GetMetadata().GetId()
   if nodeGroupID == "" {
       return errors.New("node group ID is missing")
   }
   ```

2. Set `MinNodeCount` and `MaxNodeCount` on the node group's autoscaling spec:

   ```go theme={null}
   updateService := sdk.Services().MK8S().V1().NodeGroup()
   nodeGroup, err = updateService.Get(
       ctx,
       &mk8s.GetNodeGroupRequest{Id: "<node_group_ID>"},
   )
   if err != nil {
       return err
   }
   autoscaling := nodeGroup.GetSpec().GetAutoscaling()
   if autoscaling == nil {
       return errors.New("node group autoscaling is missing")
   }
   autoscaling.MinNodeCount = <minimum_number_of_nodes>
   autoscaling.MaxNodeCount = <maximum_number_of_nodes>
   updateOperation, err := updateService.Update(
       ctx,
       &mk8s.UpdateNodeGroupRequest{
           Metadata: nodeGroup.GetMetadata(),
           Spec:     nodeGroup.GetSpec(),
       },
   )
   if err != nil {
       return err
   }
   if _, err = updateOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   For example, to set the autoscaling from 2 to 4 nodes, set `MinNodeCount` to `2` and `MaxNodeCount` to `4`.

**Python SDK**

1. To find the node group ID by name:

   ```python theme={null}
   lookup_service = NodeGroupServiceClient(sdk)
   node_group = await lookup_service.get_by_name(
       GetByNameRequest(
           parent_id=mk8s_cluster_id,
           name=node_group_name,
       ),
   )
   node_group_id = node_group.metadata.id
   if not node_group_id:
       raise ValueError("node group ID is missing")
   ```

2. Set `min_node_count` and `max_node_count` on the node group's autoscaling spec:

   ```python theme={null}
   update_service = NodeGroupServiceClient(sdk)
   node_group = await update_service.get(
       GetNodeGroupRequest(id="<node_group_ID>"),
   )
   if node_group.spec is None:
       raise ValueError("node group spec is missing")
   if node_group.spec.autoscaling is None:
       raise ValueError("node group autoscaling is missing")
   node_group.spec.autoscaling.min_node_count = <minimum_number_of_nodes>
   node_group.spec.autoscaling.max_node_count = <maximum_number_of_nodes>
   update_operation = await update_service.update(
       UpdateNodeGroupRequest(
           metadata=node_group.metadata,
           spec=node_group.spec,
       ),
   )
   await update_operation.wait()
   ```

   For example, to set the autoscaling from 2 to 4 nodes, set `min_node_count` to `2` and `max_node_count` to `4`.

**JavaScript SDK**

1. To find the node group ID by name:

   ```ts theme={null}
   const lookupService = new NodeGroupService(sdk);
   const nodeGroup = await lookupService.getByName(
     GetByNameRequest.create({
       parentId: mk8sClusterId,
       name: nodeGroupName,
     }),
   );
   const nodeGroupId = nodeGroup.metadata?.id;
   if (!nodeGroupId) {
     throw new Error("node group ID is missing");
   }
   ```

2. Set `minNodeCount` and `maxNodeCount` on the node group's autoscaling spec:

   ```ts theme={null}
   const updateService = new NodeGroupService(sdk);
   const nodeGroupForUpdate = await updateService.get(
     GetNodeGroupRequest.create({
       id: "<node_group_ID>",
     }),
   );
   const autoscaling = nodeGroupForUpdate.spec?.size?.autoscaling;
   if (!autoscaling) {
     throw new Error("node group autoscaling is missing");
   }
   autoscaling.minNodeCount = <minimum_number_of_nodes>;
   autoscaling.maxNodeCount = <maximum_number_of_nodes>;
   const updateOperation = await updateService.update(
     UpdateNodeGroupRequest.create({
       metadata: nodeGroupForUpdate.metadata,
       spec: nodeGroupForUpdate.spec,
     }),
   ).result;
   await updateOperation.wait();
   ```

   For example, to set the autoscaling from 2 to 4 nodes, set `minNodeCount` to `2` and `maxNodeCount` to `4`.

The same operation changes the minimum and maximum numbers of nodes on a node group that already has autoscaling enabled.

## Troubleshooting

### More GPU nodes than required

* **Issue**: When a Managed Kubernetes cluster has the NVIDIA GPU Operator and the NVIDIA Network Operator installed, and workloads on a GPU node group are run with autoscaling, the cluster autoscaler can create more nodes in the group than the workloads require.
* **Possible reason**: A bug in Kubernetes Autoscaler that causes inconsistency in how nodes are considered ready or not ready for Pods. For more information, see [Excess multiGPU nodes when using GPU + network operators](https://github.com/kubernetes/autoscaler/issues/7956) in the Kubernetes Autoscaler repository on GitHub.
* **Solution**:

  1. Uninstall the NVIDIA operators.
  2. [Create a GPU node group](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-add-nodes-with-gpus-to-a-cluster) and [migrate your workloads](https://docs.nebius.com/kubernetes/node-groups/moving-workload.md) to it. A node group created this way uses the GPU-adapted boot disk image offered by Managed Kubernetes, which solves the issue because the NVIDIA operators are no longer required.

## See also

* [Cluster autoscaler parameters](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#what-are-the-parameters-to-ca) in the official GitHub repository.
