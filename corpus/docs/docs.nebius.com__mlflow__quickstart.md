# Getting started with Managed Service for MLflow: create your first cluster

Source: https://docs.nebius.com/mlflow/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Managed Service for MLflow: create your first cluster

MLflow helps to track and manage your machine learning experiments. With clusters for MLflow in Nebius AI Cloud, you can deploy MLflow in a cloud in just a couple of clicks and connect to it easily from machines that run your workloads.

This guide covers how to set up your environment to work with Managed Service for MLflow, create your first cluster, run a simple experiment and access its artifacts in Object Storage.

## Prerequisites

**Web console**

1. Install the **MLflow** Python package that provides an API to run and manage experiments in your code:

   ```bash theme={null}
   pip install mlflow
   ```

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. Install the following tools:

   * **MLflow**: Python package that provides an API to run and manage experiments in your code.
   * **Nebius AI Cloud CLI** ([How to install the CLI](https://docs.nebius.com/cli/install.md)): To manage all Nebius AI Cloud resources.

   Here are all the installation commands in a single copy-and-paste block:

   ```bash Ubuntu theme={null}
   pip install mlflow
   curl -sSL https://artifacts.nebius.cloud/cli/install.sh | bash
   nebius profile create
   ```

   ```bash macOS theme={null}
   pip install mlflow
   curl -sSL https://artifacts.nebius.cloud/cli/install.sh | bash
   nebius profile create
   ```

   The last command, `nebius profile create`, will guide you through several prompts. After you complete the prompts, your browser will open the Nebius AI Cloud web console sign-in screen. Sign in to the web console to complete the initialization. If you have access to multiple tenants, the CLI will prompt you to choose a tenant ID. After that, save your project ID in the CLI configuration.

   If the project ID hasn't been configured during the `nebius profile create` flow, [get the project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) and save it in the CLI configuration:

   ```bash theme={null}
   nebius config set parent-id <project_ID>
   ```

2. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. Install the **MLflow** Python package that provides an API to run and manage experiments in your code:

   ```bash theme={null}
   pip install mlflow
   ```

2. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

3. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. Install the **MLflow** Python package that provides an API to run and manage experiments in your code:

   ```bash theme={null}
   pip install mlflow
   ```

2. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

3. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. Install the **MLflow** Python package that provides an API to run and manage experiments in your code:

   ```bash theme={null}
   pip install mlflow
   ```

2. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

3. Make sure that you, or the service account that you use on your behalf, is in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Steps

### Create a cluster

**Web console**

1. In the sidebar, go to  **MLflow**.

2. Click **Create cluster**.

3. On the cluster creation page that opens, set the following parameters:

   * **Name**: Enter a name for your cluster.

   * **Service account**: Select the `mlflow-sa` service account. It was created for Managed MLflow by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud.

   * **Access**: Select the **Public and private** option.

     In this case, the cluster has both public and private tracking endpoints. You can access the public endpoint from the internet and the private endpoint from the network where the cluster is located (for example, via a virtual machine in this network).

   * **Cluster size**: Select **Medium**.

   * **Admin credentials**: Enter a username and a strong password.

4. Click **Create cluster**.

**CLI**

1. Create a password for administrator access to the cluster and save it to an environment variable:

   ```bash theme={null}
   export PASSWORD=<password>
   ```

   The password must be between 8 and 64 characters long and must contain at least the following:

   * One uppercase letter
   * One lowercase letter
   * One digit
   * One special character from \*\*-!@#\$^&\*\_=+:;'"\\|/?,.\~\§\±()\[]\{}\<>\\\`\*\*.

2. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud. Save the ID to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account get-by-name \
     --name mlflow-sa \
     --format jsonpath='{.metadata.id}')
   ```

3. Get the ID of the default network and save it to an environment variable:

   ```bash theme={null}
   export NETWORK_ID=$(nebius vpc network get-by-name \
     --name default-network \
     --format jsonpath='{.metadata.id}')
   ```

4. Create a test cluster:

   ```bash theme={null}
   nebius msp mlflow v1alpha1 cluster create \
     --name mlflow-test-cluster \
     --service-account-id $SA_ID \
     --network-id $NETWORK_ID \
     --admin-username admin \
     --admin-password $PASSWORD \
     --public-access=true
   ```

**Go SDK**

1. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud:

   ```go theme={null}
   serviceAccount, err := sdk.Services().IAM().V1().
       ServiceAccount().GetByName(
           ctx,
           &iam.GetServiceAccountByNameRequest{
               ParentId: "<project_ID>",
               Name: "mlflow-sa",
           },
       )
   if err != nil {
       return fmt.Errorf("get service account by name: %w", err)
   }
   serviceAccountID := serviceAccount.GetMetadata().GetId()
   fmt.Println(serviceAccountID)
   ```

   In `ParentId`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code prints the service account ID.

2. Get the ID of the default network:

   ```go theme={null}
   network, err := sdk.Services().VPC().V1().Network().
       GetByName(
           ctx,
           &vpc.GetNetworkByNameRequest{
               ParentId: "<project_ID>",
               Name: "default-network",
           },
       )
   if err != nil {
       return fmt.Errorf("get network by name: %w", err)
   }
   networkID := network.GetMetadata().GetId()
   fmt.Println(networkID)
   ```

   The code prints the network ID.

3. Create a test cluster:

   ```go theme={null}
   createService := sdk.Services().MSP().MLFlow().
       V1Alpha1().Cluster()
   createOperation, err := createService.Create(
       ctx,
       &mlflow.CreateClusterRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<project_ID>",
               Name: "mlflow-test-cluster",
           },
           Spec: &mlflow.ClusterSpec{
               NetworkId: "<network_ID>",
               ServiceAccountId: "<service_account_ID>",
               AdminUsername: "admin",
               AdminPassword: "<password>",
               PublicAccess: true,
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create cluster: %w", err)
   }
   _, err = createOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for cluster creation: %w", err)
   }
   ```

   The code creates the `mlflow-test-cluster` cluster with the `admin` administrator username and both public and private tracking endpoints. In the code, specify the following values:

   * `Metadata.ParentId`: Project ID.
   * `Spec.NetworkId`: Network ID that you got earlier.
   * `Spec.ServiceAccountId`: ID of the `mlflow-sa` service account that you got earlier.
   * `Spec.AdminPassword`: Strong password for the cluster administrator.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from \*\*-!@#\$^&\*\_=+:;'"\\|/?,.\~\§\±()\[]\{}\<>\\\`\*\*.

**Python SDK**

1. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud:

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account = await service_account_service.get_by_name(
       GetServiceAccountByNameRequest(
           parent_id="<project_ID>",
           name="mlflow-sa",
       ),
   )
   service_account_id = service_account.metadata.id
   print(service_account_id)
   ```

   In `parent_id`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code prints the service account ID.

