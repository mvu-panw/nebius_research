# How to send an API request using the JavaScript SDK

Source: https://docs.nebius.com/sdk/javascript/send-request

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to send an API request using the JavaScript SDK

The SDK provides service clients grouped by Nebius AI Cloud service and API version. When your application calls a typed client method, the SDK constructs and sends the corresponding API request.

For mutating operations, such as creating, updating and deleting resources, the SDK returns an operation object. If an operation is asynchronous, call `wait` to wait until it is completed.

The following example creates a [Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md) (VM).

1. [Install the JavaScript SDK, create a service account and generate its credentials file](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Create a JavaScript file with the following code.

   This script initializes the SDK with the [service account credentials file prepared in the previous step](https://docs.nebius.com/sdk/javascript/install-auth.md#initialization-and-authentication).

   ```javascript theme={null}
   import { SDK } from '@nebius/js-sdk';
   import {
     AttachedDiskSpec_AttachMode,
     CreateDiskRequest,
     CreateInstanceRequest,
     DiskService as DiskServiceClient,
     DiskSpec_DiskType,
     InstanceService as InstanceServiceClient,
   } from '@nebius/js-sdk/api/nebius/compute/v1/index';
   import { CredentialsFileReader } from '@nebius/js-sdk/runtime/service_account/credentials_file';

   async function createInstance() {
     const sdk = new SDK({
       userAgentPrefix: '<application_name>/<application_version_or_comment>',
       parentId: '<project_ID>',
       credentials: new CredentialsFileReader('<credentials_file_path>'),
     });

     try {
       const diskService = new DiskServiceClient(sdk);
       const instanceService = new InstanceServiceClient(sdk);

       // Create the boot disk.
       const diskOperation = await diskService.create(
         CreateDiskRequest.create({
           metadata: {
             parentId: '<project_ID>',
             name: 'my-boot-disk',
           },
           spec: {
             size: {
               $case: 'sizeGibibytes',
               sizeGibibytes: 93,
             },
             type: DiskSpec_DiskType.NETWORK_SSD,
             source: {
               $case: 'sourceImageFamily',
               sourceImageFamily: {
                 imageFamily: '<image_family_name>',
               },
             },
           },
         }),
       ).result;

       await diskOperation.wait();
       console.log('Boot disk ID:', diskOperation.resourceId());

       // Create the VM that uses the boot disk.
       const instanceOperation = await instanceService.create(
         CreateInstanceRequest.create({
           metadata: {
             parentId: '<project_ID>',
             name: 'my-vm',
           },
           spec: {
             resources: {
               platform: '<platform_name>',
               size: {
                 $case: 'preset',
                 preset: '<preset_name>',
               },
             },
             networkInterfaces: [
               {
                 name: 'eth0',
                 subnetId: '<subnet_ID>',
                 ipAddress: {},
               },
             ],
             bootDisk: {
               attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
               type: {
                 $case: 'existingDisk',
                 existingDisk: {
                   id: diskOperation.resourceId(),
                 },
               },
               deviceId: 'boot-disk',
             },
           },
         }),
       ).result;

       await instanceOperation.wait();
       console.log('VM ID:', instanceOperation.resourceId());
     } finally {
       await sdk.close();
     }
   }

   await createInstance();
   ```

   In the script, set the following parameters:

   * `<application_name>/<application_version_or_comment>`: Application or library name and optional version or comment.
   * `<credentials_file_path>`: Path to the service account credentials file.
   * `<project_ID>`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
   * `<image_family_name>`: [Boot disk image family](https://docs.nebius.com/compute/storage/boot-disk-images.md#image-family), for example, `ubuntu24.04-driverless`.
   * `<platform_name>`: [Compute platform](https://docs.nebius.com/compute/virtual-machines/types.md), for example, `cpu-e2`.
   * `<preset_name>`: [Resource preset](https://docs.nebius.com/compute/virtual-machines/types.md) available for the selected platform, for example, `2vcpu-8gb` for `cpu-e2`.
   * `<subnet_ID>`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

3. Execute the file:

   ```bash theme={null}
   node <file_name>.mjs
   ```

After you run the example, delete the VM and its boot disk if you no longer need them. Otherwise, Compute continues [charging](https://docs.nebius.com/compute/resources/pricing.md) for these resources.
