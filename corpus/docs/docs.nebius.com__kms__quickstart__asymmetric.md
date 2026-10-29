# Getting started with Key Management Service: Sign a hash with asymmetric keys

Source: https://docs.nebius.com/kms/quickstart/asymmetric

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Key Management Service: Sign a hash with asymmetric keys

Key Management Service (KMS) lets you create asymmetric keys that use a public and private key pair. The example below focuses on digital signatures and shows how to create your first asymmetric key, get its public key, sign a hash of a test file and verify the resulting signature.

## Prerequisites

You can create asymmetric keys in any Nebius AI Cloud interface. To sign hashes, use the Nebius AI Cloud CLI or SDKs. To verify signatures, use a local cryptographic tool such as [OpenSSL](https://openssl-library.org/source/).

**CLI**

1. Make sure that [OpenSSL](https://openssl-library.org/source/) is installed on your local machine. In this guide, you use it to generate a local hash of a file and verify a returned signature with a public key locally.
2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. Make sure that [OpenSSL](https://openssl-library.org/source/) is installed on your local machine. In this guide, you use it to verify a returned signature with a public key locally.
2. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. Make sure that [OpenSSL](https://openssl-library.org/source/) is installed on your local machine. In this guide, you use it to verify a returned signature with a public key locally.
2. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. Make sure that [OpenSSL](https://openssl-library.org/source/) is installed on your local machine. In this guide, you use it to verify a returned signature with a public key locally.
2. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Steps

### Create an asymmetric key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.

2. Click  **Create key**.

3. On the key creation page:

   * In the **Name** field, enter `my-asymmetric-key`.
   * In the **Type** field, select **Asymmetric key**.
   * In the **Algorithm** field, select **ECC (P-256)** to create a key that you can use for digital signature workflows.

4. Click **Create key**.

You need the key ID to get the public key and sign a hash. In the list of asymmetric keys, click  next to the key ID of the key you created, then save the copied value to the `KEY_ID` environment variable:

```bash theme={null}
export KEY_ID=<key_ID>
```

**CLI**

Create an asymmetric key:

```bash theme={null}
export KEY_ID=$(nebius kms asymmetric-key create \
   --name my-asymmetric-key \
   --algorithm ecdsa_nist_p256_sha_256 \
   --format jsonpath='{.metadata.id}')
```

This command includes the following parameters:

* `--name`: Name of the asymmetric key.
* `--algorithm`: [Algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For creating a key that you can use for digital signature workflows, set to `ecdsa_nist_p256_sha_256`.
* `--format jsonpath='{.metadata.id}'`: Returns only the key ID from the command output.

This command creates a public-private key pair and saves the key ID to the `KEY_ID` environment variable.

**Go SDK**

Create an asymmetric key:

```go theme={null}
asymCreateService := sdk.Services().KMS().V1().
    AsymmetricKey()
asymCreateOperation, err := asymCreateService.Create(
    ctx,
    &kms.CreateAsymmetricKeyRequest{
        Metadata: &common.ResourceMetadata{
            Name: "my-asymmetric-key",
        },
        Spec: &kms.AsymmetricKeySpec{
            Algorithm: kms.
                AsymmetricAlgorithm_ECDSA_NIST_P256_SHA_256,
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
asymKeyID := asymCreateOperation.ResourceID()
fmt.Println(asymKeyID)
```

This code includes the following parameters:

* `Metadata.Name`: Name of the asymmetric key.
* `Spec.Algorithm`: [Algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For creating a key that you can use for digital signature workflows, set to `kms.AsymmetricAlgorithm_ECDSA_NIST_P256_SHA_256`.

This code creates a public-private key pair and prints the key ID. Save the key ID because you need it to get the public key and sign a hash.

**Python SDK**

Create an asymmetric key:

```python theme={null}
service = kms.AsymmetricKeyServiceClient(sdk)
operation = await service.create(
    kms.CreateAsymmetricKeyRequest(
        metadata=ResourceMetadata(name="my-asymmetric-key"),
        spec=kms.AsymmetricKeySpec(
            algorithm=kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256,
        ),
    ),
)
await operation.wait()
asym_key_id = operation.resource_id
print(asym_key_id)
```

This code includes the following parameters:

* `metadata.name`: Name of the asymmetric key.
* `spec.algorithm`: [Algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For creating a key that you can use for digital signature workflows, set to `kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256`.

This code creates a public-private key pair and prints the key ID. Save the key ID because you need it to get the public key and sign a hash.

**JavaScript SDK**

Create an asymmetric key:

```ts theme={null}
const asymCreateService = new kms.AsymmetricKeyService(sdk);
const asymCreateOperation = await asymCreateService.create(
  kms.CreateAsymmetricKeyRequest.create({
    metadata: { name: "my-asymmetric-key" },
    spec: {
      algorithm: kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256,
    },
  }),
).result;
await asymCreateOperation.wait();
const asymKeyId = asymCreateOperation.resourceId();
console.log(asymKeyId);
```

This code includes the following parameters:

* `metadata.name`: Name of the asymmetric key.
* `spec.algorithm`: [Algorithm](https://docs.nebius.com/kms/types-operations.md#encryption-algorithms) that the key uses. For creating a key that you can use for digital signature workflows, set to `kms.AsymmetricAlgorithm.ECDSA_NIST_P256_SHA_256`.

This code creates a public-private key pair and prints the key ID. Save the key ID because you need it to get the public key and sign a hash.

### Get the public key

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Cryptography** → **KMS**.
2. Select **Asymmetric keys** and click the key you created.
3. On the **Key's overview** tab, next to **Public key**, click .
4. Create the `public_key.pem` file with the copied contents.

**CLI**

Run the following command:

```bash theme={null}
nebius kms asymmetric-crypto get-public-key \
  --key-id "$KEY_ID" \
  --format jsonpath='{.public_key}' > public_key.pem
```

This command includes the following parameters:

* `--key-id`: ID of the asymmetric key that you created.
* `--format jsonpath='{.public_key}'`: Returns only the `public_key` value.

This command writes the public key to the `public_key.pem` file.

**Go SDK**

Get the public key:

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
if err := os.WriteFile(
    "public_key.pem", []byte(publicKeyResponse.GetPublicKey()), 0600,
); err != nil {
    return fmt.Errorf("write public_key.pem: %w", err)
}
```

In the code, set `KeyId` to the ID of the asymmetric key that you created.

This code writes the public key to the `public_key.pem` file.

**Python SDK**

Get the public key:

```python theme={null}
service = kms.AsymmetricCryptoServiceClient(sdk)
response = await service.get_public_key(
    kms.AsymmetricGetPublicKeyRequest(
        key_id="<key_ID>",
    ),
)
Path("public_key.pem").write_text(response.public_key)
```

In the code, set `key_id` to the ID of the asymmetric key that you created.

This code writes the public key to the `public_key.pem` file.

**JavaScript SDK**

Get the public key:

```ts theme={null}
const publicKeyService =
  new kms.AsymmetricCryptoService(sdk);
const publicKeyResponse = await publicKeyService.getPublicKey(
  kms.AsymmetricGetPublicKeyRequest.create({
    keyId: "<key_ID>",
  }),
).result;
await writeFile("public_key.pem", publicKeyResponse.publicKey);
```

In the code, set `keyId` to the ID of the asymmetric key that you created.

This code writes the public key to the `public_key.pem` file.

### Sign a hash

1. Create the `hello.txt` file:

   **CLI**

   ```bash theme={null}
   echo 'Hello world' > hello.txt
   ```

   **Go SDK**

   ```go theme={null}
   if err := os.WriteFile(
       "hello.txt", []byte("Hello world\n"), 0600,
   ); err != nil {
       return fmt.Errorf("write plaintext file: %w", err)
   }
   ```

   **Python SDK**

   ```python theme={null}
   Path("hello.txt").write_text("Hello world\n")
   ```

   **JavaScript SDK**

   ```ts theme={null}
   await writeFile("hello.txt", "Hello world\n");
   ```

2. Generate a SHA-256 hash of the file and encode it in Base64:

   **CLI**

   ```bash theme={null}
   HASH_B64="$(openssl dgst -sha256 -binary hello.txt | openssl base64 -A)"
   printf '%s\n' "$HASH_B64"
   ```

   The command returns a Base64-encoded hash value that you need to provide for signing and saves it to the `HASH_B64` environment variable.

   **Go SDK**

   ```go theme={null}
   hashInput, err := os.ReadFile("hello.txt")
   if err != nil {
       return fmt.Errorf("read signing input: %w", err)
   }
   hashDigest := sha256.Sum256(hashInput)
   hashEncoded := base64.StdEncoding.EncodeToString(hashDigest[:])
   fmt.Println(hashEncoded)
   ```

   The code prints a Base64-encoded hash value that you need to provide for signing.

   **Python SDK**

   ```python theme={null}
   hash_input = Path("hello.txt").read_bytes()
   hash_digest = hashlib.sha256(hash_input).digest()
   hash_encoded = base64.b64encode(hash_digest).decode("ascii")
   print(hash_encoded)
   ```

   The code prints a Base64-encoded hash value that you need to provide for signing.

   **JavaScript SDK**

   ```ts theme={null}
   const hashInput = await readFile("hello.txt");
   const hashEncoded = createHash("sha256")
     .update(hashInput).digest("base64");
   console.log(hashEncoded);
   ```

   The code prints a Base64-encoded hash value that you need to provide for signing.

3. Send the hash value to KMS to sign it with your asymmetric key:

   **CLI**

   ```bash theme={null}
   nebius kms asymmetric-crypto sign-hash \
     --key-id "$KEY_ID" \
     --hash "$HASH_B64" \
     --format jsonpath='{.signature}' > signature.b64
   ```

   This command includes the following parameters:

   * `--key-id`: ID of the asymmetric key that you created.
   * `--hash`: Base64-encoded hash value generated in the previous step.
   * `--format jsonpath='{.signature}'`: Returns only the `signature` value.

   This command returns the signature as a Base64-encoded string and writes it to the `signature.b64` file.

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
   signEncoded := base64.StdEncoding.EncodeToString(
       signResponse.GetSignature(),
   )
   if err := os.WriteFile(
       "signature.b64", []byte(signEncoded), 0600,
   ); err != nil {
       return fmt.Errorf("write signature.b64: %w", err)
   }
   ```

   This code includes the following parameters:

   * `KeyId`: ID of the asymmetric key that you created.
   * `Hash`: Base64-encoded hash value generated in the previous step.

   This code encodes the returned signature in Base64 and writes it to the `signature.b64` file.

   **Python SDK**

   ```python theme={null}
   service = kms.AsymmetricCryptoServiceClient(sdk)
   response = await service.sign_hash(
       kms.AsymmetricSignHashRequest(
           key_id="<key_ID>",
           hash=base64.b64decode("<hash>", validate=True),
       ),
   )
   Path("signature.b64").write_bytes(
       base64.b64encode(response.signature),
   )
   ```

   This code includes the following parameters:

   * `key_id`: ID of the asymmetric key that you created.
   * `hash`: Base64-encoded hash value generated in the previous step.

   This code encodes the returned signature in Base64 and writes it to the `signature.b64` file.

   **JavaScript SDK**

   ```ts theme={null}
   const signService = new kms.AsymmetricCryptoService(sdk);
   const signResponse = await signService.signHash(
     kms.AsymmetricSignHashRequest.create({
       keyId: "<key_ID>",
       hash: Buffer.from("<hash>", "base64"),
     }),
   ).result;
   await writeFile(
     "signature.b64",
     Buffer.from(signResponse.signature).toString("base64"),
   );
   ```

   This code includes the following parameters:

   * `keyId`: ID of the asymmetric key that you created.
   * `hash`: Base64-encoded hash value generated in the previous step.

   This code encodes the returned signature in Base64 and writes it to the `signature.b64` file.

### Verify the signature

Verify the signature to confirm that it was created with the matching private key and that the file was not changed after it was signed.

1. Decode the saved signature in the `signature.b64` file, convert it to binary form and save it to the `signature.bin` file:

   ```bash theme={null}
   openssl base64 -d -A -in signature.b64 -out signature.bin
   ```

   OpenSSL uses the binary form of the signature for verification. Therefore, you need the `signature.bin` file in the next step.

2. Verify the signature with the public key:

   ```bash theme={null}
   openssl dgst \
     -sha256 \
     -verify public_key.pem \
     -signature signature.bin \
     hello.txt
   ```

   This command includes the following parameters:

   * `-sha256`: Hash function that matches `ecdsa_nist_p256_sha_256`.
   * `-verify`: Uses the public key file to check whether the signature was created with the matching private key.
   * `-signature`: Specifies the signature file to use for verifying the signature.
   * `hello.txt`: File that OpenSSL checks against the signature.

   If the signature is valid, OpenSSL returns:

   ```text theme={null}
   Verified OK
   ```

## What's next

* Learn [how to use asymmetric keys for encryption and decryption](https://docs.nebius.com/kms/cryptography/asymmetric.md)
