# Boot disk images for Compute virtual machines

Source: https://docs.nebius.com/compute/storage/boot-disk-images

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Boot disk images for Compute virtual machines

When you [create a boot disk](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk) for a virtual machine, you need to choose an image for the disk.

Compute supports two types of boot disk images:

* *Public images* are provided and supported by the platform by default.
* *Custom images* are images that you [create](https://docs.nebius.com/compute/storage/custom-disk-images.md) yourself with customized software and architecture.

Nebius AI Cloud provides public boot disk images for GPU and non-GPU VMs.

## Compatibility types

The image that you choose for a VM must be compatible with the VM's [platform](https://docs.nebius.com/compute/virtual-machines/types.md). There are different types of compatibility:

* *Recommended images* ensure stable VM performance.
* *Alternative images* are compatible with the platform but do not guarantee stable performance.

## Image family

Each image has a family. When you use the [Nebius AI Cloud CLI](https://docs.nebius.com/cli/reference/compute/disk/create.md) or the [provider for Terraform](https://docs.nebius.com/terraform-provider/reference/resources/compute_v1_disk.md) to create a boot disk, you need to specify its family. For example, the image Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) has the family `ubuntu24.04-cuda13.0`.

Image families for GPU VMs are either stable or latest:

* *Stable families*, such as `ubuntu24.04-cuda13.0`, keep fixed versions of the GPU driver and CUDA Toolkit. Boot disks that you create from a stable family at different times get the same GPU driver and CUDA Toolkit versions. Use them for most workloads.
* *Latest families*, such as `ubuntu24.04-cuda13-latest`, are regularly updated to the newest GPU driver and CUDA versions. Each new image in the family is tested only when it's released and boot disks you create at different times can get different GPU driver and CUDA Toolkit versions. Use them if you need the latest features, performance improvements or security patches from NVIDIA, for example, on new platforms.

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to get a list of available public images

To get a list of public boot disk images available in a [region](https://docs.nebius.com/overview/regions.md):

**CLI**

Run the following command:

```bash theme={null}
nebius compute image list-public --region <region>
```

**Go SDK**

```go theme={null}
images, err := sdk.Services().Compute().V1().
    Image().ListPublic(
        ctx,
        &compute.ListPublicRequest{
            Region: "<region>",
        },
    )
if err != nil {
    return err
}
fmt.Println(images)
```

**Python SDK**

```python theme={null}
image_service = ImageServiceClient(sdk)
images = await image_service.list_public(
    ListPublicRequest(
        region="<region>",
    ),
)
print(images)
```

**JavaScript SDK**

```ts theme={null}
const imageService = new ImageService(sdk);
const images = await imageService.listPublic(
  ListPublicRequest.create({
    region: "<region>",
  }),
);
console.log(images);
```

In the output, you'll see public images available in the specified region, including image families and other metadata.

To determine which VM platforms are compatible with a public image, check the following parameters in the output:

* `recommended_platforms`: Platforms for which the image is recommended.
* `unsupported_platforms`: Platforms for which the image is not supported (with reasons, if available).

Availability of images and their compatibility with platforms differ by region.

## Images for GPU VMs

For VMs with GPUs, create boot disks from the following images:

* Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 12), `ubuntu24.04-cuda12`

  > [!WARNING]
  >
  > The `ubuntu22.04-cuda12` image family is deprecated. Existing disks created from images in this family remain available, but creating new disks from this image family isn't supported. Migrate to newer images.

* Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13), `ubuntu24.04-cuda13.0`

* Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest), `ubuntu24.04-cuda13-latest`

  > If a VM doesn't work as expected on an image from this family, create its boot disk from the stable `ubuntu24.04-cuda13.0` family instead.

The following boot disk images are compatible with GPU VMs:

| VM platform | [Recommended images](#compatibility-types) | [Alternative images](#compatibility-types) |
| - | - | - |
| NVIDIA® B300 NVLink with Intel Granite Rapids `gpu-b300-sxm` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® B200 NVLink with Intel Emerald Rapids `gpu-b200-sxm` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® B200 NVLink with Intel Emerald Rapids `gpu-b200-sxm-a` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® H200 NVLink with Intel Sapphire Rapids `gpu-h200-sxm` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 12) `ubuntu24.04-cuda12` Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® H100 NVLink with Intel Sapphire Rapids `gpu-h100-sxm` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 12) `ubuntu24.04-cuda12` Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® RTX PRO™ 6000 with Intel Granite Rapids `gpu-rtx6000` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® RTX PRO™ 6000 with Intel Granite Rapids `gpu-rtx6000-a` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13, latest) `ubuntu24.04-cuda13-latest` |
| NVIDIA® L40S PCIe with Intel Ice Lake `gpu-l40s-a` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 12) `ubuntu24.04-cuda12` |
| NVIDIA® L40S PCIe with AMD Epyc Genoa `gpu-l40s-d` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13) `ubuntu24.04-cuda13.0` | Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 12) `ubuntu24.04-cuda12` |

