# How to create and modify Managed Service for Kubernetes® clusters

Source: https://docs.nebius.com/kubernetes/clusters/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create and modify Managed Service for Kubernetes® clusters

Managed Service for Kubernetes clusters manage and run containerized applications, providing automatic scaling, load balancing and streamlined deployment and management. In this guide, you will learn how to create, modify and delete clusters in Managed Service for Kubernetes.

For more information on managing node groups and adding them to clusters, see [Creating and modifying Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md).

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

## How to create clusters

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.

2. Click  **Create cluster**.

3. On the **Cluster** step, configure the cluster:

   1. In the **General** section:

      * Enter the cluster name.
      * (Optional) Enter labels in the `key:value` format.

   2. In the **Network** section, review the network and subnet. They are selected by default.

   3. In the **Control plane** section:

      * The Kubernetes version is set by default. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
      * A public endpoint is allocated by default. As a result, the cluster is available from the internet, you can connect to it from any machine. If you want to prevent access to the cluster from the internet, disable the public endpoint option. Then, you can connect to the cluster only from a virtual machine (VM) located in the same subnet as the cluster.

        > [!TIP]
        >
        > To only allow certain addresses to connect to the cluster, enable the public endpoint and [configure an allowlist of IP addresses](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md) for the cluster.

   4. (Optional) In the **Observability** section, enable **Audit logs** to record metadata about operations that modify the cluster. For details, see [Logs in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/logs.md).

   5. Click **Next**.

