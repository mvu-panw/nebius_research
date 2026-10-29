# How to create keys in Key Management Service

Source: https://docs.nebius.com/kms/manage/create

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create keys in Key Management Service

You can create [symmetric and asymmetric keys](https://docs.nebius.com/kms/types-operations.md#symmetric-and-asymmetric-keys) in Key Management Service (KMS):

* Create a symmetric key if you need to encrypt and decrypt data with the same key material or generate data keys for envelope encryption.
* Create an asymmetric key if you need a public-private key pair.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create a symmetric key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Click  **Create key**.

3. Specify a unique key name.

4. In the **Type** field, select **Symmetric key**.

5. (Optional) In **Rotation period**, set how often KMS should automatically [rotate the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). When a key is rotated, KMS generates a new key version and immediately sets it as the default version. You can set the rotation period in days, months or years.

   The **Algorithm** value is set automatically to **AES-256-GCM**.

6. (Optional) Add a description.

7. Click **Create key**.

The key appears in the list of symmetric keys.

**CLI**

Create a symmetric key:

```bash theme={null}
nebius kms symmetric-key create \
   --name <key_name> \
   --description "<key_description>" \
   --algorithm aes_256 \
   --rotation-period <period>
```

The command contains the following parameters:

* `--name`: Name of the key.
* `--description` (optional): Description of the key.
* `--algorithm`: [Key encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms). You can only specify the algorithm when you create a key. You can't update it later. The only supported value is `aes_256`.
* `--rotation-period` (optional): Period after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation).

  When a key is rotated, KMS generates a new key version and immediately sets it as the default version.

  Specify the value in the `NhNmNs` format, for example, `24h` or `48h30m10s`. The minimum value is `86400s` (one day) and the maximum value is `315360000s` (3650 days). The default value is `7776000s` (90 days).

**Terraform**

1. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_kms_v1_symmetric_key" "my_symmetric_key" {
     name            = "<key_name>"
     description     = "<key_description>"
     parent_id       = "<project_ID>"
     algorithm       = "AES_256"
     rotation_period = "<period>"
   }
   ```

   In the configuration, specify:

   * `name`: Name of the key.
   * `description` (optional): Description of the key.
   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `algorithm`: [Key encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms). You can only specify the algorithm when you create a key. You can't update it later. The only supported value is `AES_256`.
   * `rotation_period` (optional): Period after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation).

     When a key is rotated, KMS generates a new key version and immediately sets it as the default version.

     Specify the value in the `NhNmNs` format, for example, `24h` or `48h30m10s`. The minimum value is `86400s` (one day) and the maximum value is `315360000s` (3650 days). The default value is `7776000s` (90 days).

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a symmetric key:

```go theme={null}
symCreatePeriod, err := time.ParseDuration(
    "<period>",
)
if err != nil {
    return fmt.Errorf("parse rotation period: %w", err)
}
symCreateService := sdk.Services().KMS().V1().
    SymmetricKey()
