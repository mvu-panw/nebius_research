# How data transfers handle destination objects

Source: https://docs.nebius.com/object-storage/transfer/destination-objects

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How data transfers handle destination objects

By the time an iteration of a data transfer starts, the destination bucket may already contain objects. You can configure what Object Storage does with them:

* [Overwrite objects](#overwriting-destination-objects) that have a newer pair in the source.
* [Delete objects](#deleting-destination-objects) that no longer have a pair in the source.
* Apply the overwrite/delete setting to [unmanaged objects](#unmanaged-destination-objects) (objects in the destination that weren't transferred at previous iterations).

## Overwriting destination objects

The setting to overwrite destination objects, also known as the *overwrite strategy* in the developer tools, determines what happens when the source and destination both contain an object with the same key. Depending on the setting's value, Object Storage overwrites the destination object with the source version or leaves it unchanged:

* **Overwrite if source is newer**: Object Storage overwrites a destination object only if the source object has a newer timestamp (based on the `Last-Modified` header). This value is recommended for incremental synchronization.
* **Do not overwrite**: Object Storage doesn't overwrite existing destination objects. If an object with the same key already exists in the destination, this source object is skipped. This is the safest option to avoid accidental data loss.

You can configure overwriting objects when you [create](https://docs.nebius.com/object-storage/transfer/launch.md) a data transfer (but not for existing transfers):

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Data Transfer**.
2. Click  **Create data transfer**.
3. Select the overwriting setting under **Destination** → **Overwriting destination objects**.

**CLI**

Set `.spec.overwrite_strategy` to one of the following values:

* `IF_NEWER`: Overwrite if source is newer.
* `NEVER`: Do not overwrite.

For example:

```json theme={null}
{
  "spec": {
    "overwrite_strategy": "IF_NEWER"
  }
}
```

**Terraform**

Set the `overwrite_strategy` argument to one of the following values in your resource block:

* `"IF_NEWER"`: Overwrite if source is newer.
* `"NEVER"`: Do not overwrite.

For example:

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example" {
  overwrite_strategy = "IF_NEWER"
  # Other parameters
}
```

## Deleting destination objects

The *delete strategy* determines what happens to a destination object when its source pair no longer exists (the object was deleted from the source).

* **Delete if not in source**: At each iteration the transfer deletes the destination object when it has no corresponding object in the source. Use this to keep the destination in synchronization with the source (for example, for a replication).
* **Do not delete**: The transfer never deletes destination objects. Objects that exist only in the destination are left as-is. Use it for a backup or when you add extra objects that shouldn't be removed.

You can configure deleting objects when you [create a data transfer](https://docs.nebius.com/object-storage/transfer/launch.md) (but not for existing transfers):

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Data Transfer**.
2. Click  **Create data transfer**.
3. Select the deleting setting under **Destination** → **Deleting destination objects**.

**CLI**

Set `.spec.enable_deletes_in_destination` to `true` or `false`:

* `true`: Delete if not in source.
* `false`: Do not delete.

For example:

```json theme={null}
{
  "spec": {
    "enable_deletes_in_destination": true
  }
}
```

**Terraform**

Set the `enable_deletes_in_destination` argument to one of the following values in your resource block:

* `true`: Delete if not in source.
* `false`: Do not delete.

For example:

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example" {
  enable_deletes_in_destination = true
  # Other parameters
}
```

## Unmanaged destination objects

*Unmanaged objects* are objects in the destination bucket that weren't copied from the source bucket during the current or past transfers. You can configure whether Object Storage can [overwrite](#overwriting-destination-objects) them with source objects or [delete](#deleting-destination-objects) them when they don't have pairs in the source:

* **Allow overwriting/deleting**: Object Storage overwrites or deletes unmanaged destination objects. Use only when you're sure that you will not upload important data directly to the destination.
* **Do not overwrite/delete** (default): Object Storage doesn't overwrite or delete unmanaged destination objects. Only destination objects that were copied from the source bucket during the current or past transfers are affected.

> **Example**
>
> Consider the following states of the source bucket and the destination bucket before the start of a transfer:
>
> **Source**
>
> * object\_1
> * object\_2
> * object\_3
>
> **Destination**
>
> * object\_4
>
> `object_4` in the destination is an unmanaged object. If the transfer is configured to delete destination objects that don't have pairs in the source, and allows overwriting/deleting unmanaged destination objects, `object_4` is deleted at the next iteration:
>
> **Source**
>
> * object\_1
> * object\_2
> * object\_3
>
> **Destination**
>
> * object\_1
> * object\_2
> * object\_3

You can configure how to handle unmanaged objects when you [create a data transfer](https://docs.nebius.com/object-storage/transfer/launch.md) (but not for existing transfers):

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Storage** → **Data Transfer**.
2. Click  **Create data transfer**.
3. Select the unmanaged objects setting under **Destination** → **Unmanaged objects**.

**CLI**

Set the `.spec.touch_unmanaged` parameter:

* `true`: Allow overwriting/deleting unmanaged destination objects.
* `false` (default): Do not overwrite/delete unmanaged destination objects.

Example:

```json theme={null}
{
  "spec": {
    "touch_unmanaged": false
  }
}
```

**Terraform**

Set the `touch_unmanaged` argument to one of the following values in your resource block:

* `true`: Allow overwriting/deleting unmanaged destination objects.
* `false` (default): Do not overwrite/delete unmanaged destination objects.

Example:

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example" {
  touch_unmanaged = false
  # Other parameters
}
```
