# Working with GPUs in the Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/gpu/set-up

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Working with GPUs in the Managed Service for Kubernetes®

To run ML, AI and high-performance computing (HPC) workloads in your Managed Service for Kubernetes cluster, you need to add nodes with GPUs to it. Managed Kubernetes nodes are Compute virtual machines, and you can choose VMs with GPUs to serve as nodes in your clusters.

In this article, you will learn how to set up GPUs in a Managed Kubernetes cluster. The article also touches on interconnecting GPUs using InfiniBand™ to accelerate your workloads; this topic is covered in detail in [another article](https://docs.nebius.com/kubernetes/gpu/clusters.md).

## How to add nodes with GPUs to a cluster

When [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) in a Managed Service for Kubernetes cluster, specify a virtual machine platform that supports GPUs:

**Web console**

In the node group creation form ( **Compute** → **Kubernetes** → your cluster → **Node groups** → **Create node group**), under **Computing resources**:

1. Select **With GPU**.
2. Select a platform and a preset. For available platforms and presets, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md) and [How to find out platforms and presets available in a project](https://docs.nebius.com/compute/virtual-machines/list-platforms.md).
3. Under **GPU settings**, keep the **Install NVIDIA GPU drivers and other components** option enabled.
4. Under **Drivers**, select a CUDA driver version. For available driver versions, see [GPU drivers and other components](#gpu-drivers-and-other-components).
5. Under **Operating system**, select an OS. Available operating systems depend on the selected driver.

   > [!NOTE]
   >
   > If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), disable the **Install NVIDIA GPU drivers and other components** option. Then, [manually install the GPU operator](#how-to-install-the-drivers-and-components-on-existing-node-groups).

**CLI**

Add GPU parameters to the [nebius mk8s node-group create](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md) command:

```bash theme={null}
nebius mk8s node-group create \
  --template-resources-platform gpu-h100-sxm \
  --template-resources-preset 8gpu-128vcpu-1600gb \
  --template-gpu-settings-drivers-preset cuda13.0 \
  ...
```

* In `--template-resources-platform`, specify a platform with GPUs. In `--template-resources-preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). For available platforms and presets, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md) and [How to find out platforms and presets available in a project](https://docs.nebius.com/compute/virtual-machines/list-platforms.md).

* In `--template-gpu-settings-drivers-preset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

  If you want to [install the drivers manually](https://docs.nebius.com/kubernetes/gpu/set-up.md#drivers-install), omit the `--template-gpu-settings-drivers-preset` parameter.

  > [!NOTE]
  >
  > If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit the `--template-gpu-settings-drivers-preset` parameter. Then, [manually install the GPU operator](#how-to-install-the-drivers-and-components-on-existing-node-groups).

**Go SDK**

Add GPU parameters to the node group spec:

```go theme={null}
nodeGroupOperation, err := sdk.Services().MK8S().V1().
    NodeGroup().Create(
        ctx,
        &mk8s.CreateNodeGroupRequest{
            Metadata: &common.ResourceMetadata{
                ParentId: mk8sClusterID,
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
                    BootDisk: &mk8s.DiskSpec{
                        Size: &mk8s.DiskSpec_SizeGibibytes{
                            SizeGibibytes: 100,
                        },
                        Type: mk8s.DiskSpec_NETWORK_SSD,
                    },
                    GpuSettings: &mk8s.GpuSettings{
                        DriversPreset: "cuda13.0",
                    },
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = nodeGroupOperation.Wait(ctx); err != nil {
    return err
}
nodeGroupID := nodeGroupOperation.ResourceID()
if nodeGroupID == "" {
    return fmt.Errorf("node group ID is missing")
}
```

* In `Template.Resources.Platform`, specify a platform with GPUs. In `Template.Resources.Size.Preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). For available platforms and presets, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md) and [How to find out platforms and presets available in a project](https://docs.nebius.com/compute/virtual-machines/list-platforms.md).

* In `Template.GpuSettings.DriversPreset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](#gpu-drivers-and-other-components).

  > [!NOTE]
  >
  > If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit `Template.GpuSettings`. Then, [manually install the GPU operator](#how-to-install-the-drivers-and-components-on-existing-node-groups).

**Python SDK**

Add GPU parameters to the node group spec:

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
node_group_operation = await node_group_service.create(
    CreateNodeGroupRequest(
        metadata=ResourceMetadata(
            parent_id=mk8s_cluster_id,
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
                boot_disk=DiskSpec(
                    size_gibibytes=100,
                    type=DiskSpec__DiskType.NETWORK_SSD,
                ),
                gpu_settings=GpuSettings(
                    drivers_preset="cuda13.0",
                ),
            ),
        ),
    ),
)
await node_group_operation.wait()
node_group_id = node_group_operation.resource_id
if not node_group_id:
    raise ValueError("node group ID is missing")
```

* In `template.resources.platform`, specify a platform with GPUs. In `template.resources.preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). For available platforms and presets, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md) and [How to find out platforms and presets available in a project](https://docs.nebius.com/compute/virtual-machines/list-platforms.md).

* In `template.gpu_settings.drivers_preset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](#gpu-drivers-and-other-components).

  > [!NOTE]
  >
  > If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit `template.gpu_settings`. Then, [manually install the GPU operator](#how-to-install-the-drivers-and-components-on-existing-node-groups).

**JavaScript SDK**

Add GPU parameters to the node group spec:

```ts theme={null}
const setupNodeGroupService = new NodeGroupService(sdk);
const nodeGroupOperation = await setupNodeGroupService.create(
  CreateNodeGroupRequest.create({
    metadata: ResourceMetadata.create({
      parentId: mk8sClusterId,
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
        bootDisk: DiskSpec.create({
          size: {
            $case: "sizeGibibytes",
            sizeGibibytes: 100,
          },
          type: DiskSpec_DiskType.NETWORK_SSD,
        }),
        gpuSettings: GpuSettings.create({
          driversPreset: "cuda13.0",
        }),
      }),
    }),
  }),
).result;
await nodeGroupOperation.wait();
const nodeGroupId = nodeGroupOperation.resourceId();
if (!nodeGroupId) {
  throw new Error("node group ID is missing");
}
```

* In `template.resources.platform`, specify a platform with GPUs. In `template.resources.size.preset`, specify a compatible preset (number of GPUs and vCPUs, RAM size). For available platforms and presets, see [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md) and [How to find out platforms and presets available in a project](https://docs.nebius.com/compute/virtual-machines/list-platforms.md).

* In `template.gpuSettings.driversPreset`, specify a supported preset to use a boot disk image that contains drivers and other components for GPUs. For more details, see [GPU drivers and other components](#gpu-drivers-and-other-components).

  > [!NOTE]
  >
  > If you need to modify the NVIDIA device plug-in (for example, to enable multi-instance GPU), omit `template.gpuSettings`. Then, [manually install the GPU operator](#how-to-install-the-drivers-and-components-on-existing-node-groups).

See an [example](https://docs.nebius.com/kubernetes/node-groups/manage.md#examples) of a full node group specification.

To enable InfiniBand interconnect between the nodes with GPUs, specify a GPU cluster when creating the node group. For more details, see [Interconnecting GPUs in Managed Service for Kubernetes® clusters using InfiniBand™](https://docs.nebius.com/kubernetes/gpu/clusters.md).

To request GPUs through Dynamic Resource Allocation, see [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md).

> [!WARNING]
>
> You cannot change the VM platform and preset or the GPU cluster of an existing node group. Create a new node group instead.

## GPU drivers and other components

For node groups with GPUs, Managed Kubernetes offers boot disk images with GPU drivers and other components required for GPUs.

You can specify Managed Kubernetes GPU images with `--template-gpu-settings-drivers-preset`. The preset determines the CUDA toolkit and NVIDIA driver series. Each preset has a default operating system (OS), you can optionally override it with `--template-os`.

| Driver preset | `cuda12.8` | `cuda13.0` |
| - | - | - |
| NVIDIA Data Center GPU Driver | 570.x | 580.x |
| OS | `ubuntu24.04` | `ubuntu24.04` |

> [!WARNING]
>
> If your cluster's control plane is on Kubernetes 1.30 (deprecated), use `cuda12` instead of `cuda12.8` (Ubuntu 24.04). Kubernetes 1.31 and later support `cuda12.8`, so there is no need to use `cuda12` on these versions.

To confirm which `drivers_preset` and `os` values are supported for your platform and Kubernetes version, check the compatibility matrix:

**CLI**

```bash theme={null}
nebius mk8s node-group get-compatibility-matrix \
  --cluster-kubernetes-version 1.36 \
  --platform gpu-h200-sxm
```

Example output:

```yaml theme={null}
versions:
  - items:
      - compatible_platforms:
          - gpu-h200-sxm
        os: ubuntu24.04
      - compatible_platforms:
          - gpu-h200-sxm
        drivers_preset: cuda12.8
        os: ubuntu24.04
      - compatible_platforms:
          - gpu-h200-sxm
        drivers_preset: cuda12
        os: ubuntu24.04
      - compatible_platforms:
          - gpu-h200-sxm
        drivers_preset: cuda13.0
        os: ubuntu24.04
    kubernetes_version: "1.36"
```

**Go SDK**

```go theme={null}
matrix, err := sdk.Services().MK8S().V1().
    NodeGroup().GetCompatibilityMatrix(
        ctx,
        &mk8s.GetNodeGroupCompatibilityMatrixRequest{
            ClusterKubernetesVersion:
                "1.36",
            Platform: "gpu-h200-sxm",
        },
    )
if err != nil {
    return err
}
fmt.Println(matrix)
```

The response lists the supported combinations in `Versions.Items`, each with `CompatiblePlatforms`, `DriversPreset` and `Os`.

**Python SDK**

```python theme={null}
node_group_service = NodeGroupServiceClient(sdk)
matrix = await node_group_service.get_compatibility_matrix(
    GetNodeGroupCompatibilityMatrixRequest(
        cluster_kubernetes_version="1.36",
        platform="gpu-h200-sxm",
    ),
)
print(matrix)
```

The response lists the supported combinations in `versions.items`, each with `compatible_platforms`, `drivers_preset` and `os`.

**JavaScript SDK**

```ts theme={null}
const nodeGroupService = new NodeGroupService(sdk);
const matrix = await nodeGroupService.getCompatibilityMatrix(
  GetNodeGroupCompatibilityMatrixRequest.create({
    clusterKubernetesVersion: "1.36",
    platform: "gpu-h200-sxm",
  }),
);
console.log(matrix);
```

The response lists the supported combinations in `versions.items`, each with `compatiblePlatforms`, `driversPreset` and `os`.

Use the returned `drivers_preset` and `os` values to select the driver branch and, optionally, an operating system (OS) in a node group configuration. For instructions on how to specify these parameters when creating a node group, see [How to add nodes with GPUs to a cluster](#how-to-add-nodes-with-gpus-to-a-cluster).

### How to change the driver preset

To change the driver preset for an existing node group:

**CLI**

```bash theme={null}
nebius mk8s node-group update \
  --id <group_ID> \
  --auto-approve \
  --template-gpu-settings-drivers-preset <new_preset>
```

**Go SDK**

```go theme={null}
groupForDriver, err := sdk.Services().MK8S().V1().
    NodeGroup().Get(
        ctx,
        &mk8s.GetNodeGroupRequest{Id: "<group_ID>"},
    )
if err != nil {
    return err
}
groupDriverSpec := groupForDriver.GetSpec()
if groupDriverSpec == nil || groupDriverSpec.GetTemplate() == nil {
    return errors.New("node group template is missing")
}
if groupDriverSpec.GetTemplate().GetGpuSettings() == nil {
    groupDriverSpec.GetTemplate().GpuSettings = &mk8s.GpuSettings{}
}
groupDriverSpec.GetTemplate().GetGpuSettings().DriversPreset =
    "<new_preset>"
driverGroupOp, err := sdk.Services().MK8S().V1().NodeGroup().
    Update(
        ctx,
        &mk8s.UpdateNodeGroupRequest{
            Metadata: groupForDriver.GetMetadata(),
            Spec:     groupDriverSpec,
        },
    )
if err != nil {
    return err
}
if _, err = driverGroupOp.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

```python theme={null}
driver_group_service = NodeGroupServiceClient(sdk)
group_for_driver = await driver_group_service.get(
    GetNodeGroupRequest(id="<group_ID>"),
)
if (
    group_for_driver.spec is None
    or group_for_driver.spec.template is None
):
    raise ValueError("node group template is missing")
if group_for_driver.spec.template.gpu_settings is None:
    group_for_driver.spec.template.gpu_settings = GpuSettings()
group_for_driver.spec.template.gpu_settings.drivers_preset = \
    "<new_preset>"
driver_group_operation = await driver_group_service.update(
    UpdateNodeGroupRequest(
        metadata=group_for_driver.metadata,
        spec=group_for_driver.spec,
    ),
)
await driver_group_operation.wait()
```

**JavaScript SDK**

```ts theme={null}
const driverGroupService = new NodeGroupService(sdk);
const groupForDriver = await driverGroupService.get(
  GetNodeGroupRequest.create({
    id: "<group_ID>",
  }),
);
if (!groupForDriver.spec?.template) {
  throw new Error("node group template is missing");
}
groupForDriver.spec.template.gpuSettings ??= GpuSettings.create({});
groupForDriver.spec.template.gpuSettings.driversPreset =
  "<new_preset>";
const driverGroupOperation = await driverGroupService.update(
  UpdateNodeGroupRequest.create({
    metadata: groupForDriver.metadata,
    spec: groupForDriver.spec,
  }),
).result;
await driverGroupOperation.wait();
```

> [!WARNING]
>
> When you change the driver preset, Managed Kubernetes recreates all nodes in the group according to the group's [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters).

### How to install the drivers and components on existing node groups

You can create a node group without the boot disk image. For example, you may opt not to use the **Install NVIDIA GPU drivers and other components** option when you create the node group in the web console. In this case, you can choose one of the following options to install the drivers and components:

* **Create a new node group with the image and migrate your workloads to it** (recommended)

  For instructions, see [Moving workload from the existing node group](https://docs.nebius.com/kubernetes/node-groups/moving-workload.md).

* **Modify the node group to use the image**

  > [!WARNING]
  >
  > When you modify a node group, Managed Kubernetes recreates each node according to the group's [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters).

  > **How to modify the node group**
  >
  > **CLI**
  >
  > Run the [nebius mk8s node-group update](https://docs.nebius.com/cli/reference/mk8s/node-group/update.md) command:
  >
  > ```bash theme={null}
  > nebius mk8s node-group update \
  >   --id <node_group_ID> \
  >   --auto-approve \
  >   --template-gpu-settings-drivers-preset cuda13.0
  > ```
  >
  > **Go SDK**
  >
  > Set `Template.GpuSettings.DriversPreset` on the node group and update it:
  >
  > ```go theme={null}
  > nodeGroup, err := sdk.Services().MK8S().V1().
  >     NodeGroup().Get(
  >         ctx,
  >         &mk8s.GetNodeGroupRequest{Id: "<node_group_ID>"},
  >     )
  > if err != nil {
  >     return err
  > }
  > nodeGroupSpec := nodeGroup.GetSpec()
  > if nodeGroupSpec == nil || nodeGroupSpec.GetTemplate() == nil {
  >     return errors.New("node group template spec is missing")
  > }
  > if nodeGroupSpec.GetTemplate().GetGpuSettings() == nil {
  >     nodeGroupSpec.GetTemplate().GpuSettings = &mk8s.GpuSettings{}
  > }
  > gpuSettings := nodeGroupSpec.GetTemplate().GetGpuSettings()
  > gpuSettings.DriversPreset = "cuda13.0"
  > updateNodeGroupOperation, err := sdk.Services().MK8S().V1().
  >     NodeGroup().Update(
  >         ctx,
  >         &mk8s.UpdateNodeGroupRequest{
  >             Metadata: nodeGroup.GetMetadata(),
  >             Spec:     nodeGroupSpec,
  >         },
  >     )
  > if err != nil {
  >     return err
  > }
  > if _, err = updateNodeGroupOperation.Wait(ctx); err != nil {
  >     return err
  > }
  > ```
  >
  > **Python SDK**
  >
  > Set `template.gpu_settings.drivers_preset` on the node group and update it:
  >
  > ```python theme={null}
  > node_group_service = NodeGroupServiceClient(sdk)
  > node_group = await node_group_service.get(
  >     GetNodeGroupRequest(id="<node_group_ID>"),
  > )
  > if node_group.spec is None or node_group.spec.template is None:
  >     raise ValueError("node group template spec is missing")
  > if node_group.spec.template.gpu_settings is None:
  >     node_group.spec.template.gpu_settings = GpuSettings()
  > node_group.spec.template.gpu_settings.drivers_preset = "cuda13.0"
  > update_node_group_operation = await node_group_service.update(
  >     UpdateNodeGroupRequest(
  >         metadata=node_group.metadata,
  >         spec=node_group.spec,
  >     ),
  > )
  > await update_node_group_operation.wait()
  > ```
  >
  > **JavaScript SDK**
  >
  > Set `template.gpuSettings.driversPreset` on the node group and update it:
  >
  > ```ts theme={null}
  > const updateNodeGroupService = new NodeGroupService(sdk);
  > const nodeGroup = await updateNodeGroupService.get(
  >   GetNodeGroupRequest.create({
  >     id: "<node_group_ID>",
  >   }),
  > );
  > if (!nodeGroup.spec?.template) {
  >   throw new Error("node group template spec is missing");
  > }
  > nodeGroup.spec.template.gpuSettings ??= GpuSettings.create({});
  > nodeGroup.spec.template.gpuSettings.driversPreset = "cuda13.0";
  > const updateNodeGroupOperation = await updateNodeGroupService.update(
  >   UpdateNodeGroupRequest.create({
  >     metadata: nodeGroup.metadata,
  >     spec: nodeGroup.spec,
  >   }),
  > ).result;
  > await updateNodeGroupOperation.wait();
  > ```

* **Manually install NVIDIA operators**

  You can install Kubernetes operators from NVIDIA that manage components required for GPUs and their networking:

  * **NVIDIA Network Operator**

    Installing NVIDIA Network Operator is required when at least one node group in the cluster does not use the boot disk image offered by Managed Kubernetes and satisfies any of the following conditions:

    * The node group uses NVIDIA B200 GPUs.
    * The node group is added to a GPU cluster for [InfiniBand interconnection](https://docs.nebius.com/kubernetes/gpu/clusters.md).

    In all other cases, NVIDIA Network Operator is optional.

  * **NVIDIA GPU Operator**

    Any cluster with at least one node group that has GPUs and does not use the boot disk image offered by Managed Kubernetes, must have NVIDIA GPU Operator installed.

  To install the operators, follow the instructions, depending on whether you enabled the InfiniBand interconnection:

  > **With InfiniBand: GPU and network operators**
  >
  > > [!WARNING]
  > >
  > > Install and check the operators in the exact order presented in these instructions. The operators depend on each other.
  >
  > 1. Prepare your environment:
  >
  >    1. Configure kubectl, the Kubernetes CLI, to work with your cluster:
  >
  >       ```bash theme={null}
  >       nebius mk8s cluster get-credentials \
  >         --id <cluster_ID> --external
  >       ```
  >
  >       For more details, see [How to connect to Managed Service for Kubernetes® clusters using kubectl](https://docs.nebius.com/kubernetes/connect.md).
  >
  >    2. Install [Helm](https://helm.sh/docs/), the package manager for Kubernetes that we will use to install the operator:
  >
  >       ```bash theme={null}
  >       curl -fsSL -o get_helm.sh \
  >         https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
  >       chmod 700 get_helm.sh
  >       ./get_helm.sh
  >       ```
  >
  >       For more ways to install, see the [Helm documentation](https://helm.sh/docs/intro/install/).
  >
  > 2. Install the NVIDIA Network Operator from the Nebius AI Cloud chart repository:
  >
  >    ```bash theme={null}
  >    helm install network-operator \
  >      oci://cr.eu-north1.nebius.cloud/marketplace/nebius/nvidia-network-operator/chart/network-operator \
  >      --version 25.7.0 \
  >      -n nvidia-network-operator --create-namespace \
  >      --wait
  >    ```
  >
  > 3. Verify that the NVIDIA Network Operator installed its components correctly. Get the `NICClusterPolicy` instance status:
  >
  >    ```bash theme={null}
  >    kubectl get nicclusterpolicy.mellanox.com nic-cluster-policy \
  >      -n nvidia-network-operator -o json | jq -r '.status'
  >    ```
  >
  >    The output example is the following:
  >
  >    ```json theme={null}
  >    {
  >      "appliedStates": [
  >        ...
  >        {
  >          "name": "state-OFED",
  >          "state": "ready"
  >        },
  >        ...
  >      ],
  >      "state": "ready"
  >    }
  >    ```
  >
  >    While `state-OFED` is `notReady`, you can check the driver installation logs:
  >
  >    ```bash theme={null}
  >    kubectl logs -n nvidia-network-operator \
  >      $(kubectl get pods -n nvidia-network-operator \
  >      | grep mofed | head -1 | awk '{print $1}')
  >    ```
  >
  > 4. Install the NVIDIA GPU Operator from the Nebius AI Cloud chart repository:
  >
  >    ```bash For NVIDIA B300 GPUs theme={null}
  >    helm install gpu-operator \
  >      oci://cr.eu-north1.nebius.cloud/marketplace/nebius/nvidia-gpu-operator/chart/gpu-operator \
  >      --version v25.10.0 \
  >      --set driver.version=580.95.05 \
  >      -n nvidia-gpu-operator \
  >      --create-namespace \
  >      --wait
  >    ```
  >
  >    ```bash For any other GPUs theme={null}
  >    helm install gpu-operator \
  >      oci://cr.eu-north1.nebius.cloud/marketplace/nebius/nvidia-gpu-operator/chart/gpu-operator \
  >      --version v25.10.0 \
  >      -n nvidia-gpu-operator \
  >      --create-namespace \
  >      --wait
  >    ```
  >
  >    [GPUDirect RDMA](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-operator-rdma.html) is enabled by default and uses the recommended DMA-BUF Linux kernel module.
  >
  >    For more command parameters, see the [NVIDIA GPU Operator documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html#common-chart-customization-options).
  >
  > 5. Verify that the GPU driver is installed correctly.
  >
  >    > [!WARNING]
  >    >
  >    > Do not check the GPU driver until you install both operators.
  >
  >    Get the last log line from each DaemonSet that installs the driver:
  >
  >    ```bash theme={null}
  >    for pod in $(kubectl get pods -n nvidia-gpu-operator \
  >        | grep nvidia-driver-daemonset | awk '{print $1}'); do
  >      echo -e "$pod:\n\t$(kubectl logs -n nvidia-gpu-operator $pod --tail 1)";
  >    done
  >    ```
  >
  >    If the last lines are `Done, now waiting for signal`, the driver should work correctly.

  > **Without InfiniBand: GPU operator**
  >
  > 1. Prepare your environment:
  >
  >    1. Configure kubectl, the Kubernetes CLI, to work with your cluster:
  >
  >       ```bash theme={null}
  >       nebius mk8s cluster get-credentials \
  >         --id <cluster_ID> --external
  >       ```
  >
  >       For more details, see [How to connect to Managed Service for Kubernetes® clusters using kubectl](https://docs.nebius.com/kubernetes/connect.md).
  >
  >    2. Install [Helm](https://helm.sh/docs/), the package manager for Kubernetes that we will use to install the operator:
  >
  >       ```bash theme={null}
  >       curl -fsSL -o get_helm.sh \
  >         https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
  >       chmod 700 get_helm.sh
  >       ./get_helm.sh
  >       ```
  >
  >       For more ways to install, see the [Helm documentation](https://helm.sh/docs/intro/install/).
  >
  > 2. Install the NVIDIA GPU Operator from the Nebius AI Cloud chart repository:
  >
  >    ```bash For NVIDIA B300 GPUs theme={null}
  >    helm install gpu-operator \
  >      oci://cr.eu-north1.nebius.cloud/marketplace/nebius/nvidia-gpu-operator/chart/gpu-operator \
  >      --version v25.10.0 \
  >      --set driver.version=580.95.05 \
  >      -n nvidia-gpu-operator --create-namespace \
  >      --wait
  >    ```
  >
  >    ```bash For any other GPUs theme={null}
  >    helm install gpu-operator \
  >      oci://cr.eu-north1.nebius.cloud/marketplace/nebius/nvidia-gpu-operator/chart/gpu-operator \
  >      --version v25.10.0 \
  >      -n nvidia-gpu-operator --create-namespace \
  >      --wait
  >    ```
  >
  >    For more options, see the [NVIDIA GPU Operator documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html#common-chart-customization-options).
  >
  > 3. Verify that the GPU driver is installed correctly.
  >
  >    Get the last log line from each DaemonSet that installs the driver:
  >
  >    ```bash theme={null}
  >    for pod in $(kubectl get pods -n nvidia-gpu-operator \
  >        | grep nvidia-driver-daemonset | awk '{print $1}'); do
  >      echo -e "$pod:\n\t$(kubectl logs -n nvidia-gpu-operator $pod --tail 1)";
  >    done
  >    ```
  >
  >    If the last lines are `Done, now waiting for signal`, the driver should work correctly.

## Example: Using CUDA for vector addition

To test CUDA support in the cluster with GPU nodes and drivers installed on them, you can run a small CUDA application, which adds two vectors together:

1. [Connect to the cluster using kubectl](https://docs.nebius.com/kubernetes/connect.md).
2. Follow instructions in the [NVIDIA GPU Operator documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html#cuda-vectoradd).

## See also

* [Dynamic Resource Allocation](https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation.md)
* [Interconnecting GPUs in a Managed Kubernetes cluster using InfiniBand](https://docs.nebius.com/kubernetes/gpu/clusters.md)
* [Tutorial: Running NCCL tests in a cluster with InfiniBand-connected GPUs](https://docs.nebius.com/kubernetes/gpu/nccl-test.md)
* [Creating and modifying node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md)

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
