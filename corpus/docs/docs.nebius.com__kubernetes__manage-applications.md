# Deploying and deleting applications for Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/manage-applications

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying and deleting applications for Managed Service for Kubernetes®

Nebius AI Cloud provides several applications that you can deploy on [Managed Kubernetes clusters](https://docs.nebius.com/kubernetes/clusters/manage.md). For example, you can deploy a database, a certificate manager or libraries for LLM inference. You can use popular tools, such as [Argo CD](https://argo-cd.readthedocs.io/en/stable/) and [Grafana Loki](https://grafana.com/oss/loki/).

For information about deploying applications, see [Deploying applications in Nebius AI Cloud](https://docs.nebius.com/applications/deploy.md).

Each application requires at least one node group in a cluster. You can create it [beforehand](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups) or during the [application deployment](#how-to-find-and-deploy-an-application).

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to find and deploy an application

To see the list of applications for Managed Kubernetes and deploy an application:

**Web console**

1. In the sidebar, go to  **Applications**.
2. In the **Deployment** dropdown, select **Kubernetes** to see only applications that support Kubernetes deployment.
3. Choose an application, open its page and click **Deploy on cluster**.
4. Configure the application. If you do not have a suitable Managed Kubernetes cluster to deploy the application, you can create a new cluster on this step. The application creates the necessary node groups in the new or existing cluster automatically.
5. Click **Deploy application**.
6. Wait until the statuses of the cluster and application are `Running`.

## How to delete an application

**Web console**

1. In the sidebar, go to  **Applications**.
2. Go to the **Installed** tab to see your deployed applications.
3. Find the application you want to delete and open it.
4. On the application details page, go to the **Settings** tab.
5. Click **Delete application**.
6. To confirm that you want to delete the application, enter its name and click **Delete application**.

When you delete an application, node groups created with it remain in the cluster and are subject to Managed Kubernetes [charges](https://docs.nebius.com/kubernetes/resources/pricing.md) and [quotas](https://docs.nebius.com/kubernetes/resources/quotas-limits.md). If you do not need these node groups, [delete them](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-delete-node-groups).