4. On the **Node groups** step, optionally configure one or more node groups.

   You can create a cluster without node groups and add them later. For more information, see [Creating and modifying Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md).

   To add a node group during cluster creation:

   1. Click **Add node group**.

   2. Configure the node group. If you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), the **Reservations** step is also shown between **General** and **Compute resources**.

      1. On the **General** step:

         * Enter the node group name.

         * (Optional) Enable **Assign public IPv4 addresses** if you want the nodes to be accessible from the internet.

         * Under **Size**:

           * (Optional) Enable **Autoscaling** if you want to let the node group scale up or down depending on the workload.
           * Specify the initial **Number of nodes**.

         * Under **Advanced**:

           * **Auto-repair** is enabled by default. When enabled, Managed Kubernetes automatically replaces unhealthy nodes.
           * (Optional) Specify **Max pods per node** to limit how many Pods can run on each node in the group.

      2. If the **Reservations** step is shown, select **Reservation usage**:

         * **With reservations**: Resources are allocated from reservations ([capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md)). This ensures that resources are always available, even if VMs in the node group are stopped (for example, by you or a [maintenance event](https://docs.nebius.com/kubernetes/maintenance/index.md)).

           In the **Reservation** section, you can configure the following options:

           * **Any (existing and future)** (default): Compute selects among your matching capacity block groups automatically.
           * **Specific capacity block groups**: Select one or more capacity block groups. Each option shows the capacity block group ID, reservation period and GPU usage. Make sure the selected groups have enough capacity and do not expire soon.
           * **Switch to PAYG**: Choose whether the VM can start after you create or restart it without active intervals in selected capacity block groups:

             * **When reservation is exhausted** (default): The VM can start as a pay-as-you-go VM when no capacity is available in the selected capacity block groups.
             * **Never**: The VM cannot start without available capacity in the selected capacity block groups.

             This does not affect the VM when it is running. If an interval in a selected capacity block group expires while the VM is running, the VM always continues as a pay-as-you-go VM, regardless of this setting.

           If you have capacity block groups in multiple regions, select a **Region** first.

         * **Without reservations**: Resources are allocated from a common pool, and no reservations are used for the node group.

      3. On the **Compute resources** step:

         * Select whether the node group should have GPUs.

         * Select a regular or preemptible VM type.

           VMs without GPUs only support the regular type. For information about preemptible node groups, see [Creating and modifying Managed Service for Kubernetes® node groups — Preemptible node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md#preemptible-node-groups).

         * If you create the node group with reservations, specify a **Reservation ID**.

         * Select an available [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md) (a combination of GPUs, vCPUs and RAM) that fits your workload requirements.

         * (Optional) If you create a node group with 8 GPUs (for example, for training models), use a GPU cluster for the node group. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. To use a GPU cluster, select an existing one or click  **Create** in the **GPU cluster** field and specify the cluster name and InfiniBand fabric. To select the fabric, see [InfiniBand fabrics](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics).

         * (Optional) Enable or disable **GPU settings**. They are enabled by default, and they allow Managed Kubernetes to pre-install NVIDIA drivers and the [Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html). You can also select a specific NVIDIA CUDA driver version.

         * Select an operating system for the nodes (for example, `Ubuntu 24.04 LTS`).

      4. On the **Storage** step, select the disk type and specify the size in GiB. Supported [disk types](https://docs.nebius.com/compute/storage/types.md#disk-types) are **SSD**, **SSD NRD** and **SSD IO**.

         (Optional) To attach a shared filesystem, click  **Attach shared filesystem**, select an existing filesystem or create a new one, and specify a mount tag.

      5. On the **Additional** step:

         * (Optional) In the **Username and SSH key** field, add credentials, so you can [connect to the node group](https://docs.nebius.com/compute/virtual-machines/connect.md):

           1. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).
           2. In the **Username and SSH key** field, select an existing key or click  **Create** to add a new one.

         * (Optional) Select or create a [service account](https://docs.nebius.com/iam/overview.md) that will perform actions on behalf of the nodes.

   3. To add another node group with a different configuration, click **Add node group**.

   4. To remove a node group, click  →  **Delete** next to its name.

   5. Click **Next**.

5. (Optional) On the **Applications** step, select applications to deploy to the cluster. Each application requires at least one node group. For more information, see [Deploying and deleting applications for Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/manage-applications.md).

   1. Click **Next**.

6. On the **Review** step, check the cluster configuration and click **Create cluster**.

**CLI**

Create a cluster:

```bash theme={null}
nebius mk8s cluster create \
  --name <cluster_name> \
  --labels <key1=value1,key2=value2,...> \
  --control-plane-endpoints-public-endpoint=<true|false> \
  --control-plane-endpoints-public-endpoint-allowed-cidrs <allowed_CIDR_blocks> \
  --control-plane-version 1.36 \
  --control-plane-subnet-id <subnet_ID> \
  --control-plane-etcd-cluster-size <number_of_etcd_stores>
```

The command contains the following parameters:

* `--name`: The cluster name.
* `--labels`: Labels in the `key=value` format.

- `--control-plane-endpoints-public-endpoint`: Enables a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

  If you want to limit access to the cluster, set the parameter to `false`. Then, users can connect to the cluster only from a virtual machine in the same subnet.

- `--control-plane-endpoints-public-endpoint-allowed-cidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

  Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`.

  Pass each CIDR block as a separate `--control-plane-endpoints-public-endpoint-allowed-cidrs` parameter.

  For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

* `--control-plane-version`: The Kubernetes version. The default and recommended version is 1.36. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
* `--control-plane-subnet-id`: The [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
* `--control-plane-etcd-cluster-size`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). If you do not specify the number, the cluster is created with three etcd stores. This ensures high availability and makes the cluster more reliable; data stored in etcd is accessible even in case of failures.

  You can specify a lower number. However, the enabled high availability does not affect the cost of the cluster.

**Terraform**

1. Create the following configuration file:

   ```hcl theme={null}
   resource "nebius_mk8s_v1_cluster" "<cluster_name>" {
     name = "<cluster_name>"
     parent_id = "<project_ID>"
     labels = {
       <key1> = "<value1>"
       <key2> = "<value2>"
       ...
       <keyN> = "<valueN>"
     }
     control_plane = {
       endpoints = {
         public_endpoint = {}
       }
       version           = "1.36"
       subnet_id         = "<subnet_ID>"
       etcd_cluster_size = <number_of_etcd_stores>
     }
   }
   ```

   The file contains the following parameters:

   * `name`: The cluster name.
   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `labels`: Labels in the `key=value` format.
   * `control_plane`: Settings of the cluster's [control plane](https://docs.nebius.com/kubernetes/components.md#control-plane-components):

     * `endpoints.public_endpoint`: Its value `{}` enables a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

       If you want to limit access to the cluster, delete the parameter. Then, users can connect to the cluster only from a virtual machine in the same subnet.
     * `version`: The Kubernetes version. The default and recommended version is 1.36. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
     * `subnet-id`: The [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
     * `etcd_cluster_size`: Number or [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). If you do not specify the number, the cluster is created with three etcd stores. This ensures high availability and makes the cluster more reliable; data stored in etcd is accessible even in case of failures.

       You can specify a lower number. However, the enabled high availability does not affect the cost of the cluster.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a cluster:

```go theme={null}
var endpoints *mk8s.ControlPlaneEndpointsSpec
if <true|false> {
    endpoints = &mk8s.ControlPlaneEndpointsSpec{
        PublicEndpoint: &mk8s.PublicEndpointSpec{
            AllowedCidrs: strings.Split("<allowed_CIDR_blocks>", ","),
        },
    }
}
createOperation, err := sdk.Services().MK8S().V1().
    Cluster().Create(
        ctx,
        &mk8s.CreateClusterRequest{
            Metadata: &common.ResourceMetadata{
                Name:   "<cluster_name>",
                Labels: map[string]string{"key1": "value1", "key2": "value2"},
            },
            Spec: &mk8s.ClusterSpec{
                ControlPlane: &mk8s.ControlPlaneSpec{
                    Version:          "1.36",
                    SubnetId:         "<subnet_ID>",
                    Endpoints:        endpoints,
                    EtcdClusterSize:  <number_of_etcd_stores>,
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = createOperation.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameters:

* `<true|false>`: Set to `true` to create a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

  If you want to limit access to the cluster, set it to `false`. Then, the cluster gets no public endpoint and users can connect to it only from a virtual machine in the same subnet.

* `PublicEndpoint.AllowedCidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

  Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`. The example splits a comma-separated string, so pass multiple blocks as `192.168.0.0/24,8.8.8.64/26`.

  For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

- `Metadata.Name`: The cluster name.
- `Metadata.Labels`: Labels in the `key: value` format.
- `Spec.ControlPlane.Version`: The Kubernetes version. The default and recommended version is 1.36. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
- `Spec.ControlPlane.SubnetId`: The [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
- `EtcdClusterSize`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). If you do not specify the number, the cluster is created with three etcd stores. This ensures high availability and makes the cluster more reliable; data stored in etcd is accessible even in case of failures.

  You can specify a lower number. However, the enabled high availability doesn't affect the cost of the cluster.

**Python SDK**

Create a cluster:

```python theme={null}
endpoints = None
if <True|False>:
    endpoints = ControlPlaneEndpointsSpec(
        public_endpoint=PublicEndpointSpec(
            allowed_cidrs="<allowed_CIDR_blocks>".split(","),
        ),
    )
cluster_service = ClusterServiceClient(sdk)
create_operation = await cluster_service.create(
    CreateClusterRequest(
        metadata=ResourceMetadata(
            name="<cluster_name>",
            labels={"key1": "value1", "key2": "value2"},
        ),
        spec=ClusterSpec(
            control_plane=ControlPlaneSpec(
                version="1.36",
                subnet_id="<subnet_ID>",
                endpoints=endpoints,
                etcd_cluster_size=<number_of_etcd_stores>,
            ),
        ),
    ),
)
await create_operation.wait()
```

The code contains the following parameters:

* `<True|False>`: Set to `True` to create a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

  If you want to limit access to the cluster, set it to `False`. Then, the cluster gets no public endpoint and users can connect to it only from a virtual machine in the same subnet.

* `public_endpoint.allowed_cidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

  Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`. The example splits a comma-separated string, so pass multiple blocks as `192.168.0.0/24,8.8.8.64/26`.

  For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

- `metadata.name`: The cluster name.
- `metadata.labels`: Labels in the `key: value` format.
- `spec.control_plane.version`: The Kubernetes version. The default and recommended version is 1.36. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
- `spec.control_plane.subnet_id`: The [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
- `etcd_cluster_size`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). If you don't specify the number, the cluster is created with three etcd stores. This ensures high availability and makes the cluster more reliable; data stored in etcd is accessible even in case of failures.

  You can specify a lower number. However, the enabled high availability doesn't affect the cost of the cluster.

**JavaScript SDK**

Create a cluster:

```ts theme={null}
let endpoints;
if (<true|false>) {
  endpoints = ControlPlaneEndpointsSpec.create({
    publicEndpoint: PublicEndpointSpec.create({
      allowedCidrs: "<allowed_CIDR_blocks>".split(","),
    }),
  });
}
const clusterService = new ClusterService(sdk);
const createOperation = await clusterService.create(
  CreateClusterRequest.create({
    metadata: ResourceMetadata.create({
      name: "<cluster_name>",
      labels: {"key1": "value1", "key2": "value2"},
    }),
    spec: ClusterSpec.create({
      controlPlane: ControlPlaneSpec.create({
        version: "1.36",
        subnetId: "<subnet_ID>",
        endpoints,
        etcdClusterSize: <number_of_etcd_stores>,
      }),
    }),
  }),
).result;
await createOperation.wait();
```

The code contains the following parameters:

* `<true|false>`: Set to `true` to create a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

  If you want to limit access to the cluster, set it to `false`. Then, the cluster gets no public endpoint and users can connect to it only from a virtual machine in the same subnet.

* `publicEndpoint.allowedCidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

  Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`. The example splits a comma-separated string, so pass multiple blocks as `192.168.0.0/24,8.8.8.64/26`.

  For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

- `metadata.name`: The cluster name.
- `metadata.labels`: Labels in the `key: value` format.
- `spec.controlPlane.version`: The Kubernetes version. The default and recommended version is 1.36. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
- `spec.controlPlane.subnetId`: The [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
- `etcdClusterSize`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). If you do not specify the number, the cluster is created with three etcd stores. This ensures high availability and makes the cluster more reliable; data stored in etcd is accessible even in case of failures.

  You can specify a lower number. However, the enabled high availability doesn't affect the cost of the cluster.

## How to modify clusters

**CLI**

1. Get the ID of the cluster via its name:

   ```bash theme={null}
   export K8S_CLUSTER_ID=$(nebius mk8s cluster get-by-name \
     --name <cluster_name> --format jsonpath='{.metadata.id}')
   ```

   Alternatively, you can use the listing command: `nebius mk8s cluster list`.

2. Update the cluster settings:

   ```bash theme={null}
   nebius mk8s cluster update \
     --id $K8S_CLUSTER_ID \
     --labels <key1=value1,key2=value2,...> \
     --control-plane-endpoints-public-endpoint=<true|false> \
     --control-plane-endpoints-public-endpoint-allowed-cidrs <allowed_CIDR_blocks> \
     --control-plane-etcd-cluster-size <number_of_etcd_stores>
   ```

   The command contains the following parameters:

   * `--labels`: Labels in the `key=value` format.

   - `--control-plane-endpoints-public-endpoint`: Enables a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

     If you want to limit access to the cluster, set the parameter to `false`. Then, users can connect to the cluster only from a virtual machine in the same subnet.

   - `--control-plane-endpoints-public-endpoint-allowed-cidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

     Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`.

     Pass each CIDR block as a separate `--control-plane-endpoints-public-endpoint-allowed-cidrs` parameter.

     For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

   * `--control-plane-etcd-cluster-size`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). Three of them ensure high availability of the cluster.

   Only the parameters from the command above can be changed. To perform a full cluster update, add `--full` to the command. This will update all parameters with the default values or the values specified in the `--full` command.

**Terraform**

1. Modify the manifest with the deployed infrastructure:

   ```hcl theme={null}
   resource "nebius_mk8s_v1_cluster" "<cluster_name>" {
     name = "<cluster_name>"
     labels = {
       <key1> = "<value1>"
       <key2> = "<value2>"
       ...
       <keyN> = "<valueN>"
     }
     control_plane = {
       endpoints = {
         public_endpoint = {}
       }
       etcd_cluster_size = <number_of_etcd_stores>
     }
   }
   ```

   You can change the following parameters:

   * `name`: The cluster name.
   * `labels`: Labels in the `key=value` format.
   * `control_plane`: Settings of the cluster's [control plane](https://docs.nebius.com/kubernetes/components.md#control-plane-components):

     * `endpoints.public_endpoint`: Its value `{}` enables a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

       If you want to limit access to the cluster, delete the parameter. Then, users can connect to the cluster only from a virtual machine in the same subnet.
     * `etcd_cluster_size`: Number or [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). If you do not specify the number, the cluster is created with three etcd stores. This ensures high availability and makes the cluster more reliable; data stored in etcd is accessible even in case of failures.

       You can specify a lower number. However, the enabled high availability does not affect the cost of the cluster.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the cluster via its name:

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

2. Update the cluster settings:

   ```go theme={null}
   clusterToUpdate, err := sdk.Services().MK8S().V1().
       Cluster().Get(
           ctx,
           &mk8s.GetClusterRequest{
               Id: "<cluster_ID>",
           },
       )
   if err != nil {
       return err
   }
   if clusterToUpdate.GetMetadata() == nil {
       return fmt.Errorf("cluster metadata is missing")
   }
   clusterToUpdateSpec := clusterToUpdate.GetSpec()
   if clusterToUpdateSpec == nil ||
       clusterToUpdateSpec.GetControlPlane() == nil {
       return fmt.Errorf("cluster control plane spec is missing")
   }
   clusterToUpdate.Metadata.Labels = map[string]string{"key1": "value1", "key2": "value2"}
   updateEndpoints := (*mk8s.ControlPlaneEndpointsSpec)(nil)
   if <true|false> {
       updateEndpoints = &mk8s.ControlPlaneEndpointsSpec{
           PublicEndpoint: &mk8s.PublicEndpointSpec{
               AllowedCidrs: strings.Split("<allowed_CIDR_blocks>", ","),
           },
       }
   }
   clusterToUpdateSpec.ControlPlane.Endpoints = updateEndpoints
   clusterToUpdateSpec.ControlPlane.EtcdClusterSize = <number_of_etcd_stores>
   updateOperation, err := sdk.Services().MK8S().V1().
       Cluster().Update(
           ctx,
           &mk8s.UpdateClusterRequest{
               Metadata: clusterToUpdate.GetMetadata(),
               Spec:     clusterToUpdateSpec,
           },
       )
   if err != nil {
       return err
   }
   if _, err = updateOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   The code contains the following parameters:

   * `Metadata.Labels`: Labels in the `key: value` format.

   - `<true|false>`: Set to `true` to create a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

     If you want to limit access to the cluster, set it to `false`. Then, the cluster gets no public endpoint and users can connect to it only from a virtual machine in the same subnet.

   - `PublicEndpoint.AllowedCidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

     Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`. The example splits a comma-separated string, so pass multiple blocks as `192.168.0.0/24,8.8.8.64/26`.

     For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

   * `Spec.ControlPlane.EtcdClusterSize`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). Three of them ensure high availability of the cluster.

**Python SDK**

1. Get the ID of the cluster via its name:

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

2. Update the cluster settings:

   ```python theme={null}
   update_cluster_service = ClusterServiceClient(sdk)
   cluster_to_update = await update_cluster_service.get(
       GetClusterRequest(id="<cluster_ID>"),
   )
   if cluster_to_update.metadata is None:
       raise ValueError("cluster metadata is missing")
   if cluster_to_update.spec is None:
       raise ValueError("cluster spec is missing")
   if cluster_to_update.spec.control_plane is None:
       raise ValueError("cluster control plane spec is missing")
   cluster_to_update.metadata.labels = {"key1": "value1", "key2": "value2"}
   cluster_to_update.spec.control_plane.endpoints = None
   if <True|False>:
       cluster_to_update.spec.control_plane.endpoints = (
           ControlPlaneEndpointsSpec(
               public_endpoint=PublicEndpointSpec(
                   allowed_cidrs="<allowed_CIDR_blocks>".split(","),
               ),
           )
       )
   cluster_to_update.spec.control_plane.etcd_cluster_size = (
       <number_of_etcd_stores>
   )
   update_operation = await update_cluster_service.update(
       UpdateClusterRequest(
           metadata=cluster_to_update.metadata,
           spec=cluster_to_update.spec,
       ),
   )
   await update_operation.wait()
   ```

   The code contains the following parameters:

   * `metadata.labels`: Labels in the `key: value` format.

   - `<True|False>`: Set to `True` to create a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

     If you want to limit access to the cluster, set it to `False`. Then, the cluster gets no public endpoint and users can connect to it only from a virtual machine in the same subnet.

   - `public_endpoint.allowed_cidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

     Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`. The example splits a comma-separated string, so pass multiple blocks as `192.168.0.0/24,8.8.8.64/26`.

     For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

   * `spec.control_plane.etcd_cluster_size`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). Three of them ensure high availability of the cluster.

**JavaScript SDK**

1. Get the ID of the cluster via its name:

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

2. Update the cluster settings:

   ```ts theme={null}
   const updateClusterService = new ClusterService(sdk);
   const clusterToUpdate = await updateClusterService.get(
     GetClusterRequest.create({
       id: "<cluster_ID>",
     }),
   );
   if (!clusterToUpdate.metadata) {
     throw new Error("cluster metadata is missing");
   }
   if (!clusterToUpdate.spec?.controlPlane) {
     throw new Error("cluster control plane spec is missing");
   }
   clusterToUpdate.metadata.labels = {"key1": "value1", "key2": "value2"};
   clusterToUpdate.spec.controlPlane.endpoints = undefined;
   if (<true|false>) {
     clusterToUpdate.spec.controlPlane.endpoints =
       ControlPlaneEndpointsSpec.create({
         publicEndpoint: PublicEndpointSpec.create({
           allowedCidrs: "<allowed_CIDR_blocks>".split(","),
         }),
       });
   }
   clusterToUpdate.spec.controlPlane.etcdClusterSize =
     <number_of_etcd_stores>;
   const updateOperation = await updateClusterService.update(
     UpdateClusterRequest.create({
       metadata: clusterToUpdate.metadata,
       spec: clusterToUpdate.spec,
     }),
   ).result;
   await updateOperation.wait();
   ```

   The code contains the following parameters:

   * `metadata.labels`: Labels in the `key: value` format.

   - `<true|false>`: Set to `true` to create a public endpoint. As a result, the cluster is available from the internet, and you can connect to it from any machine.

     If you want to limit access to the cluster, set it to `false`. Then, the cluster gets no public endpoint and users can connect to it only from a virtual machine in the same subnet.

   - `publicEndpoint.allowedCidrs` (optional): Allowed CIDR blocks for the public endpoint. Only the IP addresses of these CIDR blocks are allowed to connect to the cluster.

     Specify the CIDR blocks in the IPv4 format with bits for hosts equal to zero. For example, `192.168.0.0/24` or `8.8.8.64/26`. The example splits a comma-separated string, so pass multiple blocks as `192.168.0.0/24,8.8.8.64/26`.

     For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

   * `spec.controlPlane.etcdClusterSize`: Number of [etcd stores](https://docs.nebius.com/kubernetes/components.md#etcd). Three of them ensure high availability of the cluster.

## How to delete clusters

**CLI**

Get the cluster ID as shown in [How to modify clusters](#how-to-modify-clusters) and delete the cluster:

```bash theme={null}
nebius mk8s cluster delete --id $K8S_CLUSTER_ID
```

**Terraform**

1. If you manage node groups in the cluster with Terraform, first [delete the node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-delete-node-groups).
2. Remove the corresponding `nebius_mk8s_v1_cluster` resource from the configuration file.
3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Get the cluster ID as shown in [How to modify clusters](#how-to-modify-clusters) and delete the cluster:

```go theme={null}
deleteOperation, err := sdk.Services().MK8S().V1().
    Cluster().Delete(
        ctx,
        &mk8s.DeleteClusterRequest{
            Id: "<cluster_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = deleteOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

Get the cluster ID as shown in [How to modify clusters](#how-to-modify-clusters) and delete the cluster:

```python theme={null}
delete_cluster_service = ClusterServiceClient(sdk)
delete_operation = await delete_cluster_service.delete(
    DeleteClusterRequest(id="<cluster_ID>"),
)
await delete_operation.wait()
```

**JavaScript SDK**

Get the cluster ID as shown in [How to modify clusters](#how-to-modify-clusters) and delete the cluster:

```ts theme={null}
const deleteClusterService = new ClusterService(sdk);
const deleteOperation = await deleteClusterService.delete(
  DeleteClusterRequest.create({
    id: "<cluster_ID>",
  }),
).result;
await deleteOperation.wait();
```

## Examples

Creating a cluster with the Kubernetes version 1.36 and a public endpoint for the control plane:

**CLI**

```bash theme={null}
nebius mk8s cluster create \
  --name cluster-example \
  --control-plane-version 1.36 \
  --control-plane-subnet-id \
    $(nebius vpc subnet list --format jsonpath='{.items[0].metadata.id}') \
  --control-plane-endpoints-public-endpoint=true
```

**Go SDK**

`SubnetId` reads the `subnetID` variable. Assign the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) to it before you run the code.

```go theme={null}
realCreateOperation, err := sdk.Services().MK8S().V1().
    Cluster().Create(
        ctx,
        &mk8s.CreateClusterRequest{
            Metadata: &common.ResourceMetadata{
                Name: "cluster-example",
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
if _, err = realCreateOperation.Wait(ctx); err != nil {
    return err
}
```

**Python SDK**

`subnet_id` reads the `subnet_id` variable. Assign the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) to it before you run the code.

```python theme={null}
real_cluster_service = ClusterServiceClient(sdk)
real_create_operation = await real_cluster_service.create(
    CreateClusterRequest(
        metadata=ResourceMetadata(name="cluster-example"),
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
await real_create_operation.wait()
```

**JavaScript SDK**

`subnetId` reads the `subnetId` variable. Assign the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) to it before you run the code.

```ts theme={null}
const realClusterService = new ClusterService(sdk);
const realCreateOperation = await realClusterService.create(
  CreateClusterRequest.create({
    metadata: ResourceMetadata.create({
      name: "cluster-example",
    }),
    spec: ClusterSpec.create({
      controlPlane: ControlPlaneSpec.create({
        version: "1.36",
        subnetId: subnetId,
        endpoints: ControlPlaneEndpointsSpec.create({
          publicEndpoint: PublicEndpointSpec.create({}),
        }),
      }),
    }),
  }),
).result;
await realCreateOperation.wait();
```
