# InfiniBand™ networking for Compute virtual machines with GPUs

Source: https://docs.nebius.com/compute/clusters/gpu

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# InfiniBand™ networking for Compute virtual machines with GPUs

You can group your virtual machines with GPUs into a *GPU cluster*. The cluster accelerates high-performance computing (HPC) tasks such as training and inference. These tasks require a lot of processing power that a single VM cannot provide.

The GPU clusters are built with InfiniBand™ secure high-speed networking. Each GPU in a VM is connected through a network interface card (NIC) that provides 400 Gbps. As a compute VM for GPU clusters consists of 8 GPUs, the total bandwidth for a node is 3.2 Tbps.

Nebius AI Cloud uses GPUDirect RDMA, an NVIDIA® technology of remote direct memory access (RDMA) that allows data to flow directly between each GPU and its NIC, avoiding CPU, thus boosting the data exchange speed.

## InfiniBand™ fabrics

Each GPU cluster is created in one of the physical *InfiniBand™ fabrics*. This is where GPUs interconnected over InfiniBand™ are located. Each fabric has limited GPU capacity.

When creating a GPU cluster, select an InfiniBand™ fabric for it. Take into account the type of GPUs you are going to use. For example, if you select `fabric-7`, you can only add NVIDIA® H200 NVLink with Intel Sapphire Rapids GPUs to this cluster.

