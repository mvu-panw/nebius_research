# Cryptographic operations with asymmetric keys

Source: https://docs.nebius.com/kms/cryptography/asymmetric

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cryptographic operations with asymmetric keys

[Asymmetric keys](https://docs.nebius.com/kms/types-operations.md#symmetric-and-asymmetric-keys) in Key Management Service (KMS) consist of a public and private key. You can use the public key to encrypt data and the private key to decrypt it.

You can also use the private key to sign hashes and the public key to verify signatures.

## Prerequisites

You can retrieve the public key in the web console. To decrypt data and sign hashes, use the Nebius AI Cloud CLI or SDKs. To verify signatures, use a local cryptographic tool such as [OpenSSL](https://openssl-library.org/source/).

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. Alternatively, you can have an [access permit](https://docs.nebius.com/iam/authorization/groups/manage.md#setting-up-custom-groups) with the `editor` role assigned to the required key. To check your access rights, go to the [Administration → IAM](https://console.nebius.com/iam) section in the web console.

## How to get the public key

You can retrieve the public key to use it for encryption and signature verification.

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Select **Asymmetric keys** and find the required key in the list.

   To choose a key that supports what you need, check the **Algorithm** column:

   * Signing and verification: ECC (P-256)
   * Encryption: RSA-4096

3. On the **Key's overview** tab, next to **Public key**, click .

4. Save the public key contents to a local file, for example `public_key.pem`.

**CLI**

1. List asymmetric keys:

   ```bash theme={null}
   nebius kms asymmetric-key list
   ```

   In the output, copy the ID of the required asymmetric key. To choose a key that supports what you need, check the `spec.algorithm` field:

   * Signing and verification: `ecdsa_nist_p256_sha_256`, `ecdsa_nist_p384_sha_384`
   * Encryption: `rsa_4096_enc_oaep_sha_256`

2. Run the following command:

   ```bash theme={null}
   nebius kms asymmetric-crypto get-public-key \
     --key-id <key_ID>
   ```

   In the command, specify the ID of the asymmetric key.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmsasymkey-e00***
   public_key: |
     -----BEGIN PUBLIC KEY-----
     MFkwEwYHKoZ***
     -----END PUBLIC KEY-----
   ```

3. Save the `public_key` value to a local file, for example `public_key.pem`.

**Go SDK**

1. List asymmetric keys:

   ```go theme={null}
   asymListService := sdk.Services().KMS().V1().
       AsymmetricKey()
   asymListResponse, err := asymListService.List(
       ctx,
       &kms.ListAsymmetricKeysRequest{},
   )
   if err != nil {
       return fmt.Errorf("list asymmetric keys: %w", err)
   }
   fmt.Println(asymListResponse)
   ```

   In the output, copy the ID of the required asymmetric key. To choose a key that supports what you need, check the `algorithm` value:

   * Signing and verification: `ECDSA_NIST_P256_SHA_256`, `ECDSA_NIST_P384_SHA_384`
   * Encryption: `RSA_4096_ENC_OAEP_SHA_256`

2. Get the public key:

   ```go theme={null}
   publicKeyService := sdk.Services().KMS().V1().
       AsymmetricCrypto()
   publicKeyResponse, err := publicKeyService.GetPublicKey(
       ctx,
       &kms.AsymmetricGetPublicKeyRequest{
           KeyId: "<key_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf(
           "get public key with asymmetric crypto: %w", err,
       )
   }
   fmt.Printf("key_id: %s\npublic_key:\n%s\n",
       publicKeyResponse.GetKeyId(), publicKeyResponse.GetPublicKey())
   ```

   In the code, set `KeyId` to the ID of the asymmetric key.

3. Save the `public_key` value from the output to a local file, for example `public_key.pem`.

**Python SDK**

1. List asymmetric keys:

   ```python theme={null}
   service = kms.AsymmetricKeyServiceClient(sdk)
   response = await service.list(
       kms.ListAsymmetricKeysRequest(),
   )
   print(response)
   ```

   In the output, copy the ID of the required asymmetric key. To choose a key that supports what you need, check the `spec.algorithm` value:

   * Signing and verification: `ECDSA_NIST_P256_SHA_256`, `ECDSA_NIST_P384_SHA_384`
   * Encryption: `RSA_4096_ENC_OAEP_SHA_256`

2. Get the public key:

   ```python theme={null}
   service = kms.AsymmetricCryptoServiceClient(sdk)
   response = await service.get_public_key(
       kms.AsymmetricGetPublicKeyRequest(
           key_id="<key_ID>",
       ),
   )
   print(
       f"key_id: {response.key_id}\n"
       f"public_key:\n{response.public_key}"
   )
   ```

   In the code, set `key_id` to the ID of the asymmetric key.

3. Save the `public_key` value from the output to a local file, for example `public_key.pem`.

**JavaScript SDK**

1. List asymmetric keys:

   ```ts theme={null}
   const asymListService = new kms.AsymmetricKeyService(sdk);
   const asymListResponse = await asymListService.list(
     kms.ListAsymmetricKeysRequest.create({}),
   ).result;
   console.log(asymListResponse);
   ```

   In the output, copy the ID of the required asymmetric key. To choose a key that supports what you need, check the `spec.algorithm` value:

   * Signing and verification: `ECDSA_NIST_P256_SHA_256`, `ECDSA_NIST_P384_SHA_384`
   * Encryption: `RSA_4096_ENC_OAEP_SHA_256`

2. Get the public key:

   ```ts theme={null}
   const publicKeyService =
     new kms.AsymmetricCryptoService(sdk);
   const publicKeyResponse = await publicKeyService.getPublicKey(
     kms.AsymmetricGetPublicKeyRequest.create({
       keyId: "<key_ID>",
     }),
   ).result;
   console.log(
     `key_id: ${publicKeyResponse.keyId}\n` +
     `public_key:\n${publicKeyResponse.publicKey}`,
   );
   ```

   In the code, set `keyId` to the ID of the asymmetric key.

3. Save the `public_key` value from the output to a local file, for example `public_key.pem`.

## How to use asymmetric keys for encryption

For asymmetric encryption, the public key can be used to encrypt data, and only the holder of the private key can decrypt data.

### Encrypting data

Encrypt the data locally with your public key by using an external tool such as [OpenSSL](https://openssl-library.org/source/):

```bash macOS theme={null}
openssl pkeyutl \
  -in <plaintext_file> \
  -encrypt \
  -pubin \
  -inkey <path_to_public_key> \
  -pkeyopt rsa_padding_mode:oaep \
  -pkeyopt rsa_oaep_md:sha256 \
  -pkeyopt rsa_mgf1_md:sha256 | base64
```

```bash Ubuntu theme={null}
openssl pkeyutl \
  -in <plaintext_file> \
  -encrypt \
  -pubin \
  -inkey <path_to_public_key> \
  -pkeyopt rsa_padding_mode:oaep \
  -pkeyopt rsa_oaep_md:sha256 \
  -pkeyopt rsa_mgf1_md:sha256 | base64 -w 0
```

In the command, specify the following parameters:

* `-in`: Path to the file with the plaintext data to encrypt. The maximum plaintext size is 446 bytes.
* `-inkey`: Path to the file containing the public key.

The output is the ciphertext in Base64. Save this value because it is required for [decrypting the data](#decrypting-data).

> **How the maximum plaintext size is calculated**
>
> The maximum size of a plaintext message to encrypt can be calculated by using the following formula:
>
> `Message length = (k - 2) - 2 × hash length`
>
> Where:
>
> * `k`: Length of the encryption key, in bytes.
> * `hash length`: Length of the hash function, in bytes.
>
> For the RSA-4096 (`rsa_4096_enc_oaep_sha_256`) algorithm:
>
> * `k = 512`, because an RSA-4096 key is 4096 bits long, which equals 512 bytes.
> * `hash length = 32`, because SHA-256 produces a 256-bit hash, which equals 32 bytes.
>
> `Message length = (512 - 2) - 2 × 32 = 446 bytes`

### Decrypting data

To decrypt data by using an asymmetric KMS key:

**CLI**

1. Decrypt the data:

   ```bash theme={null}
   nebius kms asymmetric-crypto decrypt \
     --key-id <key_ID> \
     --ciphertext <ciphertext>
   ```

   In the command, specify the following parameters:

   * `--key-id`: ID of the asymmetric KMS key that was used for encryption. To get it, run:

     ```bash theme={null}
     nebius kms asymmetric-key list
     ```

     In the output, copy the ID of the key that you used for encryption.
   * `--ciphertext`: Encrypted data returned as `ciphertext` when you encrypted the data.

   The output contains the Base64-encoded plaintext:

   ```yaml theme={null}
   key_id: kmsasymkey-e00***
   plaintext: SGVsbG8gd29ybGQ=
   ```

2. Decode the `plaintext` value from Base64.

   For example, to decode `SGVsbG8gd29ybGQ=`:

   ```bash macOS theme={null}
   echo 'SGVsbG8gd29ybGQ=' | base64 -d
   ```

   ```bash Ubuntu theme={null}
   echo 'SGVsbG8gd29ybGQ=' | base64 -d
   ```

**Go SDK**

Decrypt the data:

```go theme={null}
decryptCiphertext, err := base64.StdEncoding.DecodeString(
    "<ciphertext>",
)
if err != nil {
    return fmt.Errorf("decode ciphertext: %w", err)
}
decryptService := sdk.Services().KMS().V1().
    AsymmetricCrypto()
decryptResponse, err := decryptService.Decrypt(
    ctx,
    &kms.AsymmetricDecryptRequest{
        KeyId: "<key_ID>",
        Ciphertext: decryptCiphertext,
    },
)
if err != nil {
    return fmt.Errorf("decrypt with asymmetric crypto: %w", err)
}
fmt.Println(string(decryptResponse.GetPlaintext()))
```

In the code, specify the following parameters:

* `KeyId`: ID of the asymmetric KMS key that was used for encryption. To get it, list the asymmetric keys:

  ```go theme={null}
  asymListService := sdk.Services().KMS().V1().
      AsymmetricKey()
  asymListResponse, err := asymListService.List(
      ctx,
      &kms.ListAsymmetricKeysRequest{},
  )
  if err != nil {
      return fmt.Errorf("list asymmetric keys: %w", err)
  }
  fmt.Println(asymListResponse)
  ```

  In the output, copy the ID of the key that you used for encryption.
* `Ciphertext`: Base64-encoded ciphertext that you got when you [encrypted the data](#encrypting-data).

The code prints the decrypted data.

**Python SDK**

Decrypt the data:

```python theme={null}
service = kms.AsymmetricCryptoServiceClient(sdk)
response = await service.decrypt(
    kms.AsymmetricDecryptRequest(
        key_id="<key_ID>",
        ciphertext=base64.b64decode("<ciphertext>", validate=True),
    ),
)
print(response.plaintext.decode())
```

In the code, specify the following parameters:

* `key_id`: ID of the asymmetric KMS key that was used for encryption. To get it, list the asymmetric keys:

  ```python theme={null}
  service = kms.AsymmetricKeyServiceClient(sdk)
  response = await service.list(
      kms.ListAsymmetricKeysRequest(),
  )
  print(response)
  ```

  In the output, copy the ID of the key that you used for encryption.
* `ciphertext`: Base64-encoded ciphertext that you got when you [encrypted the data](#encrypting-data).

The code prints the decrypted data.

**JavaScript SDK**

Decrypt the data:

```ts theme={null}
const decryptService = new kms.AsymmetricCryptoService(sdk);
const decryptResponse = await decryptService.decrypt(
  kms.AsymmetricDecryptRequest.create({
    keyId: "<key_ID>",
    ciphertext: Buffer.from("<ciphertext>", "base64"),
  }),
).result;
console.log(Buffer.from(decryptResponse.plaintext).toString());
```

In the code, specify the following parameters:

* `keyId`: ID of the asymmetric KMS key that was used for encryption. To get it, list the asymmetric keys:

  ```ts theme={null}
  const asymListService = new kms.AsymmetricKeyService(sdk);
  const asymListResponse = await asymListService.list(
    kms.ListAsymmetricKeysRequest.create({}),
  ).result;
  console.log(asymListResponse);
  ```

  In the output, copy the ID of the key that you used for encryption.
* `ciphertext`: Base64-encoded ciphertext that you got when you [encrypted the data](#encrypting-data).

The code prints the decrypted data.

## How to use asymmetric keys for digital signatures

### Signing a hash

Use the private key of an asymmetric key pair to sign a hash that you generate yourself. The signature can be verified with the public key.

1. Generate a hash of the file or data that you want to sign and encode it in Base64.

   ```bash macOS theme={null}
   openssl dgst <hash_function> -binary <path_to_file> | base64
   ```

   ```bash Ubuntu theme={null}
   openssl dgst <hash_function> -binary <path_to_file> | base64 -w 0
   ```

   In the command:

   * `<hash_function>`: OpenSSL hash function to use when generating the hash. The value depends on the algorithm your key uses: set it to `-sha256` for `ecdsa_nist_p256_sha_256` keys and to `-sha384` for `ecdsa_nist_p384_sha_384` keys.
   * `<path_to_file>`: Path to the file for which you want to generate the hash.

   The command returns a hash value that you need to provide for signing.

2. Sign the hash:

   **CLI**

   ```bash theme={null}
   nebius kms asymmetric-crypto sign-hash \
     --key-id <key_ID> \
     --hash <hash>
   ```

   In the command, specify the following parameters:

   * `--key-id`: ID of the asymmetric KMS key to use to sign the hash. To get it, run:

     ```bash theme={null}
     nebius kms asymmetric-key list
     ```

     In the output, copy the ID of the key that you want to use.
   * `--hash`: The hash value that you generated, encoded in Base64.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmsasymkey-e00***
   signature: MEUCIQDT6TEx+by5ytXEEGxAbN/h+zv***
   ```

   **Go SDK**

   ```go theme={null}
   signHash, err := base64.StdEncoding.DecodeString(
       "<hash>",
   )
   if err != nil {
       return fmt.Errorf("decode hash: %w", err)
   }
   signService := sdk.Services().KMS().V1().
       AsymmetricCrypto()
   signResponse, err := signService.SignHash(
       ctx,
       &kms.AsymmetricSignHashRequest{
           KeyId: "<key_ID>",
           Hash: signHash,
       },
   )
   if err != nil {
       return fmt.Errorf("sign hash with asymmetric crypto: %w", err)
   }
   signJSON, err := protojson.Marshal(signResponse)
   if err != nil {
       return fmt.Errorf("encode response: %w", err)
   }
   fmt.Println(string(signJSON))
   ```

   In the code, specify the following parameters:

   * `KeyId`: ID of the asymmetric KMS key to use to sign the hash. To get it, list the asymmetric keys:

     ```go theme={null}
     asymListService := sdk.Services().KMS().V1().
         AsymmetricKey()
     asymListResponse, err := asymListService.List(
         ctx,
         &kms.ListAsymmetricKeysRequest{},
     )
     if err != nil {
         return fmt.Errorf("list asymmetric keys: %w", err)
     }
     fmt.Println(asymListResponse)
     ```

     In the output, copy the ID of the key that you want to use.
   * `Hash`: The hash value that you generated, encoded in Base64.

   The code prints the response in JSON. The `signature` value in the output contains the signature, encoded in Base64.

   **Python SDK**

   ```python theme={null}
   service = kms.AsymmetricCryptoServiceClient(sdk)
   response = await service.sign_hash(
       kms.AsymmetricSignHashRequest(
           key_id="<key_ID>",
           hash=base64.b64decode("<hash>", validate=True),
       ),
   )
   print(response.to_json())
   ```

   In the code, specify the following parameters:

   * `key_id`: ID of the asymmetric KMS key to use to sign the hash. To get it, list the asymmetric keys:

     ```python theme={null}
     service = kms.AsymmetricKeyServiceClient(sdk)
     response = await service.list(
         kms.ListAsymmetricKeysRequest(),
     )
     print(response)
     ```

     In the output, copy the ID of the key that you want to use.
   * `hash`: The hash value that you generated, encoded in Base64.

   The code prints the response in JSON. The `signature` value in the output contains the signature, encoded in Base64.

   **JavaScript SDK**

   ```ts theme={null}
   const signService = new kms.AsymmetricCryptoService(sdk);
   const signResponse = await signService.signHash(
     kms.AsymmetricSignHashRequest.create({
       keyId: "<key_ID>",
       hash: Buffer.from("<hash>", "base64"),
     }),
   ).result;
   console.log(kms.AsymmetricSignHashResponse.toJSON(signResponse));
   ```

   In the code, specify the following parameters:

   * `keyId`: ID of the asymmetric KMS key to use to sign the hash. To get it, list the asymmetric keys:

     ```ts theme={null}
     const asymListService = new kms.AsymmetricKeyService(sdk);
     const asymListResponse = await asymListService.list(
       kms.ListAsymmetricKeysRequest.create({}),
     ).result;
     console.log(asymListResponse);
     ```

     In the output, copy the ID of the key that you want to use.
   * `hash`: The hash value that you generated, encoded in Base64.

   The code prints the response in JSON. The `signature` value in the output contains the signature, encoded in Base64.

3. Save the `signature` value to a local file, for example `signature.b64`.

### Verifying a signature

You can verify a signature by using the public key of the asymmetric key pair and an external tool such as [OpenSSL](https://openssl-library.org/source/).

1. Decode the saved signature from Base64:

   ```bash theme={null}
   openssl base64 -d -A -in <path_to_signature_base64_file> -out <path_to_binary_signature_file>
   ```

   KMS returns the signature as a Base64-encoded string, while OpenSSL expects a binary signature file. This command converts the saved Base64 value to a binary file that OpenSSL can use.

   For example:

   ```bash theme={null}
   openssl base64 -d -A -in signature.b64 -out signature.bin
   ```

2. Verify the signature.

   ```bash theme={null}
   openssl dgst \
     <hash_function> \
     -verify <path_to_public_key> \
     -signature <path_to_binary_signature_file> \
     <path_to_file>
   ```

   In the command:

   * `<hash_function>`: OpenSSL hash function parameter to use when verifying the signature. The value depends on the algorithm your key uses: set it to `-sha256` for `ecdsa_nist_p256_sha_256` keys, and to `-sha384` for `ecdsa_nist_p384_sha_384` keys.
   * `-verify`: Path to the [public key](#how-to-get-the-public-key).
   * `-signature`: Path to the binary signature file.
   * `<path_to_file>`: Path to the signed file.

   If the signature is valid, OpenSSL returns:

   ```text theme={null}
   Verified OK
   ```
