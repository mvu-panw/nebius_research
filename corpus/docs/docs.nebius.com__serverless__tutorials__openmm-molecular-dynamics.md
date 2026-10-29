# Molecular dynamics simulations with OpenMM in Serverless AI

Source: https://docs.nebius.com/serverless/tutorials/openmm-molecular-dynamics

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Molecular dynamics simulations with OpenMM in Serverless AI

[Molecular dynamics](https://en.wikipedia.org/wiki/Molecular_dynamics) simulations help you study how atoms and molecules move over time. They are commonly used to explore protein stability, conformational changes and ligand binding. You can run these simulations on Nebius AI Cloud using [OpenMM](https://openmm.org), a Python-based simulation engine with GPU acceleration. By packaging OpenMM in a Docker image and running it as a Serverless AI job, you only pay for the seconds the GPU is in use and avoid keeping infrastructure running between simulations.

In this tutorial, you will run a protein simulation and inspect its results. The tutorial walks you through the following steps:

1. Build the simulation image locally with Docker and push it to [Container Registry](https://docs.nebius.com/container-registry/index.md).
2. Configure an [Object Storage](https://docs.nebius.com/object-storage/overview.md) bucket for storing simulation results.
3. Run a CUDA®-accelerated protein simulation as a Serverless AI job that reads a protein structure and writes the simulation results to the Object Storage bucket.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machines](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram) (VMs)
* [Boot disks](https://docs.nebius.com/compute/resources/pricing.md#disks) attached to the VMs
* Used space in Standard storage in an [Object Storage bucket](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data)

[Container Registry](https://docs.nebius.com/container-registry/resources/pricing.md) is provided free of charge.

## Prerequisites

**Web console**

1. Install Docker on your local machine. You can install [Docker Desktop](https://docs.docker.com/get-started/get-docker/).

   If your local machine uses a different CPU architecture than AMD64 — for example, an Apple Silicon Mac or a Windows-on-ARM device — Docker Desktop builds the AMD64 image under emulation.

2. [Install the Nebius AI Cloud CLI](https://docs.nebius.com/cli/install.md). It is required to authenticate against Container Registry and to push the Docker image to it.

3. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. Install and configure the Nebius AI Cloud CLI and the AWS CLI. Here are the instructions, depending on what tools you have already installed:

   * [How to install both CLIs](https://docs.nebius.com/object-storage/quickstart.md#prepare-your-environment)
   * [How to install the Nebius AI Cloud CLI only](https://docs.nebius.com/cli/install.md)
   * How to [install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI only

   When configuring the AWS CLI, make sure to [create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#cli-2) and [its access key](https://docs.nebius.com/iam/service-accounts/access-keys.md#cli-2). The Serverless AI job uses these credentials to write results to Object Storage.

2. Install Docker on your local machine. You can install [Docker Desktop](https://docs.docker.com/get-started/get-docker/).

   If your local machine uses a different CPU architecture than AMD64 — for example, an Apple Silicon Mac or a Windows-on-ARM device — Docker Desktop builds the AMD64 image under emulation.

3. Install [jq](https://jqlang.org/) to parse JSON outputs in this tutorial:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI. It is required to authenticate against Container Registry, to push the Docker image to it and to follow the job logs.

3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI.

   When configuring the AWS CLI, make sure to [create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#go-sdk-2) and [its access key](https://docs.nebius.com/iam/service-accounts/access-keys.md#go-sdk-2). The Serverless AI job uses these credentials to write results to Object Storage.

4. Install Docker on your local machine. You can install [Docker Desktop](https://docs.docker.com/get-started/get-docker/).

   If your local machine uses a different CPU architecture than AMD64 — for example, an Apple Silicon Mac or a Windows-on-ARM device — Docker Desktop builds the AMD64 image under emulation.

5. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI. It is required to authenticate against Container Registry, to push the Docker image to it and to follow the job logs.

3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI.

   When configuring the AWS CLI, make sure to [create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#python-sdk-2) and [its access key](https://docs.nebius.com/iam/service-accounts/access-keys.md#python-sdk-2). The Serverless AI job uses these credentials to write results to Object Storage.

4. Install Docker on your local machine. You can install [Docker Desktop](https://docs.docker.com/get-started/get-docker/).

   If your local machine uses a different CPU architecture than AMD64 — for example, an Apple Silicon Mac or a Windows-on-ARM device — Docker Desktop builds the AMD64 image under emulation.

5. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI. It is required to authenticate against Container Registry, to push the Docker image to it and to follow the job logs.

3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions) and [configure](https://docs.nebius.com/object-storage/interfaces/aws-cli.md#configuring-aws-cli) the AWS CLI.

   When configuring the AWS CLI, make sure to [create a service account](https://docs.nebius.com/iam/service-accounts/manage.md#javascript-sdk-2) and [its access key](https://docs.nebius.com/iam/service-accounts/access-keys.md#javascript-sdk-2). The Serverless AI job uses these credentials to write results to Object Storage.

4. Install Docker on your local machine. You can install [Docker Desktop](https://docs.docker.com/get-started/get-docker/).

   If your local machine uses a different CPU architecture than AMD64 — for example, an Apple Silicon Mac or a Windows-on-ARM device — Docker Desktop builds the AMD64 image under emulation.

5. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Steps

### Prepare infrastructure

> [!NOTE]
>
> Create all resources in the same project.

1. Create an Object Storage bucket to store simulation results.

   Serverless AI deletes the container disk after the job completes. The bucket preserves the simulation artifacts generated by the job: the processed structure, trajectory, logs, metadata and plots.

   **Web console**

   1. In the [web console](https://console.nebius.com), go to  **Storage** → **Object Storage**.
   2. Click  **Create bucket**.
   3. Specify the `openmm-simulation` name for the bucket.
   4. In the **Bucket size** field, select **Unlimited**.
   5. Click **Create bucket**.

   **CLI**

   ```bash theme={null}
   nebius storage bucket create --name openmm-simulation
   ```

   **Go SDK**

   ```go theme={null}
   bucketService := sdk.Services().Storage().V1().Bucket()
   bucketOperation, err := bucketService.Create(
       ctx,
       &storage.CreateBucketRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "openmm-simulation",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create bucket: %w", err)
   }
   if _, err = bucketOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for bucket creation: %w", err)
   }
   ```

   In the code, set `Metadata.ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).

   **Python SDK**

   ```python theme={null}
   bucket_service = BucketServiceClient(sdk)
   bucket_operation = await bucket_service.create(
       CreateBucketRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="openmm-simulation",
           ),
       ),
   )
   await bucket_operation.wait()
   ```

   In the code, set `metadata.parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).

   **JavaScript SDK**

   ```ts theme={null}
   const bucketService = new BucketService(sdk);
   const bucketOperation = await bucketService.create(
     CreateBucketRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "openmm-simulation",
       },
     }),
   ).result;
   await bucketOperation.wait();
   ```

   In the code, set `metadata.parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).

2. In Container Registry, create a registry to host the Docker image with OpenMM.

   Hosting the image in Container Registry keeps image pulls inside the same region as your Serverless AI job, which reduces the image pull latency and improves the job start time. Serverless AI doesn't bill for start time, so you can use Docker Hub or configure a private registry if the added pull latency doesn't matter for your workflow.

   **Web console**

   1. In the web console, go to  **Storage** → **Container Registry**.
   2. Click  **Create registry**.
   3. Specify the `openmm` name for the registry.
   4. Click **Create registry**.

   **CLI**

   Create the registry:

   ```bash theme={null}
   nebius registry create --name openmm
   ```

   **Go SDK**

   Create the registry:

   ```go theme={null}
   registryService := sdk.Services().Registry().V1().Registry()
   registryOperation, err := registryService.Create(
       ctx,
       &registry.CreateRegistryRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "openmm",
           },
           Spec: &registry.RegistrySpec{},
       },
   )
   if err != nil {
       return fmt.Errorf("create registry: %w", err)
   }
   if _, err = registryOperation.Wait(ctx); err != nil {
       return fmt.Errorf("wait for registry creation: %w", err)
   }
   ```

   In the code, set `Metadata.ParentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3).

   **Python SDK**

   Create the registry:

   ```python theme={null}
   registry_service = RegistryServiceClient(sdk)
   registry_operation = await registry_service.create(
       CreateRegistryRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="openmm",
           ),
           spec=RegistrySpec(),
       ),
   )
   await registry_operation.wait()
   ```

   In the code, set `metadata.parent_id` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3).

   **JavaScript SDK**

   Create the registry:

   ```ts theme={null}
   const registryService = new RegistryService(sdk);
   const registryOperation = await registryService.create(
     CreateRegistryRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "openmm",
       },
       spec: {},
     }),
   ).result;
   await registryOperation.wait();
   ```

   In the code, set `metadata.parentId` to the [project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3).

### Build and push the image

1. Configure the Docker credential helper for Container Registry so that `docker push` can authenticate through the Nebius AI Cloud CLI:

   ```bash theme={null}
   nebius registry configure-helper
   ```

2. Clone the [Serverless AI Cookbook](https://github.com/nebius/serverless-ai-cookbook) repository and switch to the `openmm-simulation` directory:

   ```bash theme={null}
   git clone https://github.com/nebius/serverless-ai-cookbook.git && \
   cd serverless-ai-cookbook/life-science/openmm-simulation
   ```

   The `sim/` folder contains Python code with the OpenMM simulation settings. This tutorial uses the code as-is and lets you adjust the target protein and the simulation step count when you create the Serverless AI job.

   > [!TIP]
   >
   > You can explore the code and change the simulation settings — for example, by editing the OpenMM classes in `sim/utils.py` and `sim/run.py`. For more details, see [OpenMM Python API](https://docs.openmm.org/latest/api-python/index.html).

3. Export the region and the registry path to environment variables. The Docker commands below use them in the image name:

   **CLI**

   ```bash theme={null}
   export NB_REGION_ID=<region_ID>
   export NB_REGISTRY_PATH=$(nebius registry list \
      --format json \
      | jq -r '.items[] | select(.metadata.name=="openmm") | .metadata.id' \
      | cut -d- -f2)
   ```

   Replace `<region_ID>` with the ID of the [region](https://docs.nebius.com/overview/regions.md) where you create the resources, for example, `eu-north1`.

   **Go SDK**

   1. Get the registry path:

      ```go theme={null}
      lookupRegistryService := sdk.Services().Registry().V1().
          Registry()
      registries, err := lookupRegistryService.List(
          ctx,
          &registry.ListRegistriesRequest{
              ParentId: "<project_ID>",
          },
      )
      if err != nil {
          return fmt.Errorf("list registries: %w", err)
      }
      for _, item := range registries.GetItems() {
          if item.GetMetadata().GetName() == "openmm" {
              registryID := item.GetMetadata().GetId()
              fmt.Println(strings.Split(registryID, "-")[1])
              break
          }
      }
      ```

      The code prints the registry path: the registry ID without the `registry-` prefix.

   2. Export the region ID and the printed registry path to environment variables:

      ```bash theme={null}
      export NB_REGION_ID=<region_ID>
      export NB_REGISTRY_PATH=<registry_path>
      ```

      Replace `<region_ID>` with the ID of the [region](https://docs.nebius.com/overview/regions.md) where you create the resources, for example, `eu-north1`.

   **Python SDK**

   1. Get the registry path:

      ```python theme={null}
      registry_service = RegistryServiceClient(sdk)
      registries = await registry_service.list(
          ListRegistriesRequest(parent_id="<project_ID>"),
      )
      registry_path = next(
          (
              item.metadata.id.split("-")[1]
              for item in registries.items
              if item.metadata.name == "openmm"
          ),
          None,
      )
      print(registry_path)
      ```

      The code prints the registry path: the registry ID without the `registry-` prefix.

   2. Export the region ID and the printed registry path to environment variables:

      ```bash theme={null}
      export NB_REGION_ID=<region_ID>
      export NB_REGISTRY_PATH=<registry_path>
      ```

      Replace `<region_ID>` with the ID of the [region](https://docs.nebius.com/overview/regions.md) where you create the resources, for example, `eu-north1`.

   **JavaScript SDK**

   1. Get the registry path:

      ```ts theme={null}
      const lookupRegistryService = new RegistryService(sdk);
      const registries = await lookupRegistryService.list(
        ListRegistriesRequest.create({
          parentId: "<project_ID>",
        }),
      );
      const registry = registries.items.find(
        (item) => item.metadata?.name === "openmm",
      );
      const registryPath = registry?.metadata?.id?.split("-")[1];
      console.log(registryPath ?? null);
      ```

      The code prints the registry path: the registry ID without the `registry-` prefix.

   2. Export the region ID and the printed registry path to environment variables:

      ```bash theme={null}
      export NB_REGION_ID=<region_ID>
      export NB_REGISTRY_PATH=<registry_path>
      ```

      Replace `<region_ID>` with the ID of the [region](https://docs.nebius.com/overview/regions.md) where you create the resources, for example, `eu-north1`.

4. Verify that Docker is available and the daemon is running:

   ```bash theme={null}
   docker version
   docker ps
   ```

   If `docker ps` returns a table of containers (can be empty), the daemon is running. If the daemon is not running, [launch it](https://docs.docker.com/engine/daemon/start/).

5. Build the image, targeting `linux/amd64`:

   ```bash theme={null}
   docker build --platform linux/amd64 \
     -t cr.$NB_REGION_ID.nebius.cloud/$NB_REGISTRY_PATH/openmm-serverless:v1 .
   ```

   > [!NOTE]
   >
   > Serverless AI runs Docker images on the `linux/amd64` architecture. Using the `--platform linux/amd64` parameter produces an AMD64 image regardless of the host architecture of your local machine. The resulting image runs natively in Serverless AI with no runtime penalty. For more information, see [Docker official documentation](https://docs.docker.com/build/building/multi-platform/) on multi-platform builds.

6. Push the image to the registry:

   ```bash theme={null}
   docker push cr.$NB_REGION_ID.nebius.cloud/$NB_REGISTRY_PATH/openmm-serverless:v1
   ```

### Run the simulation as a Serverless AI job

Create a CUDA-accelerated job that runs a short simulation on the `1UBQ` protein structure:

**Web console**

1. In the web console, go to  **Storage** → **Container Registry**, then open the `openmm` registry and the `openmm-serverless` image.

2. In the `v1` tag row, click  → **Deploy as job**. The **Create job** page opens with **Image path** already filled in.

3. Specify the remaining job parameters:

   * **Name**: `openmm-1ubq`.
   * **Entrypoint command**: `bash -c "python -m sim.run --protein-id 1UBQ --steps 1000 && cp -r /openmm/results/. /mnt/data/"`.
   * **Job timeout in hours**: `4`.
   * **Computing resources**: With GPU.
   * **Available platform**: NVIDIA® L40S Intel.
   * **Preset**: 1 GPU — 8 CPUs — 32 GiB RAM.
   * **Mounted volumes**: Click **Attach volume** and select the `openmm-simulation` bucket.
   * **Mount path**: `/mnt/data`.

   In the entrypoint command, `/openmm/results/` is the location of simulation results inside the Docker container. The command runs the simulation and copies the results to the mounted bucket at `/mnt/data`. You can adjust `--protein-id` and `--steps` to target a different protein or change the simulation length.

4. Click **Create job**.

5. Follow the job logs to watch the simulation progress:

   1. In the sidebar, go to  **Serverless AI** → **Jobs**.
   2. Next to the job, click **View logs**. Alternatively, select the job that you want to view the logs for and switch to the **Logs** tab.

**CLI**

1. Create the environment variables with your AWS CLI credentials, the Object Storage bucket settings and the ID of the subnet where the job runs. The Serverless AI job reads the AWS and S3 variables and uploads the results to the bucket through the AWS API:
   ```bash theme={null}
   export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
   export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
   export AWS_DEFAULT_REGION=$NB_REGION_ID
   export S3_ENDPOINT_URL=https://storage.${NB_REGION_ID}.nebius.cloud
   export S3_BUCKET=openmm-simulation
   export S3_PREFIX=openmm
   export NB_SUBNET_ID=<subnet_ID>
   ```
   For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

2. Create the job:

   ```bash theme={null}
   nebius ai job create \
     --name openmm-1ubq \
     --image cr.$NB_REGION_ID.nebius.cloud/$NB_REGISTRY_PATH/openmm-serverless:v1 \
     --platform gpu-l40s-a \
     --preset 1gpu-8vcpu-32gb \
     --timeout 4h \
     --args "--protein-id 1UBQ --steps 1000" \
     --env "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" \
     --env "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" \
     --env "AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION" \
     --env "S3_ENDPOINT_URL=$S3_ENDPOINT_URL" \
     --env "S3_BUCKET=$S3_BUCKET" \
     --env "S3_PREFIX=$S3_PREFIX" \
     --subnet-id $NB_SUBNET_ID
   ```

   You can reuse this command to start several simulation jobs in parallel: for each job, change the `--name` and `--args` values — for example, `--protein-id 2PTC --steps 2000`.

3. Follow the job logs to watch the simulation progress:

   ```bash theme={null}
   nebius ai job logs <job_ID> --follow
   ```

   To get the job ID, run `nebius ai job get-by-name --name openmm-1ubq`.

**Go SDK**

1. Create the environment variables with your AWS CLI credentials, the Object Storage bucket settings and the ID of the subnet where the job runs. The Serverless AI job reads the AWS and S3 variables and uploads the results to the bucket through the AWS API:
   ```bash theme={null}
   export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
   export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
   export AWS_DEFAULT_REGION=$NB_REGION_ID
   export S3_ENDPOINT_URL=https://storage.${NB_REGION_ID}.nebius.cloud
   export S3_BUCKET=openmm-simulation
   export S3_PREFIX=openmm
   export NB_SUBNET_ID=<subnet_ID>
   ```
   For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

2. Create the job:

   ```go theme={null}
   createJobSvc := sdk.Services().Ai().V1().Job()
   regionID := os.Getenv("NB_REGION_ID")
   registryPath := os.Getenv("NB_REGISTRY_PATH")
   subnetID := os.Getenv("NB_SUBNET_ID")
   if regionID == "" || registryPath == "" || subnetID == "" {
       return fmt.Errorf("NB_REGION_ID, NB_REGISTRY_PATH and " +
           "NB_SUBNET_ID must be set")
   }
   image := "cr." + regionID + ".nebius.cloud/" + registryPath +
       "/openmm-serverless:v1"
   s3EnvNames := []string{
       "AWS_ACCESS_KEY_ID",
       "AWS_SECRET_ACCESS_KEY",
       "AWS_DEFAULT_REGION",
       "S3_ENDPOINT_URL",
       "S3_BUCKET",
       "S3_PREFIX",
   }
   var jobEnv []*ai.JobSpec_EnvironmentVariable
   for _, name := range s3EnvNames {
       value, ok := os.LookupEnv(name)
       if !ok {
           return fmt.Errorf("%s is not set", name)
       }
       jobEnv = append(jobEnv, &ai.JobSpec_EnvironmentVariable{
           Name:  name,
           Value: value,
       })
   }
   createJobOp, err := createJobSvc.Create(
       ctx,
       &ai.CreateJobRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name:     "openmm-1ubq",
           },
           Spec: &ai.JobSpec{
               Image:                image,
               Args:                 "--protein-id 1UBQ --steps 1000",
               EnvironmentVariables: jobEnv,
               Platform:             "gpu-l40s-a",
               Preset:               "1gpu-8vcpu-32gb",
               Timeout:              durationpb.New(4 * time.Hour),
               // The CLI defaults to 16 GiB for GPU platforms.
               ShmSizeBytes: 17179869184,
               // The CLI defaults to 250 GiB.
               Disk: &ai.JobSpec_DiskSpec{
                   Type:      compute.DiskSpec_NETWORK_SSD,
                   SizeBytes: 268435456000,
               },
               SubnetId: subnetID,
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create job: %w", err)
   }
   if _, err = createJobOp.Wait(ctx); err != nil {
       return fmt.Errorf("wait for job creation: %w", err)
   }
   ```

   The code reads the exported variables, uses the region ID and the registry path to build the image name and passes the AWS and S3 settings to the job as environment variables.

   To start several simulation jobs in parallel, change `Metadata.Name` and `Spec.Args` for each job, for example, `--protein-id 2PTC --steps 2000`.

3. Follow the job logs to watch the simulation progress. The SDK doesn't stream job logs, so use the CLI:

   ```bash theme={null}
   nebius ai job logs <job_ID> --follow
   ```

   To get the job ID, run `nebius ai job get-by-name --name openmm-1ubq`.

**Python SDK**

1. Create the environment variables with your AWS CLI credentials, the Object Storage bucket settings and the ID of the subnet where the job runs. The Serverless AI job reads the AWS and S3 variables and uploads the results to the bucket through the AWS API:
   ```bash theme={null}
   export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
   export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
   export AWS_DEFAULT_REGION=$NB_REGION_ID
   export S3_ENDPOINT_URL=https://storage.${NB_REGION_ID}.nebius.cloud
   export S3_BUCKET=openmm-simulation
   export S3_PREFIX=openmm
   export NB_SUBNET_ID=<subnet_ID>
   ```
   For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

2. Create the job:

   ```python theme={null}
   create_job_service = JobServiceClient(sdk)
   region_id = os.environ["NB_REGION_ID"]
   registry_path = os.environ["NB_REGISTRY_PATH"]
   image = (
       f"cr.{region_id}.nebius.cloud/"
       f"{registry_path}/openmm-serverless:v1"
   )
   s3_env_names = [
       "AWS_ACCESS_KEY_ID",
       "AWS_SECRET_ACCESS_KEY",
       "AWS_DEFAULT_REGION",
       "S3_ENDPOINT_URL",
       "S3_BUCKET",
       "S3_PREFIX",
   ]
   job_env = [
       JobSpec__EnvironmentVariable(name=name, value=os.environ[name])
       for name in s3_env_names
   ]
   create_job_operation = await create_job_service.create(
       CreateJobRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="openmm-1ubq",
           ),
           spec=JobSpec(
               image=image,
               args="--protein-id 1UBQ --steps 1000",
               environment_variables=job_env,
               platform="gpu-l40s-a",
               preset="1gpu-8vcpu-32gb",
               timeout=timedelta(hours=4),
               # The CLI defaults to 16 GiB for GPU platforms.
               shm_size_bytes=17179869184,
               # The CLI defaults to 250 GiB.
               disk=JobSpec__DiskSpec(
                   type=DiskSpec__DiskType.NETWORK_SSD,
                   size_bytes=268435456000,
               ),
               subnet_id=os.environ["NB_SUBNET_ID"],
           ),
       ),
   )
   await create_job_operation.wait()
   ```

   The code reads the exported variables, uses the region ID and the registry path to build the image name and passes the AWS and S3 settings to the job as environment variables.

   To start several simulation jobs in parallel, change `metadata.name` and `spec.args` for each job, for example, `--protein-id 2PTC --steps 2000`.

3. Follow the job logs to watch the simulation progress. The SDK doesn't stream job logs, so use the CLI:

   ```bash theme={null}
   nebius ai job logs <job_ID> --follow
   ```

   To get the job ID, run `nebius ai job get-by-name --name openmm-1ubq`.

**JavaScript SDK**

1. Create the environment variables with your AWS CLI credentials, the Object Storage bucket settings and the ID of the subnet where the job runs. The Serverless AI job reads the AWS and S3 variables and uploads the results to the bucket through the AWS API:
   ```bash theme={null}
   export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
   export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
   export AWS_DEFAULT_REGION=$NB_REGION_ID
   export S3_ENDPOINT_URL=https://storage.${NB_REGION_ID}.nebius.cloud
   export S3_BUCKET=openmm-simulation
   export S3_PREFIX=openmm
   export NB_SUBNET_ID=<subnet_ID>
   ```
   For details about the subnet ID, see [How to get a subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

2. Create the job:

   ```ts theme={null}
   dayjs.extend(duration);
   const createJobService = new JobService(sdk);
   const regionId = process.env.NB_REGION_ID;
   const registryPath = process.env.NB_REGISTRY_PATH;
   const subnetId = process.env.NB_SUBNET_ID;
   if (!regionId || !registryPath || !subnetId) {
     throw new Error(
       "NB_REGION_ID, NB_REGISTRY_PATH and NB_SUBNET_ID must be set",
     );
   }
   const image = `cr.${regionId}.nebius.cloud/${registryPath}` +
     "/openmm-serverless:v1";
   const s3EnvNames = [
     "AWS_ACCESS_KEY_ID",
     "AWS_SECRET_ACCESS_KEY",
     "AWS_DEFAULT_REGION",
     "S3_ENDPOINT_URL",
     "S3_BUCKET",
     "S3_PREFIX",
   ];
   const jobEnv = s3EnvNames.map((name) => {
     const value = process.env[name];
     if (!value) {
       throw new Error(`${name} is not set`);
     }
     return { name, value };
   });
   const createJobOperation = await createJobService.create(
     CreateJobRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "openmm-1ubq",
       },
       spec: {
         image,
         args: "--protein-id 1UBQ --steps 1000",
         environmentVariables: jobEnv,
         platform: "gpu-l40s-a",
         preset: "1gpu-8vcpu-32gb",
         timeout: dayjs.duration(4, "hours"),
         // The CLI defaults to 16 GiB for GPU platforms.
         shmSizeBytes: 17179869184n,
         // The CLI defaults to 250 GiB.
         disk: {
           type: DiskSpec_DiskType.NETWORK_SSD,
           sizeBytes: 268435456000n,
         },
         subnetId,
       },
     }),
   ).result;
   await createJobOperation.wait();
   ```

   The code reads the exported variables, uses the region ID and the registry path to build the image name and passes the AWS and S3 settings to the job as environment variables.

   To start several simulation jobs in parallel, change `metadata.name` and `spec.args` for each job, for example, `--protein-id 2PTC --steps 2000`.

3. Follow the job logs to watch the simulation progress. The SDK doesn't stream job logs, so use the CLI:

   ```bash theme={null}
   nebius ai job logs <job_ID> --follow
   ```

   To get the job ID, run `nebius ai job get-by-name --name openmm-1ubq`.

A healthy CUDA-accelerated job prints the following line near the start of the logs:

```text theme={null}
Using OpenMM platform: CUDA
```

If the line shows `CPU` or `Reference` instead, the GPU runtime didn't initialize and the simulation will be far slower than expected.

### View results in the bucket

**Web console**

The job uploads the simulation results to the bucket in the folder named `<protein_id>_<timestamp>/` — for example, `1UBQ_20260512_192514/`.

To view results:

1. In the web console, go to  **Storage** → **Object Storage**.
2. Open the `openmm-simulation` bucket.
3. Open the output folder of the latest job.

**CLI**

The job uploads the simulation results to the bucket through the [AWS S3-compatible API](https://docs.nebius.com/object-storage/interfaces/s3-api-compatibility.md) at `s3://<bucket>/<prefix>/<protein_id>_<timestamp>/` — for example, `s3://openmm-simulation/openmm/1UBQ_20260512_192514/`.

To view results:

1. List the job outputs in the bucket:

   ```bash theme={null}
   aws s3 ls "s3://$S3_BUCKET/$S3_PREFIX/" \
     --endpoint-url "$S3_ENDPOINT_URL"
   ```

2. Download a specific job output locally:

   ```bash theme={null}
   aws s3 sync "s3://$S3_BUCKET/$S3_PREFIX/<output>/" "./results/<output>/" \
     --endpoint-url "$S3_ENDPOINT_URL"
   ```

A completed simulation contains the following artifacts:

* `<protein>_processed.pdb` — the processed input structure.
* `<protein>_trajectory.dcd` — the trajectory of the simulation.
* `<protein>_simulation.log` — the simulation log.
* `<protein>_metadata.txt` — the simulation metadata.
* `plots/` — visualizations generated from the trajectory.

To inspect the simulation locally, open the downloaded `<protein_id>_processed.pdb` and `<protein_id>_trajectory.dcd` files in a molecular visualization tool of your choice, for example, [PyMOL](https://www.pymol.org/).

![PyMOL rendering of the 1UBQ protein structure](https://mintcdn.com/nebius-ai-cloud/GJF9LhwGqChu49Y0/_assets/serverless/openmm-pymol-visualization.png?fit=max\&auto=format\&n=GJF9LhwGqChu49Y0\&q=85\&s=9e1e81809d1cd342de36cf617650145b)

Generated in PyMOL from `1UBQ_processed.pdb`

## How to delete the created resources

A Serverless AI job stops billing the moment it completes, but the bucket keeps accruing charges until you remove it. The container registry is free of charge; delete it if you no longer need the image. The service account and its access key live at the tenant level, don't accrue charges and can be reused for future workloads.

If you don't need the bucket, [delete it](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets), so Nebius AI Cloud doesn't charge for it.
