# How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups

Source: https://docs.nebius.com/kubernetes/networking/non-default-subnet

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups

By default, when you create a Managed Service for Kubernetes cluster, its control plane uses the [default subnet of the default network](https://docs.nebius.com/vpc/overview.md#default-virtual-networks-resources) in your project. Node groups inherit the control plane's subnet. You might want to use custom subnets that you created, for example, to ensure [resource isolation](https://docs.nebius.com/vpc/networking/isolation.md), [allocate custom private IP addresses](https://docs.nebius.com/vpc/addressing/custom-private-addresses.md) to nodes or [disable public IP addresses](https://docs.nebius.com/vpc/addressing/disable-public-addresses.md) for them.

> [!NOTE]
>
> To ensure connectivity, the control plane subnet and the node group subnet must belong to the same [network](https://docs.nebius.com/vpc/overview.md#network). Their [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing), however, can be different.

## A non-default network for clusters

To use a custom subnet for a cluster, [get its ID](https://docs.nebius.com/vpc/networking/resources.md) and pass it when [creating the cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters):

**CLI**

Pass the subnet ID to the `--control-plane-subnet-id` parameter:

```bash theme={null}
nebius mk8s cluster create \
  ... \
  --control-plane-subnet-id <subnet_ID>
```

**Go SDK**

Pass the subnet ID to `Spec.ControlPlane.SubnetId`:

```go theme={null}
clusterOperation, err := sdk.Services().MK8S().V1().
    Cluster().Create(
        ctx,
        &mk8s.CreateClusterRequest{
            Metadata: &common.ResourceMetadata{
                Name: "mk8s-cluster-name",
            },
            Spec: &mk8s.ClusterSpec{
                ControlPlane: &mk8s.ControlPlaneSpec{
                    Version: "1.36",
                    SubnetId: "<subnet_ID>",
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = clusterOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

Pass the subnet ID to `spec.control_plane.subnet_id`:

```python theme={null}
cluster_service = ClusterServiceClient(sdk)
cluster_operation = await cluster_service.create(
    CreateClusterRequest(
        metadata=ResourceMetadata(name="mk8s-cluster-name"),
        spec=ClusterSpec(
            control_plane=ControlPlaneSpec(
                version="1.36",
                subnet_id="<subnet_ID>",
            ),
        ),
    ),
)
await cluster_operation.wait()
```

**JavaScript SDK**

Pass the subnet ID to `spec.controlPlane.subnetId`:

```ts theme={null}
const clusterService = new ClusterService(sdk);
const clusterOperation = await clusterService.create(
  CreateClusterRequest.create({
    metadata: ResourceMetadata.create({
      name: "mk8s-cluster-name",
    }),
    spec: ClusterSpec.create({
      controlPlane: ControlPlaneSpec.create({
        version: "1.36",
        subnetId: "<subnet_ID>",
      }),
    }),
  }),
).result;
await clusterOperation.wait();
```

## A non-default network for node groups

To use a custom subnet for a node group, [get its ID](https://docs.nebius.com/vpc/networking/resources.md) and pass it when [creating the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

**CLI**

Add the subnet ID to the node group creation command by using the `--template-network-interfaces` parameter:

```bash theme={null}
nebius mk8s node-group create \
  ... \
  --template-network-interfaces '[{"public_ip_address": {}, "subnet_id": "<subnet_ID>"}]'
```

Alternatively, pass the subnet ID to the `spec.template.network_interfaces.subnet_id` parameter of the [node group configuration](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters).

**Go SDK**

Pass the subnet ID to `SubnetId` in `Spec.Template.NetworkInterfaces`:

```go theme={null}
nodeGroupOperation, err := sdk.Services().MK8S().V1().
    NodeGroup().Create(
        ctx,
        &mk8s.CreateNodeGroupRequest{
            Metadata: &common.ResourceMetadata{
                ParentId: mk8sClusterID,
                Name:     "node-group-1",
            },
            Spec: &mk8s.NodeGroupSpec{
                Version: "1.36",
                Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                    FixedNodeCount: 1,
                },
                Template: &mk8s.NodeTemplate{
                    BootDisk: &mk8s.DiskSpec{
                        Size: &mk8s.DiskSpec_SizeGibibytes{
                            SizeGibibytes: 64,
                        },
                        Type: mk8s.DiskSpec_NETWORK_SSD,
                    },
                    Resources: &mk8s.ResourcesSpec{
                        Platform: "cpu-d3",
                        Size: &mk8s.ResourcesSpec_Preset{
                            Preset: "4vcpu-16gb",
                        },
                    },
                    NetworkInterfaces:
                        []*mk8s.NetworkInterfaceTemplate{
                        {
                            PublicIpAddress: &mk8s.PublicIPAddress{},
                            SubnetId:         subnetID,
                        },
                    },
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

`SubnetId` reads the `subnetID` variable, and `ParentId` reads the `mk8sClusterID` variable. Assign the subnet ID and the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) to them before you run the code.

**Python SDK**

Pass the subnet ID to `subnet_id` in `spec.template.network_interfaces`:

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group_operation = await node_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id=mk8s_cluster_id,
            name="node-group-1",
        ),
        spec=NodeGroupSpec(
            version="1.36",
            fixed_node_count=1,
            template=NodeTemplate(
                boot_disk=DiskSpec(
                    size_gibibytes=64,
                    type=DiskSpec__DiskType.NETWORK_SSD,
                ),
                resources=ResourcesSpec(
                    platform="cpu-d3",
                    preset="4vcpu-16gb",
                ),
                network_interfaces=[
                    NetworkInterfaceTemplate(
                        public_ip_address=PublicIPAddress(),
                        subnet_id=subnet_id,
                    ),
                ],
            ),
        ),
    ),
)
await node_group_operation.wait()
```

`subnet_id` reads the `subnet_id` variable, and `parent_id` reads the `mk8s_cluster_id` variable. Assign the subnet ID and the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) to them before you run the code.

**JavaScript SDK**

Pass the subnet ID to `subnetId` in `spec.template.networkInterfaces`:

```ts theme={null}
const nodeGroupService = new NodeGroupService(sdk);
const nodeGroupOperation = await nodeGroupService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: mk8sClusterId,
      name: "node-group-1",
    }),
    spec: NodeGroupSpec.create({
      version: "1.36",
      size: {
        $case: "fixedNodeCount",
        fixedNodeCount: 1,
      },
      template: NodeTemplate.create({
        bootDisk: DiskSpec.create({
          size: {
            $case: "sizeGibibytes",
            sizeGibibytes: 64,
          },
          type: DiskSpec_DiskType.NETWORK_SSD,
        }),
        resources: ResourcesSpec.create({
          platform: "cpu-d3",
          size: {
            $case: "preset",
            preset: "4vcpu-16gb",
          },
        }),
        networkInterfaces: [
          NetworkInterfaceTemplate.create({
            publicIpAddress: PublicIPAddress.create({}),
            subnetId: subnetId,
          }),
        ],
      }),
    }),
  }),
).result;
await nodeGroupOperation.wait();
```

`subnetId` reads the `subnetId` variable, and `parentId` reads the `mk8sClusterId` variable. Assign the subnet ID and the [cluster ID](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-modify-clusters) to them before you run the code.

For more details, see [How to create node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups).