> [!WARNING]
>
> The `1gpu-20vcpu-224gb` preset for NVIDIA® B200 platforms (`gpu-b200-sxm` and `gpu-b200-sxm-a`) requires [driver](#gpu-drivers-and-other-components) version 580.x or newer. Earlier driver versions are not supported.

### GPU drivers and other components

The boot disk images for VMs with GPUs include the following components:

<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>`ubuntu24.04-cuda12`</th>
      <th>`ubuntu24.04-cuda13.0`</th>
      <th>`ubuntu24.04-cuda13-latest`</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Drivers preset</td>
      <td>`cuda12.8`</td>
      <td>`cuda13.0`</td>
      <td>Latest available</td>
    </tr>

    <tr>
      <td>CUDA Toolkit</td>
      <td>12.8 ([release notes](https://docs.nvidia.com/cuda/archive/12.8.0/))</td>
      <td>13.0 ([release notes](https://docs.nvidia.com/cuda/archive/13.0.0/))</td>
      <td>Latest 13.x</td>
    </tr>

    <tr>
      <td>NVIDIA® Data Center GPU Driver</td>
      <td>570.x</td>
      <td>580.x</td>
      <td>Latest available</td>
    </tr>

    <tr>
      <td>Linux kernel</td>
      <td>6.11, NVIDIA® HWE</td>
      <td>6.11, NVIDIA® HWE</td>
      <td>6.11, NVIDIA® HWE</td>
    </tr>

    <tr>
      <td>Networking package</td>
      <td>[NVIDIA® DOCA](https://developer.nvidia.com/networking/doca) 2.9.2 ([release notes](https://docs.nvidia.com/doca/archive/2-9-2-lts-ovs-update/doca+release+notes/index.html))</td>
      <td>NVIDIA® DOCA 3.1.0 ([release notes](https://docs.nvidia.com/doca/archive/3-1-0/doca+release+notes/index.html))</td>
      <td>NVIDIA® DOCA, latest available</td>
    </tr>

    <tr>
      <td>Other components</td>

      <td colspan="3">
        <ul>
          <li>[NVIDIA® Collective Communications Library](https://developer.nvidia.com/nccl) (NCCL)</li>
          <li>[NVIDIA® Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)</li>
          <li>[NVIDIA® Data Center GPU Manager](https://developer.nvidia.com/dcgm) (DCGM)</li>
          <li>[Nebius AI Cloud monitoring agent](https://docs.nebius.com/observability/agents/monitoring-agent.md)</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

To check the current versions of components in `ubuntu24.04-cuda13-latest` images, [get a list of available public images](#how-to-get-a-list-of-available-public-images).

## Images for non-GPU VMs

For VMs without GPUs, create boot disks from the Ubuntu 24.04 LTS, `ubuntu24.04-driverless` image without GPU drivers and components.

The images without drivers are also compatible with GPU VMs, but you need to install the drivers and components manually. We recommend using the [dedicated images for GPU VMs](#images-for-gpu-vms).

The following boot disk images are compatible with non-GPU VMs:

| VM platform | [Recommended images](#compatibility-types) | [Alternative images](#compatibility-types) |
| - | - | - |
| Non-GPU AMD EPYC Genoa `cpu-d3` | Ubuntu 24.04 LTS `ubuntu24.04-driverless` | None |
| Non-GPU Intel Ice Lake `cpu-e2` | Ubuntu 24.04 LTS `ubuntu24.04-driverless` | None |

> [!WARNING]
>
> The `ubuntu22.04-driverless` image family is deprecated. Existing disks created from images in this family remain available, but creating new disks from this image family isn't supported. Migrate to newer images.

## Security updates

Automatic security updates are disabled by default. We recommend that you check the compatibility of new library versions on a test VM, and then apply the updates manually to all running GPU nodes. If you do need automatic updates, you can [enable](https://docs.nebius.com/compute/storage/automatic-updates.md) them.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