2. Get the ID of the default network:

   ```python theme={null}
   network_service = NetworkServiceClient(sdk)
   network = await network_service.get_by_name(
       GetNetworkByNameRequest(
           parent_id="<project_ID>",
           name="default-network",
       ),
   )
   network_id = network.metadata.id
   print(network_id)
   ```

   The code prints the network ID.

3. Create a test cluster:

   ```python theme={null}
   create_service = mlflow.ClusterServiceClient(sdk)
   create_operation = await create_service.create(
       mlflow.CreateClusterRequest(
           metadata=ResourceMetadata(
               parent_id="<project_ID>",
               name="mlflow-test-cluster",
           ),
           spec=mlflow.ClusterSpec(
               network_id="<network_ID>",
               service_account_id="<service_account_ID>",
               admin_username="admin",
               admin_password="<password>",
               public_access=True,
           ),
       ),
   )
   await create_operation.wait()
   ```

   The code creates the `mlflow-test-cluster` cluster with the `admin` administrator username and both public and private tracking endpoints. In the code, specify the following values:

   * `metadata.parent_id`: Project ID.
   * `spec.network_id`: Network ID that you got earlier.
   * `spec.service_account_id`: ID of the `mlflow-sa` service account that you got earlier.
   * `spec.admin_password`: Strong password for the cluster administrator.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from \*\*-!@#\$^&\*\_=+:;'"\\|/?,.\~\§\±()\[]\{}\<>\\\`\*\*.

