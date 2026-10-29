# Getting started with Key Management Service: Use symmetric keys for encryption

Source: https://docs.nebius.com/kms/quickstart/symmetric

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Key Management Service: Use symmetric keys for encryption

Key Management Service (KMS) lets you create symmetric keys that use the same key material for encryption and decryption. The example below shows how to create your first symmetric key, encrypt sample data and decrypt it.

## Prerequisites

You can create symmetric keys in any Nebius AI Cloud interface, but to encrypt and decrypt data, use the Nebius AI Cloud CLI or SDKs.

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

## Steps

### Create a symmetric key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Click  **Create key**.

3. On the key creation page:

   * In the **Name** field, enter `my-symmetric-key`.
   * In the **Type** field, preserve **Symmetric key**.

4. Click **Create key**.

This creates a symmetric key with the `AES_256_GCM` algorithm and the default rotation period of three months.

You need the key ID to encrypt and decrypt data. In the list of symmetric keys, click  next to the key ID of the key you created, then save the copied value to the `KEY_ID` environment variable:

```bash theme={null}
export KEY_ID=<key_ID>
```

**CLI**

Create a symmetric key:

```bash theme={null}
export KEY_ID=$(nebius kms symmetric-key create \
  --name my-symmetric-key \
  --algorithm aes_256 \
  --format jsonpath='{.metadata.id}')
```

This command includes the following parameters:

* `--name`: Name of the symmetric key.
* `--algorithm`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For symmetric keys, KMS only supports the `aes_256` algorithm.
* `--format jsonpath='{.metadata.id}'`: Returns only the key ID from the command output.

This command creates a symmetric key with the default rotation period of three months and saves the key ID to the `KEY_ID` environment variable.

**Go SDK**

Create a symmetric key:

```go theme={null}
symCreateService := sdk.Services().KMS().V1().
    SymmetricKey()
symCreateOperation, err := symCreateService.Create(
    ctx,
    &kms.CreateSymmetricKeyRequest{
        Metadata: &common.ResourceMetadata{
            Name: "my-symmetric-key",
        },
        Spec: &kms.SymmetricKeySpec{
            Algorithm: kms.SymmetricAlgorithm_AES_256,
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
symKeyID := symCreateOperation.ResourceID()
fmt.Println(symKeyID)
```

This code includes the following parameters:

* `Metadata.Name`: Name of the symmetric key.
* `Spec.Algorithm`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For symmetric keys, KMS only supports the `kms.SymmetricAlgorithm_AES_256` algorithm.

This code creates a symmetric key with the default rotation period of three months and prints the key ID. Save the key ID because you need it to encrypt and decrypt data.

**Python SDK**

Create a symmetric key:

```python theme={null}
service = kms.SymmetricKeyServiceClient(sdk)
operation = await service.create(
    kms.CreateSymmetricKeyRequest(
        metadata=ResourceMetadata(name="my-symmetric-key"),
        spec=kms.SymmetricKeySpec(
            algorithm=kms.SymmetricAlgorithm.AES_256,
        ),
    ),
)
await operation.wait()
sym_key_id = operation.resource_id
print(sym_key_id)
```

This code includes the following parameters:

* `metadata.name`: Name of the symmetric key.
* `spec.algorithm`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For symmetric keys, KMS only supports the `kms.SymmetricAlgorithm.AES_256` algorithm.

This code creates a symmetric key with the default rotation period of three months and prints the key ID. Save the key ID because you need it to encrypt and decrypt data.

**JavaScript SDK**

Create a symmetric key:

```ts theme={null}
const symCreateService = new kms.SymmetricKeyService(sdk);
const symCreateOperation = await symCreateService.create(
  kms.CreateSymmetricKeyRequest.create({
    metadata: { name: "my-symmetric-key" },
    spec: {
      algorithm: kms.SymmetricAlgorithm.AES_256,
    },
  }),
).result;
await symCreateOperation.wait();
const symKeyId = symCreateOperation.resourceId();
console.log(symKeyId);
```

This code includes the following parameters:

* `metadata.name`: Name of the symmetric key.
* `spec.algorithm`: [Encryption algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For symmetric keys, KMS only supports the `kms.SymmetricAlgorithm.AES_256` algorithm.

This code creates a symmetric key with the default rotation period of three months and prints the key ID. Save the key ID because you need it to encrypt and decrypt data.

### Encrypt data

**CLI**

1. Encode the text `Hello world` in Base64:

   ```bash Ubuntu theme={null}
   printf '%s' 'Hello world' | base64 -w 0
   ```

   ```bash macOS theme={null}
   printf '%s' 'Hello world' | base64
   ```

   The output looks like the following:

   ```text theme={null}
   SGVsbG8gd29ybGQ=
   ```

2. Encrypt the text `Hello world`:

   ```bash theme={null}
   nebius kms symmetric-crypto encrypt \
     --key-id "$KEY_ID" \
     --plaintext SGVsbG8gd29ybGQ=
   ```

   This command includes the following parameters:

   * `--key-id`: ID of the symmetric key that you created.
   * `--plaintext`: Base64-encoded value of your text.

   The command returns the `ciphertext` value that you need for decrypting the data later:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   ciphertext: AhIClM3o***
   ```

**Go SDK**

Encrypt the text `Hello world`:

```go theme={null}
encryptService := sdk.Services().KMS().V1().
    SymmetricCrypto()
encryptResponse, err := encryptService.Encrypt(
    ctx,
    &kms.SymmetricEncryptRequest{
        KeyId: "<key_ID>",
        Plaintext: []byte("Hello world"),
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

This code includes the following parameters:

* `KeyId`: ID of the symmetric key that you created.
* `Plaintext`: Your text.

The code prints the Base64-encoded `ciphertext` value that you need for decrypting the data later:

```yaml theme={null}
key_id: kmssymkey-e00***
ciphertext: AhIClM3o***
```

**Python SDK**

Encrypt the text `Hello world`:

```python theme={null}
service = kms.SymmetricCryptoServiceClient(sdk)
response = await service.encrypt(
    kms.SymmetricEncryptRequest(
        key_id="<key_ID>",
        plaintext="Hello world".encode(),
    ),
)
encrypt_encoded = base64.b64encode(
    response.ciphertext,
).decode("ascii")
print(f"key_id: {response.key_id}\nciphertext: {encrypt_encoded}")
```

This code includes the following parameters:

* `key_id`: ID of the symmetric key that you created.
* `plaintext`: Your text.

The code prints the Base64-encoded `ciphertext` value that you need for decrypting the data later:

```yaml theme={null}
key_id: kmssymkey-e00***
ciphertext: AhIClM3o***
```

**JavaScript SDK**

Encrypt the text `Hello world`:

```ts theme={null}
const encryptService = new kms.SymmetricCryptoService(sdk);
const encryptResponse = await encryptService.encrypt(
  kms.SymmetricEncryptRequest.create({
    keyId: "<key_ID>",
    plaintext: Buffer.from("Hello world"),
  }),
).result;
const encryptEncoded = Buffer.from(
  encryptResponse.ciphertext,
).toString("base64");
console.log(
  `key_id: ${encryptResponse.keyId}\nciphertext: ${encryptEncoded}`,
);
```

This code includes the following parameters:

* `keyId`: ID of the symmetric key that you created.
* `plaintext`: Your text.

The code prints the Base64-encoded `ciphertext` value that you need for decrypting the data later:

```yaml theme={null}
key_id: kmssymkey-e00***
ciphertext: AhIClM3o***
```

### Decrypt data

To decrypt the data, use the same symmetric key and the returned ciphertext:

**CLI**

1. Decrypt the data:

   ```bash theme={null}
   nebius kms symmetric-crypto decrypt \
     --key-id "$KEY_ID" \
     --ciphertext <ciphertext>
   ```

   This command includes the following parameters:

   * `--key-id`: ID of the symmetric key that you created.
   * `--ciphertext`: Ciphertext returned when you encrypted the plaintext.

   The output contains the Base64-encoded plaintext:

   ```yaml theme={null}
   key_id: kmssymkey-e00***
   plaintext: SGVsbG8gd29ybGQ=
   ```

2. Decode the `plaintext` value from Base64:

   ```bash theme={null}
   printf '%s' 'SGVsbG8gd29ybGQ=' | base64 -d
   ```

   The output is:

   ```text theme={null}
   Hello world
   ```

**Go SDK**

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
    },
)
if err != nil {
    return fmt.Errorf("decrypt with symmetric crypto: %w", err)
}
fmt.Println(string(decryptResponse.GetPlaintext()))
```

This code includes the following parameters:

* `KeyId`: ID of the symmetric key that you created.
* `Ciphertext`: Base64-encoded ciphertext returned when you encrypted the plaintext.

The code prints the decrypted text:

```text theme={null}
Hello world
```

**Python SDK**

```python theme={null}
service = kms.SymmetricCryptoServiceClient(sdk)
response = await service.decrypt(
    kms.SymmetricDecryptRequest(
        key_id="<key_ID>",
        ciphertext=base64.b64decode("<ciphertext>", validate=True),
    ),
)
print(response.plaintext.decode())
```

This code includes the following parameters:

* `key_id`: ID of the symmetric key that you created.
* `ciphertext`: Base64-encoded ciphertext returned when you encrypted the plaintext.

The code prints the decrypted text:

```text theme={null}
Hello world
```

**JavaScript SDK**

```ts theme={null}
const decryptService = new kms.SymmetricCryptoService(sdk);
const decryptResponse = await decryptService.decrypt(
  kms.SymmetricDecryptRequest.create({
    keyId: "<key_ID>",
    ciphertext: Buffer.from("<ciphertext>", "base64"),
  }),
).result;
console.log(Buffer.from(decryptResponse.plaintext).toString());
```

This code includes the following parameters:

* `keyId`: ID of the symmetric key that you created.
* `ciphertext`: Base64-encoded ciphertext returned when you encrypted the plaintext.

The code prints the decrypted text:

```text theme={null}
Hello world
```

## What's next

* Learn [how to rotate a symmetric key manually](https://docs.nebius.com/kms/manage/rotate.md)
* Learn how to encrypt larger volumes of data with [envelope encryption](https://docs.nebius.com/kms/cryptography/symmetric.md#how-to-use-envelope-encryption)
