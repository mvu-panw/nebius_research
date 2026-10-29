# Connecting to the JupyterLab® application in Nebius AI Cloud

Source: https://docs.nebius.com/applications/jupyterlab/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Connecting to the JupyterLab® application in Nebius AI Cloud

After [deploying the JupyterLab application](https://docs.nebius.com/applications/jupyterlab/deploy.md) on a Managed Service for Kubernetes® cluster, you can connect to it in the [web console](https://console.nebius.com).

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Download the [Nebius AI Cloud certificate](https://storage.eu-north1.nebius.cloud/msp-certs/ca.pem) and install it according to your operating system instructions.

   You only need the certificate in the following cases:

   * You deployed the application before June 27, 2025, in a project located in the `eu-north1` or `eu-west1` [regions](https://docs.nebius.com/overview/regions.md).
   * You deployed the application before June 30, 2025, in a project located in the `us-central1` region.

   You can find the deployment date on your application's page.

## How to connect

1. In the [web console](https://console.nebius.com), go to  **Applications**.
2. Under **Installed applications**, click on your application.
3. Under **Artifacts**, copy the URL from **Public endpoint**.
4. Go to the URL in your web browser.
5. To log in, enter the credentials from the application creation form: the username that you specified and the password that the form generated.

## What's next

After connecting to the application, you can [work with notebooks](https://docs.nebius.com/applications/jupyterlab/notebooks.md).

***

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
