# How to connect to a tunnel

Source: https://docs.nebius.com/tunnels/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to connect to a tunnel

To connect a service to a tunnel, configure and run a tunnel agent. You'll need the tunnel ID in the agent configuration.

## Prerequisites

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

   You need this role to create a group and grant it a role for the tunnel.

3. [Get the project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3) and the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2), and save them to environment variables:

   ```bash theme={null}
   export PROJECT_ID=<project_ID>
   ```

   ```bash theme={null}
   export TENANT_ID=<tenant_ID>
   ```

4. Get the tunnel ID by listing tunnels in your project:

   ```bash theme={null}
   nebius tunnel list
   ```

   The command uses the project ID from your CLI profile configuration. Copy the ID of the tunnel that you want to connect to and save it to an environment variable:

   ```bash theme={null}
   export TUNNEL_ID=<tunnel_ID>
   ```

5. If you plan to run the agent on a VM, [get the subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM you want to create.

   You also need the `admin` role to create a VM with a service account attached.

   Create the service account in the same project as the VM. The tunnel agent authenticates as this service account, so it only needs the [applicationtunnel.agent](https://docs.nebius.com/iam/authorization/roles.md#nebius-tunnels) role for the tunnel. It doesn't need any Compute permissions.

   > [!NOTE]
   >
   > A VM's service account is set only at creation and can't be changed afterwards. To attach a different service account, [create a new VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

   You need this role to create a group and grant it a role for the tunnel.

3. [Get the project ID](https://docs.nebius.com/iam/manage-projects.md#go-sdk-3) and the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2). You specify them in the code later.

4. Get the tunnel ID by listing tunnels in your project:

   ```go theme={null}
   listTunnelsService := sdk.Services().Tunnel().V1().
       Tunnel()
   listTunnels, err := listTunnelsService.List(
       ctx,
       &tunnel.ListTunnelRequest{},
   )
   if err != nil {
       return fmt.Errorf("list tunnels: %w", err)
   }
   fmt.Println(listTunnels)
   ```

   The code uses the project ID that you set with `gosdk.WithParentID` when initializing the SDK. In the response, find the tunnel that you want to connect to and copy its ID from `Metadata.Id`.

5. If you plan to run the agent on a VM, [get the subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM you want to create.

   You also need the `admin` role to create a VM with a service account attached.

   Create the service account in the same project as the VM. The tunnel agent authenticates as this service account, so it only needs the [applicationtunnel.agent](https://docs.nebius.com/iam/authorization/roles.md#nebius-tunnels) role for the tunnel. It doesn't need any Compute permissions.

   > [!NOTE]
   >
   > A VM's service account is set only at creation and can't be changed afterwards. To attach a different service account, [create a new VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

   You need this role to create a group and grant it a role for the tunnel.

3. [Get the project ID](https://docs.nebius.com/iam/manage-projects.md#python-sdk-3) and the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2). You specify them in the code later.

4. Get the tunnel ID by listing tunnels in your project:

   ```python theme={null}
   list_tunnels_service = TunnelServiceClient(sdk)
   list_tunnels = await list_tunnels_service.list(
       ListTunnelRequest(),
   )
   print(list_tunnels)
   ```

   The code uses the project ID that you set in `parent_id` when initializing the SDK. In the response, find the tunnel that you want to connect to and copy its ID from `metadata.id`.

5. If you plan to run the agent on a VM, [get the subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM you want to create.

   You also need the `admin` role to create a VM with a service account attached.

   Create the service account in the same project as the VM. The tunnel agent authenticates as this service account, so it only needs the [applicationtunnel.agent](https://docs.nebius.com/iam/authorization/roles.md#nebius-tunnels) role for the tunnel. It doesn't need any Compute permissions.

   > [!NOTE]
   >
   > A VM's service account is set only at creation and can't be changed afterwards. To attach a different service account, [create a new VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

   You need this role to create a group and grant it a role for the tunnel.

3. [Get the project ID](https://docs.nebius.com/iam/manage-projects.md#javascript-sdk-3) and the [tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2). You specify them in the code later.

4. Get the tunnel ID by listing tunnels in your project:

   ```ts theme={null}
   const listTunnelsService = new TunnelService(sdk);
   const listTunnels = await listTunnelsService.list(
     ListTunnelRequest.create({}),
   ).result;
   console.log(listTunnels);
   ```

   The code uses the project ID that you set in `parentId` when initializing the SDK. In the response, find the tunnel that you want to connect to and copy its ID from `metadata.id`.

5. If you plan to run the agent on a VM, [get the subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM you want to create.

   You also need the `admin` role to create a VM with a service account attached.

   Create the service account in the same project as the VM. The tunnel agent authenticates as this service account, so it only needs the [applicationtunnel.agent](https://docs.nebius.com/iam/authorization/roles.md#nebius-tunnels) role for the tunnel. It doesn't need any Compute permissions.

   > [!NOTE]
   >
   > A VM's service account is set only at creation and can't be changed afterwards. To attach a different service account, [create a new VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

## Connecting a service

To connect to a tunnel, first set up access for the tunnel agent and then launch this agent.

### Setting up access for the tunnel agent

1. Create a service account and save its ID:

   **CLI**

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account create \
     --name "tunnel-agent" \
     --parent-id "$PROJECT_ID" \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   createSaService := sdk.Services().IAM().V1().
       ServiceAccount()
   createSaOperation, err := createSaService.Create(
       ctx,
       &iam.CreateServiceAccountRequest{
           Metadata: &common.ResourceMetadata{
               Name: "tunnel-agent",
               ParentId: "<project_ID>",
           },
           Spec: &iam.ServiceAccountSpec{},
       },
   )
   if err != nil {
       return fmt.Errorf("create service account: %w", err)
   }
   createSaOperation, err = createSaOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create service account: %w", err)
   }
   saID := createSaOperation.ResourceID()
   fmt.Println(saID)
   ```

   In the code, set `ParentId` in `ResourceMetadata` to the project ID. The code prints the ID of the service account.

   **Python SDK**

   ```python theme={null}
   create_sa_service = ServiceAccountServiceClient(sdk)
   create_sa_operation = await create_sa_service.create(
       CreateServiceAccountRequest(
           metadata=ResourceMetadata(
               name="tunnel-agent",
               parent_id="<project_ID>",
           ),
           spec=ServiceAccountSpec(),
       ),
   )
   await create_sa_operation.wait()
   sa_id = create_sa_operation.resource_id
   print(sa_id)
   ```

   In the code, set `parent_id` in `ResourceMetadata` to the project ID. The code prints the ID of the service account.

   **JavaScript SDK**

   ```ts theme={null}
   const createSaService = new ServiceAccountService(sdk);
   const createSaOperation = await createSaService.create(
     CreateServiceAccountRequest.create({
       metadata: ResourceMetadata.create({
         name: "tunnel-agent",
         parentId: "<project_ID>",
       }),
       spec: ServiceAccountSpec.create({}),
     }),
   ).result;
   await createSaOperation.wait();
   const saId = createSaOperation.resourceId();
   console.log(saId);
   ```

   In the code, set `parentId` in `ResourceMetadata` to the project ID. The code prints the ID of the service account.

   > [!NOTE]
   >
   > To grant wider access instead of creating a dedicated group with the `applicationtunnel.agent` role, you can [add the service account to the `editors` group](https://docs.nebius.com/iam/service-accounts/manage#granting-editor-access-to-the-service-account).

2. Create a group for Nebius Tunnels service accounts and save its ID:

   **CLI**

   ```bash theme={null}
   export GROUP_ID=$(nebius iam group create \
     --name "tunnel-agents" \
     --parent-id "$TENANT_ID" \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   createGroupService := sdk.Services().IAM().V1().
       Group()
   createGroupOperation, err := createGroupService.Create(
       ctx,
       &iam.CreateGroupRequest{
           Metadata: &common.ResourceMetadata{
               Name: "tunnel-agents",
               ParentId: "<tenant_ID>",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create group: %w", err)
   }
   createGroupOperation, err = createGroupOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create group: %w", err)
   }
   groupID := createGroupOperation.ResourceID()
   fmt.Println(groupID)
   ```

   In the code, set `ParentId` in `ResourceMetadata` to the tenant ID. The code prints the ID of the group.

   **Python SDK**

   ```python theme={null}
   create_group_service = GroupServiceClient(sdk)
   create_group_operation = await create_group_service.create(
       CreateGroupRequest(
           metadata=ResourceMetadata(
               name="tunnel-agents",
               parent_id="<tenant_ID>",
           ),
       ),
   )
   await create_group_operation.wait()
   group_id = create_group_operation.resource_id
   print(group_id)
   ```

   In the code, set `parent_id` in `ResourceMetadata` to the tenant ID. The code prints the ID of the group.

   **JavaScript SDK**

   ```ts theme={null}
   const createGroupService = new GroupService(sdk);
   const createGroupOperation = await createGroupService.create(
     CreateGroupRequest.create({
       metadata: ResourceMetadata.create({
         name: "tunnel-agents",
         parentId: "<tenant_ID>",
       }),
     }),
   ).result;
   await createGroupOperation.wait();
   const groupId = createGroupOperation.resourceId();
   console.log(groupId);
   ```

   In the code, set `parentId` in `ResourceMetadata` to the tenant ID. The code prints the ID of the group.

3. Grant the group the `applicationtunnel.agent` role for the tunnel:

   **CLI**

   ```bash theme={null}
   nebius iam access-permit create \
     --parent-id "$GROUP_ID" \
     --resource-id "$TUNNEL_ID" \
     --role applicationtunnel.agent
   ```

   **Go SDK**

   ```go theme={null}
   accessPermitService := sdk.Services().IAM().V1().
       AccessPermit()
   accessPermitOperation, err := accessPermitService.Create(
       ctx,
       &iam.CreateAccessPermitRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<group_ID>",
           },
           Spec: &iam.AccessPermitSpec{
               ResourceId: "<tunnel_ID>",
               Role: "applicationtunnel.agent",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create access permit: %w", err)
   }
   accessPermitOperation, err = accessPermitOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create access permit: %w", err)
   }
   ```

   In the code, set `ParentId` in `ResourceMetadata` to the group ID and `ResourceId` in `AccessPermitSpec` to the tunnel ID.

   **Python SDK**

   ```python theme={null}
   access_permit_service = AccessPermitServiceClient(sdk)
   access_permit_operation = await access_permit_service.create(
       CreateAccessPermitRequest(
           metadata=ResourceMetadata(
               parent_id="<group_ID>",
           ),
           spec=AccessPermitSpec(
               resource_id="<tunnel_ID>",
               role="applicationtunnel.agent",
           ),
       ),
   )
   await access_permit_operation.wait()
   ```

   In the code, set `parent_id` in `ResourceMetadata` to the group ID and `resource_id` in `AccessPermitSpec` to the tunnel ID.

   **JavaScript SDK**

   ```ts theme={null}
   const accessPermitService = new AccessPermitService(sdk);
   const accessPermitOperation = await accessPermitService.create(
     CreateAccessPermitRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<group_ID>",
       }),
       spec: AccessPermitSpec.create({
         resourceId: "<tunnel_ID>",
         role: "applicationtunnel.agent",
       }),
     }),
   ).result;
   await accessPermitOperation.wait();
   ```

   In the code, set `parentId` in `ResourceMetadata` to the group ID and `resourceId` in `AccessPermitSpec` to the tunnel ID.

   > [!NOTE]
   >
   > To grant access to more tunnels, create the permit on a broader resource: a project or a tenant. A permit on a project applies to all tunnels in that project. A permit on a tenant applies to all tunnels in all projects in the tenant.

4. Add the service account to the group:

   **CLI**

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id "$GROUP_ID" \
     --member-id "$SA_ID"
   ```

   **Go SDK**

   ```go theme={null}
   membershipService := sdk.Services().IAM().V1().
       GroupMembership()
   membershipOperation, err := membershipService.Create(
       ctx,
       &iam.CreateGroupMembershipRequest{
           Metadata: &common.ResourceMetadata{
               ParentId: "<group_ID>",
           },
           Spec: &iam.GroupMembershipSpec{
               MemberId: "<service_account_ID>",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create group membership: %w", err)
   }
   membershipOperation, err = membershipOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create group membership: %w", err)
   }
   ```

   In the code, set `ParentId` in `ResourceMetadata` to the group ID and `MemberId` in `GroupMembershipSpec` to the service account ID.

   **Python SDK**

   ```python theme={null}
   membership_service = GroupMembershipServiceClient(sdk)
   membership_operation = await membership_service.create(
       CreateGroupMembershipRequest(
           metadata=ResourceMetadata(
               parent_id="<group_ID>",
           ),
           spec=GroupMembershipSpec(
               member_id="<service_account_ID>",
           ),
       ),
   )
   await membership_operation.wait()
   ```

   In the code, set `parent_id` in `ResourceMetadata` to the group ID and `member_id` in `GroupMembershipSpec` to the service account ID.

   **JavaScript SDK**

   ```ts theme={null}
   const membershipService = new GroupMembershipService(sdk);
   const membershipOperation = await membershipService.create(
     CreateGroupMembershipRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<group_ID>",
       }),
       spec: GroupMembershipSpec.create({
         memberId: "<service_account_ID>",
       }),
     }),
   ).result;
   await membershipOperation.wait();
   ```

   In the code, set `parentId` in `ResourceMetadata` to the group ID and `memberId` in `GroupMembershipSpec` to the service account ID.

### Installing and running the agent

You can run the tunnel agent [in Docker](#running-the-agent-in-docker), in a Kubernetes cluster [by using Helm](#running-the-agent-by-using-helm) or [on a Nebius VM](#running-the-agent-on-a-vm).

#### Creating an authorized key for Docker and Helm

In Docker and Kubernetes, the agent authenticates as the service account by using an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md). On a Nebius VM, the agent doesn't need a key, so go to [Running the agent on a VM](#running-the-agent-on-a-vm).

1. Create a key pair:

   ```bash theme={null}
   openssl genrsa -out ./private_key.pem 4096
   openssl rsa -in ./private_key.pem -pubout -out ./public_key.pem
   ```

   The command creates the `private_key.pem` and `public_key.pem` files in the current directory.

2. Upload the public key and save its ID:

   **CLI**

   ```bash theme={null}
   export PUBLIC_KEY_ID=$(nebius iam auth-public-key create \
     --account-service-account-id "$SA_ID" \
     --data "$(cat ./public_key.pem)" \
     --format jsonpath='{.metadata.id}')
   ```

   **Go SDK**

   ```go theme={null}
   publicKeyData, err := os.ReadFile("./public_key.pem")
   if err != nil {
       return fmt.Errorf("read public key: %w", err)
   }
   keyAccount := &iam.Account{
       Type: &iam.Account_ServiceAccount_{
           ServiceAccount: &iam.Account_ServiceAccount{
               Id: "<service_account_ID>",
           },
       },
   }
   publicKeyService := sdk.Services().IAM().V1().
       AuthPublicKey()
   publicKeyOperation, err := publicKeyService.Create(
       ctx,
       &iam.CreateAuthPublicKeyRequest{
           Spec: &iam.AuthPublicKeySpec{
               Account: keyAccount,
               Data: string(publicKeyData),
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create auth public key: %w", err)
   }
   publicKeyOperation, err = publicKeyOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create auth public key: %w", err)
   }
   publicKeyID := publicKeyOperation.ResourceID()
   fmt.Println(publicKeyID)
   ```

   In the code, set `Id` in `Account_ServiceAccount` to the service account ID. The code reads the public key from the `public_key.pem` file and prints the ID of the authorized key.

   **Python SDK**

   ```python theme={null}
   public_key_data = Path("./public_key.pem").read_text()
   key_account = Account(
       service_account=Account__ServiceAccount(
           id="<service_account_ID>",
       ),
   )
   public_key_service = AuthPublicKeyServiceClient(sdk)
   public_key_operation = await public_key_service.create(
       CreateAuthPublicKeyRequest(
           spec=AuthPublicKeySpec(
               account=key_account,
               data=public_key_data,
           ),
       ),
   )
   await public_key_operation.wait()
   public_key_id = public_key_operation.resource_id
   print(public_key_id)
   ```

   In the code, set `id` in `Account__ServiceAccount` to the service account ID. The code reads the public key from the `public_key.pem` file and prints the ID of the authorized key.

   **JavaScript SDK**

   ```ts theme={null}
   const publicKeyData =
     await readFile("./public_key.pem", "utf8");
   const keyAccount = Account.create({
     type: {
       $case: "serviceAccount",
       serviceAccount: Account_ServiceAccount.create({
         id: "<service_account_ID>",
       }),
     },
   });
   const publicKeyService = new AuthPublicKeyService(sdk);
   const publicKeyOperation = await publicKeyService.create(
     CreateAuthPublicKeyRequest.create({
       metadata: ResourceMetadata.create({}),
       spec: AuthPublicKeySpec.create({
         account: keyAccount,
         data: publicKeyData,
       }),
     }),
   ).result;
   await publicKeyOperation.wait();
   const publicKeyId = publicKeyOperation.resourceId();
   console.log(publicKeyId);
   ```

   In the code, set `id` in `Account_ServiceAccount` to the service account ID. The code reads the public key from the `public_key.pem` file and prints the ID of the authorized key.

#### Running the agent in Docker

1. Install [Docker Engine](https://docs.docker.com/engine/install/).

2. In the directory with the `private_key.pem` file, create `config.yaml` for the agent:

   ```yaml theme={null}
   tunnel_id: <tunnel_ID>

   iam:
     service_account:
       service_account_id: <service_account_ID>
       public_key_id: <authorized_key_ID>
       private_key_path: "./private_key.pem"

   services:
     - name: web
       target: localhost:8080
       type: http
   ```

   In the file, replace:

   * `<tunnel_ID>` with the tunnel ID. If you use the CLI, it's the value of `$TUNNEL_ID`.
   * `<service_account_ID>` with the service account ID. If you use the CLI, it's the value of `$SA_ID`.
   * `<authorized_key_ID>` with the ID of the authorized key. If you use the CLI, it's the value of `$PUBLIC_KEY_ID`.

   In the agent configuration, `services.name` can contain up to 20 characters and must use only lowercase Latin letters and digits (`[a-z0-9]`). Don't use dashes or dots.

   For multiple services, configure the `services` section like this:

   ```yaml theme={null}
   services:
     - name: api
       target: localhost:8080
       type: http
     - name: grpc
       target: localhost:9090
       type: http
       protocol: h2
     - name: db
       target: localhost:5432
       type: tcp
   ```

3. Run the agent using a cross-platform Docker image:

   ```bash theme={null}
   docker run -v $PWD:/home/nonroot \
     cr.eu-north1.nebius.cloud/marketplace/docker/nebius-tunnel-agent:latest \
     -config ./config.yaml
   ```

   When the agent connects, it returns the public endpoint for each service. The endpoint format is:

   ```text theme={null}
   <service_name>-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud:443
   ```

   Where:

   * `service_name` is the `services.name` value from the agent configuration.
   * `tunnel_masked_ID` is the mask of the tunnel ID without the `applicationtunnel-` prefix and regional routing code. For example, for `applicationtunnel-e00abcdef123456789`, the tunnel ID mask is `abcdef123456789`.
   * `region` is the [region](https://docs.nebius.com/overview/regions.md) of the project where the tunnel was created, for example `eu-north1`.

#### Running the agent by using Helm

1. [Install Helm](https://helm.sh/docs/intro/install/).

2. Create `custom.values.yaml` with the service account credentials and agent config:

   ```yaml theme={null}
   secret:
     data:
       private_key.pem: |
         # Your private key
     items:
       - key: private_key.pem
         path: sa/private_key.pem

   config:
     tunnel_id: <tunnel_ID>
     iam:
       service_account:
         service_account_id: <service_account_ID>
         public_key_id: <authorized_key_ID>
         private_key_path: sa/private_key.pem
     services:
       - name: web
         target: localhost:8080
         type: http
   ```

   In the file, replace:

   * `<tunnel_ID>` with the tunnel ID. If you use the CLI, it's the value of `$TUNNEL_ID`.
   * `<service_account_ID>` with the service account ID. If you use the CLI, it's the value of `$SA_ID`.
   * `<authorized_key_ID>` with the ID of the authorized key. If you use the CLI, it's the value of `$PUBLIC_KEY_ID`.
   * The private key placeholder with the contents of `private_key.pem`.

   In the agent configuration, `services.name` can contain up to 20 characters and must use only lowercase Latin letters and digits (`[a-z0-9]`). Don't use dashes or dots.

   For multiple services, add them to the `config.services` section:

   ```yaml theme={null}
   config:
     services:
       - name: api
         target: localhost:8080
         type: http
       - name: grpc
         target: localhost:9090
         type: http
         protocol: h2
       - name: db
         target: localhost:5432
         type: tcp
   ```

3. Install the agent in your Kubernetes cluster:

   ```bash theme={null}
   helm install nebius-tunnel-agent \
     oci://cr.eu-north1.nebius.cloud/marketplace/chart/nebius-tunnel-agent \
     -f custom.values.yaml
   ```

   When the agent connects, it returns the public endpoint for each service. The endpoint format is:

   ```text theme={null}
   <service_name>-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud:443
   ```

   Where:

   * `service_name` is the `services.name` value from the agent configuration.
   * `tunnel_masked_ID` is the mask of the tunnel ID without the `applicationtunnel-` prefix and regional routing code. For example, for `applicationtunnel-e00abcdef123456789`, the tunnel ID mask is `abcdef123456789`.
   * `region` is the [region](https://docs.nebius.com/overview/regions.md) of the project where the tunnel was created, for example `eu-north1`.

#### Running the agent on a VM

On a Nebius VM, the agent authenticates through the instance metadata service. This requires attaching a service account to the VM when you create it, as described in [Prerequisites](#prerequisites).

1. Prepare the cloud-init configuration file. You'll attach it to the VM when you create it.

   Save the following configuration to a file named `cloud-init.yaml` in your working directory. Before saving, replace:

   * `<username>` with the username you'll use to connect.
   * `<public_SSH_key>` with your SSH public key.
   * `<tunnel_ID>` with the tunnel ID. If you use the CLI, it's the value of `$TUNNEL_ID`.

   > **cloud-init.yaml**
   >
   > ```yaml theme={null}
   > users:
   >   - name: <username>
   >     sudo: "ALL=(ALL) NOPASSWD:ALL"
   >     shell: /bin/bash
   >     ssh_authorized_keys:
   >       - <public_SSH_key>
   >
   > write_files:
   >   - path: /etc/nebius-tunnel-agent/config.yaml
   >     permissions: "0640"
   >     content: |
   >       tunnel_id: <tunnel_ID>
   >
   >       iam:
   >         metadata:
   >           enabled: true
   >
   >       services:
   >         - name: web
   >           target: 127.0.0.1:8080
   >           type: http
   >
   >   - path: /etc/systemd/system/nebius-tunnel-agent.service
   >     permissions: "0644"
   >     content: |
   >       [Unit]
   >       Description=Nebius tunnel agent
   >       Documentation=https://docs.nebius.com/tunnels
   >       After=network-online.target
   >       Wants=network-online.target
   >
   >       [Service]
   >       Type=simple
   >       User=tunna
   >       Group=tunna
   >       ExecStart=/usr/local/bin/nebius-tunnel-agent --config /etc/nebius-tunnel-agent/config.yaml
   >       Restart=always
   >       RestartSec=5
   >       NoNewPrivileges=true
   >       ProtectSystem=strict
   >       ProtectHome=true
   >       PrivateTmp=true
   >       ReadOnlyPaths=/etc/nebius-tunnel-agent
   >
   >       [Install]
   >       WantedBy=multi-user.target
   >
   >   - path: /usr/local/sbin/install-nebius-tunnel-agent
   >     permissions: "0755"
   >     content: |
   >       #!/bin/bash
   >       set -euo pipefail
   >
   >       VERSION="${AGENT_VERSION:-latest}"
   >       BASE="https://storage.eu-north1.nebius.cloud/products/releases/nebius-tunnel-agent"
   >       CONF_DIR=/etc/nebius-tunnel-agent
   >
   >       # Select the agent archive for the VM architecture
   >       case "$(uname -m)" in
   >         x86_64)        PLATFORM=linux-x86_64 ;;
   >         aarch64|arm64) PLATFORM=linux-aarch64 ;;
   >         *) echo "unsupported architecture: $(uname -m)" >&2; exit 1 ;;
   >       esac
   >       ASSET="nebius-tunnel-agent-${PLATFORM}.tar.gz"
   >
   >       TMP="$(mktemp -d)"
   >       trap 'rm -rf "$TMP"' EXIT
   >
   >       # Download a file with retry handling
   >       fetch() {
   >         curl -fsSL --retry 5 --retry-delay 3 --retry-connrefused -o "$2" "$1"
   >       }
   >
   >       # Download and verify the agent archive
   >       fetch "$BASE/$VERSION/$ASSET" "$TMP/$ASSET"
   >       fetch "$BASE/$VERSION/checksums-sha256.txt" "$TMP/checksums-sha256.txt"
   >       (cd "$TMP" && sha256sum --ignore-missing -c checksums-sha256.txt)
   >
   >       # Install the agent binary
   >       tar -xzf "$TMP/$ASSET" -C "$TMP"
   >       install -m0755 "$TMP/nebius-tunnel-agent" /usr/local/bin/nebius-tunnel-agent
   >
   >       # Create the dedicated system user and start the service
   >       getent group tunna >/dev/null || groupadd --system tunna
   >       id -u tunna >/dev/null 2>&1 || useradd --system --gid tunna \
   >         --no-create-home --shell /usr/sbin/nologin tunna
   >       chown -R tunna:tunna "$CONF_DIR"
   >       chmod 0750 "$CONF_DIR"
   >       chmod 0640 "$CONF_DIR/config.yaml"
   >
   >       systemctl daemon-reload
   >       systemctl enable nebius-tunnel-agent.service
   >       systemctl restart nebius-tunnel-agent.service
   >
   > runcmd:
   >   - [/usr/local/sbin/install-nebius-tunnel-agent]
   > ```
   >
   > This configuration enables the following actions:
   >
   > * Add a username and a public SSH key to the VM.
   > * Download the tunnel agent, verify its checksum and install it as a systemd service running under a dedicated `tunna` system user.
   > * Authenticate by using the service account attached to the VM, through the instance metadata service. No key files are involved.
   > * Create the `web` [Nebius Tunnels service](https://docs.nebius.com/tunnels/overview.md#supported-traffic) that exposes `127.0.0.1:8080` on the VM.

   In the agent configuration, `services.name` can contain up to 20 characters and must use only lowercase Latin letters and digits (`[a-z0-9]`). Don't use dashes or dots.

   For multiple services, add them to the `services` section of `config.yaml` in the `cloud-init` file:

   ```yaml theme={null}
   services:
     - name: api
       target: 127.0.0.1:8080
       type: http
     - name: grpc
       target: 127.0.0.1:9090
       type: http
       protocol: h2
     - name: db
       target: 127.0.0.1:5432
       type: tcp
   ```

2. Create the VM:

   **CLI**

   ```bash theme={null}
   nebius compute instance create \
     --name tunnel-agent-vm \
     --resources-platform cpu-d3 \
     --resources-preset 4vcpu-16gb \
     --boot-disk-attach-mode READ_WRITE \
     --boot-disk-managed-disk-name tunnel-agent-vm-boot \
     --boot-disk-managed-disk-type network_ssd \
     --boot-disk-managed-disk-size-gibibytes 20 \
     --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-driverless \
     --network-interfaces "[{\"name\": \"eth0\", \"ip_address\": {}, \"public_ip_address\": {}, \"subnet_id\": \"<subnet_ID>\"}]" \
     --service-account-id <service_account_ID> \
     --cloud-init-user-data "$(cat cloud-init.yaml)"
   ```

   In the command, specify the subnet ID from [Prerequisites](#prerequisites) and the ID of the service account you created earlier.

   **Go SDK**

   ```go theme={null}
   cloudInit, err := os.ReadFile("cloud-init.yaml")
   if err != nil {
       return fmt.Errorf("read cloud init: %w", err)
   }
   resources := &compute.ResourcesSpec{
       Platform: "cpu-d3",
       Size: &compute.ResourcesSpec_Preset{
           Preset: "4vcpu-16gb",
       },
   }
   bootDiskSpec := &compute.DiskSpec{
       Type: compute.DiskSpec_NETWORK_SSD,
       Size: &compute.DiskSpec_SizeGibibytes{
           SizeGibibytes: 20,
       },
       Source: &compute.DiskSpec_SourceImageFamily{
           SourceImageFamily: &compute.SourceImageFamily{
               ImageFamily: "ubuntu24.04-driverless",
           },
       },
   }
   bootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "tunnel-agent-vm-boot",
               Spec: bootDiskSpec,
           },
       },
   }
   networkInterface := &compute.NetworkInterfaceSpec{
       Name: "eth0",
       SubnetId: "<subnet_ID>",
       IpAddress: &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   createInstanceService := sdk.Services().Compute().V1().
       Instance()
   createInstanceOperation, err := createInstanceService.Create(
       ctx,
       &compute.CreateInstanceRequest{
           Metadata: &common.ResourceMetadata{
               Name: "tunnel-agent-vm",
           },
           Spec: &compute.InstanceSpec{
               Resources: resources,
               BootDisk: bootDisk,
               NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                   networkInterface,
               },
               ServiceAccountId: "<service_account_ID>",
               CloudInitUserData: string(cloudInit),
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create instance: %w", err)
   }
   createInstanceOperation, err = createInstanceOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create instance: %w", err)
   }
   ```

   In the code, set `SubnetId` in `NetworkInterfaceSpec` to the subnet ID from [Prerequisites](#prerequisites) and `ServiceAccountId` in `InstanceSpec` to the ID of the service account you created earlier. The code reads the cloud-init configuration from the `cloud-init.yaml` file in the working directory.

   **Python SDK**

   ```python theme={null}
   cloud_init = Path("cloud-init.yaml").read_text()
   boot_disk_spec = DiskSpec(
       type=DiskSpec.DiskType.NETWORK_SSD,
       size_gibibytes=20,
       source_image_family=SourceImageFamily(
           image_family="ubuntu24.04-driverless",
       ),
   )
   boot_disk = AttachedDiskSpec(
       attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
       managed_disk=ManagedDisk(
           name="tunnel-agent-vm-boot",
           spec=boot_disk_spec,
       ),
   )
   network_interface = NetworkInterfaceSpec(
       name="eth0",
       subnet_id="<subnet_ID>",
       ip_address=IPAddress(),
       public_ip_address=PublicIPAddress(),
   )
   create_instance_service = InstanceServiceClient(sdk)
   create_instance_operation = await create_instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(
               name="tunnel-agent-vm",
           ),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-d3",
                   preset="4vcpu-16gb",
               ),
               boot_disk=boot_disk,
               network_interfaces=[network_interface],
               service_account_id="<service_account_ID>",
               cloud_init_user_data=cloud_init,
           ),
       ),
   )
   await create_instance_operation.wait()
   ```

   In the code, set `subnet_id` in `NetworkInterfaceSpec` to the subnet ID from [Prerequisites](#prerequisites) and `service_account_id` in `InstanceSpec` to the ID of the service account you created earlier. The code reads the cloud-init configuration from the `cloud-init.yaml` file in the working directory.

   **JavaScript SDK**

   ```ts theme={null}
   const cloudInit = await readFile("cloud-init.yaml", "utf8");
   const sourceImage = SourceImageFamily.create({
     imageFamily: "ubuntu24.04-driverless",
   });
   const bootDiskSpec = DiskSpec.create({
     type: DiskSpec_DiskType.NETWORK_SSD,
     size: {
       $case: "sizeGibibytes",
       sizeGibibytes: 20,
     },
     source: {
       $case: "sourceImageFamily",
       sourceImageFamily: sourceImage,
     },
   });
   const managedDisk = ManagedDisk.create({
     name: "tunnel-agent-vm-boot",
     spec: bootDiskSpec,
   });
   const bootDisk = AttachedDiskSpec.create({
     attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
     type: {
       $case: "managedDisk",
       managedDisk,
     },
   });
   const networkInterface = NetworkInterfaceSpec.create({
     name: "eth0",
     subnetId: "<subnet_ID>",
     ipAddress: IPAddress.create({}),
     publicIpAddress: PublicIPAddress.create({}),
   });
   const createInstanceService = new InstanceService(sdk);
   const createInstanceOperation =
     await createInstanceService.create(
       CreateInstanceRequest.create({
         metadata: ResourceMetadata.create({
           name: "tunnel-agent-vm",
         }),
         spec: InstanceSpec.create({
           resources: ResourcesSpec.create({
             platform: "cpu-d3",
             size: {
               $case: "preset",
               preset: "4vcpu-16gb",
             },
           }),
           bootDisk: bootDisk,
           networkInterfaces: [networkInterface],
           serviceAccountId: "<service_account_ID>",
           cloudInitUserData: cloudInit,
         }),
       }),
     ).result;
   await createInstanceOperation.wait();
   ```

   In the code, set `subnetId` in `NetworkInterfaceSpec` to the subnet ID from [Prerequisites](#prerequisites) and `serviceAccountId` in `InstanceSpec` to the ID of the service account you created earlier. The code reads the cloud-init configuration from the `cloud-init.yaml` file in the working directory.

3. Get the public IP address of the VM:

   **CLI**

   ```bash theme={null}
   export PUBLIC_IP_ADDRESS=$(nebius compute instance get-by-name \
     --name <VM_name> \
     --format json \
     | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
   ```

   In the command, specify the name of the VM you created.

   **Go SDK**

   ```go theme={null}
   publicInstance, err := sdk.Services().Compute().V1().
       Instance().GetByName(
           ctx,
           &common.GetByNameRequest{
               Name: "<VM_name>",
           },
       )
   if err != nil {
       return err
   }
   publicAddress := publicInstance.GetStatus().
       GetNetworkInterfaces()[0].GetPublicIpAddress().GetAddress()
   publicIPAddress := strings.Split(publicAddress, "/")[0]
   if publicIPAddress == "" {
       return fmt.Errorf("public IP address is missing")
   }
   ```

   In the code, set `Name` in `GetByNameRequest` to the name of the VM you created. The code saves the public IP address to `publicIPAddress`.

   **Python SDK**

   ```python theme={null}
   public_ip_service = InstanceServiceClient(sdk)
   public_instance = await public_ip_service.get_by_name(
       GetByNameRequest(name="<VM_name>"),
   )
   public_address = (
       public_instance.status.network_interfaces[0]
       .public_ip_address.address
   )
   public_ip_address = public_address.split("/")[0]
   ```

   In the code, set `name` in `GetByNameRequest` to the name of the VM you created. The code saves the public IP address to `public_ip_address`.

   **JavaScript SDK**

   ```ts theme={null}
   const publicIpInstanceService = new InstanceService(sdk);
   const publicIpInstance = await publicIpInstanceService.getByName(
     GetByNameRequest.create({
       name: "<VM_name>",
     }),
   );
   const publicAddress = publicIpInstance.status
     ?.networkInterfaces[0]?.publicIpAddress?.address;
   let publicIpAddress = publicAddress?.split("/")[0];
   ```

   In the code, set `name` in `GetByNameRequest` to the name of the VM you created. The code saves the public IP address to `publicIpAddress`.

   To connect from another VM in the same network, get the [private IP address or FQDN](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) instead.

4. Connect to the VM:

   ```bash theme={null}
   ssh <username>@<VM_address_or_FQDN>
   ```

5. Verify that the agent registered with the tunnel:

   To confirm that the agent registered with the tunnel, check the status of the service:

   ```bash theme={null}
   sudo systemctl status nebius-tunnel-agent
   ```

   For live logs, run:

   ```bash theme={null}
   sudo journalctl -u nebius-tunnel-agent -f
   ```

   If the agent doesn't register, check the logs for these common causes:

   * **The VM has no service account attached.** `systemctl status` still shows `active (running)`, but the agent retries indefinitely, showing `IMDS token request failed: 404 Not Found` followed by `connection closed before registering`.
     You can't attach a service account to an existing VM. Create a new one with `--service-account-id` instead.
   * **The attached service account doesn't have the `applicationtunnel.agent` role.** The agent authenticates, but the tunnel rejects the connection.
     Grant the role to the service account as described earlier in this guide.

   In the log output, the agent reports the public endpoint for each service. The endpoint format is:

   ```text theme={null}
   <service_name>-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud
   ```

   Where:

   * `service_name` is the `services.name` value from the agent configuration.
   * `tunnel_masked_ID` is the mask of the tunnel ID without the `applicationtunnel-` prefix and regional routing code. For example, for `applicationtunnel-e00abcdef123456789`, the tunnel ID mask is `abcdef123456789`.
   * `region` is the [region](https://docs.nebius.com/overview/regions.md) of the project where the tunnel was created, for example `eu-north1`.
