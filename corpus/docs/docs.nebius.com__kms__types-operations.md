# Key types and operations in Key Management Service

Source: https://docs.nebius.com/kms/types-operations

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Key types and operations in Key Management Service

Key Management Service (KMS) supports two key types: *symmetric keys* and *asymmetric keys*.

## Symmetric and asymmetric keys

The main difference between symmetric and asymmetric keys is how [cryptographic operations](#cryptographic-operations-and-use-cases) are performed.

* In *symmetric encryption*, the same key is used to encrypt and decrypt data.
* In *asymmetric encryption*, a public key is used to encrypt data, and the matching private key is used to decrypt it. The private key is also used to create a digital signature, and the public key is used to verify it.

Use a symmetric key for data protection, including [envelope encryption](#envelope-encryption). Use an asymmetric key for key exchange and digital signatures.

## Encryption algorithms

Symmetric keys in KMS use **AES-256-GCM** with 256-bit keys in [Galois/Counter Mode](https://en.wikipedia.org/wiki/Galois/Counter_Mode) (GCM). This is the algorithm used for direct encryption and envelope encryption workflows. It supports additional authenticated data, which lets you verify additional context during decryption for increased security.

Asymmetric keys are available with the following algorithms:

* **RSA-4096** (`RSA_4096_ENC_OAEP_SHA_256`): a widely compatible public-key algorithm commonly used for data encryption. It uses a larger key than elliptic-curve cryptography (ECC) algorithms.
* **ECC (P-256)** (`ECDSA_NIST_P256_SHA_256`): an algorithm used for digital signature workflows. It is more lightweight than ECC (P-384), with faster operations and smaller signatures.
* **ECC (P-384)** (`ECDSA_NIST_P384_SHA_384`): an algorithm used for digital signature workflows that provides a higher security level than ECC (P-256).

## Cryptographic operations and use cases

Symmetric and asymmetric keys in KMS support different cryptographic operations.

### Symmetric key operations

| **Operation** | **What it does** | **Typical use cases** |
| - | - | - |
| **Encrypt** | Encrypts data by using a symmetric KMS key. | Protecting application data directly through KMS. |
| **Decrypt** | Decrypts data that was encrypted by using a symmetric KMS key. | Reading data that was previously encrypted through KMS. |
| **Generate data key** | Creates a temporary *data encryption key* and protects it by using a symmetric key. | Envelope encryption for files, records, archives or other application data. |
| **Rotate** | Generates a new key version and sets it as the default version. | Workflows where you want to rotate keys regularly for security, either manually or automatically. |

For information about how to perform these operations, see:

* [Cryptographic operations with symmetric keys](https://docs.nebius.com/kms/cryptography/symmetric.md)
* [How to rotate symmetric keys in Key Management Service](https://docs.nebius.com/kms/manage/rotate.md)

#### Envelope encryption

Symmetric keys support *envelope encryption* to encrypt large volumes of data locally where the KMS key protects a temporary data encryption key (DEK) and your application uses that temporary key for encrypting data. In this model, the KMS key acts as a key encryption key (KEK).

With envelope encryption, KMS does not encrypt the data itself. Instead, your application uses the DEK locally to encrypt and decrypt the data, while KMS protects the DEK. This creates a two-layer structure.

Envelope encryption provides stronger security because the KEK is stored and protected in KMS.

#### Key rotation

Symmetric keys support *key rotation*, which lets you refresh the cryptographic material behind a key while continuing to use the same key resource. When a key is rotated, KMS creates a new key version and immediately sets it as the default version.

You can rotate a symmetric key manually, or you can configure automatic rotation by setting a rotation period when you [create](https://docs.nebius.com/kms/manage/create.md#how-to-create-a-symmetric-key) or [update](https://docs.nebius.com/kms/manage/update.md#how-to-update-a-symmetric-key) the key.

### Asymmetric key operations

| **Operation** | **What it does** | **Typical use cases** |
| - | - | - |
| **Decrypt** | Uses a private key to decrypt data that was encrypted by using a matching public key. | Workflows where one system encrypts data by using a public key and only a private key holder can decrypt it. |
| **Sign hash** | Uses a private key to create a digital signature over a hash value. | Signing workflows where a user or application signs data by using a private key, and other systems verify the signature by using a public key. |
| **Get public key** | Returns a public key for the asymmetric key pair. | Sharing a public key by using applications or external systems for encryption, or signature verification outside KMS. |

For information about how to perform these operations, see [Cryptographic operations with asymmetric keys](https://docs.nebius.com/kms/cryptography/asymmetric.md).
