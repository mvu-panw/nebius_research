# Installation of dstack for AI workload orchestration

Source: https://docs.nebius.com/3p-integrations/dstack

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Installation of dstack for AI workload orchestration

Nebius AI Cloud supports integration with [dstack](https://dstack.ai/docs/). This is an open-source container orchestrator for AI workload management. It is a streamlined alternative to [Slurm](https://slurm.schedmd.com/documentation.html) and [Kubernetes](https://kubernetes.io/docs/home/), and designed especially for AI. For example, by using `dstack` you can develop, train and deploy AI models.

To get started with `dstack`, install its server on your local machine. After that, you can create and deploy `dstack` resources, such as tasks or services.

> [!TIP]
>
> If you don't want to use your local machine, you can [create a Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md) and then [connect to it](https://docs.nebius.com/compute/virtual-machines/connect.md).

## Costs

If you install `dstack` on your local machine, Nebius AI Cloud doesn't charge for the resources required for the `dstack` server installation.

If you use a VM, see the [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md).

## Steps

### Prepare a service account

To configure access to Nebius AI Cloud for the `dstack` server:

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#create-a-service-account).
3. [Add it to a group](https://docs.nebius.com/iam/service-accounts/manage.md#grant-editor-access-to-the-service-account) that has at least the `editor` role within your tenant; for example, the default `editors` group.
4. Upload an authorized key to the created service account:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.

   2. Go to the **Service accounts** tab.

   3. Open the created service account's page.

   4. Go to the **Authorized keys** tab and then click  **Upload authorized key**.

   5. Generate the key:

      ```bash theme={null}
      openssl genrsa -out private.pem 4096 && \
      openssl rsa -in private.pem -outform PEM -pubout \
      -out public.pem
      ```

   6. In the web console, attach the generated `public.pem` file to the service account.

   7. (Optional) Specify the date when the key should expire.

   8. Click the **Upload key** button.

   After that, the key appears in the list of authorized keys.

### Create a configuration file for the `dstack` server

1. Create the `~/.dstack/server/` directory and go into it:

   ```bash theme={null}
   mkdir -p ~/.dstack/server
   cd ~/.dstack/server
   ```

2. Create the following `config.yml` configuration file:

   ```yml theme={null}
   projects:
   - name: main
     backends:
     - type: nebius
       creds:
         type: service_account
         service_account_id: serviceaccount-***
         public_key_id: publickey-***
         private_key_file: <path/to/private.pem>
   ```

   Specify the following parameters:

   * `service_account_id`: ID of the created service account. You can copy the ID from the [Service accounts](https://console.nebius.com/iam/service-accounts) page.
   * `public_key_id`: ID of the uploaded authorized key. To copy the ID, go to the created service account's page and open the **Authorized keys** tab.
   * `private_key_file`: Path to the `private.pem` file. It was generated as part of the authorized key.

### Deploy the configuration file and run the server

1. [Install Python](https://www.python.org/downloads/) version 3.10 or higher.

2. Install `dstack`:

   ```bash theme={null}
   pip3 install "dstack[nebius]" -U
   ```

   If you receive `error: externally-managed-environment`, create a [virtual Python environment](https://docs.python.org/3/library/venv.html) and run this command there. As a result, you install the package isolated from the basic environment.

   Alternatively, run the installation command with the `--break-system-packages` parameter. This option is not as secure as a virtual environment, but it can be useful when you work in a dedicated directory with `dstack` commands. The launch-server command runs in a separate terminal tab in the background until you interrupt it. As a result, you may need to have `dstack` commands available in all the tabs, not only on the tab with the virtual environment.

   > **How to prepare a virtual environment**
   >
   > 1. Create it:
   >
   >    ```bash theme={null}
   >    python3 -m venv <environment_name>
   >    ```
   >
   > 2. Activate the environment:
   >
   >    ```bash theme={null}
   >    source <environment_name>/bin/activate
   >    ```
   >
   >    A directory with the environment name is created.
   >
   > Now, you can install required Python packages. When you no longer need the created virtual environment, run the `deactivate` command and delete the environment directory.

3. Run the `dstack` server:

   ```bash theme={null}
   dstack server
   ```

   > **The command output**
   >
   > ```text theme={null}
   > ╱╱╭╮╱╱╭╮╱╱╱╱╱╱╭╮
   > ╱╱┃┃╱╭╯╰╮╱╱╱╱╱┃┃
   > ╭━╯┣━┻╮╭╋━━┳━━┫┃╭╮
   > ┃╭╮┃━━┫┃┃╭╮┃╭━┫╰╯╯
   > ┃╰╯┣━━┃╰┫╭╮┃╰━┫╭╮╮
   > ╰━━┻━━┻━┻╯╰┻━━┻╯╰╯
   > ╭━━┳━━┳━┳╮╭┳━━┳━╮
   > ┃━━┫┃━┫╭┫╰╯┃┃━┫╭╯
   > ┣━━┃┃━┫┃╰╮╭┫┃━┫┃
   > ╰━━┻━━┻╯╱╰╯╰━━┻╯
   >
   > [12:34:23] INFO     Applying ~/.dstack/server/config.yml...
   > [12:34:27] INFO     dstack._internal.server.services.plugins:77 Found not enabled builtin plugin rest_plugin. Plugin will not be loaded.
   >            INFO     Configured the main project in ~/.dstack/config.yml
   >            INFO     The admin token is ******
   >            INFO     The dstack server 0.19.17 is running at http://127.0.0.1:3000
   > ```
   >
   > You can open the `dstack` web interface by using the provided address and token.

   The command doesn't finish and keeps the server running until you interrupt the command.

4. Create a dedicated directory to work with `dstack`:

   ```bash theme={null}
   mkdir <path/to/new/directory>
   cd <path/to/new/directory>
   ```

5. Initialize the server:

   ```bash theme={null}
   dstack init
   ```

Now, you can start orchestrating your AI workloads.

## What's next

To manage AI workloads, you can configure and operate with `dstack` resources. They allow you to deploy AI models and optimize usage of cloud resources. For more information, see `dstack` documentation for those resources:

* [Dev environments](https://dstack.ai/docs/concepts/dev-environments/)
* [Tasks](https://dstack.ai/docs/concepts/tasks/)
* [Services](https://dstack.ai/docs/concepts/services/)
* [Fleets](https://dstack.ai/docs/concepts/fleets/)

## See also

* [Protips](https://dstack.ai/docs/guides/protips/) in `dstack` documentation
