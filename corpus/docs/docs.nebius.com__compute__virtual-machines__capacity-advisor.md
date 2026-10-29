# Capacity advisor for GPU availability in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/capacity-advisor

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Capacity advisor for GPU availability in Nebius AI Cloud

Nebius AI Cloud's *capacity advisor* provides insights into GPU capacity availability for launching virtual machines (VMs) with specific hardware presets. It helps you understand where you can launch VMs based on your [quotas](https://docs.nebius.com/compute/resources/quotas-limits.md) and the current physical capacity in Nebius AI Cloud [regions](https://docs.nebius.com/overview/regions.md).

## Scope

The capacity advisor provides data for the following virtual machines with GPUs:

* **By service**:

  * VMs that you create directly in Compute
  * [Managed Soperator](https://docs.nebius.com/slurm-soperator/index.md) nodes
  * [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/index.md) nodes
  * VMs launched by [Serverless AI](https://docs.nebius.com/serverless/index.md) for running Devlabs, jobs and endpoints

* **By type**:

  * [Regular VMs](https://docs.nebius.com/compute/virtual-machines/manage.md)
  * [Preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md)
  * [VMs with reservations](https://docs.nebius.com/compute/virtual-machines/reservations.md)

Data about computing resource availability of VMs without GPUs isn't provided.

> [!WARNING]
>
> Data provided by the capacity advisor is accurate as of a specific timestamp included in the data and doesn't guarantee availability of GPU resources at creation time.

## Prerequisites

**Web console**

Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant
; for example, the default `viewers` group.
You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant
   ; for example, the default `viewers` group.
   You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant
   ; for example, the default `viewers` group.
   You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant
   ; for example, the default `viewers` group.
   You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant
   ; for example, the default `viewers` group.
   You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

Nebius AI Cloud provider for Terraform doesn't support the capacity advisor.

## How to get data from the capacity advisor

> [!NOTE]
>
> For preemptible VMs, the capacity advisor estimates availability by using the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md), as if the **Follow spot price** option were selected. If you use a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) with a max price lower than the current spot price, the actual number of VMs you can start may be lower than shown, including zero.

**Web console**

In the sidebar, go to  **Administration** → **Capacity dashboard**.

For each VM platform, preset, region, InfiniBand™ fabric and VM type (regular, preemptible or with reservations), the capacity advisor shows:

* How many VMs you can launch, based on your quotas and the current physical capacity (for regular and [preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md) VMs) or on your active [capacity reservations](https://docs.nebius.com/compute/virtual-machines/reservations.md) (for VMs with reservations).
* How likely you are to be able to launch the displayed number of regular or preemptible VMs.

  > For example, if your quota for a certain kind of VMs is 10 VMs, you have a high chance of launching them all when the overall capacity is in the hundreds, but a low chance when the capacity is less than 10 VMs.

  As reservations guarantee you a certain number of GPUs that aren't subject to quotas, the chance of launch isn't displayed for VMs with reservations.

**CLI**

1. Get the tenant ID.

   To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

2. Run `nebius capacity resource-advice list` to get the capacity advisor data:

   ```bash theme={null}
   nebius capacity resource-advice list --parent-id <tenant_ID>
   ```

In the output, each list item contains data for a single combination of VM platform, preset, region, InfiniBand™ fabric and VM type:

```yaml highlight={3-8,15-16,19-22,25-28} theme={null}
items:
  - spec:
      region: eu-north1
      fabric: fabric-2
      compute_instance:
        platform: gpu-h100-sxm
        preset:
          name: 1gpu-16vcpu-200gb
          resources:
            vcpu_count: 16
            memory_gibibytes: 200
            gpu_count: 1
        gpu_memory_gigabytes: 80
    status:
      reserved:
        availability_level: AVAILABILITY_LEVEL_LIMIT_REACHED
        data_state: DATA_STATE_FRESH
        effective_at: "2026-03-27T11:25:55.695087Z"
      on_demand:
        available: 24
        limit: 32
        availability_level: AVAILABILITY_LEVEL_HIGH
        data_state: DATA_STATE_FRESH
        effective_at: "2026-03-27T11:08:07.360Z"
      preemptible:
        available: 22
        limit: 128
        availability_level: AVAILABILITY_LEVEL_MEDIUM
        data_state: DATA_STATE_FRESH
        effective_at: "2026-03-27T11:08:07.360Z"
  ...
```

In the `.items[*].status` fields, `on_demand`, `preemptible` and `reserved` contain data about regular VMs, preemptible VMs and VMs with reservations, respectively. Each of these fields contains the following data:

* `available`: Maximum number of VMs that you can launch, based on your quotas and the current physical capacity.

* `limit`: Your current quota.

* `availability_level`: Level of resource availability. Possible values:

  * `AVAILABILITY_LEVEL_LOW`: **Low chance of launch** — Available capacity is significantly lower than your quota. Creating resources might not be possible.
  * `AVAILABILITY_LEVEL_MEDIUM`: **Medium chance of launch** — Available capacity is lower than your quota. Creating resources is possible, but may fail.
  * `AVAILABILITY_LEVEL_HIGH`: **High chance of launch** — Available capacity is enough to fully satisfy your quota.
  * `AVAILABILITY_LEVEL_LIMIT_REACHED`: **Launch impossible** — No available capacity.

* `data_state`: State of the data. Possible values:

  * `DATA_STATE_FRESH`: Data is up to date (fetched recently).
  * `DATA_STATE_STALE`: Data is stale (fetched a long time ago).
  * `DATA_STATE_UNKNOWN`: Capacity advisor failed to fetch data.

* `effective_at`: Timestamp of the last update.

**Go SDK**

1. Get the tenant ID.

   To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

2. List the capacity advisor data:

   ```go theme={null}
   advice, err := sdk.Services().Capacity().V1().
       ResourceAdvice().List(
           ctx,
           &capacity.ListResourceAdviceRequest{
               ParentId: "<tenant_ID>",
           },
       )
   if err != nil {
       return err
   }
   fmt.Println(advice)
   ```

   In the code, set `ParentId` to the tenant ID.

The response contains `Items`, where each item has a `Spec` and a `Status`. `Spec` includes `Region`, `Fabric` and `ComputeInstance` (with `Platform`, `Preset.Name` and `GpuMemoryGigabytes`). `Status` contains `OnDemand`, `Preemptible` and `Reserved`, each with:

* `Available`: Maximum number of VMs you can launch.
* `Limit`: Your current quota.
* `AvailabilityLevel`: Level of resource availability.
* `DataState`: State of the data.
* `EffectiveAt`: Timestamp of the last update.

**Python SDK**

1. Get the tenant ID.

   To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

2. List the capacity advisor data:

   ```python theme={null}
   resource_advice_service = ResourceAdviceServiceClient(sdk)
   advice = await resource_advice_service.list(
       ListResourceAdviceRequest(parent_id="<tenant_ID>"),
   )
   print(advice)
   ```

   In the code, set `parent_id` to the tenant ID.

The response contains `items`, where each item has a `spec` and a `status`. `spec` includes `region`, `fabric` and `compute_instance` (with `platform`, `preset.name` and `gpu_memory_gigabytes`). `status` contains `on_demand`, `preemptible` and `reserved`, each with:

* `available`: Maximum number of VMs you can launch.
* `limit`: Your current quota.
* `availability_level`: Level of resource availability.
* `data_state`: State of the data.
* `effective_at`: Timestamp of the last update.

**JavaScript SDK**

1. Get the tenant ID.

   To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

2. List the capacity advisor data:

   ```ts theme={null}
   const resourceAdviceService =
     new ResourceAdviceService(sdk);
   const advice = await resourceAdviceService.list(
     ListResourceAdviceRequest.create({
       parentId: "<tenant_ID>",
     }),
   );
   console.log(advice);
   ```

   In the code, set `parentId` to the tenant ID.

The response contains `items`, where each item has a `spec` and a `status`. `spec` includes `region`, `fabric` and `computeInstance` (with `platform`, `preset.name` and `gpuMemoryGigabytes`). `status` contains `onDemand`, `preemptible` and `reserved`, each with:

* `available`: Maximum number of VMs you can launch.
* `limit`: Your current quota.
* `availabilityLevel`: Level of resource availability.
* `dataState`: State of the data.
* `effectiveAt`: Timestamp of the last update.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