symCreateOperation, err := symCreateService.Create(
    ctx,
    &kms.CreateSymmetricKeyRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<key_name>",
        },
        Spec: &kms.SymmetricKeySpec{
            Description: "<key_description>",
            Algorithm: kms.SymmetricAlgorithm_AES_256,
            RotationPeriod: durationpb.New(symCreatePeriod),
        },
    },
)
if err != nil {
    return fmt.Errorf("create symmetric key: %w", err)
}
symCreateOperation, err = symCreateOperation.Wait(ctx)
if err != nil {
    return fmt.Errorf("wait for operation: %w", err)
}
symCreateResult, err := symCreateService.Get(
    ctx,
    &kms.GetSymmetricKeyRequest{
        Id: symCreateOperation.ResourceID(),
    },
)
if err != nil {
    return fmt.Errorf("get key: %w", err)
}
fmt.Println(symCreateResult)
```

In the code, specify:

* `Metadata.Name`: Name of the key.
* `Spec.Description` (optional): Description of the key.
* `Spec.Algorithm`: [Key encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms). You can only specify the algorithm when you create a key. You can't update it later. The only supported value is `kms.SymmetricAlgorithm_AES_256`.
* `Spec.RotationPeriod` (optional): Period after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). The code parses the `<period>` value with `time.ParseDuration`. To use the default period, remove the `time.ParseDuration` call and the `RotationPeriod` line.

  When a key is rotated, KMS generates a new key version and immediately sets it as the default version.

  Specify the value in the `NhNmNs` format, for example, `24h` or `48h30m10s`. The minimum value is `86400s` (one day) and the maximum value is `315360000s` (3650 days). The default value is `7776000s` (90 days).

**Python SDK**

Create a symmetric key:

```python theme={null}
service = kms.SymmetricKeyServiceClient(sdk)
operation = await service.create(
    kms.CreateSymmetricKeyRequest(
        metadata=ResourceMetadata(name="<key_name>"),
        spec=kms.SymmetricKeySpec(
            description="<key_description>",
            algorithm=kms.SymmetricAlgorithm.AES_256,
            rotation_period=timedelta(hours=720),
        ),
    ),
)
await operation.wait()
result = await service.get(
    kms.GetSymmetricKeyRequest(id=operation.resource_id),
)
print(result)
```

In the code, specify:

* `metadata.name`: Name of the key.
* `spec.description` (optional): Description of the key.
* `spec.algorithm`: [Key encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms). You can only specify the algorithm when you create a key. You can't update it later. The only supported value is `kms.SymmetricAlgorithm.AES_256`.
* `spec.rotation_period` (optional): Period, as a `timedelta`, after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). The example sets 720 hours. When a key is rotated, KMS generates a new key version and immediately sets it as the default version. The minimum value is one day and the maximum value is 3650 days. The default value is 90 days.

**JavaScript SDK**

Create a symmetric key:

```ts theme={null}
const symCreateService = new kms.SymmetricKeyService(sdk);
dayjs.extend(duration);
const symCreateOperation = await symCreateService.create(
  kms.CreateSymmetricKeyRequest.create({
    metadata: { name: "<key_name>" },
    spec: {
      description: "<key_description>",
      algorithm: kms.SymmetricAlgorithm.AES_256,
      rotationPeriod: dayjs.duration(720, "hours"),
    },
  }),
).result;
await symCreateOperation.wait();
const symCreateResult = await symCreateService.get(
  kms.GetSymmetricKeyRequest.create({
    id: symCreateOperation.resourceId(),
  }),
).result;
console.log(symCreateResult);
```

In the code, specify:

* `metadata.name`: Name of the key.
* `spec.description` (optional): Description of the key.
* `spec.algorithm`: [Key encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms). You can only specify the algorithm when you create a key. You can't update it later. The only supported value is `kms.SymmetricAlgorithm.AES_256`.
* `spec.rotationPeriod` (optional): Period, as a Day.js duration, after which KMS automatically [rotates the key material](https://docs.nebius.com/kms/types-operations.md#key-rotation). The example sets 720 hours. When a key is rotated, KMS generates a new key version and immediately sets it as the default version. The minimum value is one day and the maximum value is 3650 days. The default value is 90 days.

## How to create an asymmetric key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.
2. Click  **Create key**.
3. Specify a unique key name.
4. In the **Type** field, select **Asymmetric key**.
5. In the **Algorithm** field, select **RSA-4096** or **ECC (P-256)**.
6. (Optional) Add a description.
7. Click **Create key**.

The key appears in the list of asymmetric keys.

**CLI**

Create an asymmetric key:

```bash theme={null}
nebius kms asymmetric-key create \
   --name <key_name> \
   --description "<key_description>" \
   --algorithm <asymmetric_key_algorithm>
```

The command contains the following parameters:

* `--name`: Name of the key.
* `--description` (optional): Description of the key.
* `--algorithm`: [Cryptographic algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) to use with the key. You can only specify the algorithm when you create a key. You can't update it later. The supported values are:

  * `ecdsa_nist_p256_sha_256`
  * `ecdsa_nist_p384_sha_384`
  * `rsa_4096_enc_oaep_sha_256`

**Terraform**

1. Create the following configuration:

   ```hcl theme={null}
   resource "nebius_kms_v1_asymmetric_key" "my_asymmetric_key" {
     name        = "<key_name>"
     description = "<key_description>"
     parent_id   = "<project_ID>"
     algorithm   = "<asymmetric_key_algorithm>"
   }
   ```

   In the configuration, specify:

   * `name`: Name of the key.
   * `description` (optional): Description of the key.
   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `algorithm`: [Cryptographic algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) to use with the key. You can only specify the algorithm when you create a key. You can't update it later. The supported values are:

     * `ECDSA_NIST_P256_SHA_256`
     * `ECDSA_NIST_P384_SHA_384`
     * `RSA_4096_ENC_OAEP_SHA_256`

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create an asymmetric key:

```go theme={null}
asymCreateService := sdk.Services().KMS().V1().
    AsymmetricKey()
