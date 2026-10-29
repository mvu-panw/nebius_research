# How to delete a Managed Service for MLflow cluster

Source: https://docs.nebius.com/mlflow/clusters/delete

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to delete a Managed Service for MLflow cluster

Delete a cluster when you no longer need it to stop incurring compute charges. When you delete a cluster, all data stored in it is permanently deleted. The Object Storage bucket used for artifacts is not deleted automatically. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to delete a cluster

**Web console**

1. In the sidebar, go to  **MLflow**.
2. Open the page of the cluster you want to delete.
3. On the **Settings** tab, click **Delete cluster**.
4. In the window that opens, confirm the deletion.

**CLI**

1. Get the ID of the cluster you want to delete:

   ```bash theme={null}
   nebius msp mlflow v1alpha1 cluster list
   ```

2. Delete the cluster:

   ```bash theme={null}
   nebius msp mlflow v1alpha1 cluster delete <cluster_ID>
   ```

**Terraform**

1. Remove the corresponding `nebius_msp_mlflow_v1alpha1_cluster` resource from the configuration file.
2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```
3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Get the ID of the cluster you want to delete:

   ```go theme={null}
   listService := sdk.Services().MSP().MLFlow().
       V1Alpha1().Cluster()
   clusters, err := listService.List(
       ctx,
       &mlflow.ListClustersRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("list clusters: %w", err)
   }
   fmt.Println(clusters)
   ```

   In `ParentId`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

2. Delete the cluster:

   ```go theme={null}
   deleteService := sdk.Services().MSP().MLFlow().
       V1Alpha1().Cluster()
   deleteOperation, err := deleteService.Delete(
       ctx,
       &mlflow.DeleteClusterRequest{Id: "<cluster_ID>"},
   )
   if err != nil {
       return fmt.Errorf("delete cluster: %w", err)
   }
   _, err = deleteOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for cluster deletion: %w", err)
   }
   ```

   In `Id`, specify the cluster ID. The code waits until the deletion operation completes.

**Python SDK**

1. Get the ID of the cluster you want to delete:

   ```python theme={null}
   list_service = mlflow.ClusterServiceClient(sdk)
   clusters = await list_service.list(
       mlflow.ListClustersRequest(parent_id="<project_ID>"),
   )
   print(clusters)
   ```

   In `parent_id`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

2. Delete the cluster:

   ```python theme={null}
   delete_service = mlflow.ClusterServiceClient(sdk)
   delete_operation = await delete_service.delete(
       mlflow.DeleteClusterRequest(id="<cluster_ID>"),
   )
   await delete_operation.wait()
   ```

   In `id`, specify the cluster ID. The code waits until the deletion operation completes.

**JavaScript SDK**

1. Get the ID of the cluster you want to delete:

   ```ts theme={null}
   const listService = new mlflow.ClusterService(sdk);
   const clusters = await listService.list(
     mlflow.ListClustersRequest.create({
       parentId: "<project_ID>",
     }),
   ).result;
   console.log(clusters);
   ```

   In `parentId`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).

2. Delete the cluster:

   ```ts theme={null}
   const deleteService = new mlflow.ClusterService(sdk);
   const deleteOperation = await deleteService.delete(
     mlflow.DeleteClusterRequest.create({ id: "<cluster_ID>" }),
   ).result;
   await deleteOperation.wait();
   ```

   In `id`, specify the cluster ID. The code waits until the deletion operation completes.
