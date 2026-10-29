# Object key prefixes in data transfers

Source: https://docs.nebius.com/object-storage/transfer/key-prefixes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Object key prefixes in data transfers

By default, all source objects are transferred in a data transfer, and their [keys](https://docs.nebius.com/object-storage/overview.md#keys-prefixes-and-object-hierarchy) are unchanged in the destination. You can optionally use source and destination prefixes to change this behavior:

* *Source prefix* filters objects in the source bucket.
* *Destination prefix* is added to keys of all transferred objects.

> For example, if the source prefix is `test_dir/` and the destination prefix is `migration/`, the data transfer only works with source objects that have keys starting with `test_dir/`. In the destination, the data transfer replaces the `test_dir/` prefix in object keys with `migration/`. A source object named `test_dir/somefile.txt` becomes `migration/somefile.txt` in the destination.

You can specify prefixes when you [create](https://docs.nebius.com/object-storage/transfer/launch.md) or [modify](https://docs.nebius.com/object-storage/transfer/manage.md) a data transfer:

**Web console**

In the [web console](https://console.nebius.com/datatransfer), append prefixes to the names of the source and destination buckets (for example, `mybucket/test_dir/`).

**CLI**

Set the `.spec.source.prefix` and `.spec.destination.prefix` parameters in your configuration file:

```json theme={null}
{
  "spec": {
    "source": {
      "prefix": "test_dir/"
    },
    "destination": {
      "prefix": "migration/"
    }
  }
}
```

**Terraform**

Use the `prefix` argument in the `source` and `destination` blocks:

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example" {
  source {
    prefix = "test_dir/"
    # Other source parameters
  }
  destination {
    prefix = "migration/"
    # Other destination parameters
  }
  # Other parameters
}
```