**JavaScript SDK**

1. Get the ID of the `mlflow-sa` service account. It was created by default after you [signed up](https://docs.nebius.com/signup-billing/sign-up.md) for Nebius AI Cloud:

   ```ts theme={null}
   const serviceAccountService =
     new ServiceAccountService(sdk);
   const serviceAccount = await serviceAccountService.getByName(
     GetServiceAccountByNameRequest.create({
       parentId: "<project_ID>",
       name: "mlflow-sa",
     }),
   ).result;
   const serviceAccountId = serviceAccount.metadata.id;
   console.log(serviceAccountId);
   ```

   In `parentId`, specify the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id). The code prints the service account ID.

2. Get the ID of the default network:

   ```ts theme={null}
   const networkService = new NetworkService(sdk);
   const network = await networkService.getByName(
     GetNetworkByNameRequest.create({
       parentId: "<project_ID>",
       name: "default-network",
     }),
   ).result;
   const networkId = network.metadata.id;
   console.log(networkId);
   ```

   The code prints the network ID.

3. Create a test cluster:

   ```ts theme={null}
   const createService = new mlflow.ClusterService(sdk);
   const createOperation = await createService.create(
     mlflow.CreateClusterRequest.create({
       metadata: {
         parentId: "<project_ID>",
         name: "mlflow-test-cluster",
       },
       spec: {
         networkId: "<network_ID>",
         serviceAccountId: "<service_account_ID>",
         adminUsername: "admin",
         adminPassword: "<password>",
         publicAccess: true,
       },
     }),
   ).result;
   await createOperation.wait();
   ```

   The code creates the `mlflow-test-cluster` cluster with the `admin` administrator username and both public and private tracking endpoints. In the code, specify the following values:

   * `metadata.parentId`: Project ID.
   * `spec.networkId`: Network ID that you got earlier.
   * `spec.serviceAccountId`: ID of the `mlflow-sa` service account that you got earlier.
   * `spec.adminPassword`: Strong password for the cluster administrator.

     The password must be between 8 and 64 characters long and must contain at least the following:

     * One uppercase letter
     * One lowercase letter
     * One digit
     * One special character from \*\*-!@#\$^&\*\_=+:;'"\\|/?,.\~\§\±()\[]\{}\<>\\\`\*\*.

Together with the cluster, Managed Service for MLflow creates a bucket in Object Storage to store the experiment logs and metrics. This bucket is not deleted automatically after you delete the cluster. You are still charged for the bucket until you [delete](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets) it.

### Configure connection to MLflow Tracking

