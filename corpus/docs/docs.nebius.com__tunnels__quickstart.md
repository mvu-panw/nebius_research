# Getting started with Nebius Tunnels: Connect a VM service to the internet

Source: https://docs.nebius.com/tunnels/quickstart

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started with Nebius Tunnels: Connect a VM service to the internet

The Nebius Tunnels service exposes a service to the internet without configuring firewall ports. Your service could be running anywhere: on a VM, your local machine or another cloud provider.

In this guide, you'll create a tunnel, prepare access for a tunnel agent, create a Compute virtual machine (VM) with the agent preinstalled, deploy a demo service on it and access the service through a public tunnel URL.

## Costs

Nebius Tunnels is provided free of charge during preview. If you create a VM for this guide, Nebius AI Cloud charges you for [Compute resources](https://docs.nebius.com/compute/resources/pricing.md).

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

   You need this role to create a group and grant it a role for the tunnel.

   You also need the `admin` role to create a VM with a service account attached.

   Create the service account in the same project as the VM. The tunnel agent authenticates as this service account, so it only needs the [applicationtunnel.agent](https://docs.nebius.com/iam/authorization/roles.md#nebius-tunnels) role for the tunnel. It doesn't need any Compute permissions.

   > [!NOTE]
   >
   > A VM's service account is set only at creation and can't be changed afterwards. To attach a different service account, [create a new VM](https://docs.nebius.com/compute/virtual-machines/manage.md#create-a-vm).

2. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

3. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

4. [Get the subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id) for the VM you create.

5. [Get the project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3) and save it to an environment variable:

   ```bash theme={null}
   export PROJECT_ID=<project_ID>
   ```

6. [Get the tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2) and save it to an environment variable:

   ```bash theme={null}
   export TENANT_ID=<tenant_ID>
   ```

   You need the tenant ID when granting the service account access to Nebius Tunnels.

## Steps

### Create a tunnel

Create a tunnel and save its ID:

```bash theme={null}
export TUNNEL_ID=$(nebius tunnel create \
  --title "quickstart-tunnel" \
  --format jsonpath='{.metadata.id}')
```

### Prepare agent access

On the VM, the tunnel agent authenticates through the instance metadata service — no need to generate or copy keys.

1. Create a service account for the tunnel agent and save its ID:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account create \
     --name "tunnel-agent" \
     --parent-id "$PROJECT_ID" \
     --format jsonpath='{.metadata.id}')
   ```

2. Create a group for Nebius Tunnels service accounts and save its ID:

   ```bash theme={null}
   export GROUP_ID=$(nebius iam group create \
     --name "tunnel-agents" \
     --parent-id "$TENANT_ID" \
     --format jsonpath='{.metadata.id}')
   ```

3. Grant the group the `applicationtunnel.agent` role for the tunnel:

   ```bash theme={null}
   nebius iam access-permit create \
     --parent-id "$GROUP_ID" \
     --resource-id "$TUNNEL_ID" \
     --role applicationtunnel.agent
   ```

4. Add the service account to the group:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id "$GROUP_ID" \
     --member-id "$SA_ID"
   ```

### Create the VM

1. Prepare the cloud-init configuration file. You'll attach it to the VM when you create it.

   Save the following configuration to a file named `cloud-init.yaml` in your working directory. Before saving, replace:

   * `<username>` with the username you'll use to connect
   * `<public_SSH_key>` with your SSH public key
   * `<tunnel_ID>` with the value of `$TUNNEL_ID`

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

2. Create the VM:
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

3. Get the public IP address of the VM:

   ```bash theme={null}
   export PUBLIC_IP_ADDRESS=$(nebius compute instance get-by-name \
     --name <VM_name> \
     --format json \
     | jq -r '.status.network_interfaces[0].public_ip_address.address | split("/")[0]')
   ```

   In the command, specify the name of the VM you created.

4. Connect to the VM:

   ```bash theme={null}
   ssh <username>@<VM_address_or_FQDN>
   ```

### Prepare and deploy a local HTTP service

> [!NOTE]
>
> Follow this section on your VM via SSH.

Start the `busybox` HTTP server on your VM:

1. Install the `busybox` package:

   ```sh theme={null}
   sudo apt-get update && sudo apt-get install -y busybox
   ```

2. In your home directory, create a `www/` directory and add an HTML file to serve via the tunnel:

   ```sh theme={null}
   mkdir -p ~/www
   cat > ~/www/index.html <<'EOF'
   <!DOCTYPE html>
   <html>
   <head>
     <title>Nebius Tunnels test</title>
   </head>
   <body>
     <h1>Nebius Tunnels test page</h1>
     <p>This page tests the functionality of the Nebius Tunnels service.</p>
   </body>
   </html>
   EOF
   ```

3. Create a unit file:

   ```sh theme={null}
   sudo tee /etc/systemd/system/busybox-httpd.service > /dev/null <<'EOF'
   [Unit]
   Description=Busybox HTTP service
   After=network.target

   [Service]
   ExecStart=/bin/busybox httpd -f -p 8080 -h /home/<username>/www
   Restart=on-failure
   User=<username>

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   In the unit file, replace `<username>` with the username you used to connect to the VM.

4. Apply the new unit file, start the `busybox-httpd` service and check its status:

   ```sh theme={null}
   sudo systemctl daemon-reload
   sudo systemctl enable --now busybox-httpd
   sudo systemctl status busybox-httpd
   ```

### Verify the tunnel agent

> [!NOTE]
>
> Follow this section on your VM via SSH.

The cloud-init configuration installs and starts the tunnel agent automatically when the VM boots, so there's nothing left to run manually.

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

In the log output, the agent reports the public endpoint in the following format:

```text theme={null}
<service_name>-<tunnel_masked_ID>.tunnel.applications.<region>.nebius.cloud
```

Where:

* `service_name` is the `services.name` value from the agent configuration.
* `tunnel_masked_ID` is the mask of the tunnel ID without the `applicationtunnel-` prefix and regional routing code. For example, for `applicationtunnel-e00abcdef123456789`, the tunnel ID mask is `abcdef123456789`.
* `region` is the [region](https://docs.nebius.com/overview/regions.md) of the project where the tunnel was created, for example `eu-north1`.

### Access the service on the VM via the tunnel

On your local machine, add `https://` to the beginning of the public endpoint address and open it in your browser, or run `curl https://<public_endpoint>` in your terminal.
