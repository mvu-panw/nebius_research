# How to enable automatic security updates

Source: https://docs.nebius.com/compute/storage/automatic-updates

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to enable automatic security updates

The Ubuntu [images](https://docs.nebius.com/compute/storage/boot-disk-images.md) used on boot disks of VMs include the `unattended-upgrades` package that can install security updates automatically. However, unexpected updates might break running GPU workloads. For this reason, unattended upgrades are disabled by default. We recommend that you check the compatibility of new library versions on a test VM, and then apply the updates manually to all running GPU nodes.

If you do need constant security updates, you can enable `unattended-upgrades`.

## For an existing VM

1. [Connect](https://docs.nebius.com/compute/virtual-machines/connect.md) to the VM.

2. Check that the updates are enabled in the configuration:

   ```bash theme={null}
   sudo nano /etc/apt/apt.conf.d/20auto-upgrades
   ```

   The following values should be equal to 1. If they are set to 0, change them to 1:

   ```bash theme={null}
   APT::Periodic::Update-Package-Lists "1";
   APT::Periodic::Unattended-Upgrade "1";
   ```

3. Start the upgrade services:

   ```bash theme={null}
   sudo systemctl unmask apt-daily.service apt-daily-upgrade.service
   sudo systemctl enable apt-daily.timer apt-daily-upgrade.timer
   sudo systemctl start apt-daily.timer apt-daily-upgrade.timer
   ```

4. Check the service status:

   ```bash theme={null}
   systemctl status apt-daily.timer apt-daily-upgrade.timer
   ```

   Output for active updates should look like the following:

   ```bash theme={null}
   ● apt-daily.timer - Daily apt download activities
        Loaded: loaded (/usr/lib/systemd/system/apt-daily.timer; enabled; preset: enabled)
        Active: active (waiting) since Wed 2025-10-01 14:59:29 UTC; 7s ago
       Trigger: Thu 2025-10-02 04:54:23 UTC; 13h left
      Triggers: ● apt-daily.service

   ● apt-daily-upgrade.timer - Daily apt upgrade and clean activities
        Loaded: loaded (/usr/lib/systemd/system/apt-daily-upgrade.timer; enabled; preset: enabled)
        Active: active (waiting) since Wed 2025-10-01 14:59:29 UTC; 7s ago
       Trigger: Thu 2025-10-02 06:10:29 UTC; 15h left
      Triggers: ● apt-daily-upgrade.service
   ```

## During VM creation

When you create a new VM, you can enable unattended upgrades for the VM in the [user data configuration](https://docs.nebius.com/compute/virtual-machines/manage.md#optional-create-a-user-data-configuration).

**Web console**

On the VM creation page in to the **User data** section, enable the custom cloud-init configuration. The window below contains the code that specifies users who can connect to the VM. Add the following code to enable updates:

```yaml theme={null}
users:
  - name: $USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - $(cat ~/.ssh/id_ed25519.pub)

package_update: true
packages:
  - unattended-upgrades

write_files:
  - path: /etc/apt/apt.conf.d/20auto-upgrades
    permissions: '0644'
    content: |
      APT::Periodic::Update-Package-Lists "1";
      APT::Periodic::Unattended-Upgrade "1";

runcmd:
  - systemctl unmask apt-daily.service apt-daily-upgrade.service
  - systemctl enable --now apt-daily.timer apt-daily-upgrade.timer
  - systemctl restart unattended-upgrades
```

**CLI**

Create a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/explanation/about-cloud-config.html) format. Add the following code to enable updates for users who can connect to the VM:

```bash theme={null}
export USER_DATA=$(jq -Rrs '.' <<EOF
#cloud-config
users:
  - name: $USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - $(cat ~/.ssh/id_ed25519.pub)

package_update: true
packages:
  - unattended-upgrades

write_files:
  - path: /etc/apt/apt.conf.d/20auto-upgrades
    permissions: '0644'
    content: |
      APT::Periodic::Update-Package-Lists "1";
      APT::Periodic::Unattended-Upgrade "1";

runcmd:
  - systemctl unmask apt-daily.service apt-daily-upgrade.service
  - systemctl enable --now apt-daily.timer apt-daily-upgrade.timer
  - systemctl restart unattended-upgrades
EOF
)
```

Pass the configured user data to the `--cloud-init-user-data` parameter in the [nebius compute instance create](https://docs.nebius.com/cli/reference/compute/instance/create.md) command.

**Terraform**

Create a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/explanation/about-cloud-config.html) format. Add the following code to enable updates for users who can connect to the VM:

```bash theme={null}
export USER_DATA=$(jq -Rrs '.' <<EOF
#cloud-config
users:
  - name: $USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - $(cat ~/.ssh/id_ed25519.pub)

package_update: true
packages:
  - unattended-upgrades

write_files:
  - path: /etc/apt/apt.conf.d/20auto-upgrades
    permissions: '0644'
    content: |
      APT::Periodic::Update-Package-Lists "1";
      APT::Periodic::Unattended-Upgrade "1";

runcmd:
  - systemctl unmask apt-daily.service apt-daily-upgrade.service
  - systemctl enable --now apt-daily.timer apt-daily-upgrade.timer
  - systemctl restart unattended-upgrades
EOF
)
```

Pass the configured user data to the `cloud_init_user_data` parameter in the Terraform resource for the VM.

**Go SDK**

Create a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/explanation/about-cloud-config.html) format. Add the following code to enable updates for users who can connect to the VM:

```go theme={null}
publicKeyBytes, err := os.ReadFile(
    os.ExpandEnv("$HOME/.ssh/id_ed25519.pub"),
)
if err != nil {
    return err
}
publicKey := strings.TrimSpace(string(publicKeyBytes))
userData := "#cloud-config\nusers:\n" +
    "  - name: user\n" +
    "    sudo: ALL=(ALL) NOPASSWD:ALL\n" +
    "    shell: /bin/bash\n" +
    "    ssh_authorized_keys:\n" +
    "      - " + publicKey + "\n\n" +
    "package_update: true\n" +
    "packages:\n" +
    "  - unattended-upgrades\n\n" +
    "write_files:\n" +
    "  - path: /etc/apt/apt.conf.d/20auto-upgrades\n" +
    "    permissions: '0644'\n" +
    "    content: |\n" +
    "      APT::Periodic::Update-Package-Lists \"1\";\n" +
    "      APT::Periodic::Unattended-Upgrade \"1\";\n\n" +
    "runcmd:\n" +
    "  - systemctl unmask apt-daily.service apt-daily-upgrade.service\n" +
    "  - systemctl enable --now apt-daily.timer apt-daily-upgrade.timer\n" +
    "  - systemctl restart unattended-upgrades"
```

Pass the configured user data to `InstanceSpec.CloudInitUserData` when creating the VM.

**Python SDK**

Create a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/explanation/about-cloud-config.html) format. Add the following code to enable updates for users who can connect to the VM:

