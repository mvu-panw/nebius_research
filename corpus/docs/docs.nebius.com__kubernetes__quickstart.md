# How to get started with Managed Service for Kubernetes®: Create your first cluster for Kubernetes

Source: https://docs.nebius.com/kubernetes/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to get started with Managed Service for Kubernetes®: Create your first cluster for Kubernetes

With [Kubernetes](https://kubernetes.io/), you can efficiently manage and scale your containerized ML/AI applications and ensure they are portable and fault-tolerant. To get started, create a Managed Service for Kubernetes cluster and its child node group in the `eu-north1` region. Then, connect to the cluster.

## Prerequisites

**Web console**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   You will use the CLI to get the cluster credentials for connecting with kubectl.

2. Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl), the Kubernetes command-line interface:

   ```bash Ubuntu theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   ```bash macOS theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   chmod +x ./kubectl
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Install [jq](https://jqlang.github.io/jq/) to extract IDs from JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl), the Kubernetes command-line interface:

   ```bash Ubuntu theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   ```bash macOS theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   chmod +x ./kubectl
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   You will use the CLI to get the cluster credentials for connecting with kubectl.

3. Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl), the Kubernetes command-line interface:

   ```bash Ubuntu theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   ```bash macOS theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   chmod +x ./kubectl
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   You will use the CLI to get the cluster credentials for connecting with kubectl.

3. Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl), the Kubernetes command-line interface:

   ```bash Ubuntu theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   ```bash macOS theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   chmod +x ./kubectl
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   You will use the CLI to get the cluster credentials for connecting with kubectl.

3. Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl), the Kubernetes command-line interface:

   ```bash Ubuntu theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   ```bash macOS theme={null}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   chmod +x ./kubectl
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

## Steps

### Create a cluster and a node group

The cluster's control plane runs Kubernetes version 1.36, which is the default [version](https://docs.nebius.com/kubernetes/versions.md) for Managed Kubernetes clusters.

**Web console**

1. In the sidebar, go to  **Compute** → **Kubernetes**.

2. Click  **Create cluster**.

   The creation flow is a step-by-step wizard. The sidebar shows your progress through the configuration sections. To move between sections, click **Back** and **Next**.

3. On the **Cluster** step, enter the cluster name and review the settings:

   * Select the network and subnet.
   * Keep the recommended Kubernetes version 1.36. For supported versions, see [Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/versions.md).
   * Keep the public endpoint enabled. As a result, the cluster is available from the internet, and you can connect to it from any machine.

