# Managing endpoints in Serverless AI

Source: https://docs.nebius.com/serverless/endpoints/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing endpoints in Serverless AI

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
  ```

* Install [jq](https://jqlang.org/) to parse JSON output:

  ```bash Ubuntu theme={null}
  sudo apt-get install jq
  ```

  ```bash macOS theme={null}
  brew install jq
  ```

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

* [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

* [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

* [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**REST API**

* Get an access token to [authenticate to the REST API](https://docs.nebius.com/rest-api/authentication.md).

* Install [jq](https://jqlang.org/) to parse JSON output:

  ```bash Ubuntu theme={null}
  sudo apt-get install jq
  ```

  ```bash macOS theme={null}
  brew install jq
  ```

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create an endpoint

To deploy an AI model, create an endpoint. Serverless AI endpoints run on Compute virtual machines (VMs) managed by Serverless AI. You can access your model by using the endpoint.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.

2. Click  **Create endpoint**.

3. Specify the endpoint name.

4. In **Configuration**, select **Custom**.

5. Configure **Endpoint settings**:

   1. In **Image path**, set the path to the container image.

   2. If you use a private registry, in **Private registry**, select an existing registry or click  **Add** and provide the details for your registry.

   3. In **Ports**, set the container ports for the endpoint. You can add multiple ports.

   4. (Optional) In **Entrypoint command**, specify the entrypoint command for the container.

      If you need to pass container arguments, specify them in this field as well.

   5. (Optional) In **Environment variables**, specify environment variables in key-value pairs.

   6. (Optional) In **Secret environment variables**, click  **Create secret** to store a sensitive value in [SecretStash](https://docs.nebius.com/mysterybox/overview.md) and inject it as an environment variable. In the window that opens, specify the **Key** (environment variable name) and **Value** (secret data), then click **Create**.

   7. (Optional) In **Authentication**, enable token authentication if the endpoint serves production traffic.

      The system generates a token. Copy and save the token securely before proceeding.

      If you are prototyping or testing, you can leave authentication disabled.

6. (Optional) Configure the **Computing resources** section:

   1. Select whether the underlying VM should have GPUs.

   2. Specify the VM type: regular or [preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md).

      VMs without GPUs only support the regular type.

      If the endpoint runs on a preemptible VM, Nebius AI Cloud can revoke the VM at any time. The endpoint stops with the `Preempted` [code](https://docs.nebius.com/serverless/lifecycle.md#endpoint-statuses), but you can [start it](https://docs.nebius.com/serverless/maintenance/stop-start.md#how-to-stop-and-restart-an-endpoint) again after that.

      The VM type doesn't affect how long capacity for an endpoint is being provisioned.

   3. Select the [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

   4. If you selected the preemptible VM type, in **Max price**, select or create a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md), or choose **Follow spot price**.

7. (Optional) Configure **Storage** settings:

   * Under **Container disk size**, specify at least 50 GiB for GPU workloads or 20 GiB for CPU-only workloads. If the container image requires a bigger disk size, set at least the minimum required value for the image. Otherwise, the workloads won't be able to launch.

     For more information, see how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).

   * Under **Mounted volumes**, click **Attach volume** to attach a bucket or a filesystem. You can create a bucket or filesystem, or use an existing one. To create a new bucket, see [Bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters). To create a new filesystem, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

8. (Optional) In the **Files** section, add one or more small configuration files to inject into the container at launch:
   * Select **Upload files** to upload files from your machine, or **Create text files** to enter the file content and click **Create file**.
   * In **Mount path**, specify the absolute path to the file in the container, for example, `/mnt/files/config.yaml`.
     Injected files are read-only and limited to 64 KiB each.

9. (Optional) In the **Access** section, configure **User name and SSH key** to [connect to the running workload for debugging](https://docs.nebius.com/serverless/jobs/failure.md#connect-to-the-container-by-using-ssh).

   You can create new credentials or select existing ones. If you decide to use an existing credential, make sure that the SSH key is stored for the **nebius** username.

10. Configure the **Network** section:
    * Select a subnet or create a new one.
    * Select the IP address type: **Public static IP** or **Private IP**. If you want to connect to the resource from the internet, select **Public static IP**.

11. Click **Create endpoint**.

**CLI**

> [!TIP]
>
> With the command below, you specify all values directly in the command. This is useful for scripts, configuration-driven workflows, continuous integration (CI) and agents. Alternatively, you can run `nebius ai create` to use the interactive flow where the CLI prompts you for parameter values step by step.

To create an endpoint, run the following command:

```bash theme={null}
nebius ai endpoint create \
  --name <endpoint_name> \
  --image <image_path> \
  --registry-username <username> \
  --registry-password <password> \
  --container-command "<command>" \
  --container-port <port> \
  --args "<arguments>" \
  --env "<key=value>" \
  --env-secret <key=secret_selector> \
  --auth token \
  --token <token> \
  --volume "<source:container_path[:mode]|s3://bucket:/container_path[:mode[:profile]]>" \
  --inject-file "<local_path>:<absolute_container_path>" \
  --subnet-id <subnet_ID> \
  --platform <platform_ID> \
  --preset <preset> \
  --disk-size <size> \
  --shm-size <size> \
  --ssh-key "$(cat <path_to_SSH_public_key>)" \
  --preemptible \
  --follows-spot-price \
  --public
