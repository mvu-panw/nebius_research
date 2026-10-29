# Topology-aware scheduling for GPU workloads in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/gpu/topology-aware-scheduling

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Topology-aware scheduling for GPU workloads in Managed Service for Kubernetes®

Modern AI/ML workloads depend heavily on high-throughput, low-latency communication between nodes. In GPU clusters connected via InfiniBand™, the physical network topology has a direct impact on performance.

Topology-aware scheduling (TAS) enables Kubernetes schedulers to optimize workload placement based on how nodes are physically connected within the InfiniBand fabric.

With this feature, Nebius AI Cloud exposes InfiniBand topology information as *node labels*, allowing schedulers to place workloads on nodes that are closer in the network hierarchy. This can improve communication efficiency and provide performance gains for distributed workloads.

For more information about Kubernetes scheduling, see the [Kubernetes scheduler documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/).

## Prerequisites

1. [Create a Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) and [attach at least one GPU node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) to it.
2. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).
3. [Connect to the cluster by using kubectl](https://docs.nebius.com/kubernetes/connect.md).

## How to view topology labels in your cluster

View the topology labels on GPU nodes with the following command:

```bash theme={null}
kubectl get nodes -L topology.nebius.com/gpu-cluster-id,topology.nebius.com/tier-2,topology.nebius.com/tier-1,kubernetes.io/hostname
```

The following labels can be present on GPU nodes:

| Label | Description |
| - | - |
| `topology.nebius.com/gpu-cluster-id` | Identifies a connected high-speed network domain. Nodes with the same value have high-speed network connectivity between each other. |
| `topology.nebius.com/tier-0` | The closest topology level. For example, this can represent a direct accelerator interconnect, such as multi-node NVLink between NVIDIA GPUs. This label is set only for nodes that support this type of communication. |
| `topology.nebius.com/tier-1` | A lower-level network locality domain. For example, this can represent rack-level switches that connect nodes in one or more racks into a single block. |
| `topology.nebius.com/tier-2` | A wider network locality domain. For example, this can represent spine-level switches that connect multiple blocks inside a data center. |

The lower the tier level shared by two nodes, the better the expected communication performance between them. For example, two nodes with the same `topology.nebius.com/tier-1` value are expected to be closer to each other than two nodes that only share the same `topology.nebius.com/tier-2` value.

### Example output

```text theme={null}
NAME                                 STATUS   ROLES    AGE    VERSION   GPU-CLUSTER-ID                         TIER-2                             TIER-1                             HOSTNAME
computeinstance-e00f4wsk77x4vsr58s   Ready    <none>   144d   v1.32.9   computegpucluster-e00agxzkvne8558nv8   959d125cbd887219574193fdba27b2c8   282cfcbf8e735653e4ce9884052cb523   computeinstance-e00f4wsk77x4vsr58s
computeinstance-e00nm33x3y9597zzxj   Ready    <none>   54d    v1.32.9                                                                                                                computeinstance-e00nm33x3y9597zzxj
computeinstance-e00tw5jypq4zvfrsrx   Ready    <none>   77d    v1.32.9   computegpucluster-e00z7ftxx6dacdbra5   5ca19afc3d62844695b08033aeba635b   297bbb6a0db40d875c266b589dc95f5b   computeinstance-e00tw5jypq4zvfrsrx
computeinstance-e00v7g42bam61yqzp3   Ready    <none>   144d   v1.32.9   computegpucluster-e00agxzkvne8558nv8   959d125cbd887219574193fdba27b2c8   04011d5d2b17ec74672df94efbbeeb15   computeinstance-e00v7g42bam61yqzp3
```

Nodes that share the same value for a label belong to the same *topology domain* at that level. A topology domain is a group of nodes that are physically close to each other in the network hierarchy and are therefore expected to have faster communication between them. For example, in the sample output:

* `computeinstance-e00f4wsk77x4vsr58s` and `computeinstance-e00v7g42bam61yqzp3` share the same `GPU-CLUSTER-ID` and `TIER-2` values, which means they belong to the same high-speed network domain and the same wider network locality domain. These nodes have different `TIER-1` values, which indicates that they belong to different lower-level locality domains.
* `computeinstance-e00tw5jypq4zvfrsrx` belongs to a different GPU cluster and topology hierarchy because all of its topology label values are different.
* `computeinstance-e00nm33x3y9597zzxj` does not have topology labels. This usually means that the node is not attached to a GPU cluster, or TAS is not enabled.

The exact physical meaning of each tier depends on the infrastructure configuration and is not guaranteed to match these examples.

## How to enable topology-aware scheduling

[Kueue](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/) is used below as an example scheduler. You can also use other schedulers that support TAS, such as [Volcano](https://volcano.sh/en/docs/network_topology_aware_scheduling/).

### Steps

#### Install and configure Kueue

1. [Install Kueue](https://kueue.sigs.k8s.io/docs/getting-started/installation/#install-a-released-version).

2. Enable TAS:

   ```bash theme={null}
   kubectl -n kueue-system patch deployment kueue-controller-manager \
    --type json \
    -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--feature-gates=TopologyAwareScheduling=true"}]'
   ```

3. Create a file named `kueue-tas.yaml` to configure the Kueue resources:

   ```yaml theme={null}
   apiVersion: kueue.x-k8s.io/v1beta2
   kind: Topology
   metadata:
     name: ib-topology
   spec:
     levels:
       - nodeLabel: "topology.nebius.com/gpu-cluster-id"
       - nodeLabel: "topology.nebius.com/tier-2"
       - nodeLabel: "topology.nebius.com/tier-1"
       - nodeLabel: "kubernetes.io/hostname"
   ---
   apiVersion: kueue.x-k8s.io/v1beta2
   kind: ResourceFlavor
   metadata:
     name: gpu-flavor-tas
   spec:
     nodeLabels:
       nebius.com/node-group-id: "<node_group_ID>"
     topologyName: "ib-topology"
     tolerations:
       - key: "nvidia.com/gpu"
         operator: "Exists"
         effect: "NoSchedule"
   ---
   apiVersion: kueue.x-k8s.io/v1beta2
   kind: ClusterQueue
   metadata:
     name: gpu-cluster-queue-tas
   spec:
     namespaceSelector: {}
     resourceGroups:
       - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
         flavors:
           - name: "gpu-flavor-tas"
             resources:
               - name: "cpu"
                 nominalQuota: 100
               - name: "memory"
                 nominalQuota: "100Gi"
               - name: "nvidia.com/gpu"
                 nominalQuota: "16"
   ---
   apiVersion: kueue.x-k8s.io/v1beta2
   kind: LocalQueue
   metadata:
     name: gpu-user-queue-tas
     namespace: default
   spec:
     clusterQueue: gpu-cluster-queue-tas
   ```

   To get the `<node_group_ID>`, open your Kubernetes cluster in the web console, go to the **Node groups** tab and copy the node group ID.

4. Apply the configuration:

   ```bash theme={null}
   kubectl apply -f kueue-tas.yaml
   ```

5. Check that the Kueue resources were created:

   ```bash theme={null}
   kubectl get topology,resourceflavor,clusterqueue,localqueue
   ```

#### Schedule workloads with TAS using Kueue

To request TAS, add a topology annotation to the Pod template of your workload.

1. Create a file named `job-tas.yaml` that requests TAS for the workload:

   ```yaml theme={null}
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: job-tas
     namespace: default
     labels:
       kueue.x-k8s.io/queue-name: gpu-user-queue-tas
   spec:
     parallelism: <number_of_replicas>
     completions: <number_of_replicas>
     completionMode: Indexed
     template:
       metadata:
         annotations:
           <annotations_string>
       spec:
         containers:
         - name: dummy-job
           image: registry.k8s.io/e2e-test-images/agnhost:2.53
           args: ["pause"]
           resources:
             requests:
               cpu: "100m"
               memory: "100Mi"
               nvidia.com/gpu: 8
             limits:
               nvidia.com/gpu: 8
         restartPolicy: Never
   ```

   Replace the following variables:

   * `<number_of_replicas>`: Number of Pods that are running in parallel.
   * `<annotations_string>`: Requested topology constraint. See the following table for available values:

     | Scenario | Description | Value of `<annotations_string>` |
     | - | - | - |
     | Required to run within a GPU cluster | Kueue admits the workload only if enough resources are available within the same GPU cluster. Otherwise, the workload remains pending until resources become available or the topology constraint changes. | `kueue.x-k8s.io/podset-required-topology: "topology.nebius.com/gpu-cluster-id"` |
     | Required to run within a topology domain | Kueue admits the workload only if enough resources are available within the same topology domain. Otherwise, the workload remains pending until resources become available or the topology constraint changes. | `kueue.x-k8s.io/podset-required-topology: "topology.nebius.com/tier-2"` |
     | Preferred to run within a topology domain | Kueue tries to schedule Pods within the same topology domain. If this is not possible, Kueue can place Pods across multiple topology domains. | `kueue.x-k8s.io/podset-preferred-topology: "topology.nebius.com/tier-2"` |

     In Kueue, a *podset* represents a group of Pods belonging to the same workload (for example, replicas of a Job).

2. Create the Job:

   ```bash theme={null}
   kubectl apply -f job-tas.yaml
   ```

3. Check admission status:

   ```bash theme={null}
   kubectl get workloads -A
   kubectl describe workload <workload_name> -n <namespace>
   ```

   If Kueue does not admit the workload, reduce parallelism, use less restrictive topology constraints or increase available GPU capacity.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
