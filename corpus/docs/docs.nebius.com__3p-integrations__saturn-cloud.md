# Deploying Saturn Cloud on a Managed Service for Kubernetes® cluster

Source: https://docs.nebius.com/3p-integrations/saturn-cloud

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying Saturn Cloud on a Managed Service for Kubernetes® cluster

[Saturn Cloud](https://saturncloud.io/) is an AI development platform. Your team can use it to run development workspaces by using JupyterLab® or RStudio. Saturn Cloud also runs scheduled jobs and deployments that serve models and dashboards. It manages the environments for these workloads and automatically scales the computing resources that they need.

You can deploy and run Saturn Cloud on a [Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/index.md) cluster by using the ready Terraform recipe. It creates the cluster, its node groups, and a [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) and then installs Saturn Cloud on the cluster.

To deploy Saturn Cloud, sign up in Saturn Cloud to get the recipe settings for your organization, prepare the infrastructure for the recipe, and apply it. Then log in to Saturn Cloud and run code in a JupyterLab workspace to test the deployment.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Managed Kubernetes nodes](https://docs.nebius.com/kubernetes/resources/pricing.md#nodes)
* [Compute disks](https://docs.nebius.com/compute/resources/pricing.md#disks)
* [Shared filesystem](https://docs.nebius.com/compute/resources/pricing.md#shared-filesystems)
* [Object Storage bucket](https://docs.nebius.com/object-storage/resources/pricing.md)

## Prerequisites

1. Make sure that you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `admin` role within your tenant
   ; for example, the default `admins` group.
   You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

   You need this role because the deployment adds service accounts to the `editors` and `viewers` groups of your tenant.

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

3. [Install Terraform](https://developer.hashicorp.com/terraform/install) 1.8 or later. The recipe uses provider functions that earlier versions of Terraform don't support.

4. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl). Terraform uses kubectl to move the system components of the cluster to the system nodes.

5. [Install jq](https://jqlang.github.io/jq/download/) to extract IDs from the JSON data returned by the Nebius AI Cloud CLI.

6. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

## Steps

### Sign up in Saturn Cloud

1. Go to the [Saturn Cloud registration page](https://manager.saturnenterprise.io/v2/register).

2. Specify the following settings:

   * **Organization Name**: Name of your organization in Saturn Cloud. The name becomes part of your Saturn Cloud domain. For example, if the name is `my-team`, the domain is `my-team.saturnenterprise.io`.
   * **Email Address**: Email address of the Saturn Cloud administrator.
   * **Cloud Provider**: Nebius.

3. Click **Create Account**.

4. Open the activation email from Saturn Cloud. This email includes a command that activates your account — run this command.

   After that, Saturn Cloud sends the second email with the setup instructions and the `terraform.tfvars` file. The file contains the configuration of your Saturn Cloud installation, including a bootstrap token.

   Only download the file from this email. Don't create a repository based on the instructions in the email. You'll use the [saturncloud-reference-terraform](https://github.com/saturncloud/saturncloud-reference-terraform/tree/main) repository instead.

> [!WARNING]
>
> The bootstrap token from the `terraform.tfvars` file expires in 4 hours. If you can't complete the deployment within this time frame, request a new `terraform.tfvars` file with a new token.

> [accordion] What to do if the bootstrap token expires
>
> If the token expires, run the following command:
>
> ```bash theme={null}
> curl -X POST https://manager.saturnenterprise.io/v2/resend-setup \
>   -H "Content-Type: application/json" \
>   -d '{
>     "name": "<organization_name>",
>     "email": "<email_address>"
>   }'
> ```
>
> In the request body, set the organization and email that you specified when you registered in Saturn Cloud.
>
> Saturn Cloud sends you the setup email again. The `terraform.tfvars` file in this email has a new bootstrap token. Copy the `saturn_bootstrap_token` value from this file to the `terraform.tfvars` file that you use for the deployment.

### Prepare infrastructure

1. Clone the [Saturn Cloud reference Terraform](https://github.com/saturncloud/saturncloud-reference-terraform) repository and go to the `nebius` directory:

   ```bash theme={null}
   git clone https://github.com/saturncloud/saturncloud-reference-terraform.git
   cd saturncloud-reference-terraform/nebius
   ```

2. Replace the `terraform.tfvars` file in the `nebius` directory with the file from the Saturn Cloud email.

3. Add the path of your public SSH key to `terraform.tfvars`, for example:

   ```hcl theme={null}
   ssh_public_key = {
     path = "~/.ssh/id_ed25519.pub"
   }
   ```

   The nodes of the cluster use this key. If you don't add the path, Terraform uses `~/.ssh/id_rsa.pub`, and `terraform apply` fails if `id_rsa.pub` doesn't exist.

4. Save the IDs of your tenant and project, and the region of the project, to environment variables:

   ```bash theme={null}
   export NEBIUS_TENANT_ID=<tenant_ID>
   export NEBIUS_PROJECT_ID=<project_ID>
   export NEBIUS_REGION=<region>
   ```

   For more information, see:

   * [How to get a tenant ID](https://docs.nebius.com/iam/get-tenants.md)
   * [How to get a project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id)
   * [List of regions](https://docs.nebius.com/overview/regions.md)

   The setup email asks you to set a region in `terraform.tfvars`. You don't need to do this because the `environment.sh` script sets the region from the `NEBIUS_REGION` environment variable.

5. In the `nebius` directory of the cloned repository, run the `environment.sh` script:

   ```bash theme={null}
   source ./environment.sh
   ```

   The script creates the following resources:

   * The `saturn-cloud-sa` service account in the `editors` group of your tenant.
   * A bucket for the Terraform state, with versioning enabled.
   * An access key of the service account, so that Terraform can access the bucket. The access key expires after one day.

   The script also saves the values that Terraform needs to environment variables. For example, it saves an IAM access token, which expires after 12 hours, and the ID of the first subnet in your project, which the cluster uses.

   The first time you run the script, it shows an error that the `saturn-cloud-sa` service account is not found. You can ignore this error because the script creates the service account right after this check.

### Deploy Saturn Cloud and Nebius AI Cloud resources

Before you deploy Saturn Cloud, define the configuration of node groups that you create. The default configuration is located in the `nebius/variables.tf` file, in the `node_pools` variable.

Each group starts with no nodes. The cluster adds up to 10 nodes to a group when your workloads need them. When you create a workload in Saturn Cloud, you select one of these node groups.

In addition, the default configuration includes a shared filesystem with the 100 GiB size.

1. (Optional) If you want to change the configuration of the node groups (for example, the region doesn't support the default `gpu-h200-sxm` [Compute platform](https://docs.nebius.com/compute/virtual-machines/types.md)), uncomment and adjust the `node_pools` parameter in the `terraform.tfvars` file. Thus, Terraform only creates node groups with configuration from this parameter.

   In `node_pools`, in `terraform.tfvars`:

   * Preserve the group with the `cpu-d3` platform and the `4vcpu-16gb` preset because Saturn Cloud builds images on these nodes.
   * Replace the `gpu-h200-sxm` platform with the required one, if needed.
   * If you don't need nodes with eight GPUs, remove the group with the `8gpu-128vcpu-1600gb` preset. If you keep it, specify an [InfiniBand™ fabric](https://docs.nebius.com/compute/clusters/gpu.md#infiniband-fabrics) in the `infiniband_fabric` parameter.

   For the supported values of the platforms and presets, see the `nebius/validation.tf` file.

2. (Optional) If you want to change the size of the shared filesystem, add the `filestore_disk_size_gibibytes` parameter to `terraform.tfvars` and set the size in GiB.

3. To use up-to-date versions of resources and to make sure that the resources are created successfully, update the following files in the repository:

   * In the `provider.tf` file, in `provider "nebius"`, set the following contents:

     ```hcl theme={null}
     domain = "api.nebius.cloud:443"
     default_labels = {
       "msp.nebius.com/skypilot-context-name" = "saturn-cluster"
     }
     ```

     If `provider "nebius"` already includes some contents, replace them with the lines above.

   * In the `terraform.tf` file, in `required_providers.nebius`, update `source` and `version` to the following:

     ```hcl theme={null}
     source  = "nebius/nebius"
     version = ">= 0.6.8"
     ```

   * In the `terraform.tfvars` file, specify an up-to-date Kubernetes version: `k8s_version = "<version>"`. To get the up-to-date version, see [Available Kubernetes versions](https://docs.nebius.com/kubernetes/versions.md#available-kubernetes-versions).

   * In the `nebius/mk8s.tf` file, add the following contents to the `nebius_mk8s_v1_cluster` resource:

     ```hcl theme={null}
     lifecycle {
       ignore_changes = [labels]
     }
     ```

4. Initialize Terraform in the working directory:
   ```bash theme={null}
   terraform init
   ```

5. Apply the changes:

   ```bash theme={null}
   terraform apply
   ```

   Terraform creates the following resources in your project in Nebius AI Cloud:

   * Managed Kubernetes cluster with a group of system nodes and the node groups from `node_pools`.
   * Shared filesystem.
   * Service account that the nodes use to pull images from Container Registry.

   You can check these resources in the [web console](https://console.nebius.com).

   Terraform creates the resources. After that, Saturn Cloud installs its components in the Managed Kubernetes cluster. The resource creation and component installation can take about 15 minutes in total. When the installation is complete, Saturn Cloud sends a welcome email to the administrator's email address.

### Log in to Saturn Cloud

Once installation is finished, Saturn Cloud deploys a website for your organization, `https://app.<organization_name>.saturnenterprise.io`. At this website, you can access the Saturn Cloud dashboard and run workloads.

1. Open the welcome email from Saturn Cloud and follow the link for resetting a password. The link expires in 4 hours.

   > [!WARNING]
   >
   > If the browser shows that the website can't be found, the DNS record for your Saturn Cloud domain isn't available yet. Wait 15 minutes and try again.

2. On this website, set the password of the `admin` user. After that, the Saturn Cloud dashboard opens automatically.

### Test the deployment

To test the deployment, create a workspace with JupyterLab® preinstalled in Saturn Cloud and run code in JupyterLab:

1. On the **Dashboard** page, click **Create a resource**.

2. On the **Instance Size** step, select the values that correspond to your configuration:

   * **Cloud**: `Nebius`.
   * **GPU Type** and **Memory**: should correspond to the preset in the Terraform manifest. For example, if you specify the `1gpu-16vcpu-200gb` preset in `node_pools`, in `terraform.tfvars`, select the `H200` GPU type and the `200Gi` memory.

   After that, select the suggested configuration and click **Next**.

3. On the **Resource Type** step, select **New Python Server** and click **Next**.

4. On the **Details** step, specify a name for the workspace in the **Name** field and click **Create Resource**.

5. On the workspace page that opens, click **Start**.

   Wait until the status of the workspace changes to `Running`. The cluster first adds a node for the workspace, so the workspace can take a few minutes to start.

6. Click **Jupyter Lab**.

7. In JupyterLab, create a notebook and run the following code:

   ```python theme={null}
   import os
   print(os.cpu_count())
   ```

   The output is the number of vCPUs in the preset of the node group that you selected.

8. Stop the workspace in Saturn Cloud. Close the JupyterLab window and then click **Stop** on the workspace page. In the window that opens, click **Yes** to confirm the action.

To learn how to invite your team, configure single sign-on, and run jobs and deployments, see the [Saturn Cloud documentation](https://saturncloud.io/docs/).

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources, so Nebius AI Cloud doesn't charge for them.

The `terraform destroy` command deletes only the resources that Terraform created: the Managed Kubernetes cluster, its node groups, and the shared filesystem. The `environment.sh` script creates the bucket and the service account by using the Nebius AI Cloud CLI, and the cluster creates disks for Saturn Cloud workspaces. The following steps delete all of these resources:

1. On the workspace page in Saturn Cloud, click **Delete** to delete the workspace. In the window that opens, click **Yes** to confirm the action.

2. Go to the `nebius` directory of the cloned repository and run the `environment.sh` script again:

   ```bash theme={null}
   export NEBIUS_TENANT_ID=<tenant_ID>
   export NEBIUS_PROJECT_ID=<project_ID>
   export NEBIUS_REGION=<region>
   source ./environment.sh
   ```

   Terraform reads the project and subnet IDs, the IAM access token, and the access key to the bucket with the Terraform state from environment variables that the script sets. These variables exist only in the terminal session where you ran the script, and the token and the key expire. The script sets the variables again.

3. Get the ID of the Managed Kubernetes cluster:

   > [tab] CLI
   >
   > ```bash theme={null}
   > nebius mk8s cluster get-by-name \
   >   --name saturn-cluster \
   >   --format jsonpath='{.metadata.id}'
   > ```

   > [tab] Go SDK
   >
   > ```go theme={null}
   > clusterService := sdk.Services().MK8S().V1().Cluster()
   > cluster, err := clusterService.GetByName(
   >     ctx,
   >     &common.GetByNameRequest{
   >         Name: "saturn-cluster",
   >     },
   > )
   > if err != nil {
   >     return err
   > }
   > fmt.Println(cluster.GetMetadata().GetId())
   > ```

   > [tab] Python SDK
   >
   > ```python theme={null}
   > cluster_service = ClusterServiceClient(sdk)
   > cluster = await cluster_service.get_by_name(
   >     GetByNameRequest(name="saturn-cluster"),
   > )
   > print(cluster.metadata.id)
   > ```

   > [tab] JavaScript SDK
   >
   > ```ts theme={null}
   > const clusterService = new ClusterService(sdk);
   > const cluster = await clusterService.getByName(
   >   GetByNameRequest.create({
   >     name: "saturn-cluster",
   >   }),
   > );
   > console.log(cluster.metadata?.id);
   > ```

   > [tab] REST API
   >
   > ```bash theme={null}
   > curl --request GET \
   >   --url 'https://api.nebius.cloud/mk8s/v1/clusters/get-by-name' \
   >   --get \
   >   --data-urlencode "parentId=<project_ID>" \
   >   --data-urlencode "name=saturn-cluster" \
   >   --header "Authorization: Bearer <access_token>" \
   >   | jq -r '.metadata.id'
   > ```

   Save the received ID. The disks of the workspaces have the cluster ID in their labels. After Terraform deletes the cluster, use this ID to find these disks.

4. Delete the resources that Terraform created:

   ```bash theme={null}
   terraform destroy
   ```

   The command can fail with the `Error uninstalling release` error. In this case, run the command again.

5. Get the IDs of the disks that the cluster created for Saturn Cloud workspaces:

   > [tab] CLI
   >
   > ```bash theme={null}
   > nebius compute disk list \
   >   --format json \
   >   | jq -r --arg CLUSTER_ID "<cluster_ID>" '.items[]?
   >     | select(.metadata.labels["compute.csi.nebius.com/cluster-id"] == $CLUSTER_ID)
   >     | .metadata.id'
   > ```

   > [tab] Go SDK
   >
   > ```go theme={null}
   > diskService := sdk.Services().Compute().V1().Disk()
   > clusterLabel := "compute.csi.nebius.com/cluster-id"
   > disks, err := diskService.List(
   >     ctx,
   >     &compute.ListDisksRequest{
   >         ParentId: "<project_ID>",
   >     },
   > )
   > if err != nil {
   >     return err
   > }
   > for _, disk := range disks.GetItems() {
   >     labels := disk.GetMetadata().GetLabels()
   >     if labels[clusterLabel] == "<cluster_ID>" {
   >         fmt.Println(disk.GetMetadata().GetId())
   >     }
   > }
   > ```

   > [tab] Python SDK
   >
   > ```python theme={null}
   > disk_service = DiskServiceClient(sdk)
   > cluster_label = "compute.csi.nebius.com/cluster-id"
   > disks = await disk_service.list(
   >     ListDisksRequest(parent_id="<project_ID>"),
   > )
   > for disk in disks.items:
   >     if (
   >         disk.metadata.labels.get(cluster_label)
   >         == "<cluster_ID>"
   >     ):
   >         print(disk.metadata.id)
   > ```

   > [tab] JavaScript SDK
   >
   > ```ts theme={null}
   > const diskService = new DiskService(sdk);
   > const clusterLabel = "compute.csi.nebius.com/cluster-id";
   > const disks = await diskService.list(
   >   ListDisksRequest.create({
   >     parentId: "<project_ID>",
   >   }),
   > );
   > for (const disk of disks.items) {
   >   if (
   >     disk.metadata?.labels[clusterLabel]
   >     === "<cluster_ID>"
   >   ) {
   >     console.log(disk.metadata?.id);
   >   }
   > }
   > ```

   > [tab] REST API
   >
   > ```bash theme={null}
   > curl --request GET \
   >   --url 'https://api.nebius.cloud/compute/v1/disks' \
   >   --get \
   >   --data-urlencode "parentId=<project_ID>" \
   >   --header "Authorization: Bearer <access_token>" \
   >   | jq -r --arg CLUSTER_ID "<cluster_ID>" '.items[]?
   >     | select(.metadata.labels["compute.csi.nebius.com/cluster-id"] == $CLUSTER_ID)
   >     | .metadata.id'
   > ```

6. [Delete the disks](https://docs.nebius.com/compute/storage/manage.md#how-to-delete-a-volume) with these IDs.

7. [Delete the bucket](https://docs.nebius.com/object-storage/buckets/manage.md#delete-a-non-empty-bucket-after-a-delay) that stores the Terraform state. Its name starts with `tfstate-saturn-cloud-`.

8. [Delete the service account](https://docs.nebius.com/iam/service-accounts/manage.md#deleting-a-service-account) `saturn-cloud-sa`. Nebius AI Cloud also deletes its access keys and removes it from the `editors` group.

## See also

* [Installation (Nebius)](https://saturncloud.io/docs/enterprise/nebius/) in Saturn Cloud documentation

***

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
