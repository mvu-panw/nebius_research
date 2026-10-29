# Managing jobs in Serverless AI

Source: https://docs.nebius.com/serverless/jobs/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing jobs in Serverless AI

*Serverless AI jobs* run container images as one-off or scheduled batch workloads. They are suitable for training, fine-tuning and data processing where you want to use computing resources only to perform a task and stop when the task is done. Each job runs on a Compute virtual machine (VM) managed by Serverless AI and billed only while the job is running.

## Prerequisites

**Web console**

Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

* [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

  Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:

  ```bash theme={null}
  cat ~/.nebius/config.yaml
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

* Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## How to create a job

To run a container image as a batch workload for training, fine-tuning or data processing, create a job:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.

2. Click  **Create job**.

3. In **Configuration**, select **Custom**.

4. Configure **Job settings**:

   1. In **Image path**, set the path to the container image.

   2. If you use a private registry, in **Private registry**, select an existing registry or click  **Add**, and provide the details for your registry.

   3. (Optional) In **Entrypoint command**, specify the entrypoint command for the container.

      If you need to pass container arguments, specify them in this field as well.

   4. (Optional) In **Environment variables**, specify environment variables in key-value pairs.

   5. (Optional) In **Secret environment variables**, click  **Create secret** to store a sensitive value in [SecretStash](https://docs.nebius.com/mysterybox/overview.md) and inject it as an environment variable. In the window that opens, specify the **Key** (environment variable name) and **Value** (secret data), then click **Create**.

   6. (Optional) In **Job timeout in hours**, specify the number of hours after which the job will be canceled if not completed.

5. (Optional) Configure the **Computing resources** section:

   1. Select whether the underlying VM should have GPUs.

   2. Specify the VM type: regular or [preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md).

      VMs without GPUs only support the regular type.

   3. Select the [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

   4. If you selected the preemptible VM type, in **Max price**, select or create a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md), or choose **Follow spot price**.

6. (Optional) Configure **Storage** settings:

   * Under **Container disk size**, specify at least 50 GiB for GPU workloads or 20 GiB for CPU-only workloads. If the container image requires a bigger disk size, set at least the minimum required value for the image. Otherwise, the workloads won't be able to launch.

     For more information, see how [disk performance depends on disk size](https://docs.nebius.com/compute/storage/types.md#disk-performance).

   * Under **Mounted volumes**, click **Attach volume** to attach a bucket or a filesystem. You can create a bucket or filesystem, or use an existing one. To create a new bucket, see [Bucket parameters](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters). To create a new filesystem, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

7. (Optional) In the **Files** section, add one or more small configuration files to inject into the container at launch:
   * Select **Upload files** to upload files from your machine, or **Create text files** to enter the file content and click **Create file**.
   * In **Mount path**, specify the absolute path to the file in the container, for example, `/mnt/files/config.yaml`.
     Injected files are read-only and limited to 64 KiB each.

8. (Optional) In the **Access** section, configure **User name and SSH key** to [connect to the running workload for debugging](https://docs.nebius.com/serverless/jobs/failure.md#connect-to-the-container-by-using-ssh).

   You can create new credentials or select existing ones. If you decide to use an existing credential, make sure that the SSH key is stored for the **nebius** username.

9. Configure the **Network** section:
   * Select a subnet or create a new one.
   * Select the IP address type: **Public static IP** or **Private IP**. If you want to connect to the resource from the internet, select **Public static IP**.

10. Click **Create job**.

**CLI**

> [!TIP]
>
> With the command below, you specify all values directly in the command. This is useful for scripts, configuration-driven workflows, continuous integration (CI) and agents. Alternatively, you can run `nebius ai create` to use the interactive flow where the CLI prompts you for parameter values step by step.

Run the following command:

```bash theme={null}
nebius ai job create \
  --name <job_name> \
  --image <image_path> \
  --registry-username <username> \
  --registry-password <password> \
  --container-command "<command>" \
  --args "<arguments>" \
  --env <key=value> \
  --env-secret <key=secret_selector> \
  --working-dir <absolute_path> \
  --timeout <duration> \
  --platform <platform_ID> \
  --preset <preset> \
  --disk-size <size> \
  --volume <source:container_path[:mode]|s3://bucket:/container_path[:mode[:profile]]> \
  --inject-file "<local_path>:<absolute_container_path>" \
  --subnet-id <subnet_ID> \
  --shm-size <size> \
  --ssh-key <SSH_public_key> \
  --preemptible \
  --follows-spot-price
```

> **Job creation example**
>
> ```bash theme={null}
> nebius ai job create \
>   --name training-job \
>   --image nvidia/cuda:13.1.1-runtime-ubuntu24.04 \
>   --container-command bash \
>   --args "-c nvidia-smi" \
>   --platform gpu-l40s-a \
>   --preset 1gpu-8vcpu-32gb \
>   --timeout 1h \
>   --inject-file "config.yaml:/workspace/config.yaml" \
>   --subnet-id vpcsubnet-e***
> ```

In the command, specify the following parameters:

* **Job settings:**

  * `--name`: Job name.

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

  * `--working-dir` (optional): Working directory (absolute path).
  * `--timeout` (optional): Job timeout (for example, `2h30m10s`, `24h`). Minimum: `1h`, maximum: `168h`. Default: `24h`.
  * `--restart-policy` (optional): Whether to automatically restart the job when its container exits with an error (`--restart-policy on-failure`) or to only run it once and never restart it (`--restart-policy never`). For more details, see [Automatic job restarts](https://docs.nebius.com/serverless/jobs/auto-restarts.md).
  * `--inject-file` (optional): Mount a local file into the job container at launch. Use the format `<local_path>:<absolute_container_path>`. To inject multiple files, repeat the parameter. The mounted file is read-only and limited to 64 KiB.
  * `--volume` (optional): [Bucket](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the job container and to store the job results and checkpoints. Volumes persist if the job is recreated after a [maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md).

    Specify the value in either format:

    * `source:container_path[:mode]` for mounting Nebius shared filesystems and existing bucket or volume resources by ID or name.
    * `s3://bucket:/container_path[:mode[:profile]]` for mounting an Object Storage bucket with AWS profile credentials or S3 credentials stored in SecretStash. The `profile` is the AWS credentials profile to use. If you manage your credentials with [SecretStash](https://docs.nebius.com/mysterybox/overview.md), use `profile@<secret_selector>`, where `<secret_selector>` is a secret name, secret ID, version ID or a combined secret/version selector such as `mbsec-e00***@mbsecver-e00***`

    The supported modes are `ro`, read only, and `rw`, read-write (default). Repeat for multiple volumes. For example:

    ```bash theme={null}
    --volume 'computefilesystem-e***:/input:ro' \
    --volume 'storagebucket-e***:/output:rw' \
    --volume 's3://training-results:/output:rw:default'
    ```

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

For the full list of parameters, see the [nebius ai job create](https://docs.nebius.com/cli/reference/ai/job/create.md) CLI reference.

**Go SDK**

Run the following code:

```go theme={null}
jobFileContent, err := os.ReadFile("<local_path>")
if err != nil {
    return fmt.Errorf("read injected file: %w", err)
}
jobSpotPricing := &ai.PricingModelSpec{
    Model: &ai.PricingModelSpec_FollowsSpotPrice{
        FollowsSpotPrice: &ai.FollowsSpotPriceSpec{},
    },
}
createJobService := sdk.Services().Ai().V1().Job()
createJobOperation, err := createJobService.Create(
    ctx,
    &ai.CreateJobRequest{
        Metadata: &common.ResourceMetadata{
            ParentId: "<project_ID>",
            Name:     "<job_name>",
        },
        Spec: &ai.JobSpec{
            Image:            "<image_path>",
            RegistryCredentials: &ai.JobSpec_RegistryCredentials{
                Username: "<username>",
                Password: "<password>",
            },
            ContainerCommand: "<command>",
            Args:             "<arguments>",
            EnvironmentVariables: []*ai.JobSpec_EnvironmentVariable{
                {
                    Name:  "<environment_variable_name>",
                    Value: "<environment_variable_value>",
                },
                {
                    Name: "<secret_environment_variable_name>",
                    MysteryboxSecret: &ai.JobSpec_MysteryBoxSecretRef{
                        SecretId:  "<secret_ID>",
                        VersionId: "<version_ID>",
                    },
                },
            },
            WorkingDir: "<absolute_path>",
            Timeout:          durationpb.New(time.Hour),
            Platform:         "<platform_ID>",
            Preset:           "<preset>",
            Disk: &ai.JobSpec_DiskSpec{
                Type:      compute.DiskSpec_NETWORK_SSD,
                SizeBytes: <disk_size_in_bytes>,
            },
            Volumes: []*ai.JobSpec_VolumeMount{
                {
                    Source:        "<source>",
                    ContainerPath: "<absolute_container_path>",
                    Mode:          ai.JobSpec_VolumeMount_READ_WRITE,
                },
            },
            InjectedFiles: []*ai.JobSpec_FileInjection{
                {
                    ContainerPath: "<absolute_container_path>",
                    Content:       jobFileContent,
                },
            },
            SubnetId:         "<subnet_ID>",
            ShmSizeBytes: <shared_memory_size_in_bytes>,
            SshAuthorizedKeys: []string{"<SSH_public_key>"},
            PublicIp: true,
            Preemptible:      true,
            PricingModel:     jobSpotPricing,
        },
    },
)
if err != nil {
    return fmt.Errorf("create job: %w", err)
}
if _, err = createJobOperation.Wait(ctx); err != nil {
    return fmt.Errorf("wait for job creation: %w", err)
}
```

> **Job creation example**
>
> ```go theme={null}
> exampleJobFileContent, err := os.ReadFile("config.yaml")
> if err != nil {
>     return fmt.Errorf("read injected file: %w", err)
> }
> exampleJobService := sdk.Services().Ai().V1().Job()
> exampleJobOperation, err := exampleJobService.Create(
>     ctx,
>     &ai.CreateJobRequest{
>         Metadata: &common.ResourceMetadata{
>             Name:     "training-job",
>         },
>         Spec: &ai.JobSpec{
>             Image: "nvidia/cuda:13.1.1-runtime-ubuntu24.04",
>             ContainerCommand: "bash",
>             Args:         "-c nvidia-smi",
>             Platform:     "gpu-l40s-a",
>             Preset:       "1gpu-8vcpu-32gb",
>             Timeout:      durationpb.New(time.Hour),
>             ShmSizeBytes: 17179869184,
>             Disk: &ai.JobSpec_DiskSpec{
>                 Type:      compute.DiskSpec_NETWORK_SSD,
>                 SizeBytes: 268435456000,
>             },
>             InjectedFiles: []*ai.JobSpec_FileInjection{
>                 {
>                     ContainerPath: "/workspace/config.yaml",
>                     Content:       exampleJobFileContent,
>                 },
>             },
>             SubnetId:     "<subnet_ID>",
>         },
>     },
> )
> if err != nil {
>     return fmt.Errorf("create example job: %w", err)
> }
> if _, err = exampleJobOperation.Wait(ctx); err != nil {
>     return fmt.Errorf("wait for example job: %w", err)
> }
> ```

In the code, set the following parameters:

* **Job settings:**

  * `Metadata.ParentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).
  * `Metadata.Name`: Job name.
  * `Spec.Image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  * `Spec.RegistryCredentials` (optional): Credentials to authenticate if you pull an image from a private registry.

    * `Spec.RegistryCredentials.Username`: Username.
    * `Spec.RegistryCredentials.Password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  * `Spec.ContainerCommand` (optional): Entrypoint command for the container.
  * `Spec.Args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  * `Spec.EnvironmentVariables` (optional): Environment variables for the container.
    * `Spec.EnvironmentVariables[].Name`: Environment variable name.
    * `Spec.EnvironmentVariables[].Value`: Environment variable value.
    * `Spec.EnvironmentVariables[].MysteryboxSecret`: Secret to read the value from instead of `Value`. Set `SecretId` and `VersionId` to the ID and version ID of the secret.
  * `Spec.WorkingDir` (optional): Working directory (absolute path).
  * `Spec.Timeout` (optional): Job timeout as a protobuf duration, for example `durationpb.New(2 * time.Hour)`. Minimum: 1 hour, maximum: 168 hours. Default: 24 hours. The code sets a 1-hour timeout.
  * `Spec.RestartAttempts` (optional): Set to `-1` to automatically restart the job when its container exits with an error, or to `0` (default) to run it once. For more details, see [Automatic job restarts](https://docs.nebius.com/serverless/jobs/auto-restarts.md#go-sdk-2).
  * `Spec.Volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the job container and to store the job results and checkpoints. Volumes persist if the job is recreated after a [maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md).
    * `Spec.Volumes[].Source`: Volume ID or name.
    * `Spec.Volumes[].ContainerPath`: Absolute path where the volume is mounted in the container.
    * `Spec.Volumes[].Mode`: Mount mode: `ai.JobSpec_VolumeMount_READ_ONLY` or `ai.JobSpec_VolumeMount_READ_WRITE`.
  * `Spec.InjectedFiles` (optional): Files to mount into the job container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
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
  * `Spec.PublicIp` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM.
  * `Spec.Preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `false`, the container runs on a regular VM.
  * `Spec.PricingModel` (optional): Pricing model for the VM. It must match `Spec.Preemptible`: use `OnDemand` for a regular VM. For a preemptible VM, use `FollowsSpotPrice` or `SpotPricingPolicy`. Set `Spec.PricingModel.Model` to one of:
    * `&ai.PricingModelSpec_OnDemand{OnDemand: &ai.OnDemandSpec{}}`: Regular, non-preemptible VM.
    * `&ai.PricingModelSpec_FollowsSpotPrice{FollowsSpotPrice: &ai.FollowsSpotPriceSpec{}}`: Accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price. The code sets this model.
    * `&ai.PricingModelSpec_SpotPricingPolicy{SpotPricingPolicy: &ai.SpotPricingPolicySpec{Id: "<policy_ID>"}}`: Use the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) with the specified ID to set the maximum price for a preemptible VM.

**Python SDK**

Run the following code:

```python theme={null}
create_job_service = JobServiceClient(sdk)
create_job_operation = await create_job_service.create(
    CreateJobRequest(
        metadata=ResourceMetadata(
            parent_id="<project_ID>",
            name="<job_name>",
        ),
        spec=JobSpec(
            image="<image_path>",
            registry_credentials=JobSpec__RegistryCredentials(
                username="<username>",
                password="<password>",
            ),
            container_command="<command>",
            args="<arguments>",
            environment_variables=[
                JobSpec__EnvironmentVariable(
                    name="<environment_variable_name>",
                    value="<environment_variable_value>",
                ),
                JobSpec__EnvironmentVariable(
                    name="<secret_environment_variable_name>",
                    mysterybox_secret=JobSpec__MysteryBoxSecretRef(
                        secret_id="<secret_ID>",
                        version_id="<version_ID>",
                    ),
                ),
            ],
            working_dir="<absolute_path>",
            timeout=timedelta(hours=1),
            platform="<platform_ID>",
            preset="<preset>",
            disk=JobSpec__DiskSpec(
                type=DiskSpec__DiskType.NETWORK_SSD,
                size_bytes=<disk_size_in_bytes>,
            ),
            volumes=[
                JobSpec__VolumeMount(
                    source="<source>",
                    container_path="<absolute_container_path>",
                    mode=JobSpec__VolumeMount__Mode.READ_WRITE,
                ),
            ],
            injected_files=[
                JobSpec__FileInjection(
                    container_path="<absolute_container_path>",
                    content=Path("<local_path>").read_bytes(),
                ),
            ],
            subnet_id="<subnet_ID>",
            shm_size_bytes=<shared_memory_size_in_bytes>,
            ssh_authorized_keys=["<SSH_public_key>"],
            public_ip=True,
            preemptible=True,
            pricing_model=PricingModelSpec(
                follows_spot_price=FollowsSpotPriceSpec(),
            ),
        ),
    ),
)
await create_job_operation.wait()
```

> **Job creation example**
>
> ```python theme={null}
> example_job_service = JobServiceClient(sdk)
> example_job_operation = await example_job_service.create(
>     CreateJobRequest(
>         metadata=ResourceMetadata(
>             name="training-job",
>         ),
>         spec=JobSpec(
>             image=(
>                 "nvidia/cuda:13.1.1-runtime-ubuntu24.04"
>             ),
>             container_command="bash",
>             args="-c nvidia-smi",
>             platform="gpu-l40s-a",
>             preset="1gpu-8vcpu-32gb",
>             timeout=timedelta(hours=1),
>             shm_size_bytes=17179869184,
>             disk=JobSpec__DiskSpec(
>                 type=DiskSpec__DiskType.NETWORK_SSD,
>                 size_bytes=268435456000,
>             ),
>             injected_files=[
>                 JobSpec__FileInjection(
>                     container_path="/workspace/config.yaml",
>                     content=Path("config.yaml").read_bytes(),
>                 ),
>             ],
>             subnet_id="<subnet_ID>",
>         ),
>     ),
> )
> await example_job_operation.wait()
> ```

In the code, set the following parameters:

* **Job settings:**

  * `metadata.parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).
  * `metadata.name`: Job name.
  * `spec.image`: Container image reference in the `registry/path:tag` or `registry/path@digest` format. Use an image from a public registry or your authenticated private registry.
  * `spec.registry_credentials` (optional): Credentials to authenticate if you pull an image from a private registry.

    * `spec.registry_credentials.username`: Username.
    * `spec.registry_credentials.password`: Personal access token, password or an API key. Depends on where your registry is hosted. It can be Docker Hub, Microsoft Azure, GitHub, NVIDIA or a custom registry.

    If you pull an image from a public registry or from [Container Registry](https://docs.nebius.com/container-registry/index.md) in the same project, you don't need to specify credentials.
  * `spec.container_command` (optional): Entrypoint command for the container.
  * `spec.args` (optional): Arguments for `docker run` to pass to the entrypoint command.
  * `spec.environment_variables` (optional): Environment variables for the container.
    * `spec.environment_variables[].name`: Environment variable name.
    * `spec.environment_variables[].value`: Environment variable value.
    * `spec.environment_variables[].mysterybox_secret`: Secret to read the value from instead of `value`. Set `secret_id` and `version_id` to the ID and version ID of the secret.
  * `spec.working_dir` (optional): Working directory (absolute path).
  * `spec.timeout` (optional): Job timeout as a Python `timedelta`, for example `timedelta(hours=2)`. Minimum: 1 hour, maximum: 168 hours. Default: 24 hours. The code sets a 1-hour timeout.
  * `spec.restart_attempts` (optional): Set to `-1` to automatically restart the job when its container exits with an error, or to `0` (default) to run it once. For more details, see [Automatic job restarts](https://docs.nebius.com/serverless/jobs/auto-restarts.md#python-sdk-2).
  * `spec.volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the job container and to store the job results and checkpoints. Volumes persist if the job is recreated after a [maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md).
    * `spec.volumes[].source`: Volume ID or name.
    * `spec.volumes[].container_path`: Absolute path where the volume is mounted in the container.
    * `spec.volumes[].mode`: Mount mode: `JobSpec__VolumeMount__Mode.READ_ONLY` or `JobSpec__VolumeMount__Mode.READ_WRITE`.
  * `spec.injected_files` (optional): Files to mount into the job container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
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
  * `spec.public_ip` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM.
  * `spec.preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `False`, the container runs on a regular VM.
  * `spec.pricing_model` (optional): Pricing model for the VM. It must match `spec.preemptible`: use `on_demand` for a regular VM. For a preemptible VM, use `follows_spot_price` or `spot_pricing_policy`. Specify one of:
    * `spec.pricing_model.on_demand`: `OnDemandSpec()` for a regular, non-preemptible VM.
    * `spec.pricing_model.follows_spot_price`: `FollowsSpotPriceSpec()` to accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price. The code sets this model.
    * `spec.pricing_model.spot_pricing_policy`: `SpotPricingPolicySpec(id="<policy_ID>")` with the ID of the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) that sets the maximum price for a preemptible VM.

**JavaScript SDK**

Run the following code:

```ts theme={null}
dayjs.extend(duration);
const jobTimeout = dayjs.duration(1, "hour");
const createJobService = new JobService(sdk);
const createJobOperation = await createJobService.create(
  CreateJobRequest.create({
    metadata: {
      parentId: "<project_ID>",
      name: "<job_name>",
    },
    spec: {
      image: "<image_path>",
      registryCredentials: {
        username: "<username>",
        password: "<password>",
      },
      containerCommand: "<command>",
      args: "<arguments>",
      environmentVariables: [
        {
          name: "<environment_variable_name>",
          value: "<environment_variable_value>",
        },
        {
          name: "<secret_environment_variable_name>",
          mysteryboxSecret: {
            secretId: "<secret_ID>",
            versionId: "<version_ID>",
          },
        },
      ],
      workingDir: "<absolute_path>",
      timeout: jobTimeout,
      platform: "<platform_ID>",
      preset: "<preset>",
      disk: {
        type: DiskSpec_DiskType.NETWORK_SSD,
        sizeBytes: BigInt("<disk_size_in_bytes>"),
      },
      volumes: [
        {
          source: "<source>",
          containerPath: "<absolute_container_path>",
          mode: JobSpec_VolumeMount_Mode.READ_WRITE,
        },
      ],
      injectedFiles: [
        {
          containerPath: "<absolute_container_path>",
          content: await readFile("<local_path>"),
        },
      ],
      subnetId: "<subnet_ID>",
      shmSizeBytes: BigInt("<shared_memory_size_in_bytes>"),
      sshAuthorizedKeys: ["<SSH_public_key>"],
      publicIp: true,
      preemptible: true,
      pricingModel: {
        model: {
          $case: "followsSpotPrice",
          followsSpotPrice: {},
        },
      },
    },
  }),
).result;
await createJobOperation.wait();
```

> **Job creation example**
>
> ```ts theme={null}
> dayjs.extend(duration);
> const exampleJobTimeout = dayjs.duration(1, "hour");
> const exampleJobService = new JobService(sdk);
> const exampleJobOperation = await exampleJobService.create(
>   CreateJobRequest.create({
>     metadata: {
>       name: "training-job",
>     },
>     spec: {
>       image: "nvidia/cuda:13.1.1-runtime-ubuntu24.04",
>       containerCommand: "bash",
>       args: "-c nvidia-smi",
>       platform: "gpu-l40s-a",
>       preset: "1gpu-8vcpu-32gb",
>       timeout: exampleJobTimeout,
>       shmSizeBytes: 17179869184n,
>       disk: {
>         type: DiskSpec_DiskType.NETWORK_SSD,
>         sizeBytes: BigInt("268435456000"),
>       },
>       injectedFiles: [
>         {
>           containerPath: "/workspace/config.yaml",
>           content: await readFile("config.yaml"),
>         },
>       ],
>       subnetId: "<subnet_ID>",
>     },
>   }),
> ).result;
> await exampleJobOperation.wait();
> ```

In the code, set the following parameters:

* **Job settings:**

  * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).
  * `metadata.name`: Job name.
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
    * `spec.environmentVariables[].mysteryboxSecret`: Secret to read the value from instead of `value`. Set `secretId` and `versionId` to the ID and version ID of the secret.
  * `spec.workingDir` (optional): Working directory (absolute path).
  * `spec.timeout` (optional): Job timeout as a `dayjs.Duration`, for example `dayjs.duration(2, "hours")`. Minimum: 1 hour, maximum: 168 hours. Default: 24 hours. The code sets a 1-hour timeout.
  * `spec.restartAttempts` (optional): Set to `-1n` to automatically restart the job when its container exits with an error, or to `0` (default) to run it once. For more details, see [Automatic job restarts](https://docs.nebius.com/serverless/jobs/auto-restarts.md#javascript-sdk-2).
  * `spec.volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the job container and to store the job results and checkpoints. Volumes persist if the job is recreated after a [maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md).
    * `spec.volumes[].source`: Volume ID or name.
    * `spec.volumes[].containerPath`: Absolute path where the volume is mounted in the container.
    * `spec.volumes[].mode`: Mount mode: `JobSpec_VolumeMount_Mode.READ_ONLY` or `JobSpec_VolumeMount_Mode.READ_WRITE`.
  * `spec.injectedFiles` (optional): Files to mount into the job container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
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
  * `spec.publicIp` (optional): Whether to assign a [public IP address](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses) to the underlying VM.
  * `spec.preemptible` (optional): Whether to use a [preemptible VM](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Preemptible VMs can help reduce computing costs for workloads that tolerate interruptions, but they can be stopped by Compute at any time. Charges depend on the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md). Only GPU platforms offer preemptible VMs. If omitted or set to `false`, the container runs on a regular VM.
  * `spec.pricingModel` (optional): Pricing model for the VM. It must match `spec.preemptible`: use `onDemand` for a regular VM. For a preemptible VM, use `followsSpotPrice` or `spotPricingPolicy`. Set `spec.pricingModel.model` to one of:
    * `{ $case: "onDemand", onDemand: {} }`: Regular, non-preemptible VM.
    * `{ $case: "followsSpotPrice", followsSpotPrice: {} }`: Accept the current [spot price](https://docs.nebius.com/signup-billing/pricing-policy.md) for a preemptible VM, with no maximum price. The code sets this model.
    * `{ $case: "spotPricingPolicy", spotPricingPolicy: { id: "<policy_ID>" } }`: Use the [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) with the specified ID to set the maximum price for a preemptible VM.

**REST API**

Send the following request:

```bash theme={null}
curl --request POST \
  --url 'https://api.nebius.cloud/ai/v1/jobs' \
  --header "Authorization: Bearer <access_token>" \
  --header 'Content-Type: application/json' \
  --data '{
    "metadata": {
      "parentId": "<project_ID>",
      "name": "my-job-1"
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
      "workingDir": "<absolute_path>",
      "timeout": "<duration>",
      "platform": "<platform_ID>",
      "preset": "<preset>",
      "disk": {
        "type": "NETWORK_SSD",
        "sizeBytes": "<disk_size_in_bytes>"
      },
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
      "shmSizeBytes": "<shared_memory_size_in_bytes>",
      "sshAuthorizedKeys": [
        "<SSH_public_key>"
      ],
      "subnetId": "<subnet_ID>",
      "preemptible": true,
      "pricingModel": {"followsSpotPrice": {}}
    }
  }'

```

> **Job creation example**
>
> ```bash theme={null}
> curl --request POST \
>   --url 'https://api.nebius.cloud/ai/v1/jobs' \
>   --header "Authorization: Bearer <access_token>" \
>   --header 'Content-Type: application/json' \
>   --data '{
>     "metadata": {
>       "parentId": "<project_ID>",
>       "name": "training-job"
>     },
>     "spec": {
>       "image": "nvidia/cuda:13.1.1-runtime-ubuntu24.04",
>       "containerCommand": "bash",
>       "args": "-c nvidia-smi",
>       "platform": "gpu-l40s-a",
>       "preset": "1gpu-8vcpu-32gb",
>       "timeout": "3600s",
>       "subnetId": "vpcsubnet-e***",
>       "shmSizeBytes": "17179869184",
>       "disk": {
>         "type": "NETWORK_SSD",
>         "sizeBytes": "268435456000"
>       }
>     }
>   }'
>
> ```

In the `Authorization` header, replace `<access_token>` with the access token that you got in the prerequisites.

The request includes the following parameters:

* **Job settings:**

  * `metadata.parentId`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id).
  * `metadata.name`: Job name.
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
  * `spec.workingDir` (optional): Working directory (absolute path).
  * `spec.timeout` (optional): Job timeout in seconds with the `s` suffix (for example, `9000s`). Minimum: `3600s` (1 hour), maximum: `604800s` (168 hours). Default: `86400s` (24 hours).
  * `spec.restartAttempts` (optional): Set to `"-1"` to automatically restart the job when its container exits with an error, or to `"0"` (default) to run it once. For more details, see [Automatic job restarts](https://docs.nebius.com/serverless/jobs/auto-restarts.md).
  * `spec.volumes` (optional): [Buckets](https://docs.nebius.com/object-storage/overview.md#buckets) or [shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to mount to the job container and to store the job results and checkpoints. Volumes persist if the job is recreated after a [maintenance event](https://docs.nebius.com/compute/virtual-machines/maintenance.md).
    * `spec.volumes[].source`: Volume ID or name.
    * `spec.volumes[].containerPath`: Absolute path where the volume is mounted in the container.
    * `spec.volumes[].mode`: Mount mode: `READ_ONLY` or `READ_WRITE`.
  * `spec.injectedFiles` (optional): Files to mount into the job container at launch. To inject multiple files, add multiple items. Each mounted file is read-only and limited to 64 KiB.
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

The job creation usually takes a few minutes. Jobs run until the workload finishes.

When the job completes successfully or fails, the underlying VM is deleted automatically. If you mounted volumes, they will remain, and you should delete them manually.

## How to check job logs

For this operation, it's enough to be in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `viewer` role within your tenant; for example, the default `viewers` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

> [!NOTE]
>
> Checking job logs is available only in the web console and CLI.

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.
2. Next to the job, click **View logs**. Alternatively, select the job that you want to view the logs for and switch to the **Logs** tab.

You can use the period or log level filters to filter the logs. You can also use the [LogQL query language](https://docs.nebius.com/observability/logs/query-language.md).

**CLI**

Run the following command:

```bash theme={null}
nebius ai job logs <job_ID> --follow
```

You can add the following parameters to control the output:

* `--follow` or `-f`: Stream logs in real time.
* `--since <value>`: Show logs starting from the specified time. For example, `1h` (from 1 hour ago), `30m` (from 30 minutes ago) or `2024-01-01` (from that date).
* `--tail <value>`: Number of recent lines to show in the output.
* `--timestamps`: Include timestamps in the output.
* `--until <value>`: Show logs up to the specified time. For example, `1h` (up to 1 hour ago), `30m` (up to 30 minutes ago) or `2024-01-01` (up to that date).

## How to cancel a job

If you don't need a job to continue running, you can cancel it. The jobs that finish with `COMPLETED` status are canceled automatically.

To cancel a job:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.
2. Find the job and then click  → **Cancel**.
3. In the window that opens, confirm canceling the job.

**CLI**

1. List jobs:

   ```bash theme={null}
   nebius ai job list
   ```

   In the output, copy the ID of the required job.

2. To cancel a job, run:

   ```bash theme={null}
   nebius ai job cancel <job_ID>
   ```

**Go SDK**

1. List jobs:

   ```go theme={null}
   listJobService := sdk.Services().Ai().V1().Job()
   jobs, err := listJobService.List(
       ctx,
       &ai.ListJobsRequest{ParentId: "<project_ID>"},
   )
   if err != nil {
       return fmt.Errorf("list jobs: %w", err)
   }
   fmt.Println(jobs)
   ```

   In `ai.ListJobsRequest`, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3). In the response, copy the `Metadata.Id` of the required job.

2. To cancel a job, run:

   ```go theme={null}
   cancelJobService := sdk.Services().Ai().V1().Job()
   cancelJobOperation, err := cancelJobService.Cancel(
       ctx,
       &ai.CancelJobRequest{Id: "<job_ID>"},
   )
   if err != nil {
       return fmt.Errorf("cancel job: %w", err)
   }
   if _, err = cancelJobOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for job cancellation: %w", err)
   }
   ```

   In `ai.CancelJobRequest`, set `Id` to the job ID that you copied.

**Python SDK**

1. List jobs:

   ```python theme={null}
   list_job_service = JobServiceClient(sdk)
   jobs = await list_job_service.list(
       ListJobsRequest(parent_id="<project_ID>"),
   )
   print(jobs)
   ```

   In `ListJobsRequest`, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3). In the response, copy the `metadata.id` of the required job.

2. To cancel a job, run:

   ```python theme={null}
   cancel_job_service = JobServiceClient(sdk)
   cancel_job_operation = await cancel_job_service.cancel(
       CancelJobRequest(id="<job_ID>"),
   )
   await cancel_job_operation.wait()
   ```

   In `CancelJobRequest`, set `id` to the job ID that you copied.

**JavaScript SDK**

1. List jobs:

   ```ts theme={null}
   const listJobService = new JobService(sdk);
   const jobs = await listJobService.list(
     ListJobsRequest.create({
       parentId: "<project_ID>",
     }),
   );
   console.log(jobs);
   ```

   In `ListJobsRequest`, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3). In the response, copy the `metadata.id` of the required job.

2. To cancel a job, run:

   ```ts theme={null}
   const cancelJobService = new JobService(sdk);
   const cancelJobOperation = await cancelJobService.cancel(
     CancelJobRequest.create({ id: "<job_ID>" }),
   ).result;
   await cancelJobOperation.wait();
   ```

   In `CancelJobRequest`, set `id` to the job ID that you copied.

**REST API**

1. List jobs:

   ```bash theme={null}
   curl --request GET \
     --url "https://api.nebius.cloud/ai/v1/jobs?parentId=<project_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * The [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in the `parentId` query parameter.

   In the response, copy the `metadata.id` of the required job.

2. Cancel the job:

   ```bash theme={null}
   curl --request POST \
     --url 'https://api.nebius.cloud/ai/v1/jobs/cancel' \
     --header "Authorization: Bearer <access_token>" \
     --header 'Content-Type: application/json' \
     --data '{
       "id": "<job_ID>"
     }'
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * `<job_ID>`: Job ID that you copied.

Canceling a job immediately stops the underlying VM and deletes the container disk. The job remains in the list of jobs. Mounted volumes are retained. You can remove the mounted volumes manually. See the guides on [deleting a filesystem](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md#how-to-delete-the-created-resources) and [deleting a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets).

If you need to remove any record about the job from the job list, delete the job instead of canceling it.

## How to delete a job

To delete a job:

**Web console**

1. In the sidebar, go to  **Serverless AI** → **Jobs**.
2. Find the job and then click  → **Delete**.
3. In the window that opens, confirm deleting the job.

**CLI**

1. List jobs:

   ```bash theme={null}
   nebius ai job list
   ```

   In the output, copy the ID of the required job.

2. Delete the job:

   ```bash theme={null}
   nebius ai job delete <job_ID>
   ```

**Go SDK**

1. List jobs:

   ```go theme={null}
   listJobService := sdk.Services().Ai().V1().Job()
   jobs, err := listJobService.List(
       ctx,
       &ai.ListJobsRequest{ParentId: "<project_ID>"},
   )
   if err != nil {
       return fmt.Errorf("list jobs: %w", err)
   }
   fmt.Println(jobs)
   ```

   In `ai.ListJobsRequest`, set `ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3). In the response, copy the `Metadata.Id` of the required job.

2. Delete the job:

   ```go theme={null}
   deleteJobService := sdk.Services().Ai().V1().Job()
   deleteJobOperation, err := deleteJobService.Delete(
       ctx,
       &ai.DeleteJobRequest{Id: "<job_ID>"},
   )
   if err != nil {
       return fmt.Errorf("delete job: %w", err)
   }
   if _, err = deleteJobOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for job deletion: %w", err)
   }
   ```

   In `ai.DeleteJobRequest`, set `Id` to the job ID that you copied.

**Python SDK**

1. List jobs:

   ```python theme={null}
   list_job_service = JobServiceClient(sdk)
   jobs = await list_job_service.list(
       ListJobsRequest(parent_id="<project_ID>"),
   )
   print(jobs)
   ```

   In `ListJobsRequest`, set `parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3). In the response, copy the `metadata.id` of the required job.