4. On the **Node groups** step, add a node group to the cluster:

   1. Click  **Add node group**.
   2. On the **General** step, enter the node group name. Keep the rest of the settings unchanged.
   3. On the **Compute resources** step, select **Without GPU**. Select the **Non-GPU Intel Ice Lake** [platform](https://docs.nebius.com/compute/virtual-machines/types.md). Under **Size**, set the **Number of nodes** to 2. Under **Settings**, select your project. Select the preset with 2 CPUs and 8 GiB of RAM. Then, select an operating system for the nodes, for example, Ubuntu 24.04 LTS.
   4. On the **Storage** step, under **Node storage**, select the **SSD** disk type and set the size to 128 GiB.
   5. On the **Additional** step, keep the default settings.
   6. Click **Add node group**.

5. Go to the **Review** step, check the cluster configuration and click **Create**.

6. After the cluster is created, copy the cluster ID from its page and save the ID to an environment variable. You will need it to connect to the cluster:

   ```bash theme={null}
   export CLUSTER_ID=<cluster_ID>
   ```

**CLI**

1. Your cluster's control plane and nodes use private IP addresses from the default subnet. Get its ID:

   ```bash theme={null}
   export SUBNET_ID=$(nebius vpc subnet list \
     --format jsonpath='{.items[0].metadata.id}')
   ```

2. Create a cluster with a public endpoint allocated to its control plane, and get the cluster ID:

   ```bash theme={null}
   export CLUSTER_ID=$(nebius mk8s cluster create \
     --name quickstart-mk8s-cluster \
     --control-plane-subnet-id $SUBNET_ID \
     --control-plane-endpoints-public-endpoint=true \
     --format jsonpath='{.metadata.id}')
   ```

3. Create a node group and add it to the cluster:

   ```bash theme={null}
   nebius mk8s node-group create \
     --name quickstart-mk8s-nodes \
     --parent-id $CLUSTER_ID \
     --fixed-node-count 2 \
     --template-resources-platform "cpu-e2" \
     --template-resources-preset "2vcpu-8gb" \
     --template-boot-disk-type network_ssd \
     --template-boot-disk-size-bytes 137438953472 \
     --template-network-interfaces "[{\"subnet_id\": \"$SUBNET_ID\"}]"
   ```

   The command creates a group of 2 nodes. Each node is a non-GPU (`--template-resources-platform "cpu-e2"`) virtual machine that has 2 vCPUs, 8 GiB of RAM and a 128 GiB Network SSD boot disk.

**Go SDK**

1. Your cluster's control plane and nodes use private IP addresses from the default subnet. Get its ID:

   ```go theme={null}
   subnets, err := sdk.Services().VPC().V1().
       Subnet().List(
           ctx,
           &vpc.ListSubnetsRequest{
               ParentId: "<project_ID>",
           },
       )
   if err != nil {
       return err
   }
   if len(subnets.GetItems()) == 0 {
       return fmt.Errorf("no subnets found")
   }
   subnetID := subnets.GetItems()[0].GetMetadata().GetId()
   ```

   For `ParentId`, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code saves the ID of the first subnet in the project to `subnetID`.

2. Create a cluster with a public endpoint allocated to its control plane, and get the cluster ID:

   ```go theme={null}
   clusterOperation, err := sdk.Services().MK8S().V1().
       Cluster().Create(
           ctx,
           &mk8s.CreateClusterRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<project_ID>",
                   Name:     "quickstart-mk8s-cluster",
               },
               Spec: &mk8s.ClusterSpec{
                   ControlPlane: &mk8s.ControlPlaneSpec{
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
   clusterID := clusterOperation.ResourceID()
   if clusterID == "" {
       return fmt.Errorf("cluster ID is missing")
   }
   ```

3. Create a node group and add it to the cluster:

   ```go theme={null}
   publicKeyData, err := os.ReadFile(
       os.ExpandEnv("$HOME/.ssh/id_ed25519.pub"),
   )
   if err != nil {
       return err
   }
   publicKey := strings.TrimSpace(string(publicKeyData))
   cloudInitUserData := "#cloud-config\nusers:\n" +
       "  - name: user\n" +
       "    sudo: ALL=(ALL) NOPASSWD:ALL\n" +
       "    shell: /bin/bash\n" +
       "    ssh_authorized_keys:\n" +
       "      - " + publicKey
   networkInterfaces := []*mk8s.NetworkInterfaceTemplate{
       {
           PublicIpAddress: &mk8s.PublicIPAddress{},
           SubnetId:         subnetID,
       },
   }
   nodeGroupOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Create(
           ctx,
           &mk8s.CreateNodeGroupRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: clusterID,
                   Name:     "quickstart-mk8s-nodes",
               },
               Spec: &mk8s.NodeGroupSpec{
                   Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                       FixedNodeCount: 2,
                   },
                   Template: &mk8s.NodeTemplate{
                       Resources: &mk8s.ResourcesSpec{
                           Platform: "cpu-e2",
                           Size: &mk8s.ResourcesSpec_Preset{
                               Preset: "2vcpu-8gb",
                           },
                       },
                       BootDisk: &mk8s.DiskSpec{
                           Size: &mk8s.DiskSpec_SizeBytes{
                               SizeBytes: 137438953472,
                           },
                           Type: mk8s.DiskSpec_NETWORK_SSD,
                       },
                       CloudInitUserData: cloudInitUserData,
                       NetworkInterfaces: networkInterfaces,
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

   The code creates a group of 2 nodes. Each node is a non-GPU (`Platform: "cpu-e2"`) virtual machine that has 2 vCPUs, 8 GiB of RAM and a 128 GiB Network SSD boot disk.

   The nodes get public IP addresses, and `CloudInitUserData` grants the `user` account access with the SSH key from `$HOME/.ssh/id_ed25519.pub`. Create this key pair before you run the code.

**Python SDK**

1. Your cluster's control plane and nodes use private IP addresses from the default subnet. Get its ID:

   ```python theme={null}
   subnet_service = SubnetServiceClient(sdk)
   subnets = await subnet_service.list(
       ListSubnetsRequest(parent_id="<project_ID>"),
   )
   if not subnets.items:
       raise ValueError("no subnets found")
   subnet_id = subnets.items[0].metadata.id
   ```

   For `parent_id`, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code saves the ID of the first subnet in the project to `subnet_id`.

2. Create a cluster with a public endpoint allocated to its control plane, and get the cluster ID:

   ```python theme={null}
   cluster_service = ClusterServiceClient(sdk)
   cluster_operation = await cluster_service.create(
       CreateClusterRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="quickstart-mk8s-cluster",
           ),
           spec=ClusterSpec(
               control_plane=ControlPlaneSpec(
                   subnet_id=subnet_id,
                   endpoints=ControlPlaneEndpointsSpec(
                       public_endpoint=PublicEndpointSpec(),
                   ),
               ),
           ),
       ),
   )
   await cluster_operation.wait()
   cluster_id = cluster_operation.resource_id
   if not cluster_id:
       raise ValueError("cluster ID is missing")
   ```

3. Create a node group and add it to the cluster:

   ```python theme={null}
   public_key_path = Path.home() / ".ssh" / "id_ed25519.pub"
   public_key = public_key_path.read_text().strip()
   cloud_init_user_data = "\n".join(
       [
           "#cloud-config",
           "users:",
           "  - name: user",
           "    sudo: ALL=(ALL) NOPASSWD:ALL",
           "    shell: /bin/bash",
           "    ssh_authorized_keys:",
           f"      - {public_key}",
       ],
   )
   node_group_service = NodeGroupServiceClient(sdk)
   node_group_operation = await node_group_service.create(
       CreateNodeGroupRequest(
           metadata=ResourceMetadata(
               parent_id=cluster_id,
               name="quickstart-mk8s-nodes",
           ),
           spec=NodeGroupSpec(
               fixed_node_count=2,
               template=NodeTemplate(
                   resources=ResourcesSpec(
                       platform="cpu-e2",
                       preset="2vcpu-8gb",
                   ),
                   boot_disk=DiskSpec(
                       size_bytes=137438953472,
                       type=DiskSpec__DiskType.NETWORK_SSD,
                   ),
                   cloud_init_user_data=cloud_init_user_data,
                   network_interfaces=[
                       NetworkInterfaceTemplate(
                           public_ip_address=PublicIPAddress(),
                           subnet_id=subnet_id,
                       ),
                   ],
               ),
           ),
       ),
   )
   await node_group_operation.wait()
   node_group_id = node_group_operation.resource_id
   if not node_group_id:
       raise ValueError("node group ID is missing")
   ```

   The code creates a group of 2 nodes. Each node is a non-GPU (`platform="cpu-e2"`) virtual machine that has 2 vCPUs, 8 GiB of RAM and a 128 GiB Network SSD boot disk.

   The nodes get public IP addresses, and `cloud_init_user_data` grants the `user` account access with the SSH key from `~/.ssh/id_ed25519.pub`. Create this key pair before you run the code.

**JavaScript SDK**

1. Your cluster's control plane and nodes use private IP addresses from the default subnet. Get its ID:

   ```ts theme={null}
   const subnetService = new SubnetService(sdk);
   const subnets = await subnetService.list(
     ListSubnetsRequest.create({
       parentId: "<project_ID>",
     }),
   );
   const subnetId = subnets.items[0]?.metadata?.id;
   if (!subnetId) {
     throw new Error("no subnets found");
   }
   ```

   For `parentId`, specify your [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code saves the ID of the first subnet in the project to `subnetId`.

2. Create a cluster with a public endpoint allocated to its control plane, and get the cluster ID:

   ```ts theme={null}
   const clusterService = new ClusterService(sdk);
   const clusterOperation = await clusterService.create(
     CreateClusterRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<project_ID>",
         name: "quickstart-mk8s-cluster",
       }),
       spec: ClusterSpec.create({
         controlPlane: ControlPlaneSpec.create({
           subnetId: subnetId,
           endpoints: ControlPlaneEndpointsSpec.create({
             publicEndpoint: PublicEndpointSpec.create({}),
           }),
         }),
       }),
     }),
   ).result;
   await clusterOperation.wait();
   const clusterId = clusterOperation.resourceId();
   if (!clusterId) {
     throw new Error("cluster ID is missing");
   }
   ```

3. Create a node group and add it to the cluster:

   ```ts theme={null}
   const homeDir = process.env.HOME;
   if (!homeDir) {
     throw new Error("HOME is not set");
   }
   const publicKey = (
     await readFile(`${homeDir}/.ssh/id_ed25519.pub`, "utf8")
   ).trim();
   const cloudInitUserData = [
     "#cloud-config",
     "users:",
     "  - name: user",
     "    sudo: ALL=(ALL) NOPASSWD:ALL",
     "    shell: /bin/bash",
     "    ssh_authorized_keys:",
     "      - " + publicKey,
   ].join("\n");
   const nodeGroupService = new NodeGroupService(sdk);
   const nodeGroupOperation = await nodeGroupService.create(
     CreateNodeGroupRequest.create({
       metadata: ResourceMetadata.create({
         parentId: clusterId,
         name: "quickstart-mk8s-nodes",
       }),
       spec: NodeGroupSpec.create({
         size: {
           $case: "fixedNodeCount",
           fixedNodeCount: 2,
         },
         template: NodeTemplate.create({
           resources: ResourcesSpec.create({
             platform: "cpu-e2",
             size: {
               $case: "preset",
               preset: "2vcpu-8gb",
             },
           }),
           bootDisk: DiskSpec.create({
             size: {
               $case: "sizeBytes",
               sizeBytes: 137438953472,
             },
             type: DiskSpec_DiskType.NETWORK_SSD,
           }),
           cloudInitUserData,
           networkInterfaces: [
             NetworkInterfaceTemplate.create({
               publicIpAddress: PublicIPAddress.create({}),
               subnetId: subnetId,
             }),
           ],
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

   The code creates a group of 2 nodes. Each node is a non-GPU (`platform: "cpu-e2"`) virtual machine that has 2 vCPUs, 8 GiB of RAM and a 128 GiB Network SSD boot disk.

   The nodes get public IP addresses, and `cloudInitUserData` grants the `user` account access with the SSH key from `$HOME/.ssh/id_ed25519.pub`. Create this key pair before you run the code.

### Connect to the cluster

Cluster credentials for kubectl come from the CLI regardless of the interface that you used to create the cluster.

1. Create a kubeconfig file containing the cluster details for kubectl.

   If you created the cluster with an SDK, first save the returned cluster ID to the `CLUSTER_ID` environment variable:

   ```bash theme={null}
   export CLUSTER_ID=<cluster_ID>
   ```

   Then, create the file:

   ```bash theme={null}
   nebius mk8s cluster get-credentials \
     --id $CLUSTER_ID --external
   ```

2. Check that the cluster is accessible. For example:

   * Get addresses of the control plane and cluster services:

     ```bash theme={null}
     kubectl cluster-info
     ```

   * Get the list of Pods:

     ```bash theme={null}
     kubectl get pods -A
     ```

## What's next

* [How to create and modify Managed Service for Kubernetes® clusters](https://docs.nebius.com/kubernetes/clusters/manage.md)
* [Creating and modifying Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/node-groups/manage.md)
