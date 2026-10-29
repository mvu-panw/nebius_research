# Working with InfiniBand™ topology of a GPU cluster

Source: https://docs.nebius.com/compute/clusters/gpu/topology/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Working with InfiniBand™ topology of a GPU cluster

[InfiniBand™ topology](https://docs.nebius.com/compute/clusters/gpu/topology.md) can help you increase performance of multi-VM jobs in GPU clusters.

## Prerequisites

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to get InfiniBand™ topology of a GPU cluster

After you [create a GPU cluster and add VMs to it](https://docs.nebius.com/compute/clusters/gpu/index.md#how-to-enable-infiniband-for-vms-with-gpus), you can view the InfiniBand™ topology of this cluster and its VMs.

**Cluster topology**

To get the topology for all VMs in a GPU cluster:

**CLI**

Run the following command:

```bash theme={null}
nebius compute gpu-cluster get --id computegpucluster-***
```

In the `--id` parameter, specify the GPU cluster ID.

The output example is the following:

```text theme={null}
...
status:
  infiniband_topology_path:
    instances:
      - instance_id: computeinstance-***rnqz
        path:
          - ***27bf
          - ***bb9b
          - ***b7ad
      - instance_id: computeinstance-***pepp
        path:
          - ***27bf
          - ***bb9b
          - ***e1ff
      - ...
```

**Go SDK**

```go theme={null}
gpuCluster, err := sdk.Services().Compute().V1().
    GpuCluster().Get(
        ctx,
        &compute.GetGpuClusterRequest{
            Id: "computegpucluster-***",
        },
    )
if err != nil {
    return err
}
fmt.Println(gpuCluster)
```

In the code, specify the GPU cluster ID.

**Python SDK**

```python theme={null}
gpu_cluster_service = GpuClusterServiceClient(sdk)
gpu_cluster = await gpu_cluster_service.get(
    GetGpuClusterRequest(id="computegpucluster-***"),
)
print(gpu_cluster)
```

In the code, specify the GPU cluster ID.

**JavaScript SDK**

```ts theme={null}
const getGpuClusterService = new GpuClusterService(sdk);
const gpuCluster = await getGpuClusterService.get(
  GetGpuClusterRequest.create({
    id: "computegpucluster-***",
  }),
);
console.log(gpuCluster);
```

In the code, specify the GPU cluster ID.

**VM topology**

To get the topology for an individual VM:

**CLI**

Run the following command:

```bash theme={null}
nebius compute instance get --id computeinstance-***
```

In the `--id` parameter, specify the ID of the VM attached to the GPU cluster.

The output example is the following:

```text theme={null}
...
status:
  infiniband_topology_path:
    path:
      - ***27bf
      - ***bb9b
      - ***e1ff
```

**Go SDK**

```go theme={null}
instance, err := sdk.Services().Compute().V1().
    Instance().Get(
        ctx,
        &compute.GetInstanceRequest{
            Id: "computeinstance-***",
        },
    )
if err != nil {
    return err
}
fmt.Println(instance)
```

In the code, specify the ID of the VM attached to the GPU cluster.

**Python SDK**

```python theme={null}
instance_service = InstanceServiceClient(sdk)
instance = await instance_service.get(
    GetInstanceRequest(id="computeinstance-***"),
)
print(instance)
```

In the code, specify the ID of the VM attached to the GPU cluster.

**JavaScript SDK**

```ts theme={null}
const getInstanceService = new InstanceService(sdk);
const instance = await getInstanceService.get(
  GetInstanceRequest.create({
    id: "computeinstance-***",
  }),
);
console.log(instance);
```

In the code, specify the ID of the VM attached to the GPU cluster.

In the topology data, the `path` list shows components of the [InfiniBand™ network layers](https://docs.nebius.com/compute/clusters/gpu/topology.md#architecture-of-infiniband-topology):

```text theme={null}
***27bf # 1st network layer (InfiniBand™ fabric)
***bb9b # 2nd network layer (point of delivery, POD)
***e1ff # 3rd network layer (scalable unit, SU)
```

## How to create the Slurm topology configuration

To set up topology in [Slurm](https://slurm.schedmd.com) and run jobs for ML workloads, you need the [topology.conf](https://slurm.schedmd.com/topology.conf.html) file. This file shows the network hierarchy: how nodes are interconnected, what layers they are located at and what switches are used.

The `topology.conf` file represents InfiniBand™ topology. You can create this file based on the [information about a given GPU cluster](#how-to-get-infiniband-topology-of-a-gpu-cluster). To create the file, run one of the scripts from the [Nebius AI Cloud solution library](https://github.com/nebius/nebius-solution-library/tree/main/scripts/ib-topology) on GitHub.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
