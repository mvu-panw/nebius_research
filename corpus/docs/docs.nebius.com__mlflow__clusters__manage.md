# How to create a Managed Service for MLflow cluster

Source: https://docs.nebius.com/mlflow/clusters/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create a Managed Service for MLflow cluster

A Managed Service for MLflow cluster is a hosted MLflow tracking server with its own tracking endpoints, admin credentials for the MLflow UI and a bucket in Object Storage for experiment artifacts. Your training code connects to a tracking endpoint of the cluster to log experiments, metrics and models.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create a cluster

**Web console**

1. In the sidebar, go to  **MLflow**.

2. Click  **Create cluster**.

3. On the page that opens, enter the cluster name and optional description.

4. Select the `mlflow-sa` service account. It was created for Managed MLflow by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud.

5. In the **Access** field, select configuration for *tracking endpoints*:

   * **Public and private**: The cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).
   * **Private only**: The cluster only has a private tracking endpoint.

   URIs of public and private tracking endpoints start with `public-tracking` and `private-tracking`, respectively.

6. Select a network where the cluster should be located.

7. Select a `medium` cluster size.

   Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

8. In the **Bucket for artifacts** block, select a bucket to store logs and metrics of machine learning experiments launched in the cluster.

   Alternatively, select the **Auto** option to create the bucket automatically.

   This bucket is not deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

9. In the **Admin credentials** block, specify the username and password of the cluster administrator.

   The password must be between 8 and 64 characters long and must contain at least the following:

   * One uppercase letter
   * One lowercase letter
   * One digit
   * One special character from **-!@#\$^&\*\_=+:;'"|/?,.\~§±()\[]{}\<>\`**.

10. Click **Create cluster**.

**CLI**

1. Create a password for administrator access to the cluster and save it to an environment variable:

   ```bash theme={null}
   export PASSWORD=<password>
   ```

   The password must be between 8 and 64 characters long and must contain at least the following:

   * One uppercase letter
   * One lowercase letter
   * One digit
   * One special character from **-!@#\$^&\*\_=+:;'"|/?,.\~§±()\[]{}\<>\`**.

2. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud. Save the ID to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account get-by-name \
     --name mlflow-sa \
     --format jsonpath='{.metadata.id}')
   ```

3. Get the ID of the default network and save it to an environment variable:

   ```bash theme={null}
   export NETWORK_ID=$(nebius vpc network get-by-name \
     --name default-network \
     --format jsonpath='{.metadata.id}')
   ```

4. Create a cluster:

   ```bash theme={null}
   nebius msp mlflow v1alpha1 cluster create \
     --name <cluster_name> \
     --description "<cluster_description>" \
     --network-id $NETWORK_ID \
     --size medium \
     --public-access=<true|false> \
     --admin-username <username> \
     --admin-password $PASSWORD \
     --service-account-id $SA_ID \
     --storage-bucket-name <bucket_name>
   ```

   The command contains the following parameters:

   * `--name`: Cluster name.

   * `--description`: Cluster description.

   * `--network-id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

   * `--size`: Size of resources allocated to the cluster. Only `medium` size is available.

     Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

   * `--public-access`: Configuration for tracking endpoints:

     * If `true`, the cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).
     * If `false`, the cluster only has a private tracking endpoint.

     URIs of public and private tracking endpoints start with `public-tracking` and `private-tracking`, respectively.

   * `--admin-username`: Name of the cluster administrator, for example `admin`.

   * `--admin-password`: Administrator password that you set earlier.

   * `--service-account-id`: ID of the `mlflow-sa` service account.

   * `--storage-bucket-name` (optional): Name of the bucket to store logs and metrics from machine learning experiments launched in the cluster. If you do not specify this parameter, a bucket is created automatically.

     This bucket is not deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

**Terraform**

