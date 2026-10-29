# Preemptible virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/preemptible

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Preemptible virtual machines

*Preemptible VMs*, also known as spot VMs or spot instances, are virtual machines that Compute may stop at any time. This can happen, for example, when the system needs resources to launch a regular VM in the same region, or if the current spot price exceeds the maximum price set in the pricing policy associated with the preemptible VM.

Compute sends a `SIGTERM` signal 60 seconds before stopping the VM. If your system does not respond in time, Compute sends a `SIGKILL` signal to force shutdown.

Compute preserves all data on the volumes attached to a stopped preemptible VM. It does not preserve dynamic resources, such as dynamic public IP addresses.

Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they don't provide guaranteed availability. Preemptible VMs are charged at the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). To manage the cost of preemptible VMs, you can:

* [Check current spot prices and their history](https://docs.nebius.com/signup-billing/spot-prices.md).
* Set the maximum spot price at which your VMs can start and keep running by using a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md).
* Run your VMs at the current spot price without a maximum by choosing **Follow spot price**.

You can't convert an existing VM from regular to preemptible or the other way around. To get a preemptible VM, create a new one.

## Supported platforms

You can run preemptible VMs on all [VM platforms with GPUs](https://docs.nebius.com/compute/virtual-machines/types.md).

To get an up-to-date list of platforms, run the `nebius compute platform list` [command](https://docs.nebius.com/cli/reference/compute/platform/list.md). The platforms available for preemptible VMs are marked as `allowed_for_preemptibles: true`.

## Prerequisites

If you use the web console, you don't need to complete any prerequisites.

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Terraform**

[Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to create a preemptible VM

When you create a preemptible VM, configure one of the [spot pricing](https://docs.nebius.com/signup-billing/pricing-policy.md) settings. You can select a pricing policy to set the maximum price, or follow the spot price to have the VM run at the current spot price.

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. Click **Create resource** → **Virtual machine**.
3. If you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), on the **General** step, select **Pay-as-you-go VM**. If you do not have capacity block groups, the wizard skips the **General** step and opens **Compute** instead.
4. On the **Compute** step, select **With GPUs** or **Without GPUs**, set the VM type to **Preemptible** and select a [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).
5. In **Max price**, select or create a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md), or choose **Follow spot price**.

   For more information about the full wizard, see [How to create a virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

**CLI**

When [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md):

* Select a [platform that supports preemptible VMs](#supported-platforms).

* Add one of the following [spot pricing](https://docs.nebius.com/signup-billing/pricing-policy.md) parameters. The example command below uses `--follows-spot-price`:

  * `--spot-pricing-policy-id <pricing_policy_ID>`: Select a pricing policy that sets the maximum spot price. For information on how to get a pricing policy ID or create a new policy, see [Managing pricing policies](https://docs.nebius.com/signup-billing/manage-pricing-policy.md).
  * `--follows-spot-price`: Accept the current spot price without setting a maximum spot price.

* Add the following parameters to the `nebius compute instance create` command:

  ```bash theme={null}
  nebius compute instance create \
    ... \
    --recovery-policy fail \
    --preemptible-on-preemption stop \
    --follows-spot-price
  ```

  In this configuration, the following values are specified:

  * `recovery_policy` defines what Compute does with a VM after it's preempted or fails. Preemptible VMs support only the `FAIL` value, which stops the VM. They do not support the `RECOVER` value, which tries to restart the VM. Setting `RECOVER` for a preemptible VM results in an error.
  * `on_preemption` specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.

For details about the `nebius compute instance create` command, see the [Nebius AI Cloud CLI reference](https://docs.nebius.com/cli/reference/compute/instance/create.md).

**Terraform**

When creating a VM, select a [platform that supports preemptible VMs](#supported-platforms) and set the following parameters in the VM configuration:

```hcl theme={null}
resource "nebius_compute_v1_instance" "instance" {
  ...
  recovery_policy = "FAIL"
  preemptible     = {
    on_preemption = "STOP"
  }
  follows_spot_price = {}
  ...
}
```

In this configuration, the following values are specified:

* `recovery_policy` defines what Compute does with a VM after it's preempted or fails. Preemptible VMs support only the `FAIL` value, which stops the VM. They do not support the `RECOVER` value, which tries to restart the VM. Setting `RECOVER` for a preemptible VM results in an error.
* `on_preemption` specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.

- `follows_spot_price` accepts the current spot price without setting a maximum price. To set a maximum price, use `spot_pricing_policy = { id = "<pricing_policy_ID>" }` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

For details about the `nebius_compute_v1_instance` Terraform resource, see the [provider reference](https://docs.nebius.com/terraform-provider/reference/resources/compute_v1_instance.md).

**Go SDK**

When [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md):

* Select a [platform that supports preemptible VMs](#supported-platforms).
* Set the preemptible VM parameters in the code:

  ```go theme={null}
  resources := &compute.ResourcesSpec{
      Platform: "gpu-l40s-a",
      Size: &compute.ResourcesSpec_Preset{
          Preset: "1gpu-24vcpu-96gb",
      },
  }
  bootDisk := &compute.AttachedDiskSpec{
      AttachMode: compute.AttachedDiskSpec_READ_WRITE,
      Type: &compute.AttachedDiskSpec_ExistingDisk{
          ExistingDisk: &compute.ExistingDisk{
              Id: bootDiskID,
          },
      },
  }
  networkInterface := &compute.NetworkInterfaceSpec{
      Name:            "eth0",
      SubnetId:        subnetID,
      IpAddress:       &compute.IPAddress{},
      PublicIpAddress: &compute.PublicIPAddress{},
  }
  instanceSpec := &compute.InstanceSpec{
      Resources:         resources,
      BootDisk:          bootDisk,
      NetworkInterfaces: []*compute.NetworkInterfaceSpec{
          networkInterface,
      },
      RecoveryPolicy: compute.InstanceRecoveryPolicy_FAIL,
      Preemptible: &compute.PreemptibleSpec{
          OnPreemption: compute.PreemptibleSpec_STOP,
      },
      PricingModel: &compute.InstanceSpec_FollowsSpotPrice{
          FollowsSpotPrice: &compute.FollowsSpotPriceSpec{},
      },
  }
  preemptibleOperation, err := sdk.Services().Compute().V1().
      Instance().Create(
          ctx,
          &compute.CreateInstanceRequest{
              Metadata: &common.ResourceMetadata{
                  Name: "preemptible-instance",
              },
              Spec: instanceSpec,
          },
      )
  if err != nil {
      return err
  }
  if _, err = preemptibleOperation.Wait(ctx); err != nil {
      return err
  }
  ```

  In this configuration, the following values are specified:

  * `RecoveryPolicy` defines what Compute does with a VM after it's preempted or fails. Preemptible VMs support only the `FAIL` value, which stops the VM. They do not support the `RECOVER` value, which tries to restart the VM. Setting `RECOVER` for a preemptible VM results in an error.
  * `OnPreemption` specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.
  * `FollowsSpotPrice` accepts the current spot price without setting a maximum price. To set a maximum price, use `SpotPricingPolicy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

**Python SDK**

When [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md):

* Select a [platform that supports preemptible VMs](#supported-platforms).
* Set the preemptible VM parameters in the code:

  ```python theme={null}
  instance_service = InstanceServiceClient(sdk)
  preemptible_operation = await instance_service.create(
      CreateInstanceRequest(
          metadata=ResourceMetadata(
              name="preemptible-instance",
          ),
          spec=InstanceSpec(
              resources=ResourcesSpec(
                  platform="gpu-l40s-a",
                  preset="1gpu-24vcpu-96gb",
              ),
              boot_disk=AttachedDiskSpec(
                  attach_mode=(
                      AttachedDiskSpec.AttachMode.READ_WRITE
                  ),
                  existing_disk=ExistingDisk(id=boot_disk_id),
              ),
              network_interfaces=[
                  NetworkInterfaceSpec(
                      name="eth0",
                      subnet_id=subnet_id,
                      ip_address=IPAddress(),
                      public_ip_address=PublicIPAddress(),
                  ),
              ],
              recovery_policy=InstanceRecoveryPolicy.FAIL,
              preemptible=PreemptibleSpec(
                  on_preemption=(
                      PreemptibleSpec.PreemptionPolicy.STOP
                  ),
              ),
              follows_spot_price=FollowsSpotPriceSpec(),
          ),
      ),
  )
  await preemptible_operation.wait()
  ```

  In this configuration, the following values are specified:

  * `recovery_policy` defines what Compute does with a VM after it's preempted or fails. Preemptible VMs support only the `FAIL` value, which stops the VM. They do not support the `RECOVER` value, which tries to restart the VM. Setting `RECOVER` for a preemptible VM results in an error.
  * `on_preemption` specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.

  - `follows_spot_price` accepts the current spot price without setting a maximum price. To set a maximum price, use `spot_pricing_policy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

**JavaScript SDK**

When [creating a VM](https://docs.nebius.com/compute/virtual-machines/manage.md):

* Select a [platform that supports preemptible VMs](#supported-platforms).
* Set the preemptible VM parameters in the code:

  ```ts theme={null}
  const instanceService = new InstanceService(sdk);
  const preemptibleOperation = await instanceService.create(
    CreateInstanceRequest.create({
      metadata: ResourceMetadata.create({
        name: "preemptible-instance",
      }),
      spec: InstanceSpec.create({
        resources: ResourcesSpec.create({
          platform: "gpu-l40s-a",
          size: {
            $case: "preset",
            preset: "1gpu-24vcpu-96gb",
          },
        }),
        bootDisk: AttachedDiskSpec.create({
          attachMode:
            AttachedDiskSpec_AttachMode.READ_WRITE,
          type: {
            $case: "existingDisk",
            existingDisk: ExistingDisk.create({
              id: bootDiskId,
            }),
          },
        }),
        networkInterfaces: [
          NetworkInterfaceSpec.create({
            name: "eth0",
            subnetId,
            ipAddress: IPAddress.create({}),
            publicIpAddress: PublicIPAddress.create({}),
          }),
        ],
        recoveryPolicy: InstanceRecoveryPolicy.FAIL,
        preemptible: PreemptibleSpec.create({
          onPreemption:
            PreemptibleSpec_PreemptionPolicy.STOP,
        }),
        pricingModel: {
          $case: "followsSpotPrice",
          followsSpotPrice: FollowsSpotPriceSpec.create({}),
        },
      }),
    }),
  ).result;
  await preemptibleOperation.wait();
  ```

  In this configuration, the following values are specified:

  * `recoveryPolicy` defines what Compute does with a VM after it's preempted or fails. Preemptible VMs support only the `FAIL` value, which stops the VM. They do not support the `RECOVER` value, which tries to restart the VM. Setting `RECOVER` for a preemptible VM results in an error.
  * `onPreemption` specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.
  * `followsSpotPrice` accepts the current spot price without setting a maximum price. To set a maximum price, use `spotPricingPolicy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

> [!TIP]
>
> A dynamic IP address is released when a preemptible VM stops. To keep your workload stable, consider using a static IP address instead.

## How to continue working with a stopped preemptible VM

When Compute stops a preemptible VM, it preserves all data on the attached volumes. To resume work, [start the VM](https://docs.nebius.com/compute/virtual-machines/stop-start.md) again. If you used a dynamic IP address, update all systems that depended on the old IP address.

If the VM uses local SSD disks, use them with caution. Local SSD disks are ephemeral, meaning any data stored on them will be lost when the preemptible VM stops.

You can also [create a regular VM](https://docs.nebius.com/compute/virtual-machines/manage.md) with the same attached volumes.
