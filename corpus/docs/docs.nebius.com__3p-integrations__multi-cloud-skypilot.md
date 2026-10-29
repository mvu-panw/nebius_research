# Multi-cloud orchestration in SkyPilot

Source: https://docs.nebius.com/3p-integrations/multi-cloud-skypilot

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Multi-cloud orchestration in SkyPilot

If you prefer using multiple cloud providers, you can connect SkyPilot to third-party clouds, in addition to Nebius AI Cloud. As a result, you can run workloads across different clouds, optimize your costs and more flexibly manage hardware configuration.

You can connect a SkyPilot cluster to Google Cloud, AWS and Runpod when you create a cluster or edit its settings in Nebius AI Cloud. To connect a third-party cloud, get credentials in this cloud and specify them in the SkyPilot cluster configuration.

## How to connect third-party clouds when creating a SkyPilot cluster

1. In the [web console](https://console.nebius.com/), go to  **AI orchestration** → **SkyPilot**.

   If you don't have a SkyPilot cluster yet, the creation page opens.

2. In the **Multi-cloud orchestration** section, add the clouds that you want to connect:

   **Google Cloud**

   1. In Google Cloud, create a service account and grant it the required roles. Then, generate a JSON key for this service account.

      For more information, see [SkyPilot documentation](https://docs.skypilot.ai/en/stable/cloud-setup/cloud-permissions/gcp.html#service-account).

   2. On the SkyPilot cluster form, click  next to Google Cloud.

   3. Add the key to the **Service account key** field. Upload it as a file, or copy and paste its contents as a JSON.

   4. Specify the [project ID](https://support.google.com/googleapi/answer/7014113?hl=en) from Google Cloud.

   **AWS**

   1. In AWS, [create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-key-self-managed.html#Using_CreateAccessKey).

      After it's created, you can get the [access key ID and secret access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html). Save them — you can only retrieve the secret access key right after creation.

   2. On the SkyPilot cluster form, click  next to AWS.

   3. Specify the received data in the **Access key ID** and **Secret access key** fields.

   **Runpod**

   1. In Runpod, [create an API key](https://docs.runpod.io/get-started/api-keys#create-an-api-key).
   2. On the SkyPilot cluster form, click  next to Runpod.
   3. Specify the key in the **API key** field.

3. Click **Create cluster**.

You can only check that the third-party clouds are connected successfully in the SkyPilot web interface after the cluster starts running. To open the web interface, go to the public endpoint of the cluster.

## How to connect third-party clouds when updating a SkyPilot cluster

> [!NOTE]
>
> Connecting third-party clouds restarts the cluster.

1. In the [web console](https://console.nebius.com/), go to  **AI orchestration** → **SkyPilot**.

   If a SkyPilot cluster is created, its page opens.

2. Go to the **Settings** tab.

3. In the **Multi-cloud orchestration** section, add the clouds that you want to connect:

   **Google Cloud**

   1. In Google Cloud, create a service account and grant it the required roles. Then, generate a JSON key for this service account.

      For more information, see [SkyPilot documentation](https://docs.skypilot.ai/en/stable/cloud-setup/cloud-permissions/gcp.html#service-account).

   2. On the SkyPilot cluster form, click  next to Google Cloud.

   3. Add the key to the **Service account key** field. Upload it as a file, or copy and paste its contents as a JSON.

   4. Specify the [project ID](https://support.google.com/googleapi/answer/7014113?hl=en) from Google Cloud.

   **AWS**

   1. In AWS, [create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-key-self-managed.html#Using_CreateAccessKey).

      After it's created, you can get the [access key ID and secret access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html). Save them — you can only retrieve the secret access key right after creation.

   2. On the SkyPilot cluster form, click  next to AWS.

   3. Specify the received data in the **Access key ID** and **Secret access key** fields.

   **Runpod**

   1. In Runpod, [create an API key](https://docs.runpod.io/get-started/api-keys#create-an-api-key).
   2. On the SkyPilot cluster form, click  next to Runpod.
   3. Specify the key in the **API key** field.

4. Click **Save changes**.

   After that, the cluster restarts.

You can only check that the third-party clouds are connected successfully in the SkyPilot web interface after the cluster restarts. To open this web interface, go to the public endpoint of the cluster.

## How to disconnect third-party clouds from a SkyPilot cluster

> [!NOTE]
>
> Disconnecting third-party clouds restarts the cluster.

If you don't need third-party clouds anymore, disconnect them:

1. In the [web console](https://console.nebius.com/), go to  **AI orchestration** → **SkyPilot**.

   The cluster page opens.

2. Go to the **Settings** tab and then check the **Multi-cloud orchestration** section. It shows what clouds are currently added.

3. Next to the cloud that you want to remove, click  → **Remove**.

4. In the window that opens, confirm the action.

5. Click **Save changes**.

   After that, the cluster restarts.