1. Create the following configuration file:

   ```sh theme={null}
   resource "nebius_msp_mlflow_v1alpha1_cluster" "<cluster_name>" {
      name                = "<cluster_name>"
      description         = "<cluster_description>"
      network_id          = "<network_ID>"
      size                = "medium"
      parent_id           = "<project_ID>"
      public_access       = <true|false>
      admin_username      = "<username>"
      admin_password      = "<password>"
      service_account_id  = "<service_account_ID>"
      storage_bucket_name = "<bucket>"
   }
   ```

   The file contains the following parameters:

   * `name`: Cluster name.

   * `description`: Cluster description.

   * `network_id`: [Network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

   * `size`: Size of resources allocated to the cluster. Only `medium` size is available.

     Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).

   * `public_access`: Configuration for tracking endpoints:

     * If `true`, the cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).
     * If `false`, the cluster only has a private tracking endpoint.

     URIs of public and private tracking endpoints start with `public-tracking` and `private-tracking`, respectively.

   * `admin_username`: Name of the cluster administrator, for example `admin`.

   * `admin_password`: Administrator password that you set earlier.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from **-!@#\$^&\*\_=+:;'"|/?,.\~§±()\[]{}\<>\`**.

   * `service_account_id`: ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud.

   * `storage_bucket_name` (optional): Name of the bucket to store logs and metrics from machine learning experiments launched in the cluster. If you do not specify this parameter, a bucket is created automatically.

     This bucket is not deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

2. Check that the configuration is correct:

   ```sh theme={null}
   terraform validate
   ```

3. Apply the changes:

   ```sh theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud:

   ```go theme={null}
   serviceAccount, err := sdk.Services().IAM().V1().
       ServiceAccount().GetByName(
           ctx,
           &iam.GetServiceAccountByNameRequest{
               ParentId: "<project_ID>",
               Name: "mlflow-sa",
           },
       )
   if err != nil {
       return fmt.Errorf("get service account by name: %w", err)
   }
   serviceAccountID := serviceAccount.GetMetadata().GetId()
   fmt.Println(serviceAccountID)
   ```

   In `ParentId`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code prints the service account ID.

2. Get the ID of the default network:

   ```go theme={null}
   network, err := sdk.Services().VPC().V1().Network().
       GetByName(
           ctx,
           &vpc.GetNetworkByNameRequest{
               ParentId: "<project_ID>",
               Name: "default-network",
           },
       )
   if err != nil {
       return fmt.Errorf("get network by name: %w", err)
   }
   networkID := network.GetMetadata().GetId()
   fmt.Println(networkID)
   ```

   The code prints the network ID.

3. Create a cluster:

   ```go theme={null}
   createService := sdk.Services().MSP().MLFlow().
       V1Alpha1().Cluster()
   createOperation, err := createService.Create(
       ctx,
       &mlflow.CreateClusterRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name: "<cluster_name>",
           },
           Spec: &mlflow.ClusterSpec{
               NetworkId: "<network_ID>",
               ServiceAccountId: "<service_account_ID>",
               AdminUsername: "<username>",
               AdminPassword: "<password>",
               PublicAccess: <true|false>,
               Description: "<cluster_description>",
               Size: "medium",
               StorageBucketName: "<bucket_name>",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create cluster: %w", err)
   }
   _, err = createOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for cluster creation: %w", err)
   }
   ```

   The code contains the following parameters:

   * `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * `Metadata.Name`: Cluster name.

   * `Spec.NetworkId`: Network ID that you got earlier.

   * `Spec.ServiceAccountId`: ID of the `mlflow-sa` service account that you got earlier.

   * `Spec.AdminUsername`: Name of the cluster administrator, for example `admin`.

   * `Spec.AdminPassword`: Administrator password.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from **-!@#\$^&\*\_=+:;'"|/?,.\~§±()\[]{}\<>\`**.

   * `Spec.PublicAccess`: Configuration for tracking endpoints:

     * If `true`, the cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).
     * If `false`, the cluster only has a private tracking endpoint.

     URIs of public and private tracking endpoints start with `public-tracking` and `private-tracking`, respectively.

   * `Spec.Description`: Cluster description.

   * `Spec.Size`: Size of resources allocated to the cluster. Only `medium` size is available.

     Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

   * `Spec.StorageBucketName` (optional): Name of the bucket to store logs and metrics from machine learning experiments launched in the cluster. If you don't specify this parameter, a bucket is created automatically.

     This bucket isn't deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

**Python SDK**

1. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud:

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(
           parent_id="<project_ID>",
           name="mlflow-sa",
       ),
   )
   service_account_id = service_account.metadata.id
   print(service_account_id)
   ```

   In `parent_id`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code prints the service account ID.

2. Get the ID of the default network:

   ```python theme={null}
   network_service = NetworkServiceClient(sdk)
   network = await network_service.get_by_name(
       GetNetworkByNameRequest(
           parent_id="<project_ID>",
           name="default-network",
       ),
   )
   network_id = network.metadata.id
   print(network_id)
   ```

   The code prints the network ID.

3. Create a cluster:

   ```python theme={null}
   create_service = mlflow.ClusterServiceClient(sdk)
   create_operation = await create_service.create(
       mlflow.CreateClusterRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="<cluster_name>",
           ),
           spec=mlflow.ClusterSpec(
               network_id="<network_ID>",
               service_account_id="<service_account_ID>",
               admin_username="<username>",
               admin_password="<password>",
               public_access=<True|False>,
               description="<cluster_description>",
               size="medium",
               storage_bucket_name="<bucket_name>",
           ),
       ),
   )
   await create_operation.wait()
   ```

   The code contains the following parameters:

   * `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * `metadata.name`: Cluster name.

   * `spec.network_id`: Network ID that you got earlier.

   * `spec.service_account_id`: ID of the `mlflow-sa` service account that you got earlier.

   * `spec.admin_username`: Name of the cluster administrator, for example `admin`.

   * `spec.admin_password`: Administrator password.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from **-!@#\$^&\*\_=+:;'"|/?,.\~§±()\[]{}\<>\`**.

   * `spec.public_access`: Configuration for tracking endpoints:

     * If `True`, the cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).
     * If `False`, the cluster only has a private tracking endpoint.

     URIs of public and private tracking endpoints start with `public-tracking` and `private-tracking`, respectively.

   * `spec.description`: Cluster description.

   * `spec.size`: Size of resources allocated to the cluster. Only `medium` size is available.

     Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

   * `spec.storage_bucket_name` (optional): Name of the bucket to store logs and metrics from machine learning experiments launched in the cluster. If you don't specify this parameter, a bucket is created automatically.

     This bucket isn't deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

**JavaScript SDK**

1. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud:

   ```ts theme={null}
   const serviceAccountService =
     new ServiceAccountService(sdk);
   const serviceAccount = await serviceAccountService.getByName(
     GetServiceAccountByNameRequest.create({
       parentId: "<project_ID>",
       name: "mlflow-sa",
     }),
   ).result;
   const serviceAccountId = serviceAccount.metadata.id;
   console.log(serviceAccountId);
   ```

   In `parentId`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code prints the service account ID.

2. Get the ID of the default network:

   ```ts theme={null}
   const networkService = new NetworkService(sdk);
   const network = await networkService.getByName(
     GetNetworkByNameRequest.create({
       parentId: "<project_ID>",
       name: "default-network",
     }),
   ).result;
   const networkId = network.metadata.id;
   console.log(networkId);
   ```

   The code prints the network ID.

3. Create a cluster:

   ```ts theme={null}
   const createService = new mlflow.ClusterService(sdk);
   const createOperation = await createService.create(
     mlflow.CreateClusterRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "<cluster_name>",
       },
       spec: {
         networkId: "<network_ID>",
         serviceAccountId: "<service_account_ID>",
         adminUsername: "<username>",
         adminPassword: "<password>",
         publicAccess: <true|false>,
         description: "<cluster_description>",
         size: "medium",
         storageBucketName: "<bucket_name>",
       },
     }),
   ).result;
   await createOperation.wait();
   ```

   The code contains the following parameters:

   * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

   * `metadata.name`: Cluster name.

   * `spec.networkId`: Network ID that you got earlier.

   * `spec.serviceAccountId`: ID of the `mlflow-sa` service account that you got earlier.

   * `spec.adminUsername`: Name of the cluster administrator, for example `admin`.

   * `spec.adminPassword`: Administrator password.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from **-!@#\$^&\*\_=+:;'"|/?,.\~§±()\[]{}\<>\`**.

   * `spec.publicAccess`: Configuration for tracking endpoints:

     * If `true`, the cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).
     * If `false`, the cluster only has a private tracking endpoint.

     URIs of public and private tracking endpoints start with `public-tracking` and `private-tracking`, respectively.

   * `spec.description`: Cluster description.

   * `spec.size`: Size of resources allocated to the cluster. Only `medium` size is available.

     Each `medium` cluster includes 8 vCPUs, 32 GiB RAM and a 200 GiB Network SSD disk.

   * `spec.storageBucketName` (optional): Name of the bucket to store logs and metrics from machine learning experiments launched in the cluster. If you don't specify this parameter, a bucket is created automatically.

     This bucket isn't deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.
