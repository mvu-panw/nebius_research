# Data transfer types and stop conditions

Source: https://docs.nebius.com/object-storage/transfer/stop-condition

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Data transfer types and stop conditions

Data transfers are based on consecutive [iterations](https://docs.nebius.com/object-storage/transfer/overview.md#iterations). Each iteration passes the source and destination buckets once. You can configure the number of iterations and the interval between them. To do so:

* Specify the data transfer type if you [launch the data transfer](https://docs.nebius.com/object-storage/transfer/launch.md) in the web console.
* Set the stop condition if you launch the data transfer by using the CLI or other developer tools.

## Data transfer type (web console)

When you create a data transfer in the web console, you can select the *data transfer type*:

* **One-time transfer**: Data transfer is completed after just one iteration. One-time transfers are designed for data migration and backup.
* **Replication**: Iterations continue until you stop or delete the data transfer. Replications are designed for continuous synchronization between a source and a destination.

## Stop condition (developer tools)

When you use the CLI or other developer tools to create a data transfer, set a *stop condition* in the data transfer configuration. This condition specifies when the data transfer should stop.

The configuration must include exactly one of the following options:

* `.spec.after_one_iteration` (same as the **One-time transfer** type): Transfer stops after completing its first iteration. The value should be an empty object.

  **CLI**

  ```json theme={null}
  {
    "spec": {
      "after_one_iteration": {},
      // Other parameters
    }
  }
  ```

  **Terraform**

  ```hcl theme={null}
  resource "nebius_storage_v1_transfer" "one_time_transfer" {
    stop_condition {
      after_one_iteration = true
    }
    # Other parameters
  }
  ```

* `.spec.after_n_empty_iterations`: Transfer stops after a number of consecutive [empty iterations](https://docs.nebius.com/object-storage/transfer/overview.md#empty-iterations). For example, after five iterations:

  **CLI**

  ```json theme={null}
  {
    "spec": {
      "after_n_empty_iterations": {
        "empty_iterations_threshold": 5
      },
      // Other parameters
    }
  }
  ```

  **Terraform**

  ```hcl theme={null}
  resource "nebius_storage_v1_transfer" "empty_iterations_transfer" {
    stop_condition {
      after_n_empty_iterations {
        empty_iterations_threshold = 5
      }
    }
    # Other parameters
  }
  ```

* `.spec.infinite` (same as the **Replication** type): Transfer continues indefinitely until manually stopped.

  **CLI**

  ```json theme={null}
  {
    "spec": {
      "infinite": {},
      // Other parameters
    }
  }
  ```

  **Terraform**

  ```hcl theme={null}
  resource "nebius_storage_v1_transfer" "infinite_transfer" {
    stop_condition {
      infinite = true
    }
    # Other parameters
  }
  ```

## Interval between iterations

For data transfers with more than one iteration, you can optionally configure an interval between iterations:

**Web console**

In the [web console](https://console.nebius.com/datatransfer), this setting appears under **Interval between iterations** when you [create](https://docs.nebius.com/object-storage/transfer/launch.md) or [modify](https://docs.nebius.com/object-storage/transfer/manage.md) a data transfer.

**CLI**

```json theme={null}
{
  "spec": {
    "inter_iteration_interval": "<HhMmSs>"
    // Other parameters
  }
}
```

**Terraform**

```hcl theme={null}
resource "nebius_storage_v1_transfer" "example_transfer" {
  inter_iteration_interval = "<HhMmSs>"
  # Other parameters
}
```

In the value, specify the number of hours, minutes and seconds for the interval. For example, `1h20m40s`.
