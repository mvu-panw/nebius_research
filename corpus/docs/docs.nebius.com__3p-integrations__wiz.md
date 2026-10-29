# Connecting Wiz to Nebius AI Cloud

Source: https://docs.nebius.com/3p-integrations/wiz

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Connecting Wiz to Nebius AI Cloud

Nebius AI Cloud supports integration with [Wiz](https://www.wiz.io), a cloud security platform that inventories cloud resources and assesses how they are configured. Wiz collects information about your resources in Compute, Managed Service for Kubernetes®, Virtual Networks and Object Storage to detect misconfigurations and notify you about them.

To scan a Nebius AI Cloud tenant, Wiz uses a *connector* that authenticates as a Nebius AI Cloud [service account](https://docs.nebius.com/iam/service-accounts/authentication.md) and makes read-only API requests. One connector covers a single tenant and discovers the projects that its service account can access, including the projects that you create later.

This guide explains how to prepare the Nebius AI Cloud side of the connection: create a service account for Wiz, give it read access to your resources and issue an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) for it. After that, you pass the credentials of the service account to Wiz.

> [!NOTE]
>
> For Nebius AI Cloud, Wiz agentless disk scanning is unavailable. Only scanning through the API is supported.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. Get access to [Wiz](https://app.wiz.io) by using a role that has write permissions for deployments.

   For more details, see the [Wiz documentation](https://docs.wiz.io/docs/user-roles-settings) (requires logging in).

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

4. Get access to [Wiz](https://app.wiz.io) by using a role that has write permissions for deployments.

   For more details, see the [Wiz documentation](https://docs.wiz.io/docs/user-roles-settings).

## Steps

### Create a service account

Create a dedicated service account for Wiz. This way, the access of the connector does not depend on the accounts that you use for other purposes.

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.
2. Click **Create resource** → **Service account**.
3. In the window that opens, specify the service account name (for example, `wiz-scanner`) and select the project.
4. Click **Create and continue**.

**CLI**

Create a service account and save its ID to an environment variable:

```bash theme={null}
export SA_ID=$(nebius iam service-account create \
  --name wiz-scanner \
  --format jsonpath='{.metadata.id}')
```

### Add the service account to the group

The group to which you add the connector's service account manages its access to your resources:

* To let the connector read the configuration of your resources, add the service account to the default `viewers` group. This group has the tenant-wide `viewer` role, so the connector can view the resources of all projects in the tenant. The `viewer` role also provides access to the data in your resources.

* If you want the connector to read the configuration of your resources without access to the data in them, grant the `security-auditor` role to a custom group and add the service account to this group instead. For instructions, see [Managing custom groups](https://docs.nebius.com/iam/authorization/groups/manage.md).

For more details, see [Security roles](https://docs.nebius.com/iam/authorization/roles.md#security).

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.
2. On the **Groups** tab, click the **viewers** group.
3. On the group page, click **Manage** → **Members**.
4. In the window that opens, switch to the **Service accounts** tab.
5. Select the project in which you created the service account.
6. Find the service account and click  **Add** next to its name.

**CLI**

1. Get and copy the ID of the `viewers` group:

   ```bash theme={null}
   nebius iam group get-by-name \
     --name viewers --parent-id <tenant_ID> \
     --format jsonpath='{.metadata.id}'
   ```

   In the command, specify the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).

2. Add the service account to the group:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id <viewers_group_ID> \
     --member-id $SA_ID
   ```

### Create an authorized key

Wiz authenticates as the service account by using an authorized key pair: you upload the public key to Nebius AI Cloud and pass the private key to Wiz.

1. Create a key pair on your local machine:

   ```bash theme={null}
   openssl genrsa -out private.pem 4096 && \
   openssl rsa -in private.pem -outform PEM -pubout -out public.pem
   ```

   This command creates the `public.pem` and `private.pem` key files in the directory where you run it.

2. Upload the public key and get the ID of the created authorized key:

   **Web console**

   1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM**.
   2. Open the **Service accounts** tab.
   3. Open the page of the required service account.
   4. Click  **Upload authorized key**.
   5. Click  **Attach file** and then select `public.pem`.
   6. (Optional) Set an expiration date.
   7. Click **Upload key**.

   The key is displayed on the **Authorized keys** tab.

   On the **Authorized keys** tab, click  next to the ID of the public key that you uploaded. You will specify this ID in Wiz.

   **CLI**

   ```bash theme={null}
   nebius iam auth-public-key create \
     --account-service-account-id $SA_ID \
     --data "$(cat public.pem)" \
     --format jsonpath='{.metadata.id}'
   ```

   The command returns the ID of the authorized key. You will specify this ID in Wiz.

   To set an expiration date for the key, add the `--expires-at` parameter with a timestamp in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format: `--expires-at <YYYY-MM-DDThh:mm:ssZ>`. The date must be in the future.

> [!TIP]
>
> After you pass the private key to Wiz, store it in [SecretStash](https://docs.nebius.com/mysterybox/overview.md) and delete the local copy. This way, the key is kept encrypted and you can access it later without keeping a file on your local machine.

### Create a connector in Wiz

In Wiz, create a connector for Nebius AI Cloud and specify the following values:

* ID of the service account:

  **Web console**

  In the sidebar, go to  **Administration** → **IAM**. On the **Service accounts** tab, find the service account that you created and copy its ID.

  **CLI**

  Get the ID from the environment variable:

  ```bash theme={null}
  echo $SA_ID
  ```

* ID of the authorized key. In Wiz, it is referred to as the public key ID.

* Private key, the `private.pem` file.

In the settings of the connector, you can also select the projects that Wiz scans.

For instructions, follow the [Wiz documentation](https://docs.wiz.io/docs/connect-to-nebius) (requires logging in).

After you create the connector, Wiz starts collecting information about your resources. Every request that the connector makes is attributed to the service account, so you can find these requests in [audit events](https://docs.nebius.com/audit-logs/events/view.md).

## Troubleshooting

### Wiz can't access your resources

If you set an expiration date for the authorized key, the connector stops working after this date. To restore access:

1. In the web console, open the page of the service account and switch to the **Authorized keys** tab.
2. Check the expiration date of the key that the connector uses.
3. If the key has expired, [create a new authorized key](#create-an-authorized-key) for the same service account.
4. In the settings of the connector in Wiz, replace the ID of the authorized key and the private key with the new ones.

## How to revoke access

To stop Wiz from accessing your resources, [delete the service account](https://docs.nebius.com/iam/service-accounts/manage.md#deleting-a-service-account) that you created for the connector. After that, the connector can no longer authenticate to your tenant.
