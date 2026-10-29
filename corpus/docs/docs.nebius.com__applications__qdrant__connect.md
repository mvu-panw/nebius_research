# Connecting to the Qdrant application in Nebius AI Cloud

Source: https://docs.nebius.com/applications/qdrant/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Connecting to the Qdrant application in Nebius AI Cloud

After [deploying](https://docs.nebius.com/applications/deploy.md) the Qdrant application on a Managed Service for Kubernetes® cluster, you can connect to it in the [web console](https://console.nebius.com).

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Download the [Nebius AI Cloud certificate](https://storage.eu-north1.nebius.cloud/msp-certs/ca.pem) and install it according to your operating system instructions.

   You only need the certificate in the following cases:

   * You deployed the application before June 27, 2025, in a project located in the `eu-north1` or `eu-west1` [regions](https://docs.nebius.com/overview/regions.md).
   * You deployed the application before June 30, 2025, in a project located in the `us-central1` region.

   You can find the deployment date on your application's page.

## How to connect

1. In the [web console](https://console.nebius.com), go to  **Applications**.
2. Switch to the **Installed** tab and open your application.
3. Under **Artifacts**, copy the URL from **Public endpoint**.
4. Connect to a Qdrant interface of your choice:

**Web interface**

1. Go to `https://<public_endpoint>/dashboard` in your web browser.
2. To log in, enter the API key (regular or read-only) that the application creation form generated.

**Python**

Call the `QdrantClient()` constructor and specify the URL and the API key (regular or read-only) that the application creation form generated. For example:

```python theme={null}
from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://<public_endpoint>",
    api_key="<API_key>",
)
```

For more details, see the [Python Qdrant client](https://github.com/qdrant/qdrant-client) on GitHub and [Qdrant documentation](https://qdrant.tech/documentation/).

**API**

Send API requests to `https://<public_endpoint>` and use the `api-key` HTTP header to specify the API key (regular or read-only) that the application creation form generated. For example:

```bash theme={null}
curl -X GET 'https://<public_endpoint>/collections' \
  --header 'api-key: <API_key>'
```

For more details, see [Qdrant documentation](https://qdrant.tech/documentation/) and [API reference](https://api.qdrant.tech/).