```python theme={null}
public_key = (
    Path.home()
    .joinpath(".ssh/id_ed25519.pub")
    .read_text()
    .strip()
)
user_data = "\n".join(
    [
        "#cloud-config",
        "users:",
        "  - name: user",
        "    sudo: ALL=(ALL) NOPASSWD:ALL",
        "    shell: /bin/bash",
        "    ssh_authorized_keys:",
        f"      - {public_key}",
        "",
        "package_update: true",
        "packages:",
        "  - unattended-upgrades",
        "",
        "write_files:",
        "  - path: /etc/apt/apt.conf.d/20auto-upgrades",
        "    permissions: '0644'",
        "    content: |",
        '      APT::Periodic::Update-Package-Lists "1";',
        '      APT::Periodic::Unattended-Upgrade "1";',
        "",
        "runcmd:",
        "  - systemctl unmask apt-daily.service apt-daily-upgrade.service",
        "  - systemctl enable --now apt-daily.timer apt-daily-upgrade.timer",
        "  - systemctl restart unattended-upgrades",
    ],
)
```

Pass the configured user data to `InstanceSpec.cloud_init_user_data` when creating the VM.

**JavaScript SDK**

Create a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/explanation/about-cloud-config.html) format. Add the following code to enable updates for users who can connect to the VM:

```ts theme={null}
const publicKey = readFileSync(
  `${process.env.HOME}/.ssh/id_ed25519.pub`,
  "utf8",
).trim();
const userData = [
  "#cloud-config",
  "users:",
  "  - name: user",
  "    sudo: ALL=(ALL) NOPASSWD:ALL",
  "    shell: /bin/bash",
  "    ssh_authorized_keys:",
  "      - " + publicKey,
  "",
  "package_update: true",
  "packages:",
  "  - unattended-upgrades",
  "",
  "write_files:",
  "  - path: /etc/apt/apt.conf.d/20auto-upgrades",
  "    permissions: '0644'",
  "    content: |",
  '      APT::Periodic::Update-Package-Lists "1";',
  '      APT::Periodic::Unattended-Upgrade "1";',
  "",
  "runcmd:",
  "  - systemctl unmask apt-daily.service apt-daily-upgrade.service",
  "  - systemctl enable --now apt-daily.timer apt-daily-upgrade.timer",
  "  - systemctl restart unattended-upgrades",
].join("\n");
```

Pass the configured user data to `InstanceSpec.cloudInitUserData` when creating the VM.
