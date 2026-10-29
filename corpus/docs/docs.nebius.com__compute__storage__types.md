# Types of storage volumes in Compute

Source: https://docs.nebius.com/compute/storage/types

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Types of storage volumes in Compute

In Compute, storage resources that can be added to virtual machines (VMs) as separate managed resources are called *volumes*. Compute offers two types of managed volumes and one host-local storage option:

* [Disks](#disks):

  * **Network SSD disks**: managed *block storage* volumes.
  * **Local SSD disks**: *ephemeral* host-local block storage.

* [Shared filesystems](#shared-filesystems) are *file storage* volumes. A filesystem can be shared by multiple VMs.

Nebius AI Cloud also provides *object storage* through a separate service, [Object Storage](https://docs.nebius.com/object-storage/index.md). Together, these block, file and object storage options cover all [use cases](#use-cases-and-suggestions) for data preparation, training and inference workloads, as well as associated infrastructure (boot disks, database hosts etc.)

## Disks

*Disks* provide block storage for Compute VMs. Data that you put on disks is divided into blocks that are stored efficiently and reliably on underlying physical drives.

You can create boot disks and additional disks. A *boot disk* is a core disk in a VM, and an *additional disk* is mainly for data storage.

Compute provides different disk sources:

* [Public disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md) supported by the platform.
* [Custom disk images](https://docs.nebius.com/compute/storage/custom-disk-images.md) that you create and tailor to your needs.
* Custom image families that contain a series of custom images and provide the latest image for the disk.
* [Disk snapshots](https://docs.nebius.com/compute/storage/disk-snapshots.md), which are point-in-time copies of a disk state.

Alternatively, you can [create](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk) a blank disk.

Images and image families are only supported for boot disks.

### Network and local SSD disks

Compute offers two kinds of disks:

* [Network SSD disks](#network-ssd-disks) can be created as a boot disk for a VM, from one of the boot disk images provided by Nebius AI Cloud, or as an empty additional disk. One Compute network SSD disk can only be added to one running VM at a time.
* [Local SSD disks](#local-ssd-disks) are Non-Volatile Memory Express (NVMe) drives physically attached to the Compute host that runs a virtual machine (VM). They are not created or managed as separate storage resources, and you can only add them when [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

#### Network SSD disks

* **Network SSD** (`network_ssd`)

  Reliable disks backed by solid state drives (SSDs). Best used for infrastructure purposes: as VM boot disks, disks on Slurm controller VMs, etc.

  Reliability of Network SSD disks is ensured by means of [erasure coding](https://en.wikipedia.org/wiki/Erasure_code). A disk will tolerate up to two concurrent hardware failures in the Nebius AI Cloud [region](https://docs.nebius.com/overview/regions.md).

* **Network SSD Non-replicated** (Network SSD NRD, `network_ssd_non_replicated`)

  High-performance disks backed by SSDs. Best used as temporary storage without strict reliability requirements, for example, a boot disk for nodes in Managed Service for Kubernetes® clusters where redundancy is less important.

  Data blocks of Network SSD Non-replicated disks are stored in [NVMe namespaces](https://nvmexpress.org/resource/nvme-namespaces/) on underlying SSDs. The size of each namespace is 93 GiB, so the disk size must be a multiple of 93 GiB.

  > [!WARNING]
  >
  > Network SSD Non-replicated disks have no redundancy. It's not recommended to store any persistent data on these disks. If a disk fails, its data will be lost.

* **Network SSD IO M3** (`network_ssd_io_m3`)

  High-performance and reliable disks backed by SSDs. Best used in performance-critical storage solutions, for example, as storage disks in GlusterFS clusters.

  In addition to performance levels similar to Network SSD Non-replicated disks, Network SSD IO M3 disks are reliable through replication, with each disk's data mirrored to three physical drives.

  In the disk type name, "IO" stands for "input/output (optimized)" and "M3" stands for "mirrors 3".

#### Local SSD disks

Consider local SSD disks if your workload needs high-performance, low-latency storage for data that can be recreated. Local SSD disks are ephemeral, meaning temporary: their data is erased when the VM is stopped or deleted.

Local SSD disks are available only on some platforms, presets and regions. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

Local SSD disks are useful for:

* Scratch space for files and intermediate outputs that can be recreated.
* Training or inference workloads that require low latency.
* Read or write caches for data that can be recreated.

### Disk types comparison

Network SSD disk types are differentiated by several characteristics:

* **Performance** (bandwidth and IOPS): Local SSD > SSD IO M3 = SSD Non-replicated > SSD
* **Reliability**: SSD IO M3 > SSD > SSD Non-replicated = Local SSD
* **Price per 1 GiB per month**: SSD Non-replicated \< Local SSD \< SSD \< SSD IO M3

You can choose the size of a network disk, but local SSD disks are attached to the VM host as part of a predefined configuration for the selected platform and preset. For more details, see the following comparison table. The values for local SSD disks are the performance numbers per one local SSD disk.

The bandwidth and IOPS values below are upper bounds; actual performance depends on workload.

| **Disk type** | **Network SSD** | **Network SSD NRD** | **Network SSD IO M3** | **Local SSD disk**¹ |
| - | - | - | - | - |
| Capacity | 1–8192 GiB (= 8 TiB) | 93–262,074 GiB (\~ 256 TiB), multiples of 93 GiB | 93–262,074 GiB (\~ 256 TiB), multiples of 93 GiB | 3.5 TiB |
| Read/write bandwidth | 450 MiB/s | 2 GiB/s | 2 GiB/s | Read: 6.8 GB/s Write: 2.6 GB/s |
| Read IOPS | 20,000 | 75,000 | 75,000 | 510,000 |
| Write IOPS | 20,000 | 75,000 | 75,000 | 350,000 |
| Reliability features | Erasure coding – tolerates two concurrent hardware failures | None | Replication – data mirrored to three drives | None |
| [Price per 1 GiB per month](https://docs.nebius.com/compute/resources/pricing.md)² | \$0.071 | \$0.053 | \$0.118 | \$0.065 |

¹ For local SSD disks, the listed values are achieved under synthetic workload.

² The listed prices are valid as of March 9, 2026. For up-to-date prices, see [Price per 1 GiB per month](https://docs.nebius.com/compute/resources/pricing.md).

### VM-managed and standalone disks

When you [create a VM](https://docs.nebius.com/compute/virtual-machines/manage.md), you can use either VM-managed or standalone disks:

* *VM-managed disks* are the disks that you create along with the VM. Their lifecycle is tied to the VM. When you delete the VM, all of its VM-managed disks are deleted with the VM in a single operation.

  This makes VM-managed disks a good fit for ephemeral workloads, for example, training jobs or inference clusters where the VM and its storage should be cleaned up together.

* *Standalone disks* are the disks that you create separately from the VM and attach them later to the VM by using the disk ID.

  Use standalone disks when you need them to persist independently after the VM is deleted, for example, to reattach them to another VM or to enable deletion protection.

Renaming a VM-managed disk deletes the existing disk and creates a new one with a new name. All data on the disk is permanently lost. To rename a VM-managed disk without data loss, [convert it to a standalone disk](https://docs.nebius.com/compute/storage/manage.md#how-to-make-a-disk-vm-managed-or-standalone) and then rename it.

### Encryption of disks

Data encryption helps protect personal and other sensitive data and reduces the risk of unauthorized access. Whether encryption is enabled by default depends on the disk type.

For Network SSD disks, encryption is enabled by default and cannot be disabled. For Network SSD NRD and Network SSD IO M3 disks, encryption is optional, and you can [enable it when you create a disk](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk). Encryption is available for both boot disks and secondary disks.

Local SSD disks are not encrypted and no other data protection method is applied to them. Ensuring the protection of data stored on these devices is your responsibility. We don't recommend using local SSD disks for data that can't be recreated.

For more information, see [Encryption in Nebius AI Cloud](https://docs.nebius.com/security/encryption.md).

### Disk performance

Disk performance depends on both the disk type and its size — it increases as you add more allocation units. Every allocation unit contributes equally to the overall bandwidth and IOPS until you reach the [upper bounds](#disk-types-comparison) for the disk. While you have fewer allocation units than needed to reach the upper bounds, the disk performance equals the sum of each unit's performance. Once the sum reaches the upper bound for bandwidth or IOPS, adding more capacity does not increase performance any further.

Disk performance metrics per allocation unit are shown in the following table. The bandwidth and IOPS values below are upper bounds; actual performance depends on workload.

| **Disk type** | **Network SSD** | **Network SSD NRD** | **Network SSD IO M3** | **Local SSD disk**¹ |
| - | - | - | - | - |
| Allocation unit size | 32 GiB | 93 GiB | 93 GiB | 3.5 TiB |
| Read bandwidth per unit | 15 MiB/s | 110 MiB/s | 110 MiB/s | 6.8 GB/s |
| Write bandwidth per unit | 15 MiB/s | 82 MiB/s | 82 MiB/s | 2.6 GB/s |
| Read IOPS per unit | 1,000 | 28,000 | 28,000 | 510,000 |
| Write IOPS per unit | 1,000 | 5,600 | 5,600 | 350,000 |

¹ For local SSD disks, the listed values are peak numbers achieved per disk under synthetic workload.

Disk encryption also affects the disk performance. Encryption requires additional processing of write operations; therefore, it can reduce performance by up to 15%.

Local SSD disks can only be enabled during VM creation, cannot be scaled later, and are available only in fixed configurations. For supported configurations, see [Using local SSD disks on Compute virtual machines](https://docs.nebius.com/compute/storage/local-disks.md#availability). For other disks, you can choose your disk size in multiples of its allocation units to achieve the desired performance.

Examples:

**SSD disk**

How to reach the maximum for each disk performance metric:

* Read/write bandwidth:
  * Maximum overall bandwidth is 450 MiB/s.
  * Number of allocation units needed to achieve it = Maximum overall read/write bandwidth ÷ Maximum read/write bandwidth per unit = 450 MiB/s ÷ 15 MiB/s = 30 units.
  * Minimum disk size = 30 × 32 GiB = 960 GiB.
* Read IOPS:
  * Maximum overall read IOPS is 20,000.
  * Number of allocation units needed to achieve it = Maximum overall read IOPS ÷ Maximum overall read IOPS per unit = 20,000 ÷ 1,000 = 20 units.
  * Minimum disk size = 20 × 32 GiB = 640 GiB.
* Write IOPS:
  * Maximum overall write IOPS is 20,000.
  * Number of allocation units needed to achieve it = Maximum overall write IOPS ÷ Maximum write IOPS per unit = 20,000 ÷ 1,000 = 20 units.
  * Minimum disk size = 20 × 32 GiB = 640 GiB.

To achieve the maximum disk performance for all metrics, you need a disk of 960 GiB or more.

**SSD NRD or SSD IO M3 disk**

How to reach the maximum for each disk performance metric:

* Read bandwidth:
  * Maximum overall read bandwidth is 2 GiB/s.
  * Number of allocation units needed to achieve it = Maximum overall read bandwidth ÷ Maximum read bandwidth per unit = 2048 MiB/s ÷ 110 MiB/s ≈ 18.62, rounding up to 19 units.
  * Minimum disk size = 19 × 93 GiB = 1767 GiB.
* Write bandwidth:
  * Maximum overall write bandwidth is 2 GiB/s.
  * Number of allocation units needed to achieve it = Maximum overall write bandwidth ÷ Maximum write bandwidth per unit = 2048 MiB/s ÷ 82 MiB/s ≈ 24.98, rounding up to 25 units.
  * Minimum disk size = 25 × 93 GiB = 2325 GiB.
* Read IOPS:
  * Maximum overall read IOPS is 75,000.
  * Number of allocation units needed to achieve it = Maximum overall read IOPS ÷ Maximum read IOPS per unit = 75,000 ÷ 28,000 ≈ 2.68, rounding up to 3 units.
  * Minimum disk size = 3 × 93 GiB = 279 GiB.
* Write IOPS:
  * Maximum overall write IOPS is 75,000.
  * Number of allocation units needed to achieve it = Maximum overall write IOPS ÷ Maximum write IOPS per unit = 75,000 ÷ 5,600 ≈ 13.39, rounding up to 14 units.
  * Minimum disk size = 14 × 93 GiB = 1302 GiB.

To achieve the maximum disk performance for all metrics, you need a disk of 2325 GiB or more.

## Shared filesystems

Shared filesystems provide file storage for Compute VMs. When VMs work with file storage, they work with a hierarchy of folders and files, as opposed to blocks when disks are involved.

One shared filesystem can be attached to multiple VMs at once. All VMs that the filesystem is attached to must belong to the same [project](https://docs.nebius.com/iam/overview.md#projects). Sharing a filesystem across projects is not supported, even if the projects are in the same [region](https://docs.nebius.com/overview/regions.md). To use a shared filesystem on a VM that it is attached to, you must mount it as a virtiofs device.

Filesystems support [data encryption](https://docs.nebius.com/security/encryption.md) by default; you cannot disable it. Encryption allows you to store personal and other sensitive data on filesystems securely, and reduce the risk of unauthorized access.

You can attach buckets to a shared filesystem, which exposes the data in the filesystem through the Object Storage interface. This lets you read and write data to and from the filesystem by using the AWS CLI and other S3-compatible tools. To learn more, refer to [filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md).

### Filesystem specifications

Nebius provides shared filesystems that are generally based on solid state drives (`network_ssd` in developer tools such as Nebius AI Cloud CLI or provider for Terraform) to back them up.

Shared filesystems have the following specifications:

* Capacity: 1–104,857,600 GiB (= 102,400 TiB = 100 PiB)

* Tested read bandwidth per client: up to 15 GiB/s¹

* Tested write bandwidth per client: up to 10 GiB/s¹

* Tested aggregate read bandwidth: up to 1.9 TiB/s²

* Tested aggregate write bandwidth: up to 1.5 TiB/s²

* Maximum file size: 512 GiB × filesystem's [block size](https://docs.nebius.com/compute/storage/manage.md#type-encryption-and-size) in KiB (for example, for the default block size it will be 512 GiB × 4 = 2TiB)

* Maximum number of [inodes](https://www.kernel.org/doc/html/v6.3/filesystems/vfs.html#the-inode-object):

  * For filesystems up to 256 GiB: 4,194,304 (4 × 2<sup>20</sup>)
  * For filesystems larger than 256 GiB: filesystem's size ÷ 64 KiB

  For example, if the filesystem's size is 512 GiB, its maximum number of inodes is (512 × 2<sup>30</sup>) ÷ (64 × 2<sup>10</sup>) = 8 × 2<sup>20</sup> = 8,388,608.

* Reliability features: Erasure coding – tolerates two concurrent hardware failures

* [Price per 1 GiB per month](https://docs.nebius.com/compute/resources/pricing.md)³: \$0.08

¹ Actual bandwidth depends on the GPU platform and the region.

² Measured on a filesystem with 20 PiB of usable capacity. Aggregate bandwidth grows with filesystem capacity, so larger filesystems can exceed these values.

³ The price is shown as of July 2, 2025. For up-to-date prices, see [Price per 1 GiB per month](https://docs.nebius.com/compute/resources/pricing.md).

### Filesystem performance

Filesystem performance depends on its size — performance increases with each 4 TiB of the filesystem size. Every 4 TiB contributes equally to the [aggregate bandwidth](#filesystem-specifications) of the filesystem.

Each 4 TiB of SSD filesystem improves the performance metrics by the following values:

* Read bandwidth: by up to 3.70 GiB/s.
* Write bandwidth: by up to 1.89 GiB/s.

### POSIX compliance and consistency guarantees for filesystems

Shared filesystems provide POSIX-compliant filesystem semantics for workloads that don't involve conflicting access across multiple VMs. In particular, POSIX semantics are guaranteed when VMs operate on independent sets of files and directories, without modifying files or directories accessed by other VMs.

When multiple VMs access the same files or directories, the following consistency guarantees apply:

* File contents — close-to-open consistency with additional synchronization guarantees. Changes made to a file by one VM are guaranteed to become visible to another VM when the reading VM opens the file after any of the following events:

  * The writing VM closes the file.
  * The writing VM successfully calls `fsync()` on the file.
  * A write using `O_DIRECT` completes successfully on the writing VM.

  Concurrent access to an already-open file from multiple VMs doesn't provide full POSIX consistency guarantees.

* Directory entries and inode metadata — eventual consistency. Directory entries and inode metadata are cached on each VM for up to 15 seconds. Consequently, changes made by one VM (such as creating, deleting, or renaming files, or modifying file attributes) may not be immediately visible to other VMs. For example, after one VM deletes a file, another VM may continue to see a stale directory entry for up to 15 seconds.

These limitations apply to cross-VM access. Operations within a single VM retain POSIX semantics.

## Storage types comparison

| Characteristic | [Local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) | [Network disks](https://docs.nebius.com/compute/storage/types.md#disks) | [Shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) |
| - | - | - | - |
| Durability | Ephemeral | Durable | Durable |
| Attachment model | Tied to the VM run and physical host | Independent volume attached to one running VM at a time | Independent volume that can be shared by multiple VMs |
| Capacity model | Preconfigured, all or none | User-defined | User-defined |

## Use cases and suggestions

Here is an overview of various stages of ML/AI workloads and storage options that Compute and other Nebius AI Cloud services provide for these stages, as well as general suggestions for using Compute storage.

### Infrastructure

* **VM boot disks: Network SSD disks**

  For OS and system data on your VMs, the main storage requirement is reliability, so the suggested disk type is Network SSD.

* **VM storage disks: Network SSD IO M3 disks**

  If you are building storage solutions on VMs, for example, GlusterFS clusters, use Network SSD IO M3 disks for speed and reliability.

* **Managed Kubernetes node storage: Network SSD Non-replicated disks**

  For Kubernetes worker nodes where data reliability isn't a top priority (as the data is often transient), Network SSD Non-replicated disks provide high performance and low latency.

* **Database hosts: Network SSD IO M3 disks**

  Database workloads often demand consistent and high input/output operations per second (IOPS), and Network SSD IO M3 disks offer the best combination of reliability and speed.

### Data preparation

* **Storing and preprocessing datasets: Object Storage buckets**

  Object Storage is ideal for handling large, unstructured datasets and provides a scalable solution for preprocessing tasks like data normalization or augmentation.

### Training

* **Streaming datasets to workers: SSD shared filesystems or Object Storage buckets**

  In most cases, SSD shared filesystems ensure fast access to datasets during training, without bottlenecks. For exceptionally large datasets (1 PiB+) or distributed training across external workers, Object Storage buckets provide a scalable solution.

* **Sharing code between workers: SSD shared filesystems**

  By using SSD shared filesystems, multiple workers can efficiently access and synchronize code during distributed training, ensuring consistency and minimizing latency.

* **Checkpoints: SSD shared filesystems, then Object Storage buckets**

  During training, SSD shared filesystems allow for quickly saving and loading checkpoints, thus ensuring minimal disruption. Once training is completed, asynchronous transfer to Object Storage reduces costs while maintaining accessibility for future use.

* **Scratch space: local SSD disks**

  On [supported platforms, presets and regions](https://docs.nebius.com/compute/storage/local-disks.md#availability), [local SSD disks](https://docs.nebius.com/compute/storage/local-disks.md) provide host-local NVMe for data that can be recreated and benefits from high performance and low latency. Treat them as ephemeral and keep important data on durable storage.

### Inference

* **Autoscaling, sharing weights between GPUs: SSD shared filesystems**

  When inference workloads require scaling across multiple VMs with GPUs, SSD shared filesystems allow for fast sharing of model weights, thus ensuring consistent performance across nodes during autoscaling.

* **Sharing results: Object Storage buckets**

  Once inference tasks are completed, Object Storage is ideal for sharing outputs such as logs, predictions or reports with other users or systems, due to its scalable and cost-efficient nature.

### General suggestions

* For maximum IOPS, reads and writes to a volume should be close to its [block size](https://docs.nebius.com/compute/storage/manage.md#type-encryption-and-size).
* For maximum bandwidth, reads and writes to a volume should be in 4 MiB chunks.

## See also

* [How to create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm)
* [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md)
* [Attaching and mounting Compute volumes to VMs](https://docs.nebius.com/compute/storage/use.md)
* [How to detach additional volumes from virtual machines](https://docs.nebius.com/compute/storage/detach-volume.md)
* [Local SSD disks for Compute virtual machines](https://docs.nebius.com/compute/storage/local-disks.md)
