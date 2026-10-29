# Running NCCL tests in a Managed Service for Kubernetes® cluster with InfiniBand™-connected GPUs

Source: https://docs.nebius.com/kubernetes/gpu/nccl-test

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running NCCL tests in a Managed Service for Kubernetes® cluster with InfiniBand™-connected GPUs

To boost performance of the high-performance computing (HPC) and AI workloads that you run in a Managed Service for Kubernetes cluster, you can set it up so that the GPUs on its nodes are interconnected directly using InfiniBand.

In this tutorial, you will create a Managed Service for Kubernetes cluster with GPUs interconnected using InfiniBand, install operators and drivers from NVIDIA on it, and run NVIDIA NCCL tests to check InfiniBand performance.

## Costs

The tutorial includes the following chargeable resources:

* [Compute virtual machines with GPUs](https://docs.nebius.com/compute/resources/pricing.md)
* [Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/resources/pricing.md)

## Prerequisites

1. Set up the interface that you are going to use:

   **CLI**

   [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   **Go SDK**

   1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
   2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

      You will use the CLI to generate a kubeconfig file for kubectl.

   **Python SDK**

   1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
   2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

      You will use the CLI to generate a kubeconfig file for kubectl.

   **JavaScript SDK**

   1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
   2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

      You will use the CLI to generate a kubeconfig file for kubectl.

2. Get the IDs of the default subnet and the `k8s-node-group-sa` default service account:

   **CLI**

   ```bash theme={null}
   export SUBNET_ID=$(nebius vpc subnet list \
     --format jsonpath='{.items[0].metadata.id}')
   export SA_ID=$(nebius iam service-account get-by-name \
     --name k8s-node-group-sa \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   subnets, err := sdk.Services().VPC().V1().
       Subnet().List(ctx, &vpc.ListSubnetsRequest{})
   if err != nil {
       return err
   }
   if len(subnets.GetItems()) == 0 {
       return errors.New("no subnets found")
   }
   subnetID := subnets.GetItems()[0].GetMetadata().GetId()
   serviceAccount, err := sdk.Services().IAM().V1().
       ServiceAccount().GetByName(
           ctx,
           &iam.GetServiceAccountByNameRequest{
               Name: "k8s-node-group-sa",
           },
       )
   if err != nil {
       return err
   }
   saID := serviceAccount.GetMetadata().GetId()
   if saID == "" {
       return errors.New("service account ID is missing")
   }
   ```

   The code saves the IDs to the `subnetID` and `saID` variables.

   **Python SDK**

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnets = await subnet_service.list(ListSubnetsRequest())
   if not subnets.items:
       raise ValueError("no subnets found")
   subnet_id = subnets.items[0].metadata.id
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(name="k8s-node-group-sa"),
   )
   sa_id = service_account.metadata.id
   if not sa_id:
       raise ValueError("service account ID is missing")
   ```

   The code saves the IDs to the `subnet_id` and `sa_id` variables.

   **JavaScript SDK**

   ```ts theme={null}
   const subnetService = new SubnetService(sdk);
   const subnets = await subnetService.list(
     ListSubnetsRequest.create({}),
   );
   const subnetId = subnets.items[0]?.metadata?.id;
   if (!subnetId) {
     throw new Error("no subnets found");
   }
   const serviceAccountService = new ServiceAccountService(sdk);
   const serviceAccount = await serviceAccountService.getByName(
     GetServiceAccountByNameRequest.create({
       name: "k8s-node-group-sa",
     }),
   );
   const saId = serviceAccount.metadata?.id;
   if (!saId) {
     throw new Error("service account ID is missing");
   }
   ```

   The code saves the IDs to the `subnetId` and `saId` variables.

3. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [Helm](https://helm.sh/docs/intro/install/).

## Steps

### Set up a Managed Service for Kubernetes cluster with GPUs and InfiniBand

1. Create a GPU cluster:

   **CLI**

   ```bash theme={null}
   export GPU_CLUSTER_ID=$(nebius compute gpu-cluster create \
     --name k8s-gpus --infiniband-fabric fabric-3 \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   gpuClusterOperation, err := sdk.Services().Compute().V1().
       GpuCluster().Create(
           ctx,
           &compute.CreateGpuClusterRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "k8s-gpus",
               },
               Spec: &compute.GpuClusterSpec{
                   InfinibandFabric: "fabric-3",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = gpuClusterOperation.Wait(ctx); err != nil {
       return err
   }
   gpuClusterID := gpuClusterOperation.ResourceID()
   if gpuClusterID == "" {
       return fmt.Errorf("GPU cluster ID is missing")
   }
   ```

   **Python SDK**

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   gpu_cluster_operation = await gpu_cluster_service.create(
       CreateGpuClusterRequest(
           metadata=ResourceMetadata(name="k8s-gpus"),
           spec=GpuClusterSpec(infiniband_fabric="fabric-3"),
       ),
   )
   await gpu_cluster_operation.wait()
   gpu_cluster_id = gpu_cluster_operation.resource_id
   if not gpu_cluster_id:
       raise ValueError("GPU cluster ID is missing")
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const gpuClusterService = new GpuClusterService(sdk);
   const gpuClusterOperation = await gpuClusterService.create(
     CreateGpuClusterRequest.create({
       metadata: ResourceMetadata.create({
         name: "k8s-gpus",
       }),
       spec: GpuClusterSpec.create({
         infinibandFabric: "fabric-3",
       }),
     }),
   ).result;
   await gpuClusterOperation.wait();
   const gpuClusterId = gpuClusterOperation.resourceId();
   if (!gpuClusterId) {
     throw new Error("GPU cluster ID is missing");
   }
   ```

2. Create a Managed Service for Kubernetes cluster with a public endpoint:

   **CLI**

   ```bash theme={null}
   export MK8S_CLUSTER_ID=$(nebius mk8s cluster create \
     --name nccl \
     --control-plane-version 1.36 \
     --control-plane-endpoints-public-endpoint=true \
     --control-plane-subnet-id $SUBNET_ID \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   clusterOperation, err := sdk.Services().MK8S().V1().
       Cluster().Create(
           ctx,
           &mk8s.CreateClusterRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "nccl",
               },
               Spec: &mk8s.ClusterSpec{
                   ControlPlane: &mk8s.ControlPlaneSpec{
                       Version: "1.36",
                       SubnetId: subnetID,
                       Endpoints: &mk8s.ControlPlaneEndpointsSpec{
                           PublicEndpoint: &mk8s.PublicEndpointSpec{},
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = clusterOperation.Wait(ctx); err != nil {
       return err
   }
   mk8sClusterID := clusterOperation.ResourceID()
   if mk8sClusterID == "" {
       return fmt.Errorf("cluster ID is missing")
   }
   ```

   **Python SDK**

   ```python theme={null}
   cluster_service = ClusterServiceClient(sdk)
   cluster_operation = await cluster_service.create(
       CreateClusterRequest(
           metadata=ResourceMetadata(name="nccl"),
           spec=ClusterSpec(
               control_plane=ControlPlaneSpec(
                   version="1.36",
                   subnet_id=subnet_id,
                   endpoints=ControlPlaneEndpointsSpec(
                       public_endpoint=PublicEndpointSpec(),
                   ),
               ),
           ),
       ),
   )
   await cluster_operation.wait()
   mk8s_cluster_id = cluster_operation.resource_id
   if not mk8s_cluster_id:
       raise ValueError("cluster ID is missing")
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const clusterService = new ClusterService(sdk);
   const clusterOperation = await clusterService.create(
     CreateClusterRequest.create({
       metadata: ResourceMetadata.create({
         name: "nccl",
       }),
       spec: ClusterSpec.create({
         controlPlane: ControlPlaneSpec.create({
           version: "1.36",
           subnetId,
           endpoints: ControlPlaneEndpointsSpec.create({
             publicEndpoint: PublicEndpointSpec.create({}),
           }),
         }),
       }),
     }),
   ).result;
   await clusterOperation.wait();
   const mk8sClusterId = clusterOperation.resourceId();
   if (!mk8sClusterId) {
     throw new Error("cluster ID is missing");
   }
   ```

3. Create a node group in the cluster:

   **CLI**

   ```bash theme={null}
   nebius mk8s node-group create \
     --name nccl-gpu-nodes \
     --parent-id $MK8S_CLUSTER_ID \
     --fixed-node-count 2 \
     --template-service-account-id $SA_ID \
     --template-resources-platform "gpu-h100-sxm" \
     --template-resources-preset "8gpu-128vcpu-1600gb" \
     --template-boot-disk-type network_ssd \
     --template-boot-disk-size-bytes 137438953472 \
     --template-gpu-settings-drivers-preset cuda13.0 \
     --template-gpu-cluster-id $GPU_CLUSTER_ID
   ```

   **Go SDK**

   ```go theme={null}
   nodeGroupOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Create(
           ctx,
           &mk8s.CreateNodeGroupRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: mk8sClusterID,
                   Name:     "nccl-gpu-nodes",
               },
               Spec: &mk8s.NodeGroupSpec{
                   Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                       FixedNodeCount: 2,
                   },
                   Template: &mk8s.NodeTemplate{
                       ServiceAccountId: saID,
                       Resources: &mk8s.ResourcesSpec{
                           Platform: "gpu-h100-sxm",
                           Size: &mk8s.ResourcesSpec_Preset{
                               Preset: "8gpu-128vcpu-1600gb",
                           },
                       },
                       BootDisk: &mk8s.DiskSpec{
                           Size: &mk8s.DiskSpec_SizeBytes{
                               SizeBytes: 137438953472,
                           },
                           Type: mk8s.DiskSpec_NETWORK_SSD,
                       },
                       GpuSettings: &mk8s.GpuSettings{
                           DriversPreset: "cuda13.0",
                       },
                       GpuCluster: &mk8s.GpuClusterSpec{
                           Id: gpuClusterID,
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
   ```

   **Python SDK**

   ```python theme={null}
   node_group_service = NodeGroupServiceClient(sdk)
   node_group_operation = await node_group_service.create(
       CreateNodeGroupRequest(
           metadata=ResourceMetadata(
               parent_id=mk8s_cluster_id,
               name="nccl-gpu-nodes",
           ),
           spec=NodeGroupSpec(
               fixed_node_count=2,
               template=NodeTemplate(
                   service_account_id=sa_id,
                   resources=ResourcesSpec(
                       platform="gpu-h100-sxm",
                       preset="8gpu-128vcpu-1600gb",
                   ),
                   boot_disk=DiskSpec(
                       size_bytes=137438953472,
                       type=DiskSpec__DiskType.NETWORK_SSD,
                   ),
                   gpu_settings=GpuSettings(drivers_preset="cuda13.0"),
                   gpu_cluster=GpuClusterSpec(id=gpu_cluster_id),
               ),
           ),
       ),
   )
   await node_group_operation.wait()
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const nodeGroupService = new NodeGroupService(sdk);
   const nodeGroupOperation = await nodeGroupService.create(
     CreateNodeGroupRequest.create({
       metadata: ResourceMetadata.create({
         parentId: mk8sClusterId,
         name: "nccl-gpu-nodes",
       }),
       spec: NodeGroupSpec.create({
         size: {
           $case: "fixedNodeCount",
           fixedNodeCount: 2,
         },
         template: NodeTemplate.create({
           serviceAccountId: saId,
           resources: ResourcesSpec.create({
             platform: "gpu-h100-sxm",
             size: {
               $case: "preset",
               preset: "8gpu-128vcpu-1600gb",
             },
           }),
           bootDisk: DiskSpec.create({
             size: {
               $case: "sizeBytes",
               sizeBytes: 137438953472,
             },
             type: DiskSpec_DiskType.NETWORK_SSD,
           }),
           gpuSettings: GpuSettings.create({
             driversPreset: "cuda13.0",
           }),
           gpuCluster: GpuClusterSpec.create({
             id: gpuClusterId,
           }),
         }),
       }),
     }),
   ).result;
   await nodeGroupOperation.wait();
   ```

   For this tutorial, it is required that:

   * The node group has the GPU cluster specified.

   * The node group includes at least two nodes.

   * The nodes use a [VM platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md) compatible with GPU clusters:

     | Platform | Presets | [Regions](https://docs.nebius.com/overview/regions.md) |
     | - | - | - |
     | NVIDIA® B300 NVLink with Intel Granite Rapids  (`gpu-b300-sxm`) | `8gpu-192vcpu-2768gb` | `uk-south1`, `eu-west2`, `us-north1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm`) | `8gpu-160vcpu-1792gb` | `us-central1` |
     | NVIDIA® B200 NVLink with Intel Emerald Rapids  (`gpu-b200-sxm-a`) | `8gpu-160vcpu-1792gb` | `me-west1` |
     | NVIDIA® H200 NVLink with Intel Sapphire Rapids  (`gpu-h200-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1`, `eu-north2`*\**, `eu-west1`, `us-central1` |
     | NVIDIA® H100 NVLink with Intel Sapphire Rapids  (`gpu-h100-sxm`) | `8gpu-128vcpu-1600gb` | `eu-north1` |

     In this example, the nodes use the `gpu-h100-sxm` VM platform with the `8gpu-128vcpu-1600gb` preset.

   * The nodes use a boot disk image offered by Managed Kubernetes that contains drivers and other components for GPUs. Without this image, you need to install the drivers and components manually. For more details, see [GPU drivers and other components](https://docs.nebius.com/kubernetes/gpu/set-up.md#gpu-drivers-and-other-components).

4. Generate a kubeconfig file with the cluster details for kubectl. This step uses the CLI regardless of the interface that you used to create the cluster.

   If you created the cluster with an SDK, first save the returned cluster ID to the `MK8S_CLUSTER_ID` environment variable:

   ```bash theme={null}
   export MK8S_CLUSTER_ID=<cluster_ID>
   ```

   Then, generate the file:

   ```bash theme={null}
   nebius mk8s cluster get-credentials \
     --id $MK8S_CLUSTER_ID --external
   ```

   To verify that kubectl is connected to the cluster, you can run `kubectl cluster-info`.

### Run the NCCL tests

1. Install the [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/trainer/legacy-v1/overview/) (also known as Kubeflow Trainer).

   ```bash theme={null}
   kubectl apply --server-side -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.9.3"
   ```

2. Create a namespace for the tests, named `nccl-test` in this tutorial:

   ```
   kubectl create ns nccl-test
   ```

3. Create `nccl-test.yaml` with an `MPIJob` for your tests.

   > [!NOTE]
   >
   > This example is for 2 nodes. If you [created a node group](#set-up-a-managed-service-for-kubernetes-cluster-with-gpus-and-infiniband) with a different number of nodes, change accordingly the `mpirun` command in `.spec.mpiReplicaSpecs.Launcher.template.spec.containers[0].args` and the number of workers in `.spec.mpiReplicaSpecs.Worker.replicas`.

   > **nccl-test.yaml — NVIDIA B200 GPUs**
   >
   > ```yaml theme={null}
   > apiVersion: kubeflow.org/v1
   > kind: MPIJob
   > metadata:
   >   name: nccl-test-nebius
   > spec:
   >   slotsPerWorker: 8 # Number of GPUs on each node
   >   mpiReplicaSpecs:
   >     Launcher:
   >       replicas: 1
   >       template:
   >         spec:
   >           containers:
   >           - args:
   >             # In `-np 16`, 16 is the total number of GPUs on all nodes
   >             # (`.spec.slotsPerWorker` × `.spec.mpiReplicaSpecs.Worker.replicas`)
   >             - 'mpirun -np 16 -bind-to none -x LD_LIBRARY_PATH
   >               -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=eth0
   >               -mca coll ^hcoll
   >               -x UCX_NET_DEVICES=eth0
   >               -x NCCL_IB_HCA=mlx5
   >               -x SHARP_COLL_ENABLE_PCI_RELAXED_ORDERING=1
   >               -x NCCL_COLLNET_ENABLE=0
   >               /opt/nccl_tests/build/all_reduce_perf -b 512M -e 8G -f 2 -g 1'
   >             command:
   >             - /bin/bash
   >             - -c
   >             env:
   >             - name: OMPI_ALLOW_RUN_AS_ROOT
   >               value: "1"
   >             - name: OMPI_ALLOW_RUN_AS_ROOT_CONFIRM
   >               value: "1"
   >             image: cr.eu-north1.nebius.cloud/nebius-benchmarks/nccl-tests:2.26.5-ubu22.04-cu12.8
   >             name: nccl
   >             resources:
   >               requests:
   >                 cpu: 2
   >                 memory: 1208Mi
   >             securityContext:
   >               privileged: true
   >           initContainers:
   >           - command:
   >             - sh
   >             - -c
   >             - ulimit -Hl unlimited && ulimit -Sl unlimited
   >             image: busybox:1.27.2
   >             name: init-limit
   >             securityContext:
   >               privileged: true
   >     Worker:
   >       replicas: 2 # Number of nodes
   >       template:
   >         spec:
   >           automountServiceAccountToken: false
   >           containers:
   >           - image: cr.eu-north1.nebius.cloud/nebius-benchmarks/nccl-tests:2.26.5-ubu22.04-cu12.8
   >             name: nccl
   >             resources:
   >               # If you have other applications running in your cluster,
   >               # adjust the `cpu` and `memory` values according to
   >               # the resources available on the nodes
   >               limits:
   >                 cpu: 96
   >                 memory: 1600G
   >                 nvidia.com/gpu: 8
   >               requests:
   >                 cpu: 96
   >                 memory: 1600G
   >                 nvidia.com/gpu: 8
   >             securityContext:
   >               privileged: true
   >             volumeMounts:
   >             - mountPath: /dev/shm
   >               name: dshm
   >           enableServiceLinks: false
   >           initContainers:
   >           - command:
   >             - sh
   >             - -c
   >             - ulimit -Hl unlimited && ulimit -Sl unlimited
   >             image: busybox:1.27.2
   >             name: init-limit
   >             securityContext:
   >               privileged: true
   >           volumes:
   >           - emptyDir:
   >               medium: Memory
   >             name: dshm
   >   runPolicy:
   >     cleanPodPolicy: Running
   > ```

   > **nccl-test.yaml — NVIDIA H200 or H100 GPUs**
   >
   > ```yaml theme={null}
   > apiVersion: kubeflow.org/v1
   > kind: MPIJob
   > metadata:
   >   name: nccl-test-nebius
   > spec:
   >   slotsPerWorker: 8 # Number of GPUs on each node
   >   mpiReplicaSpecs:
   >     Launcher:
   >       replicas: 1
   >       template:
   >         spec:
   >           containers:
   >           - args:
   >             # In `-np 16`, 16 is the total number of GPUs on all nodes
   >             # (`.spec.slotsPerWorker` × `.spec.mpiReplicaSpecs.Worker.replicas`)
   >             - 'mpirun -np 16 -bind-to none -x LD_LIBRARY_PATH
   >               -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=eth0
   >               -x NCCL_IB_HCA=mlx5
   >               -x UCX_NET_DEVICES=eth0
   >               -x SHARP_COLL_ENABLE_PCI_RELAXED_ORDERING=1
   >               -x NCCL_COLLNET_ENABLE=0
   >               /opt/nccl_tests/build/all_reduce_perf -b 512M -e 8G -f 2 -g 1'
   >             command:
   >             - /bin/bash
   >             - -c
   >             env:
   >             - name: OMPI_ALLOW_RUN_AS_ROOT
   >               value: "1"
   >             - name: OMPI_ALLOW_RUN_AS_ROOT_CONFIRM
   >               value: "1"
   >             image: cr.eu-north1.nebius.cloud/nebius-benchmarks/nccl-tests:2.23.4-ubu22.04-cu12.4
   >             name: nccl
   >             resources:
   >               requests:
   >                 cpu: 2
   >                 memory: 1208Mi
   >             securityContext:
   >               privileged: true
   >           initContainers:
   >           - command:
   >             - sh
   >             - -c
   >             - ulimit -Hl unlimited && ulimit -Sl unlimited
   >             image: busybox:1.27.2
   >             name: init-limit
   >             securityContext:
   >               privileged: true
   >     Worker:
   >       replicas: 2 # Number of nodes
   >       template:
   >         spec:
   >           automountServiceAccountToken: false
   >           containers:
   >           - image: cr.eu-north1.nebius.cloud/nebius-benchmarks/nccl-tests:2.23.4-ubu22.04-cu12.4
   >             name: nccl
   >             resources:
   >               # If you have other applications running in your cluster,
   >               # adjust the `cpu` and `memory` values according to
   >               # the resources available on the nodes
   >               limits:
   >                 cpu: 96
   >                 memory: 1600G
   >                 nvidia.com/gpu: 8
   >               requests:
   >                 cpu: 96
   >                 memory: 1600G
   >                 nvidia.com/gpu: 8
   >             securityContext:
   >               privileged: true
   >             volumeMounts:
   >             - mountPath: /dev/shm
   >               name: dshm
   >           enableServiceLinks: false
   >           initContainers:
   >           - command:
   >             - sh
   >             - -c
   >             - ulimit -Hl unlimited && ulimit -Sl unlimited
   >             image: busybox:1.27.2
   >             name: init-limit
   >             securityContext:
   >               privileged: true
   >           volumes:
   >           - emptyDir:
   >               medium: Memory
   >             name: dshm
   >   runPolicy:
   >     cleanPodPolicy: Running
   > ```

4. Deploy the `MPIJob` in `nccl-test`:

   ```text theme={null}
   kubectl apply -f nccl-test.yaml -n nccl-test
   ```

5. Check that the test Pods are running:

   ```bash theme={null}
   kubectl get pods -w -n nccl-test
   ```

   Wait until all the Pods are running, like this:

   ```text theme={null}
   NAME                        READY   STATUS    RESTARTS   AGE
   nccl-test-nebius-launcher   1/1     Running   0          24s
   nccl-test-nebius-worker-0   1/1     Running   0          24s
   nccl-test-nebius-worker-1   1/1     Running   0          24s
   ```

6. Check the test logs:

   ```bash theme={null}
   kubectl logs -f nccl-test-nebius-launcher -n nccl-test \
     | grep -v "NCCL INFO"
   ```

   In the result, check the average bus bandwidth. If its value is higher than 300 GB/sec, the connection is stable.

   Example:

   ```
   ...
   #                                                              out-of-place                       in-place
   #       size         count      type   redop    root     time   algbw   busbw #wrong     time   algbw   busbw #wrong
   #        (B)    (elements)                               (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)
      536870912     134217728     float     sum      -1   3674.4  146.11  283.09      0   3648.4  147.15  285.11      0
     1073741824     268435456     float     sum      -1   6411.6  167.47  324.47      0   6416.7  167.33  324.21      0
     2147483648     536870912     float     sum      -1    12735  168.62  326.71      0    12979  165.45  320.57      0
     4294967296    1073741824     float     sum      -1    25389  169.17  327.76      0    25598  167.79  325.09      0
     8589934592    2147483648     float     sum      -1    50979  168.50  326.47      0    50799  169.10  327.63      0
   # Out of bounds values : 0 OK
   # Avg bus bandwidth    : 317.11
   ```

   The average bus bandwidth is not equal to the InfiniBand one as some of the NCCL operations it measures use NVLink. Nevertheless, it accurately estimates the connection.

   To stop streaming logs, press **Ctrl** + **C**.

7. Delete the `MPIJob`.

   ```text theme={null}
   kubectl delete -f nccl-test.yaml -n nccl-test
   ```

   > [!NOTE]
   >
   > You should delete the `MPIJob` even if you want to run another test. In this case, redeploy the `MPIJob` as described in steps 2–3.

## How to delete the created resources

Some of the created resources are chargeable. If you do not need them, delete these resources, so Nebius AI Cloud does not charge for them:

* Delete the installed operator:

  ```bash theme={null}
  kubectl delete -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.9.3"
  ```

* Delete the node group with GPUs:

  **CLI**

  ```bash theme={null}
  export MK8S_CLUSTER_ID=$(nebius mk8s cluster get-by-name \
    --name nccl --format jsonpath='{.metadata.id}')
  nebius mk8s node-group delete --id \
    $(nebius mk8s node-group get-by-name \
    --name nccl-gpu-nodes --parent-id $MK8S_CLUSTER_ID \
    --format jsonpath='{.metadata.id}')
  ```

  **Go SDK**

  ```go theme={null}
  cluster, err := sdk.Services().MK8S().V1().
      Cluster().GetByName(
          ctx,
          &common.GetByNameRequest{Name: "nccl"},
      )
  if err != nil {
      return err
  }
  clusterID := cluster.GetMetadata().GetId()
  if clusterID == "" {
      return errors.New("cluster ID is missing")
  }
  nodeGroup, err := sdk.Services().MK8S().V1().
      NodeGroup().GetByName(
          ctx,
          &common.GetByNameRequest{
              ParentId: clusterID,
              Name:     "nccl-gpu-nodes",
          },
      )
  if err != nil {
      return err
  }
  nodeGroupID := nodeGroup.GetMetadata().GetId()
  if nodeGroupID == "" {
      return errors.New("node group ID is missing")
  }
  deleteOperation, err := sdk.Services().MK8S().V1().
      NodeGroup().Delete(
          ctx,
          &mk8s.DeleteNodeGroupRequest{Id: nodeGroupID},
      )
  if err != nil {
      return err
  }
  if _, err = deleteOperation.Wait(ctx); err != nil {
      return err
  }
  ```

  **Python SDK**

  ```python theme={null}
  cluster_service = ClusterServiceClient(sdk)
  cluster = await cluster_service.get_by_name(
      GetByNameRequest(name="nccl"),
  )
  cluster_id = cluster.metadata.id
  node_group_service = NodeGroupServiceClient(sdk)
  node_group = await node_group_service.get_by_name(
      GetByNameRequest(
          parent_id=cluster_id,
          name="nccl-gpu-nodes",
      ),
  )
  node_group_operation = await node_group_service.delete(
      DeleteNodeGroupRequest(id=node_group.metadata.id),
  )
  await node_group_operation.wait()
  ```

  **JavaScript SDK**

  ```ts theme={null}
  const clusterService = new ClusterService(sdk);
  const cluster = await clusterService.getByName(
    GetByNameRequest.create({
      name: "nccl",
    }),
  );
  const clusterId = cluster.metadata?.id;
  if (!clusterId) {
    throw new Error("cluster ID is missing");
  }
  const nodeGroupService = new NodeGroupService(sdk);
  const nodeGroup = await nodeGroupService.getByName(
    GetByNameRequest.create({
      parentId: clusterId,
      name: "nccl-gpu-nodes",
    }),
  );
  const nodeGroupId = nodeGroup.metadata?.id;
  if (!nodeGroupId) {
    throw new Error("node group ID is missing");
  }
  const deleteOperation = await nodeGroupService.delete(
    DeleteNodeGroupRequest.create({
      id: nodeGroupId,
    }),
  ).result;
  await deleteOperation.wait();
  ```

* Delete the entire cluster:

  **CLI**

  ```bash theme={null}
  nebius mk8s cluster delete --id \
    $(nebius mk8s cluster get-by-name \
    --name nccl --format jsonpath='{.metadata.id}')
  ```

  **Go SDK**

  ```go theme={null}
  clusterToDelete, err := sdk.Services().MK8S().V1().
      Cluster().GetByName(
          ctx,
          &common.GetByNameRequest{Name: "nccl"},
      )
  if err != nil {
      return err
  }
  clusterToDeleteID := clusterToDelete.GetMetadata().GetId()
  if clusterToDeleteID == "" {
      return errors.New("cluster ID is missing")
  }
  deleteClusterOperation, err := sdk.Services().MK8S().V1().
      Cluster().Delete(
          ctx,
          &mk8s.DeleteClusterRequest{Id: clusterToDeleteID},
      )
  if err != nil {
      return err
  }
  if _, err = deleteClusterOperation.Wait(ctx); err != nil {
      return err
  }
  ```

  **Python SDK**

  ```python theme={null}
  delete_cluster_service = ClusterServiceClient(sdk)
  cluster_to_delete = await delete_cluster_service.get_by_name(
      GetByNameRequest(name="nccl"),
  )
  cluster_operation = await delete_cluster_service.delete(
      DeleteClusterRequest(id=cluster_to_delete.metadata.id),
  )
  await cluster_operation.wait()
  ```

  **JavaScript SDK**

  ```ts theme={null}
  const deleteClusterService = new ClusterService(sdk);
  const clusterToDelete = await deleteClusterService.getByName(
    GetByNameRequest.create({
      name: "nccl",
    }),
  );
  const clusterToDeleteId = clusterToDelete.metadata?.id;
  if (!clusterToDeleteId) {
    throw new Error("cluster ID is missing");
  }
  const deleteClusterOperation = await deleteClusterService.delete(
    DeleteClusterRequest.create({
      id: clusterToDeleteId,
    }),
  ).result;
  await deleteClusterOperation.wait();
  ```

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