1. Get the cluster tracking endpoint and save it to an environment variable:

   **Web console**

   Go to the cluster page and copy the **Public Tracking URI** value. Prepend `https://` to it and save the resulting URL to an environment variable:

   ```bash theme={null}
   export MLFLOW_TRACKING_URI=https://<public_tracking_URI>
   ```

   **CLI**

   Run the following command:

   ```bash theme={null}
   export MLFLOW_TRACKING_URI=https://$(nebius msp mlflow v1alpha1 cluster get-by-name \
     --name mlflow-test-cluster \
     --format jsonpath='{.status.tracking_endpoint}')
   ```

   **Go SDK**

   Get the tracking endpoint of the cluster:

   ```go theme={null}
   trackingService := sdk.Services().MSP().MLFlow().
       V1Alpha1().Cluster()
   trackingCluster, err := trackingService.GetByName(
       ctx,
       &mlflow.GetClusterByNameRequest{
           ParentId: "<project_ID>",
           Name: "mlflow-test-cluster",
       },
   )
   if err != nil {
       return fmt.Errorf("get cluster by name: %w", err)
   }
   mlflowTrackingURI := "https://" +
       trackingCluster.GetStatus().GetTrackingEndpoint()
   if err := os.Setenv(
       "MLFLOW_TRACKING_URI", mlflowTrackingURI,
   ); err != nil {
       return fmt.Errorf("set tracking URI: %w", err)
   }
   fmt.Println(trackingCluster.GetStatus().GetTrackingEndpoint())
   ```

   In `ParentId`, specify the project ID. The code sets the `MLFLOW_TRACKING_URI` environment variable for the process that runs it and prints the tracking endpoint. To use the endpoint in your terminal, run the code and save its output to an environment variable:

   ```bash theme={null}
   export MLFLOW_TRACKING_URI=https://$(<command_that_runs_your_code>)
   ```

   In this command, set the command that runs your code, for example, `go run .`. The code must print only the tracking endpoint, otherwise the variable gets the whole output.

   **Python SDK**

   Get the tracking endpoint of the cluster:

   ```python theme={null}
   tracking_service = mlflow.ClusterServiceClient(sdk)
   tracking_cluster = await tracking_service.get_by_name(
       mlflow.GetClusterByNameRequest(
           parent_id="<project_ID>",
           name="mlflow-test-cluster",
       ),
   )
   os.environ["MLFLOW_TRACKING_URI"] = (
       "https://" + tracking_cluster.status.tracking_endpoint
   )
   print(tracking_cluster.status.tracking_endpoint)
   ```

   In `parent_id`, specify the project ID. The code sets the `MLFLOW_TRACKING_URI` environment variable for the process that runs it and prints the tracking endpoint. To use the endpoint in your terminal, run the code and save its output to an environment variable:

   ```bash theme={null}
   export MLFLOW_TRACKING_URI=https://$(<command_that_runs_your_code>)
   ```

   In this command, set the command that runs your code, for example, `python3 main.py`. The code must print only the tracking endpoint, otherwise the variable gets the whole output.

   **JavaScript SDK**

   Get the tracking endpoint of the cluster:

   ```ts theme={null}
   const trackingService = new mlflow.ClusterService(sdk);
   const trackingCluster = await trackingService.getByName(
     mlflow.GetClusterByNameRequest.create({
       parentId: "<project_ID>",
       name: "mlflow-test-cluster",
     }),
   ).result;
   process.env.MLFLOW_TRACKING_URI =
     "https://" + (trackingCluster.status?.trackingEndpoint ?? "");
   console.log(trackingCluster.status?.trackingEndpoint ?? "");
   ```

   In `parentId`, specify the project ID. The code sets the `MLFLOW_TRACKING_URI` environment variable for the process that runs it and prints the tracking endpoint. To use the endpoint in your terminal, run the code and save its output to an environment variable:

   ```bash theme={null}
   export MLFLOW_TRACKING_URI=https://$(<command_that_runs_your_code>)
   ```

   In this command, set the command that runs your code, for example, `node main.mjs`. The code must print only the tracking endpoint, otherwise the variable gets the whole output.

