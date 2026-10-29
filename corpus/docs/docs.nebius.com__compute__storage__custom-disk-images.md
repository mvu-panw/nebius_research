# Creating custom boot disk images

Source: https://docs.nebius.com/compute/storage/custom-disk-images

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating custom boot disk images

*Custom images* allow you to quickly [create virtual machines (VMs)](#how-to-create-a-vm-from-a-custom-image) or boot disks with all the necessary software, OS and configuration, which can greatly reduce infrastructure deployment time and ensure consistency across environments.

You can [create](#how-to-create-a-custom-boot-disk-image), [edit or delete](#how-to-edit-or-delete-a-custom-boot-disk-image) custom [boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md) in the web console, by using the CLI or by using a Nebius SDK. Alternatively, you can create custom boot disk images by using [Packer with the Nebius plug-in](https://docs.nebius.com/compute/storage/packer.md).

## Prerequisites

**Web console**

1. Make sure that you have enough quotas for images (**Number of images** and **Total storage capacity of all images**). You can view quotas and request changes on the [Administration → Limits → Quotas](https://console.nebius.com/limits/quotas) page of the web console.
2. Prepare the source from which the image inherits configuration and architecture. Choose one of the following types of sources:

   * Boot disk. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md) and install the software that the image should inherit. The image will be based on the boot disk of this VM and will include the installed software.
   * Disk snapshot. [Create a snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md#how-to-create-a-snapshot) from a boot disk and reuse this snapshot for the image.
   * File with the ready image. [Upload an image file to a bucket](https://docs.nebius.com/object-storage/objects/upload-download.md#upload-a-single-file) in Object Storage and use this file to create the image.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure that you have enough quotas for images (**Number of images** and **Total storage capacity of all images**). You can view quotas and request changes on the [Administration → Limits → Quotas](https://console.nebius.com/limits/quotas) page of the web console.
3. Prepare the source from which the image inherits configuration and architecture. Choose one of the following types of sources:

   * Boot disk. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md) and install the software that the image should inherit. The image will be based on the boot disk of this VM and will include the installed software.
   * Disk snapshot. [Create a snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md#how-to-create-a-snapshot) from a boot disk and reuse this snapshot for the image.
   * File with the ready image. [Upload an image file to a bucket](https://docs.nebius.com/object-storage/objects/upload-download.md#upload-a-single-file) in Object Storage and use this file to create the image.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure that you have enough quotas for images (**Number of images** and **Total storage capacity of all images**). You can view quotas and request changes on the [Administration → Limits → Quotas](https://console.nebius.com/limits/quotas) page of the web console.
3. Prepare the source from which the image inherits configuration and architecture. Choose one of the following types of sources:

   * Boot disk. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md) and install the software that the image should inherit. The image will be based on the boot disk of this VM and will include the installed software.
   * Disk snapshot. [Create a snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md#how-to-create-a-snapshot) from a boot disk and reuse this snapshot for the image.
   * File with the ready image. [Upload an image file to a bucket](https://docs.nebius.com/object-storage/objects/upload-download.md#upload-a-single-file) in Object Storage and use this file to create the image.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure that you have enough quotas for images (**Number of images** and **Total storage capacity of all images**). You can view quotas and request changes on the [Administration → Limits → Quotas](https://console.nebius.com/limits/quotas) page of the web console.
3. Prepare the source from which the image inherits configuration and architecture. Choose one of the following types of sources:

   * Boot disk. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md) and install the software that the image should inherit. The image will be based on the boot disk of this VM and will include the installed software.
   * Disk snapshot. [Create a snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md#how-to-create-a-snapshot) from a boot disk and reuse this snapshot for the image.
   * File with the ready image. [Upload an image file to a bucket](https://docs.nebius.com/object-storage/objects/upload-download.md#upload-a-single-file) in Object Storage and use this file to create the image.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure that you have enough quotas for images (**Number of images** and **Total storage capacity of all images**). You can view quotas and request changes on the [Administration → Limits → Quotas](https://console.nebius.com/limits/quotas) page of the web console.
3. Prepare the source from which the image inherits configuration and architecture. Choose one of the following types of sources:

   * Boot disk. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm), [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md) and install the software that the image should inherit. The image will be based on the boot disk of this VM and will include the installed software.
   * Disk snapshot. [Create a snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md#how-to-create-a-snapshot) from a boot disk and reuse this snapshot for the image.
   * File with the ready image. [Upload an image file to a bucket](https://docs.nebius.com/object-storage/objects/upload-download.md#upload-a-single-file) in Object Storage and use this file to create the image.

## How to create a custom boot disk image

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Disks**.

2. Click **Create resource** and then select **Image**.

3. In the window that opens, specify the name of your image.

4. Select the image source:

   * **Disk**: Create an image from a disk. Specify the following parameters:

     * **Project of source disk**: Project that the source disk of your image belongs to.
     * **Source disk**: Disk used as the source for your image. The image will retain the basic architecture, size and installed software of the source disk.

       > [!NOTE]
       >
       > You cannot create images from disks that are attached to a VM that is currently running. Stop the VM before attempting to create an image.

   * **Snapshot**: Create an image from a disk snapshot. Select the snapshot in the **Source snapshot** field.

   * **Object Storage file**: Import an image from a bucket. Specify the path to the file that you uploaded to the bucket. For example, `s3://nebius-bucket-test/my-image-file.qcow2`.

     You can copy and paste this value. To copy it, go to the bucket page. In the line of the uploaded image file, click  → **Copy key**.

     For information about requirements to the image file, see [Importing your own image into Compute](https://docs.nebius.com/compute/storage/import-image.md#prerequisites).

5. (Optional) Specify the image family. It represents a new or existing label used to group your custom images into a family. If you create a VM or a boot disk from this image family, you will use the latest image in the family.

6. (Optional) Specify the image description.

7. (Optional) Under **Advanced settings**, specify:

   * **Image family description**: Description of the family that your new image belongs to (if you specified one).
   * **Recommended platforms**: Comma-separated list of compatible [platforms](https://docs.nebius.com/compute/virtual-machines/types.md) that your image will use by default.
   * **Unsupported platforms**: Comma-separated list of platforms that your image architecture is *not* compatible with. Must be in the `<platform>=<description>` format. For example, `gpu-l40s-d=not supported`.

8. Click **Create image**.

The new image will appear on the **Images** tab in  **Storage** → **Disks**.

**CLI**

1. If the source disk for your image is attached to a VM that is currently running, stop it:

   ```bash theme={null}
   nebius compute instance stop --id <VM_ID>
   ```

   To get the VM ID, run `nebius compute instance list`.

2. Create an image:

   ```bash theme={null}
   nebius compute image create \
      --name <image_name> \
      --source-disk-id <disk_ID> \
      --parent-id <project_ID> \
      --source-disk-snapshot-id <snapshot_ID> \
      --source-storage-bucket-name <bucket_name> \
      --source-storage-object-name <object_name> \
      --image-family <image_family_name> \
      --description <image_description> \
      --image-family-human-readable <image_family_description> \
      --recommended-platforms "<platform_1>,<platform_2>,..." \
      --unsupported-platforms "<platform>=<description>"
   ```

   The CLI command includes the following parameters:

   * `--name`: Name of your image.

   * Image sources. Use one of the following:

     * `--source-disk-id`: ID of the source disk that you want to create an image from. Use together with `--parent-id`: ID of the project that the source disk belongs to.

       To get both `--parent-id` and `--source-disk-id`, run `nebius compute disk list`.

     * `--source-disk-snapshot-id`: ID of the [disk snapshot](https://docs.nebius.com/compute/storage/disk-snapshots.md) that you want to create an image from.

       To get the snapshot ID, run `nebius compute disk-snapshot list`.

     * `--source-storage-bucket-name` and `--source-storage-object-name`: Bucket and object that contain the source image.

       You can import an image from a file that meets certain [requirements](https://docs.nebius.com/compute/storage/import-image.md#prerequisites). To do so, upload this file to a bucket. Then, specify the name of this bucket in the `--source-storage-bucket-name` parameter and the name of the file in the `--source-storage-object-name` parameter.

       > **Creating an image from a bucket**
       >
       > ```bash theme={null}
       > nebius compute image create \
       >    --name <image_name> \
       >    --source-storage-bucket-name <bucket_name> \
       >    --source-storage-object-name <object_name>
       > ```

   * `--image-family` (optional): New or existing label used to group your custom images into a family. If you create a VM or a boot disk from this image family, you will use the latest image in the family.

   * `--description` (optional): Description of your image.

   * `--image-family-human-readable` (optional): Description of the family that your new image belongs to (if you specified one).

   * `--recommended-platforms` (optional): Comma-separated list of compatible [platforms](https://docs.nebius.com/compute/virtual-machines/types.md) that your image will use by default.

   * `--unsupported-platforms` (optional): Comma-separated list of platforms that your image architecture is *not* compatible with. Must be in the `<platform>=<description>` format. For example, `gpu-l40s-d=not supported`.

**Go SDK**

1. If the source disk for your image is attached to a VM that is currently running, stop it:

   ```go theme={null}
   operation, err := sdk.Services().Compute().V1().
       Instance().Stop(
           ctx,
           &compute.StopInstanceRequest{
               Id: "<VM_ID>",
           },
       )
   if err != nil {
       return err
   }
   if _, err = operation.Wait(ctx); err != nil {
       return err
   }
   ```

2. Create an image:

   ```go theme={null}
   familyDescription := "<image_family_description>"
   recommendedPlatforms := []string{}
   for _, platform := range strings.Split(
       "<platform_1>,<platform_2>,...",
       ",",
   ) {
       platform = strings.TrimSpace(platform)
       if platform != "" {
           recommendedPlatforms = append(recommendedPlatforms, platform)
       }
   }
   unsupportedPlatforms := map[string]string{}
   for _, platform := range strings.Split(
       "<platform>=<description>",
       ",",
   ) {
       parts := strings.SplitN(platform, "=", 2)
       if len(parts) == 2 && parts[0] != "" {
           unsupportedPlatforms[parts[0]] = parts[1]
       }
   }

   imageOperation, err := sdk.Services().Compute().V1().
       Image().Create(
           ctx,
           &compute.CreateImageRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<project_ID>",
                   Name:     "<image_name>",
               },
               Spec: &compute.ImageSpec{
                   Description: "<image_description>",
                   ImageFamily: "<image_family_name>",
                   Source: &compute.ImageSpec_SourceDiskId{
                       SourceDiskId: "<disk_ID>",
                   },
                   ImageFamilyHumanReadable: familyDescription,
                   RecommendedPlatforms: recommendedPlatforms,
                   UnsupportedPlatforms: unsupportedPlatforms,
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

   The code includes the following parameters:

   * `Metadata.ParentId`: ID of the project that the source disk belongs to.
   * `Metadata.Name`: Name of your image.
   * `Spec.Description` (optional): Description of your image.
   * `Spec.ImageFamily` (optional): New or existing label used to group your custom images into a family.
   * `Spec.Source.SourceDiskId`: ID of the source disk that you want to create an image from.
   * `Spec.ImageFamilyHumanReadable` (optional): Description of the family that your new image belongs to.
   * `Spec.RecommendedPlatforms` (optional): Compatible platforms that your image will use by default.
   * `Spec.UnsupportedPlatforms` (optional): Platforms that your image architecture is not compatible with.

   The Object Storage example uses `Metadata.Name`, `Spec.Source.SourceStorage.BucketName` and `Spec.Source.SourceStorage.ObjectName`.

   > **Creating an image from a bucket**
   >
   > ```go theme={null}
   > imageOperation, err = sdk.Services().Compute().V1().
   >     Image().Create(
   >         ctx,
   >         &compute.CreateImageRequest{
   >             Metadata: &common.ResourceMetadata{
   >                 Name: "<image_name>",
   >             },
   >             Spec: &compute.ImageSpec{
   >                 Source: &compute.ImageSpec_SourceStorage_{
   >                     SourceStorage: &compute.ImageSpec_SourceStorage{
   >                         BucketName: "<bucket_name>",
   >                         ObjectName: "<object_name>",
   >                     },
   >                 },
   >             },
   >         },
   >     )
   > if err != nil {
   >     return err
   > }
   > if _, err = imageOperation.Wait(ctx); err != nil {
   >     return err
   > }
   > ```

**Python SDK**

1. If the source disk for your image is attached to a VM that is currently running, stop it:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   stop_instance_operation = await instance_service.stop(
       StopInstanceRequest(id="<VM_ID>"),
   )
   await stop_instance_operation.wait()
   ```

2. Create an image:

   ```python theme={null}
   recommended_platforms = [
       platform.strip()
       for platform in "<platform_1>,<platform_2>,...".split(",")
       if platform.strip()
   ]
   unsupported_platforms = dict(
       platform.split("=", 1)
       for platform in "<platform>=<description>".split(",")
       if platform
   )

   image_service = ImageServiceClient(sdk)
   create_image_operation = await image_service.create(
       CreateImageRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="<image_name>",
           ),
           spec=ImageSpec(
               source_disk_id="<disk_ID>",
               image_family="<image_family_name>",
               description="<image_description>",
               image_family_human_readable="<image_family_description>",
               recommended_platforms=recommended_platforms,
               unsupported_platforms=unsupported_platforms,
           ),
       ),
   )
   await create_image_operation.wait()
   ```

   The code includes the following parameters:

   * `metadata.parent_id`: ID of the project that the source disk belongs to.
   * `metadata.name`: Name of your image.
   * `spec.source_disk_id`: ID of the source disk that you want to create an image from.
   * `spec.image_family` (optional): New or existing label used to group your custom images into a family.
   * `spec.description` (optional): Description of your image.
   * `spec.image_family_human_readable` (optional): Description of the family that your new image belongs to.
   * `spec.recommended_platforms` (optional): Compatible platforms that your image will use by default.
   * `spec.unsupported_platforms` (optional): Platforms that your image architecture is not compatible with.

   The Object Storage example uses `metadata.name`, `spec.source_storage.bucket_name` and `spec.source_storage.object_name`.

   > **Creating an image from a bucket**
   >
   > ```python theme={null}
   > image_service = ImageServiceClient(sdk)
   > create_image_operation = await image_service.create(
   >     CreateImageRequest(
   >         metadata=ResourceMetadata(
   >             name="<image_name>",
   >         ),
   >         spec=ImageSpec(
   >             source_storage=ImageSpec.SourceStorage(
   >                 bucket_name="<bucket_name>",
   >                 object_name="<object_name>",
   >             ),
   >         ),
   >     ),
   > )
   > await create_image_operation.wait()
   > ```

**JavaScript SDK**

1. If the source disk for your image is attached to a VM that is currently running, stop it:

   ```ts theme={null}
   const stopInstanceService = new InstanceService(sdk);
   const stopInstanceOperation = await stopInstanceService.stop(
     StopInstanceRequest.create({
       id: "<VM_ID>",
     }),
   ).result;
   await stopInstanceOperation.wait();
   ```

2. Create an image:

   ```ts theme={null}
   const recommendedPlatforms = "<platform_1>,<platform_2>,..."
     .split(",")
     .map((platform) => platform.trim())
     .filter(Boolean);
   const unsupportedPlatforms = Object.fromEntries(
     "<platform>=<description>"
       .split(",")
       .filter(Boolean)
       .map((platform) => platform.split("=", 2)),
   );

   const createImageService = new ImageService(sdk);
   const createImageOperation = await createImageService.create(
     CreateImageRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<project_ID>",
         name: "<image_name>",
       }),
       spec: ImageSpec.create({
         source: {
           $case: "sourceDiskId",
           sourceDiskId: "<disk_ID>",
         },
         imageFamily: "<image_family_name>",
         description: "<image_description>",
         imageFamilyHumanReadable: "<image_family_description>",
         recommendedPlatforms,
         unsupportedPlatforms,
       }),
     }),
   ).result;
   await createImageOperation.wait();
   ```

   The code includes the following parameters:

   * `metadata.parentId`: ID of the project that the source disk belongs to.
   * `metadata.name`: Name of your image.
   * `spec.source.sourceDiskId`: ID of the source disk that you want to create an image from.
   * `spec.imageFamily` (optional): New or existing label used to group your custom images into a family.
   * `spec.description` (optional): Description of your image.
   * `spec.imageFamilyHumanReadable` (optional): Description of the family that your new image belongs to.
   * `spec.recommendedPlatforms` (optional): Compatible platforms that your image will use by default.
   * `spec.unsupportedPlatforms` (optional): Platforms that your image architecture is not compatible with.

   The Object Storage example uses `metadata.name`, `spec.source.sourceStorage.bucketName` and `spec.source.sourceStorage.objectName`.

   > **Creating an image from a bucket**
   >
   > ```ts theme={null}
   > const createBucketImageService = new ImageService(sdk);
   > const createBucketImageOperation =
   >   await createBucketImageService.create(
   >     CreateImageRequest.create({
   >       metadata: ResourceMetadata.create({
   >         name: "<image_name>",
   >       }),
   >       spec: ImageSpec.create({
   >         source: {
   >           $case: "sourceStorage",
   >           sourceStorage: ImageSpec_SourceStorage.create({
   >             bucketName: "<bucket_name>",
   >             objectName: "<object_name>",
   >           }),
   >         },
   >       }),
   >     }),
   >   ).result;
   > await createBucketImageOperation.wait();
   > ```

## How to edit or delete a custom boot disk image

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Disks**.

2. Switch to the **Images** tab and open the image you want to access.

   The **Image overview** tab shows detailed information about the image and the source disk that it's based on.

3. On the image page, switch to the **Settings** tab.

4. Update the image name or click **Delete image** to delete it.

**CLI**

* To check the status of your image, run:

  ```bash theme={null}
  nebius compute image get computeimage-e***
  ```

  To get the image ID, run `nebius compute image list`.

* To edit your image (for example, rename it), run:

  ```bash theme={null}
  nebius compute image update computeimage-e***
  ```

  For more information about the command parameters, see the [command reference](https://docs.nebius.com/cli/reference/compute/image/update.md).

* To delete your image, run:

  ```bash theme={null}
  nebius compute image delete computeimage-e***
  ```

**Go SDK**

* Check the status of your image:

  ```go theme={null}
  imageDetails, err := sdk.Services().Compute().V1().
      Image().Get(
          ctx,
          &compute.GetImageRequest{
              Id: "computeimage-e***",
          },
      )
  if err != nil {
      return err
  }
  fmt.Println(imageDetails)
  ```

* Edit your image, for example, rename it:

  ```go theme={null}
  imageForUpdate, err := sdk.Services().Compute().V1().
      Image().Get(
          ctx,
          &compute.GetImageRequest{
              Id: "computeimage-e***",
          },
      )
  if err != nil {
      return err
  }
  if imageForUpdate.GetSpec() == nil {
      return errors.New("image spec is missing")
  }
  imageOperation, err = sdk.Services().Compute().V1().
      Image().Update(
          ctx,
          &compute.UpdateImageRequest{
              Metadata: imageForUpdate.Metadata,
              Spec:     imageForUpdate.Spec,
          },
      )
  if err != nil {
      return err
  }
  if _, err = imageOperation.Wait(ctx); err != nil {
      return err
  }
  ```

* Delete your image:

  ```go theme={null}
  deleteImageOperation, err := sdk.Services().Compute().V1().
      Image().Delete(
          ctx,
          &compute.DeleteImageRequest{
              Id: "computeimage-e***",
          },
      )
  if err != nil {
      return err
  }
  if _, err = deleteImageOperation.Wait(ctx); err != nil {
      return err
  }
  ```

**Python SDK**

* Check the status of your image:

  ```python theme={null}
  image_service = ImageServiceClient(sdk)
  image = await image_service.get(
      GetImageRequest(id="computeimage-e***"),
  )
  print(image)
  ```

* Edit your image, for example, rename it:

  ```python theme={null}
  image_service = ImageServiceClient(sdk)
  image = await image_service.get(
      GetImageRequest(id="computeimage-e***"),
  )
  if image.spec is None:
      raise ValueError("image spec is missing")
  update_image_operation = await image_service.update(
      UpdateImageRequest(
          metadata=image.metadata,
          spec=image.spec,
      ),
  )
  await update_image_operation.wait()
  ```

* Delete your image:

  ```python theme={null}
  image_service = ImageServiceClient(sdk)
  delete_image_operation = await image_service.delete(
      DeleteImageRequest(id="computeimage-e***"),
  )
  await delete_image_operation.wait()
  ```

**JavaScript SDK**

* Check the status of your image:

  ```ts theme={null}
  const getImageService = new ImageService(sdk);
  const imageDetails = await getImageService.get(
    GetImageRequest.create({
      id: "computeimage-e***",
    }),
  );
  console.log(imageDetails);
  ```

* Edit your image, for example, rename it:

  ```ts theme={null}
  const updateImageService = new ImageService(sdk);
  const imageForUpdate = await updateImageService.get(
    GetImageRequest.create({
      id: "computeimage-e***",
    }),
  );
  if (!imageForUpdate.spec) {
    throw new Error("image spec is missing");
  }
  const updateImageOperation = await updateImageService.update(
    UpdateImageRequest.create({
      metadata: imageForUpdate.metadata,
      spec: imageForUpdate.spec,
    }),
  ).result;
  await updateImageOperation.wait();
  ```

* Delete your image:

  ```ts theme={null}
  const deleteImageService = new ImageService(sdk);
  const deleteImageOperation = await deleteImageService.delete(
    DeleteImageRequest.create({
      id: "computeimage-e***",
    }),
  ).result;
  await deleteImageOperation.wait();
  ```

## How to create a VM from a custom image

After your custom boot disk image is ready, you can deploy a VM from it or create a boot disk based on this image.

**Web console**

To create a VM from a custom image:

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Disks** → **Images**.
2. Next to the image, click  → **Create virtual machine**.
3. [Configure and create the VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

> [!NOTE]
>
> You can also select a custom image on the VM creation page. To do that, click  in the **Boot disk** section and select your custom image or image family in **Image configuration**.

**CLI**

1. Create a boot disk based on a custom image:

   ```bash theme={null}
   nebius compute disk create \
      --name <disk_name> \
      --type network_<ssd|ssd_non_replicated|ssd_io_m3> \
      --size-gibibytes <size> \
      --block-size-bytes <block_size> \
      --source-image-id computeimage-***
   ```

   To get the image ID, run `nebius compute image list`.

2. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with the new disk.

   Use the ID of the boot disk created earlier with the `--boot-disk-existing-disk-id` parameter.

**Go SDK**

1. Create a boot disk based on a custom image:

   ```go theme={null}
   // One of compute.DiskSpec_NETWORK_SSD,
   // compute.DiskSpec_NETWORK_SSD_NON_REPLICATED,
   // or compute.DiskSpec_NETWORK_SSD_IO_M3.
   diskType := compute.DiskSpec_NETWORK_SSD

   diskOperation, err := sdk.Services().Compute().V1().
       Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<disk_name>",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: <size>,
                   },
                   BlockSizeBytes: <block_size>,
                   Type:           diskType,
                   Source: &compute.DiskSpec_SourceImageId{
                       SourceImageId: "computeimage-***",
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
   ```

2. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with the new disk.

   Use the ID of the boot disk created earlier.

**Python SDK**

1. Create a boot disk based on a custom image:

   ```python theme={null}
   # One of DiskSpec.DiskType.NETWORK_SSD,
   # DiskSpec.DiskType.NETWORK_SSD_NON_REPLICATED,
   # or DiskSpec.DiskType.NETWORK_SSD_IO_M3.
   disk_type = DiskSpec.DiskType.NETWORK_SSD

   disk_service = DiskServiceClient(sdk)
   create_disk_operation = await disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(
               name="<disk_name>",
           ),
           spec=DiskSpec(
               block_size_bytes=<block_size>,
               type=disk_type,
               source_image_id="computeimage-***",
               size_gibibytes=<size>,
           ),
       ),
   )
   await create_disk_operation.wait()
   ```

2. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with the new disk.

   Use the ID of the boot disk created earlier.

**JavaScript SDK**

1. Create a boot disk based on a custom image:

   ```ts theme={null}
   // One of DiskSpec_DiskType.NETWORK_SSD,
   // DiskSpec_DiskType.NETWORK_SSD_NON_REPLICATED,
   // or DiskSpec_DiskType.NETWORK_SSD_IO_M3.
   const imageDiskType = DiskSpec_DiskType.NETWORK_SSD;

   const createDiskFromImageService = new DiskService(sdk);
   const createDiskFromImageOperation =
     await createDiskFromImageService.create(
       CreateDiskRequest.create({
         metadata: ResourceMetadata.create({
           name: "<disk_name>",
         }),
         spec: DiskSpec.create({
           blockSizeBytes: <block_size>,
           type: imageDiskType,
           source: {
             $case: "sourceImageId",
             sourceImageId: "computeimage-***",
           },
           size: {
             $case: "sizeGibibytes",
             sizeGibibytes: <size>,
           },
         }),
       }),
     ).result;
   await createDiskFromImageOperation.wait();
   ```

2. [Create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm) with the new disk.

   Use the ID of the boot disk created earlier.