```

> **Endpoint creation example**
>
> ```bash theme={null}
> nebius ai endpoint create \
>   --name my-chatbot \
>   --image vllm/vllm-openai:latest \
>   --container-command "python3 -m vllm.entrypoints.openai.api_server" \
>   --container-port 8000 \
>   --env MODEL=llama-3-70b \
>   --auth token \
>   --token df88e*** \
>   --volume "storagebucket-e***:/output:rw" \
>   --inject-file "config.yaml:/etc/app/config.yaml" \
>   --subnet-id vpcsubnet-e*** \
>   --platform gpu-h100-sxm \
>   --preset 1gpu-16vcpu-200gb \
>   --disk-size 250Gi \
>   --shm-size 128Mi \
>   --ssh-key "$(cat ~/.ssh/id_ed25519.pub)" \
>   --public
> ```

In the command, specify the following parameters:

* **Endpoint characteristics:**

  * `--name`: Endpoint name.

  - `--image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  - `--registry-username`, `--registry-password` (optional): Credentials to authenticate if you pull an image from a private registry. Alternatively, use `--registry-secret` for credentials stored in [SecretStash](https://docs.nebius.com/mysterybox/index.md).

    * `--registry-username`: Username.
    * `--registry-password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  - `--registry-secret` (optional): [SecretStash secret](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions) selector with `registry_username` and `registry_password` payload keys. You can specify a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`.
  - `--container-command` (optional): Entrypoint command for the container.
  - `--args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  - `--env` (optional): Environment variables for the container. Set them in the `key=value` format where `key` is the environment variable and the `value` is the value of this variable. If you need to set several variables, list the `key=value` pairs separated by commas.
  - `--env-secret` (optional): Environment variables loaded from a [SecretStash secret](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions). Set them in the `key=secret_selector` format, where `key` is the environment variable name and must match a [payload](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions) key in the secret, and `secret_selector` is a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`. If you need to set several variables, list the pairs separated by commas. You cannot use the same `key` in both `--env` and `--env-secret`.

  * `--container-port` (optional): Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
  * `--auth` (optional): Authentication method.

    If the parameter isn't set (default), no authentication is required. Useful when you want to create an endpoint prototype and test it.

    If you set `--auth token`, you enable authentication. Useful for production purposes. When you [call the endpoint](#how-to-call-an-endpoint), specify the token in the `"Authorization: Bearer <token>"` HTTP header. Use `--token` or `--token-secret` to configure the token. If you don't provide either, the CLI generates a random token.

    * `--token` (optional): Token for authentication. To generate one manually, run `openssl rand -hex 32`. If you don't provide `--token`, the CLI generates one for you.
    * `--token-secret` (optional): [SecretStash](https://docs.nebius.com/mysterybox/overview.md) secret selector with the `AUTH_TOKEN` payload key. You can specify a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`.
  * `--inject-file` (optional): Mount a local file into the endpoint container at launch. Use the format `<local_path>:<absolute_container_path>`. To inject multiple files, repeat the parameter. The mounted file is read-only and limited to 64 KiB.
  * `--volume` (optional): [Bucket](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the endpoint container. You can use volumes to store model files and other endpoint artifacts.

    Specify the value in either format:

    * `source:container_path[:mode]` for mounting Nebius shared filesystems and existing bucket or volume resources by ID or name.
    * `s3://bucket:/container_path[:mode[:profile]]` for mounting an Object Storage bucket with AWS profile credentials or S3 credentials stored in SecretStash. The `profile` is the AWS credentials profile to use. If you manage your credentials with [SecretStash](https://docs.nebius.com/mysterybox/overview.md), use `profile@<secret_selector>`, where `<secret_selector>` is a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`

    The supported modes are `ro`, read only, and `rw`, read-write (default). Repeat for multiple volumes. For example:

    ```bash theme={null}
    --volume 'computefilesystem-e***:/input:ro' \
    --volume 'storagebucket-e***:/output:rw' \
    --volume 's3://training-results:/output:rw:default'
    ```

  In `source`, you can specify either the volume ID or its name.

* **Underlying VM characteristics:**

  * `--subnet-id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id). Required if the project has multiple subnets.

  * `--platform`: VM platform. See available platforms in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).

  * `--preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform. See available presets in [Presets for GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).

  * `--disk-size`: Disk size of the underlying VM. Specify the value such as `100Gi`, `500Gi` or `1Ti`. The default value is `250Gi`.

    Set at least 50 GiB for GPU workloads or 20 GiB for CPU-only workloads. If the container image requires a bigger disk size, set at least the minimum required value for the image. Otherwise, the workloads won't be able to launch.

    For more information, see how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).

  * `--shm-size` (optional): Shared memory size of `/dev/shm`. Specify the value such as `64Mi`, `128Mi` or `1Gi`. The default value is `16Gi`.

  * `--ssh-key` (optional): SSH key to access the underlying VM by SSH. When you add an SSH key, a public dynamic IP address is assigned. Before you add the key, check the quota on the number of public IP addresses in the [web console](https://console.nebius.com/quota).

  * `--preemptible` (optional): Use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Requires `--follows-spot-price` or `--spot-pricing-policy-id`. Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If you omit this parameter, the container runs on a regular VM.

  * `--spot-pricing-policy-id` (optional): [Pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) ID that sets the maximum price you agree to pay for the preemptible VM. Requires `--preemptible`. Mutually exclusive with `--follows-spot-price` and `--on-demand`.

  * `--follows-spot-price` (optional): Accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for the preemptible VM, with no maximum price. Requires `--preemptible`. Mutually exclusive with `--spot-pricing-policy-id` and `--on-demand`.

  * `--on-demand` (optional): Run on a regular, non-preemptible VM. This is the default when you omit `--preemptible`. Cannot be combined with `--preemptible`, `--spot-pricing-policy-id` or `--follows-spot-price`.

  - `--public` (optional): Assigns a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM. Not required to reach the endpoint from the internet, because each HTTP port is available through the endpoint's managed HTTPS URL.

**Go SDK**

Run the following code:

```go theme={null}
fileContent, err := os.ReadFile("<local_path>")
if err != nil {
    return fmt.Errorf("read injected file: %w", err)
}
sshKey, err := os.ReadFile("<path_to_SSH_public_key>")
if err != nil {
    return fmt.Errorf("read SSH public key: %w", err)
}
endpointSpotPricing := &ai.PricingModelSpec{
    Model: &ai.PricingModelSpec_FollowsSpotPrice{
        FollowsSpotPrice: &ai.FollowsSpotPriceSpec{},
    },
}
createEndpointService := sdk.Services().Ai().V1().Endpoint()
createEndpointOperation, err := createEndpointService.Create(
    ctx,
    &ai.CreateEndpointRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name:     "<endpoint_name>",
        },
        Spec: &ai.EndpointSpec{
            Image:            "<image_path>",
            ContainerCommand: "<command>",
            Args:             "<arguments>",
            EnvironmentVariables:
                []*ai.EndpointSpec_EnvironmentVariable{
                    {
                        Name:  "<environment_variable_name>",
                        Value: "<environment_variable_value>",
                    },
                    {
                        Name: "<environment_variable_name>",
                        MysteryboxSecret:
                            &ai.EndpointSpec_MysteryBoxSecretRef{
                                SecretId:  "<secret_ID>",
                                VersionId: "<version_ID>",
                            },
                    },
                },
            Ports: []*ai.EndpointSpec_Port{
                {
                    ContainerPort: <port>,
                    Protocol: ai.EndpointSpec_Port_HTTP,
                },
            },
            AuthToken: "<token>",
            Volumes: []*ai.EndpointSpec_VolumeMount{
                {
                    Source: "<source>",
                    ContainerPath:
                        "<absolute_container_path>",
                    Mode: ai.EndpointSpec_VolumeMount_READ_WRITE,
                },
            },
            RegistryCredentials: &ai.EndpointSpec_RegistryCredentials{
                Username: "<username>",
                Password: "<password>",
            },
            InjectedFiles: []*ai.EndpointSpec_FileInjection{
                {
                    ContainerPath: "<absolute_container_path>",
                    Content:       fileContent,
                },
            },
            SubnetId:            "<subnet_ID>",
            Platform:            "<platform_ID>",
            Preset:              "<preset>",
            Disk: &ai.EndpointSpec_DiskSpec{
                Type:      compute.DiskSpec_NETWORK_SSD,
                SizeBytes: <disk_size_in_bytes>,
            },
            ShmSizeBytes:     <shared_memory_size_in_bytes>,
            SshAuthorizedKeys: []string{string(sshKey)},
            Preemptible:      true,
            PricingModel:     endpointSpotPricing,
            PublicIp:         true,
        },
    },
)
if err != nil {
    return fmt.Errorf("create endpoint: %w", err)
}
if _, err = createEndpointOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for endpoint creation: %w", err)
}
```

> **Endpoint creation example**
>
> ```go theme={null}
> exampleVolume := "storagebucket-e***:/output:rw"
> exampleModeIndex := strings.LastIndex(exampleVolume, ":")
> if exampleModeIndex < 0 {
>     return fmt.Errorf("volume must include a mount mode")
> }
> exampleVolumePath := exampleVolume[:exampleModeIndex]
> examplePathIndex := strings.LastIndex(exampleVolumePath, ":")
> if examplePathIndex < 0 {
>     return fmt.Errorf("volume must include a container path")
> }
> exampleSource := exampleVolumePath[:examplePathIndex]
> examplePath := exampleVolumePath[examplePathIndex+1:]
> exampleFileContent, err := os.ReadFile("config.yaml")
> if err != nil {
>     return fmt.Errorf("read injected file: %w", err)
> }
> homeDir, err := os.UserHomeDir()
> if err != nil {
>     return fmt.Errorf("get home directory: %w", err)
> }
> exampleSSHKey, err := os.ReadFile(
>     filepath.Join(homeDir, ".ssh", "id_ed25519.pub"),
> )
> if err != nil {
>     return fmt.Errorf("read SSH public key: %w", err)
> }
> exampleEndpointService := sdk.Services().Ai().V1().Endpoint()
> exampleEndpointOperation, err := exampleEndpointService.Create(
>     ctx,
>     &ai.CreateEndpointRequest{
>         Metadata: &common.ResourceMetadata{
>             Name:     "my-chatbot",
>         },
>         Spec: &ai.EndpointSpec{
>             Image: "vllm/vllm-openai:latest",
>             ContainerCommand:
>                 "python3 -m vllm.entrypoints.openai.api_server",
>             EnvironmentVariables:
>                 []*ai.EndpointSpec_EnvironmentVariable{
>                     {
>                         Name:  "MODEL",
>                         Value: "llama-3-70b",
>                     },
>                 },
>             Ports: []*ai.EndpointSpec_Port{
>                 {
>                     ContainerPort: 8000,
>                     Protocol: ai.EndpointSpec_Port_HTTP,
>                 },
>             },
>             AuthToken: "df88e***",
>             Volumes: []*ai.EndpointSpec_VolumeMount{
>                 {
>                     Source:        exampleSource,
>                     ContainerPath: examplePath,
>                     Mode:
>                         ai.EndpointSpec_VolumeMount_READ_WRITE,
>                 },
>             },
>             InjectedFiles: []*ai.EndpointSpec_FileInjection{
>                 {
>                     ContainerPath: "/etc/app/config.yaml",
>                     Content:       exampleFileContent,
>                 },
>             },
>             SubnetId:      "vpcsubnet-e***",
>             Platform:      "gpu-h100-sxm",
>             Preset:        "1gpu-16vcpu-200gb",
>             Disk: &ai.EndpointSpec_DiskSpec{
>                 Type: compute.DiskSpec_NETWORK_SSD,
>                 SizeBytes: 268435456000,
>             },
>             ShmSizeBytes: 134217728,
>             SshAuthorizedKeys:
>                 []string{string(exampleSSHKey)},
>             PublicIp: true,
>         },
>     },
> )
> if err != nil {
>     return fmt.Errorf("create example endpoint: %w", err)
> }
> if _, err = exampleEndpointOperation.Wait(ctx); err != nil {
>     return fmt.Errorf("wait for example endpoint: %w", err)
> }
> ```

In the code, set the following parameters:

* **Endpoint characteristics:**

  * `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
  * `Metadata.Name`: Endpoint name.
  * `Spec.Image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  * `Spec.ContainerCommand` (optional): Entrypoint command for the container.
  * `Spec.Args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  * `Spec.EnvironmentVariables` (optional): Environment variables for the container.
    * `Spec.EnvironmentVariables[].Name`: Environment variable name.
    * `Spec.EnvironmentVariables[].Value`: Environment variable value.
    * `Spec.EnvironmentVariables[].MysteryboxSecret`: Secret to read the value from instead of `Value`. Set `SecretId` and `VersionId` to the ID and version ID of the secret.
  * `Spec.Ports` (optional): Ports that the endpoint exposes.
    * `Spec.Ports[].ContainerPort`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
    * `Spec.Ports[].Protocol`: Protocol used by the exposed port.
  * `Spec.AuthToken` (optional): Token for authentication. To generate one manually, run `openssl rand -hex 32`. If omitted, authentication is disabled.
  * `Spec.Volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the endpoint container. You can use volumes to store model files and other endpoint artifacts.
    * `Spec.Volumes[].Source`: Volume ID or name.
    * `Spec.Volumes[].ContainerPath`: Absolute path where the volume is mounted in the container.
    * `Spec.Volumes[].Mode`: Mount mode: `ai.EndpointSpec_VolumeMount_READ_ONLY` or `ai.EndpointSpec_VolumeMount_READ_WRITE`.
  * `Spec.RegistryCredentials` (optional): Credentials to authenticate if you pull an image from a private registry.

    * `Spec.RegistryCredentials.Username`: Username.
    * `Spec.RegistryCredentials.Password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  * `Spec.InjectedFiles` (optional): Files to mount into the endpoint container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
    * `Spec.InjectedFiles[].ContainerPath`: Absolute path where the file is mounted in the container.
    * `Spec.InjectedFiles[].Content`: Content of the file as a byte slice, for example read from disk with `os.ReadFile`.

* **Underlying VM characteristics:**

  * `Spec.SubnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#go-sdk-3). Required if the project has multiple subnets.
  * `Spec.Platform`: VM platform. See available platforms in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).
  * `Spec.Preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform. See available presets in [Presets for GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).
  * `Spec.Disk.Type`: Disk type for the underlying VM.
  * `Spec.Disk.SizeBytes`: Disk size of the underlying VM in bytes. The default value is 250 GiB. See how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).
  * `Spec.ShmSizeBytes` (optional): Shared memory size of `/dev/shm` in bytes. The default value is 16 GiB.
  * `Spec.SshAuthorizedKeys` (optional): SSH public keys to access the underlying VM by SSH. When you add an SSH key, a public dynamic IP address is assigned. Before you add the key, check the quota on the number of public IP addresses in the [web console](https://console.nebius.com/quota).
  * `Spec.Preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `false`, the container runs on a regular VM.
  * `Spec.PricingModel` (optional): Pricing model for the VM. It must match `Spec.Preemptible`: use `OnDemand` for a regular VM. For a preemptible VM, use `FollowsSpotPrice` or `SpotPricingPolicy`. Set `Spec.PricingModel.Model` to one of:
    * `&ai.PricingModelSpec_OnDemand{OnDemand: &ai.OnDemandSpec{}}`: Regular, non-preemptible VM.
    * `&ai.PricingModelSpec_FollowsSpotPrice{FollowsSpotPrice: &ai.FollowsSpotPriceSpec{}}`: Accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price. The code sets this model.
    * `&ai.PricingModelSpec_SpotPricingPolicy{SpotPricingPolicy: &ai.SpotPricingPolicySpec{Id: "<policy_ID>"}}`: Use the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) with the specified ID to set the maximum price for a preemptible VM.
  * `Spec.PublicIp` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM. A public IP address isn't required to reach the endpoint through its managed HTTPS URL.

**Python SDK**

Run the following code:

```python theme={null}
ssh_key = (
    Path("<path_to_SSH_public_key>").read_text().strip()
)
create_endpoint_service = EndpointServiceClient(sdk)
create_endpoint_operation = await create_endpoint_service.create(
    CreateEndpointRequest(
        metadata=ResourceMetadata(
            parent_id="<project_ID>",
            name="<endpoint_name>",
        ),
        spec=EndpointSpec(
            image="<image_path>",
            container_command="<command>",
            args="<arguments>",
            environment_variables=[
                EndpointSpec__EnvironmentVariable(
                    name="<environment_variable_name>",
                    value="<environment_variable_value>",
                ),
                EndpointSpec__EnvironmentVariable(
                    name="<environment_variable_name>",
                    mysterybox_secret=(
                        EndpointSpec__MysteryBoxSecretRef(
                            secret_id="<secret_ID>",
                            version_id="<version_ID>",
                        )
                    ),
                ),
            ],
            ports=[
                EndpointSpec__Port(
                    container_port=<port>,
                    protocol=(
                        EndpointSpec__Port__Protocol.HTTP
                    ),
                ),
            ],
            auth_token="<token>",
            volumes=[
                EndpointSpec__VolumeMount(
                    source="<source>",
                    container_path=(
                        "<absolute_container_path>"
                    ),
                    mode=EndpointSpec__VolumeMount__Mode.READ_WRITE,
                ),
            ],
            registry_credentials=EndpointSpec__RegistryCredentials(
                username="<username>",
                password="<password>",
            ),
            injected_files=[
                EndpointSpec__FileInjection(
                    container_path="<absolute_container_path>",
                    content=Path("<local_path>").read_bytes(),
                ),
            ],
            subnet_id="<subnet_ID>",
            platform="<platform_ID>",
            preset="<preset>",
            disk=EndpointSpec__DiskSpec(
                type=DiskSpec__DiskType.NETWORK_SSD,
                size_bytes=<disk_size_in_bytes>,
            ),
            shm_size_bytes=<shared_memory_size_in_bytes>,
            ssh_authorized_keys=[ssh_key],
            preemptible=True,
            pricing_model=PricingModelSpec(
                follows_spot_price=FollowsSpotPriceSpec(),
            ),
            public_ip=True,
        ),
    ),
)
await create_endpoint_operation.wait()
```

> **Endpoint creation example**
>
> ```python theme={null}
> example_volume = "storagebucket-e***:/output:rw"
> example_mode_index = example_volume.rfind(":")
> if example_mode_index < 0:
>     raise ValueError("volume must include a mount mode")
> example_volume_path = example_volume[:example_mode_index]
> example_path_index = example_volume_path.rfind(":")
> if example_path_index < 0:
>     raise ValueError("volume must include a container path")
> example_source = example_volume_path[:example_path_index]
> example_path = example_volume_path[example_path_index + 1 :]
> example_ssh_key = (
>     Path.home() / ".ssh" / "id_ed25519.pub"
> ).read_text().strip()
> example_endpoint_service = EndpointServiceClient(sdk)
> example_endpoint_operation = await example_endpoint_service.create(
>     CreateEndpointRequest(
>         metadata=ResourceMetadata(
>             name="my-chatbot",
>         ),
>         spec=EndpointSpec(
>             image="vllm/vllm-openai:latest",
>             container_command=(
>                 "python3 -m vllm.entrypoints.openai.api_server"
>             ),
>             environment_variables=[
>                 EndpointSpec__EnvironmentVariable(
>                     name="MODEL",
>                     value="llama-3-70b",
>                 ),
>             ],
>             ports=[
>                 EndpointSpec__Port(
>                     container_port=8000,
>                     protocol=(
>                         EndpointSpec__Port__Protocol.HTTP
>                     ),
>                 ),
>             ],
>             auth_token="df88e***",
>             volumes=[
>                 EndpointSpec__VolumeMount(
>                     source=example_source,
>                     container_path=example_path,
>                     mode=(
>                         EndpointSpec__VolumeMount__Mode.READ_WRITE
>                     ),
>                 ),
>             ],
>             injected_files=[
>                 EndpointSpec__FileInjection(
>                     container_path="/etc/app/config.yaml",
>                     content=Path("config.yaml").read_bytes(),
>                 ),
>             ],
>             subnet_id="vpcsubnet-e***",
>             platform="gpu-h100-sxm",
>             preset="1gpu-16vcpu-200gb",
>             disk=EndpointSpec__DiskSpec(
>                 type=DiskSpec__DiskType.NETWORK_SSD,
>                 size_bytes=268435456000,
>             ),
>             shm_size_bytes=134217728,
>             ssh_authorized_keys=[example_ssh_key],
>             public_ip=True,
>         ),
>     ),
> )
> await example_endpoint_operation.wait()
> ```

In the code, set the following parameters:

* **Endpoint characteristics:**

  * `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
  * `metadata.name`: Endpoint name.
  * `spec.image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  * `spec.container_command` (optional): Entrypoint command for the container.
  * `spec.args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  * `spec.environment_variables` (optional): Environment variables for the container.
    * `spec.environment_variables[].name`: Environment variable name.
    * `spec.environment_variables[].value`: Environment variable value.
    * `spec.environment_variables[].mysterybox_secret`: Secret to read the value from instead of `value`. Set `secret_id` and `version_id` to the ID and version ID of the secret.
  * `spec.ports` (optional): Ports that the endpoint exposes.
    * `spec.ports[].container_port`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
    * `spec.ports[].protocol`: Protocol used by the exposed port.
  * `spec.auth_token` (optional): Token for authentication. To generate one manually, run `openssl rand -hex 32`. If omitted, authentication is disabled.
  * `spec.volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the endpoint container. You can use volumes to store model files and other endpoint artifacts.
    * `spec.volumes[].source`: Volume ID or name.
    * `spec.volumes[].container_path`: Absolute path where the volume is mounted in the container.
    * `spec.volumes[].mode`: Mount mode: `EndpointSpec__VolumeMount__Mode.READ_ONLY` or `EndpointSpec__VolumeMount__Mode.READ_WRITE`.
  * `spec.registry_credentials` (optional): Credentials to authenticate if you pull an image from a private registry.

    * `spec.registry_credentials.username`: Username.
    * `spec.registry_credentials.password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  * `spec.injected_files` (optional): Files to mount into the endpoint container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
    * `spec.injected_files[].container_path`: Absolute path where the file is mounted in the container.
    * `spec.injected_files[].content`: Content of the file as bytes, for example read from disk with `Path(...).read_bytes()`.

* **Underlying VM characteristics:**

  * `spec.subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#python-sdk-3). Required if the project has multiple subnets.
  * `spec.platform`: VM platform. See available platforms in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).
  * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform. See available presets in [Presets for GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).
  * `spec.disk.type`: Disk type for the underlying VM.
  * `spec.disk.size_bytes`: Disk size of the underlying VM in bytes. The default value is 250 GiB. See how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).
  * `spec.shm_size_bytes` (optional): Shared memory size of `/dev/shm` in bytes. The default value is 16 GiB.
  * `spec.ssh_authorized_keys` (optional): SSH public keys to access the underlying VM by SSH. When you add an SSH key, a public dynamic IP address is assigned. Before you add the key, check the quota on the number of public IP addresses in the [web console](https://console.nebius.com/quota).
  * `spec.preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `False`, the container runs on a regular VM.
  * `spec.pricing_model` (optional): Pricing model for the VM. It must match `spec.preemptible`: use `on_demand` for a regular VM. For a preemptible VM, use `follows_spot_price` or `spot_pricing_policy`. Specify one of:
    * `spec.pricing_model.on_demand`: `OnDemandSpec()` for a regular, non-preemptible VM.
    * `spec.pricing_model.follows_spot_price`: `FollowsSpotPriceSpec()` to accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price. The code sets this model.
    * `spec.pricing_model.spot_pricing_policy`: `SpotPricingPolicySpec(id="<policy_ID>")` with the ID of the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) that sets the maximum price for a preemptible VM.
  * `spec.public_ip` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM. A public IP address isn't required to reach the endpoint through its managed HTTPS URL.

**JavaScript SDK**

Run the following code:

```ts theme={null}
const sshKey = await readFile(
  "<path_to_SSH_public_key>",
  "utf8",
);
const createEndpointService = new EndpointService(sdk);
const createEndpointOperation = await createEndpointService.create(
  CreateEndpointRequest.create({
    metadata: {
      parentId: "<project_ID>",
      name: "<endpoint_name>",
    },
    spec: {
      image: "<image_path>",
      containerCommand: "<command>",
      args: "<arguments>",
      environmentVariables: [
        {
          name: "<environment_variable_name>",
          value: "<environment_variable_value>",
        },
        {
          name: "<environment_variable_name>",
          mysteryboxSecret: {
            secretId: "<secret_ID>",
            versionId: "<version_ID>",
          },
        },
      ],
      ports: [
        {
          containerPort: <port>,
          protocol: EndpointSpec_Port_Protocol.HTTP,
        },
      ],
      authToken: "<token>",
      volumes: [
        {
          source: "<source>",
          containerPath: "<absolute_container_path>",
          mode: EndpointSpec_VolumeMount_Mode.READ_WRITE,
        },
      ],
      registryCredentials: {
        username: "<username>",
        password: "<password>",
      },
      injectedFiles: [
        {
          containerPath: "<absolute_container_path>",
          content: await readFile("<local_path>"),
        },
      ],
      subnetId: "<subnet_ID>",
      platform: "<platform_ID>",
      preset: "<preset>",
      disk: {
        type: DiskSpec_DiskType.NETWORK_SSD,
        sizeBytes: BigInt("<disk_size_in_bytes>"),
      },
      shmSizeBytes: BigInt("<shared_memory_size_in_bytes>"),
      sshAuthorizedKeys: [sshKey.trim()],
      preemptible: true,
      pricingModel: {
        model: {
          $case: "followsSpotPrice",
          followsSpotPrice: {},
        },
      },
      publicIp: true,
    },
  }),
).result;
await createEndpointOperation.wait();
```

> **Endpoint creation example**
>
> ```ts theme={null}
> const exampleVolume = "storagebucket-e***:/output:rw";
> const exampleModeIndex = exampleVolume.lastIndexOf(":");
> if (exampleModeIndex < 0) {
>   throw new Error("volume must include a mount mode");
> }
> const exampleVolumePath = exampleVolume.slice(
>   0,
>   exampleModeIndex,
> );
> const examplePathIndex = exampleVolumePath.lastIndexOf(":");
> if (examplePathIndex < 0) {
>   throw new Error("volume must include a container path");
> }
> const exampleSource = exampleVolumePath.slice(
>   0,
>   examplePathIndex,
> );
> const examplePath = exampleVolumePath.slice(
>   examplePathIndex + 1,
> );
> const exampleSSHKey = await readFile(
>   join(homedir(), ".ssh", "id_ed25519.pub"),
>   "utf8",
> );
> const exampleEndpointService = new EndpointService(sdk);
> const exampleEndpointOperation =
>   await exampleEndpointService.create(
>     CreateEndpointRequest.create({
>       metadata: {
>         name: "my-chatbot",
>       },
>       spec: {
>         image: "vllm/vllm-openai:latest",
>         containerCommand:
>           "python3 -m vllm.entrypoints.openai.api_server",
>         environmentVariables: [
>           {
>             name: "MODEL",
>             value: "llama-3-70b",
>           },
>         ],
>         ports: [
>           {
>             containerPort: 8000,
>             protocol: EndpointSpec_Port_Protocol.HTTP,
>           },
>         ],
>         authToken: "df88e***",
>         volumes: [
>           {
>             source: exampleSource,
>             containerPath: examplePath,
>             mode: EndpointSpec_VolumeMount_Mode.READ_WRITE,
>           },
>         ],
>         injectedFiles: [
>           {
>             containerPath: "/etc/app/config.yaml",
>             content: await readFile("config.yaml"),
>           },
>         ],
>         subnetId: "vpcsubnet-e***",
>         platform: "gpu-h100-sxm",
>         preset: "1gpu-16vcpu-200gb",
>         disk: {
>           type: DiskSpec_DiskType.NETWORK_SSD,
>           sizeBytes: BigInt("268435456000"),
>         },
>         shmSizeBytes: BigInt("134217728"),
>         sshAuthorizedKeys: [exampleSSHKey.trim()],
>         publicIp: true,
>       },
>     }),
>   ).result;
> await exampleEndpointOperation.wait();
> ```

In the code, set the following parameters:

* **Endpoint characteristics:**

  * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
  * `metadata.name`: Endpoint name.
  * `spec.image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  * `spec.containerCommand` (optional): Entrypoint command for the container.
  * `spec.args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  * `spec.environmentVariables` (optional): Environment variables for the container.
    * `spec.environmentVariables[].name`: Environment variable name.
    * `spec.environmentVariables[].value`: Environment variable value.
    * `spec.environmentVariables[].mysteryboxSecret`: Secret to read the value from instead of `value`. Set `secretId` and `versionId` to the ID and version ID of the secret.
  * `spec.ports` (optional): Ports that the endpoint exposes.
    * `spec.ports[].containerPort`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
    * `spec.ports[].protocol`: Protocol used by the exposed port.
  * `spec.authToken` (optional): Token for authentication. To generate one manually, run `openssl rand -hex 32`. If omitted, authentication is disabled.
  * `spec.volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the endpoint container. You can use volumes to store model files and other endpoint artifacts.
    * `spec.volumes[].source`: Volume ID or name.
    * `spec.volumes[].containerPath`: Absolute path where the volume is mounted in the container.
    * `spec.volumes[].mode`: Mount mode: `EndpointSpec_VolumeMount_Mode.READ_ONLY` or `EndpointSpec_VolumeMount_Mode.READ_WRITE`.
  * `spec.registryCredentials` (optional): Credentials to authenticate if you pull an image from a private registry.

    * `spec.registryCredentials.username`: Username.
    * `spec.registryCredentials.password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  * `spec.injectedFiles` (optional): Files to mount into the endpoint container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
    * `spec.injectedFiles[].containerPath`: Absolute path where the file is mounted in the container.
    * `spec.injectedFiles[].content`: Content of the file as bytes, for example read from disk with `readFile`.

* **Underlying VM characteristics:**

  * `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#javascript-sdk-3). Required if the project has multiple subnets.
  * `spec.platform`: VM platform. See available platforms in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).
  * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform. See available presets in [Presets for GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).
  * `spec.disk.type`: Disk type for the underlying VM.
  * `spec.disk.sizeBytes`: Disk size of the underlying VM in bytes, as a `bigint`. The default value is 250 GiB. See how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).
  * `spec.shmSizeBytes` (optional): Shared memory size of `/dev/shm` in bytes, as a `bigint`. The default value is 16 GiB.
  * `spec.sshAuthorizedKeys` (optional): SSH public keys to access the underlying VM by SSH. When you add an SSH key, a public dynamic IP address is assigned. Before you add the key, check the quota on the number of public IP addresses in the [web console](https://console.nebius.com/quota).
  * `spec.preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `false`, the container runs on a regular VM.
  * `spec.pricingModel` (optional): Pricing model for the VM. It must match `spec.preemptible`: use `onDemand` for a regular VM. For a preemptible VM, use `followsSpotPrice` or `spotPricingPolicy`. Set `spec.pricingModel.model` to one of:
    * `{ $case: "onDemand", onDemand: {} }`: Regular, non-preemptible VM.
    * `{ $case: "followsSpotPrice", followsSpotPrice: {} }`: Accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price. The code sets this model.
    * `{ $case: "spotPricingPolicy", spotPricingPolicy: { id: "<policy_ID>" } }`: Use the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) with the specified ID to set the maximum price for a preemptible VM.
  * `spec.publicIp` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM. A public IP address isn't required to reach the endpoint through its managed HTTPS URL.

**REST API**

Send the following request:

```bash theme={null}
curl --request POST \
  --url 'https://api.nebius.cloud/ai/v1/endpoints' \
  --header "Authorization: Bearer <access_token>" \
  --header 'Content-Type: application/json' \
  --data '{
    "metadata": {
      "parentId": "<project_ID>",
      "name": "my-endpoint"
    },
    "spec": {
      "image": "<image_path>",
      "registryCredentials": {"username": "<username>", "password": "<password>"},
      "containerCommand": "<command>",
      "args": "<arguments>",
      "environmentVariables": [
        {
          "name": "<environment_variable_name>",
          "value": "<environment_variable_value>"
        }
      ],
      "ports": [
        {
          "containerPort": <port>,
          "protocol": "HTTP"
        }
      ],
      "authToken": "<token>",
      "volumes": [
        {
          "source": "<volume_ID_or_name>",
          "containerPath": "<absolute_container_path>",
          "mode": "<READ_ONLY_or_READ_WRITE>"
        }
      ],
      "injectedFiles": [
        {
          "containerPath": "<absolute_container_path>",
          "content": "<base64_encoded_file_content>"
        }
      ],
      "subnetId": "<subnet_ID>",
      "platform": "<platform_ID>",
      "preset": "<preset>",
      "disk": {
        "type": "NETWORK_SSD",
        "sizeBytes": "<disk_size_in_bytes>"
      },
      "shmSizeBytes": "<shared_memory_size_in_bytes>",
      "sshAuthorizedKeys": [
        "<SSH_public_key>"
      ],
      "preemptible": true,
      "pricingModel": {"followsSpotPrice": {}},
      "publicIp": true
    }
  }'