2. Set up other [environment variables](https://mlflow.org/docs/latest/python_api/mlflow.environment_variables.html) used by MLflow Tracking:

   ```bash theme={null}
   export MLFLOW_TRACKING_USERNAME=<admin_username>
   export MLFLOW_TRACKING_PASSWORD=<admin_password>
   export MLFLOW_EXPERIMENT_NAME=<default_experiment_name>
   ```

For more details on secure connection to the tracking server, see [MLflow documentation](https://mlflow.org/docs/latest/tracking/server.html#secure-tracking-server).

### Run an experiment and check its results

1. Run an experiment:

   1. Create a Python script, `nebius_mlflow_test.py`, that trains a linear regression model on a simple, randomly populated dataset and uses MLflow autologging to log the training:

      ```python theme={null}
      import mlflow
      import numpy as np
      from sklearn.model_selection import train_test_split
      from sklearn.linear_model import LinearRegression

      np.random.seed(42)
      X = np.random.rand(100, 1)
      y = 3.5 * X.squeeze() + np.random.randn(100) * 0.5
      X_train, X_test, y_train, y_test = train_test_split(
          X, y, test_size=0.2, random_state=42)

      mlflow.autolog()

      model = LinearRegression()
      model.fit(X_train, y_train)
      ```

   2. Run the script:

      ```bash theme={null}
      python3 nebius_mlflow_test.py
      ```

2. Check the experiment artifacts:

   **Web console**

   1. Go to the cluster page and click **Go to web UI**.
   2. Enter the admin credentials you specified when creating the cluster.
   3. In the MLflow UI, select the experiment you just ran and review its results.

   **CLI**

   1. Get the public tracking endpoint URL of the cluster:

      ```bash theme={null}
      nebius msp mlflow v1alpha1 cluster get-by-name \
        --name mlflow-test-cluster \
        --format jsonpath='{.status.tracking_endpoint}'
      ```

   2. Open the URL in your browser and enter the admin credentials you specified when creating the cluster.

   3. In the MLflow UI, select the experiment you just ran and review its results.

   **Go SDK**

   1. Get the public tracking endpoint URL of the cluster:

      ```go theme={null}
      publicTrackingService := sdk.Services().MSP().MLFlow().
          V1Alpha1().Cluster()
      publicTrackingCluster, err := publicTrackingService.GetByName(
          ctx,
          &mlflow.GetClusterByNameRequest{
              ParentId: "<project_ID>",
              Name: "mlflow-test-cluster",
          },
      )
      if err != nil {
          return fmt.Errorf("get cluster by name: %w", err)
      }
      fmt.Println(publicTrackingCluster.GetStatus().GetTrackingEndpoint())
      ```

      In `ParentId`, specify the project ID.

   2. Open the printed URL in your browser and enter the admin credentials you specified when creating the cluster.

   3. In the MLflow UI, select the experiment you just ran and review its results.

   **Python SDK**

   1. Get the public tracking endpoint URL of the cluster:

      ```python theme={null}
      public_tracking_service = mlflow.ClusterServiceClient(sdk)
      public_tracking_cluster = await public_tracking_service.get_by_name(
          mlflow.GetClusterByNameRequest(
              parent_id="<project_ID>",
              name="mlflow-test-cluster",
          ),
      )
      print(public_tracking_cluster.status.tracking_endpoint)
      ```

      In `parent_id`, specify the project ID.

   2. Open the printed URL in your browser and enter the admin credentials you specified when creating the cluster.

   3. In the MLflow UI, select the experiment you just ran and review its results.

   **JavaScript SDK**

   1. Get the public tracking endpoint URL of the cluster:

      ```ts theme={null}
      const publicTrackingService =
        new mlflow.ClusterService(sdk);
      const publicTrackingCluster = await publicTrackingService.getByName(
        mlflow.GetClusterByNameRequest.create({
          parentId: "<project_ID>",
          name: "mlflow-test-cluster",
        }),
      ).result;
      console.log(publicTrackingCluster.status?.trackingEndpoint ?? "");
      ```

      In `parentId`, specify the project ID.

   2. Open the printed URL in your browser and enter the admin credentials you specified when creating the cluster.

   3. In the MLflow UI, select the experiment you just ran and review its results.

> [!NOTE]
>
> If the client where you work requires a certificate, use the certificate provided by your operating system. For example, check the `/etc/ssl/` folder on macOS.