2. Delete the job:

   ```python theme={null}
   delete_job_service = JobServiceClient(sdk)
   delete_job_operation = await delete_job_service.delete(
       DeleteJobRequest(id="<job_ID>"),
   )
   await delete_job_operation.wait()
   ```

   In `DeleteJobRequest`, set `id` to the job ID that you copied.

**JavaScript SDK**

1. List jobs:

   ```ts theme={null}
   const listJobService = new JobService(sdk);
   const jobs = await listJobService.list(
     ListJobsRequest.create({
       parentId: "<project_ID>",
     }),
   );
   console.log(jobs);
   ```

   In `ListJobsRequest`, set `parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3). In the response, copy the `metadata.id` of the required job.

2. Delete the job:

   ```ts theme={null}
   const deleteJobService = new JobService(sdk);
   const deleteJobOperation = await deleteJobService.delete(
     DeleteJobRequest.create({ id: "<job_ID>" }),
   ).result;
   await deleteJobOperation.wait();
   ```

   In `DeleteJobRequest`, set `id` to the job ID that you copied.

**REST API**

1. List jobs:

   ```bash theme={null}
   curl --request GET \
     --url "https://api.nebius.cloud/ai/v1/jobs?parentId=<project_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * The [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) in the `parentId` query parameter.

   In the response, copy the `metadata.id` of the required job.

2. Delete the job:

   ```bash theme={null}
   curl --request DELETE \
     --url "https://api.nebius.cloud/ai/v1/jobs/<job_ID>" \
     --header "Authorization: Bearer <access_token>"
   ```

   In the request, specify:

   * Your access token in the `Authorization` header.
   * The job ID that you copied in the request path.

When the job is deleted, it disappears from the list of jobs. If a job is running, deleting cancels the job first.

If the job uses additional volumes, they are not deleted with it. You can remove the mounted volumes manually. See the guides on [deleting a filesystem](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md#how-to-delete-the-created-resources) and [deleting a bucket](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets).
