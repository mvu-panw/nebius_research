# InfiniBand™ topology of a GPU cluster

Source: https://docs.nebius.com/compute/clusters/gpu/topology

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# InfiniBand™ topology of a GPU cluster

## Why InfiniBand topology is important

Workload managers like [Slurm](https://slurm.schedmd.com) and [Volcano](https://volcano.sh/en/docs/) allow you to specify the network topology of your virtual machines within a GPU cluster for *topology-aware job scheduling*. Topology files describe how the VMs are located relative to each other. When you provide a topology file to a workload manager, it schedules distributed jobs on the worker nodes that are topologically closest to each other. This reduces network latency in such jobs and leads to better performance in both real workloads and synthetic tests.

> For example, the [AllReduce](https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md#allreduce) tests from the [NCCL Tests suite](https://github.com/NVIDIA/nccl-tests) that we ran in Nebius AI Cloud as topology-aware jobs have shown performance gains of up to 20%, depending on cluster size, compared to the same tests without the topology provided.

## Architecture of InfiniBand topology

Every virtual machine with GPUs is connected to a set of three nodes related to a particular [InfiniBand fabric](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics). Every node is located on a separate network layer. The hierarchy of an InfiniBand network includes the following layers with different types of switches:

1. InfiniBand fabric layer. Contains a root switch.
2. Point of delivery (POD). Represents a set of racks with servers. Core switches interconnect PODs.
3. Scalable unit (SU). Consists of a set of servers. Leaf switches interconnect scalable units.

![image](https://mintcdn.com/nebius-ai-cloud/1Ha0sWR6e1mnIaHS/_assets/compute/infiniband-topology.svg?fit=max\&auto=format\&n=1Ha0sWR6e1mnIaHS\&q=85\&s=7102c09389941e8bfbd15e9ead1ec842)

## Cost of network communication

The cost of network communication increases as you go to a higher layer. For example, if you need to transfer data from one POD to another, the data goes through a root switch. This leads to a higher cost of resources. Mutual connections between PODs or SUs do not influence the cost.

If a connection or data exchange takes place within one entity (POD or SU), the cost of network communication does not change.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
