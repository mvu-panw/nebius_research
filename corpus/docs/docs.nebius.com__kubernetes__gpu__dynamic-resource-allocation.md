# Dynamic resource allocation in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/gpu/dynamic-resource-allocation

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Dynamic resource allocation in Managed Service for Kubernetes®

Dynamic resource allocation (DRA) is a Kubernetes feature that lets workloads request specialized devices, such as GPUs and remote direct memory access (RDMA) network interfaces.

Without DRA, a GPU resource request specifies only a quantity, such as `nvidia.com/gpu: 1`. Kubernetes schedules the Pod on a node with enough available GPUs. With DRA, a workload can request devices from a DeviceClass and specify requirements for their properties and configuration. Kubernetes selects suitable devices, schedules the Pod on a node that can access them and asks the device driver to prepare them for the container.

Managed Service for Kubernetes supports DRA for two kinds of devices:

| Device | Driver | Provided by | DeviceClass |
| - | - | - | - |
| NVIDIA® GPU | NVIDIA® DRA driver (`gpu.nvidia.com`) | Installed and maintained by you | `gpu.nvidia.com` |
| RDMA or InfiniBand™ network interface | DRANet (`dra.net`) | Managed by Nebius | `rdma.networking.nebius.ai` or `ib.networking.nebius.ai` |

This guide explains how to enable DRA on a node group and use it to allocate resources to a workload.

> [!WARNING]
>
> Allocating a GPU claim and a network interface to the same Pod does not guarantee that the devices share a PCI root or the same non-uniform memory access (NUMA) node. If the workload requires that placement, validate it in the application.

## Prerequisites

