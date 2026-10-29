# Deploying NVIDIA Blueprint for virtual screening in Nebius AI Cloud

Source: https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/deploy

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying NVIDIA Blueprint for virtual screening in Nebius AI Cloud

To work with NVIDIA Blueprint for virtual screening in Nebius AI Cloud, you can deploy it as an application in the [web console](https://console.nebius.com).

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Make sure that you have enough quota for GPUs. The Blueprint requires a minimum of four GPUs to run.
3. [Create a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) that meets the following requirements:

   * A public endpoint is allocated.
   * [A node group has at least four GPUs](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-add-nodes-with-gpus-to-a-cluster).
   * [NVIDIA® GPU Operator](https://console.nebius.com/applications/overview/nebius/nvidia-gpu-operator) and [NVIDIA® Device Plugin](https://console.nebius.com/applications/overview/nebius/nvidia-device-plugin) are deployed on the cluster.

## How to deploy

1. In the [web console](https://console.nebius.com), go to  **Applications**.

2. Find **NVIDIA Blueprint for virtual screening** by searching for it or browsing by category, then open the application page.

3. Click **Deploy on cluster** to deploy using the Kubernetes option.

4. Configure the application:

   1. In **Application name** and **Namespace**, enter unique names for your deployment.
   2. Enter your NGC API key. If you do not yet have an NGC key, see [How to get an NGC Key](#how-to-get-an-ngc-key).
   3. Under **Disk size**, specify a value between `2000 Gi` and `10000 Gi`. At least `2000 Gi` is required to download the models. Disks do not scale automatically, so enter a size that is sufficient for your needs.
   4. In **JupyterHub admin password**, click **Generate** to create a secure password, copy it and then select **I saved the password securely**.
   5. In **JupyterHub accessibility**, choose how the JupyterHub interface can be accessed.

5. Click **Deploy application**.

6. Wait until the application status becomes `Running`. The deployment might take up to three hours.

When deployment completes, a dialog with connection instructions opens. Follow it to get the JupyterHub URL or IP address depending on the selected access method.

## How to get an NGC Key

If you do not yet have an NGC key, you can get one by the following steps:

1. Go to [NVIDIA NGC website](https://ngc.nvidia.com/).
2. Enter your email, password and other necessary credentials to create an account.
3. Once registered, go to [build.nvidia.com](https://build.nvidia.com/) and click **Generate API key**. Follow the steps and copy the API key and paste it in the deployment configuration.

## How to access the Blueprint via JupyterHub

After the application is deployed, you can access it via JupyterHub by IP or by using port forwarding.

### Access by IP

1. [Install](https://kubernetes.io/docs/tasks/tools/#kubectl) and [configure](https://docs.nebius.com/kubernetes/connect.md) `kubectl`.

2. Run the following command to get the external IP address:

   ```bash theme={null}
   kubectl describe svc proxy-public -n <namespace> | grep "LoadBalancer Ingress:"
   ```

3. In your browser, go to `http://<IP>` and log in as **admin**. Use the password that you saved during deployment.

### Access by port forwarding

1. [Install](https://kubernetes.io/docs/tasks/tools/#kubectl) and [configure](https://docs.nebius.com/kubernetes/connect.md) `kubectl`.

2. Set up port forwarding:

   ```bash theme={null}
   kubectl --namespace <namespace> port-forward service/proxy-public 8080:http
   ```

3. Open [http://localhost:8080](http://localhost:8080) in your browser. On the login screen, enter **admin** as the username and use the password that you saved during deployment.

### Managing users

To create and manage users in JupyterHub, do the following:

1. In the JupyterHub top menu, select **File → Hub Control Panel**.
2. Click **Admin → Add Users**.
3. Enter usernames, one per line. To grant a user admin rights, select the **Admin** checkbox.
4. Click **Add Users**.

New users create their own passwords the first time they sign in.

## How to delete the Blueprint

1. In the [web console](https://console.nebius.com), go to  **Applications**.
2. Find the deployed Blueprint in the list and open it.
3. In the application, go to the **Settings** tab.
4. Under **Delete application**, click **Delete**.
5. Confirm the deletion.

## What's next

When the application is running, you can [access it via JupyterHub](#how-to-access-the-blueprint-via-jupyterhub) to run the sample notebook and experiment with the Blueprint.
