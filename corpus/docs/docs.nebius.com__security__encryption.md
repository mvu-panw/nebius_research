# Encryption in Nebius AI Cloud

Source: https://docs.nebius.com/security/encryption

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Encryption in Nebius AI Cloud

Nebius AI Cloud provides built-in encryption to protect customer data at rest across its storage services. The storage type determines the encryption method and whether encryption is enabled by default.

## Key management

[Key Management Service](https://docs.nebius.com/kms/index.md) (KMS) securely manages and regularly rotates key encryption keys (KEKs). KMS includes a general-purpose key management system and an additional subsystem integrated at the infrastructure level.

For storage types that use KMS, encryption keys are managed by the platform. Services generate and manage data encryption keys (DEKs), while KMS manages the KEKs. You can't select, view, rotate, or revoke these platform-managed keys, and keys that you create in KMS can't be attached to these resources.

## Encryption by storage type

### Disks in Compute

Encryption algorithms and default settings vary by [disk type](https://docs.nebius.com/compute/storage/types.md#network-and-local-ssd-disks). Encryption is available for both boot disks and secondary disks.

* **Network SSD Non-replicated and Network SSD IO M3**: encryption is optional. [When enabled](https://docs.nebius.com/compute/storage/manage.md#how-to-create-a-disk), data is encrypted at both the service and infrastructure levels. Service-level encryption uses AES-128-XTS.

  * DEKs are generated and managed by the Compute service.
  * KEKs are managed by KMS.
* **Network SSD**: encryption is enabled by default at the infrastructure level and can't be disabled.
* **Local SSD**: these disks are not encrypted, and no other data protection method is applied to them. Ensuring the protection of data stored on these devices is your responsibility.

For more information, see [Encryption of disks](https://docs.nebius.com/compute/storage/types.md#encryption-of-disks).

### Shared filesystems in Compute

Data stored in [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) is encrypted by default at the infrastructure level, and encryption can't be disabled. Encryption is applied to the physical disks in the storage cluster. This ensures that all data blocks are protected without affecting performance.

### Buckets in Object Storage

Data stored in [Object Storage buckets](https://docs.nebius.com/object-storage/overview.md#buckets) is encrypted at the service and infrastructure levels. Across all storage classes, data is encrypted with AES-256 using KMS-managed keys.

* DEKs are generated and managed by the Object Storage service.
* KEKs are managed by [KMS](#key-management).

### WEKA filesystems

Data stored in [WEKA filesystems](https://www.weka.io/company/weka-newsroom/press-releases/weka-and-nebius-partner-to-catalyze-ai-innovation-with-ultra-high-performance-cloud-infrastructure-solution/) can be encrypted at the service level.

You need to explicitly enable data encryption when you create a WEKA filesystem. It is not possible to convert a WEKA filesystem to an encrypted filesystem later.

WEKA uses the XTS-AES-256 algorithm, with two independent AES-256 keys.

* DEKs are generated and managed by the WEKA service.
* KEKs are managed by [KMS](#key-management).
