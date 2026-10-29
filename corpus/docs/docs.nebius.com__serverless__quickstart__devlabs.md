# Getting started with Serverless AI Devlabs: Deploy JupyterLab®

Source: https://docs.nebius.com/serverless/quickstart/devlabs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Serverless AI Devlabs: Deploy JupyterLab®

Serverless AI Devlabs provide an interactive environment for coding and prototyping, without the need to manage infrastructure. This quickstart shows how to create a Devlab from the JupyterLab® template and open it in your browser.

## Prerequisites

**Web console**

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: Make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: Make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

**CLI**

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

* In the [Administration → Limits → Quotas](https://console.nebius.com/quota) section, check the following quotas:

  * **Number of virtual machines** (VMs) under **Compute**: Make sure that at least one VM is available.
  * **Allocations** under **Virtual Networks**: Make sure that at least one allocation is available.

  If necessary, [increase the quotas](https://docs.nebius.com/overview/quotas.md#change-quotas).

* [Install](https://docs.nebius.com/cli/install.md) and [configure](https://docs.nebius.com/cli/configure.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
  ```

## Steps

### Create a Devlab

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. Click  **Create Devlab**, choose **Template** and select **JupyterLab**.
3. Review the prefilled Devlab settings. The console generates the Jupyter token automatically. Copy and save the token securely.
4. Click **Create Devlab**.

**CLI**

1. Create a random Jupyter token of exactly 16 alphanumeric characters. For example:

   ```bash theme={null}
   export JUPYTER_TOKEN=$(openssl rand -hex 8)
   ```

2. Create a Devlab from the JupyterLab template:

   ```bash theme={null}
   nebius ai devlab create \
     --name my-jupyter \
     --template jupyter \
     --input jupyter_token=$JUPYTER_TOKEN
   ```

   The command uses the following parameters:

   * `--name`: Devlab name.
   * `--template`: Template to use. In this quickstart, use `jupyter` for the JupyterLab template.
   * `--input jupyter_token=<token>`: Jupyter token that you provide. The token must consist of 16 alphanumeric characters.

   `--platform`, `--preset` and `--disk-size` are optional. If you omit them, the CLI selects the default GPU platform, the smallest suitable preset and a 250 GiB disk.

Wait for the Devlab to start running.

### Open JupyterLab

When the Devlab is running, open its managed HTTPS URL in a browser. A public IP address is not required.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. Open the page of the required Devlab.
3. Wait until the Devlab is running. Then, in the **Network** section, copy the public Devlab address from the **Public Devlabs** field.
4. In a browser, open the URL and enter the Jupyter token in the JupyterLab password field. Use the token that the console generated when you created the Devlab.

**CLI**

1. List Devlabs and find the Devlab that you created (`my-jupyter`):

   ```bash theme={null}
   nebius ai devlab list
   ```

2. Save the Devlab ID to an environment variable:

   ```bash theme={null}
   export DEVLAB_ID=$(nebius ai devlab get-by-name \
     --name my-jupyter \
     --format jsonpath='{.metadata.id}')
   ```

3. Get the Devlab details and copy the HTTPS URL from the output:

   ```bash theme={null}
   nebius ai devlab get "$DEVLAB_ID"
   ```

4. In a browser, open the HTTPS URL and enter the Jupyter token in the JupyterLab password field. Use the `$JUPYTER_TOKEN` value that you set at create time.

### View logs

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. In the Devlab list, next to the Devlab, click **View logs**. Alternatively, click  → **View logs**.

**CLI**

View Devlab logs:

```bash theme={null}
nebius ai devlab logs "$DEVLAB_ID" --follow
```

## Expected results

* The JupyterLab Devlab reaches the **Running** status.
* You can open JupyterLab from the managed HTTPS URL and sign in with the Jupyter token in the password field.
* You can view Devlab logs.

## Delete the Devlab

If you no longer need the Devlab, delete it. Once you delete the Devlab, you will not be charged for its computing resources or container disk.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. In the Devlab list, find the Devlab and click  → **Delete**.
3. Confirm the Devlab deletion.

**CLI**

```bash theme={null}
nebius ai devlab delete "$DEVLAB_ID"
```

## See also

* [Managing Devlabs in Serverless AI](https://docs.nebius.com/serverless/devlabs/manage.md)
* [About Serverless AI](https://docs.nebius.com/serverless/overview.md)

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