Available fabrics and corresponding regions ([private regions](https://docs.nebius.com/overview/regions.md) are marked with \*):

| Fabric | GPU platform | [Region](https://docs.nebius.com/overview/regions.md) |
| - | - | - |
| `fabric-2` | NVIDIA® H100 NVLink with Intel Sapphire Rapids (`gpu-h100-sxm`) | `eu-north1` |
| `fabric-3` | NVIDIA® H100 NVLink with Intel Sapphire Rapids (`gpu-h100-sxm`) | `eu-north1` |
| `fabric-4` | NVIDIA® H100 NVLink with Intel Sapphire Rapids (`gpu-h100-sxm`) | `eu-north1` |
| `fabric-5` | NVIDIA® H200 NVLink with Intel Sapphire Rapids (`gpu-h200-sxm`) | `eu-west1` |
| `fabric-6` | NVIDIA® H100 NVLink with Intel Sapphire Rapids (`gpu-h100-sxm`) | `eu-north1` |
| `fabric-7` | NVIDIA® H200 NVLink with Intel Sapphire Rapids (`gpu-h200-sxm`) | `eu-north1` |
| `eu-north2-a` | NVIDIA® H200 NVLink with Intel Sapphire Rapids (`gpu-h200-sxm`) | `eu-north2`\* |
| `eu-west2-a` | NVIDIA® B300 NVLink with Intel Granite Rapids (`gpu-b300-sxm`) | `eu-west2` |
| `me-west1-a` | NVIDIA® B200 NVLink with Intel Emerald Rapids (`gpu-b200-sxm-a`) | `me-west1` |
| `uk-south1-a` | NVIDIA® B300 NVLink with Intel Granite Rapids (`gpu-b300-sxm`) | `uk-south1` |
| `us-central1-a` | NVIDIA® H200 NVLink with Intel Sapphire Rapids (`gpu-h200-sxm`) | `us-central1` |
| `us-central1-b` | NVIDIA® B200 NVLink with Intel Emerald Rapids (`gpu-b200-sxm`) | `us-central1` |
| `us-north1-a` | NVIDIA® B300 NVLink with Intel Granite Rapids (`gpu-b300-sxm`) | `us-north1` |

> [!NOTE]
>
> In most cases, you do not need to change the preselected fabric. We recommend that you create a GPU cluster in another fabric only if it is better suited for a different platform or if you experience capacity issues with an existing GPU cluster.

## Isolation and security of InfiniBand™ traffic

Nebius AI Cloud isolates InfiniBand™ traffic between GPU clusters by using InfiniBand™ *partition keys* (P-Keys).

Each GPU cluster is assigned a unique P-Key to create isolation inside shared [physical InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/topology.md). This way, nodes in different GPU clusters cannot communicate over InfiniBand™ even if they use the same fabric infrastructure. This creates isolation between [tenants](https://docs.nebius.com/iam/overview.md#tenants) without requiring a dedicated physical fabric for each cluster.

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

## How to enable InfiniBand™ for VMs with GPUs

**Web console**

1. Create a GPU cluster:

   1. In the sidebar, go to  **Compute** → **GPU clusters**.
   2. Click  **Create GPU cluster**.
   3. On the page that opens, specify the cluster name. It should contain from 3 to 63 characters: lowercase letters, numbers and hyphens.
   4. Select the InfiniBand™ fabric.
   5. Click **Create GPU cluster**.

2. Add VMs to the cluster. You can assign a GPU cluster only when creating a VM:

   > [!WARNING]
   >
   > All virtual machines added to a GPU cluster must be in the same [project](https://docs.nebius.com/iam/overview.md#projects) as the GPU cluster.

   1. In the sidebar, go to  **Compute** → **Virtual machines**.
   2. Click **Create resource** → **Virtual machine**.
   3. On the **Compute** step of the VM creation wizard, select a platform and preset compatible with GPU clusters. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).
   4. In the **Settings** section, select an existing GPU cluster in the **GPU cluster** field, or create a new one.
   5. On the **Storage** step, select the boot disk for NVIDIA® GPUs. For details, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

You can also create a GPU cluster while [creating the first VM in it](https://docs.nebius.com/compute/virtual-machines/manage.md):

1. On the **Compute** step of the VM creation wizard:

   1. Select a platform and a preset compatible with GPU clusters. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).
   2. In the **Settings** section, create or select a GPU cluster in the **GPU cluster** field.

2. On the **Storage** step, select the boot disk for NVIDIA® GPUs. For details, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

**CLI**

1. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

2. If you have not set your project ID as `parent-id`, or you want to create resources in a different project, [get the project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) and update your [CLI profile](https://docs.nebius.com/cli/configure.md):
   ```bash theme={null}
   nebius profile update --parent-id <project_ID>
   ```

3. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand™ fabric](#infiniband-fabrics) for VM interconnection and save it to an environment variable:

   ```bash theme={null}
   export INFINIBAND_FABRIC=<fabric>
   ```

4. Create a GPU cluster and save its ID:

   ```bash theme={null}
   export GPU_CLUSTER_ID=$(nebius compute gpu-cluster create \
     --name <gpu_cluster_name> \
     --infiniband-fabric $INFINIBAND_FABRIC \
     --format jsonpath='{.metadata.id}')
   ```

   Where:

   * `Name`: A cluster name that you can use to quickly find the cluster.

5. Create a boot disk optimized for VMs with NVIDIA® GPUs:

   ```bash theme={null}
   export BOOT_DISK_ID=$(nebius compute disk create \
     --name <boot_disk_name> \
     --size-gibibytes 200 \
     --type network_ssd \
     --source-image-family-image-family ubuntu24.04-cuda13.0 \
     --block-size-bytes 4096 \
     --format jsonpath='{.metadata.id}')
   ```

   For compatible boot disk images (`--source-image-family-image-family`), see [Boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md).

6. [Create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with GPUs and specify the GPU cluster ID in its parameters.

   > [!WARNING]
   >
   > All virtual machines added to a GPU cluster must be in the same [project](https://docs.nebius.com/iam/overview.md#projects) as the GPU cluster.

   For example:

   ```bash theme={null}
   nebius compute instance create \
     --resources-platform gpu-h100-sxm \
     --resources-preset 8gpu-128vcpu-1600gb \
     --gpu-cluster-id $GPU_CLUSTER_ID \
     --boot-disk-existing-disk-id $BOOT_DISK_ID \
     ...
   ```

   Specify a VM platform with GPUs in `--resources-platform`, and a preset compatible with GPU clusters in `--resources-preset`. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

**Go SDK**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand™ fabric](#infiniband-fabrics) for VM interconnection and set it in the code:

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
                   Name: "<gpu_cluster_name>",
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
   ```

   Where:

   * `Metadata.Name`: A cluster name that you can use to quickly find the cluster.

3. Create a boot disk optimized for VMs with NVIDIA® GPUs:

   ```go theme={null}
   diskOperation, err := sdk.Services().Compute().V1().
       Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<boot_disk_name>",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 200,
                   },
                   BlockSizeBytes: 4096,
                   Type:           compute.DiskSpec_NETWORK_SSD,
                   Source: &compute.DiskSpec_SourceImageFamily{
                       SourceImageFamily: &compute.SourceImageFamily{
                           ImageFamily: "ubuntu24.04-cuda13.0",
                       },
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
   bootDiskID := diskOperation.ResourceID()
   ```

   For compatible boot disk images, see [Boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md).

4. [Create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with GPUs and specify the GPU cluster ID in its parameters.

   > [!WARNING]
   >
   > All virtual machines added to a GPU cluster must be in the same [project](https://docs.nebius.com/iam/overview.md#projects) as the GPU cluster.

   ```go theme={null}
   attachMode := compute.AttachedDiskSpec_READ_WRITE
   instanceOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "vm",
               },
               Spec: &compute.InstanceSpec{
                   Stopped: true,
                   Resources: &compute.ResourcesSpec{
                       Platform: "gpu-h100-sxm",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "8gpu-128vcpu-1600gb",
                       },
                   },
                   GpuCluster: &compute.InstanceGpuClusterSpec{
                       Id: gpuClusterID,
                   },
                   BootDisk: &compute.AttachedDiskSpec{
                       AttachMode: attachMode,
                       Type: &compute.AttachedDiskSpec_ExistingDisk{
                           ExistingDisk: &compute.ExistingDisk{
                               Id: bootDiskID,
                           },
                       },
                   },
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       {
                           Name:      "ni",
                           SubnetId:  subnetID,
                           IpAddress: &compute.IPAddress{},
                           PublicIpAddress: &compute.PublicIPAddress{},
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = instanceOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   Specify a VM platform with GPUs and a preset compatible with GPU clusters. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

**Python SDK**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand™ fabric](#infiniband-fabrics) for VM interconnection and set it in the code:

   ```python theme={null}
   infiniband_fabric = "<fabric>"
   ```

2. Create a GPU cluster and save its ID:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   create_cluster_operation = await gpu_cluster_service.create(
       CreateGpuClusterRequest(
           metadata=ResourceMetadata(
               name="<gpu_cluster_name>",
           ),
           spec=GpuClusterSpec(
               infiniband_fabric=infiniband_fabric,
           ),
       ),
   )
   await create_cluster_operation.wait()
   gpu_cluster_id = create_cluster_operation.resource_id
   ```

   Where:

   * `metadata.name`: A cluster name that you can use to quickly find the cluster.

3. Create a boot disk optimized for VMs with NVIDIA® GPUs:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   create_disk_operation = await disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(
               name="<boot_disk_name>",
           ),
           spec=DiskSpec(
               block_size_bytes=4096,
               type=DiskSpec.DiskType.NETWORK_SSD,
               source_image_family=SourceImageFamily(
                   image_family="ubuntu24.04-cuda13.0",
               ),
               size_gibibytes=200,
           ),
       ),
   )
   await create_disk_operation.wait()
   boot_disk_id = create_disk_operation.resource_id
   ```

   For compatible boot disk images, see [Boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md).

4. [Create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with GPUs and specify the GPU cluster ID in its parameters.

   > [!WARNING]
   >
   > All virtual machines added to a GPU cluster must be in the same [project](https://docs.nebius.com/iam/overview.md#projects) as the GPU cluster.

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   create_instance_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(
               name="vm",
           ),
           spec=InstanceSpec(
               stopped=True,
               resources=ResourcesSpec(
                   platform="gpu-h100-sxm",
                   preset="8gpu-128vcpu-1600gb",
               ),
               gpu_cluster=InstanceGpuClusterSpec(
                   id=gpu_cluster_id,
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   existing_disk=ExistingDisk(id=boot_disk_id),
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="ni",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await create_instance_operation.wait()
   ```

   Specify a VM platform with GPUs and a preset compatible with GPU clusters. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

**JavaScript SDK**

1. Depending on your project's [region](https://docs.nebius.com/overview/regions.md), select an [InfiniBand™ fabric](#infiniband-fabrics) for VM interconnection and set it in the code:

   ```ts theme={null}
   const infinibandFabric = "<fabric>";
   ```

2. Create a GPU cluster and save its ID:

   ```ts theme={null}
   const gpuClusterService = new GpuClusterService(sdk);
   const createGpuClusterOperation = await gpuClusterService.create(
     CreateGpuClusterRequest.create({
       metadata: ResourceMetadata.create({
         name: "<gpu_cluster_name>",
       }),
       spec: GpuClusterSpec.create({
         infinibandFabric,
       }),
     }),
   ).result;
   await createGpuClusterOperation.wait();
   const gpuClusterId = createGpuClusterOperation.resourceId();
   ```

   Where:

   * `metadata.name`: A cluster name that you can use to quickly find the cluster.

3. Create a boot disk optimized for VMs with NVIDIA® GPUs:

   ```ts theme={null}
   const diskService = new DiskService(sdk);
   const createDiskOperation = await diskService.create(
     CreateDiskRequest.create({
       metadata: ResourceMetadata.create({
         name: "<boot_disk_name>",
       }),
       spec: DiskSpec.create({
         blockSizeBytes: 4096,
         type: DiskSpec_DiskType.NETWORK_SSD,
         source: {
           $case: "sourceImageFamily",
           sourceImageFamily: SourceImageFamily.create({
             imageFamily: "ubuntu24.04-cuda13.0",
           }),
         },
         size: {
           $case: "sizeGibibytes",
           sizeGibibytes: 200,
         },
       }),
     }),
   ).result;
   await createDiskOperation.wait();
   const bootDiskId = createDiskOperation.resourceId();
   ```

   For compatible boot disk images, see [Boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md).

4. [Create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with GPUs and specify the GPU cluster ID in its parameters.

   > [!WARNING]
   >
   > All virtual machines added to a GPU cluster must be in the same [project](https://docs.nebius.com/iam/overview.md#projects) as the GPU cluster.

   ```ts theme={null}
   const instanceService = new InstanceService(sdk);
   const createInstanceOperation = await instanceService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "vm",
       }),
       spec: InstanceSpec.create({
         stopped: true,
         resources: ResourcesSpec.create({
           platform: "gpu-h100-sxm",
           size: {
             $case: "preset",
             preset: "8gpu-128vcpu-1600gb",
           },
         }),
         gpuCluster: InstanceGpuClusterSpec.create({
           id: gpuClusterId,
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: bootDiskId,
             }),
           },
         }),
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "ni",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
       }),
     }),
   ).result;
   await createInstanceOperation.wait();
   ```

   Specify a VM platform with GPUs and a preset compatible with GPU clusters. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

## How to test the connection with the NCCL tests

To test InfiniBand™ performance in a Compute cluster, you can run the NVIDIA® Collective Communications Library (NCCL) test in it. For instructions, see our tutorial on running distributed jobs with [MPIrun](https://docs.nebius.com/3p-integrations/mpirun.md): it uses the NCCL test as an example.

## How to delete a GPU cluster

Before deleting a GPU cluster, make sure all virtual machines in the cluster are deleted or moved to another cluster.

**Web console**

1. In the sidebar, go to  **Compute** → **GPU clusters**.
2. In the row of the GPU cluster you want to delete, click  → **Delete**.
3. In the window that opens, confirm the deletion.

**CLI**

1. Get the ID of the GPU cluster you want to delete:

   ```bash theme={null}
   nebius compute gpu-cluster list
   ```

2. Delete the GPU cluster:

   ```bash theme={null}
   nebius compute gpu-cluster delete <GPU_cluster_ID>
   ```

**Go SDK**

1. Get the ID of the GPU cluster you want to delete:

   ```go theme={null}
   gpuClusters, err := sdk.Services().Compute().V1().
       GpuCluster().List(
           ctx,
           &compute.ListGpuClustersRequest{
               ParentId: nbProject,
           },
       )
   if err != nil {
       return err
   }
   fmt.Println(gpuClusters)
   ```

2. Delete the GPU cluster:

   ```go theme={null}
   delClusterOp, err := sdk.Services().Compute().V1().
       GpuCluster().Delete(
           ctx,
           &compute.DeleteGpuClusterRequest{
               Id: "<GPU_cluster_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = delClusterOp.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the ID of the GPU cluster you want to delete:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   gpu_clusters = await gpu_cluster_service.list(
       ListGpuClustersRequest(parent_id=nb_project),
   )
   print(gpu_clusters)
   ```

2. Delete the GPU cluster:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   delete_cluster_operation = await gpu_cluster_service.delete(
       DeleteGpuClusterRequest(id="<GPU_cluster_ID>"),
   )
   await delete_cluster_operation.wait()
   ```

**JavaScript SDK**

1. Get the ID of the GPU cluster you want to delete:

   ```ts theme={null}
   const listGpuClusterService = new GpuClusterService(sdk);
   const gpuClusters = await listGpuClusterService.list(
     ListGpuClustersRequest.create({
       parentId: nbProject,
     }),
   );
   console.log(gpuClusters);
   ```

2. Delete the GPU cluster:

   ```ts theme={null}
   const deleteGpuClusterService = new GpuClusterService(sdk);
   const deleteClusterOperation = await deleteGpuClusterService.delete(
     DeleteGpuClusterRequest.create({
       id: "<GPU_cluster_ID>",
     }),
   ).result;
   await deleteClusterOperation.wait();
   ```

## See also

* [How to test a GPU cluster physical state in Compute](https://docs.nebius.com/compute/clusters/gpu/test.md)
* [InfiniBand™ networking for Compute virtual machines with GPUs](https://docs.nebius.com/kubernetes/gpu/clusters.md)
* [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md)
* [Running the all-reduce NCCL performance test in Soperator clusters](https://docs.nebius.com/slurm-soperator/jobs/examples/nccl-all-reduce.md)

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
