# Getting started with Compute: Host an LLM on Nebius AI Cloud

Source: https://docs.nebius.com/compute/quickstart-host-model

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Compute: Host an LLM on Nebius AI Cloud

You can create a virtual machine (VM) in Nebius AI Cloud, deploy the [Qwen/Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) large language model (LLM) on the VM and then use [Open WebUI](https://openwebui.com/) to provide access to the model in a browser.

## Before you start

Meet the following prerequisites, depending on the preferred interface:

**Web console**

Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. To extract JSON data from the CLI output, install [jq](https://jqlang.github.io/jq/):

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

## Create the VM

**Web console**

1. Go to the [web console](https://console.nebius.com), click **Create resource** and then select **Virtual machine**.

2. On the VM creation page that opens, set the following parameters:
   * **Platform**: NVIDIA® H100 NVLink with Intel Sapphire Rapids.

   * **Preset**: 1 GPU - 16 CPUs - 200 GiB RAM.

   * **Boot disk image**: Ubuntu 22.04 LTS for NVIDIA® GPUs (CUDA® 12). For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

   * **Boot disk size**: 300 GiB SSD.

   * **Network**: Select the **Public IP address: Auto assign static IP** option.

   * **Username and SSH key**: Select the public key that you created earlier.

     In this field, do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

3. Click **Create VM**.

The given example assumes that you work with a VM that has a public address, so you can later [connect to this VM by SSH](#connect-to-the-vm). However, if you need an isolated VM, do not assign a public address. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**CLI**

1. Create a boot disk and save its ID to an environment variable:

   ```bash theme={null}
   export BOOT_DISK_ID=$(nebius compute disk create \
     --name openwebui-disk-1 \
     --size-gibibytes 300 \
     --type network_ssd \
     --source-image-family-image-family ubuntu24.04-cuda13.0 \
     --block-size-bytes 4096 \
     --format jsonpath='{.metadata.id}')
   ```

   The command creates a 300 GiB SSD disk with a 4 KiB block size, and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Get the default subnet ID and save it to an environment variable:

   ```bash theme={null}
   export SUBNET_ID=$(nebius vpc subnet list \
     --format jsonpath='{.items[0].metadata.id}')
   ```

3. Create the VM with one GPU:

   ```bash theme={null}
   export USER_DATA=$(jq -Rrs '.' <<EOF
   #cloud-config
   users:
     - name: <username>
       sudo: ALL=(ALL) NOPASSWD:ALL
       shell: /bin/bash
       ssh_authorized_keys:
         - $(cat ~/.ssh/id_ed25519.pub)
   EOF
   )

   export VM_ID=$(nebius compute instance create \
     --name openwebui \
     --resources-platform gpu-h100-sxm \
     --resources-preset 1gpu-16vcpu-200gb \
     --boot-disk-existing-disk-id "$BOOT_DISK_ID" \
     --boot-disk-attach-mode READ_WRITE \
     --cloud-init-user-data "$USER_DATA" \
     --network-interfaces "[{\"name\": \"default-subnet\", \"subnet_id\": \"$SUBNET_ID\", \"ip_address\": {}, \"public_ip_address\": {}}]" \
     --format jsonpath='{.metadata.id}')
   ```

The given example assumes that you work with a VM that has a public address, so you can later [connect to this VM by SSH](#connect-to-the-vm). However, if you need an isolated VM without a public address, remove `"public_ip_address": {}` from the `--network-interfaces` parameter. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**Go SDK**

1. Create a boot disk:

   ```go theme={null}
   bootDiskOperation, err := sdk.Services().Compute().V1().
       Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "openwebui-disk-1",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 300,
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
   if _, err = bootDiskOperation.Wait(ctx); err != nil {
       return err
   }
   bootDiskID := bootDiskOperation.ResourceID()
   ```

   The code creates a 300 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Get the default subnet ID:

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

3. Create the VM with one GPU:

   ```go theme={null}
   hostResources := &compute.ResourcesSpec{
       Platform: "gpu-h100-sxm",
       Size: &compute.ResourcesSpec_Preset{
           Preset: "1gpu-16vcpu-200gb",
       },
   }
   hostBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ExistingDisk{
           ExistingDisk: &compute.ExistingDisk{
               Id: bootDiskID,
           },
       },
   }
   hostNetworkInterface := &compute.NetworkInterfaceSpec{
       Name:            "default-subnet",
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   hostInstanceSpec := &compute.InstanceSpec{
       Resources: hostResources,
       BootDisk:  hostBootDisk,
       NetworkInterfaces: []*compute.NetworkInterfaceSpec{
           hostNetworkInterface,
       },
       CloudInitUserData: userData,
   }
   hostOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "openwebui",
               },
               Spec: hostInstanceSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = hostOperation.Wait(ctx); err != nil {
       return err
   }
   ```

The given example assumes that you work with a VM that has a public address, so you can later [connect to this VM by SSH](#connect-to-the-vm). However, if you need an isolated VM without a public address, remove the public IP address specification from the network interface parameters. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**Python SDK**

1. Create a boot disk:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   boot_disk_operation = await disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(
               name="openwebui-disk-1",
           ),
           spec=DiskSpec(
               block_size_bytes=4096,
               type=DiskSpec.DiskType.NETWORK_SSD,
               source_image_family=SourceImageFamily(
                   image_family="ubuntu24.04-cuda13.0",
               ),
               size_gibibytes=300,
           ),
       ),
   )
   await boot_disk_operation.wait()
   boot_disk_id = boot_disk_operation.resource_id
   ```

   The code creates a 300 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Get the default subnet ID:

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnets = await subnet_service.list(ListSubnetsRequest())
   if not subnets.items:
       raise ValueError("no subnets found")
   subnet_id = subnets.items[0].metadata.id
   ```

3. Create the VM with one GPU:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   host_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="openwebui"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="gpu-h100-sxm",
                   preset="1gpu-16vcpu-200gb",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   existing_disk=ExistingDisk(id=boot_disk_id),
               ),
               cloud_init_user_data=user_data,
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="default-subnet",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await host_operation.wait()
   ```

The given example assumes that you work with a VM that has a public address, so you can later [connect to this VM by SSH](#connect-to-the-vm). However, if you need an isolated VM without a public address, remove the public IP address specification from the network interface parameters. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

**JavaScript SDK**

1. Create a boot disk:

   ```ts theme={null}
   const diskService = new DiskService(sdk);
   const bootDiskOperation = await diskService.create(
     CreateDiskRequest.create({
       metadata: ResourceMetadata.create({
         name: "openwebui-disk-1",
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
           sizeGibibytes: 300,
         },
       }),
     }),
   ).result;
   await bootDiskOperation.wait();
   const bootDiskId = bootDiskOperation.resourceId();
   ```

   The code creates a 300 GiB SSD disk with a 4 KiB block size and an Ubuntu boot image with pre-installed NVIDIA® GPU drivers. For details about boot disk images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

2. Get the default subnet ID:

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

3. Create the VM with one GPU:

   ```ts theme={null}
   const instanceService = new InstanceService(sdk);
   const hostOperation = await instanceService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "openwebui",
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
               id: bootDiskId,
             }),
           },
         }),
         cloudInitUserData: userData,
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "default-subnet",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
       }),
     }),
   ).result;
   await hostOperation.wait();
   ```

The given example assumes that you work with a VM that has a public address, so you can later [connect to this VM by SSH](#connect-to-the-vm). However, if you need an isolated VM without a public address, remove the public IP address specification from the network interface parameters. To access the VM, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md) later. This approach enhances security and still provides access to the VM within the same subnet.

For more information about creating VMs and managing their network parameters, see [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md).

## Connect to the VM

1. Get the public IP address of the VM:

   **Web console**

   1. Open the VM page.
   2. In the **Network** block, copy the **Public IPv4** value.

   **CLI**

   Run the following command:

   ```bash theme={null}
   export PUBLIC_IP_ADDRESS=$(nebius compute instance get-by-name \
     --name openwebui \
     --format json \
     | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
   ```

   **Go SDK**

   ```go theme={null}
   publicInstance, err := sdk.Services().Compute().V1().
       Instance().GetByName(
           ctx,
           &common.GetByNameRequest{
               Name: "openwebui",
           },
       )
   if err != nil {
       return err
   }
   publicAddress := publicInstance.GetStatus().
       GetNetworkInterfaces()[0].
       GetPublicIpAddress().GetAddress()
   publicIPAddress := strings.Split(publicAddress, "/")[0]
   if publicIPAddress == "" {
       return fmt.Errorf("public IP address is missing")
   }
   ```

   **Python SDK**

   ```python theme={null}
   public_ip_service = InstanceServiceClient(sdk)
   public_instance = await public_ip_service.get_by_name(
       GetByNameRequest(name="openwebui"),
   )
   public_address = (
       public_instance.status.network_interfaces[0]
       .public_ip_address.address
   )
   public_ip_address = public_address.split("/")[0]
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const publicIpService = new InstanceService(sdk);
   const publicInstance = await publicIpService.getByName(
     GetByNameRequest.create({
       name: "openwebui",
     }),
   );
   const publicAddress = publicInstance.status
     ?.networkInterfaces[0]?.publicIpAddress?.address;
   const publicIpAddress = publicAddress?.split("/")[0];
   if (!publicIpAddress) {
     throw new Error("public IP address is missing");
   }
   ```

2. Connect to the VM:

   ```bash theme={null}
   ssh <username>@<ip_address>
   ```

   Specify the received public IP address and the username that you set during the VM creation.

## Create a virtual environment and install the necessary packages

To work with Open WebUI, you need a dedicated [virtual environment](https://docs.python.org/3/tutorial/venv.html). It enables you to set up and run the OpenWebUI server in isolation from other software on the VM. To create a virtual environment, use [Miniconda](https://docs.anaconda.com/miniconda/).

To configure the environment:

1. Download and install the latest Miniconda version:

   ```bash theme={null}
   mkdir -p ~/miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   rm ~/miniconda3/miniconda.sh
   ```

2. Initialize Miniconda:

   ```bash theme={null}
   source ~/miniconda3/bin/activate
   ```

   On initialization, Miniconda activates its `base` environment.

3. Create an `OpenWebUI` environment with Python 3.11:

   ```bash theme={null}
   conda create -n OpenWebUI python=3.11
   conda init bash
   echo "conda activate OpenWebUI " >> ~/.bashrc
   source ~/.bashrc
   ```

   This command creates and activates a new environment.

4. Install [Ollama](https://ollama.com/), which provides access to the model:

   ```bash theme={null}
   curl -fsSL https://ollama.com/install.sh | sh
   ```

5. Install Open WebUI:

   ```bash theme={null}
   pip install open-webui
   ```

## Start the Open WebUI server

1. Start the server:

   ```bash theme={null}
   open-webui serve
   ```

2. Open the Open WebUI interface in the browser. To do this, enter the `http://<public_ip_address>:8080` address in the search bar.

3. In the Open WebUI interface, create an account to work with LLMs locally within the VM. For details on working with Open WebUI, see [their documentation](https://docs.openwebui.com/).

If you need to restart the server, use the same command: `open-webui serve`.

## Download the Qwen/Qwen2.5-72B-Instruct model

1. In Open WebUI, click **Select a model**.
2. Paste `qwen2.5:72b` into the search bar.
3. Click **Pull "qwen2.5:72b" from Ollama** and wait for the download to finish.
4. Click **Select a model** again and then choose Qwen/Qwen2.5-72B-Instruct.

Now you can chat with the model in the browser.

## Make Open WebUI start automatically

With the current configuration, you need to manually start the Open WebUI server every time you connect to your VM. Alternatively, you can configure the server to start up whenever the VM starts. To do this:

1. Create a `systemd` service file for Open WebUI and open the file in an editor:

   ```bash theme={null}
   sudo nano /etc/systemd/system/openwebui.service
   ```

2. Paste the following contents into the file and save it. Specify the username that you set during the VM creation:

   ```ini theme={null}
   [Unit]
   Description=OpenWebUI Server
   After=network.target
   [Service]
   User=<username>
   WorkingDirectory=/home/<username>/
   ExecStart=/home/<username>/miniconda3/envs/OpenWebUI/bin/open-webui serve
   Restart=always
   [Install]
   WantedBy=multi-user.target
   ```

3. To make the new service file recognizable, reload `systemd`:

   ```bash theme={null}
   sudo systemctl daemon-reload
   ```

4. To start automatically and immediately, enable the `systemd` service:

   ```bash theme={null}
   sudo systemctl enable openwebui.service
   sudo systemctl start openwebui.service
   ```

5. Verify that the service is running:

   ```bash theme={null}
   sudo systemctl status openwebui.service
   ```

Whenever you start up your VM in the web console, Open WebUI now automatically launches in the background. You can directly access it in the browser at `http://ip_address:8080` and work with the Qwen/Qwen2.5-72B-Instruct model.
