# Pulling images from Container Registry for workloads in Managed Service for Kubernetes® clusters

Source: https://docs.nebius.com/kubernetes/workloads/images-container-registry

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Pulling images from Container Registry for workloads in Managed Service for Kubernetes® clusters

If a node group in a Managed Service for Kubernetes cluster has a [service account](https://docs.nebius.com/iam/overview.md#accounts-and-members) added to it, Pods hosted by the group's nodes can pull images from Container Registry without additional authentication.

> [!NOTE]
>
> We recommend using the service account from the same [project](https://docs.nebius.com/iam/overview.md#projects) as the node group.

To set up pulling images without authentication:

1. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. In your Managed Kubernetes cluster, [create or modify a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md) so that a service account from a group with at least the `viewer` role is added to it. A service account for node groups that your project came with, `k8s-node-group-sa`, is in the default `viewers` group.

   > [!WARNING]
   >
   > Currently, it is not possible to create a node group with a service account using the web console.

   For example:

   **CLI**

   The commands below assume that the Nebius AI Cloud CLI is configured as described in its [documentation](https://docs.nebius.com/cli/configure.md), including adding the [project](https://docs.nebius.com/iam/overview.md#projects) ID in the CLI profile's `parent-id`, and that the Managed Kubernetes cluster ID is stored in the `MK8S_CLUSTER_ID` environment variable.

   ```bash theme={null}
   export MK8S_SA_ID=$(nebius iam service-account get-by-name \
     --name k8s-node-group-sa \
     --format jsonpath='{.metadata.id}')
   nebius mk8s node-group create \
     --parent-id $MK8S_CLUSTER_ID \
     --name node-group-example \
     --fixed-node-count 2 \
     --template-service-account-id $MK8S_SA_ID \
     --template-resources-platform cpu-e2 \
     --template-resources-preset 2vcpu-8gb
   ```

   For details about `nebius mk8s node-group create`, see the [CLI reference](https://docs.nebius.com/cli/reference/mk8s/node-group/create.md).

   **Terraform**

   The configuration below assumes that the [project](https://docs.nebius.com/iam/overview.md#projects) ID and Managed Kubernetes cluster ID are stored in the `project_id` and `mk8s_cluster_id` [Terraform input variables](https://developer.hashicorp.com/terraform/language/values/variables), respectively.

   ```hcl theme={null}
   data "nebius_iam_v1_service_account" "k8s_node_group" {
     parent_id = var.project_id
     name      = "k8s-node-group-sa"
   }

   resource "nebius_mk8s_v1_node_group" "example" {
     parent_id = var.mk8s_cluster_id
     name      = "node-group-example"

     fixed_node_count = 2

     template = {
       service_account_id = data.nebius_iam_v1_service_account.k8s_node_group.id

       resources = {
         platform = "cpu-e2"
         preset   = "2vcpu-8gb"
       }
     }
   }
   ```

   For details about the `nebius_mk8s_v1_node_group` Terraform resource, see the [provider reference](https://docs.nebius.com/terraform-provider/reference/resources/mk8s_v1_node_group.md).

   **Go SDK**

   The code below assumes that the Managed Kubernetes cluster ID is stored in the `mk8sClusterID` variable.

   ```go theme={null}
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
   nodeGroupOperation, err := sdk.Services().MK8S().V1().
       NodeGroup().Create(
           ctx,
           &mk8s.CreateNodeGroupRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: mk8sClusterID,
                   Name:     "node-group-example",
               },
               Spec: &mk8s.NodeGroupSpec{
                   Size: &mk8s.NodeGroupSpec_FixedNodeCount{
                       FixedNodeCount: 2,
                   },
                   Template: &mk8s.NodeTemplate{
                       ServiceAccountId: saID,
                       Resources: &mk8s.ResourcesSpec{
                           Platform: "cpu-e2",
                           Size: &mk8s.ResourcesSpec_Preset{
                               Preset: "2vcpu-8gb",
                           },
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

   The code looks the `k8s-node-group-sa` service account up by name and passes its ID to `Spec.Template.ServiceAccountId`.

   **Python SDK**

   The code below assumes that the Managed Kubernetes cluster ID is stored in the `mk8s_cluster_id` variable.

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(name="k8s-node-group-sa"),
   )
   sa_id = service_account.metadata.id
   if not sa_id:
       raise ValueError("service account ID is missing")
   node_group_service = NodeGroupServiceClient(sdk)
   node_group_operation = await node_group_service.create(
       CreateNodeGroupRequest(
           metadata=ResourceMetadata(
               parent_id=mk8s_cluster_id,
               name="node-group-example",
           ),
           spec=NodeGroupSpec(
               fixed_node_count=2,
               template=NodeTemplate(
                   service_account_id=sa_id,
                   resources=ResourcesSpec(
                       platform="cpu-e2",
                       preset="2vcpu-8gb",
                   ),
               ),
           ),
       ),
   )
   await node_group_operation.wait()
   ```

   The code looks the `k8s-node-group-sa` service account up by name and passes its ID to `spec.template.service_account_id`.

   **JavaScript SDK**

   The code below assumes that the Managed Kubernetes cluster ID is stored in the `mk8sClusterId` variable.

   ```ts theme={null}
   const serviceAccountService =
     new ServiceAccountService(sdk);
   const serviceAccount = await serviceAccountService.getByName(
     GetServiceAccountByNameRequest.create({
       name: "k8s-node-group-sa",
     }),
   );
   const saId = serviceAccount.metadata?.id;
   if (!saId) {
     throw new Error("service account ID is missing");
   }
   const nodeGroupService = new NodeGroupService(sdk);
   const nodeGroupOperation = await nodeGroupService.create(
     CreateNodeGroupRequest.create({
       metadata: ResourceMetadata.create({
         parentId: mk8sClusterId,
         name: "node-group-example",
       }),
       spec: NodeGroupSpec.create({
         size: {
           $case: "fixedNodeCount",
           fixedNodeCount: 2,
         },
         template: NodeTemplate.create({
           serviceAccountId: saId,
           resources: ResourcesSpec.create({
             platform: "cpu-e2",
             size: {
               $case: "preset",
               preset: "2vcpu-8gb",
             },
           }),
         }),
       }),
     }),
   ).result;
   await nodeGroupOperation.wait();
   ```

   The code looks the `k8s-node-group-sa` service account up by name and passes its ID to `spec.template.serviceAccountId`.

After setting up node groups, you can just refer to Container Registry images in your manifests (for Pods or other resources that manage Pods, such as Deployments) without providing credentials to pull them.

> For example, if your nginx image is at `cr.eu-north1.nebius.cloud/<registry_ID>/nginx:mynginx` (you can get the registry ID in the web console or by using the [nebius registry list](https://docs.nebius.com/cli/reference/registry/list.md) CLI command), here is how to refer to it in a Deployment manifest:
>
> ```yaml theme={null}
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: nginx-deployment
> spec:
>   replicas: 1
>   selector:
>     matchLabels:
>       app: nginx
>   template:
>     metadata:
>       labels:
>         app: nginx
>     spec:
>       containers:
>         - name: nginx
>           image: cr.eu-north1.nebius.cloud/<registry_ID>/nginx:mynginx
>           ports:
>             - containerPort: 80
> ```
