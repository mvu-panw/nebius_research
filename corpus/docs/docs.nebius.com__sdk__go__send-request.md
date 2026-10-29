# How to send an API request using the Go SDK

Source: https://docs.nebius.com/sdk/go/send-request

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to send an API request using the Go SDK

The SDK provides service clients grouped by Nebius AI Cloud service and API version. When your application calls a typed client method, the SDK constructs and sends the corresponding API request.

For mutating operations, such as creating, updating and deleting resources, the SDK returns an operation object. If an operation is asynchronous, call `Wait` to wait until it is completed.

The following example creates a [Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md) (VM).

1. [Install the Go SDK, create a service account and generate its credentials file](https://docs.nebius.com/sdk/go/install-auth.md).

2. Create a Go file with the following code.

   This script initializes the SDK with the [service account credentials file prepared in the previous step](https://docs.nebius.com/sdk/go/install-auth.md#initialization-and-authentication).

   ```go theme={null}
   package main

   import (
      "context"
      "fmt"

      "github.com/nebius/gosdk"
      "github.com/nebius/gosdk/auth"
      common "github.com/nebius/gosdk/proto/nebius/common/v1"
      compute "github.com/nebius/gosdk/proto/nebius/compute/v1"
   )

   // Run the resource creation workflow.
   func main() {
      if err := CreateInstance(context.Background()); err != nil {
         panic(err)
      }
   }

   // CreateInstance creates a boot disk and a VM that uses it.
   func CreateInstance(ctx context.Context) error {
      // Initialize the SDK with service account credentials.
      sdk, err := gosdk.New(
         ctx,
         gosdk.WithUserAgentPrefix("<application_name>/<application_version_or_comment>"),
         gosdk.WithParentID("<project_ID>"),
         gosdk.WithCredentials(
            gosdk.ServiceAccountReader(
               auth.NewServiceAccountCredentialsFileParser(
                  nil,
                  "<credentials_file_path>",
               ),
            ),
         ),
      )
      if err != nil {
         return fmt.Errorf("create gosdk: %w", err)
      }
      defer sdk.Close()

      // Create the boot disk.
      diskOperation, err := sdk.Services().Compute().V1().Disk().Create(ctx, &compute.CreateDiskRequest{
         Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name:     "my-boot-disk",
         },
         Spec: &compute.DiskSpec{
            Size: &compute.DiskSpec_SizeGibibytes{
               SizeGibibytes: 93,
            },
            Type: compute.DiskSpec_NETWORK_SSD,
            Source: &compute.DiskSpec_SourceImageFamily{
               SourceImageFamily: &compute.SourceImageFamily{
                  ParentId:    "<project_ID>",
                  ImageFamily: "<image_family_name>",
               },
            },
         },
      })
      if err != nil {
         return fmt.Errorf("create disk: %w", err)
      }

      diskOperation, err = diskOperation.Wait(ctx)
      if err != nil {
         return fmt.Errorf("wait for disk create: %w", err)
      }

      // Create the VM that uses the boot disk.
      instanceOperation, err := sdk.Services().Compute().V1().Instance().Create(ctx, &compute.CreateInstanceRequest{
         Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name:     "my-vm",
         },
         Spec: &compute.InstanceSpec{
            Resources: &compute.ResourcesSpec{
               Platform: "<platform_name>",
               Size: &compute.ResourcesSpec_Preset{
                  Preset: "<preset_name>",
               },
            },
            NetworkInterfaces: []*compute.NetworkInterfaceSpec{
               {
                  Name:      "eth0",
                  SubnetId:  "<subnet_ID>",
                  IpAddress: &compute.IPAddress{},
               },
            },
            BootDisk: &compute.AttachedDiskSpec{
               AttachMode: compute.AttachedDiskSpec_READ_WRITE,
               Type: &compute.AttachedDiskSpec_ExistingDisk{
                  ExistingDisk: &compute.ExistingDisk{
                     Id: diskOperation.ResourceID(),
                  },
               },
               DeviceId: "boot-disk",
            },
         },
      })
      if err != nil {
         return fmt.Errorf("create VM: %w", err)
      }

      _, err = instanceOperation.Wait(ctx)
      if err != nil {
         return fmt.Errorf("wait for VM creation: %w", err)
      }

      return nil
   }
   ```

   In the script, set the following parameters:

   * `<application_name>/<application_version_or_comment>`: Application or library name and optional version or comment.
   * `<credentials_file_path>`: Path to the service account credentials file.
   * `<project_ID>`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
   * `<image_family_name>`: [Boot disk image family](https://docs.nebius.com/compute/storage/boot-disk-images.md#image-family), for example, `ubuntu24.04-driverless`.
   * `<platform_name>`: [Compute platform](https://docs.nebius.com/compute/virtual-machines/types.md), for example, `cpu-e2`.
   * `<preset_name>`: [Resource preset](https://docs.nebius.com/compute/virtual-machines/types.md) available for the selected platform, for example, `2vcpu-8gb` for `cpu-e2`.
   * `<subnet_ID>`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

3. Execute the file:

   ```bash theme={null}
   go run <file_name>.go
   ```

After you run the example, delete the VM and its boot disk if you no longer need them. Otherwise, Compute continues [charging](https://docs.nebius.com/compute/resources/pricing.md) for these resources.