1. [Create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) that runs Kubernetes 1.34 or later, or [upgrade](https://docs.nebius.com/kubernetes/manage-versions.md) an existing cluster. Kubernetes 1.34 is the first version in which the DRA API, `resource.k8s.io/v1`, is stable. For the versions available in Managed Kubernetes, see [Kubernetes versions](https://docs.nebius.com/kubernetes/versions.md).
2. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [connect to the cluster](https://docs.nebius.com/kubernetes/connect.md).
3. [Install jq](https://jqlang.github.io/jq/download/).
4. [Install Helm](https://helm.sh/docs/intro/install/).

## How to enable DRA on a node group

Enable DRA in the GPU settings of the node group. The legacy NVIDIA device plug-in and the NVIDIA DRA driver must not manage the same GPUs. This setting prepares the nodes for GPU DRA and disables the legacy plug-in on that group.

When you use a preinstalled NVIDIA driver, select a [driver preset](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components). Otherwise, install the NVIDIA GPU Operator and, for InfiniBand, the NVIDIA Network Operator. When installing GPU Operator, set `devicePlugin.enabled=false` so the Operator does not start the legacy plug-in. For the commands and installation order, see [How to install the drivers and components on existing node groups](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups).

Use one of the following:

* To create a node group, add the DRA settings in the [create request](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups):

  **CLI**

  Add `--template-gpu-settings-dra=true` to the create command:

  ```bash theme={null}
  nebius mk8s node-group create \
    --template-gpu-settings-dra=true \
    --template-gpu-settings-drivers-preset <driver_preset> \
    ...
  ```

  Set `<driver_preset>` when you use a preinstalled driver. Otherwise, omit `--template-gpu-settings-drivers-preset`.

  **Terraform**

  Add `dra = true` to `gpu_settings` in the [`nebius_mk8s_v1_node_group`](https://docs.nebius.com/terraform-provider/reference/resources/mk8s_v1_node_group) resource:

  ```hcl theme={null}
  resource "nebius_mk8s_v1_node_group" "<node_group_name>" {
      gpu_settings = {
        dra            = true
        drivers_preset = "<driver_preset>"
      }
    }
  }
  ```

  Set `<driver_preset>` when you use a preinstalled driver. Otherwise, omit `drivers_preset`.

  **Go SDK**

  In the create call, set `GpuSettings` to:

  ```go theme={null}
  GpuSettings: &mk8s.GpuSettings{
      Dra:           true,
      DriversPreset: "<driver_preset>",
  },
  ```

  Set `<driver_preset>` when you use a preinstalled driver. Otherwise, omit `DriversPreset`.

  **Python SDK**

  In the create call, set `gpu_settings` to:

  ```python theme={null}
  gpu_settings=GpuSettings(
      dra=True,
      drivers_preset="<driver_preset>",
  ),
  ```

  Set `<driver_preset>` when you use a preinstalled driver. Otherwise, omit `drivers_preset`.

  **JavaScript SDK**

  In the create call, set `gpuSettings` to:

  ```javascript theme={null}
  gpuSettings: GpuSettings.create({
    dra: true,
    driversPreset: "<driver_preset>",
  }),
  ```

  Set `<driver_preset>` when you use a preinstalled driver. Otherwise, omit `driversPreset`.

* To enable DRA on an existing node group, add the same settings when you [update the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-modify-node-groups).

  > [!WARNING]
  >
  > Enabling or disabling DRA on an existing node group recreates its nodes according to the group's [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#deployment-strategy-and-quotas).

After enabling DRA, proceed with one of the following:

* [Allocating a GPU](#allocating-a-gpu).
* [Allocating an RDMA or InfiniBand interface](#allocating-an-rdma-or-infiniband-interface).

## Allocating a GPU

Managed Kubernetes does not install the NVIDIA DRA driver. Install and maintain the driver yourself.

### Install the NVIDIA DRA driver

1. Add the NVIDIA chart repository:

   ```bash theme={null}
   helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
   helm repo update
   ```

2. Install the supported NVIDIA DRA driver version:

   ```bash theme={null}
   helm install nvidia-dra-driver-gpu nvidia/nvidia-dra-driver-gpu \
     --create-namespace \
     --namespace nvidia-dra-driver-gpu \
     --set gpuResourcesEnabledOverride=true \
     --wait
   ```

   For other chart values required by your node image, see the [NVIDIA DRA driver for GPUs documentation](https://github.com/NVIDIA/k8s-dra-driver-gpu).

### Check the NVIDIA DRA driver

1. Check that the driver Pods are ready:

   ```bash theme={null}
   kubectl get pods -n nvidia-dra-driver-gpu
   ```

   The output lists one controller Pod and one kubelet plugin Pod for each GPU node. All Pods are `Running`, with all containers ready:

   ```text theme={null}
   NAME                                     READY   STATUS    RESTARTS   AGE
   dra-driver-nvidia-gpu-controller-***     1/1     Running   0          4d21h
   dra-driver-nvidia-gpu-kubelet-plugin-*** 2/2     Running   0          4d21h
   dra-driver-nvidia-gpu-kubelet-plugin-*** 2/2     Running   0          4d21h
   dra-driver-nvidia-gpu-kubelet-plugin-*** 2/2     Running   0          4d21h
   ...
   ```

2. Check that the driver has created the GPU DeviceClass:

   ```bash theme={null}
   kubectl get deviceclass gpu.nvidia.com
   ```

   The expected output is:

   ```text theme={null}
   NAME             AGE
   gpu.nvidia.com   4d21h
   ```

3. Check that the driver has published the GPU inventory:

   ```bash theme={null}
   kubectl get resourceslices -o json |
     jq '[
       .items[]
       | select(.spec.driver == "gpu.nvidia.com")
       | {node: .spec.nodeName, devices: [.spec.devices[].name]}
     ]'
   ```

   The output lists every target GPU node with its GPUs, for example:

   ```json theme={null}
   [
     {
       "node": "computeinstance-e00***",
       "devices": [
         "gpu-3",
         "gpu-2",
         "gpu-1",
         "gpu-0"
       ]
     },
     {
       "node": "computeinstance-e00***",
       "devices": [
         "gpu-3",
         "gpu-2",
         "gpu-1",
         "gpu-0"
       ]
     }
   ]
   ```

### Request a GPU

1. Save the following manifest as `gpu-workload.yaml`.

   Replace `<tested_cuda_image>` with a container image that includes `nvidia-smi`. The Pod command runs `nvidia-smi` to confirm the GPU. For example, `nvidia/cuda:13.1.1-runtime-ubuntu24.04`.

   ```yaml theme={null}
   apiVersion: resource.k8s.io/v1
   kind: ResourceClaimTemplate
   metadata:
     name: gpu
   spec:
     spec:
       devices:
         requests:
           - name: gpu
             exactly:
               deviceClassName: gpu.nvidia.com
               count: 1
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: gpu-workload
   spec:
     restartPolicy: Never
     resourceClaims:
       - name: gpu
         resourceClaimTemplateName: gpu
     containers:
       - name: workload
         image: <tested_cuda_image>
         command: ["sh", "-c", "nvidia-smi && sleep infinity"]
         resources:
           claims:
             - name: gpu
   ```

2. Create the ResourceClaimTemplate and Pod:

   ```bash theme={null}
   kubectl apply -f gpu-workload.yaml
   ```

3. Wait until the Pod is running:

   ```bash theme={null}
   kubectl get pod gpu-workload --watch
   ```

4. Check that the GPU is visible in the container:

   ```bash theme={null}
   kubectl exec gpu-workload -- nvidia-smi
   ```

   The output lists one allocated GPU.

## Allocating an RDMA or InfiniBand interface

### How managed DRANet works

When you enable DRA on a node group in a [GPU cluster](https://docs.nebius.com/kubernetes/gpu/clusters.md), Managed Kubernetes installs and maintains the DRANet driver for you. You don't need to install it yourself. Managed Kubernetes:

* Runs the `dranet` DaemonSet in the `kube-system` namespace on nodes labeled `nebius.com/dranet-rdma-capable=true`.
* Discovers the RDMA-capable network interfaces on those nodes.
* Publishes the discovered interfaces to Kubernetes as ResourceSlices.
* Provides DeviceClasses that workloads can use to request an RDMA or InfiniBand interface.

### Check managed DRANet

1. Check that the `dranet` DaemonSet is running:

   ```bash theme={null}
   kubectl get ds -A | grep -E 'NAMESPACE|dranet'
   ```

   The expected output is:

   ```text theme={null}
   NAMESPACE     NAME     DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                         AGE
   kube-system   dranet   <nodes>   <nodes>   <nodes>  <nodes>      <nodes>     nebius.com/dranet-rdma-capable=true   <age>
   ```

   The DaemonSet is in the `kube-system` namespace. The ready count matches the number of eligible nodes, and the node selector is `nebius.com/dranet-rdma-capable=true`.

2. Check that Managed Kubernetes has created the network DeviceClasses:

   ```bash theme={null}
   kubectl get deviceclass rdma.networking.nebius.ai ib.networking.nebius.ai -o name
   ```

   The expected output is:

   ```text theme={null}
   deviceclass.resource.k8s.io/rdma.networking.nebius.ai
   deviceclass.resource.k8s.io/ib.networking.nebius.ai
   ```

   The DeviceClasses select the following interfaces:

   | DeviceClass | Interface selected |
   | - | - |
   | `rdma.networking.nebius.ai` | Any RDMA-capable interface |
   | `ib.networking.nebius.ai` | An InfiniBand interface |

3. Check that DRANet has published the network-device inventory:

   ```bash theme={null}
   kubectl get resourceslices -o json |
     jq '[
       .items[]
       | select(.spec.driver == "dra.net")
       | {node: .spec.nodeName, devices: [.spec.devices[] | {name, attributes}]}
     ]'
   ```

   Each device lists its name and attributes. Confirm that the interface is RDMA-capable.

> [!NOTE]
>
> Don't request both `rdma.networking.nebius.ai` and `ib.networking.nebius.ai` when the workload needs only one network device. Kubernetes treats them as independent device requests and allocates two separate devices.

Choose one DeviceClass based on the workload requirements:

* Use `ib.networking.nebius.ai` when the workload specifically requires an InfiniBand interface. InfiniBand interfaces are RDMA-capable, so you don't need an additional request for `rdma.networking.nebius.ai`.
* Use `rdma.networking.nebius.ai` when the workload can use any RDMA-capable interface, including either InfiniBand or Ethernet-based RDMA.

Request both only when the workload requires two separate network devices.

### Request an InfiniBand interface

The following example requests one interface from the `ib.networking.nebius.ai` DeviceClass. To request any RDMA-capable interface instead, use `rdma.networking.nebius.ai`.

1. Save the following manifest as `ib-workload.yaml`.

   Replace `<container_image_with_rdma_tools>` with a container image that includes the RDMA user-space tools you use to test the allocated interface.

   ```yaml theme={null}
   apiVersion: resource.k8s.io/v1
   kind: ResourceClaimTemplate
   metadata:
     name: ib-network
   spec:
     spec:
       devices:
         requests:
           - name: ib
             exactly:
               deviceClassName: ib.networking.nebius.ai
               count: 1
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: rdma-workload
   spec:
     restartPolicy: Never
     resourceClaims:
       - name: network
         resourceClaimTemplateName: ib-network
     containers:
       - name: workload
         image: <container_image_with_rdma_tools>
         command: ["sleep", "infinity"]
         resources:
           claims:
             - name: network
   ```

   `count` specifies the number of interfaces to allocate. It does not change the bandwidth of an individual interface. If you omit `count`, the default is 1.

2. Create the ResourceClaimTemplate and the Pod:

   ```bash theme={null}
   kubectl apply -f ib-workload.yaml
   ```

3. Wait until the Pod is running:

   ```bash theme={null}
   kubectl get pod rdma-workload --watch
   ```

### Verify the network allocation

1. Get the generated claim name from the Pod:

   ```bash theme={null}
   kubectl get pod rdma-workload -o jsonpath='{.status.resourceClaimStatuses}'
   ```

2. Inspect the generated ResourceClaim. Replace `<claim_name>` with the name from the previous command:

   ```bash theme={null}
   kubectl get resourceclaim <claim_name> -o yaml
   ```

   In `status.allocation.devices.results`, the allocation contains the DRANet driver, device pool and allocated device:

   ```yaml theme={null}
   status:
     allocation:
       devices:
         results:
           - request: ib
             driver: dra.net
             pool: <pool_name>
             device: <device_name>
   ```

3. Check that the allocated interface is visible inside the container:

   ```bash theme={null}
   kubectl exec rdma-workload -- ls /sys/class/net
   ```

   In addition to the default interfaces, the output contains the allocated interface:

   ```text theme={null}
   eth0
   lo
   <allocated_interface>
   ```

4. Check that the RDMA devices are visible to the container:

   ```bash theme={null}
   kubectl exec rdma-workload -- ls /sys/class/infiniband
   ```

   The output contains the associated RDMA device, for example:

   ```text theme={null}
   mlx5_0
   ```

A ResourceClaim allocation and an interface visible in the container confirm that Kubernetes has passed the interface to the Pod. They don't show that RDMA traffic works. Test connectivity and throughput with the application's network test.

## See also

* [Working with GPUs](https://docs.nebius.com/kubernetes/gpu/set-up.md)
* [Interconnecting GPUs with InfiniBand](https://docs.nebius.com/kubernetes/gpu/clusters.md)
* [Dynamic Resource Allocation](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) in the Kubernetes documentation, including DeviceClasses and ResourceClaims

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
