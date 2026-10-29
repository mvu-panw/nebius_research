# Receiving webhooks in a private service by using Nebius Tunnels

Source: https://docs.nebius.com/tunnels/tutorials/webhook

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Receiving webhooks in a private service by using Nebius Tunnels

Webhook providers such as GitHub, Stripe and Telegram send requests to publicly reachable HTTPS endpoints. A webhook handler running on a virtual machine (VM) without a public IP address cannot receive these requests directly. Nebius Tunnels provides a public HTTPS endpoint for the webhook handler. A tunnel agent running on the VM establishes an outbound connection to Nebius Tunnels. When a webhook provider sends a request to the public endpoint, Nebius Tunnels forwards it through this connection to the handler on the VM. The VM does not need an open inbound firewall port. The tunnel URL remains stable for the lifetime of the tunnel. You can configure this URL as the webhook endpoint in the external service and continue using the same URL for subsequent requests.

When the VM starts, the tunnel agent starts automatically and connects to the tunnel. Requests sent to the public tunnel URL are forwarded through this connection to the service running on the VM.

## Limitations

Before creating the infrastructure, consider the following:

* Connect only one VM to each tunnel. Connecting multiple VMs to the same tunnel is not supported.
* Nebius Tunnels forwards incoming requests but does not authenticate their senders. Configure your webhook handler to verify the signature provided by the webhook provider.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Compute virtual machine](https://docs.nebius.com/compute/resources/pricing.md#virtual-machines-gpus-vcpus-ram)
* [Boot disk](https://docs.nebius.com/compute/resources/pricing.md#disks) attached to the VM

Nebius Tunnels is [in preview](https://docs.nebius.com/overview/services.md#service-and-application-stages) and provided free of charge.

## Steps

### Create a tunnel

**Web console**

1. In the [web console](https://console.nebius.com), select the project where you want to create the infrastructure. All resources must be located in the same project.
2. Go to  **Networking** → **Tunnels**.
3. Click  **Create tunnel**.
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

Create a VM without a public IP address and use a cloud-init configuration to install and start the tunnel agent and a sample webhook handler. Attach the service account you configured earlier so that the tunnel agent can connect to the tunnel.

> [!WARNING]
>
> If you need to change the VM configuration later, update `webhook.yaml`, delete the VM and create a new one. A tunnel should be associated with only one VM, and you can't change the cloud-init configuration of an existing VM.

1. [Generate an SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md#generating-a-key-pair).

2. Prepare the cloud-init configuration file. You'll attach it to the VM.

   In this file, specify two parameters:

   * `users.ssh_authorized_keys`: Public SSH key.
   * `write_files.content.tunnel_id`: ID of the tunnel.

   > **webhook.yaml**
   >
   > ```yaml theme={null}
   > #cloud-config
   > users:
   >   - name: ubuntu
   >     sudo: "ALL=(ALL) NOPASSWD:ALL"
   >     shell: /bin/bash
   >     ssh_authorized_keys:
   >       - <public_SSH_key>
   >
   > # Driverless images don't include Docker, so install it during VM initialization.
   > package_update: true
   > packages:
   >   - docker.io
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
   >         - name: hook
   >           type: http
   >           target: 127.0.0.1:8080
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
   >   - path: /etc/systemd/system/webhook-sink.service
   >     permissions: "0644"
   >     content: |
   >       [Unit]
   >       Description=go-httpbin webhook sink (behind a Nebius tunnel)
   >       After=network-online.target docker.service
   >       Wants=network-online.target
   >       Requires=docker.service
   >
   >       [Service]
   >       ExecStartPre=-/usr/bin/docker rm -f webhook-sink
   >       ExecStartPre=/usr/bin/docker pull ghcr.io/mccutchen/go-httpbin:2.22
   >       ExecStart=/usr/bin/docker run --rm --name webhook-sink \
   >         -p 127.0.0.1:8080:8080 \
   >         ghcr.io/mccutchen/go-httpbin:2.22
   >       ExecStop=/usr/bin/docker stop webhook-sink
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
   >   - systemctl enable --now webhook-sink.service
   > ```
   >
   > This configuration enables the following actions:
   >
   > * Add a username and a public SSH key to the VM.
   >
   > * Install Docker on the VM.
   >
   > * Authenticate by using the service account attached to the VM.
   >
   > * Create two [Nebius Tunnels services](https://docs.nebius.com/tunnels/overview.md#supported-traffic):
   >
   >   * `hook`: To receive incoming webhook requests on port 8080.
   >   * `ssh`: To connect to the VM by using SSH.
   >
   > * Deploy the tunnel agent on the VM.
   >
   > * Deploy `go-httpbin` as a placeholder webhook receiver. Replace it with your own service and point `target` at its port.

3. Create the VM:

   **Web console**

   1. In the sidebar, go to  **Compute** → **Virtual machines**.

   2. Click **Create resource** → **Virtual machine**.

      The creation flow is a step-by-step wizard. The sidebar shows your progress through the configuration sections. To move between sections, click **Back** and **Next**.

   3. On the **Compute** step, configure computing resources:

      1. In the **Platform** section, select:

         * Without GPUs
         * Regular
         * Non-GPU AMD Epyc Genoa

      2. In the **Settings** section, set:

         * **Preset**: 2 CPUs - 8 GiB RAM.
         * **Project**: The project where you create all resources for the tunnel.
         * **VM name**: `tunnel-hook`.

   4. On the **Storage** step, preserve the **Ubuntu 24.04 LTS** disk image and the SSD disk type, but change the disk size to 20 GiB.

   5. On the **Network** step, check the network and subnet. Keep **None** in the **Public IP address** field.

   6. On the **Configuration** step, configure the access, identity and VM startup settings:

      1. In the **Service account** field, select the `tunnel-agent-sa` service account.
      2. Enable a custom cloud-init configuration file.
      3. In the field that appears, paste the contents of the `webhook.yaml` file prepared earlier.

   7. On the **Review** step, check the full VM configuration. To change a section quickly, click  next to the corresponding block. The wizard opens the relevant step with your current settings.

   8. Click **Create VM**.

   **CLI**

   ```bash theme={null}
   nebius compute instance create \
     --name tunnel-hook \
     --resources-platform cpu-e2 \
     --resources-preset 2vcpu-8gb \
     --boot-disk-attach-mode READ_WRITE \
     --boot-disk-managed-disk-name tunnel-hook-boot \
     --boot-disk-managed-disk-type network_ssd \
     --boot-disk-managed-disk-size-gibibytes 20 \
     --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-driverless \
     --network-interfaces "[{\"name\": \"eth0\", \"ip_address\": {}, \"subnet_id\": \"<subnet_ID>\"}]" \
     --service-account-id <service_account_ID> \
     --cloud-init-user-data "$(cat webhook.yaml)"
   ```

   In the command, specify the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and the ID of the `tunnel-agent-sa` service account.

   **Go SDK**

   ```go theme={null}
   webhookCloudInit, err := os.ReadFile("webhook.yaml")
   if err != nil {
       return fmt.Errorf("read cloud init: %w", err)
   }
   webhookResources := &compute.ResourcesSpec{
       Platform: "cpu-e2",
       Size: &compute.ResourcesSpec_Preset{
           Preset: "2vcpu-8gb",
       },
   }
   webhookBootDiskSpec := &compute.DiskSpec{
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
   webhookBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "tunnel-hook-boot",
               Spec: webhookBootDiskSpec,
           },
       },
   }
   webhookNetworkInterface := &compute.NetworkInterfaceSpec{
       Name: "eth0",
       SubnetId: "<subnet_ID>",
       IpAddress: &compute.IPAddress{},
   }
   createWebhookVmService := sdk.Services().Compute().V1().
       Instance()
   createWebhookVmOperation, err := createWebhookVmService.Create(
       ctx,
       &compute.CreateInstanceRequest{
           Metadata: &common.ResourceMetadata{
               Name: "tunnel-hook",
           },
           Spec: &compute.InstanceSpec{
               Resources: webhookResources,
               BootDisk: webhookBootDisk,
               NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                   webhookNetworkInterface,
               },
               ServiceAccountId: "<service_account_ID>",
               CloudInitUserData: string(webhookCloudInit),
           },
       },
   )
   if err != nil {
       return fmt.Errorf("create instance: %w", err)
   }
   createWebhookVmOperation, err = createWebhookVmOperation.Wait(ctx)
   if err != nil {
       return fmt.Errorf("wait for create instance: %w", err)
   }
   ```

   In the code, set `SubnetId` in `NetworkInterfaceSpec` to the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and `ServiceAccountId` in `InstanceSpec` to the ID of the `tunnel-agent-sa` service account. The code reads the cloud-init configuration from the `webhook.yaml` file in the working directory.

   **Python SDK**

   ```python theme={null}
   webhook_cloud_init = Path("webhook.yaml").read_text()
   webhook_boot_disk_spec = DiskSpec(
       type=DiskSpec.DiskType.NETWORK_SSD,
       size_gibibytes=20,
       source_image_family=SourceImageFamily(
           image_family="ubuntu24.04-driverless",
       ),
   )
   webhook_boot_disk = AttachedDiskSpec(
       attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
       managed_disk=ManagedDisk(
           name="tunnel-hook-boot",
           spec=webhook_boot_disk_spec,
       ),
   )
   webhook_network_interface = NetworkInterfaceSpec(
       name="eth0",
       subnet_id="<subnet_ID>",
       ip_address=IPAddress(),
   )
   create_webhook_vm_service = InstanceServiceClient(sdk)
   create_webhook_vm_operation = await create_webhook_vm_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(
               name="tunnel-hook",
           ),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="cpu-e2",
                   preset="2vcpu-8gb",
               ),
               boot_disk=webhook_boot_disk,
               network_interfaces=[webhook_network_interface],
               service_account_id="<service_account_ID>",
               cloud_init_user_data=webhook_cloud_init,
           ),
       ),
   )
   await create_webhook_vm_operation.wait()
   ```

   In the code, set `subnet_id` in `NetworkInterfaceSpec` to the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and `service_account_id` in `InstanceSpec` to the ID of the `tunnel-agent-sa` service account. The code reads the cloud-init configuration from the `webhook.yaml` file in the working directory.

   **JavaScript SDK**

   ```ts theme={null}
   const webhookCloudInit =
     await readFile("webhook.yaml", "utf8");
   const webhookSourceImage = SourceImageFamily.create({
     imageFamily: "ubuntu24.04-driverless",
   });
   const webhookBootDiskSpec = DiskSpec.create({
     type: DiskSpec_DiskType.NETWORK_SSD,
     size: {
       $case: "sizeGibibytes",
       sizeGibibytes: 20,
     },
     source: {
       $case: "sourceImageFamily",
       sourceImageFamily: webhookSourceImage,
     },
   });
   const webhookManagedDisk = ManagedDisk.create({
     name: "tunnel-hook-boot",
     spec: webhookBootDiskSpec,
   });
   const webhookBootDisk = AttachedDiskSpec.create({
     attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
     type: {
       $case: "managedDisk",
       managedDisk: webhookManagedDisk,
     },
   });
   const webhookNetworkInterface = NetworkInterfaceSpec.create({
     name: "eth0",
     subnetId: "<subnet_ID>",
     ipAddress: IPAddress.create({}),
   });
   const createWebhookVmService = new InstanceService(sdk);
   const createWebhookVmOperation =
     await createWebhookVmService.create(
       CreateInstanceRequest.create({
         metadata: ResourceMetadata.create({
           name: "tunnel-hook",
         }),
         spec: InstanceSpec.create({
           resources: ResourcesSpec.create({
             platform: "cpu-e2",
             size: {
               $case: "preset",
               preset: "2vcpu-8gb",
             },
           }),
           bootDisk: webhookBootDisk,
           networkInterfaces: [webhookNetworkInterface],
           serviceAccountId: "<service_account_ID>",
           cloudInitUserData: webhookCloudInit,
         }),
       }),
     ).result;
   await createWebhookVmOperation.wait();
   ```

   In the code, set `subnetId` in `NetworkInterfaceSpec` to the [subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) and `serviceAccountId` in `InstanceSpec` to the ID of the `tunnel-agent-sa` service account. The code reads the cloud-init configuration from the `webhook.yaml` file in the working directory.

Wait for the VM to start running.

### Check the result

The tunnel agent starts as soon as the VM boots. The `webhook-sink` service starts shortly after Docker pulls the `go-httpbin` image.

To check that the webhook endpoint is working, send a test request from your local machine:

```bash theme={null}
curl -X POST \
  https://hook-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud/anything \
  -H "Content-Type: application/json" \
  -d '{"ping": 1}'
```

In the URL, specify:

* `tunnel_masked_ID`: Mask of the tunnel ID without the `applicationtunnel-` prefix and regional routing code. Contains the last 15 characters of the tunnel ID. For example, for `applicationtunnel-e00abcdef123456789`, the masked ID of the tunnel is `abcdef123456789`.
* `region`: [Region](https://docs.nebius.com/overview/regions.md) of the project where you created the resources.

For more information about the tunnel URL, see [Supported traffic](https://docs.nebius.com/tunnels/overview.md#supported-traffic).

The expected response is a JSON object that echoes back the request details:

```json theme={null}
{
  "method": "POST",
  "url": "https://hook-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud/anything",
  "data": "{\"ping\": 1}",
  ...
}
```

If the response is `failed to connect to local service`, the `webhook-sink` service hasn't started yet. Wait a few moments and try again. If it still fails, see [Troubleshooting](#troubleshooting).

Once the endpoint is working, paste the tunnel URL — `https://hook-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud` — into the webhook settings of your provider (GitHub, Stripe, Telegram, etc.). The tunnel URL is stable for the tunnel's lifetime, so you only need to do this once.

To replace `go-httpbin` with your own webhook handler, update `webhook.yaml`, delete the VM and create it again. Configure your handler to listen on port 8080, or change the tunnel agent's `target` to match your handler's port.

## Troubleshooting

If the test request fails, or the tunnel returns `failed to connect to local service`, connect to the VM and check the tunnel agent and the webhook handler. The VM has no public IP address. Connect through the `ssh` service of the tunnel.

### Connect to the VM

Connect to the VM as described in [Connecting to a virtual machine without a public IP address](https://docs.nebius.com/tunnels/tutorials/connect-vm.md#connect-to-the-virtual-machine).

If you still can't open the session, use the [serial console](https://docs.nebius.com/compute/virtual-machines/serial-console.md) and run the checks below from there.

### Check the tunnel agent

On the VM, check the agent service and its logs:

```bash theme={null}
sudo systemctl status nebius-tunnel-agent.service
sudo journalctl -u nebius-tunnel-agent.service
```

Add `-f` to follow new log lines, for example `sudo journalctl -u nebius-tunnel-agent.service -f`.

When the agent has registered with the tunnel, the logs include the public endpoint of each service.

If the agent doesn't register, check for these common causes:

* **The VM has no service account attached.** `systemctl status` still shows `active (running)`, but the agent retries indefinitely, showing `IMDS token request failed: 404 Not Found` followed by `connection closed before registering`. You can't attach a service account to an existing VM. Delete the VM and create a new one with the `tunnel-agent-sa` service account attached.
* **The tunnel agent isn't authorized to connect to the tunnel.** Verify that the `tunnel-agent-sa` service account belongs to the `tunnel-agents` group and that the group includes the `applicationtunnel.agent` role for this tunnel. Check the steps in [Configure access for the tunnel agent](#configure-access-for-the-tunnel-agent).

Check that `tunnel_id` in the agent configuration is the ID of the tunnel you created:

```bash theme={null}
sudo grep tunnel_id /etc/nebius-tunnel-agent/config.yaml
```

The value looks like `applicationtunnel-e00abcdef123456789`. If it is still the `<tunnel_ID>` placeholder, or it points at a different tunnel, delete the VM and create it again with the correct tunnel ID in `webhook.yaml`.

### Check the webhook handler

The `hook` service forwards requests to `webhook-sink` on port 8080. Check that service and its logs:

```bash theme={null}
sudo systemctl status webhook-sink.service
sudo journalctl -u webhook-sink.service
```

`webhook-sink` runs `go-httpbin` in Docker. If the unit is active and requests still fail, check the container:

```bash theme={null}
sudo docker ps -a --filter name=webhook-sink
sudo docker logs webhook-sink
```

The first command should return a container named `webhook-sink`. Its status should begin with `Up`, and the port mapping should be `127.0.0.1:8080->8080/tcp`. This means that the container is running and its port `8080` is available through the VM's loopback interface.

The output of the second command should contain the following message:

```text theme={null}
go-httpbin listening on http://0.0.0.0:8080
```

### Check cloud-init

Use this check if either `systemctl status` command reports that the `nebius-tunnel-agent.service` or `webhook-sink.service` unit could not be found. This means that cloud-init might not have completed successfully.

Check the cloud-init output:

```bash theme={null}
sudo tail -n 200 /var/log/cloud-init-output.log
```

The log records the installation of the tunnel agent and the startup of `webhook-sink.service`. Check it for errors related to downloading or installing the tunnel agent, installing Docker or starting the webhook handler. After resolving the error, delete the VM and create it again with the corrected `webhook.yaml` file because cloud-init runs only when the VM is created.

## How to delete the created resources

The created VM and its boot disk are chargeable. If you don't need them, [delete the VM](https://docs.nebius.com/compute/virtual-machines/delete.md), so Nebius AI Cloud doesn't charge for the resources. The boot disk is deleted automatically when you delete the VM.

You can also delete free resources:

* [Tunnel](https://docs.nebius.com/tunnels/delete.md)
* [Service account](https://docs.nebius.com/iam/service-accounts/manage.md#deleting-a-service-account)
* [Custom group](https://docs.nebius.com/iam/authorization/groups/delete-groups.md)
