# Deploying applications in Nebius AI Cloud

Source: https://docs.nebius.com/applications/deploy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying applications in Nebius AI Cloud

To deploy an application in Nebius AI Cloud, browse the Applications marketplace, find the application you want to use and deploy it on a [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/clusters/manage.md) cluster.

Each application is either *in preview* (for testing and feedback, free of charge) or *generally available* (for production environments, usually paid). For more information, see [Service and application stages](https://docs.nebius.com/overview/services.md#service-and-application-stages) in the Nebius AI Cloud overview.

If an application stage is not explicitly marked as in preview, the application is generally available.

## Prerequisites

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

You also need a [Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) with at least one [node group](https://docs.nebius.com/kubernetes/node-groups/manage.md). If you do not have them, you can create them when you deploy the application.

## How to find and deploy an application

1. In the [web console](https://console.nebius.com), go to  **Applications**.

2. Find the application that you need. You can search applications by name or filter them by category.

3. Open the application page by clicking the application card.

4. Click **Deploy on cluster** and configure the application. If you do not have a suitable Managed Kubernetes cluster, you can create one at this step.

5. Click **Deploy application**.

6. Wait until the application status is `Running`. The setup time varies by application configuration.

> [!NOTE]
>
> You can deploy each application in a project once. To deploy an application again, delete its previous deployment first.
