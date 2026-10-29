# Capacity reservations for Compute virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/reservations

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Capacity reservations for Compute virtual machines

To make sure that GPU capacity is always available for your virtual machines (VMs), you can reserve GPUs. A *reservation* represents a [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md), and it reserves a specific number of GPUs that are allocated to your infrastructure. GPUs from a reservation remain available, even if a VM is stopped. Without reservations, GPU capacity is taken from a shared pool and returned when a VM is stopped (for example, by you or a [maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md)).

To start using reservations, send a request to your Nebius manager. In this request, specify how many GPUs you would like to reserve and for what period. If you are not in contact with a Nebius manager, you can ask [technical support](https://console.nebius.com/support/create-ticket) to connect you with one.

After reservations are ready, you can add them to your VMs when you create or update these VMs. You can also check your capacity block groups on the **Limits** page and get detailed information about them. For more information, see [List of capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md#list-of-capacity-block-groups).

> [!NOTE]
>
> GPUs allocated from reservations do not count towards [quotas on the number of GPUs](https://docs.nebius.com/compute/resources/quotas-limits.md#gpu-virtual-machines).

## How to add reservations to VMs

VMs of a regular type and with GPUs support reservations. [Preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) and VMs without GPUs do not support them.

**Web console**

If you want to [create a VM](https://docs.nebius.com/compute/virtual-machines/create.md#create-a-vm) and you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), on the **General** step, select **Reserved VM**. On the **Compute** step, select a platform and configure the **Reservation** settings. If you do not have capacity block groups, the wizard skips the **General** step and opens **Compute** instead.

If you want to modify an existing VM, [stop it](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) first and then go to its **Settings** tab on the VM page. Next, update the reservation settings.

The **Reservation** section is only displayed if you have capacity block groups.

In the **Reservation** section, you can configure the following options:

* **Any (existing and future)** (default): Compute selects among your matching capacity block groups automatically.
* **Specific capacity block groups**: Select one or more capacity block groups. Each option shows the capacity block group ID, reservation period and GPU usage. Make sure the selected groups have enough capacity and do not expire soon.
* **Switch to PAYG**: Choose whether the VM can start after you create or restart it without active intervals in selected capacity block groups:

  * **When reservation is exhausted** (default): The VM can start as a pay-as-you-go VM when no capacity is available in the selected capacity block groups.
  * **Never**: The VM cannot start without available capacity in the selected capacity block groups.

  This does not affect the VM when it is running. If an interval in a selected capacity block group expires while the VM is running, the VM always continues as a pay-as-you-go VM, regardless of this setting.

If you have capacity block groups in multiple regions, select a **Region** first.

**CLI**

Use the `--reservation-policy-*` parameters when creating or updating a VM:

* To create a VM, use the following command:

  ```bash theme={null}
  nebius compute instance create \
    ... \
    --reservation-policy-policy <auto|forbid|strict> \
    --reservation-policy-reservation-ids <reservations>
  ```

* To update a VM, [stop it](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually) first and then use the following command:

  ```bash theme={null}
  nebius compute instance update \
    ... \
    --reservation-policy-policy <auto|forbid|strict> \
    --reservation-policy-reservation-ids <reservations>
  ```

Description of the parameters:

* `--reservation-policy-policy`: Policy for reservation usage. Supports the following values:

  * `auto`: VM resources are allocated from reservations. If no reservations are currently available, the VM runs without them. In this case, resources for the VM are provided from the common pool.

    > [!NOTE]
    >
    > The `auto` value is the default. If you don't have any reservations and you don't set the `--reservation-policy-policy` parameter, the `auto` value applies and the VM runs without reservations.
  * `forbid`: VM resources are provided from the common pool, and no reservations are used.
  * `strict`: VM resources are exclusively allocated from reservations. The VM doesn't run without the reservations.

* `--reservation-policy-reservation-ids` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation-ids` | **Behavior** |
| - | - | - |
| `auto` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `auto` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `forbid` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `forbid` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `strict` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `strict` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**Terraform**

Use the `reservation_policy` parameter in the VM configuration:

```hcl theme={null}
resource "nebius_compute_v1_instance" "my_vm" {
  ...
  reservation_policy = {
    policy          = "<AUTO|FORBID|STRICT>"
    reservation_ids = "<reservations>"
  }
  ...
}
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the following values:

  * `AUTO`: VM resources are allocated from reservations. If no reservations are currently available, the VM runs without them. In this case, resources for the VM are provided from the common pool.

    > [!NOTE]
    >
    > The `AUTO` value is the default. If you don't have any reservations and you don't set the `policy` parameter, the `AUTO` value applies and the VM runs without reservations.
  * `FORBID`: VM resources are provided from the common pool, and no reservations are used.
  * `STRICT`: VM resources are exclusively allocated from reservations. The VM doesn't run without the reservations.

* `reservation_ids`: IDs of specific reservations (capacity block groups). You can use this parameter with the `AUTO` and `STRICT` reservation usages:

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation_ids` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**Go SDK**

Use `ReservationPolicy` in `InstanceSpec` when creating or updating a VM:

```go theme={null}
reservationPolicy := &compute.ReservationPolicy{
    Policy: compute.ReservationPolicy_STRICT,
    ReservationIds: []string{
        "<reservation_ID>",
    },
}
```

Description of the parameters:

* `Policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `ReservationIds` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `Policy` | `ReservationIds` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**Python SDK**

Use `reservation_policy` in `InstanceSpec` when creating or updating a VM:

```python theme={null}
reservation_policy = ReservationPolicy(
    policy=ReservationPolicy.Policy.STRICT,
    reservation_ids=["<reservation_ID>"],
)
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `reservation_ids` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservation_ids` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

**JavaScript SDK**

Use `reservationPolicy` in `InstanceSpec` when creating or updating a VM:

```ts theme={null}
const reservationPolicy = ReservationPolicy.create({
  policy: ReservationPolicy_Policy.STRICT,
  reservationIds: ["<reservation_ID>"],
});
```

Description of the parameters:

* `policy`: Policy for reservation usage. Supports the `AUTO`, `FORBID` and `STRICT` values.
* `reservationIds` (optional): IDs of specific reservations (capacity block groups). Use this parameter only if you need specific reservations.

  Specify the IDs in the order in which reservations should apply. For instance, resources should be allocated from the first specified reservation. When it is exhausted or expired, the service uses resources from the second specified reservation, and so on.

  Make sure to select reservations that have enough capacity and that do not expire in several days.

To find out how different combinations of parameter values impact the result, see the table below:

| `policy` | `reservationIds` | **Behavior** |
| - | - | - |
| `AUTO` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, VM resources are provided from the common pool, not from a reservation. |
| `AUTO` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit (for example, they are not currently active or there are not enough GPUs), VM resources are provided from the common pool. |
| `FORBID` | Not specified | VM resources are provided from the common pool. No reservations are used. |
| `FORBID` | Specified | Not supported. If you apply this combination, it will result in a validation error. |
| `STRICT` | Not specified | Compute tries to launch a VM in any available and suitable reservation. If none is found, a request for creating or updating a VM fails. |
| `STRICT` | Specified | Compute tries to launch a VM in one of the specified reservations. If none of them fit, a request for creating or updating a VM fails. |

## How to find information about reservations for an already configured VM

You can check the list of VMs and an overview of a given VM to find information about the VM reservations.

### List of VMs

The [list of VMs](https://console.nebius.com/compute) provides the following:

* The **Platform and VM type** column shows what configuration you have set up for a given VM.
* The **Current reservations** column shows what reservations are currently used.

Data in these columns does not always match:

* If a VM is preemptible or stopped, **Current reservations** do not show any data (**N/A** is displayed).
* If capacity in reservations is exhausted, **Current reservations** show that there are no reservations currently consumed.

### VM overview

On the VM page, on the **VM overview** tab, in the **Resource capacity** block, you can find more detailed information:

* The **VM type**, **Reservation usage** and **If no capacity** fields show the configuration that you have set up.
* The **Current reservations** and **Next interval** fields show the current consumption of reservations.

  If the VM runs without reservations, no data about them is displayed.

## Billing for reservations

Reservations and [billing models](https://docs.nebius.com/signup-billing/billing-models/overview.md) do not match directly. If your VMs run without reservations, this does not mean that the pay-as-you-go (PAYG) pricing applies by default for these VMs. It depends on whether you have an addendum for the commitment discounts.

When a Nebius manager creates reservations for you, they also prepare an addendum for the commitment discounts. After the addendum comes into force, you are charged for VMs based on this billing model. If your VM runs without reservations, the service still charges you based on the commitment discounts because of the addendum.

If you do not have the addendum, your VMs are based on PAYG.

## See also

* [Capacity block groups in Nebius AI Cloud](https://docs.nebius.com/overview/limits/capacity-block-groups.md)
* [Capacity reservations for Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md)
