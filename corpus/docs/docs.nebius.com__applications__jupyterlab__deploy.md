# Deploying the JupyterLab® application in Nebius AI Cloud

Source: https://docs.nebius.com/applications/jupyterlab/deploy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying the JupyterLab® application in Nebius AI Cloud

To work with JupyterLab notebooks, deploy the JupyterLab application on a [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/clusters/manage.md) cluster in the [web console](https://console.nebius.com).

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

You also need a [Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) with at least one [node group](https://docs.nebius.com/kubernetes/node-groups/manage.md). If you do not have them, you can create them when you deploy the application.

## How to deploy

1. In the [web console](https://console.nebius.com), go to  **Applications**.
2. Find JupyterLab by searching for it or browsing by category, then open the application page.
3. Click **Deploy on cluster**.
4. Configure the application. If you do not have a suitable Managed Kubernetes cluster, you can create one at this step.
5. Click **Deploy application**.
6. Wait until the application status is `Running`.

> [!NOTE]
>
> You can deploy each application in a project once. To deploy an application again, delete its previous deployment first.

## What's next

When the application is running, you can [connect to it](https://docs.nebius.com/applications/jupyterlab/connect.md).

***

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