```

> **Endpoint creation example**
>
> ```bash theme={null}
> curl --request POST \
>   --url 'https://api.nebius.cloud/ai/v1/endpoints' \
>   --header "Authorization: Bearer <access_token>" \
>   --header 'Content-Type: application/json' \
>   --data '{
>     "metadata": {
>       "parentId": "<project_ID>",
>       "name": "my-chatbot"
>     },
>     "spec": {
>       "image": "vllm/vllm-openai:latest",
>       "containerCommand": "python3 -m vllm.entrypoints.openai.api_server",
>       "environmentVariables": [
>         {
>           "name": "MODEL",
>           "value": "llama-3-70b"
>         }
>       ],
>       "ports": [
>         {
>           "containerPort": 8000,
>           "protocol": "HTTP"
>         }
>       ],
>       "authToken": "df88e***",
>       "volumes": [
>         {
>           "source": "storagebucket-e***",
>           "containerPath": "/output",
>           "mode": "READ_WRITE"
>         }
>       ],
>       "injectedFiles": [
>         {
>           "containerPath": "/etc/app/config.yaml",
>           "content": "'"$(base64 < config.yaml | tr -d '\n')"'"
>         }
>       ],
>       "subnetId": "vpcsubnet-e***",
>       "platform": "gpu-h100-sxm",
>       "preset": "1gpu-16vcpu-200gb",
>       "disk": {
>         "type": "NETWORK_SSD",
>         "sizeBytes": "268435456000"
>       },
>       "shmSizeBytes": "134217728",
>       "sshAuthorizedKeys": [
>         "'"$(cat ~/.ssh/id_ed25519.pub)"'"
>       ],
>       "publicIp": true
>     }
>   }'
>
> ```

In the `Authorization` header, replace `<access_token>` with the access token that you got in the prerequisites.

The request includes the following parameters:

* **Endpoint characteristics:**

  * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).
  * `metadata.name`: Endpoint name.
  * `spec.image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  * `spec.registryCredentials` (optional): Credentials to authenticate if you pull an image from a private registry.

    * `spec.registryCredentials.username`: Username.
    * `spec.registryCredentials.password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  * `spec.containerCommand` (optional): Entrypoint command for the container.
  * `spec.args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  * `spec.environmentVariables` (optional): Environment variables for the container.
    * `spec.environmentVariables[].name`: Environment variable name.
    * `spec.environmentVariables[].value`: Environment variable value.
  * `spec.ports` (optional): Ports that the endpoint exposes.
    * `spec.ports[].containerPort`: Port on which the application listens in the container. Each HTTP port is available through the endpoint's managed HTTPS URL.
    * `spec.ports[].protocol`: Protocol used by the exposed port.
  * `spec.authToken` (optional): Token for authentication. To generate one manually, run `openssl rand -hex 32`. If omitted, authentication is disabled.
  * `spec.volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the endpoint container. You can use volumes to store model files and other endpoint artifacts.
    * `spec.volumes[].source`: Volume ID or name.
    * `spec.volumes[].containerPath`: Absolute path where the volume is mounted in the container.
    * `spec.volumes[].mode`: Mount mode: `READ_ONLY` or `READ_WRITE`.
  * `spec.injectedFiles` (optional): Files to mount into the endpoint container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
    * `spec.injectedFiles[].containerPath`: Absolute path where the file is mounted in the container.
    * `spec.injectedFiles[].content`: Base64-encoded file content.

* **Underlying VM characteristics:**

  * `spec.subnetId`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id). Required if the project has multiple subnets.
  * `spec.platform`: VM platform. See available platforms in [Types of virtual machines and GPUs in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/types.md).
  * `spec.preset`: Number of GPUs, vCPUs and RAM allocated to the container. The preset must match the selected platform. See available presets in [Presets for GPU platforms](https://docs.nebius.com/compute/virtual-machines/types.md#presets-for-gpu-platforms).
  * `spec.disk.type`: Disk type for the underlying VM.
  * `spec.disk.sizeBytes`: Disk size of the underlying VM in bytes. The default value is 250 GiB. See how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).
  * `spec.shmSizeBytes` (optional): Shared memory size of `/dev/shm` in bytes. The default value is 16 GiB.
  * `spec.sshAuthorizedKeys` (optional): SSH public keys to access the underlying VM by SSH. When you add an SSH key, a public dynamic IP address is assigned. Before you add the key, check the quota on the number of public IP addresses in the [web console](https://console.nebius.com/quota).
  * `spec.preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `false`, the container runs on a regular VM.
  * `spec.pricingModel` (optional): Pricing model for the VM. It must match `spec.preemptible`: use `onDemand` for a regular VM. For a preemptible VM, use `followsSpotPrice` or `spotPricingPolicy`. Specify one of:
    * `spec.pricingModel.onDemand`: Empty object `{}` for a regular, non-preemptible VM.
    * `spec.pricingModel.followsSpotPrice`: Empty object `{}` to accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price.
    * `spec.pricingModel.spotPricingPolicy.id`: ID of the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) that sets the maximum price for a preemptible VM.
  * `spec.publicIp` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM. A public IP address isn't required to reach the endpoint through its managed HTTPS URL.

