# How to send an API request using the Python SDK

Source: https://docs.nebius.com/sdk/python/send-request

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to send an API request using the Python SDK

The SDK provides service clients grouped by Nebius AI Cloud service and API version. When your application calls a typed client method, the SDK constructs and sends the corresponding API request.

For mutating operations, such as creating, updating and deleting resources, the SDK returns an operation object. If an operation is asynchronous, call `wait` to wait until it is completed.

The following example creates a [Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md) (VM).

1. [Install the Python SDK, create a service account and prepare its authentication credentials](https://docs.nebius.com/sdk/python/install-auth.md).

2. Create a Python file with the following code.

   This script initializes the SDK with the [authentication credentials prepared in the previous step](https://docs.nebius.com/sdk/python/install-auth.md#initialization-and-authentication).

   ```python theme={null}
   import asyncio

   from nebius.api.nebius.common.v1 import ResourceMetadata
   from nebius.api.nebius.compute.v1 import (
       AttachedDiskSpec,
       CreateDiskRequest,
       CreateInstanceRequest,
       DiskServiceClient,
       DiskSpec,
       ExistingDisk,
       InstanceServiceClient,
       InstanceSpec,
       IPAddress,
       NetworkInterfaceSpec,
       ResourcesSpec,
       SourceImageFamily,
   )
   from nebius.sdk import SDK


   async def create_instance() -> None:
       # Initialize the SDK with the service account private key file.
       sdk = SDK(
           user_agent_prefix="<application_name>/<application_version_or_comment>",
           parent_id="<project_ID>",
           service_account_private_key_file_name="<private_key_file_path>",
           service_account_public_key_id="<public_key_ID>",
           service_account_id="<service_account_ID>",
       )

       async with sdk:
           disk_service = DiskServiceClient(sdk)
           instance_service = InstanceServiceClient(sdk)

           # Create the boot disk.
           disk_operation = await disk_service.create(
               CreateDiskRequest(
                   metadata=ResourceMetadata(
                       parent_id="<project_ID>",
                       name="my-boot-disk",
                   ),
                   spec=DiskSpec(
                       size_gibibytes=93,
                       type=DiskSpec.DiskType.NETWORK_SSD,
                       source_image_family=SourceImageFamily(
                           image_family="<image_family_name>",
                       ),
                   ),
               )
           )

           await disk_operation.wait()

           # Create the VM that uses the boot disk.
           instance_operation = await instance_service.create(
               CreateInstanceRequest(
                   metadata=ResourceMetadata(
                       parent_id="<project_ID>",
                       name="my-vm",
                   ),
                   spec=InstanceSpec(
                       resources=ResourcesSpec(
                           platform="<platform_name>",
                           preset="<preset_name>",
                       ),
                       network_interfaces=[
                           NetworkInterfaceSpec(
                               name="eth0",
                               subnet_id="<subnet_ID>",
                               ip_address=IPAddress(),
                           ),
                       ],
                       boot_disk=AttachedDiskSpec(
                           attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                           existing_disk=ExistingDisk(
                               id=disk_operation.resource_id,
                           ),
                           device_id="boot-disk",
                       ),
                   ),
               )
           )

           await instance_operation.wait()


   if __name__ == "__main__":
       asyncio.run(create_instance())
   ```

   In the script, set the following parameters:

   * `<application_name>/<application_version_or_comment>`: Application or library name and optional version or comment.
   * `<private_key_file_path>`: Path to the private key file.
   * `<public_key_ID>`: Authorized key ID.
   * `<service_account_ID>`: Service account ID.
   * `<project_ID>`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
   * `<image_family_name>`: [Boot disk image family](https://docs.nebius.com/compute/storage/boot-disk-images.md#image-family), for example, `ubuntu24.04-driverless`.
   * `<platform_name>`: [Compute platform](https://docs.nebius.com/compute/virtual-machines/types.md), for example, `cpu-e2`.
   * `<preset_name>`: [Resource preset](https://docs.nebius.com/compute/virtual-machines/types.md) available for the selected platform, for example, `2vcpu-8gb` for `cpu-e2`.
   * `<subnet_ID>`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

3. Execute the file:

   ```bash theme={null}
   python3 <file_name>.py
   ```

After you run the example, delete the VM and its boot disk if you no longer need them. Otherwise, Compute continues [charging](https://docs.nebius.com/compute/resources/pricing.md) for these resources.
