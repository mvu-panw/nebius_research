# Importing your own image into Compute

Source: https://docs.nebius.com/compute/storage/import-image

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Importing your own image into Compute

You can import an image file into Nebius AI Cloud, and create boot disks and virtual machines (VMs) based on your custom image. To make an import, upload an image file to a bucket in Object Storage and create an image in Compute.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Prepare an image that meets the following requirements:

   * BIOS mode
   * AMD64 or ARM64 architecture
   * `.vmdk`, `.vhd`, `.raw` or `.qcow2` format for the image file

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Prepare an image that meets the following requirements:

   * BIOS mode
   * AMD64 or ARM64 architecture
   * `.vmdk`, `.vhd`, `.raw` or `.qcow2` format for the image file

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Prepare an image that meets the following requirements:

   * BIOS mode
   * AMD64 or ARM64 architecture
   * `.vmdk`, `.vhd`, `.raw` or `.qcow2` format for the image file

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Prepare an image that meets the following requirements:

   * BIOS mode
   * AMD64 or ARM64 architecture
   * `.vmdk`, `.vhd`, `.raw` or `.qcow2` format for the image file

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Prepare an image that meets the following requirements:

   * BIOS mode
   * AMD64 or ARM64 architecture
   * `.vmdk`, `.vhd`, `.raw` or `.qcow2` format for the image file

## How to import an image and create a boot disk and a VM

1. [Create an Object Storage bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets).

   The bucket, image and VM should be in the same region.

2. [Upload](https://docs.nebius.com/object-storage/objects/upload-download.md#upload-a-single-file) your image file to this bucket.

3. Create an image based on the uploaded file:

   **Web console**

   1. Copy the key of the file object:

      1. In the [web console](https://console.nebius.com), go to  **Storage** → **Object Storage**.
      2. Open the bucket page.
      3. In the line of the uploaded object, click  → **Copy key**.

   2. Create the image in Nebius AI Cloud:

      1. In the web console, go to  **Storage** → **Disks**.

      2. Click **Create resource** → **Image**.

      3. In the window that opens, specify the name of your image.

      4. In the **Source** field, select **Object Storage file**.

      5. In the **Object Storage file** field, specify the copied object key.

         The value must meet the `s3://<bucket>/<object>` format. For example, `s3://nebius-bucket-test/my-image-file.qcow2`.

      6. Click **Create image**.

      The new image appears on the **Images** tab in  **Storage** → **Disks**.

   **CLI**

   ```bash theme={null}
   nebius compute image create \
      --name <image_name> \
      --source-storage-bucket-name <bucket_name> \
      --source-storage-object-name <object_name>
   ```

   For example, if the object of the image file has the `s3://nebius-bucket-test/my-image-file.qcow2` key:

   * `--source-storage-bucket-name` should be `nebius-bucket-test`
   * `--source-storage-object-name` should be `my-image-file.qcow2`

   > [!NOTE]
   >
   > By default, the AMD64 architecture is used for the image. If you want to use ARM64, add the `--cpu-architecture arm64` parameter to the command above.

   **Go SDK**

   ```go theme={null}
   imageOperation, err = sdk.Services().Compute().V1().
       Image().Create(
           ctx,
           &compute.CreateImageRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<image_name>",
               },
               Spec: &compute.ImageSpec{
                   Source: &compute.ImageSpec_SourceStorage_{
                       SourceStorage: &compute.ImageSpec_SourceStorage{
                           BucketName: "<bucket_name>",
                           ObjectName: "<object_name>",
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = imageOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   For example, if the object of the image file has the `s3://nebius-bucket-test/my-image-file.qcow2` key:

   * `BucketName` should be `nebius-bucket-test`
   * `ObjectName` should be `my-image-file.qcow2`

   **Python SDK**

   ```python theme={null}
   image_service = ImageServiceClient(sdk)
   create_image_operation = await image_service.create(
       CreateImageRequest(
           metadata=ResourceMetadata(
               name="<image_name>",
           ),
           spec=ImageSpec(
               source_storage=ImageSpec.SourceStorage(
                   bucket_name="<bucket_name>",
                   object_name="<object_name>",
               ),
           ),
       ),
   )
   await create_image_operation.wait()
   ```

   For example, if the object of the image file has the `s3://nebius-bucket-test/my-image-file.qcow2` key:

   * `bucket_name` should be `nebius-bucket-test`
   * `object_name` should be `my-image-file.qcow2`

   **JavaScript SDK**

   ```ts theme={null}
   const createBucketImageService = new ImageService(sdk);
   const createBucketImageOperation =
     await createBucketImageService.create(
       CreateImageRequest.create({
         metadata: ResourceMetadata.create({
           name: "<image_name>",
         }),
         spec: ImageSpec.create({
           source: {
             $case: "sourceStorage",
             sourceStorage: ImageSpec_SourceStorage.create({
               bucketName: "<bucket_name>",
               objectName: "<object_name>",
             }),
           },
         }),
       }),
     ).result;
   await createBucketImageOperation.wait();
   ```

   For example, if the object of the image file has the `s3://nebius-bucket-test/my-image-file.qcow2` key:

   * `bucketName` should be `nebius-bucket-test`
   * `objectName` should be `my-image-file.qcow2`

4. When the image is ready, [create a boot disk](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk) with it.

5. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with the new boot disk.

6. (Optional) If you don't need the image file in the bucket, delete it. The image in Compute won't use it anymore.
