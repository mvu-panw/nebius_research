# Data transfer limits on request rate and bandwidth

Source: https://docs.nebius.com/object-storage/transfer/limits

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Data transfer limits on request rate and bandwidth

Every data transfer has limits for request rate and bandwidth. You can set them when you [create](https://docs.nebius.com/object-storage/transfer/launch.md) or [modify](https://docs.nebius.com/object-storage/transfer/manage.md) a data transfer. The values of the limits represent maximum thresholds that a data transfer will not exceed. If you don't set the limits or set them to zero, the default values apply:

* Request rate: 4000 requests per second.
* Bandwidth: 50 GiB/s.

The limits are useful in the following cases:

* Your source provider imposes rate or bandwidth restrictions.
* You need to reserve request capacity and bandwidth for other processes.

The request rate and bandwidth cannot be unlimited, but you can set high values for them if you need large capacity.

To set the limits for request rate and bandwidth:

**Web console**

In the [web console](https://console.nebius.com/datatransfer), set transfer limits under **Destination**. Specify **Request rate limit** and **Bandwidth limit** with your desired values (for example, `1000` requests per second and `1073741824` bytes per second for 1 GiB/s) when you create or modify a data transfer.

**CLI**

Use the `.spec.limiters.requests_per_second` and `.spec.limiters.bandwidth_bytes_per_second` parameters:

```json theme={null}
{
  "spec": {
    "limiters": {
      "requests_per_second": 1000,
      "bandwidth_bytes_per_second": 1073741824
    },
    // Other parameters
  }
}
```

**Terraform**

Use the `limiters.requests_per_second` and `limiters.bandwidth_bytes_per_second` arguments:

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example" {
  limiters {
    requests_per_second          = 1000
    bandwidth_bytes_per_second   = 1073741824
  }
  # Other parameters
}
```