The endpoint creation takes approximately five minutes.

## How to call an endpoint

For this operation, it's enough to be in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

You can call an endpoint when you want to interact with an AI model hosted in this endpoint; for example, when you want to chat with the model.

Each HTTP port is available through a managed `https://` URL. gRPC also uses the managed HTTPS URL. For TCP ports, use the managed `tls://<host>:443` URL with a TLS client.

Endpoints support managed public URLs, shown in **Public endpoints** as `https://...`. For some previously created endpoints, **Public endpoints** can show `IP:port` instead.

To call the endpoint:

1. Get the endpoint's managed HTTPS URL:

   **Web console**

   1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
   2. Open the page of the required endpoint.
   3. Wait until the endpoint is running. Then, in the **Network** section, copy the public endpoint from the **Public endpoints** field. Depending on how the endpoint is exposed, this field can show either a managed `https://...` URL or `IP:port`.

   **CLI**

   1. To get the endpoint ID, list all endpoints:
      ```bash theme={null}
      nebius ai endpoint list
      ```
      In the output, copy the ID of the required endpoint.
   2. Get the endpoint's managed HTTPS URL:

      ```bash theme={null}
      nebius ai endpoint get <endpoint_ID> --format json \
        | jq -r '.status.public_endpoints[] | select(startswith("https://"))' | head -1
      ```

   **Go SDK**

   1. List endpoints:

      ```go theme={null}
      listEndpointService := sdk.Services().Ai().V1().Endpoint()
      endpoints, err := listEndpointService.List(
          ctx,
          &ai.ListEndpointsRequest{
              ParentId: "<project_ID>",
          },
      )
      if err != nil {
          return fmt.Errorf("list endpoints: %w", err)
      }
      fmt.Println(endpoints)
      ```

      In `ai.ListEndpointsRequest`, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3). In the response, copy the `Metadata.Id` of the required endpoint.

   2. Get the endpoint's managed HTTPS URL:

      ```go theme={null}
      getEndpointService := sdk.Services().Ai().V1().Endpoint()
      endpoint, err := getEndpointService.Get(
          ctx,
          &ai.GetEndpointRequest{
              Id: "<endpoint_ID>",
          },
      )
      if err != nil {
          return fmt.Errorf("get endpoint: %w", err)
      }
      for _, address := range endpoint.GetStatus().GetPublicEndpoints() {
          if strings.HasPrefix(address, "https://") {
              fmt.Println(address)
              break
          }
      }
      ```

      In `ai.GetEndpointRequest`, set `Id` to the endpoint ID that you copied. The code prints the endpoint's managed HTTPS URL.

   **Python SDK**

   1. List endpoints:

      ```python theme={null}
      list_endpoint_service = EndpointServiceClient(sdk)
      endpoints = await list_endpoint_service.list(
          ListEndpointsRequest(parent_id="<project_ID>"),
      )
      print(endpoints)
      ```

      In `ListEndpointsRequest`, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3). In the response, copy the `metadata.id` of the required endpoint.

   2. Get the endpoint's managed HTTPS URL:

      ```python theme={null}
      get_endpoint_service = EndpointServiceClient(sdk)
      endpoint = await get_endpoint_service.get(
          GetEndpointRequest(id="<endpoint_ID>"),
      )
      public_endpoint = next(
          (
              address
              for address in endpoint.status.public_endpoints
              if address.startswith("https://")
          ),
          None,
      )
      if public_endpoint is not None:
          print(public_endpoint)
      ```

      In `GetEndpointRequest`, set `id` to the endpoint ID that you copied. The code prints the endpoint's managed HTTPS URL.

   **JavaScript SDK**

   1. List endpoints:

      ```ts theme={null}
      const listEndpointService = new EndpointService(sdk);
      const endpoints = await listEndpointService.list(
        ListEndpointsRequest.create({
          parentId: "<project_ID>",
        }),
      );
      console.log(endpoints);
      ```

      In `ListEndpointsRequest`, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3). In the response, copy the `metadata.id` of the required endpoint.

   2. Get the endpoint's managed HTTPS URL:

      ```ts theme={null}
      const getEndpointService = new EndpointService(sdk);
      const endpoint = await getEndpointService.get(
        GetEndpointRequest.create({
          id: "<endpoint_ID>",
        }),
      );
      const publicEndpoint = endpoint.status?.publicEndpoints.find(
        (address) => address.startsWith("https://"),
      );
      if (publicEndpoint !== undefined) {
        console.log(publicEndpoint);
      }
      ```

      In `GetEndpointRequest`, set `id` to the endpoint ID that you copied. The code prints the endpoint's managed HTTPS URL.

   **REST API**

   1. List endpoints:

      ```bash theme={null}
      curl --request GET \
        --url "https://api.nebius.cloud/ai/v1/endpoints?parentId=<project_ID>" \
        --header "Authorization: Bearer <access_token>"
      ```

      In the request, specify:

      * Your access token in the `Authorization` header.
      * The [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in the `parentId` query parameter.

      In the response, copy the `metadata.id` of the required endpoint.

   2. Get the endpoint's managed HTTPS URL:

      ```bash theme={null}
      curl --request GET \
        --url "https://api.nebius.cloud/ai/v1/endpoints/<endpoint_ID>" \
        --header "Authorization: Bearer <access_token>" \
        | jq -r '.status.publicEndpoints[] | select(startswith("https://"))' | head -1
      ```

      In the request, specify:

      * Your access token in the `Authorization` header.
      * The endpoint ID from `metadata.id`, in the request path.

2. Call the endpoint by using an HTTP client. For example, with `curl`:

   ```bash theme={null}
   curl "<endpoint_URL>/v1/chat/completions" \
      -H "Authorization: Bearer <token>" \
      -H "Content-Type: application/json" \
      -d '{
         "model": "llama-3-70b",
         "messages": [
            {"role": "user", "content": "Tell a joke about AI."}
         ]
      }'
   ```

   In the command, specify the following parameters:

   * `<endpoint_URL>`: Managed HTTPS URL that you copied earlier.
   * `<token>`: Authentication token that you specified when you created the endpoint. If you didn't specify any token, don't use the `Authorization` HTTP header.
   * `model`: AI model that is hosted in the endpoint and that you chat with.
   * `content`: Message that you want to send to the model.

   The response looks like the following:

   ```json theme={null}
   {
     "choices": [
       {
         "message": {
           "role": "assistant",
           "content": "Why did the AI cross the road? Because it learned the optimal path after 10,000 epochs."
         }
       }
     ]
   }
   ```

### Traffic and connection limits

Managed public URLs of `https://` and `tls://` endpoints are served through [Nebius Tunnels](https://docs.nebius.com/tunnels/resources/quotas-limits.md), which means the limits for Tunnels apply to them. The limits for each endpoint are measured separately:

| Limit | Value per endpoint |
| - | - |
| Traffic, inbound and outbound combined | 120 Mbps |
| New client connections | 300 per second |

> [!WARNING]
>
> You cannot change the above limits from the web console.

All endpoints in a project share the [project limit](https://docs.nebius.com/tunnels/resources/quotas-limits.md), and all endpoints and tunnels in a region share the region limit. An endpoint never gets more than its own limit, but it can get less when its project or region is busy. When usage reaches a limit, responses may take longer until usage drops below the limit. Take these limits into account when you plan endpoints that serve high request volumes or large responses, such as audio, video or long streamed model outputs.

## How to change the endpoint container

After you create an endpoint, you can't change its settings, such as a container image, an entrypoint command, computing resources or environment variables. If you still need to change them, do one of the following:

* [Delete the endpoint](#how-to-delete-an-endpoint) and [create a new one](#how-to-create-an-endpoint) with the required settings. The new endpoint is provided with a **new HTTPS URL**.
* Update the image under the same image path and tag that the endpoint is already using. After that, [restart the endpoint](https://docs.nebius.com/serverless/maintenance/stop-start.md#how-to-stop-and-restart-an-endpoint). Serverless AI pulls the image again and runs a new version while the **same HTTPS URL and IP address** are preserved for the endpoint. This works only if the endpoint references a tag, not a fixed digest.

## How to delete an endpoint

When you delete an endpoint, Serverless AI automatically deletes its VM and container (boot) disk.

If you no longer need the endpoint, delete it:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Endpoints**.
2. Find the endpoint and then click  → **Delete**.
3. In the window that opens, confirm the deletion.

**CLI**

1. To get the endpoint ID, list all endpoints:
   ```bash theme={null}
   nebius ai endpoint list
   ```
   In the output, copy the ID of the required endpoint.
2. Delete the endpoint:

   ```bash theme={null}
   nebius ai endpoint delete --id <endpoint_ID>
   ```

   If a static IP address is assigned to the endpoint, the prompt asks to confirm the address release. Enter `y` to confirm or `n` to keep the address allocated in a pool.

**Go SDK**

1. List endpoints:

   ```go theme={null}
   listEndpointService := sdk.Services().Ai().V1().Endpoint()
   endpoints, err := listEndpointService.List(
       ctx,
       &ai.ListEndpointsRequest{
           ParentId: "<project_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("list endpoints: %w", err)
   }
   fmt.Println(endpoints)
   ```

   In `ai.ListEndpointsRequest`, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3). In the response, copy the `Metadata.Id` of the required endpoint.

2. Delete the endpoint:

   ```go theme={null}
   deleteEndpointService := sdk.Services().Ai().V1().Endpoint()
   deleteEndpointOperation, err := deleteEndpointService.Delete(
       ctx,
       &ai.DeleteEndpointRequest{
           Id: "<endpoint_ID>",
       },
   )
   if err != nil {
       return fmt.Errorf("delete endpoint: %w", err)
   }
   if _, err = deleteEndpointOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for endpoint deletion: %w", err)
   }
   ```

   In `ai.DeleteEndpointRequest`, set `Id` to the endpoint ID that you copied.

**Python SDK**

1. List endpoints:

   ```python theme={null}
   list_endpoint_service = EndpointServiceClient(sdk)
   endpoints = await list_endpoint_service.list(
       ListEndpointsRequest(parent_id="<project_ID>"),
   )
   print(endpoints)
   ```

   In `ListEndpointsRequest`, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3). In the response, copy the `metadata.id` of the required endpoint.

2. Delete the endpoint:

   ```python theme={null}
   delete_endpoint_service = EndpointServiceClient(sdk)
   delete_endpoint_operation = await delete_endpoint_service.delete(
       DeleteEndpointRequest(id="<endpoint_ID>"),
   )
   await delete_endpoint_operation.wait()
   ```

   In `DeleteEndpointRequest`, set `id` to the endpoint ID that you copied.

**JavaScript SDK**

1. List endpoints:

   ```ts theme={null}
   const listEndpointService = new EndpointService(sdk);
   const endpoints = await listEndpointService.list(
     ListEndpointsRequest.create({
       parentId: "<project_ID>",
     }),
   );
   console.log(endpoints);
   ```

   In `ListEndpointsRequest`, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3). In the response, copy the `metadata.id` of the required endpoint.

2. Delete the endpoint:

   ```ts theme={null}
   const deleteEndpointService = new EndpointService(sdk);
   const deleteEndpointOperation = await deleteEndpointService.delete(
     DeleteEndpointRequest.create({
       id: "<endpoint_ID>",
     }),
   ).result;
   await deleteEndpointOperation.wait();
   ```

   In `DeleteEndpointRequest`, set `id` to the endpoint ID that you copied.

**REST API**

1. List endpoints:

   ```bash theme={null}
   curl --request GET \
     --url "https://api.nebius.cloud/ai/v1/endpoints?parentId=<project_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * The [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in the `parentId` query parameter.

   In the response, copy the `metadata.id` of the required endpoint.

2. Delete the endpoint:

   ```bash theme={null}
   curl --request DELETE \
     --url "https://api.nebius.cloud/ai/v1/endpoints/<endpoint_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * The endpoint ID that you copied in the request path.

## See also

* [How to stop and restart an endpoint](https://docs.nebius.com/serverless/maintenance/stop-start.md#endpoints)
