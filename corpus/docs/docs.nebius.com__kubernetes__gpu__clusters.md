# Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™

Source: https://docs.nebius.com/kubernetes/gpu/clusters

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™

To accelerate ML, AI and high-performance computing (HPC) workloads that you run in your [Managed Service for Kubernetes clusters with GPUs](https://docs.nebius.com/kubernetes/gpu/set-up.md), you can interconnect the GPUs using [InfiniBand](https://www.infinibandta.org/about-infiniband/), a high-throughput, low-latency networking standard. For more details about InfiniBand in Nebius AI Cloud, see the [Compute documentation](https://docs.nebius.com/compute/clusters/gpu.md).

In this article, you will learn how to set up InfiniBand in a Managed Kubernetes cluster.

## How to enable InfiniBand for a node group

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.
2. Open the page of the cluster where you want to create a node group.
3. Click  **Create node group**.
4. Under **Computing resources**:

   1. Select **With GPU**.

   2. Select a platform and a preset compatible with GPU clusters. The compatible platforms and presets:

      | Platform | Presets | [Regions](https://docs.nebius.com/overview/regions.md) |
      | - | - | - |
      | NVIDIA® B300 NVLink with Intel Granite Rapids  (`gpu-b300-sxm`) | `8gpu-192vcpu-2768gb` | `uk-south1`, `eu-west2`, `us-north1` |
      | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm`) | `8gpu-160vcpu-1792gb` | `us-central1` |
      | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm-a`) | `8gpu-160vcpu-1792gb` | `me-west1` |
      | NVIDIA® H200 NVLink with Intel Sapphire Rapids  (`gpu-h200-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1`, `eu-north2`*\**, `eu-west1`, `us-central1` |
      | NVIDIA® H100 NVLink with Intel Sapphire Rapids  (`gpu-h100-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1` |

   3. Select a GPU cluster or create one. If the field is inactive, make sure you have selected a compatible platform and preset.

      > [!WARNING]
      >
      > All virtual machines added to a GPU cluster must be in the same [project](https://docs.nebius.com/iam/overview.md#projects) as the GPU cluster.

   4. Under **GPU settings**, keep the **Install NVIDIA GPU drivers and other components** option enabled.

      If you want to [install the drivers manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups), disable this option.

**CLI**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand fabric](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics) and save it to an environment variable:

   ```bash theme={null}
   export INFINIBAND_FABRIC=<fabric>
   ```

2. Create a GPU cluster and save its ID:

   ```bash theme={null}
   export GPU_CLUSTER_ID=$(nebius compute gpu-cluster create \
     --name gpu-cluster-name \
     --infiniband-fabric $INFINIBAND_FABRIC \
     --format jsonpath='{.metadata.id}')
   ```

3. [Create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) with GPUs and specify the GPU cluster ID in its parameters by using the [nebius mk8s node-group create](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md) command:

   ```bash theme={null}
   nebius mk8s node-group create \
     --template-resources-platform gpu-h100-sxm \
     --template-resources-preset 8gpu-128vcpu-1600gb \
     --template-gpu-cluster-id $GPU_CLUSTER_ID \
     --template-gpu-settings-drivers-preset cuda13.0 \
     ...
   ```

   > [!WARNING]
   >
   > If a node group uses a GPU cluster, the GPU cluster must be located in the same project as the node group's parent cluster.

   * In `--template.gpu-cluster-id`, specify the GPU cluster ID.

   * In `--template-resources-platform`, specify a platform with GPUs. In `--template-resources-preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). The compatible platforms and presets are:

     | Platform | Presets | [Regions](https://docs.nebius.com/overview/regions.md) |
     | - | - | - |
     | NVIDIA® B300 NVLink with Intel Granite Rapids  (`gpu-b300-sxm`) | `8gpu-192vcpu-2768gb` | `uk-south1`, `eu-west2`, `us-north1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm`) | `8gpu-160vcpu-1792gb` | `us-central1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm-a`) | `8gpu-160vcpu-1792gb` | `me-west1` |
     | NVIDIA® H200 NVLink with Intel Sapphire Rapids  (`gpu-h200-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1`, `eu-north2`*\**, `eu-west1`, `us-central1` |
     | NVIDIA® H100 NVLink with Intel Sapphire Rapids  (`gpu-h100-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1` |

   * In `--template-gpu-settings-drivers-preset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

     If you want to [install the drivers manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#drivers-install), omit the `--template-gpu-settings-drivers-preset` parameter.

**Go SDK**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand fabric](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics):

   ```go theme={null}
   infinibandFabric := "<fabric>"
   ```

2. Create a GPU cluster and save its ID:

   ```go theme={null}
   gpuClusterOperation, err := sdk.Services().Compute().V1().
       GpuCluster().Create(
           ctx,
           &compute.CreateGpuClusterRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "gpu-cluster-name",
               },
               Spec: &compute.GpuClusterSpec{
                   InfinibandFabric: infinibandFabric,
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = gpuClusterOperation.Wait(ctx); err != nil {
       return err
   }
   gpuClusterID := gpuClusterOperation.ResourceID()
   if gpuClusterID == "" {
       return fmt.Errorf("GPU cluster ID is missing")
   }
   ```

3. [Create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) with GPUs and specify the GPU cluster ID in its parameters:

   ```go theme={null}
   nodeGroupOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Create(
           ctx,
           &mk8s.CreateNodeGroupRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: mk8sClusterID,
                   Name:     "node-group-example",
               },
               Spec: &mk8s.NodeGroupSpec{
                   Version: "1.36",
                   Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                       FixedNodeCount: 1,
                   },
                   Template: &mk8s.NodeTemplate{
                       Resources: &mk8s.ResourcesSpec{
                           Platform: "gpu-h100-sxm",
                           Size: &mk8s.ResourcesSpec_Preset{
                               Preset: "8gpu-128vcpu-1600gb",
                           },
                       },
                       BootDisk: &mk8s.DiskSpec{
                           Size: &mk8s.DiskSpec_SizeGibibytes{
                               SizeGibibytes: 100,
                           },
                           Type: mk8s.DiskSpec_NETWORK_SSD,
                       },
                       GpuCluster: &mk8s.GpuClusterSpec{
                           Id: gpuClusterID,
                       },
                       GpuSettings: &mk8s.GpuSettings{
                           DriversPreset: "cuda13.0",
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

   * In `Template.GpuCluster.Id`, specify the GPU cluster ID.

   * In `Template.Resources.Platform`, specify a platform with GPUs. In `Template.Resources.Size.Preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). The compatible platforms and presets are:

     | Platform | Presets | [Regions](https://docs.nebius.com/overview/regions.md) |
     | - | - | - |
     | NVIDIA® B300 NVLink with Intel Granite Rapids  (`gpu-b300-sxm`) | `8gpu-192vcpu-2768gb` | `uk-south1`, `eu-west2`, `us-north1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm`) | `8gpu-160vcpu-1792gb` | `us-central1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm-a`) | `8gpu-160vcpu-1792gb` | `me-west1` |
     | NVIDIA® H200 NVLink with Intel Sapphire Rapids  (`gpu-h200-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1`, `eu-north2`*\**, `eu-west1`, `us-central1` |
     | NVIDIA® H100 NVLink with Intel Sapphire Rapids  (`gpu-h100-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1` |

   * In `Template.GpuSettings.DriversPreset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

     If you want to [install the drivers manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups), omit `Template.GpuSettings`.

**Python SDK**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand fabric](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics):

   ```python theme={null}
   infiniband_fabric = "<fabric>"
   ```

2. Create a GPU cluster and save its ID:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   gpu_cluster_operation = await gpu_cluster_service.create(
       CreateGpuClusterRequest(
           metadata=ResourceMetadata(name="gpu-cluster-name"),
           spec=GpuClusterSpec(
               infiniband_fabric=infiniband_fabric,
           ),
       ),
   )
   await gpu_cluster_operation.wait()
   gpu_cluster_id = gpu_cluster_operation.resource_id
   if not gpu_cluster_id:
       raise ValueError("GPU cluster ID is missing")
   ```

3. [Create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) with GPUs and specify the GPU cluster ID in its parameters:

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group_operation = await node_group_service.create(
       CreateNodeGroupRequest(
           metadata=ResourceMetadata(
               parent_id=mk8s_cluster_id,
               name="node-group-example",
           ),
           spec=NodeGroupSpec(
               version="1.36",
               fixed_node_count=1,
               template=NodeTemplate(
                   resources=ResourcesSpec(
                       platform="gpu-h100-sxm",
                       preset="8gpu-128vcpu-1600gb",
                   ),
                   boot_disk=DiskSpec(
                       size_gibibytes=100,
                       type=DiskSpec__DiskType.NETWORK_SSD,
                   ),
                   gpu_cluster=GpuClusterSpec(id=gpu_cluster_id),
                   gpu_settings=GpuSettings(drivers_preset="cuda13.0"),
               ),
           ),
       ),
   )
   await node_group_operation.wait()
   ```

   * In `template.gpu_cluster.id`, specify the GPU cluster ID.

   * In `template.resources.platform`, specify a platform with GPUs. In `template.resources.preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). The compatible platforms and presets are:

     | Platform | Presets | [Regions](https://docs.nebius.com/overview/regions.md) |
     | - | - | - |
     | NVIDIA® B300 NVLink with Intel Granite Rapids  (`gpu-b300-sxm`) | `8gpu-192vcpu-2768gb` | `uk-south1`, `eu-west2`, `us-north1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm`) | `8gpu-160vcpu-1792gb` | `us-central1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm-a`) | `8gpu-160vcpu-1792gb` | `me-west1` |
     | NVIDIA® H200 NVLink with Intel Sapphire Rapids  (`gpu-h200-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1`, `eu-north2`*\**, `eu-west1`, `us-central1` |
     | NVIDIA® H100 NVLink with Intel Sapphire Rapids  (`gpu-h100-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1` |

   * In `template.gpu_settings.drivers_preset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

     If you want to [install the drivers manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups), omit `template.gpu_settings`.

**JavaScript SDK**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand fabric](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics):

   ```ts theme={null}
   const infinibandFabric = "<fabric>";
   ```

2. Create a GPU cluster and save its ID:

   ```ts theme={null}
   const gpuClusterService = new GpuClusterService(sdk);
   const gpuClusterOperation = await gpuClusterService.create(
     CreateGpuClusterRequest.create({
       metadata: ResourceMetadata.create({
         name: "gpu-cluster-name",
       }),
       spec: GpuClusterSpec.create({
         infinibandFabric,
       }),
     }),
   ).result;
   await gpuClusterOperation.wait();
   const gpuClusterId = gpuClusterOperation.resourceId();
   if (!gpuClusterId) {
     throw new Error("GPU cluster ID is missing");
   }
   ```

3. [Create a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) with GPUs and specify the GPU cluster ID in its parameters:

   ```ts theme={null}
   const nodeGroupService = new NodeGroupService(sdk);
   const nodeGroupOperation = await nodeGroupService.create(
     CreateNodeGroupRequest.create({
       metadata: ResourceMetadata.create({
         parentId: mk8sClusterId,
         name: "node-group-example",
       }),
       spec: NodeGroupSpec.create({
         version: "1.36",
         size: {
           $case: "fixedNodeCount",
           fixedNodeCount: 1,
         },
         template: NodeTemplate.create({
           resources: ResourcesSpec.create({
             platform: "gpu-h100-sxm",
             size: {
               $case: "preset",
               preset: "8gpu-128vcpu-1600gb",
             },
           }),
           bootDisk: DiskSpec.create({
             size: {
               $case: "sizeGibibytes",
               sizeGibibytes: 100,
             },
             type: DiskSpec_DiskType.NETWORK_SSD,
           }),
           gpuCluster: GpuClusterSpec.create({
             id: gpuClusterId,
           }),
           gpuSettings: GpuSettings.create({
             driversPreset: "cuda13.0",
           }),
         }),
       }),
     }),
   ).result;
   await nodeGroupOperation.wait();
   ```

   * In `template.gpuCluster.id`, specify the GPU cluster ID.

   * In `template.resources.platform`, specify a platform with GPUs. In `template.resources.size.preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). The compatible platforms and presets are:

     | Platform | Presets | [Regions](https://docs.nebius.com/overview/regions.md) |
     | - | - | - |
     | NVIDIA® B300 NVLink with Intel Granite Rapids  (`gpu-b300-sxm`) | `8gpu-192vcpu-2768gb` | `uk-south1`, `eu-west2`, `us-north1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm`) | `8gpu-160vcpu-1792gb` | `us-central1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm-a`) | `8gpu-160vcpu-1792gb` | `me-west1` |
     | NVIDIA® H200 NVLink with Intel Sapphire Rapids  (`gpu-h200-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1`, `eu-north2`*\**, `eu-west1`, `us-central1` |
     | NVIDIA® H100 NVLink with Intel Sapphire Rapids  (`gpu-h100-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1` |

   * In `template.gpuSettings.driversPreset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

     If you want to [install the drivers manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups), omit `template.gpuSettings`.

## Example: NCCL tests

To test InfiniBand performance in a Managed Service for Kubernetes cluster, you can run the NVIDIA NCCL test in it. For instructions, see our [tutorial](https://docs.nebius.com/kubernetes/gpu/nccl-test.md).

## See also

* [Working with GPUs in a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/gpu/set-up.md)
* [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md)
* [Creating and modifying node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md)

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
