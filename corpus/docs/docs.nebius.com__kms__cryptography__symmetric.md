# Cryptographic operations with symmetric keys

Source: https://docs.nebius.com/kms/cryptography/symmetric

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cryptographic operations with symmetric keys

You can use [symmetric keys](https://docs.nebius.com/kms/types-operations.md#symmetric-and-asymmetric-keys) in Key Management Service (KMS) to [encrypt](#how-to-encrypt-data) and [decrypt](#how-to-decrypt-data) application data directly. Alternatively, you can use [envelope encryption](#how-to-use-envelope-encryption) to encrypt larger volumes of data locally.

## Prerequisites

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
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

## How to encrypt data

The maximum size of data that you can encrypt with a symmetric KMS key is 64 KiB.

**CLI**

1. Prepare your data to be encrypted by encoding it in [Base64](https://developer.mozilla.org/en-US/docs/Glossary/Base64).

   For example, to encode `Hello world`:

   ```bash Ubuntu theme={null}
   echo -n "Hello world" | base64 -w 0
   ```

   ```bash macOS theme={null}
   echo -n "Hello world" | base64
   ```

   The output looks like the following:

   ```text theme={null}
   SGVsbG8gd29ybGQ=
   ```

2. Encrypt the data:

   ```bash theme={null}
   nebius kms symmetric-crypto encrypt \
     --key-id <key_ID> \
     --plaintext <plaintext_Base64> \
     --aad-context <AAD_context_Base64>
   ```

   In the command, specify the following parameters:

   * `--key-id`: ID of the symmetric key. To get it, run:

     ```bash theme={null}
     nebius kms symmetric-key list
     ```

     In the output, copy the ID of the key that you want to use.
   * `--plaintext`: Plaintext data to encrypt, encoded in Base64.
   * `--aad-context` (optional): Additional authenticated data (AAD) context linked to the ciphertext, encoded in Base64. If you specify this parameter during encryption, you must specify the same value for decryption.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
   ```

   The `ciphertext` parameter contains the encrypted version of your data. Save this value because it is required for [decrypting the data](#how-to-decrypt-data).

**Go SDK**

Encrypt the data:

```go theme={null}
encryptService := sdk.Services().KMS().V1().
    SymmetricCrypto()
encryptResponse, err := encryptService.Encrypt(
    ctx,
    &kms.SymmetricEncryptRequest{
        KeyId: "<key_ID>",
        Plaintext: []byte("<plaintext>"),
        AadContext: []byte("<AAD_context>"),
    },
)
if err != nil {
    return fmt.Errorf("encrypt with symmetric crypto: %w", err)
}
encryptEncoded := base64.StdEncoding.EncodeToString(
    encryptResponse.GetCiphertext(),
)
fmt.Printf("key_id: %s\nciphertext: %s\n",
    encryptResponse.GetKeyId(), encryptEncoded)
```

In the code, specify the following parameters:

* `KeyId`: ID of the symmetric key. To get it, list the symmetric keys:

  ```go theme={null}
  symListService := sdk.Services().KMS().V1().
      SymmetricKey()
  symListResponse, err := symListService.List(
      ctx,
      &kms.ListSymmetricKeysRequest{},
  )
  if err != nil {
      return fmt.Errorf("list symmetric keys: %w", err)
  }
  fmt.Println(symListResponse)
  ```

  In the output, copy the ID of the key that you want to use.
* `Plaintext`: Data to encrypt.
* `AadContext` (optional): Additional authenticated data (AAD) context linked to the ciphertext. If you specify this parameter during encryption, you must specify the same value for decryption. If you don't use AAD, omit this parameter.

The output looks like the following:

```yaml theme={null}
key_id: kmssymkey-e00***
ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
```

The `ciphertext` value contains the encrypted version of your data, encoded in Base64. Save this value because it is required for [decrypting the data](#how-to-decrypt-data).

**Python SDK**

Encrypt the data:

```python theme={null}
service = kms.SymmetricCryptoServiceClient(sdk)
response = await service.encrypt(
    kms.SymmetricEncryptRequest(
        key_id="<key_ID>",
        plaintext="<plaintext>".encode(),
        aad_context="<AAD_context>".encode(),
    ),
)
encrypt_encoded = base64.b64encode(
    response.ciphertext,
).decode("ascii")
print(f"key_id: {response.key_id}\nciphertext: {encrypt_encoded}")
```

In the code, specify the following parameters:

* `key_id`: ID of the symmetric key. To get it, list the symmetric keys:

  ```python theme={null}
  service = kms.SymmetricKeyServiceClient(sdk)
  response = await service.list(
      kms.ListSymmetricKeysRequest(),
  )
  print(response)
  ```

  In the output, copy the ID of the key that you want to use.
* `plaintext`: Data to encrypt.
* `aad_context` (optional): Additional authenticated data (AAD) context linked to the ciphertext. If you specify this parameter during encryption, you must specify the same value for decryption. If you don't use AAD, omit this parameter.

The output looks like the following:

```yaml theme={null}
key_id: kmssymkey-e00***
ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
```

The `ciphertext` value contains the encrypted version of your data, encoded in Base64. Save this value because it is required for [decrypting the data](#how-to-decrypt-data).

**JavaScript SDK**

Encrypt the data:

```ts theme={null}
const encryptService = new kms.SymmetricCryptoService(sdk);
const encryptResponse = await encryptService.encrypt(
  kms.SymmetricEncryptRequest.create({
    keyId: "<key_ID>",
    plaintext: Buffer.from("<plaintext>"),
    aadContext: Buffer.from("<AAD_context>"),
  }),
).result;
const encryptEncoded = Buffer.from(
  encryptResponse.ciphertext,
).toString("base64");
console.log(
  `key_id: ${encryptResponse.keyId}\nciphertext: ${encryptEncoded}`,
);
```

In the code, specify the following parameters:

* `keyId`: ID of the symmetric key. To get it, list the symmetric keys:

  ```ts theme={null}
  const symListService = new kms.SymmetricKeyService(sdk);
  const symListResponse = await symListService.list(
    kms.ListSymmetricKeysRequest.create({}),
  ).result;
  console.log(symListResponse);
  ```

  In the output, copy the ID of the key that you want to use.
* `plaintext`: Data to encrypt.
* `aadContext` (optional): Additional authenticated data (AAD) context linked to the ciphertext. If you specify this parameter during encryption, you must specify the same value for decryption. If you don't use AAD, omit this parameter.

The output looks like the following:

```yaml theme={null}
key_id: kmssymkey-e00***
ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
```

The `ciphertext` value contains the encrypted version of your data, encoded in Base64. Save this value because it is required for [decrypting the data](#how-to-decrypt-data).

## How to decrypt data

To decrypt data with a symmetric KMS key:

**CLI**

1. Decrypt the data:

   ```bash theme={null}
   nebius kms symmetric-crypto decrypt \
     --key-id <key_ID> \
     --ciphertext <ciphertext> \
     --aad-context <AAD_context_Base64>
   ```

   In the command, specify the following parameters:

   * `--key-id`: ID of the symmetric key that was used to encrypt the data. To get it, run:

     ```bash theme={null}
     nebius kms symmetric-key list
     ```

     In the output, copy the ID of the key that you used for encryption.
   * `--ciphertext`: Encrypted data returned as `ciphertext` when you [encrypted the data](#how-to-encrypt-data).
   * `--aad-context` (optional): Extra data linked to the ciphertext, encoded in Base64. If you specified this parameter when you encrypted the data, specify the same value during decryption.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   plaintext: SGVsbG8gd29ybGQ=
   ```

2. Decode the `plaintext` value from Base64.

   For example, to decode `SGVsbG8gd29ybGQ=`, run:

   ```bash theme={null}
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
    SymmetricCrypto()
decryptResponse, err := decryptService.Decrypt(
    ctx,
    &kms.SymmetricDecryptRequest{
        KeyId: "<key_ID>",
        Ciphertext: decryptCiphertext,
        AadContext: []byte("<AAD_context>"),
    },
)
if err != nil {
    return fmt.Errorf("decrypt with symmetric crypto: %w", err)
}
fmt.Println(string(decryptResponse.GetPlaintext()))
```

In the code, specify the following parameters:

* `KeyId`: ID of the symmetric key that was used to encrypt the data. To get it, list the symmetric keys:

  ```go theme={null}
  symListService := sdk.Services().KMS().V1().
      SymmetricKey()
  symListResponse, err := symListService.List(
      ctx,
      &kms.ListSymmetricKeysRequest{},
  )
  if err != nil {
      return fmt.Errorf("list symmetric keys: %w", err)
  }
  fmt.Println(symListResponse)
  ```

  In the output, copy the ID of the key that you used for encryption.
* `Ciphertext`: Base64-encoded encrypted data that you saved when you [encrypted the data](#how-to-encrypt-data).
* `AadContext` (optional): Extra data linked to the ciphertext. Specify the same value that you used when you encrypted the data. If you encrypted the data without AAD, omit this parameter.

The code prints the decrypted data.

**Python SDK**

Decrypt the data:

```python theme={null}
service = kms.SymmetricCryptoServiceClient(sdk)
response = await service.decrypt(
    kms.SymmetricDecryptRequest(
        key_id="<key_ID>",
        ciphertext=base64.b64decode("<ciphertext>", validate=True),
        aad_context="<AAD_context>".encode(),
    ),
)
print(response.plaintext.decode())
```

In the code, specify the following parameters:

* `key_id`: ID of the symmetric key that was used to encrypt the data. To get it, list the symmetric keys:

  ```python theme={null}
  service = kms.SymmetricKeyServiceClient(sdk)
  response = await service.list(
      kms.ListSymmetricKeysRequest(),
  )
  print(response)
  ```

  In the output, copy the ID of the key that you used for encryption.
* `ciphertext`: Base64-encoded encrypted data that you saved when you [encrypted the data](#how-to-encrypt-data).
* `aad_context` (optional): Extra data linked to the ciphertext. Specify the same value that you used when you encrypted the data. If you encrypted the data without AAD, omit this parameter.

The code prints the decrypted data.

**JavaScript SDK**

Decrypt the data:

```ts theme={null}
const decryptService = new kms.SymmetricCryptoService(sdk);
const decryptResponse = await decryptService.decrypt(
  kms.SymmetricDecryptRequest.create({
    keyId: "<key_ID>",
    ciphertext: Buffer.from("<ciphertext>", "base64"),
    aadContext: Buffer.from("<AAD_context>"),
  }),
).result;
console.log(Buffer.from(decryptResponse.plaintext).toString());
```

In the code, specify the following parameters:

* `keyId`: ID of the symmetric key that was used to encrypt the data. To get it, list the symmetric keys:

  ```ts theme={null}
  const symListService = new kms.SymmetricKeyService(sdk);
  const symListResponse = await symListService.list(
    kms.ListSymmetricKeysRequest.create({}),
  ).result;
  console.log(symListResponse);
  ```

  In the output, copy the ID of the key that you used for encryption.
* `ciphertext`: Base64-encoded encrypted data that you saved when you [encrypted the data](#how-to-encrypt-data).
* `aadContext` (optional): Extra data linked to the ciphertext. Specify the same value that you used when you encrypted the data. If you encrypted the data without AAD, omit this parameter.

The code prints the decrypted data.

## How to use envelope encryption

You can use [envelope encryption](https://docs.nebius.com/kms/types-operations.md#envelope-encryption) when you want KMS to use a key encryption key (KEK) stored in the service to protect a data encryption key (DEK), which is used by your application for encrypting data.

To use envelope encryption:

1. Generate a data key:

   **CLI**

   ```bash theme={null}
   nebius kms symmetric-crypto generate-data-key \
     --key-id <key_ID> \
     --data-key-spec aes_256 \
     --aad-context <AAD_context_Base64>
   ```

   In the command, specify the following parameters:

   * `--key-id`: ID of the symmetric KMS key that should encrypt the generated data key. To get it, run:

     ```bash theme={null}
     nebius kms symmetric-key list
     ```

     In the output, copy the ID of the key that you want to use.
   * `--data-key-spec`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) and key length for the generated data key. Only the `aes_256` value is supported.
   * `--aad-context` (optional): Extra data linked to the encrypted data key, encoded in Base64. If you specify this parameter, you must specify the same value when you later decrypt the encrypted data key.
   * `--skip-plaintext` (optional): Returns only the encrypted data key and doesn't return the plaintext key. For example, use this parameter if one application generates and stores encrypted data keys, while another application later decrypts and uses them. This reduces how often plaintext keys are exposed, but adds an extra step because the data key must be decrypted before use.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   data_key_plaintext: LpNuYDgpTjy0Z***
   data_key_ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
   ```

   The output contains two versions of the same generated data key:

   * `data_key_plaintext`: The plaintext version of the data key that you can use to encrypt the data.
   * `data_key_ciphertext`: The encrypted version of the data key that you need to provide to decrypt the data later.

   **Go SDK**

   ```go theme={null}
   dataKeyService := sdk.Services().KMS().V1().
       SymmetricCrypto()
   dataKeyResponse, err := dataKeyService.GenerateDataKey(
       ctx,
       &kms.GenerateDataKeyRequest{
           KeyId: "<key_ID>",
           AadContext: []byte("<AAD_context>"),
           DataKeySpec: kms.SymmetricAlgorithm_AES_256,
       },
   )
   if err != nil {
       return fmt.Errorf(
           "generate data key with symmetric crypto: %w", err,
       )
   }
   dataKeyEncoded := base64.StdEncoding.EncodeToString(
       dataKeyResponse.GetDataKeyCiphertext(),
   )
   fmt.Printf(
       "key_id: %s\ndata_key_plaintext: %s\ndata_key_ciphertext: %s\n",
       dataKeyResponse.GetKeyId(),
       base64.StdEncoding.EncodeToString(
           dataKeyResponse.GetDataKeyPlaintext(),
       ),
       dataKeyEncoded,
   )
   ```

   In the code, specify the following parameters:

   * `KeyId`: ID of the symmetric KMS key that should encrypt the generated data key. To get it, list the symmetric keys:

     ```go theme={null}
     symListService := sdk.Services().KMS().V1().
         SymmetricKey()
     symListResponse, err := symListService.List(
         ctx,
         &kms.ListSymmetricKeysRequest{},
     )
     if err != nil {
         return fmt.Errorf("list symmetric keys: %w", err)
     }
     fmt.Println(symListResponse)
     ```

     In the output, copy the ID of the key that you want to use.
   * `AadContext` (optional): Additional authenticated data (AAD) context linked to the encrypted data key. If you specify this parameter, you must specify the same value when you later decrypt the encrypted data key. If you don't use AAD, omit this parameter.
   * `DataKeySpec`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) and key length for the generated data key. Only the `kms.SymmetricAlgorithm_AES_256` value is supported.

   To get only the encrypted data key without the plaintext key, add `SkipPlaintext: true` to the request. For example, do this if one application generates and stores encrypted data keys, while another application later decrypts and uses them. This reduces how often plaintext keys are exposed, but adds an extra step because the data key must be decrypted before use.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   data_key_plaintext: LpNuYDgpTjy0Z***
   data_key_ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
   ```

   The output contains two versions of the same generated data key, encoded in Base64:

   * `data_key_plaintext`: The plaintext version of the data key that you can use to encrypt the data.
   * `data_key_ciphertext`: The encrypted version of the data key that you need to provide to decrypt the data later.

   **Python SDK**

   ```python theme={null}
   service = kms.SymmetricCryptoServiceClient(sdk)
   response = await service.generate_data_key(
       kms.GenerateDataKeyRequest(
           key_id="<key_ID>",
           aad_context="<AAD_context>".encode(),
           data_key_spec=kms.SymmetricAlgorithm.AES_256,
       ),
   )
   data_key_encoded = base64.b64encode(
       response.data_key_ciphertext,
   ).decode("ascii")
   data_key_plaintext = base64.b64encode(
       response.data_key_plaintext,
   ).decode("ascii")
   print(
       f"key_id: {response.key_id}\n"
       f"data_key_plaintext: {data_key_plaintext}\n"
       f"data_key_ciphertext: {data_key_encoded}"
   )
   ```

   In the code, specify the following parameters:

   * `key_id`: ID of the symmetric KMS key that should encrypt the generated data key. To get it, list the symmetric keys:

     ```python theme={null}
     service = kms.SymmetricKeyServiceClient(sdk)
     response = await service.list(
         kms.ListSymmetricKeysRequest(),
     )
     print(response)
     ```

     In the output, copy the ID of the key that you want to use.
   * `aad_context` (optional): Additional authenticated data (AAD) context linked to the encrypted data key. If you specify this parameter, you must specify the same value when you later decrypt the encrypted data key. If you don't use AAD, omit this parameter.
   * `data_key_spec`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) and key length for the generated data key. Only the `kms.SymmetricAlgorithm.AES_256` value is supported.

   To get only the encrypted data key without the plaintext key, add `skip_plaintext=True` to the request. For example, do this if one application generates and stores encrypted data keys, while another application later decrypts and uses them. This reduces how often plaintext keys are exposed, but adds an extra step because the data key must be decrypted before use.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   data_key_plaintext: LpNuYDgpTjy0Z***
   data_key_ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
   ```

   The output contains two versions of the same generated data key, encoded in Base64:

   * `data_key_plaintext`: The plaintext version of the data key that you can use to encrypt the data.
   * `data_key_ciphertext`: The encrypted version of the data key that you need to provide to decrypt the data later.

   **JavaScript SDK**

   ```ts theme={null}
   const dataKeyService = new kms.SymmetricCryptoService(sdk);
   const dataKeyResponse = await dataKeyService.generateDataKey(
     kms.GenerateDataKeyRequest.create({
       keyId: "<key_ID>",
       aadContext: Buffer.from("<AAD_context>"),
       dataKeySpec: kms.SymmetricAlgorithm.AES_256,
     }),
   ).result;
   const dataKeyEncoded = Buffer.from(
     dataKeyResponse.dataKeyCiphertext,
   ).toString("base64");
   const dataKeyPlaintext = Buffer.from(
     dataKeyResponse.dataKeyPlaintext,
   ).toString("base64");
   console.log(
     `key_id: ${dataKeyResponse.keyId}\n` +
     `data_key_plaintext: ${dataKeyPlaintext}\n` +
     `data_key_ciphertext: ${dataKeyEncoded}`,
   );
   ```

   In the code, specify the following parameters:

   * `keyId`: ID of the symmetric KMS key that should encrypt the generated data key. To get it, list the symmetric keys:

     ```ts theme={null}
     const symListService = new kms.SymmetricKeyService(sdk);
     const symListResponse = await symListService.list(
       kms.ListSymmetricKeysRequest.create({}),
     ).result;
     console.log(symListResponse);
     ```

     In the output, copy the ID of the key that you want to use.
   * `aadContext` (optional): Additional authenticated data (AAD) context linked to the encrypted data key. If you specify this parameter, you must specify the same value when you later decrypt the encrypted data key. If you don't use AAD, omit this parameter.
   * `dataKeySpec`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) and key length for the generated data key. Only the `kms.SymmetricAlgorithm.AES_256` value is supported.

   To get only the encrypted data key without the plaintext key, add `skipPlaintext: true` to the request. For example, do this if one application generates and stores encrypted data keys, while another application later decrypts and uses them. This reduces how often plaintext keys are exposed, but adds an extra step because the data key must be decrypted before use.

   The output looks like the following:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   data_key_plaintext: LpNuYDgpTjy0Z***
   data_key_ciphertext: CAESI2ttc3N5bWtleXZlcnNpb24tZTAwcmV0OXM1bTV4dnp6OHR***
   ```

   The output contains two versions of the same generated data key, encoded in Base64:

   * `data_key_plaintext`: The plaintext version of the data key that you can use to encrypt the data.
   * `data_key_ciphertext`: The encrypted version of the data key that you need to provide to decrypt the data later.

2. Decode the `data_key_plaintext` value from Base64 and use the resulting key to encrypt the data locally, for example, with AES-256-GCM. Store the encrypted data key together with the encrypted data and delete the plaintext data key.

3. When you need to decrypt the data later, decrypt the data key:

   **CLI**

   ```bash theme={null}
   nebius kms symmetric-crypto decrypt \
     --key-id <key_ID> \
     --ciphertext <data_key_ciphertext> \
     --aad-context <AAD_context_Base64>
   ```

   In the command, specify the following parameters:

   * `--key-id`: ID of the symmetric KMS key that was used to generate the data key. To get it, run:

     ```bash theme={null}
     nebius kms symmetric-key list
     ```

     In the output, copy the ID of the key that you used to generate the data key.
   * `--ciphertext`: The `data_key_ciphertext` value that was returned when you generated the data key.
   * `--aad-context` (optional): Extra data linked to the encrypted data key, encoded in Base64. Specify this parameter only if you provided it when you generated the data key. In that case, specify the same value here.

   The output contains the plaintext data key.

   **Go SDK**

   ```go theme={null}
   dataDecryptCiphertext, err :=
       base64.StdEncoding.DecodeString(
       "<data_key_ciphertext>",
   )
   if err != nil {
       return fmt.Errorf("decode data key ciphertext: %w", err)
   }
   dataDecryptService := sdk.Services().KMS().V1().
       SymmetricCrypto()
   dataDecryptResponse, err := dataDecryptService.Decrypt(
       ctx,
       &kms.SymmetricDecryptRequest{
           KeyId: "<key_ID>",
           Ciphertext: dataDecryptCiphertext,
           AadContext: []byte("<AAD_context>"),
       },
   )
   if err != nil {
       return fmt.Errorf("decrypt with symmetric crypto: %w", err)
   }
   dataDecryptJSON, err := protojson.Marshal(dataDecryptResponse)
   if err != nil {
       return fmt.Errorf("encode response: %w", err)
   }
   fmt.Println(string(dataDecryptJSON))
   ```

   In the code, specify the following parameters:

   * `KeyId`: ID of the symmetric KMS key that was used to generate the data key. To get it, list the symmetric keys:

     ```go theme={null}
     symListService := sdk.Services().KMS().V1().
         SymmetricKey()
     symListResponse, err := symListService.List(
         ctx,
         &kms.ListSymmetricKeysRequest{},
     )
     if err != nil {
         return fmt.Errorf("list symmetric keys: %w", err)
     }
     fmt.Println(symListResponse)
     ```

     In the output, copy the ID of the key that you used to generate the data key.
   * `Ciphertext`: The `data_key_ciphertext` value from the output when you generated the data key.
   * `AadContext` (optional): Extra data linked to the encrypted data key. Specify the same value that you used when you generated the data key. If you generated the data key without AAD, omit this parameter.

   The response returns the plaintext data key in `Plaintext`.

   **Python SDK**

   ```python theme={null}
   service = kms.SymmetricCryptoServiceClient(sdk)
   response = await service.decrypt(
       kms.SymmetricDecryptRequest(
           key_id="<key_ID>",
           ciphertext=base64.b64decode(
               "<data_key_ciphertext>", validate=True,
           ),
           aad_context="<AAD_context>".encode(),
       ),
   )
   print(response.to_json())
   ```

   In the code, specify the following parameters:

   * `key_id`: ID of the symmetric KMS key that was used to generate the data key. To get it, list the symmetric keys:

     ```python theme={null}
     service = kms.SymmetricKeyServiceClient(sdk)
     response = await service.list(
         kms.ListSymmetricKeysRequest(),
     )
     print(response)
     ```

     In the output, copy the ID of the key that you used to generate the data key.
   * `ciphertext`: The `data_key_ciphertext` value from the output when you generated the data key.
   * `aad_context` (optional): Extra data linked to the encrypted data key. Specify the same value that you used when you generated the data key. If you generated the data key without AAD, omit this parameter.

   The response returns the plaintext data key in `plaintext`.

   **JavaScript SDK**

   ```ts theme={null}
   const dataDecryptService =
     new kms.SymmetricCryptoService(sdk);
   const dataDecryptResponse = await dataDecryptService.decrypt(
     kms.SymmetricDecryptRequest.create({
       keyId: "<key_ID>",
       ciphertext: Buffer.from("<data_key_ciphertext>", "base64"),
       aadContext: Buffer.from("<AAD_context>"),
     }),
   ).result;
   console.log(kms.SymmetricDecryptResponse.toJSON(dataDecryptResponse));
   ```

   In the code, specify the following parameters:

   * `keyId`: ID of the symmetric KMS key that was used to generate the data key. To get it, list the symmetric keys:

     ```ts theme={null}
     const symListService = new kms.SymmetricKeyService(sdk);
     const symListResponse = await symListService.list(
       kms.ListSymmetricKeysRequest.create({}),
     ).result;
     console.log(symListResponse);
     ```

     In the output, copy the ID of the key that you used to generate the data key.
   * `ciphertext`: The `data_key_ciphertext` value from the output when you generated the data key.
   * `aadContext` (optional): Extra data linked to the encrypted data key. Specify the same value that you used when you generated the data key. If you generated the data key without AAD, omit this parameter.

   The response returns the plaintext data key in `plaintext`.

4. Use the plaintext data key that KMS returned to decrypt the data locally.
