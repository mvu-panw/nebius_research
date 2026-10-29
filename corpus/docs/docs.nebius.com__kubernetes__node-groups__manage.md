# Creating and modifying Managed Service for Kubernetes® node groups

Source: https://docs.nebius.com/kubernetes/node-groups/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Creating and modifying Managed Service for Kubernetes® node groups

Clusters in Managed Service for Kubernetes use Compute virtual machines as nodes to run applications. In this guide, you will learn how to create node groups, add them to clusters, modify and delete them.

In the web console, you can create node groups together with a new cluster during [cluster creation](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters).

To learn how to manage clusters outside of their node groups, see [How to create and modify Managed Service for Kubernetes® clusters](https://docs.nebius.com/kubernetes/clusters/manage.md).

## Prerequisites

> [!TIP]
>
> You do not need to complete any prerequisites if you create or modify node groups in the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. [Create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and save its ID to an environment variable:

   ```bash theme={null}
   export K8S_CLUSTER_ID=$(nebius mk8s cluster get-by-name \
     --name <cluster_name> --format jsonpath='{.metadata.id}')
   ```

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

2. [Create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters).

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. [Create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and save its ID to the `k8sClusterID` variable:

   ```go theme={null}
   clusterByName, err := sdk.Services().MK8S().V1().
       Cluster().GetByName(
           ctx,
           &common.GetByNameRequest{
               Name: "<cluster_name>",
           },
       )
   if err != nil {
       return err
   }
   k8sClusterID := clusterByName.GetMetadata().GetId()
   if k8sClusterID == "" {
       return fmt.Errorf("cluster ID is missing")
   }
   fmt.Println(k8sClusterID)
   ```

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. [Create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and save its ID to the `k8s_cluster_id` variable:

   ```python theme={null}
   lookup_cluster_service = ClusterServiceClient(sdk)
   cluster_by_name = await lookup_cluster_service.get_by_name(
       GetByNameRequest(name="<cluster_name>"),
   )
   if cluster_by_name.metadata is None:
       raise ValueError("cluster metadata is missing")
   k8s_cluster_id = cluster_by_name.metadata.id
   if not k8s_cluster_id:
       raise ValueError("cluster ID is missing")
   print(k8s_cluster_id)
   ```

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. [Create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and save its ID to the `k8sClusterId` variable:

   ```ts theme={null}
   const lookupClusterService = new ClusterService(sdk);
   const clusterByName = await lookupClusterService.getByName(
     GetByNameRequest.create({
       name: "<cluster_name>",
     }),
   );
   const k8sClusterId = clusterByName.metadata?.id;
   if (!k8sClusterId) {
     throw new Error("cluster ID is missing");
   }
   console.log(k8sClusterId);
   ```

## How to create node groups

Node groups define the characteristics of the virtual machines (VMs) that run your workloads. Each node group includes identical nodes created with the same template.

You can create different types of node groups depending on your performance, cost and availability requirements. For example, you can choose high-performance GPUs for compute-intensive workloads or preemptible VMs with [spot pricing](https://docs.nebius.com/signup-billing/pricing-policy.md) for interruptible tasks.

### Regular node groups

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.

2. Open the page of the cluster where you want to create a node group.

3. Switch to the **Node groups** tab.

4. Click  **Create node group**.

5. On the page that opens, specify a name for the node group (for example, `mk8s-node-group-test`).

6. (Optional) Enable the **Assign public IPv4 addresses** option if you want the nodes to be accessible from the internet.

7. Under **Size**, specify the initial **Number of nodes**. If you want to let the node group scale up or down depending on the workload, enable autoscaling. After that, specify the minimum and maximum number of nodes that the group can have.

8. Configure the **Computing resources** section:

   1. Select whether the node group should have GPUs.

   2. Select a regular VM type.

      VMs without GPUs only support the regular type.

      For information about creating preemptible node groups, see [instructions below](#preemptible-node-groups).

   3. (Optional) For a regular VM with GPUs, select **Reservation usage**. Specify whether Managed Kubernetes should allocate resources for the node group from [reservations](https://docs.nebius.com/kubernetes/node-groups/reservations.md).

      The **Reservation usage** field is only displayed if you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md).

      > **More information about reservation usage**
      >
      > * **With reservations**: The resources are allocated from reservations ([capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md)). For example, if a Nebius manager has created a capacity block group for you, Managed Kubernetes allocates GPUs for the node group from this capacity block group. This ensures that resources are always available, even if VMs in the node group are stopped (for example, by you or a [maintenance event](https://docs.nebius.com/kubernetes/maintenance/index.md)).
      >
      >   In the **Reservation** section, you can configure the following options:
      >
      >   * **Any (existing and future)** (default): Compute selects among your matching capacity block groups automatically.
      >   * **Specific capacity block groups**: Select one or more capacity block groups. Each option shows the capacity block group ID, reservation period and GPU usage. Make sure the selected groups have enough capacity and do not expire soon.
      >   * **Switch to PAYG**: Choose whether the VM can start after you create or restart it without active intervals in selected capacity block groups:
      >
      >     * **When reservation is exhausted** (default): The VM can start as a pay-as-you-go VM when no capacity is available in the selected capacity block groups.
      >     * **Never**: The VM cannot start without available capacity in the selected capacity block groups.
      >
      >     This does not affect the VM when it is running. If an interval in a selected capacity block group expires while the VM is running, the VM always continues as a pay-as-you-go VM, regardless of this setting.
      >
      >   If you have capacity block groups in multiple regions, select a **Region** first.
      >
      > * **Without reservations**: The resources are allocated from a common pool, and no reservations are used for the node group.

   4. Select an available [platform and a preset](https://docs.nebius.com/compute/virtual-machines/types.md) (a combination of GPUs, vCPUs and RAM) that fits your workload requirements.

   5. (Optional) If you create a node group with 8 GPUs (for example, for training models), use a GPU cluster for the node group. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single node group without InfiniBand cannot perform these tasks as quickly.

      To use a GPU cluster, select an existing one or create a new cluster:

      1. Click  **Create** in the **GPU cluster** field.
      2. In the window that opens, specify the cluster name and InfiniBand fabric. To select the fabric, see [InfiniBand fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).
      3. Click **Create**.

      > [!WARNING]
      >
      > If a node group uses a GPU cluster, the GPU cluster must be located in the same project as the node group's parent cluster.

   6. (Optional) Enable or disable **GPU settings**. They are enabled by default, and they allow Managed Kubernetes to pre-install NVIDIA drivers and the [Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html). You can also select a specific NVIDIA CUDA driver version.

      Disable **GPU settings** only if you need to [install specific driver versions manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups) or use a custom operator. Disabling is not recommended.

   7. Select an operating system for the nodes (for example, `Ubuntu 24.04 LTS`).

9. Under **Node storage**, select the disk type and specify the size in GiB. Supported [disk types](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks) are the following:

   * **SSD**: Standard solid-state drive for general-purpose workloads.
   * **SSD NRD**: Network-replicated SSD providing higher reliability through data duplication across the network.
   * **SSD IO**: High-performance SSD optimized for I/O-intensive operations with lower latency.

10. (Optional) If the selected platform and preset support local SSD disks, enable **Local SSD disks** to add ephemeral local storage to your node group.

    > [!NOTE]
    >
    > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

11. (Optional) If you want to attach a filesystem to your node group, in the **Shared filesystems** section, specify the settings of this filesystem:

    1. Click  **Attach shared filesystem**.

    2. In the window that opens, select an existing filesystem or create a new one.

    3. If you create a new filesystem, specify its name, size and the block size.

    4. Click **Attach filesystem** or **Create and attach filesystem**.

    5. After the window is closed, specify a mount tag for mounting the filesystem to the VM.

       Create your own tag, such as `my-filesystem`. Make sure that it is unique within the VM.

    6. To mount the filesystem to the node group automatically, keep the **Auto mount** option enabled.

12. (Optional) In the **Username and SSH key** field, add credentials, so you can [connect to the node group](https://docs.nebius.com/compute/virtual-machines/connect.md):

    1. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

    2. In the **Username and SSH key** field, click .

    3. If you added an SSH key earlier and you want to reuse it, select the key from the drop-down list.

       If you want to add a new key, click  **Add credentials**.

    4. In the window that opens, specify the username of the node group user, a public key of your SSH key pair and the credentials name to recognize the key in the list.

    5. Click **Add credentials**.

13. (Optional) Under **Additional**, select or create a [service account](https://docs.nebius.com/iam/overview.md) that will perform actions on behalf of the nodes.

14. Click **Create node group**.

**CLI**

Create a node group:

```bash theme={null}
nebius mk8s node-group create \
  --parent-id $K8S_CLUSTER_ID \
  --name <node_group_name> \
  --fixed-node-count <number_of_nodes> \
  --template-resources-platform <platform_ID> \
  --template-resources-preset <preset_name> \
  --template-gpu-settings-drivers-preset <driver_preset>
```

> [!NOTE]
>
> If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), don't add the `--template-gpu-settings-drivers-preset` parameter to the command. Instead, [manually install the GPU operator](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups).

**Terraform**

1. Create a node group configuration file:

   ```hcl theme={null}
   resource "nebius_mk8s_v1_node_group" "<node_group_name>" {
     name = "<node_group_name>"
     parent_id = "<cluster_ID>"
     fixed_node_count = <number_of_nodes>

     template = {
       resources = {
         platform = "<platform_ID>"
         preset = "<preset_name>"
       }

       gpu_settings = {
         drivers_preset = "<driver_preset>"
       }
     }
   }
   ```

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a node group:

```go theme={null}
regularName := (
    "<node_group_name>"
)
regularNodeCount := (
    <number_of_nodes>
)
regularPlatform := (
    "<platform_ID>"
)
regularPreset := (
    "<preset_name>"
)
regularDriverPreset := (
    "<driver_preset>"
)
regularGroupOp, err := sdk.Services().MK8S().V1().
    NodeGroup().Create(
        ctx,
        &mk8s.CreateNodeGroupRequest{
            Metadata: &common.ResourceMetadata{
                ParentId: k8sClusterID,
                Name: regularName,
            },
            Spec: &mk8s.NodeGroupSpec{
                Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                    FixedNodeCount: regularNodeCount,
                },
                Template: &mk8s.NodeTemplate{
                    Resources: &mk8s.ResourcesSpec{
                        Platform: regularPlatform,
                        Size: &mk8s.ResourcesSpec_Preset{
                            Preset: regularPreset,
                        },
                    },
                    GpuSettings: &mk8s.GpuSettings{
                        DriversPreset: regularDriverPreset,
                    },
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = regularGroupOp.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameters:

* `Metadata.Name`: Node group name.
* `Spec.Size.FixedNodeCount`: Number of nodes per group.
* `Spec.Template.Resources.Platform`: A platform with GPUs.
* `Spec.Template.Resources.Size.Preset`: A compatible preset.
* `Spec.Template.GpuSettings.DriversPreset`: GPU drivers preset.

> [!NOTE]
>
> If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit `GpuSettings`. Instead, [manually install the GPU operator](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups).

**Python SDK**

Create a node group:

```python theme={null}
regular_name = (
    "<node_group_name>"
)
regular_node_count = (
    <number_of_nodes>
)
regular_platform = (
    "<platform_ID>"
)
regular_preset = (
    "<preset_name>"
)
regular_driver_preset = (
    "<driver_preset>"
)
regular_group_service = NodeGroupServiceClient(sdk)
regular_group_operation = await regular_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id=k8s_cluster_id,
            name=regular_name,
        ),
        spec=NodeGroupSpec(
            fixed_node_count=regular_node_count,
            template=NodeTemplate(
                resources=ResourcesSpec(
                    platform=regular_platform,
                    preset=regular_preset,
                ),
                gpu_settings=GpuSettings(
                    drivers_preset=regular_driver_preset,
                ),
            ),
        ),
    ),
)
await regular_group_operation.wait()
```

The code contains the following parameters:

* `metadata.name`: Node group name.
* `spec.fixed_node_count`: Number of nodes per group.
* `spec.template.resources.platform`: A platform with GPUs.
* `spec.template.resources.preset`: A compatible preset.
* `spec.template.gpu_settings.drivers_preset`: GPU drivers preset.

> [!NOTE]
>
> If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit `gpu_settings`. Instead, [manually install the GPU operator](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups).

**JavaScript SDK**

Create a node group:

```ts theme={null}
const regularName = "<node_group_name>";
const regularNodeCount = <number_of_nodes>;
const regularPlatform = "<platform_ID>";
const regularPreset = "<preset_name>";
const regularDriverPreset =
  "<driver_preset>";
const regularGroupService = new NodeGroupService(sdk);
const regularGroupOperation = await regularGroupService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: k8sClusterId,
      name: regularName,
    }),
    spec: NodeGroupSpec.create({
      size: {
        $case: "fixedNodeCount",
        fixedNodeCount: regularNodeCount,
      },
      template: NodeTemplate.create({
        resources: ResourcesSpec.create({
          platform: regularPlatform,
          size: {
            $case: "preset",
            preset: regularPreset,
          },
        }),
        gpuSettings: GpuSettings.create({
          driversPreset: regularDriverPreset,
        }),
      }),
    }),
  }),
).result;
await regularGroupOperation.wait();
```

The code contains the following parameters:

* `metadata.name`: Node group name.
* `spec.size.fixedNodeCount`: Number of nodes per group.
* `spec.template.resources.platform`: A platform with GPUs.
* `spec.template.resources.size.preset`: A compatible preset.
* `spec.template.gpuSettings.driversPreset`: GPU drivers preset.

> [!NOTE]
>
> If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit `gpuSettings`. Instead, [manually install the GPU operator](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups).

For descriptions of node group parameters, see [Node group parameters](#node-group-parameters).

For more details about GPUs in node groups, see [Working with GPUs in the Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/gpu/set-up.md) and [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™](https://docs.nebius.com/kubernetes/gpu/clusters.md). To allocate GPUs and network devices with Dynamic Resource Allocation, see [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md).

### Preemptible node groups

Preemptible nodes use virtual machines that can be stopped by Nebius AI Cloud at any time. They can help reduce computing costs for workloads with interruptions, such as batch processing or training ML models. Preemptible node groups are charged at the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). To set the maximum price, use a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md).

For more information about how preemptible VMs work, see [Preemptible virtual machines](https://docs.nebius.com/compute/virtual-machines/preemptible.md).

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.

2. [Create a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) or choose an existing one.

3. On the cluster page, switch to the **Node groups** tab.

4. Click  **Create node group**.

5. When creating a node group, under **Computing resources**, select:

   * **With GPU**
   * **Preemptible** VM type

6. In **Max price**, select or create a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md), or choose **Follow spot price**.

For information about other node group parameters, see [instructions about creating regular node groups](#regular-node-groups).

**CLI**

Run the Nebius AI Cloud CLI command [nebius mk8s node-group create](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md) with the `--template-preemptible` parameter.

Add one of the following [spot pricing](https://docs.nebius.com/signup-billing/pricing-policy.md) parameters. The example command below uses `--template-follows-spot-price`:

* `--template-spot-pricing-policy-id <pricing_policy_ID>`: Select a pricing policy that sets the maximum spot price. For information on how to get a pricing policy ID or create a new policy, see [Managing pricing policies](https://docs.nebius.com/signup-billing/manage-pricing-policy.md).
* `--template-follows-spot-price`: Accept the current spot price without setting a maximum price.

  ```bash theme={null}
  nebius mk8s node-group create \
    ... \
    --template-preemptible \
    --template-follows-spot-price
  ```

**Terraform**

Create a node group configuration file and set the `.template.preemptible` block to enable preemptibility. Set one of the spot pricing settings:

* `spot_pricing_policy`: Select a pricing policy that sets the maximum price.
* `follows_spot_price`: Accept the current spot price without setting a maximum.

```hcl theme={null}
resource "nebius_mk8s_v1_node_group" "example" {
  name     = "preemptible-ng"
  ...

  template = {
    preemptible = {}
    follows_spot_price = {}
    ...
  }
}
```

**Go SDK**

Create a node group with `Spec.Template.Preemptible` set:

```go theme={null}
preemptibleGroupOp, err := sdk.Services().MK8S().V1().
    NodeGroup().Create(
        ctx,
        &mk8s.CreateNodeGroupRequest{
            Metadata: &common.ResourceMetadata{
                ParentId: k8sClusterID,
                Name:     "node-group-1",
            },
            Spec: &mk8s.NodeGroupSpec{
                Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                    FixedNodeCount: 1,
                },
                Template: &mk8s.NodeTemplate{
                    Resources: &mk8s.ResourcesSpec{
                        Platform: "gpu-h100-sxm",
                        Size: &mk8s.ResourcesSpec_Preset{
                            Preset: "1gpu-16vcpu-200gb",
                        },
                    },
                    Preemptible: &mk8s.PreemptibleSpec{},
                    PricingModel: &mk8s.NodeTemplate_FollowsSpotPrice{
                        FollowsSpotPrice: &mk8s.FollowsSpotPriceSpec{},
                    },
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = preemptibleGroupOp.Wait(ctx); err != nil {
    return err
}
```

`FollowsSpotPrice` accepts the current spot price without setting a maximum price. To set a maximum price, use `SpotPricingPolicy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

**Python SDK**

Create a node group with `spec.template.preemptible` set:

```python theme={null}
preemptible_group_service = NodeGroupServiceClient(sdk)
preemptible_group_operation = await preemptible_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id=k8s_cluster_id,
            name="node-group-1",
        ),
        spec=NodeGroupSpec(
            fixed_node_count=1,
            template=NodeTemplate(
                resources=ResourcesSpec(
                    platform="gpu-h100-sxm",
                    preset="1gpu-16vcpu-200gb",
                ),
                preemptible=PreemptibleSpec(),
                follows_spot_price=FollowsSpotPriceSpec(),
            ),
        ),
    ),
)
await preemptible_group_operation.wait()
```

`follows_spot_price` accepts the current spot price without setting a maximum price. To set a maximum price, use `spot_pricing_policy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

**JavaScript SDK**

Create a node group with `spec.template.preemptible` set:

```ts theme={null}
const preemptibleGroupService = new NodeGroupService(sdk);
const preemptibleGroupOperation =
  await preemptibleGroupService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: k8sClusterId,
      name: "node-group-1",
    }),
    spec: NodeGroupSpec.create({
      size: {
        $case: "fixedNodeCount",
        fixedNodeCount: 1,
      },
      template: NodeTemplate.create({
        resources: ResourcesSpec.create({
          platform: "gpu-h100-sxm",
          size: {
            $case: "preset",
            preset: "1gpu-16vcpu-200gb",
          },
        }),
        preemptible: PreemptibleSpec.create({}),
        pricingModel: {
          $case: "followsSpotPrice",
          followsSpotPrice: FollowsSpotPriceSpec.create({}),
        },
      }),
    }),
  }),
).result;
await preemptibleGroupOperation.wait();
```

`followsSpotPrice` accepts the current spot price without setting a maximum price. To set a maximum price, use `spotPricingPolicy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

## How to modify node groups

Modifying the node group template triggers a [rolling update](#deployment-strategy-and-quotas). Managed Kubernetes replaces each node with another one, with a new configuration. To check the list of the template parameters, see all `--template-*` parameters in [CLI reference](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md) or the nested schema for `template` in [Terraform reference](https://docs.nebius.com/terraform-provider/reference/resources/mk8s_v1_node_group.md#nested-schema-for-template).

If you modify other parameters, Managed Kubernetes does not replace the nodes, they remain unchanged.

During a node group update, Managed Kubernetes uses the default values of the deployment strategy [parameters](#node-group-parameters). By default, one node at a time can be unavailable during the update, and no additional compute quota is required. You can change the deployment strategy when you modify a node group.

**Web console**

To modify a node group:

1. In the sidebar, go to  **Compute** → **Kubernetes**.

2. Open the page of the required cluster and then go to the **Node groups** tab.

3. Open the page of the node group that you wish to change.

4. Switch to the **Settings** tab and then modify the required parameters.

   Parameters available for editing:

   * **Name**: Name of the node group.

   * **Size**:

     * **Number of nodes**: Target and fixed number of nodes (if autoscaling is disabled). The maximum number is 100.
     * **Enable autoscaling**: Allows you to set the range of nodes within which the [cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) adds or removes nodes as needed.

   * **Computing resources**: Select whether the node group should have GPUs, and then specify the hardware configuration:

     * **VM type**:

       * **Regular**: Standard VMs for high-availability production workloads.
       * **Preemptible**: VMs for interruptible workloads that may be stopped by the platform at any time. Charges depend on the current spot price.

     * **Available platform** and **Preset**: Combination of GPUs, vCPUs and RAM that fits your workload requirements. For more information, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

     * **GPU cluster**: GPU cluster with InfiniBand. Allows you to accelerate tasks that require HPC power.

       Available only if the node group contains 8 GPUs.

     * **GPU settings**: If enabled, the system pre-installs NVIDIA drivers and the [Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html). You can also select a specific NVIDIA CUDA driver version.

       Disable **GPU settings** only if you need to [install specific driver versions manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups) or use a custom operator.

     * **Drivers**: CUDA driver version based on enabled **GPU settings**.

     * **Operating system**: OS for the nodes, for example, `Ubuntu 24.04 LTS`.

   * **Node storage**:

     * **Disk type**: [Type of the boot disk](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
     * **Size**: Size of the boot disk in GiB.

5. Click **Save changes**.

The status of the node group changes to **Updating** while the new configuration is being applied.

**CLI**

1. Get the node group ID and save it to an environment variable:

   ```bash theme={null}
   export K8S_NODE_GROUP_ID=$(nebius mk8s node-group get-by-name \
     --parent-id $K8S_CLUSTER_ID \
     --name <node_group_name> --format jsonpath='{.metadata.id}')
   ```

2. Update the node group:

   ```bash theme={null}
   nebius mk8s node-group update \
     --id $K8S_NODE_GROUP_ID \
     (parameters)
   ```

   Only the parameters specified in the CLI command can be changed. You can do a full update instead by adding `--full` to the command. This will update all parameters with the values specified in the command or the default values.

   Add `--auto-approve` to automatically approve node recreation if it is required by the update. Otherwise, the CLI waits for confirmation before proceeding.

**Terraform**

1. In the node group configuration file, update the [parameters](#node-group-parameters) of the `nebius_mk8s_v1_node_group` resource.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the node group ID and save it to the `nodeGroupID` variable:

   ```go theme={null}
   nodeGroupByName, err := sdk.Services().MK8S().V1().
       NodeGroup().GetByName(
           ctx,
           &common.GetByNameRequest{
               ParentId: k8sClusterID,
               Name:     "<node_group_name>",
           },
       )
   if err != nil {
       return err
   }
   nodeGroupID := nodeGroupByName.GetMetadata().GetId()
   if nodeGroupID == "" {
       return errors.New("node group ID is missing")
   }
   ```

2. Update the node group. In the example, the node group gets a new `Metadata.Name`:

   ```go theme={null}
   groupForRename, err := sdk.Services().MK8S().V1().
       NodeGroup().Get(
           ctx,
           &mk8s.GetNodeGroupRequest{Id: nodeGroupID},
       )
   if err != nil {
       return err
   }
   groupForRename.GetMetadata().Name = "updated-name"
   renameGroupOp, err := sdk.Services().MK8S().V1().NodeGroup().
       Update(
           ctx,
           &mk8s.UpdateNodeGroupRequest{
               Metadata: groupForRename.GetMetadata(),
               Spec:     groupForRename.GetSpec(),
           },
       )
   if err != nil {
       return err
   }
   if _, err = renameGroupOp.Wait(ctx); err != nil {
       return err
   }
   ```

**Python SDK**

1. Get the node group ID and save it to the `node_group_id` variable:

   ```python theme={null}
   node_group_lookup_service = NodeGroupServiceClient(sdk)
   node_group_by_name = await node_group_lookup_service.get_by_name(
       GetByNameRequest(
           parent_id=k8s_cluster_id,
           name="<node_group_name>",
       ),
   )
   node_group_id = node_group_by_name.metadata.id
   if not node_group_id:
       raise ValueError("node group ID is missing")
   ```

2. Update the node group. In the example, the node group gets a new `metadata.name`:

   ```python theme={null}
   rename_group_service = NodeGroupServiceClient(sdk)
   group_for_rename = await rename_group_service.get(
       GetNodeGroupRequest(id=node_group_id),
   )
   group_for_rename.metadata.name = "updated-name"
   rename_group_operation = await rename_group_service.update(
       UpdateNodeGroupRequest(
           metadata=group_for_rename.metadata,
           spec=group_for_rename.spec,
       ),
   )
   await rename_group_operation.wait()
   ```

**JavaScript SDK**

1. Get the node group ID and save it to the `nodeGroupId` variable:

   ```ts theme={null}
   const nodeGroupLookupService = new NodeGroupService(sdk);
   const nodeGroupByName = await nodeGroupLookupService.getByName(
     GetByNameRequest.create({
       parentId: k8sClusterId,
       name: "<node_group_name>",
     }),
   );
   let nodeGroupId = nodeGroupByName.metadata?.id;
   if (!nodeGroupId) {
     throw new Error("node group ID is missing");
   }
   ```

2. Update the node group. In the example, the node group gets a new `metadata.name`:

   ```ts theme={null}
   const renameGroupService = new NodeGroupService(sdk);
   const groupForRename = await renameGroupService.get(
     GetNodeGroupRequest.create({
       id: nodeGroupId,
     }),
   );
   if (!groupForRename.metadata) {
     throw new Error("node group metadata is missing");
   }
   groupForRename.metadata.name = "updated-name";
   const renameGroupOperation = await renameGroupService.update(
     UpdateNodeGroupRequest.create({
       metadata: groupForRename.metadata,
       spec: groupForRename.spec,
     }),
   ).result;
   await renameGroupOperation.wait();
   ```

For descriptions of node group parameters, see [Node group parameters](#node-group-parameters).

## Deployment strategy and quotas

Managed Kubernetes performs a *rolling update* to each node in the group when you modify the node group template. To check the list of the template parameters, see all `--template-*` parameters in [CLI reference](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md) or the nested schema for `template` in [Terraform reference](https://docs.nebius.com/terraform-provider/reference/resources/mk8s_v1_node_group.md#nested-schema-for-template).

With the default values of the deployment strategy [parameters](#node-group-parameters), Managed Kubernetes updates one node at a time in the following order:

1. Cordons the existing node (marks it as unschedulable).
2. Drains the existing node (evicts all Pods from it).
3. Deletes the existing node.
4. Creates a replacement node.

This default behavior does not require additional compute quota during an update.

Managed Kubernetes uses the node group's *deployment strategy* to determine how, in what order and to how many nodes at a time it performs the listed steps. You can configure the deployment strategy using the corresponding [parameters](#node-group-parameters).

If you prefer Managed Kubernetes to create replacement nodes before removing the existing ones, for example to minimize workload disruption, configure a deployment strategy that allows the node group to temporarily exceed its target size during an update.

In this case, make sure that your [quotas on underlying Compute resources](https://docs.nebius.com/compute/resources/quotas-limits.md) allow for the additional nodes that can be created during a rolling update. If there is no quota available for any of the required resources, the update fails. You can check your remaining quotas on the [Administration → Limits → Quotas](https://console.nebius.com/quota) page of the web console.

> For example, each node uses 8 GPUs, 128 vCPUs, 1600 GiB RAM and a public IP address. If your deployment strategy allows up to two additional nodes during the update, you need quotas for the following additional resources:
>
> * 16 GPUs (2 × 8)
> * 256 vCPUs (2 × 128)
> * 3200 GiB RAM (2 × 1600)
> * 2 public IP addresses

When you or the [autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) scales a node group up or down, Managed Kubernetes does not recreate any nodes.

## Node group parameters

**CLI**

The `nebius mk8s node-group create` and `nebius mk8s node-group update` commands support the following parameters.

* **Metadata**

  * `--name`: Node group name. Must be unique within the tenant. Cannot be changed after creation.

* **Kubernetes version on nodes**

  * `--version`: Kubernetes version in `<major>.<minor>` format. Recommended version is 1.36. For more information, see [Kubernetes versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

* **Node group size**

  * `--fixed-node-count`: Number of nodes per group. The maximum is 100.
  * `--autoscaling-min-node-count`, `--autoscaling-max-node-count`: Allow you to set the range of nodes within which the [cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) adds or removes nodes as needed.

* **Node template**

  All nodes in a group are identical and are created based on a *node template*. A node template is similar to a virtual machine specification in Compute.

  The node template has the following parameters:

  * `--template-taints`: Array of Kubernetes [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) (rules that repel Pods from nodes) for all nodes in the group.

  * `--template-resources-platform`: ID of the Compute VM platform for the nodes. See [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `--template-resources-preset`: A compatible preset (number of GPUs and vCPUs, RAM size), see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `--template-gpu-settings-drivers-preset`: GPU drivers preset, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

  * `--template-gpu-settings-dra` (optional): Enables Dynamic Resource Allocation for the node group. See [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md#how-to-enable-dra-on-a-node-group).

  * `--template-gpu-cluster-id`: GPU cluster ID. Specify this parameter to interconnect GPU nodes using InfiniBand™. The selected platform and preset must be compatible with GPU clusters. See [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand](https://docs.nebius.com/kubernetes/gpu/clusters.md).

    > [!WARNING]
    >
    > If a node group uses a GPU cluster, the GPU cluster must be located in the same project as the node group's parent cluster.

  * `--template-service-account-id`: Service account ID. You can add a service account, for example, to [pull images from Container Registry](https://docs.nebius.com/kubernetes/workloads/images-container-registry.md).

  * `--template-network-interfaces`: Network interface configuration (for example, subnet ID, see [How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups](https://docs.nebius.com/kubernetes/networking/non-default-subnet.md)).

  * `--template-filesystems`: Filesystem for nodes, see [How to attach volumes to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms).

    > [!WARNING]
    >
    > The filesystem that you are adding to a node group must be located in the same project as the node group's parent cluster. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

  * `--template-local-disks-passthrough-group-requested` (optional): Requests [local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) when set to `true`. You can configure how the local SSD disks are added to your node group with one of the following parameters:

    * `--template-local-disks-config-kubelet-ephemeral`: Set to `true` to use the requested local SSD disks as the node's [local ephemeral storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/). Managed Kubernetes prepares, formats and mounts the resulting storage for node ephemeral data. This is the default configuration mode.
    * `--template-local-disks-config-none`: Set to `true` to provision the requested local SSD disks with no preparation.

    > [!NOTE]
    >
    > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

  * `--template-reservation-policy-policy`: Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/kubernetes/node-groups/reservations.md) and run your node group based on them. As a result, the node group resources are reserved and always available.

  * `--template-reservation-policy-reservation-ids`: IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

    For information about how to configure `--template-reservation-policy-policy` and `--template-reservation-policy-reservation-ids`, see [How to add reservations to node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md#how-to-add-reservations-to-node-groups).

* **Deployment strategy**

  The *deployment strategy* of a node group defines how it is updated when necessary — for example, when you modify the group's node template or Kubernetes version, or when nodes fail and need to be replaced. For more details, see [Deployment strategy and quotas](#deployment-strategy-and-quotas).

  The following parameters specify the deployment strategy:

  * `--strategy-max-unavailable-percent`, `--strategy-max-unavailable-count`: The maximum number of nodes in a group that can be unavailable at any time during an update, set as a percentage of the group's target size or a number of nodes. When a percentage is used, the number of nodes is calculated by rounding down.

    > For example, if the value of `--strategy-max-unavailable-percent` is 40 and the group's target size is 3, at most ⌊3 × 40%⌋ = ⌊1.2⌋ = 1 node can be unavailable at any time during the update.

    The default value is `--strategy-max-unavailable-count 1`. Cannot be set to 0 if `--strategy-max-surge-count` or `--strategy-max-surge-percent` is 0.

  * `--strategy-max-surge-percent`, `--strategy-max-surge-count`: The maximum number of nodes in a group that can exceed the group's target size at any time during an update, set as a percentage of the target size or as a number of nodes.

    > For example, if the value of `--strategy-max-surge-count` is 2 and the group's target size is 3, then the group can only have 3 + 2 = 5 nodes at any time during the update.

    The default value is `--strategy-max-surge-count 0`. Cannot be set to 0 if `--strategy-max-unavailable-count` or `--strategy-max-unavailable-percent` is 0.

  * `--strategy-drain-timeout`: The maximum amount of time it can take to drain a node during the update. If the timeout is set, a node in the updated group is deleted when it reaches the timeout, even if its draining is not complete.

    > [!WARNING]
    >
    > The default timeout is 10 minutes. If draining isn't completed within this time frame, Managed Kubernetes applies the force drain and deletes the node.

**Terraform**

The `nebius_mk8s_v1_node_group` resource supports the following parameters:

* **Metadata**

  * `parent_id`: Cluster ID.
  * `name`: Node group name. Must be unique within the tenant. Cannot be changed after creation.

* **Kubernetes version on nodes**

  * `version`: Kubernetes version in `<major>.<minor>` format. Recommended version is 1.36. For more information, see [Kubernetes versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

* **Node group size**

  * `fixed_node_count`: Number of nodes per group. The maximum is 100. Cannot be set together with `autoscaling`.
  * `autoscaling.min_node_count`, `autoscaling.max_node_count`: Allow you to set the range of nodes within which the [cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) adds or removes nodes as needed. Cannot be set together with `fixed_node_count`.

* **Node template**

  All nodes in a group are identical and are created based on a *node template*. A node template is similar to a virtual machine specification in Compute.

  The node template is configured in the `template` block and supports the following parameters:

  * `template.taints`: Array of Kubernetes [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) (rules that repel Pods from nodes) for all nodes in the group.

  * `template.resources.platform`: ID of the Compute VM platform for the nodes. See [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `template.resources.preset`: A compatible preset (number of GPUs and vCPUs, RAM size), see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `template.gpu_settings.drivers_preset`: GPU drivers preset. For more information, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

  * `template.gpu_settings.dra` (optional): Enables Dynamic Resource Allocation for the node group. See [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md#how-to-enable-dra-on-a-node-group).

  * `template.gpu_cluster.id`: GPU cluster ID. Specify this parameter to interconnect GPU nodes using InfiniBand™. The selected platform and preset must be compatible with GPU clusters. See [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand](https://docs.nebius.com/kubernetes/gpu/clusters.md).

    > [!WARNING]
    >
    > If a node group uses a GPU cluster, the GPU cluster must be located in the same project as the node group's parent cluster.

  * `template.service_account_id`: Service account ID. You can add a service account, for example, to [pull images from Container Registry](https://docs.nebius.com/kubernetes/workloads/images-container-registry.md).

  * `template.network_interfaces`: Network interface configuration (for example, subnet ID, see [How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups](https://docs.nebius.com/kubernetes/networking/non-default-subnet.md)).

  * `template.filesystems`: Filesystem for nodes, see [How to attach volumes to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms).

    > [!WARNING]
    >
    > The filesystem that you are adding to a node group must be located in the same project as the node group's parent cluster. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

  * `template.local_disks.passthrough_group.requested`: Requests [local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) when set to `true`. You can configure how the local SSD disks are added to your node group with one of the following parameters:

    * `template.local_disks.config.kubelet_ephemeral`: Set to `true` to use the requested local SSD disks as the node's [local ephemeral storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/). Managed Kubernetes prepares, formats and mounts the resulting storage for node ephemeral data. This is the default configuration mode.
    * `template.local_disks.config.none`: Set to `true` to provision the requested local SSD disks with no configuration.

    > [!NOTE]
    >
    > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

  * `template.reservation_policy.policy`: Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/kubernetes/node-groups/reservations.md) and run your node group based on them. As a result, the node group resources are reserved and always available.

  * `template.reservation_policy.reservation_ids`: IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

    For information about how to configure `template.reservation_policy.policy` and `template.reservation_policy.reservation_ids`, see [How to add reservations to node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md#how-to-add-reservations-to-node-groups).

* **Deployment strategy**

  The *deployment strategy* of a node group defines how it is updated when necessary — for example, when you modify the group's node template or Kubernetes version, or when nodes fail and need to be replaced. For more details, see [Deployment strategy and quotas](#deployment-strategy-and-quotas).

  The deployment strategy is configured in the `strategy` block:

  * `strategy.max_unavailable.percent`, `strategy.max_unavailable.count`: The maximum number of nodes in a group that can be unavailable at any time during an update, set as a percentage of the group's target size or a number of nodes. When a percentage is used, the number of nodes is calculated by rounding down.

    > For example, if `strategy.max_unavailable.percent = 40` and the group's target size is 3, at most ⌊3 × 40%⌋ = ⌊1.2⌋ = 1 node can be unavailable at any time during the update.

    The default value is 1. Cannot be set to 0 if `strategy.max_surge.count` or `strategy.max_surge.percent` is set to 0.

  * `strategy.max_surge.percent`, `strategy.max_surge.count`: The maximum number of nodes in a group that can exceed the group's target size at any time during an update, set as a percentage of the target size or as a number of nodes.

    > For example, if `strategy.max_surge.count = 2` and the group's target size is 3, then the group can have up to 3 + 2 = 5 nodes at any time during the update.

    The default value is `strategy.max_surge.count = 0`. Cannot be set to 0 if `strategy.max_unavailable.count` or `strategy.max_unavailable.percent` is set to 0.

  * `strategy.drain_timeout`: The maximum amount of time it can take to drain a node during the update. If the timeout is set, a node in the updated group is deleted when it reaches the timeout, even if its draining is not complete.

    > [!WARNING]
    >
    > The default timeout is 10 minutes. If draining isn't completed within this time frame, Managed Kubernetes applies the force drain and deletes the node.

**Go SDK**

The `mk8s.CreateNodeGroupRequest` and `mk8s.UpdateNodeGroupRequest` messages support the following parameters.

Parameters that the API defines as `oneof` fields are set through a wrapper type. For example, `Spec.Size` with a fixed node count is `Size: &mk8s.NodeGroupSpec_FixedNodeCount{FixedNodeCount: 3}`, and `Spec.Template.Resources.Size` with a preset is `Size: &mk8s.ResourcesSpec_Preset{Preset: "<preset_name>"}`. The paths below are given in their flattened form; the code samples on this page show the wrappers in place.

* **Metadata**

  * `Metadata.ParentId`: Cluster ID.
  * `Metadata.Name`: Node group name. Must be unique within the tenant. Cannot be changed after creation.

* **Kubernetes version on nodes**

  * `Spec.Version`: Kubernetes version in `<major>.<minor>` format. Recommended version is 1.36. For more information, see [Kubernetes versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

* **Node group size**

  * `Spec.Size.FixedNodeCount`: Number of nodes per group. The maximum is 100. Cannot be set together with `Spec.Size.Autoscaling`.
  * `Spec.Size.Autoscaling.MinNodeCount`, `Spec.Size.Autoscaling.MaxNodeCount`: Allow you to set the range of nodes within which the [cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) adds or removes nodes as needed. Cannot be set together with `Spec.Size.FixedNodeCount`.

* **Node template**

  All nodes in a group are identical and are created based on a *node template*. A node template is similar to a virtual machine specification in Compute.

  The node template is configured in `Spec.Template` and supports the following parameters:

  * `Spec.Template.Taints`: Array of Kubernetes [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) (rules that repel Pods from nodes) for all nodes in the group.

  * `Spec.Template.Resources.Platform`: A platform with GPUs, see [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™](https://docs.nebius.com/kubernetes/gpu/clusters.md).

  * `Spec.Template.Resources.Size.Preset`: A compatible preset (number of GPUs and vCPUs, RAM size), see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `Spec.Template.GpuSettings.DriversPreset`: GPU drivers preset, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

  * `Spec.Template.GpuSettings.Dra` (optional): Enables Dynamic Resource Allocation for the node group. See [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md#how-to-enable-dra-on-a-node-group).

  * `Spec.Template.GpuCluster.Id`: GPU cluster ID.

  * `Spec.Template.ServiceAccountId`: Service account ID. You can add a service account, for example, to [pull images from Container Registry](https://docs.nebius.com/kubernetes/workloads/images-container-registry.md).

  * `Spec.Template.NetworkInterfaces`: Network interface configuration (for example, subnet ID, see [How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups](https://docs.nebius.com/kubernetes/networking/non-default-subnet.md)).

  * `Spec.Template.Filesystems`: Filesystem for nodes, see [How to attach volumes to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms).

    > [!WARNING]
    >
    > The filesystem that you are adding to a node group must be located in the same project as the node group's parent cluster. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

  * `Spec.Template.LocalDisks.PassthroughGroup.Requested`: Requests [local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) when set to `true`. You can configure how the local SSD disks are added to your node group with one of the following parameters:

    * `Spec.Template.LocalDisks.Config.KubeletEphemeral`: Set to `true` to use the requested local SSD disks as the node's [local ephemeral storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/). Managed Kubernetes prepares, formats and mounts the resulting storage for node ephemeral data. This is the default configuration mode.
    * `Spec.Template.LocalDisks.Config.None`: Set to `true` to provision the requested local SSD disks with no configuration.

    > [!NOTE]
    >
    > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

  * `Spec.Template.ReservationPolicy.Policy`: Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/kubernetes/node-groups/reservations.md) and run your node group based on them. As a result, the node group resources are reserved and always available.

  * `Spec.Template.ReservationPolicy.ReservationIds`: IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

    For information about how to configure `Spec.Template.ReservationPolicy.Policy` and `Spec.Template.ReservationPolicy.ReservationIds`, see [How to add reservations to node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md#how-to-add-reservations-to-node-groups).

* **Deployment strategy**

  The *deployment strategy* of a node group defines how it is updated when necessary — for example, when you modify the group's node template or Kubernetes version, or when nodes fail and need to be replaced. For more details, see [Deployment strategy and quotas](#deployment-strategy-and-quotas).

  The deployment strategy is configured in `Spec.Strategy`:

  * `Spec.Strategy.MaxUnavailable.Percent`, `Spec.Strategy.MaxUnavailable.Count`: The maximum number of nodes in a group that can be unavailable at any time during an update, set as a percentage of the group's target size or a number of nodes. When a percentage is used, the number of nodes is calculated by rounding down.

    > For example, if `Spec.Strategy.MaxUnavailable.Percent` is 40 and the group's target size is 3, at most ⌊3 × 40%⌋ = ⌊1.2⌋ = 1 node can be unavailable at any time during the update.

    The default value is 1. Cannot be set to 0 if `Spec.Strategy.MaxSurge.Count` or `Spec.Strategy.MaxSurge.Percent` is set to 0.

  * `Spec.Strategy.MaxSurge.Percent`, `Spec.Strategy.MaxSurge.Count`: The maximum number of nodes in a group that can exceed the group's target size at any time during an update, set as a percentage of the target size or as a number of nodes.

    > For example, if `Spec.Strategy.MaxSurge.Count` is 2 and the group's target size is 3, then the group can have up to 3 + 2 = 5 nodes at any time during the update.

    The default value is 0. Cannot be set to 0 if `Spec.Strategy.MaxUnavailable.Count` or `Spec.Strategy.MaxUnavailable.Percent` is set to 0.

  * `Spec.Strategy.DrainTimeout`: The maximum amount of time it can take to drain a node during the update. If the timeout is set, a node in the updated group is deleted when it reaches the timeout, even if its draining is not complete.

    > [!WARNING]
    >
    > The default timeout is 10 minutes. If draining isn't completed within this time frame, Managed Kubernetes applies the force drain and deletes the node.

**Python SDK**

The `CreateNodeGroupRequest` and `UpdateNodeGroupRequest` classes support the following parameters.

* **Metadata**

  * `metadata.parent_id`: Cluster ID.
  * `metadata.name`: Node group name. Must be unique within the tenant. Cannot be changed after creation.

* **Kubernetes version on nodes**

  * `spec.version`: Kubernetes version in `<major>.<minor>` format. Recommended version is 1.36. For more information, see [Kubernetes versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

* **Node group size**

  * `spec.fixed_node_count`: Number of nodes per group. The maximum is 100. Cannot be set together with `spec.autoscaling`.
  * `spec.autoscaling.min_node_count`, `spec.autoscaling.max_node_count`: Allow you to set the range of nodes within which the [cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) adds or removes nodes as needed. Cannot be set together with `spec.fixed_node_count`.

* **Node template**

  All nodes in a group are identical and are created based on a *node template*. A node template is similar to a virtual machine specification in Compute.

  The node template is configured in `spec.template` and supports the following parameters:

  * `spec.template.taints`: Array of Kubernetes [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) (rules that repel Pods from nodes) for all nodes in the group.

  * `spec.template.resources.platform`: A platform with GPUs, see [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™](https://docs.nebius.com/kubernetes/gpu/clusters.md).

  * `spec.template.resources.preset`: A compatible preset (number of GPUs and vCPUs, RAM size), see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `spec.template.gpu_settings.drivers_preset`: GPU drivers preset, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

  * `spec.template.gpu_settings.dra` (optional): Enables Dynamic Resource Allocation for the node group. See [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md#how-to-enable-dra-on-a-node-group).

  * `spec.template.gpu_cluster.id`: GPU cluster ID.

  * `spec.template.service_account_id`: Service account ID. You can add a service account, for example, to [pull images from Container Registry](https://docs.nebius.com/kubernetes/workloads/images-container-registry.md).

  * `spec.template.network_interfaces`: Network interface configuration (for example, subnet ID, see [How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups](https://docs.nebius.com/kubernetes/networking/non-default-subnet.md)).

  * `spec.template.filesystems`: Filesystem for nodes, see [How to attach volumes to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms).

    > [!WARNING]
    >
    > The filesystem that you are adding to a node group must be located in the same project as the node group's parent cluster. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

  * `spec.template.local_disks.passthrough_group.requested`: Requests [local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) when set to `true`. You can configure how the local SSD disks are added to your node group with one of the following parameters:

    * `spec.template.local_disks.config.kubelet_ephemeral`: Set to `true` to use the requested local SSD disks as the node's [local ephemeral storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/). Managed Kubernetes prepares, formats and mounts the resulting storage for node ephemeral data. This is the default configuration mode.
    * `spec.template.local_disks.config.none`: Set to `true` to provision the requested local SSD disks with no configuration.

    > [!NOTE]
    >
    > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

  * `spec.template.reservation_policy.policy`: Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/kubernetes/node-groups/reservations.md) and run your node group based on them. As a result, the node group resources are reserved and always available.

  * `spec.template.reservation_policy.reservation_ids`: IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

    For information about how to configure `spec.template.reservation_policy.policy` and `spec.template.reservation_policy.reservation_ids`, see [How to add reservations to node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md#how-to-add-reservations-to-node-groups).

* **Deployment strategy**

  The *deployment strategy* of a node group defines how it is updated when necessary — for example, when you modify the group's node template or Kubernetes version, or when nodes fail and need to be replaced. For more details, see [Deployment strategy and quotas](#deployment-strategy-and-quotas).

  The deployment strategy is configured in `spec.strategy`:

  * `spec.strategy.max_unavailable.percent`, `spec.strategy.max_unavailable.count`: The maximum number of nodes in a group that can be unavailable at any time during an update, set as a percentage of the group's target size or a number of nodes. When a percentage is used, the number of nodes is calculated by rounding down.

    > For example, if `spec.strategy.max_unavailable.percent` is 40 and the group's target size is 3, at most ⌊3 × 40%⌋ = ⌊1.2⌋ = 1 node can be unavailable at any time during the update.

    The default value is 1. Cannot be set to 0 if `spec.strategy.max_surge.count` or `spec.strategy.max_surge.percent` is set to 0.

  * `spec.strategy.max_surge.percent`, `spec.strategy.max_surge.count`: The maximum number of nodes in a group that can exceed the group's target size at any time during an update, set as a percentage of the target size or as a number of nodes.

    > For example, if `spec.strategy.max_surge.count` is 2 and the group's target size is 3, then the group can have up to 3 + 2 = 5 nodes at any time during the update.

    The default value is 0. Cannot be set to 0 if `spec.strategy.max_unavailable.count` or `spec.strategy.max_unavailable.percent` is set to 0.

  * `spec.strategy.drain_timeout`: The maximum amount of time it can take to drain a node during the update. If the timeout is set, a node in the updated group is deleted when it reaches the timeout, even if its draining is not complete.

    > [!WARNING]
    >
    > The default timeout is 10 minutes. If draining isn't completed within this time frame, Managed Kubernetes applies the force drain and deletes the node.

**JavaScript SDK**

The `CreateNodeGroupRequest` and `UpdateNodeGroupRequest` messages support the following parameters.

Parameters that the API defines as `oneof` fields are set through a `$case` object. For example, `spec.size` with a fixed node count is `size: { $case: "fixedNodeCount", fixedNodeCount: 3 }`, and `spec.template.resources.size` with a preset is `size: { $case: "preset", preset: "<preset_name>" }`. The paths below are given in their flattened form; the code samples on this page show the `$case` objects in place.

* **Metadata**

  * `metadata.parentId`: Cluster ID.
  * `metadata.name`: Node group name. Must be unique within the tenant. Cannot be changed after creation.

* **Kubernetes version on nodes**

  * `spec.version`: Kubernetes version in `<major>.<minor>` format. Recommended version is 1.36. For more information, see [Kubernetes versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).

* **Node group size**

  * `spec.size.fixedNodeCount`: Number of nodes per group. The maximum is 100. Cannot be set together with `spec.size.autoscaling`.
  * `spec.size.autoscaling.minNodeCount`, `spec.size.autoscaling.maxNodeCount`: Allow you to set the range of nodes within which the [cluster autoscaler](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md) adds or removes nodes as needed. Cannot be set together with `spec.size.fixedNodeCount`.

* **Node template**

  All nodes in a group are identical and are created based on a *node template*. A node template is similar to a virtual machine specification in Compute.

  The node template is configured in `spec.template` and supports the following parameters:

  * `spec.template.taints`: Array of Kubernetes [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) (rules that repel Pods from nodes) for all nodes in the group.

  * `spec.template.resources.platform`: A platform with GPUs, see [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™](https://docs.nebius.com/kubernetes/gpu/clusters.md).

  * `spec.template.resources.size.preset`: A compatible preset (number of GPUs and vCPUs, RAM size), see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `spec.template.gpuSettings.driversPreset`: GPU drivers preset, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

  * `spec.template.gpuSettings.dra` (optional): Enables dynamic resource allocation for the node group. See [Dynamic resource allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md#how-to-enable-dra-on-a-node-group).

  * `spec.template.gpuCluster.id`: GPU cluster ID.

  * `spec.template.serviceAccountId`: Service account ID. You can add a service account, for example, to [pull images from Container Registry](https://docs.nebius.com/kubernetes/workloads/images-container-registry.md).

  * `spec.template.networkInterfaces`: Network interface configuration (for example, subnet ID, see [How to use a non-default subnet for Managed Service for Kubernetes® clusters and node groups](https://docs.nebius.com/kubernetes/networking/non-default-subnet.md)).

  * `spec.template.filesystems`: Filesystem for nodes, see [How to attach volumes to VMs](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms).

    > [!WARNING]
    >
    > The filesystem that you are adding to a node group must be located in the same project as the node group's parent cluster. For more details about projects and resource hierarchy in Nebius AI Cloud, see [How resources, identities and access are managed in Nebius AI Cloud](https://docs.nebius.com/iam/overview.md).

  * `spec.template.localDisks.passthroughGroup.requested`: Requests [local SSD disks](https://docs.nebius.com/compute/storage/types.md#local-ssd-disks) when set to `true`. You can configure how the local SSD disks are added to your node group with one of the following parameters:

    * `spec.template.localDisks.config.kubeletEphemeral`: Set to `true` to use the requested local SSD disks as the node's [local ephemeral storage](https://kubernetes.io/docs/concepts/storage/ephemeral-storage/). Managed Kubernetes prepares, formats and mounts the resulting storage for node ephemeral data. This is the default configuration mode.
    * `spec.template.localDisks.config.none`: Set to `true` to provision the requested local SSD disks with no configuration.

    > [!NOTE]
    >
    > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

  * `spec.template.reservationPolicy.policy`: Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/kubernetes/node-groups/reservations.md) and run your node group based on them. As a result, the node group resources are reserved and always available.

  * `spec.template.reservationPolicy.reservationIds`: IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

    For information about how to configure `spec.template.reservationPolicy.policy` and `spec.template.reservationPolicy.reservationIds`, see [How to add reservations to node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md#how-to-add-reservations-to-node-groups).

* **Deployment strategy**

  The *deployment strategy* of a node group defines how it is updated when necessary — for example, when you modify the group's node template or Kubernetes version, or when nodes fail and need to be replaced. For more details, see [Deployment strategy and quotas](#deployment-strategy-and-quotas).

  The deployment strategy is configured in `spec.strategy`:

  * `spec.strategy.maxUnavailable.percent`, `spec.strategy.maxUnavailable.count`: The maximum number of nodes in a group that can be unavailable at any time during an update, set as a percentage of the group's target size or a number of nodes. When a percentage is used, the number of nodes is calculated by rounding down.

    > For example, if `spec.strategy.maxUnavailable.percent` is 40 and the group's target size is 3, at most ⌊3 × 40%⌋ = ⌊1.2⌋ = 1 node can be unavailable at any time during the update.

    The default value is 1. Cannot be set to 0 if `spec.strategy.maxSurge.count` or `spec.strategy.maxSurge.percent` is set to 0.

  * `spec.strategy.maxSurge.percent`, `spec.strategy.maxSurge.count`: The maximum number of nodes in a group that can exceed the group's target size at any time during an update, set as a percentage of the target size or as a number of nodes.

    > For example, if `spec.strategy.maxSurge.count` is 2 and the group's target size is 3, then the group can have up to 3 + 2 = 5 nodes at any time during the update.

    The default value is 0. Cannot be set to 0 if `spec.strategy.maxUnavailable.count` or `spec.strategy.maxUnavailable.percent` is set to 0.

  * `spec.strategy.drainTimeout`: The maximum amount of time it can take to drain a node during the update. If the timeout is set, a node in the updated group is deleted when it reaches the timeout, even if its draining is not complete.

    > [!WARNING]
    >
    > The default timeout is 10 minutes. If draining isn't completed within this time frame, Managed Kubernetes applies the force drain and deletes the node.

## How to delete node groups

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.
2. Open the cluster page and then go to the **Node groups** tab.
3. Open the page of the node group that you want to remove.
4. Switch to the **Settings** tab.
5. Click **Delete node group**.
6. Confirm the deletion.

**CLI**

To delete a node group, get its ID as shown in [How to modify node groups](#how-to-modify-node-groups) and run the following command:

```bash theme={null}
nebius mk8s node-group delete --id $K8S_NODE_GROUP_ID
```

**Terraform**

1. Remove the corresponding `nebius_mk8s_v1_node_group` resource from the node group configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

To delete a node group, get its ID as shown in [How to modify node groups](#how-to-modify-node-groups) and delete the group by this ID:

```go theme={null}
deleteFileGroupOp, err := sdk.Services().MK8S().V1().
    NodeGroup().Delete(
        ctx,
        &mk8s.DeleteNodeGroupRequest{Id: nodeGroupID},
    )
if err != nil {
    return err
}
if _, err = deleteFileGroupOp.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

To delete a node group, get its ID as shown in [How to modify node groups](#how-to-modify-node-groups) and delete the group by this ID:

```python theme={null}
delete_file_group_service = NodeGroupServiceClient(sdk)
delete_file_group_operation = await delete_file_group_service.delete(
    DeleteNodeGroupRequest(id=node_group_id),
)
await delete_file_group_operation.wait()
```

**JavaScript SDK**

To delete a node group, get its ID as shown in [How to modify node groups](#how-to-modify-node-groups) and delete the group by this ID:

```ts theme={null}
const deleteFileGroupService = new NodeGroupService(sdk);
const deleteFileGroupOperation = await deleteFileGroupService.delete(
  DeleteNodeGroupRequest.create({
    id: nodeGroupId,
  }),
).result;
await deleteFileGroupOperation.wait();
```

## Examples

**CLI**

* Creating a node group with two nodes, each with 8 NVIDIA H100 GPUs, 128 vCPUs, 1600 GiB of RAM, a 100 GiB Network SSD disk and the Kubernetes version 1.36:

  ```bash theme={null}
  export SUBNET_ID=$(nebius vpc subnet list \
    --format jsonpath='{.items[0].metadata.id}')
  nebius mk8s node-group create \
    --parent-id $K8S_CLUSTER_ID \
    --name node-group-example \
    --version 1.36 \
    --fixed-node-count 2 \
    --template-resources-platform gpu-h100-sxm \
    --template-resources-preset 8gpu-128vcpu-1600gb \
    --template-gpu-settings-drivers-preset cuda13.0 \
    --template-boot-disk-type NETWORK_SSD \
    --template-boot-disk-size-gibibytes 100 \
    --template-network-interfaces "[{\"subnet_id\": \"$SUBNET_ID\"}]"
  ```

* Modifying the node group from the previous example (ID `$K8S_NODE_GROUP_ID`) to add a node and enable public IP addresses for all nodes:

  ```bash theme={null}
  nebius mk8s node-group update \
    --id $K8S_NODE_GROUP_ID \
    --auto-approve \
    --fixed-node-count 3 \
    --template-network-interfaces "[{\"subnet_id\": \"$SUBNET_ID\", \"public_ip_address\": {}}]"
  ```

**Terraform**

Creating a node group with two nodes, each with 8 NVIDIA H100 GPUs, 128 vCPUs, 1600 GiB of RAM, a 100 GiB Network SSD disk and the Kubernetes version 1.36:

```hcl theme={null}
resource "nebius_mk8s_v1_node_group" "node-group-example" {
  name = "node-group-example"
  parent_id = $K8S_CLUSTER_ID
  version = "1.36"
  fixed_node_count = 2

  template = {
    resources = {
      platform = "gpu-h100-sxm"
      preset = "8gpu-128vcpu-1600gb"
    }

    gpu_settings = {
      drivers_preset = "cuda12.8"
    }

    boot_disk = {
      type = "NETWORK_SSD"
      size_gibibytes = 100
    }
  }
}
```

**Go SDK**

* Creating a node group with two nodes, each with 8 NVIDIA H100 GPUs, 128 vCPUs, 1600 GiB of RAM, a 100 GiB Network SSD disk and the Kubernetes version 1.36:

  ```go theme={null}
  subnetGroupOp, err := sdk.Services().MK8S().V1().
      NodeGroup().Create(
          ctx,
          &mk8s.CreateNodeGroupRequest{
              Metadata: &common.ResourceMetadata{
                  ParentId: k8sClusterID,
                  Name:     "node-group-example",
              },
              Spec: &mk8s.NodeGroupSpec{
                  Version: "1.36",
                  Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                      FixedNodeCount: 2,
                  },
                  Template: &mk8s.NodeTemplate{
                      Resources: &mk8s.ResourcesSpec{
                          Platform: "gpu-h100-sxm",
                          Size: &mk8s.ResourcesSpec_Preset{
                              Preset: "8gpu-128vcpu-1600gb",
                          },
                      },
                      GpuSettings: &mk8s.GpuSettings{
                          DriversPreset: "cuda13.0",
                      },
                      BootDisk: &mk8s.DiskSpec{
                          Size: &mk8s.DiskSpec_SizeGibibytes{
                              SizeGibibytes: 100,
                          },
                          Type: mk8s.DiskSpec_NETWORK_SSD,
                      },
                      NetworkInterfaces:
                          []*mk8s.NetworkInterfaceTemplate{
                          {SubnetId: subnetID},
                      },
                  },
              },
          },
      )
  if err != nil {
      return err
  }
  if _, err = subnetGroupOp.Wait(ctx); err != nil {
      return err
  }
  ```

  `SubnetId` reads the `subnetID` variable. Assign the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) to it before you run the code.

* Modifying the node group from the previous example (ID `nodeGroupID`) to add a node and enable public IP addresses for all nodes:

  ```go theme={null}
  groupForNetwork, err := sdk.Services().MK8S().V1().
      NodeGroup().Get(
          ctx,
          &mk8s.GetNodeGroupRequest{Id: nodeGroupID},
      )
  if err != nil {
      return err
  }
  groupNetworkSpec := groupForNetwork.GetSpec()
  if groupNetworkSpec == nil || groupNetworkSpec.GetTemplate() == nil {
      return errors.New("node group template is missing")
  }
  groupNetworkSpec.Size = &mk8s.NodeGroupSpec_FixedNodeCount{
      FixedNodeCount: 3,
  }
  groupNetworkSpec.GetTemplate().NetworkInterfaces =
      []*mk8s.NetworkInterfaceTemplate{
          {
              SubnetId:         subnetID,
              PublicIpAddress: &mk8s.PublicIPAddress{},
          },
      }
  updateNetworkOp, err := sdk.Services().MK8S().V1().NodeGroup().
      Update(
          ctx,
          &mk8s.UpdateNodeGroupRequest{
              Metadata: groupForNetwork.GetMetadata(),
              Spec:     groupNetworkSpec,
          },
      )
  if err != nil {
      return err
  }
  if _, err = updateNetworkOp.Wait(ctx); err != nil {
      return err
  }
  ```

**Python SDK**

* Creating a node group with two nodes, each with 8 NVIDIA H100 GPUs, 128 vCPUs, 1600 GiB of RAM, a 100 GiB Network SSD disk and the Kubernetes version 1.36:

  ```python theme={null}
  subnet_group_service = NodeGroupServiceClient(sdk)
  subnet_group_operation = await subnet_group_service.create(
      CreateNodeGroupRequest(
          metadata=ResourceMetadata(
              parent_id=k8s_cluster_id,
              name="node-group-example",
          ),
          spec=NodeGroupSpec(
              version="1.36",
              fixed_node_count=2,
              template=NodeTemplate(
                  resources=ResourcesSpec(
                      platform="gpu-h100-sxm",
                      preset="8gpu-128vcpu-1600gb",
                  ),
                  gpu_settings=GpuSettings(drivers_preset="cuda13.0"),
                  boot_disk=DiskSpec(
                      size_gibibytes=100,
                      type=DiskSpec__DiskType.NETWORK_SSD,
                  ),
                  network_interfaces=[
                      NetworkInterfaceTemplate(subnet_id=subnet_id),
                  ],
              ),
          ),
      ),
  )
  await subnet_group_operation.wait()
  ```

  `subnet_id` reads the `subnet_id` variable. Assign the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) to it before you run the code.

* Modifying the node group from the previous example (ID `node_group_id`) to add a node and enable public IP addresses for all nodes:

  ```python theme={null}
  network_group_service = NodeGroupServiceClient(sdk)
  group_for_network = await network_group_service.get(
      GetNodeGroupRequest(id=node_group_id),
  )
  if (
      group_for_network.spec is None
      or group_for_network.spec.template is None
  ):
      raise ValueError("node group template is missing")
  group_for_network.spec.fixed_node_count = 3
  group_for_network.spec.template.network_interfaces = [
      NetworkInterfaceTemplate(
          subnet_id=subnet_id,
          public_ip_address=PublicIPAddress(),
      ),
  ]
  update_network_operation = await network_group_service.update(
      UpdateNodeGroupRequest(
          metadata=group_for_network.metadata,
          spec=group_for_network.spec,
      ),
  )
  await update_network_operation.wait()
  ```

**JavaScript SDK**

* Creating a node group with two nodes, each with 8 NVIDIA H100 GPUs, 128 vCPUs, 1600 GiB of RAM, a 100 GiB Network SSD disk and the Kubernetes version 1.36:

  ```ts theme={null}
  const subnetGroupService = new NodeGroupService(sdk);
  const subnetGroupOperation = await subnetGroupService.create(
    CreateNodeGroupRequest.create({
      metadata: ResourceMetadata.create({
        parentId: k8sClusterId,
        name: "node-group-example",
      }),
      spec: NodeGroupSpec.create({
        version: "1.36",
        size: {
          $case: "fixedNodeCount",
          fixedNodeCount: 2,
        },
        template: NodeTemplate.create({
          resources: ResourcesSpec.create({
            platform: "gpu-h100-sxm",
            size: {
              $case: "preset",
              preset: "8gpu-128vcpu-1600gb",
            },
          }),
          gpuSettings: GpuSettings.create({
            driversPreset: "cuda13.0",
          }),
          bootDisk: DiskSpec.create({
            size: {
              $case: "sizeGibibytes",
              sizeGibibytes: 100,
            },
            type: DiskSpec_DiskType.NETWORK_SSD,
          }),
          networkInterfaces: [
            NetworkInterfaceTemplate.create({
              subnetId: subnetId,
            }),
          ],
        }),
      }),
    }),
  ).result;
  await subnetGroupOperation.wait();
  ```

  `subnetId` reads the `subnetId` variable. Assign the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) to it before you run the code.

* Modifying the node group from the previous example (ID `nodeGroupId`) to add a node and enable public IP addresses for all nodes:

  ```ts theme={null}
  const networkGroupService = new NodeGroupService(sdk);
  const groupForNetwork = await networkGroupService.get(
    GetNodeGroupRequest.create({
      id: nodeGroupId,
    }),
  );
  if (!groupForNetwork.spec?.template) {
    throw new Error("node group template is missing");
  }
  groupForNetwork.spec.size = {
    $case: "fixedNodeCount",
    fixedNodeCount: 3,
  };
  groupForNetwork.spec.template.networkInterfaces = [
    NetworkInterfaceTemplate.create({
      subnetId: subnetId,
      publicIpAddress: PublicIPAddress.create({}),
    }),
  ];
  const updateNetworkOperation = await networkGroupService.update(
    UpdateNodeGroupRequest.create({
      metadata: groupForNetwork.metadata,
      spec: groupForNetwork.spec,
    }),
  ).result;
  await updateNetworkOperation.wait();
  ```

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
