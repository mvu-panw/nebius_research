# How to manage object versioning in a bucket

Source: https://docs.nebius.com/object-storage/buckets/versioning

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage object versioning in a bucket

Object versioning allows you to keep multiple versions of the same object in a bucket. When versioning is enabled, each update to an object creates a new version instead of replacing the existing one.

Versioning helps protect data from accidental deletion, overwriting or application errors and allows you to restore previous versions of objects.

When versioning is enabled for a bucket:

* Each object version receives a unique version ID
* Uploading an object with the same key creates a new version
* Previous versions remain stored in the bucket

If multiple write operations for the same object occur simultaneously, Object Storage stores all of the resulting object versions.

By default, versioning is disabled on buckets. After you enable versioning, you cannot fully disable it and can only suspend it.

> [!NOTE]
>
> For lower latency and higher throughput in high-load scenarios, we recommend using buckets with versioning disabled.

> [!WARNING]
>
> If your bucket has expiration lifecycle rules that permanently delete objects and you want to maintain the same behavior after enabling versioning, configure expiration for non-current object versions. Non-current version expiration rules manage the deletion of non-current object versions in a versioning-enabled bucket. For more information, see [Configure expiration lifecycle rules](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-expiration-lifecycle-rules).

## How to enable bucket versioning

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Object Storage**.
2. Open the page of the required bucket.
3. Go to the **Settings** tab.
4. In the **Versioning** field, select **Enabled**.
5. Click **Save changes**.

**Nebius AI Cloud CLI**

1. Get the bucket ID:
   ```bash theme={null}
   export BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <bucket_name> --format jsonpath='{.metadata.id}')
   ```
2. Enable versioning for the bucket:
   ```bash theme={null}
   nebius storage bucket update --id $BUCKET_ID --versioning-policy enabled
   ```

**AWS CLI**

Run the following command:

```bash theme={null}
aws s3api put-bucket-versioning \
  --bucket <bucket_name> \
  --versioning-configuration Status=Enabled \
  --endpoint-url https://storage.<region>.nebius.cloud
```

After versioning is enabled, all subsequent object uploads and modifications create new versions.

> [!NOTE]
>
> After you enable versioning for an *existing* bucket for the first time, it may take up to 15 minutes to come into effect. We recommend waiting 15 minutes before performing any write operations (`PUT` or `DELETE`) to avoid issues with object visibility and version tracking. If you enable or suspend versioning when [*creating* a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-create-buckets), it is available immediately with no waiting period.

## How to suspend bucket versioning

If needed, you can suspend versioning for a bucket:

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Object Storage**.
2. Open the page of the required bucket.
3. Go to the **Settings** tab.
4. In the **Versioning** field, enable the **Suspend** option.
5. Click **Save changes**.

**Nebius AI Cloud CLI**

1. Get the bucket ID:
   ```bash theme={null}
   export BUCKET_ID=$(nebius storage bucket get-by-name \
     --name <bucket_name> --format jsonpath='{.metadata.id}')
   ```
2. Suspend versioning for the bucket:
   ```bash theme={null}
   nebius storage bucket update --id $BUCKET_ID --versioning-policy suspended
   ```

**AWS CLI**

Run the following command:

```bash theme={null}
aws s3api put-bucket-versioning \
--bucket <bucket_name> \
--versioning-configuration Status=Suspended \
--endpoint-url https://storage.<region>.nebius.cloud
```