asymCreateOperation, err := asymCreateService.Create(
    ctx,
    &kms.CreateAsymmetricKeyRequest{
        Metadata: &common.ResourceMetadata{
            Name: "<key_name>",
        },
        Spec: &kms.AsymmetricKeySpec{
            Description: "<key_description>",
            Algorithm: kms.AsymmetricAlgorithm_ECDSA_NIST_P256_SHA_256,
        },
    },
)
if err != nil {
    return fmt.Errorf("create asymmetric key: %w", err)
}
asymCreateOperation, err = asymCreateOperation.Wait(ctx)
if err != nil {
    return fmt.Errorf("wait for operation: %w", err)
}
asymCreateResult, err := asymCreateService.Get(
    ctx,
    &kms.GetAsymmetricKeyRequest{
        Id: asymCreateOperation.ResourceID(),
    },
)
if err != nil {
    return fmt.Errorf("get key: %w", err)
}
fmt.Println(asymCreateResult)
```

In the code, specify:

* `Metadata.Name`: Name of the key.
* `Spec.Description` (optional): Description of the key.
* `Spec.Algorithm`: [Cryptographic algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) to use with the key. You can only specify the algorithm when you create a key. You can't update it later. The supported values are:

  * `kms.AsymmetricAlgorithm_ECDSA_NIST_P256_SHA_256`
  * `kms.AsymmetricAlgorithm_ECDSA_NIST_P384_SHA_384`
  * `kms.AsymmetricAlgorithm_RSA_4096_ENC_OAEP_SHA_256`

**Python SDK**

Create an asymmetric key:

```python theme={null}
service = kms.AsymmetricKeyServiceClient(sdk)
operation = await service.create(
    kms.CreateAsymmetricKeyRequest(
        metadata=ResourceMetadata(name="<key_name>"),
        spec=kms.AsymmetricKeySpec(
            description="<key_description>",
            algorithm=kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256,
        ),
    ),
)
await operation.wait()
result = await service.get(
    kms.GetAsymmetricKeyRequest(id=operation.resource_id),
)
print(result)
```

In the code, specify:

* `metadata.name`: Name of the key.
* `spec.description` (optional): Description of the key.
* `spec.algorithm`: [Cryptographic algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) to use with the key. You can only specify the algorithm when you create a key. You can't update it later. The supported values are:

  * `kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256`
  * `kms.AsymmetricAlgorithm.ECDSA_NIST_P384_SHA_384`
  * `kms.AsymmetricAlgorithm.RSA_4096_ENC_OAEP_SHA_256`

**JavaScript SDK**

Create an asymmetric key:

```ts theme={null}
const asymCreateService = new kms.AsymmetricKeyService(sdk);
const asymCreateOperation = await asymCreateService.create(
  kms.CreateAsymmetricKeyRequest.create({
    metadata: { name: "<key_name>" },
    spec: {
      description: "<key_description>",
      algorithm: kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256,
    },
  }),
).result;
await asymCreateOperation.wait();
const asymCreateResult = await asymCreateService.get(
  kms.GetAsymmetricKeyRequest.create({
    id: asymCreateOperation.resourceId(),
  }),
).result;
console.log(asymCreateResult);
```

In the code, specify:

* `metadata.name`: Name of the key.
* `spec.description` (optional): Description of the key.
* `spec.algorithm`: [Cryptographic algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) to use with the key. You can only specify the algorithm when you create a key. You can't update it later. The supported values are:

  * `kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256`
  * `kms.AsymmetricAlgorithm.ECDSA_NIST_P384_SHA_384`
  * `kms.AsymmetricAlgorithm.RSA_4096_ENC_OAEP_SHA_256`

## See also

* [Cryptographic operations with symmetric keys](https://docs.nebius.com/kms/cryptography/symmetric.md)
* [Cryptographic operations with asymmetric keys](https://docs.nebius.com/kms/cryptography/asymmetric.md)
* [How to rotate symmetric keys in Key Management Service](https://docs.nebius.com/kms/manage/rotate.md)
