# Deploying an LLM on a virtual machine by using Nebius Tunnels

Source: https://docs.nebius.com/tunnels/tutorials/llm

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying an LLM on a virtual machine by using Nebius Tunnels

You can deploy and run a large language model (LLM) on a GPU virtual machine (VM) and then chat with this model via a secure [tunnel](https://docs.nebius.com/tunnels/overview.md#how-tunnels-work) in Nebius Tunnels. The VM goes without a public IP address, but by using the tunnel, anyone can access the LLM from the internet and connect to the VM. Meanwhile, the VM stays isolated.

To establish the tunnel, the VM configuration includes a tunnel agent. The agent runs on the VM automatically after the VM starts. When you send a message to the model, the tunnel routes the traffic to the agent. Thus, only the IP address of the tunnel is exposed to the internet.

> [!NOTE]
>
> Use one VM per tunnel. Do not add several VMs to a single tunnel.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machine](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram)
* [Boot disk](https://docs.nebius.com/compute/resources/pricing.md#disks) attached to the VM

Nebius Tunnels is [in preview](https://docs.nebius.com/overview/services.md#service-and-application-stages) and provided free of charge.

## Steps

### Create a tunnel

**Web console**

1. In the [web console](https://console.nebius.com), select the project where you want to create the infrastructure. All resources must be located in the same project.
2. Go to  **Networking** → **Tunnels**.
3. Click  **Create tunnel**.
4. On the page that opens, set the tunnel name to `my-tunnel`.
5. Click **Create tunnel**.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   When configuring the CLI profile, set the project where you want to create the infrastructure. All resources must be located in the same project.

   All `nebius` commands by default use the [project ID](https://docs.nebius.com/iam/manage-projects.md#how-to-get-a-project-id) from your CLI profile configuration.

2. Create a tunnel:

   ```bash theme={null}
   nebius tunnel create --title my-tunnel 
   ```

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

   When initializing the SDK, set the project where you want to create the infrastructure in `gosdk.WithParentID`. All resources must be located in the same project.

2. Create a tunnel:

   ```go theme={null}
   createTunnelService := sdk.Services().Tunnel().V1().
       Tunnel()
   createTunnelOperation, err := createTunnelService.Create(
       ctx,
       &tunnel.CreateTunnelRequest{
           Spec: &tunnel.TunnelSpec{
               Title: "my-tunnel",
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create tunnel: %w", err)
   }
   createTunnelOperation, err = createTunnelOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create tunnel: %w", err)
   }
   tunnelID := createTunnelOperation.ResourceID()
   fmt.Println(tunnelID)
   ```

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

   When initializing the SDK, set the project where you want to create the infrastructure in `parent_id`. All resources must be located in the same project.

2. Create a tunnel:

   ```python theme={null}
   create_tunnel_service = TunnelServiceClient(sdk)
   create_tunnel_operation = await create_tunnel_service.create(
       CreateTunnelRequest(
           spec=TunnelSpec(
               title="my-tunnel",
           ),
       ),
   )
   await create_tunnel_operation.wait()
   tunnel_id = create_tunnel_operation.resource_id
   print(tunnel_id)
   ```

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

   When initializing the SDK, set the project where you want to create the infrastructure in `parentId`. All resources must be located in the same project.

2. Create a tunnel:

   ```ts theme={null}
   const createTunnelService = new TunnelService(sdk);
   const createTunnelOperation = await createTunnelService.create(
     CreateTunnelRequest.create({
       metadata: ResourceMetadata.create({}),
       spec: TunnelSpec.create({
         title: "my-tunnel",
       }),
     }),
   ).result;
   await createTunnelOperation.wait();
   const tunnelId = createTunnelOperation.resourceId();
   console.log(tunnelId);
   ```

### Configure access for the tunnel agent

To authorize the VM in the tunnel, prepare a service account with the `applicationtunnel.agent` role. Later, you attach this service account to the VM.

1. Create the service account:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.
   2. Click **Create resource** → **Service account**.
   3. In the window that opens, set the name to `tunnel-agent-sa` and select the project.
   4. Click **Create and continue**.

   **CLI**

   ```bash theme={null}
   nebius iam service-account create --name tunnel-agent-sa 
   ```

   **Go SDK**

   ```go theme={null}
   createSaService := sdk.Services().IAM().V1().
       ServiceAccount()
   createSaOperation, err := createSaService.Create(
       ctx,
       &iam.CreateServiceAccountRequest{
           Metadata: &common.ResourceMetadata{
               Name: "tunnel-agent-sa",
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

   **Python SDK**

   ```python theme={null}
   create_sa_service = ServiceAccountServiceClient(sdk)
   create_sa_operation = await create_sa_service.create(
       CreateServiceAccountRequest(
           metadata=ResourceMetadata(
               name="tunnel-agent-sa",
           ),
           spec=ServiceAccountSpec(),
       ),
   )
   await create_sa_operation.wait()
   sa_id = create_sa_operation.resource_id
   print(sa_id)
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const createSaService = new ServiceAccountService(sdk);
   const createSaOperation = await createSaService.create(
     CreateServiceAccountRequest.create({
       metadata: ResourceMetadata.create({
         name: "tunnel-agent-sa",
       }),
       spec: ServiceAccountSpec.create({}),
     }),
   ).result;
   await createSaOperation.wait();
   const saId = createSaOperation.resourceId();
   console.log(saId);
   ```

2. Create a [custom group](https://docs.nebius.com/iam/authorization/groups/index.md#custom-groups) in Identity and Access Management to assign the role to the service account:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.
   2. Click **Create resource** → **Group**.
   3. In the window that opens, set the group name to `tunnel-agents`. In the **Scope** field, select the project where you create all the resources.
   4. Click **Create**.

   **CLI**

   ```bash theme={null}
   nebius iam group create --name tunnel-agents 
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

   **Python SDK**

   ```python theme={null}
   create_group_service = GroupServiceClient(sdk)
   create_group_operation = await create_group_service.create(
       CreateGroupRequest(
           metadata=ResourceMetadata(
               name="tunnel-agents",
           ),
       ),
   )
   await create_group_operation.wait()
   group_id = create_group_operation.resource_id
   print(group_id)
   ```

   **JavaScript SDK**

   ```ts theme={null}
   const createGroupService = new GroupService(sdk);
   const createGroupOperation = await createGroupService.create(
     CreateGroupRequest.create({
       metadata: ResourceMetadata.create({
         name: "tunnel-agents",
       }),
     }),
   ).result;
   await createGroupOperation.wait();
   const groupId = createGroupOperation.resourceId();
   console.log(groupId);
   ```

3. Attach the tunnel and grant the `applicationtunnel.agent` role to this group. You can't grant this role in the web console.

   **CLI**

   1. Get the group ID:

      ```bash theme={null}
      nebius iam group list
      ```

      The ID is specified in the `items.metadata.id` parameter in the output.

   2. Get the tunnel ID:

      ```bash theme={null}
      nebius tunnel list
      ```

   3. Create an access permit in the custom group:

      ```bash theme={null}
      nebius iam access-permit create \
        --parent-id <group_ID> \
        --resource-id <tunnel_ID> \
        --role applicationtunnel.agent
      ```

   **Go SDK**

   1. Get the group ID:

      ```go theme={null}
      listGroupsService := sdk.Services().IAM().V1().
          Group()
      listGroups, err := listGroupsService.List(
          ctx,
          &iam.ListGroupsRequest{},
      )
      if err != nil {
          return fmt.Errorf("list groups: %w", err)
      }
      fmt.Println(listGroups)
      ```

      In the response, the ID of the `tunnel-agents` group is in `Metadata.Id`.

   2. Get the tunnel ID:

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

   3. Create an access permit in the custom group:

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

   1. Get the group ID:

      ```python theme={null}
      list_groups_service = GroupServiceClient(sdk)
      list_groups = await list_groups_service.list(
          ListGroupsRequest(),
      )
      print(list_groups)
      ```

      In the response, the ID of the `tunnel-agents` group is in `metadata.id`.

   2. Get the tunnel ID:

      ```python theme={null}
      list_tunnels_service = TunnelServiceClient(sdk)
      list_tunnels = await list_tunnels_service.list(
          ListTunnelRequest(),
      )
      print(list_tunnels)
      ```

   3. Create an access permit in the custom group:

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

   1. Get the group ID:

      ```ts theme={null}
      const listGroupsService = new GroupService(sdk);
      const listGroups = await listGroupsService.list(
        ListGroupsRequest.create({}),
      ).result;
      console.log(listGroups);
      ```

      In the response, the ID of the `tunnel-agents` group is in `metadata.id`.

   2. Get the tunnel ID:

      ```ts theme={null}
      const listTunnelsService = new TunnelService(sdk);
      const listTunnels = await listTunnelsService.list(
        ListTunnelRequest.create({}),
      ).result;
      console.log(listTunnels);
      ```

   3. Create an access permit in the custom group:

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

4. Add the service account to the group:

   **Web console**

   1. Go to  **Administration** → **IAM**.
   2. On the **Groups** tab, find and open the `tunnel-agents` group.
   3. Click  **Add members**.
   4. In the window that opens, add the `tunnel-agent-sa` service account.
   5. Once the account is added, close the window.

   Check the group page in general. Make sure that:

   * The `tunnel-agent-sa` service account is specified on the **Members** tab.
   * The tunnel and the `applicationtunnel.agent` role are specified on the **Access permits** tab.

   **CLI**

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id <group_ID> \
     --member-id <service_account_ID>
   ```

   To get the service account ID, run:

   ```bash theme={null}
   nebius iam service-account list
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

   In the code, set `ParentId` in `ResourceMetadata` to the group ID and `MemberId` in `GroupMembershipSpec` to the ID of the `tunnel-agent-sa` service account.

   To get the service account ID, list the service accounts:

   ```go theme={null}
   listServiceAccountsService := sdk.Services().IAM().V1().
       ServiceAccount()
   listServiceAccounts, err := listServiceAccountsService.List(
       ctx,
       &iam.ListServiceAccountRequest{},
   )
   if err != nil {
       return fmt.Errorf("list service accounts: %w", err)
   }
   fmt.Println(listServiceAccounts)
   ```

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

   In the code, set `parent_id` in `ResourceMetadata` to the group ID and `member_id` in `GroupMembershipSpec` to the ID of the `tunnel-agent-sa` service account.

   To get the service account ID, list the service accounts:

   ```python theme={null}
   list_service_accounts_service = (
       ServiceAccountServiceClient(sdk)
   )
   list_service_accounts = await list_service_accounts_service.list(
       ListServiceAccountRequest(),
   )
   print(list_service_accounts)
   ```

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

   In the code, set `parentId` in `ResourceMetadata` to the group ID and `memberId` in `GroupMembershipSpec` to the ID of the `tunnel-agent-sa` service account.

   To get the service account ID, list the service accounts:

   ```ts theme={null}
   const listServiceAccountsService =
     new ServiceAccountService(sdk);
   const listServiceAccounts = await listServiceAccountsService.list(
     ListServiceAccountRequest.create({}),
   ).result;
   console.log(listServiceAccounts);
   ```

### Create a virtual machine

Prepare the VM configuration that includes the Qwen/Qwen3-8B model and the tunnel agent. Then, create the VM — the model and agent are deployed on the VM automatically.

> [!WARNING]
>
> If you need to change the VM configuration later, delete the VM and create a new one. A tunnel should be associated with only one VM, and you can't change the cloud-init configuration of an existing VM.

1. [Generate an SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md#generating-a-key-pair).

2. Prepare the cloud-init configuration file. You'll attach it to the VM.

   In this file, specify two parameters:

   * `users.ssh_authorized_keys`: Public SSH key.
   * `write_files.content.tunnel_id`: ID of the tunnel.

   > **llm.yaml**
   >
   > ```yaml theme={null}
   > users:
   >   - name: ubuntu
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
   >       logging:
   >         level: info
   >         format: json
   >
   >       services:
   >         - name: llm
   >           type: http
   >           target: 127.0.0.1:8000
   >         - name: ssh
   >           type: tcp
   >           target: 127.0.0.1:22
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
   >       fetch() {
   >         curl -fsSL --retry 5 --retry-delay 3 --retry-connrefused -o "$2" "$1"
   >       }
   >       fetch "$BASE/$VERSION/$ASSET" "$TMP/$ASSET"
   >       fetch "$BASE/$VERSION/checksums-sha256.txt" "$TMP/checksums-sha256.txt"
   >
   >       (cd "$TMP" && sha256sum --ignore-missing -c checksums-sha256.txt)
   >
   >       tar -xzf "$TMP/$ASSET" -C "$TMP"
   >       install -m0755 "$TMP/nebius-tunnel-agent" /usr/local/bin/nebius-tunnel-agent
   >
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
   >   - path: /etc/systemd/system/vllm.service
   >     permissions: "0644"
   >     content: |
   >       [Unit]
   >       Description=vLLM (OpenAI-compatible API behind a Nebius tunnel)
   >       After=network-online.target docker.service
   >       Wants=network-online.target
   >       Requires=docker.service
   >
   >       [Service]
   >       ExecStartPre=-/usr/bin/docker rm -f vllm
   >       ExecStartPre=/usr/bin/docker pull vllm/vllm-openai:latest
   >       ExecStart=/usr/bin/docker run --rm --name vllm \
   >         --gpus all \
   >         -p 127.0.0.1:8000:8000 \
   >         -v /opt/vllm/hf-cache:/root/.cache/huggingface \
   >         vllm/vllm-openai:latest \
   >         --model Qwen/Qwen3-8B \
   >         --served-model-name qwen3-8b \
   >         --max-model-len 8192 \
   >         --host 0.0.0.0 --port 8000
   >       ExecStop=/usr/bin/docker stop vllm
   >       Restart=on-failure
   >       RestartSec=10
   >       TimeoutStartSec=0
   >
   >       [Install]
   >       WantedBy=multi-user.target
   >
   > runcmd:
   >   # Agent first: the tunnel is up while the backend is still pulling images.
   >   - [/usr/local/sbin/install-nebius-tunnel-agent]
   >   - mkdir -p /opt/vllm/hf-cache
   >   - systemctl enable --now vllm.service
   > ```
   >
   > This configuration enables the following actions:
   >
   > * Add a username and a public SSH key to the VM.
   >
   > * Authenticate by using the service account attached to the VM.
   >
   > * Create two [Nebius Tunnels services](https://docs.nebius.com/tunnels/overview.md#supported-traffic):
   >
   >   * `llm`: To address the model and chat with it.
   >   * `ssh`: To connect to the VM by using SSH.
   >
   > * Deploy the tunnel agent on the VM.
   >
   > * Deploy a Docker image with the Qwen/Qwen3-8B model on the VM.

3. Create the VM:

   **Web console**

   1. In the sidebar, go to  **Compute** → **Virtual machines**.

   2. Click **Create resource** → **Virtual machine**.

      The creation flow is a step-by-step wizard. The sidebar shows your progress through the configuration sections. To move between sections, click **Back** and **Next**.

   3. On the **Compute** step, configure computing resources:

      1. In the **Platform** section, select:

         * With GPUs
         * Regular
         * NVIDIA® H100 NVLink

      2. In the **Settings** section, set:

         * **Preset**: 1 GPU - 16 CPUs - 200 GiB RAM.
         * **Project**: The project where you create all resources for the tunnel.
         * **VM name**: `tunnel-llm`.

   4. On the **Storage** step:

      1. Preserve the **Ubuntu 24.04 LTS for NVIDIA® GPUs (CUDA® 13)** disk image.
      2. Change the disk type to Network SSD IO M3.
      3. Change the disk size to 186 GiB.

   5. On the **Network** step, check the network and subnet. Keep **None** in the **Public IP address** field.

   6. On the **Configuration** step, configure the access, identity and VM startup settings:

      1. In the **Service account** field, select the `tunnel-agent-sa` service account.
      2. Enable a custom cloud-init configuration file.
      3. In the field that appears, paste the contents of the `llm.yaml` file prepared earlier.

   7. On the **Review** step, check the full VM configuration. To change a section quickly, click  next to the corresponding block. The wizard opens the relevant step with your current settings.

   8. Click **Create VM**.

   **CLI**

   ```bash theme={null}
   nebius compute instance create \
     --name tunnel-llm \
     --resources-platform gpu-h100-sxm \
     --resources-preset 1gpu-16vcpu-200gb \
     --boot-disk-attach-mode READ_WRITE \
     --boot-disk-managed-disk-name tunnel-llm-boot \
     --boot-disk-managed-disk-type network_ssd_io_m3 \
     --boot-disk-managed-disk-size-gibibytes 186 \
     --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-cuda13.0 \
     --network-interfaces "[{\"name\": \"eth0\", \"ip_address\": {}, \"subnet_id\": \"<subnet_ID>\"}]" \
     --service-account-id <service_account_ID> \
     --cloud-init-user-data "$(cat llm.yaml)"
   ```

   In the command, specify the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and the ID of the `tunnel-agent-sa` service account.

   **Go SDK**

   ```go theme={null}
   cloudInit, err := os.ReadFile("llm.yaml")
   if err != nil {
       return fmt.Errorf("read cloud init: %w", err)
   }
   resources := &compute.ResourcesSpec{
       Platform: "gpu-h100-sxm",
       Size: &compute.ResourcesSpec_Preset{
           Preset: "1gpu-16vcpu-200gb",
       },
   }
   bootDiskSpec := &compute.DiskSpec{
       Type: compute.DiskSpec_NETWORK_SSD_IO_M3,
       Size: &compute.DiskSpec_SizeGibibytes{
           SizeGibibytes: 186,
       },
       Source: &compute.DiskSpec_SourceImageFamily{
           SourceImageFamily: &compute.SourceImageFamily{
               ImageFamily: "ubuntu24.04-cuda13.0",
           },
       },
   }
   bootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "tunnel-llm-boot",
               Spec: bootDiskSpec,
           },
       },
   }
   networkInterface := &compute.NetworkInterfaceSpec{
       Name: "eth0",
       SubnetId: "<subnet_ID>",
       IpAddress: &compute.IPAddress{},
   }
   createVmService := sdk.Services().Compute().V1().
       Instance()
   createVmOperation, err := createVmService.Create(
       ctx,
       &compute.CreateInstanceRequest{
           Metadata: &common.ResourceMetadata{
               Name: "tunnel-llm",
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
   createVmOperation, err = createVmOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create instance: %w", err)
   }
   ```

   In the code, set `SubnetId` in `NetworkInterfaceSpec` to the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and `ServiceAccountId` in `InstanceSpec` to the ID of the `tunnel-agent-sa` service account. The code reads the cloud-init configuration from the `llm.yaml` file in the working directory.

   **Python SDK**

   ```python theme={null}
   cloud_init = Path("llm.yaml").read_text()
   boot_disk_spec = DiskSpec(
       type=DiskSpec.DiskType.NETWORK_SSD_IO_M3,
       size_gibibytes=186,
       source_image_family=SourceImageFamily(
           image_family="ubuntu24.04-cuda13.0",
       ),
   )
   boot_disk = AttachedDiskSpec(
       attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
       managed_disk=ManagedDisk(
           name="tunnel-llm-boot",
           spec=boot_disk_spec,
       ),
   )
   network_interface = NetworkInterfaceSpec(
       name="eth0",
       subnet_id="<subnet_ID>",
       ip_address=IPAddress(),
   )
   create_vm_service = InstanceServiceClient(sdk)
   create_vm_operation = await create_vm_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(
               name="tunnel-llm",
           ),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="gpu-h100-sxm",
                   preset="1gpu-16vcpu-200gb",
               ),
               boot_disk=boot_disk,
               network_interfaces=[network_interface],
               service_account_id="<service_account_ID>",
               cloud_init_user_data=cloud_init,
           ),
       ),
   )
   await create_vm_operation.wait()
   ```

   In the code, set `subnet_id` in `NetworkInterfaceSpec` to the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and `service_account_id` in `InstanceSpec` to the ID of the `tunnel-agent-sa` service account. The code reads the cloud-init configuration from the `llm.yaml` file in the working directory.

   **JavaScript SDK**

   ```ts theme={null}
   const cloudInit = await readFile("llm.yaml", "utf8");
   const sourceImage = SourceImageFamily.create({
     imageFamily: "ubuntu24.04-cuda13.0",
   });
   const bootDiskSpec = DiskSpec.create({
     type: DiskSpec_DiskType.NETWORK_SSD_IO_M3,
     size: {
       $case: "sizeGibibytes",
       sizeGibibytes: 186,
     },
     source: {
       $case: "sourceImageFamily",
       sourceImageFamily: sourceImage,
     },
   });
   const managedDisk = ManagedDisk.create({
     name: "tunnel-llm-boot",
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
   });
   const createVmService = new InstanceService(sdk);
   const createVmOperation = await createVmService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "tunnel-llm",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "gpu-h100-sxm",
           size: {
             $case: "preset",
             preset: "1gpu-16vcpu-200gb",
           },
         }),
         bootDisk: bootDisk,
         networkInterfaces: [networkInterface],
         serviceAccountId: "<service_account_ID>",
         cloudInitUserData: cloudInit,
       }),
     }),
   ).result;
   await createVmOperation.wait();
   ```

   In the code, set `subnetId` in `NetworkInterfaceSpec` to the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and `serviceAccountId` in `InstanceSpec` to the ID of the `tunnel-agent-sa` service account. The code reads the cloud-init configuration from the `llm.yaml` file in the working directory.

Wait for the VM to start running.

### Check the result and chat with the LLM

The first VM boot pulls the LLM Docker image and model weights. The model deployment takes 10-20 minutes. The tunnel agent becomes available before the LLM starts.

1. To check the status of the model deployment, connect to the VM through the `ssh` tunnel service:

   ```bash theme={null}
   ssh -o ProxyCommand="openssl s_client -quiet -verify_quiet -servername %h -connect %h:443" \
      ubuntu@ssh-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud
   ```

   In the VM address, specify:

   * `tunnel_masked_ID`: Mask of the tunnel ID without the `applicationtunnel-` prefix and regional routing code. Contains the last 15 characters of the tunnel ID. For example, for `applicationtunnel-e00abcdef123456789`, the masked ID of the tunnel is `abcdef123456789`.
   * `region`: [Region](https://docs.nebius.com/overview/regions.md) of the project where you created the resources.

   For more information about the tunnel URL, see [Supported traffic](https://docs.nebius.com/tunnels/overview.md#supported-traffic).

2. Check logs:

   ```bash theme={null}
   journalctl -u vllm -f
   ```

   When the logs contain `INFO: Application startup complete`, the model is ready to serve requests.

3. Disconnect from the VM.

4. Send a chat completion request from your local machine:

   ```bash theme={null}
   curl https://llm-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "qwen3-8b",
       "stream": false,
       "messages": [{"role": "user", "content": "Say hi"}]
     }'
   ```

   The result is a JSON response with the model's answer in the `choices[0].message.content` parameter.

   If the response is `failed to connect to local service`, this means that the model hasn't started yet. Wait a few minutes and try again.

## How to delete the created resources

The created VM and its boot disk are chargeable. If you don't need them, [delete the VM](https://docs.nebius.com/compute/virtual-machines/delete.md), so Nebius AI Cloud doesn't charge for the resources. The boot disk is deleted automatically when you delete the VM.

You can also delete free resources:

* [Tunnel](https://docs.nebius.com/tunnels/delete.md)
* [Service account](https://docs.nebius.com/iam/service-accounts/manage.md#deleting-a-service-account)
* [Custom group](https://docs.nebius.com/iam/authorization/groups/delete-groups.md)
