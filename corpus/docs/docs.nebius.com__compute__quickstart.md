# Getting started with Compute: Create your first Nebius AI Cloud virtual machine

Source: https://docs.nebius.com/compute/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Compute: Create your first Nebius AI Cloud virtual machine

To set up infrastructure for ML workloads, create the following resources in the `eu-north1` region:

* Virtual machine (VM) with eight GPUs and a shared filesystem for training
* Virtual machine with one GPU for inference

Then, connect to them.

## Prerequisites

**Web console**

Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

* Install [jq](https://jqlang.github.io/jq/) to extract IDs from JSON data returned by the Nebius AI Cloud CLI:

  ```bash Ubuntu theme={null}
  sudo apt-get install jq
  ```

  ```bash macOS theme={null}
  brew install jq
  ```

* Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

* Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

* Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

* Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

## Create a VM with eight GPUs with InfiniBand™ and a shared filesystem for training

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. Click **Create resource** → **Virtual machine**.

   The creation flow is a step-by-step wizard. The sidebar shows your progress through the configuration sections. To move between sections, click **Back** and **Next**.

3. On the **Compute** step, configure computing resources:

   1. In the **Platform** section, select **With GPUs** and **Regular**. Then, select a [platform](https://docs.nebius.com/compute/virtual-machines/types.md) with NVIDIA® H100, H200 or B200 GPUs. Only these platforms support GPU clusters.

   2. In the **Settings** section, select a **Preset** with 8 GPUs.

   3. Create a GPU cluster for the VM. InfiniBand in the GPU cluster interconnects the VM GPUs for high-speed networking and efficient training.

      To use a GPU cluster, select an existing one or create a new cluster:

      1. Click  **Create** in the **GPU cluster** field.
      2. In the window that opens, specify the cluster name and InfiniBand fabric. To select the fabric, see [InfiniBand fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).
      3. Click **Create**.

   4. In the same section, select the **Project** for the VM location and specify the **VM name**.

4. On the **Storage** step, configure the boot disk and attach a shared filesystem:

   1. In the **Boot disk** section, click  next to the boot disk. In the window that opens, keep **New VM-managed disk** selected, choose an Ubuntu [operating system](https://docs.nebius.com/compute/storage/boot-disk-images.md#images-for-gpu-vms) with pre-installed NVIDIA® GPU drivers, set the size to 50 GiB and click **Save**.

   2. In the **Shared filesystems** section, click  **Attach shared filesystem**.

   3. In the window that opens, create a new filesystem: specify its name, set the size to 50 GiB and the block size to 4 KiB. Click **Attach filesystem**.

   4. After the window is closed, in the **Mount tag** field, specify a tag for mounting the filesystem to the VM.

      Create your own tag, such as `my-filesystem`. Make sure that it is unique within the VM.

   5. To mount the filesystem to the VM automatically, keep the **Auto mount** option enabled.

5. On the **Network** step, select the **Network** and **Subnet**. In the **Public IP address** field, select **Auto (dynamic)**, so you can later connect to the VM by SSH.

6. On the **Configuration** step, in the **Access** section, add credentials so you can connect to the VM:

   1. In the **Username and SSH key** field, click  **Create**.
   2. In the window that opens, specify the username of the VM user, a public key of your SSH key pair and the credentials name to recognize the key in the list.

      Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.
   3. Click **Add credentials**.

7. On the **Review** step, check the full VM configuration. To change a section quickly, click  next to the corresponding block. The wizard opens the relevant step with your current settings.

   Then, click **Create VM**.

For more information about the wizard settings, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**CLI**

1. Create a shared filesystem and save its ID to an environment variable:

   ```bash theme={null}
   export TR_VM_FILESYSTEM_ID=$(nebius compute filesystem create \
     --name training-vm-filesystem-1 \
     --size-gibibytes 50 \
     --type network_ssd \
     --block-size-bytes 4096 \
     --format jsonpath='{.metadata.id}')
   ```

   The command creates a 50 GiB SSD shared filesystem with 4 KiB blocks.

2. Get the subnet ID and save it to an environment variable:

   ```bash theme={null}
   export SUBNET_ID=$(nebius vpc subnet list \
     --format jsonpath='{.items[0].metadata.id}')
   ```

   Possible subnet ID: `vpcsubnet-***`.

3. For high-speed networking and efficient training, consider interconnecting multiple VM GPUs in a GPU cluster using InfiniBand. To do this, before creating the VM, create a GPU cluster to connect the VM and get its ID:

   ```bash theme={null}
   export GPU_CLUSTER_ID=$(nebius compute gpu-cluster create \
     --name gpu-cluster-name \
     --infiniband-fabric fabric-3 \
     --format jsonpath='{.metadata.id}')
   ```

4. Create a VM with 8 GPUs for training:

   ```bash theme={null}
   export USER_DATA=$(jq -Rrs '.' <<EOF
   #cloud-config
   users:
     - name: user
       sudo: ALL=(ALL) NOPASSWD:ALL
       shell: /bin/bash
       ssh_authorized_keys:
         - $(cat ~/.ssh/id_ed25519.pub)
   EOF
   )

   export TR_VM_ID=$(nebius compute instance create \
     --name training-vm \
     --resources-platform gpu-h100-sxm \
     --resources-preset 8gpu-128vcpu-1600gb \
     --boot-disk-managed-disk-name training-vm-disk-1 \
     --boot-disk-managed-disk-type network_ssd \
     --boot-disk-managed-disk-size-gibibytes 50 \
     --boot-disk-managed-disk-block-size-bytes 4096 \
     --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-cuda13.0 \
     --boot-disk-attach-mode READ_WRITE \
     --cloud-init-user-data "$USER_DATA" \
     --filesystems "[{\"existing_filesystem\": {\"id\": \"$TR_VM_FILESYSTEM_ID\"}, \"attach_mode\": \"READ_WRITE\", \"mount_tag\": \"training-vm-filesystem-1\"}]" \
     --network-interfaces "[{\"name\": \"eth0\", \"subnet_id\": \"$SUBNET_ID\", \"ip_address\": {}, \"public_ip_address\": {}}]" \
     --gpu-cluster-id "$GPU_CLUSTER_ID" \
     --format jsonpath='{.metadata.id}')
   ```

   For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**Go SDK**

1. Create a boot disk:

   ```go theme={null}
   trainingDiskOperation, err := sdk.Services().Compute().V1().
       Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "training-vm-disk-1",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 50,
                   },
                   BlockSizeBytes: 4096,
                   Type: compute.DiskSpec_NETWORK_SSD,
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
   if _, err = trainingDiskOperation.Wait(ctx); err != nil {
       return err
   }
   trainingBootDiskID := trainingDiskOperation.ResourceID()
   ```

   The code creates a 50 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Create a shared filesystem:

   ```go theme={null}
   trainingFSOperation, err := sdk.Services().Compute().V1().
       Filesystem().Create(
           ctx,
           &compute.CreateFilesystemRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "training-vm-filesystem-1",
               },
               Spec: &compute.FilesystemSpec{
                   Size: &compute.FilesystemSpec_SizeGibibytes{
                       SizeGibibytes: 50,
                   },
                   BlockSizeBytes: 4096,
                   Type: compute.FilesystemSpec_NETWORK_SSD,
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = trainingFSOperation.Wait(ctx); err != nil {
       return err
   }
   trainingFilesystemID := trainingFSOperation.ResourceID()
   ```

   The code creates a 50 GiB SSD shared filesystem with 4 KiB blocks.

3. Get the subnet ID:

   ```go theme={null}
   subnets, err := sdk.Services().VPC().V1().
       Subnet().List(
           ctx,
           &vpc.ListSubnetsRequest{},
       )
   if err != nil {
       return err
   }
   if len(subnets.GetItems()) == 0 {
       return errors.New("no subnets found")
   }
   subnetID := subnets.GetItems()[0].GetMetadata().GetId()
   ```

   Possible subnet ID: `vpcsubnet-e0dcbaa76x2024xyz8`.

4. For high-speed networking and efficient training, consider interconnecting multiple VM GPUs in a GPU cluster using InfiniBand™. To do this, before creating the VM, create a GPU cluster to connect the VM and get its ID:

   ```go theme={null}
   gpuClusterOperation, err := sdk.Services().Compute().V1().
       GpuCluster().Create(
           ctx,
           &compute.CreateGpuClusterRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "gpu-cluster-name",
               },
               Spec: &compute.GpuClusterSpec{
                   InfinibandFabric: "fabric-3",
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

5. Create a VM with 8 GPUs for training:

   ```go theme={null}
   var gpuCluster *compute.InstanceGpuClusterSpec
   if gpuClusterID != "" {
       gpuCluster = &compute.InstanceGpuClusterSpec{
           Id: gpuClusterID,
       }
   }
   trainingNetworkName :=
       "multi-gpu-node-compute-api-" +
           "network-interface"
   trainingResources := &compute.ResourcesSpec{
       Platform: "gpu-h100-sxm",
       Size: &compute.ResourcesSpec_Preset{
           Preset: "8gpu-128vcpu-1600gb",
       },
   }
   trainingBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ExistingDisk{
           ExistingDisk: &compute.ExistingDisk{
               Id: trainingBootDiskID,
           },
       },
   }
   trainingExistingFS := &compute.ExistingFilesystem{
       Id: trainingFilesystemID,
   }
   trainingFilesystem := &compute.AttachedFilesystemSpec{
       AttachMode: compute.AttachedFilesystemSpec_READ_WRITE,
       MountTag:   "training-vm-filesystem-1",
       Type: &compute.AttachedFilesystemSpec_ExistingFilesystem{
           ExistingFilesystem: trainingExistingFS,
       },
   }
   trainingNetwork := &compute.NetworkInterfaceSpec{
       Name:            trainingNetworkName,
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   trainingSpec := &compute.InstanceSpec{
       Resources:  trainingResources,
       GpuCluster: gpuCluster,
       BootDisk:   trainingBootDisk,
       Filesystems: []*compute.AttachedFilesystemSpec{
           trainingFilesystem,
       },
       CloudInitUserData: userData,
       NetworkInterfaces: []*compute.NetworkInterfaceSpec{
           trainingNetwork,
       },
   }
   trainingVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "training-vm",
               },
               Spec: trainingSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = trainingVMOperation.Wait(ctx); err != nil {
       return err
   }
   trainingVMID := trainingVMOperation.ResourceID()
   ```

   The given example assumes that you work with VMs that have public addresses, so you can later [connect to these VMs by SSH](#connect-to-the-vms). However, if you need isolated VMs without public addresses, do not set `PublicIpAddress` in the network interface specification. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

   For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**Python SDK**

1. Create a boot disk:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   training_disk_operation = await disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(
               name="training-vm-disk-1",
           ),
           spec=DiskSpec(
               block_size_bytes=4096,
               type=DiskSpec.DiskType.NETWORK_SSD,
               source_image_family=SourceImageFamily(
                   image_family="ubuntu24.04-cuda13.0",
               ),
               size_gibibytes=50,
           ),
       ),
   )
   await training_disk_operation.wait()
   training_boot_disk_id = training_disk_operation.resource_id
   ```

   The code creates a 50 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Create a shared filesystem:

   ```python theme={null}
   filesystem_service = FilesystemServiceClient(sdk)
   training_fs_operation = await filesystem_service.create(
       CreateFilesystemRequest(
           metadata=ResourceMetadata(
               name="training-vm-filesystem-1",
           ),
           spec=FilesystemSpec(
               block_size_bytes=4096,
               type=FilesystemSpec.FilesystemType.NETWORK_SSD,
               size_gibibytes=50,
           ),
       ),
   )
   await training_fs_operation.wait()
   training_filesystem_id = training_fs_operation.resource_id
   ```

   The code creates a 50 GiB SSD shared filesystem with 4 KiB blocks.

3. Get the subnet ID:

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnets = await subnet_service.list(ListSubnetsRequest())
   if not subnets.items:
       raise ValueError("no subnets found")
   subnet_id = subnets.items[0].metadata.id
   ```

   Possible subnet ID: `vpcsubnet-e0dcbaa76x2024xyz8`.

4. For high-speed networking and efficient training, consider interconnecting multiple VM GPUs in a GPU cluster using InfiniBand™. To do this, before creating the VM, create a GPU cluster to connect the VM and get its ID:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   gpu_cluster_operation = await gpu_cluster_service.create(
       CreateGpuClusterRequest(
           metadata=ResourceMetadata(
               name="gpu-cluster-name",
           ),
           spec=GpuClusterSpec(
               infiniband_fabric="fabric-3",
           ),
       ),
   )
   await gpu_cluster_operation.wait()
   gpu_cluster_id = gpu_cluster_operation.resource_id
   ```

5. Create a VM with 8 GPUs for training:

   ```python theme={null}
   gpu_cluster = None
   if gpu_cluster_id:
       gpu_cluster = InstanceGpuClusterSpec(id=gpu_cluster_id)
   training_network_name = (
       "multi-gpu-node-compute-api-"
       "network-interface"
   )
   instance_service = InstanceServiceClient(sdk)
   training_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="training-vm"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="gpu-h100-sxm",
                   preset="8gpu-128vcpu-1600gb",
               ),
               gpu_cluster=gpu_cluster,
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   existing_disk=ExistingDisk(
                       id=training_boot_disk_id,
                   ),
               ),
               filesystems=[
                   AttachedFilesystemSpec(
                       attach_mode=(
                           AttachedFilesystemSpec.AttachMode.READ_WRITE
                       ),
                       existing_filesystem=ExistingFilesystem(
                           id=training_filesystem_id,
                       ),
                       mount_tag="training-vm-filesystem-1",
                   ),
               ],
               cloud_init_user_data=user_data,
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name=training_network_name,
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await training_vm_operation.wait()
   training_vm_id = training_vm_operation.resource_id
   ```

   The given example assumes that you work with VMs that have public addresses, so you can later [connect to these VMs by SSH](#connect-to-the-vms). However, if you need isolated VMs without public addresses, do not set `public_ip_address` in the network interface specification. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

   For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**JavaScript SDK**

1. Create a boot disk:

   ```ts theme={null}
   const diskService = new DiskService(sdk);
   const trainingDiskOperation = await diskService.create(
     CreateDiskRequest.create({
       metadata: ResourceMetadata.create({
         name: "training-vm-disk-1",
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
           sizeGibibytes: 50,
         },
       }),
     }),
   ).result;
   await trainingDiskOperation.wait();
   const trainingBootDiskId = trainingDiskOperation.resourceId();
   ```

   The code creates a 50 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Create a shared filesystem:

   ```ts theme={null}
   const filesystemService = new FilesystemService(sdk);
   const trainingFsOperation = await filesystemService.create(
     CreateFilesystemRequest.create({
       metadata: ResourceMetadata.create({
         name: "training-vm-filesystem-1",
       }),
       spec: FilesystemSpec.create({
         blockSizeBytes: 4096,
         type: FilesystemSpec_FilesystemType.NETWORK_SSD,
         size: {
           $case: "sizeGibibytes",
           sizeGibibytes: 1024,
         },
       }),
     }),
   ).result;
   await trainingFsOperation.wait();
   const trainingFilesystemId =
     trainingFsOperation.resourceId();
   ```

   The code creates a 50 GiB SSD shared filesystem with 4 KiB blocks.

3. Get the subnet ID:

   ```ts theme={null}
   const subnetService = new SubnetService(sdk);
   const subnets = await subnetService.list(
     ListSubnetsRequest.create({}),
   );
   const subnetId = subnets.items[0]?.metadata?.id;
   if (!subnetId) {
     throw new Error("no subnets found");
   }
   ```

   Possible subnet ID: `vpcsubnet-e0dcbaa76x2024xyz8`.

4. For high-speed networking and efficient training, consider interconnecting multiple VM GPUs in a GPU cluster using InfiniBand™. To do this, before creating the VM, create a GPU cluster to connect the VM and get its ID:

   ```ts theme={null}
   const gpuClusterService = new GpuClusterService(sdk);
   const gpuClusterOperation = await gpuClusterService.create(
     CreateGpuClusterRequest.create({
       metadata: ResourceMetadata.create({
         name: "gpu-cluster-name",
       }),
       spec: GpuClusterSpec.create({
         infinibandFabric: "fabric-3",
       }),
     }),
   ).result;
   await gpuClusterOperation.wait();
   let gpuClusterId = gpuClusterOperation.resourceId();
   ```

5. Create a VM with 8 GPUs for training:

   ```ts theme={null}
   const gpuCluster = gpuClusterId
     ? InstanceGpuClusterSpec.create({ id: gpuClusterId })
     : undefined;
   const trainingNetworkName =
     "multi-gpu-node-compute-api-" +
     "network-interface";
   const instanceService = new InstanceService(sdk);
   const trainingVmOperation = await instanceService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "training-vm",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "gpu-h100-sxm",
           size: {
             $case: "preset",
             preset: "8gpu-128vcpu-1600gb",
           },
         }),
         gpuCluster,
         bootDisk: AttachedDiskSpec.create({
           attachMode:
             AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: trainingBootDiskId,
             }),
           },
         }),
         filesystems: [
           AttachedFilesystemSpec.create({
             attachMode:
               AttachedFilesystemSpec_AttachMode.READ_WRITE,
             mountTag: "training-vm-filesystem-1",
             type: {
               $case: "existingFilesystem",
               existingFilesystem:
                 ExistingFilesystem.create({
                   id: trainingFilesystemId,
                 }),
             },
           }),
         ],
         cloudInitUserData: userData,
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: trainingNetworkName,
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
       }),
     }),
   ).result;
   await trainingVmOperation.wait();
   const trainingVmId = trainingVmOperation.resourceId();
   ```

   The given example assumes that you work with VMs that have public addresses, so you can later [connect to these VMs by SSH](#connect-to-the-vms). However, if you need isolated VMs without public addresses, do not set `publicIpAddress` in the network interface specification. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

   For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

## Create a VM with one GPU for inference

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. Click **Create resource** → **Virtual machine**.

3. On the **Compute** step, configure computing resources:

   1. In the **Platform** section, select **With GPUs** and **Regular**. Then, select any [GPU platform](https://docs.nebius.com/compute/virtual-machines/types.md).
   2. In the **Settings** section, select a **Preset** with one GPU and the **Project** for the VM location, and specify the **VM name**.

4. On the **Storage** step, in the **Boot disk** section, click  next to the boot disk. In the window that opens, keep **New VM-managed disk** selected, choose an Ubuntu operating system with pre-installed NVIDIA® GPU drivers, set the size to 50 GiB and click **Save**.

5. On the **Network** step, select the **Network** and **Subnet**. In the **Public IP address** field, select **Auto (dynamic)**, so you can later connect to the VM by SSH.

6. On the **Configuration** step, in the **Access** section, add the same username and SSH public key that you used for the VM with eight GPUs.

7. On the **Review** step, check the full VM configuration and click **Create VM**.

**CLI**

Create a VM with one GPU for inference:

```bash theme={null}
export INF_VM_ID=$(nebius compute instance create \
  --name inference-vm \
  --resources-platform gpu-h100-sxm \
  --resources-preset 1gpu-16vcpu-200gb \
  --boot-disk-managed-disk-name inference-vm-disk-1 \
  --boot-disk-managed-disk-type network_ssd \
  --boot-disk-managed-disk-size-gibibytes 50 \
  --boot-disk-managed-disk-block-size-bytes 4096 \
  --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-cuda13.0 \
  --boot-disk-attach-mode READ_WRITE \
  --cloud-init-user-data "$USER_DATA" \
  --network-interfaces "[{\"name\": \"eth0\", \"subnet_id\": \"$SUBNET_ID\", \"ip_address\": {}, \"public_ip_address\": {}}]" \
  --format jsonpath='{.metadata.id}')
```

The command creates the VM with a boot disk that has the same settings as the boot disk of the training VM. It uses the same `USER_DATA` variable and cloud-init configuration as the training VM.

**Go SDK**

1. Create a boot disk:

   ```go theme={null}
   inferenceDiskOperation, err :=
       sdk.Services().Compute().V1().Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "inference-vm-disk-1",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 50,
                   },
                   BlockSizeBytes: 4096,
                   Type: compute.DiskSpec_NETWORK_SSD,
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
   if _, err = inferenceDiskOperation.Wait(ctx); err != nil {
       return err
   }
   inferenceBootDiskID := inferenceDiskOperation.ResourceID()
   ```

   The code creates a 50 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Create a VM with one GPU for inference:

   ```go theme={null}
   inferenceNetworkName :=
       "single-gpu-node-compute-api-" +
           "network-interface"
   inferenceResources := &compute.ResourcesSpec{
       Platform: "gpu-h100-sxm",
       Size: &compute.ResourcesSpec_Preset{
           Preset: "1gpu-16vcpu-200gb",
       },
   }
   inferenceBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ExistingDisk{
           ExistingDisk: &compute.ExistingDisk{
               Id: inferenceBootDiskID,
           },
       },
   }
   inferenceNetwork := &compute.NetworkInterfaceSpec{
       Name:            inferenceNetworkName,
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   inferenceSpec := &compute.InstanceSpec{
       Resources:         inferenceResources,
       BootDisk:          inferenceBootDisk,
       CloudInitUserData: userData,
       NetworkInterfaces: []*compute.NetworkInterfaceSpec{
           inferenceNetwork,
       },
   }
   inferenceVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "inference-vm",
               },
               Spec: inferenceSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = inferenceVMOperation.Wait(ctx); err != nil {
       return err
   }
   inferenceVMID := inferenceVMOperation.ResourceID()
   ```

**Python SDK**

1. Create a boot disk:

   ```python theme={null}
   inference_disk_service = DiskServiceClient(sdk)
   inference_disk_operation = await inference_disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(
               name="inference-vm-disk-1",
           ),
           spec=DiskSpec(
               block_size_bytes=4096,
               type=DiskSpec.DiskType.NETWORK_SSD,
               source_image_family=SourceImageFamily(
                   image_family="ubuntu24.04-cuda13.0",
               ),
               size_gibibytes=50,
           ),
       ),
   )
   await inference_disk_operation.wait()
   inference_boot_disk_id = inference_disk_operation.resource_id
   ```

   The code creates a 50 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Create a VM with one GPU for inference:

   ```python theme={null}
   inference_network_name = (
       "single-gpu-node-compute-api-"
       "network-interface"
   )
   inference_service = InstanceServiceClient(sdk)
   inference_vm_operation = await inference_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="inference-vm"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="gpu-h100-sxm",
                   preset="1gpu-16vcpu-200gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   existing_disk=ExistingDisk(
                       id=inference_boot_disk_id,
                   ),
               ),
               cloud_init_user_data=user_data,
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name=inference_network_name,
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await inference_vm_operation.wait()
   inference_vm_id = inference_vm_operation.resource_id
   ```

**JavaScript SDK**

1. Create a boot disk:

   ```ts theme={null}
   const inferenceDiskService = new DiskService(sdk);
   const inferenceDiskOperation =
     await inferenceDiskService.create(
       CreateDiskRequest.create({
         metadata: ResourceMetadata.create({
           name: "inference-vm-disk-1",
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
             sizeGibibytes: 50,
           },
         }),
       }),
     ).result;
   await inferenceDiskOperation.wait();
   const inferenceBootDiskId =
     inferenceDiskOperation.resourceId();
   ```

   The code creates a 50 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Create a VM with one GPU for inference:

   ```ts theme={null}
   const inferenceNetworkName =
     "single-gpu-node-compute-api-" +
     "network-interface";
   const inferenceService = new InstanceService(sdk);
   const inferenceVmOperation = await inferenceService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "inference-vm",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "gpu-h100-sxm",
           size: {
             $case: "preset",
             preset: "1gpu-16vcpu-200gb",
           },
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode:
             AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "existingDisk",
             existingDisk: ExistingDisk.create({
               id: inferenceBootDiskId,
             }),
           },
         }),
         cloudInitUserData: userData,
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: inferenceNetworkName,
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
       }),
     }),
   ).result;
   await inferenceVmOperation.wait();
   const inferenceVmId = inferenceVmOperation.resourceId();
   ```

## Connect to the VMs

Connect to the VM for training via SSH:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. Open the page of the VM and copy its public IP address.
3. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh <username>@<public_IP_address>
   ```

   Use the username that you specified when creating the VM.

**CLI**

1. Get your VM's public IP address and save it to an environment variable:

   ```bash theme={null}
   export TR_PUBLIC_IP_ADDRESS=$(nebius compute instance get \
     --id $TR_VM_ID \
     --format json \
     | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@$TR_PUBLIC_IP_ADDRESS
   ```

**Go SDK**

1. Get your VM's public IP address:

   ```go theme={null}
   trainingInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: trainingVMID,
           },
       )
   if err != nil {
       return err
   }
   trainingAddress := trainingInstance.GetStatus().
       GetNetworkInterfaces()[0].
       GetPublicIpAddress().GetAddress()
   trainingPublicIP := strings.Split(trainingAddress, "/")[0]
   if trainingPublicIP == "" {
       return fmt.Errorf("training VM public IP is missing")
   }
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@<training_public_IP_address>
   ```

**Python SDK**

1. Get your VM's public IP address:

   ```python theme={null}
   training_ip_service = InstanceServiceClient(sdk)
   training_instance = await training_ip_service.get(
       GetInstanceRequest(id=training_vm_id),
   )
   training_address = (
       training_instance.status.network_interfaces[0]
       .public_ip_address.address
   )
   training_public_ip = training_address.split("/")[0]
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@<training_public_IP_address>
   ```

**JavaScript SDK**

1. Get your VM's public IP address:

   ```ts theme={null}
   const trainingIpService = new InstanceService(sdk);
   const trainingInstance = await trainingIpService.get(
     GetInstanceRequest.create({
       id: trainingVmId,
     }),
   );
   const trainingAddress = trainingInstance.status
     ?.networkInterfaces[0]?.publicIpAddress?.address;
   const trainingPublicIp = trainingAddress?.split("/")[0];
   if (!trainingPublicIp) {
     throw new Error("training VM public IP is missing");
   }
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@<training_public_IP_address>
   ```

Connect to the VM for inference via SSH:

**Web console**

Do the same steps as for the training VM. Open the page of the inference VM, copy its public IP address and then connect to the inference VM:

```bash theme={null}
ssh <username>@<public_IP_address>
```

Use the username that you specified when creating the inference VM.

**CLI**

1. Get your VM's public IP address and save it to an environment variable:

   ```bash theme={null}
   export INF_PUBLIC_IP_ADDRESS=$(nebius compute instance get \
     --id $INF_VM_ID \
     --format json \
     | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@$INF_PUBLIC_IP_ADDRESS
   ```

**Go SDK**

1. Get your VM's public IP address:

   ```go theme={null}
   inferenceInstance, err := sdk.Services().Compute().V1().
       Instance().Get(
           ctx,
           &compute.GetInstanceRequest{
               Id: inferenceVMID,
           },
       )
   if err != nil {
       return err
   }
   inferenceAddress := inferenceInstance.GetStatus().
       GetNetworkInterfaces()[0].
       GetPublicIpAddress().GetAddress()
   inferencePublicIP := strings.Split(inferenceAddress, "/")[0]
   if inferencePublicIP == "" {
       return fmt.Errorf("inference VM public IP is missing")
   }
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@<inference_public_IP_address>
   ```

**Python SDK**

1. Get your VM's public IP address:

   ```python theme={null}
   inference_ip_service = InstanceServiceClient(sdk)
   inference_instance = await inference_ip_service.get(
       GetInstanceRequest(id=inference_vm_id),
   )
   inference_address = (
       inference_instance.status.network_interfaces[0]
       .public_ip_address.address
   )
   inference_public_ip = inference_address.split("/")[0]
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@<inference_public_IP_address>
   ```

**JavaScript SDK**

1. Get your VM's public IP address:

   ```ts theme={null}
   const inferenceIpService = new InstanceService(sdk);
   const inferenceInstance = await inferenceIpService.get(
     GetInstanceRequest.create({
       id: inferenceVmId,
     }),
   );
   const inferenceAddress = inferenceInstance.status
     ?.networkInterfaces[0]?.publicIpAddress?.address;
   const inferencePublicIp = inferenceAddress?.split("/")[0];
   if (!inferencePublicIp) {
     throw new Error("inference VM public IP is missing");
   }
   ```

2. Use the public IP address to connect to the VM:

   ```bash theme={null}
   ssh user@<inference_public_IP_address>
   ```

## What's next

* Learn about [VM and GPU types](https://docs.nebius.com/compute/virtual-machines/types.md)
* Learn how to [create different types of VMs](https://docs.nebius.com/compute/virtual-machines/manage.md)
* Learn more about [VM networking](https://docs.nebius.com/compute/virtual-machines/network.md)
* Learn how to work with [GPU clusters](https://docs.nebius.com/compute/clusters/gpu/index.md)

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
