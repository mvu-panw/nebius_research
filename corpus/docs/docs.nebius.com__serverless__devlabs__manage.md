# Managing Devlabs in Serverless AI

Source: https://docs.nebius.com/serverless/devlabs/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing Devlabs in Serverless AI

*Serverless AI Devlabs* run container images as interactive development environments. They are suitable for coding, prototyping and debugging in the browser, including template-based setups such as code-server, JupyterLab® or ComfyUI. Each Devlab runs on a Compute virtual machine (VM) managed by Serverless AI.

## How to create a Devlab

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

To create an interactive development environment, create a Devlab:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.

2. Click  **Create Devlab**.

3. Specify the Devlab name.

4. Configure **Devlab settings**:

   1. Select **Custom** to provide your own container image, or **Template** to start from a template.

   2. If you selected **Custom**, in **Image path**, set the path to the container image.

   3. If you use a private registry, click  **Add registry** and provide the details for your registry.

   4. In **Ports**, set the container ports for the Devlab. For each port, select **HTTP** or **TCP**. You can add multiple ports. The primary web UI port gets the Devlab's managed HTTPS URL; other ports are shown in the Devlab status but are not publicly routed.

   5. (Optional) In **Entrypoint command**, specify the entrypoint command for the container.

      If you need to pass container arguments, specify them in this field as well.

   6. (Optional) In **Environment variables**, specify environment variables in key-value pairs.

   7. (Optional) In **Secret environment variables**, click  **Create secret** to store a sensitive value in [SecretStash](https://docs.nebius.com/mysterybox/overview.md) and inject it as an environment variable. In the window that opens, specify the **Key** (environment variable name) and **Value** (secret data), then click **Create**.

   8. (Optional) Enable **Bearer token authentication** if you want to protect the Devlab web UI with a token.

      1. Under **Token**, click  **Create**.
      2. In the **Create secret with token** window, specify the secret **Name** and, optionally, a **Description**.
      3. In **Token**, enter a token or click **Generate**. Copy and save the token securely before proceeding. The token is saved as the first value in a [SecretStash](https://docs.nebius.com/mysterybox/overview.md) secret.
      4. Click **Create secret**.

      If token authentication is disabled, anyone with the Devlab URL can access the service.

5. (Optional) In **Platform**, select **With GPUs** or **Without GPUs**, then select the [platform](https://docs.nebius.com/compute/virtual-machines/types.md).

6. (Optional) In **Settings**, select the [preset](https://docs.nebius.com/compute/virtual-machines/types.md). The preset must match the selected platform.

7. (Optional) Configure **Storage** settings:

   * Under **Container disk size**, specify at least 50 GiB for GPU workloads or 20 GiB for CPU-only workloads. If the container image requires a bigger disk size, set at least the minimum required value for the image. Otherwise, the workloads won't be able to launch. For more information, see how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).

     Data under the workspace path on this disk persists across stop and restart. The workspace is a path on the container disk (`/workspace` by default, or the path declared by the template). Its size is limited only by the disk size. While the Devlab is stopped, the entire container disk continues to be billed.

   * Under **Mounted volumes**, click **Attach volume** to attach a bucket or a filesystem. You can create a bucket or filesystem, or use an existing one. To create a new bucket, see [Bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters). To create a new filesystem, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

8. (Optional) In **Files**, upload files or create text files to inject into the container. The maximum file size is 64 KB.

9. Configure the **Network** section:

   * Select a network and a subnet, or create a new subnet.
   * Select the IP address type: **Auto dynamic IP** or **Private IP**.

     A public IP address is not required to open the Devlab web UI over the managed HTTPS URL. If you add an SSH key, make sure that network access allows SSH so you can connect to the VM.

10. Click **Create Devlab**.

**CLI**

1. If you want to create a Devlab from a template, list the available templates and choose one:

   ```bash theme={null}
   nebius ai devlab template list
   ```

2. Create the Devlab. Use either a template or a container image:

   * From a template:

     ```bash theme={null}
     nebius ai devlab create \
       --name <devlab_name> \
       --template <template> \
       --input <key>=<value> \
       --env <key>=<value> \
       --env-secret <key>=<secret_selector> \
       --container-port <port> \
       --workspace-path <absolute_path> \
       --volume <source:container_path[:mode]|s3://bucket:/container_path[:mode[:profile]]> \
       --inject-file "<local_path>:<absolute_container_path>" \
       --platform <platform_ID> \
       --preset <preset> \
       --disk-size <size> \
       --shm-size <size> \
       --subnet-id <subnet_ID> \
       --ssh-key <SSH_public_key> \
       --public
     ```

   > **Example: Create a Devlab from the JupyterLab template**
   >
   > ```bash theme={null}
   > nebius ai devlab create \
   >   --name my-jupyter \
   >   --template jupyter \
   >   --input jupyter_token=A1b2C3d4E5f6G7h8
   > ```
   >
   > Provide your own random Jupyter token as `--input jupyter_token=<token>`. The token must contain exactly 16 alphanumeric characters. For example, you can generate one with `openssl rand -hex 8`.

   * From a container image:

     ```bash theme={null}
     nebius ai devlab create \
       --name <devlab_name> \
       --image <image> \
       --registry-secret <secret_selector> \
       --container-command "<command>" \
       --args "<arguments>" \
       --working-dir <absolute_path> \
       --primary-route-port <port> \
       --env <key>=<value> \
       --env-secret <key>=<secret_selector> \
       --container-port <port> \
       --workspace-path <absolute_path> \
       --volume <source:container_path[:mode]|s3://bucket:/container_path[:mode[:profile]]> \
       --inject-file "<local_path>:<absolute_container_path>" \
       --platform <platform_ID> \
       --preset <preset> \
       --disk-size <size> \
       --shm-size <size> \
       --subnet-id <subnet_ID> \
       --ssh-key <SSH_public_key> \
       --public
     ```

   > **Example: Create a Devlab from a container image**
   >
   > ```bash theme={null}
   > nebius ai devlab create \
   >   --name nginx-devlab \
   >   --image docker.io/library/nginx:1.27-alpine \
   >   --platform cpu-e2 \
   >   --primary-route-port 80
   > ```

In the command, specify the following parameters:

* **Devlab settings:**

  * `--name`: Devlab name.

  * `--template` or `--image`: How to define the container. Specify one of these parameters:

    * `--template`: Template to use, for example, `jupyter`. Mutually exclusive with `--image`. The template declares the container image, entrypoint command, arguments, working directory, ports, primary web route and the default workspace path. Do not set `--image`, `--container-command`, `--args`, `--working-dir` or `--primary-route-port` with `--template`. To see available templates, run `nebius ai devlab template list`.
    * `--image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Mutually exclusive with `--template`. Required unless you set `--template`.

  * `--input` (optional for some templates; required for JupyterLab): Template input in the `key=value` format. Requires `--template`. To set several inputs, repeat the parameter.

    For the JupyterLab template, set `--input jupyter_token=<token>`, where `<token>` is a random string of exactly 16 alphanumeric characters that you provide.

  * `--registry-secret` (optional): [SecretStash](https://docs.nebius.com/mysterybox/overview.md) secret selector with `REGISTRY_USERNAME` and `REGISTRY_PASSWORD` payload keys. You can specify a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`. Use when you pull an image from a private registry. Applies only with `--image`.

  * `--container-command` (optional): Entrypoint command for the container. Applies only with `--image`. Declared by the template when you use `--template`.

  * `--args` (optional): Arguments for the entrypoint command. Applies only with `--image`. Declared by the template when you use `--template`.

  * `--working-dir` (optional): Working directory (absolute path). Applies only with `--image`. Declared by the template when you use `--template`.

  * `--primary-route-port`: Container port for the primary web UI behind the managed HTTPS URL. Required with `--image`. Declared by the template when you use `--template`. Must match an HTTP port from `--container-port`.

  * `--env` (optional): Environment variables for the container in the `key=value` format. To set several variables, repeat the parameter. With `--template`, these variables extend the template-declared ones.

  * `--env-secret` (optional): Environment variables loaded from a [SecretStash](https://docs.nebius.com/mysterybox/overview.md) secret in the `key=secret_selector` format. The value can be a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`. To set several variables, repeat the parameter.

  * `--container-port` (optional): Port to expose from the container, for example, `8080/http` or `9000/tcp`. Supported protocols are `http`, `tcp` and `udp`. To expose several ports, repeat the parameter. With `--template`, these ports extend the template-declared ones. Additional ports appear in the Devlab status but are not publicly routed unless they are the primary web route.

  * `--workspace-path` (optional): Absolute path of the workspace on the container disk. Data under this path persists across stop and restart. The default is `/workspace`. With `--template`, the template can declare a different path. You can set this path in the CLI or API; the web console does not expose it. The path must not overlap mounted volume paths. The workspace size is limited only by the container disk size (`--disk-size`).

  * `--volume` (optional): [Bucket](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the Devlab container. Volume mount paths must not overlap the workspace path.

    Specify the value in either format:

    * `source:container_path[:mode]` for mounting Nebius shared filesystems and existing bucket or volume resources by ID or name.
    * `s3://bucket:/container_path[:mode[:profile]]` for mounting an Object Storage bucket with AWS profile credentials or S3 credentials stored in SecretStash. The `profile` is the AWS credentials profile to use. If you manage your credentials with [SecretStash](https://docs.nebius.com/mysterybox/overview.md), use `profile@<secret_selector>`, where `<secret_selector>` is a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`

    The supported modes are `ro`, read only, and `rw`, read-write (default). Repeat for multiple volumes. For example:

    ```bash theme={null}
    --volume 'computefilesystem-e***:/input:ro' \
    --volume 'storagebucket-e***:/output:rw' \
    --volume 's3://training-results:/output:rw:default'
    ```

  * `--inject-file` (optional): Mount a local file into the Devlab container at launch. Use the format `<local_path>:<absolute_container_path>`. To inject multiple files, repeat the parameter. The mounted file is read-only and limited to 64 KiB.

* **Underlying VM characteristics:**

  * `--platform` (optional): VM platform. If you omit the parameter, the CLI selects the default GPU platform. For CPU-only templates, such as Open WebUI, specify a CPU platform explicitly. See available platforms in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `--preset` (optional): Number of GPUs, vCPUs and RAM allocated to the container. If you omit the parameter, the CLI selects the smallest suitable preset for the platform. The preset must match the selected platform. See available presets in [Presets for GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).

  * `--disk-size` (optional): Disk size of the underlying VM, for example, `100Gi`, `500Gi` or `1Ti`. If you omit the parameter, the default value `250Gi` applies.

    Set at least 50 GiB for GPU workloads or 20 GiB for CPU-only workloads. If the container image requires a bigger disk size, set at least the minimum required value for the image. Otherwise, the workloads won't be able to launch.

    For more information, see how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).

  * `--shm-size` (optional): Shared memory size of `/dev/shm`, for example, `64Mi`, `128Mi` or `1Gi`. With `--template`, you can set this only when the template leaves shared memory unset.

  * `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the Devlab. Required if the project has multiple subnets.

  * `--ssh-key` (optional): SSH public key to access the underlying VM by SSH. When you add an SSH key, a public dynamic IP address is assigned. Before you add the key, check the quota on the number of public IP addresses in the [web console](https://console.nebius.com/quota).

  * `--public` (optional): Assigns a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM. Not required to open the Devlab web UI over the managed HTTPS URL.

Devlab creation usually takes a few minutes. When the Devlab is running, you can open its web UI and view logs.

## How to open a Devlab

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

When a Devlab is running, you can open its web UI over a managed HTTPS URL. A public IP address is not required. If you configured an SSH key and network access that allows SSH, you can also [connect to the VM by SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. Open the page of the required Devlab.
3. Wait until the Devlab is running. Then, in the **Network** section, copy the public Devlab address from the **Public Devlabs** field.
4. In a browser, open the URL. For the JupyterLab template, enter the Jupyter token in the JupyterLab password field. If you created the Devlab in the console, use the token that the console generated.

**CLI**

1. List Devlabs and copy the required ID:

   ```bash theme={null}
   nebius ai devlab list
   ```

   You can also copy the Devlab ID from the overview page in the web console. The ID is shown under the Devlab name.

2. Get the Devlab details and copy the HTTPS URL from the output:

   ```bash theme={null}
   nebius ai devlab get <devlab_ID>
   ```

3. In a browser, open the HTTPS URL. For the JupyterLab template, enter the `jupyter_token` value that you set at create time in the JupyterLab password field.

## How to check Devlab logs

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

To view logs from a running or stopped Devlab:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. Next to the Devlab, click **View logs**. Alternatively, select the Devlab and switch to the **Logs** tab.

You can use the period or log-level filters to filter the logs. You can also use the [LogQL query language](https://docs.nebius.com/observability/logs/query-language.md).

**CLI**

Run the following command:

```bash theme={null}
nebius ai devlab logs <devlab_ID> --follow
```

## How to delete a Devlab

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

When you delete a Devlab, Serverless AI automatically deletes its VM and container disk.

If you no longer need the Devlab, delete it:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Devlabs**.
2. Find the Devlab and then click  → **Delete**.
3. In the window that opens, confirm the deletion.

**CLI**

1. List Devlabs and copy the required ID:

   ```bash theme={null}
   nebius ai devlab list
   ```

2. Delete the Devlab:

   ```bash theme={null}
   nebius ai devlab delete <devlab_ID>
   ```

If the Devlab uses additional volumes, they are not deleted with it. You can remove the mounted volumes manually. See the guides on [deleting a filesystem](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md#how-to-delete-the-created-resources) and [deleting a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets).

## See also

* [How to stop and restart a Devlab](https://docs.nebius.com/serverless/maintenance/stop-start.md#devlabs)

***

*"Jupyter" and the Jupyter logos are trademarks or registered trademarks of LF Charities, used by Nebius B.V. with permission.*
