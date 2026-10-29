# How to create a virtual machine in Nebius AI Cloud

Source: https://docs.nebius.com/compute/virtual-machines/create

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to create a virtual machine in Nebius AI Cloud

You can create a Compute virtual machine (VM) in the [web console](https://console.nebius.com), or by using the [CLI](https://docs.nebius.com/cli/index.md), [Terraform provider](https://docs.nebius.com/terraform-provider/index.md) or SDKs. You can tailor the VM configuration to your needs and, for example, attach secondary disks and filesystems, or allocate GPU resources to your VM.

## Prerequisites

If you use the web console, you don't need to complete any prerequisites.

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Terraform**

[Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

The VM that you create this way is a *standalone VM*, which is a general-purpose Compute resource. In the [web console](https://console.nebius.com), standalone VMs are displayed on the **Standalone VMs** tab of the **Virtual machines** page.

A standalone VM can be regular or [preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md): regular VMs run until you stop them, while Compute may stop preemptible VMs at any time.

## Steps

### (Optional) Create a user data configuration

> [!TIP]
>
> You do not need to create a user data configuration in advance if you create a VM in the web console.

**CLI**

To add a user for connections to a VM, create a configuration by using the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:

```bash theme={null}
export USER_DATA=$(jq -Rrs '.' <<EOF
#cloud-config
users:
  - name: $USER
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - $(cat ~/.ssh/id_ed25519.pub)
EOF
)
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The above example sets the value of the machine's `USER` environment variable as the username for the VM.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

**Terraform**

1. To add a user for connections to a VM, create a configuration by using the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format:

   ```bash theme={null}
   export USER_DATA=$(jq -Rrs '.' <<EOF
   #cloud-config
   users:
     - name: $USER
       sudo: ALL=(ALL) NOPASSWD:ALL
       shell: /bin/bash
       ssh_authorized_keys:
         - $(cat ~/.ssh/id_ed25519.pub)
   EOF
   )
   ```

   The configuration contains the following parameters:

   * `name`: Username for connecting to the VM. The above example sets the value of the machine's `USER` environment variable as the username for the VM.

     Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

   * `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

   * `shell`: Default shell.

   * `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

     To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

   You can specify several users and their public SSH keys.

   For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

2. Put the user data to a Terraform variable, so the Terraform configuration can address it:

   ```bash theme={null}
   export TF_VAR_user_data=$(printf "%s" "$USER_DATA")
   ```

3. Check that the `TF_VAR_user_data` variable contains the correct data:

   ```bash theme={null}
   printf "TF_VAR_user_data: %s\n" "$TF_VAR_user_data"
   ```

   The output is the following:

   ```text theme={null}
   TF_VAR_user_data: #cloud-config
   users:
     - name: <username>
       sudo: ALL=(ALL) NOPASSWD:ALL
       shell: /bin/bash
       ssh_authorized_keys:
         - <public_SSH_key>
   ```

4. Create the `variables.tf` file with the following contents:

   ```hcl theme={null}
   variable "user_data" {
     description = "User data in the cloud-init format"
     type        = string
   }
   ```

   The file allows the Terraform provider to address the `TF_VAR_user_data` environment variable.

5. Initialize the working directory:

   ```bash theme={null}
   terraform init
   ```

**Go SDK**

To add a user for connections to a VM, define `userData` as a string in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format.

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
    "      - " + publicKey
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The example sets `user`; replace it with your username.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

When you create the VM, pass this string to `InstanceSpec.CloudInitUserData`. The VM applies this configuration on first boot.

**Python SDK**

To add a user for connections to a VM, define `user_data` as a string in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format.

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
    ],
)
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The example sets `user`; replace it with your username.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

When you create the VM, pass this string to `InstanceSpec.cloud_init_user_data`. The VM applies this configuration on first boot.

**JavaScript SDK**

To add a user for connections to a VM, define `userData` as a string in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format.

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
].join("\n");
```

The configuration contains the following parameters:

* `name`: Username for connecting to the VM. The example sets `user`; replace it with your username.

  Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.

* `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.

* `shell`: Default shell.

* `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

  To create the key pair, follow the instructions in [Generating SSH keys](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

You can specify several users and their public SSH keys.

For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

When you create the VM, pass this string to `InstanceSpec.cloudInitUserData`. The VM applies this configuration on first boot.

### Create a VM

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.

2. Click **Create resource** → **Virtual machine**.

   The creation flow is a step-by-step wizard. The sidebar shows your progress through the configuration sections. To move between sections, click **Back** and **Next**.

3. If you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), on the **General** step, choose how Compute allocates resources:

   * **Reserved VM**: Capacity is assured by your capacity block groups. This option is for regular VMs with GPUs. If you have active capacity block groups, the card shows how many are available.
   * **Pay-as-you-go VM**: Capacity is subject to availability. This option allows [preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) and VMs without GPUs.

   If you do not have capacity block groups, the wizard skips the **General** step and opens **Compute** instead.

4. On the **Compute** step, configure computing resources:

   **Reserved VM:**

   1. In the **Platform** section, select a [platform](https://docs.nebius.com/compute/virtual-machines/types.md).

      The list shows platforms that match your capacity block groups. Each platform card shows GPU memory, the platform ID and badges for associated capacity block groups.

   2. In the **Reservation** section, configure how Compute uses your [reservations](https://docs.nebius.com/compute/virtual-machines/reservations.md).

      The **Reservation** section is only displayed if you have capacity block groups.

      1. If you have capacity block groups in multiple regions, select a **Region**.
      2. To let Compute choose among your capacity block groups automatically, select **Any (existing and future)**.
      3. To use specific capacity block groups, select them. Each option shows the capacity block group ID, reservation period and GPU usage.
      4. Under **Switch to PAYG**, choose whether the VM can start after you create or restart it without active intervals in selected capacity block groups:

         * **When reservation is exhausted**: The VM can start as a pay-as-you-go VM when no capacity is available in the selected capacity block groups.
         * **Never**: The VM cannot start without available capacity in the selected capacity block groups.

         This does not affect the VM when it is running. If an interval in a selected capacity block group expires while the VM is running, the VM always continues as a pay-as-you-go VM, regardless of this setting.

   3. In the **Settings** section, configure the following:

      1. Select a **Preset**.

      2. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a **GPU cluster** for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

         To use a GPU cluster, select an existing one or create a new cluster:

         1. Click  **Create** in the **GPU cluster** field.
         2. In the window that opens, specify the cluster name and InfiniBand fabric. To select the fabric, see [InfiniBand fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).
         3. Click **Create**.

      3. Select the **Project** for the VM location.

      4. Specify the **VM name**.

   **Pay-as-you-go VM:**

   1. In the **Platform** section, select **With GPUs** or **Without GPUs** and the VM type **Regular** or [Preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md).

      VMs without GPUs only support the regular type.

   2. Select a [platform and preset](https://docs.nebius.com/compute/virtual-machines/types.md).

      Expand a platform card to compare available presets by region. You can also see the platforms that are not currently available.

   3. If you selected [Preemptible](https://docs.nebius.com/compute/virtual-machines/preemptible.md), in **Max price**, select or create a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md), or choose **Follow spot price**.

   4. In the **Settings** section, configure the following:

      1. Select a **Preset**.

      2. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a **GPU cluster** for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

         To use a GPU cluster, select an existing one or create a new cluster:

         1. Click  **Create** in the **GPU cluster** field.
         2. In the window that opens, specify the cluster name and InfiniBand fabric. To select the fabric, see [InfiniBand fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).
         3. Click **Create**.

      3. Select the **Project** for the VM location.

      4. Specify the **VM name**.

   To check GPU availability across regions and presets before you create a VM, use the [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md).

5. On the **Storage** step, configure disks and filesystems:

   1. In the **Boot disk** section, set the boot disk settings:

      1. Click  on the boot disk card.
      2. In the window that opens, select an existing disk or create a new one.
      3. If you create a new boot disk, choose an operating system image: either a [public image](https://docs.nebius.com/compute/storage/boot-disk-images.md) provided by Nebius or a [custom image or image family](https://docs.nebius.com/compute/storage/custom-disk-images.md) that you created yourself. Also, configure the type, encryption, size and block size. For more information about these settings, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

   2. (Optional) If you want to attach an additional disk to your VM, in the **Additional disks** section:

      1. Click  **Attach disk**.
      2. In the window that opens, select an existing secondary disk or create a new one.
      3. If you create a new disk, specify its name and configure the type, encryption, size and block size.
      4. Click **Attach disk**.

      > [!WARNING]
      >
      > After you create the VM, [mount the additional disks](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these disks.

   3. (Optional) If the selected platform supports local SSD disks, enable **Local SSD disks** to add ephemeral local storage.

      > [!NOTE]
      >
      > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

   4. (Optional) If you want to attach a filesystem to your VM, in the **Shared filesystems** section:

      1. Click  **Attach shared filesystem**.

      2. In the window that opens, select an existing filesystem or create a new one.

      3. If you create a new filesystem, specify its name, size and the block size.

      4. Click **Attach filesystem**.

      5. After the window is closed, specify a mount tag for mounting the filesystem to the VM.

         Create your own tag, such as `my-filesystem`. Make sure that it is unique within the VM.

      6. To mount the filesystem to the VM automatically, keep the **Auto mount** option enabled.

6. On the **Network** step, attach the VM to a [network and subnet](https://docs.nebius.com/vpc/overview.md):

   1. Select the **Network** and **Subnet**.

   2. In the **Primary private IP address** field, select whether to automatically assign a private IP address or select an already allocated one.

      For more information, see [Private IP addresses](https://docs.nebius.com/compute/virtual-machines/network.md#private-ip-addresses).

   3. (Optional) In the **Secondary private IP address** field, assign secondary addresses. Use them as a backup option in case of incidents. For example, a backup node can take a secondary address of the main node when the main one fails. As a result, routing to this address can be preserved.

      After you click  **Add IP address**, you can specify a new address or select an already created allocation.

      You can assign no more than five secondary addresses.

   4. In the **Public IP address** field, specify whether the VM should have a public address and whether this address should be dynamic, static or taken from an allocation.

      If you need to secure your VM and make it isolated, you can create a VM without a public IP address. If you need to connect to this VM from the internet, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md). It has an IP address in the internet and an IP address in the VM's network. As a result, you can access the VM via the jump server from the internet. This approach enhances security and still provides access to the VM.

      For more information, see [How to enable a public IP address for a VM](https://docs.nebius.com/compute/virtual-machines/network.md#how-to-enable-a-public-ip-address-for-a-vm).

   5. In the **Hostname** field, specify whether to use the VM ID or a custom hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md):

      * **Same as VM ID**: The default FQDN uses the VM ID.
      * **Custom**: Specify your own hostname.

7. On the **Configuration** step, configure access, identity and VM startup settings:

   1. In the **Access** section, add credentials so you can [connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md):

      1. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).
      2. In the **Username and SSH key** field, click  **Create**.
      3. In the window that opens, specify the username of the VM user, a public key of your SSH key pair and the credentials name to recognize the key in the list.

         Do not use the `root` or `admin` usernames. They are reserved for internal needs and are not allowed to connect to a VM by SSH.
      4. Click **Add credentials**.

   2. (Optional) In the **Additional** section, select an existing service account or click  **Create** to add a new one. The service account will perform actions on behalf of the VM, for example, run scripts.

   3. (Optional) In the **User data** section, select **Enable custom cloud-init config** and set a configuration in the [cloud-init](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#users-and-groups) format.

      This configuration affects the settings for shared filesystems and access that you set up earlier:

      * If you add a cloud-init configuration, you cannot manage the **Auto mount** option for filesystems. Their mounting settings automatically appear in the configuration.
      * The username and SSH key that you specify on the **Configuration** step are automatically added to a cloud-init configuration if you enable it. Ultimately, the settings from the configuration apply, not those from the **Configuration** step.

      The default configuration that only adds the user contains the following parameters:

      * `name`: Username for connecting to the VM. The above example sets the value of your machine's `USER` environment variable as the username for the VM.
      * `sudo`: Sudo policy. `ALL=(ALL) NOPASSWD:ALL` allows users unrestricted sudo access; `False` disables sudo access for users.
      * `shell`: Default shell.
      * `ssh_authorized_keys`: User's authorized keys. Allows configuring SSH access to the VM.

      You can specify several users and their public SSH keys.

      For more information, see [cloud-init configuration examples](https://cloudinit.readthedocs.io/en/latest/reference/examples.html).

8. On the **Review** step, check the full VM configuration. To change a section quickly, click  next to the corresponding block. The wizard opens the relevant step with your current settings.

9. Click **Create VM**.

**CLI**

1. (Optional) If you want to attach a filesystem to your VM, create this filesystem:

   ```bash theme={null}
   nebius compute filesystem create \
     --name <filesystem_name> \
     --size-gibibytes 10 \
     --type network_ssd \
     --block-size-bytes 4096
   ```

   Save the filesystem ID from the output `metadata.id` parameter.

   For more information about filesystem creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

   You don't need to create disks for the VM in advance. You can create them along with the VM. Such disks are called [VM-managed](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). They are tied to the VM lifecycle.

2. (Optional) To provide the VM with an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) that reserves a static public IP address, create this allocation. As a result, the address is preserved even if you delete the VM.

   1. [Get the required subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
   2. Run the following command:

      ```bash theme={null}
      nebius vpc allocation create \
        --ipv4-public-subnet-id <subnet_ID> \
        --name <allocation_name>
      ```

      Save the allocation ID from the output `metadata.id` parameter.

   For more information about networking in Compute, see [Public IP addresses](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses).

3. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a GPU cluster for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

   To create a GPU cluster, run the following command:

   ```bash theme={null}
   nebius compute gpu-cluster create \
     --name <GPU_cluster_name> \
     --infiniband-fabric <fabric>
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

   Save the cluster ID from the output `metadata.id` parameter.

4. (Optional) Create a [service account](https://docs.nebius.com/iam/service-accounts/manage.md) that will perform actions on behalf of the VM:

   ```bash theme={null}
   nebius iam service-account create --name <service_account_name>
   ```

5. Create the VM:

   ```bash theme={null}
   nebius compute instance create \
     --name <VM_name> \
     --stopped=<true|false> \
     --resources-platform <platform> \
     --resources-preset <preset> \
     --boot-disk-managed-disk-name <boot_disk_name> \
     --boot-disk-managed-disk-type <disk_type> \
     --boot-disk-managed-disk-size-gibibytes <size> \
     --boot-disk-managed-disk-source-image-family-image-family <image_family> \
     --boot-disk-attach-mode READ_WRITE \
     --boot-disk-device-id <user_defined_ID> \
     --secondary-disks '[{"attach_mode": "READ_WRITE", "device_id": "<user-defined_ID>", "managed_disk": { "name": "<disk_name>", "spec": { "type": "<disk_type>", "size_gibibytes": 10 }}}]' \
     --filesystems '[{"existing_filesystem": {"id": "<filesystem_ID>"}, "attach_mode": "READ_WRITE", "mount_tag": "<filesystem_tag>"}]' \
     --cloud-init-user-data "$USER_DATA" \
     --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {"allocation_id": "<allocation_ID>"}, "subnet_id": "<subnet_ID>"}]' \
     --gpu-cluster-id <GPU_cluster_ID> \
     --hostname <FQDN_hostname> \
     --reservation-policy-policy <auto|forbid|strict> \
     --reservation-policy-reservation-ids <reservations> \
     --recovery-policy <recover|fail> \
     --preemptible-on-preemption stop \
     --follows-spot-price \
     --service-account-id <service_account_ID>
   ```

   The command contains the following parameters:

   * `--name`: VM's name.

   * `--stopped` (optional): To create a VM but not launch it, specify `true`. The VM will remain in the `Stopped` status. If you omit the parameter or specify `false`, the VM starts after creation.

     For more information, see [Lifecycle of a Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/lifecycle.md).

   * `--resources-platform`: [VM platform](https://docs.nebius.com/compute/virtual-machines/types.md).

   * `--resources-preset`: VM preset. Depends on the chosen platform.

   * `--boot-disk-managed-disk-name`: Name of the [VM-managed boot disk](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks) that you create along with the VM.

   * `--boot-disk-managed-disk-type`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).

   * `--boot-disk-managed-disk-size-gibibytes`: Disk size in gibibytes. Maximum boot disk size is 30,720 GiB (30 TiB).

   * `--boot-disk-managed-disk-source-image-family-image-family`: Public image that Nebius AI Cloud supports. For the list of available public images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).

   * `--boot-disk-attach-mode`: Write permission of the boot disk. The only supported value is `READ_WRITE`.

   * `--boot-disk-device-id` (optional): User-defined ID for mounting the boot disk to the VM. The default value is `disk-n` where `n` is an integer index. A `virtio-` prefix is added to the specified (or default) device ID.

   * `--secondary-disks` (optional): Settings of additional VM-managed disks that you create along with the VM. You can attach one or several disks.

     * `attach_mode`: Write permission of the additional disk. The only supported value is `READ_WRITE`.
     * `device_id`: User-defined ID for mounting the disk to the VM.
     * `managed_disk.name`: Name of a new disk.
     * `managed_disk.spec.type`: Disk type.
     * `managed_disk.spec.size_gibibytes`: Disk size in gibibytes.

   * `--filesystems` (optional): Filesystem settings. You can attach several filesystems, if required.

     * `id`: ID of the filesystem created earlier.
     * `attach_mode`: Write permission of the filesystem. The only supported value is `READ_WRITE`.
     * `mount_tag`: Tag for mounting the filesystem to the VM.

       Create your own tag, such as `my-filesystem`. Make sure that it is unique within the VM.

       If you do not specify the tag, it takes the `filesystem-N` default value where `N` is an integer. For example, `filesystem-0`.

     > [!WARNING]
     >
     > After you create the VM, [mount the additional disks and filesystems](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these volumes.

   * `--cloud-init-user-data` (optional): Configuration of VM users in the [cloud-init](https://cloud-init.io/) format.

   * `--network-interfaces`: Network settings.

     * To assign a dynamic public IP address, specify `"public_ip_address": {}`.

       A dynamic public IP address is randomly allocated from the [IPv4 public range](#get-public-ip-range) of Nebius AI Cloud and is not persistent. If a VM with a dynamic address has the `Stopped` status for more than one hour, the address is automatically returned to the IPv4 public range. After that, Compute may allocate this address to a different VM.

     * To assign a static public IP address, specify `"public_ip_address": {"static": true}`.

       A static public IP address is also randomly allocated from the IPv4 public range of Nebius AI Cloud. If you stop a VM that has a static IP address, the address will not return to the range. However, if you delete this VM, the address will return.

     * To assign the allocation created earlier, specify `"public_ip_address": {"allocation_id": "<allocation_ID>"}`.

       An allocation allows you to use a reserved static public address for the VM. This address will not return to the IPv4 range even if you delete the VM.

     * To create a VM without a public IP address, remove the `public_ip_address` parameter from the JSON. The VM will only have a private address.

       If you need to secure your VM and make it isolated, you can create a VM without a public IP address. If you need to connect to this VM from the internet, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md). It has an IP address in the internet and an IP address in the VM's network. As a result, you can access the VM via the jump server from the internet. This approach enhances security and still provides access to the VM.

   * `--gpu-cluster-id` (optional): ID of the GPU cluster created earlier.

   * `--local-disks-passthrough-group-requested` (optional): Requests local SSD disks to be added to the VM when set to `true`.

     > [!NOTE]
     >
     > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

   * `--hostname` (optional): Hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md). By default, the FQDN has the `<VM_ID>.<VM_network_ID>.compute.internal.` format. If you want to customize it, use a hostname instead of the VM's ID in the FQDN. For example, if you specify `--hostname my-host`, the FQDN is `my-host.vpcnetwork-e00***.compute.internal.`.

   * `--reservation-policy-policy` (optional): Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/compute/virtual-machines/reservations.md) and run your VM based on them. As a result, the VM resources are reserved and always available.

   * `--reservation-policy-reservation-ids` (optional): IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

     For information about how to configure `--reservation-policy-policy` and `--reservation-policy-reservation-ids`, see [How to add reservations to VMs](https://docs.nebius.com/compute/virtual-machines/reservations.md#how-to-add-reservations-to-vms).

   * `--recovery-policy` (optional): Defines what Compute does with the VM after it is preempted or fails.

     [Preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) only support the `fail` value that stops the VM. They do not support the `recover` value that tries to restart the VM. If you set `recover` for a preemptible VM, it will cause an error.

   * `--preemptible-on-preemption` (optional; for preemptible VMs only): Specifies what happens when the VM is preempted. The only supported value is `stop`: Compute stops the VM without deleting or restarting it.

   * `--spot-pricing-policy-id` (optional; for preemptible VMs): ID of the pricing policy that sets the maximum spot price. For information on how to get a pricing policy ID or create a new policy, see [Managing pricing policies](https://docs.nebius.com/signup-billing/manage-pricing-policy.md). Do not use this parameter together with `--follows-spot-price`.

   * `--follows-spot-price` (optional; for preemptible VMs): Accepts the current spot price without setting a maximum spot price. Do not use this parameter together with `--spot-pricing-policy-id`.

   * `--service-account-id` (optional): Service account associated with the VM.

**Terraform**

1. (Optional) If you want to attach a filesystem to your VM, create this filesystem:

   ```hcl theme={null}
   resource "nebius_compute_v1_filesystem" "my_filesystem" {
     name             = "<filesystem_name>"
     parent_id        = "<project_ID>"
     size_gibibytes   = 10
     type             = "NETWORK_SSD"
     block_size_bytes = 4096
   }
   ```

   For more information, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

   You don't need to create disks for the VM in advance. You can create them along with the VM. Such disks are called [VM-managed](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). They are tied to the VM lifecycle.

2. (Optional) To provide the VM with an [allocation](https://docs.nebius.com/vpc/overview.md#allocation) that reserves a static public IP address, create this allocation. As a result, the address is preserved even if you delete the VM.

   ```hcl theme={null}
   resource "nebius_vpc_v1_allocation" "my_allocation" {
     name      = "<allocation_name>"
     parent_id = "<project_ID>"
     ipv4_public = {
       subnet_id = "<subnet_ID>"
     }
   }
   ```

   To create the allocation, [get the required subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).

   For more information about networking in Compute, see [Public IP addresses](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses).

3. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a GPU cluster for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

   To create a GPU cluster, use the following configuration:

   ```hcl theme={null}
   resource "nebius_compute_v1_gpu_cluster" "my_gpu_cluster" {
     name              = "<GPU_cluster_name>"
     parent_id         = "<project_ID>"
     infiniband_fabric = "<fabric>"
   }
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

4. (Optional) Create a [service account](https://docs.nebius.com/iam/service-accounts/manage.md) that will perform actions on behalf of the VM:

   ```hcl theme={null}
   resource "nebius_iam_v1_service_account" "my_sa" {
     name = "<service_account_name>"
     parent_id = "<project_ID>"
   }
   ```

5. (Optional) If your `resources` block uses a platform and preset that support local SSD disks, add a `local_disks` block to the `nebius_compute_v1_instance` resource in the next step. The local SSD disks are provisioned as raw Non-Volatile Memory Express (NVMe) devices (`nvme0`, `nvme1`, and so on). You can enable local SSD disks only when you create the VM. For more information, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

   For example:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     # ...
     local_disks = {
       passthrough_group = {
         requested = true
       }
     }
   }
   ```

6. Create the VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name      = "<VM_name>"
     parent_id = "<project_ID>"
     stopped   = <true|false>
     resources = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       managed_disk = {
         name = "<boot_disk_name>"
         spec = {
           type                = "<disk_type>"
           size_gibibytes      = <size>
           source_image_family = {
             image_family = "<image_family>"
           }
         }
       }
       attach_mode = "READ_WRITE"
       device_id = "<user_defined_ID>"
     }
     secondary_disks = [
       {
         managed_disk = {
           name = "<additional_disk_name>"
           spec = {
             type                = "<disk_type>"
             size_gibibytes      = <size>
           }
         }
         attach_mode = "READ_WRITE"
         device_id = "<user_defined_ID>"
       }
     ]
     filesystems = [
       {
         existing_filesystem = {
           id = nebius_compute_v1_filesystem.my_filesystem.id
         }
         attach_mode = "READ_WRITE"
         mount_tag   = "<filesystem_tag>"
       }
     ]
     cloud_init_user_data = var.user_data
     network_interfaces = [
       {
         name       = "eth0"
         ip_address = {}
         public_ip_address = {
           allocation_id = nebius_vpc_v1_allocation.my_allocation.id
         }
         subnet_id = "<subnet_ID>"
       }
     ]
     gpu_cluster = {
       id = nebius_compute_v1_gpu_cluster.my_gpu_cluster.id
     }
     hostname           = "<FQDN_prefix>"
     reservation_policy = {
       policy = "<AUTO|FORBID|STRICT>"
       reservation_ids = "<reservations>"
     }
     recovery_policy    = "<RECOVER|FAIL>"
     preemptible = {
       on_preemption = "STOP"
     }
     follows_spot_price = {}
     service_account_id = nebius_iam_v1_service_account.my_sa.id
   }
   ```

   The configuration contains the following parameters:

   * `name`: VM's name.

   * `stopped` (optional): To create a VM but not launch it, specify `true`. The VM will remain in the `Stopped` status. If you omit the parameter or specify `false`, the VM starts after creation.

     For more information, see [Lifecycle of a Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/lifecycle.md).

   * `resources.platform`: [VM platform](https://docs.nebius.com/compute/virtual-machines/types.md).

   * `resources.preset`: VM preset. Depends on the chosen platform.

   * `boot_disk`: Settings of a [VM-managed boot disk](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks) that you create along with the VM.

     * `managed_disk.name`: Name of the disk.
     * `managed_disk.spec.type`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
     * `managed_disk.spec.size_gibibytes`: Disk size in gibibytes. Maximum boot disk size is 30,720 GiB (30 TiB).
     * `managed_disk.spec.source_image_family.image_family`: Public image that Nebius AI Cloud supports. For the list of available public images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).
     * `attach_mode`: Write permission of the boot disk. The only supported value is `READ_WRITE`.
     * `device_id` (optional): User-defined ID for mounting the disk to the VM. The default value is `disk-n`, where `n` is an integer index. A `virtio-` prefix is added to the specified (or default) device ID.

   * `secondary_disks` (optional): Settings of additional VM-managed disks that you create along with the VM. You can attach one or several disks.

     * `managed_disk.name`: Name of a new disk.
     * `managed_disk.spec.type`: Disk type.
     * `managed_disk.spec.size_gibibytes`: Disk size in gibibytes.
     * `attach_mode`: Write permission of the additional disk. The only supported value is `READ_WRITE`.
     * `device_id`: User-defined ID for mounting the disk to the VM.

   * `filesystems` (optional): Filesystem settings. You can attach several filesystems, if required.

     * `existing_filesystem.id`: ID of the filesystem created earlier.
     * `attach_mode`: Write permission of the filesystem. The only supported value is `READ_WRITE`.
     * `mount_tag`: Tag for mounting the filesystem to the VM.

       Create your own tag, such as `my-filesystem`. Make sure that it is unique within the VM.

       If you do not specify the tag, it takes the `filesystem-N` default value where `N` is an integer. For example, `filesystem-0`.

     > [!WARNING]
     >
     > After you create the VM, [mount the additional disks and filesystems](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these volumes.

   * `cloud_init_user_data` (optional): Configuration of VM users in the [cloud-init](https://cloud-init.io/) format.

   * `network_interfaces`: Network settings.

     * To assign a dynamic public IP address, specify `public_ip_address = {}`.

       A dynamic public IP address is randomly allocated from the [IPv4 public range](#get-public-ip-range) of Nebius AI Cloud and is not persistent. If a VM with a dynamic address has the `Stopped` status for more than one hour, the address is automatically returned to the IPv4 public range. After that, Compute may allocate this address to a different VM.

     * To assign a static public IP address, specify `public_ip_address = {static = true}`.

       A static public IP address is also randomly allocated from the IPv4 public range of Nebius AI Cloud. If you stop a VM that has a static IP address, the address will not return to the range. However, if you delete this VM, the address will return.

     * To assign the allocation created earlier, specify `public_ip_address = {allocation_id = nebius_vpc_v1_allocation.my_allocation.id}`.

       An allocation allows you to use a reserved static public address for the VM. This address will not return to the IPv4 range even if you delete the VM.

     * To create a VM without a public IP address, remove the `public_ip_address` parameter from the configuration. The VM will only have a private address.

       If you need to secure your VM and make it isolated, you can create a VM without a public IP address. If you need to connect to this VM from the internet, you can [set up a WireGuard jump server](https://docs.nebius.com/compute/virtual-machines/wireguard.md). It has an IP address in the internet and an IP address in the VM's network. As a result, you can access the VM via the jump server from the internet. This approach enhances security and still provides access to the VM.

   * `gpu_cluster.id` (optional): ID of the GPU cluster created earlier.

   * `local_disks` (optional): Set `passthrough_group.requested = true` to request local SSD disks to be added to the VM.

     > [!NOTE]
     >
     > Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

   * `hostname` (optional): Hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md). By default, the FQDN has the `<VM_ID>.<VM_network_ID>.compute.internal.` format. If you want to customize it, use a hostname instead of the VM's ID in the FQDN. For example, if you specify `hostname = "my-host"`, the FQDN is `my-host.vpcnetwork-e00***.compute.internal.`.

   * `reservation_policy.policy` (optional): Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/compute/virtual-machines/reservations.md) and run your VM based on them. As a result, VM resources are reserved and always available.

   * `reservation_policy.reservation_ids` (optional): IDs of specific reservations. These are capacity block groups that a Nebius manager has created.

     For information about how to configure `reservation_policy.policy` and `reservation_policy.reservation_ids`, see [How to add reservations to VMs](https://docs.nebius.com/compute/virtual-machines/reservations.md#how-to-add-reservations-to-vms).

   * `recovery_policy` (optional): Defines what Compute does with the VM after it is preempted or fails.

     [Preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md) only support the `FAIL` value that stops the VM. They do not support the `RECOVER` value that tries to restart the VM. If you set `RECOVER` for a preemptible VM, it will cause an error.

   * `preemptible.on_preemption` (optional; for preemptible VMs only): Specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.

   * `spot_pricing_policy.id` (optional; for preemptible VMs): ID of the pricing policy that sets the maximum spot price. Do not use this block together with `follows_spot_price`.

   * `follows_spot_price` (optional; for preemptible VMs): Accepts the current spot price without setting a maximum spot price. Do not use this block together with `spot_pricing_policy`.

   * `service_account_id` (optional): Service account associated with the VM.

7. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

8. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. (Optional) If you want to attach a filesystem to your VM, create this filesystem:

   ```go theme={null}
   filesystemOperation, err := sdk.Services().Compute().V1().
       Filesystem().Create(
           ctx,
           &compute.CreateFilesystemRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<filesystem_name>",
               },
               Spec: &compute.FilesystemSpec{
                   Size: &compute.FilesystemSpec_SizeGibibytes{
                       SizeGibibytes: 10,
                   },
                   BlockSizeBytes: 4096,
                   Type:           compute.FilesystemSpec_NETWORK_SSD,
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = filesystemOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   For more information about filesystem creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

   You don't need to create disks for the VM in advance. You can create them along with the VM. Such disks are called [VM-managed](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). They are tied to the VM lifecycle.

2. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a GPU cluster for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

   Create a GPU cluster:

   ```go theme={null}
   gpuClusterOperation, err := sdk.Services().Compute().V1().
       GpuCluster().Create(
           ctx,
           &compute.CreateGpuClusterRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<GPU_cluster_name>",
               },
               Spec: &compute.GpuClusterSpec{
                   InfinibandFabric: "<fabric>",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = gpuClusterOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

3. (Optional) Create a [service account](https://docs.nebius.com/iam/service-accounts/manage.md) that will perform actions on behalf of the VM:

   ```go theme={null}
   serviceAccountOperation, err := sdk.Services().IAM().V1().
       ServiceAccount().Create(
           ctx,
           &iam.CreateServiceAccountRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<service_account_name>",
               },
               Spec: &iam.ServiceAccountSpec{},
           },
       )
   if err != nil {
       return err
   }
   if _, err = serviceAccountOperation.Wait(ctx); err != nil {
       return err
   }
   serviceAccountID := serviceAccountOperation.ResourceID()
   ```

4. Create the VM:

   ```go theme={null}
   managedBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       DeviceId:   "<user_defined_ID>",
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "<boot_disk_name>",
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: <size>,
                   },
                   Type: compute.DiskSpec_NETWORK_SSD,
                   Source: &compute.DiskSpec_SourceImageFamily{
                       SourceImageFamily: &compute.SourceImageFamily{
                           ImageFamily: "<image_family>",
                       },
                   },
               },
           },
       },
   }
   managedSecondaryDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       DeviceId:   "device-2",
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "managed-secondary-disk",
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 10,
                   },
                   Type: compute.DiskSpec_NETWORK_SSD,
               },
           },
       },
   }
   managedFilesystem := &compute.AttachedFilesystemSpec{
       AttachMode: compute.AttachedFilesystemSpec_READ_WRITE,
       MountTag:   "<filesystem_tag>",
       Type: &compute.AttachedFilesystemSpec_ExistingFilesystem{
           ExistingFilesystem: &compute.ExistingFilesystem{
               Id: filesystemID,
           },
       },
   }
   managedNetwork := &compute.NetworkInterfaceSpec{
       Name:            "eth0",
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   managedVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<VM_name>",
               },
               Spec: &compute.InstanceSpec{
                   ServiceAccountId: serviceAccountID,
                   Stopped:          <true|false>,
                   Resources: &compute.ResourcesSpec{
                       Platform: "<platform>",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "<preset>",
                       },
                   },
                   GpuCluster: &compute.InstanceGpuClusterSpec{
                       Id: gpuClusterID,
                   },
                   BootDisk: managedBootDisk,
                   SecondaryDisks: []*compute.AttachedDiskSpec{
                       managedSecondaryDisk,
                   },
                   Filesystems: []*compute.AttachedFilesystemSpec{
                       managedFilesystem,
                   },
                   CloudInitUserData: userData,
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       managedNetwork,
                   },
                   Hostname: "<FQDN_hostname>",
                   ReservationPolicy: &compute.ReservationPolicy{
                       Policy: compute.ReservationPolicy_FORBID,
                   },
                   RecoveryPolicy: compute.InstanceRecoveryPolicy_FAIL,
                   Preemptible: &compute.PreemptibleSpec{
                       OnPreemption: compute.PreemptibleSpec_STOP,
                   },
                   PricingModel: &compute.InstanceSpec_FollowsSpotPrice{
                       FollowsSpotPrice: &compute.FollowsSpotPriceSpec{},
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = managedVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   The code contains the following parameters:

   * `Metadata.Name`: VM's name.
   * `Spec.ServiceAccountId` (optional): Service account associated with the VM.
   * `Spec.Stopped` (optional): If you want to create a VM but not launch it, specify the `true` value. The VM will remain in the `Stopped` status.
   * `Spec.Resources.Platform`: [VM platform](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `Spec.Resources.Size.Preset`: VM preset. Depends on the chosen platform.
   * `Spec.GpuCluster.Id` (optional): ID of the GPU cluster created earlier.
   * `managedBootDisk.AttachMode`: Write permission of the boot disk. The only supported value is `READ_WRITE`.
   * `managedBootDisk.DeviceId` (optional): User-defined ID for mounting the boot disk to the VM. The default value is `disk-n` where `n` is an integer index. A `virtio-` prefix is added to the specified (or default) device ID.
   * `managedBootDisk.ManagedDisk.Name`: Name of the [VM-managed boot disk](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks) that you create along with the VM.
   * `managedBootDisk.ManagedDisk.Spec.SizeGibibytes`: Disk size in gibibytes. Maximum boot disk size is 30,720 GiB (30 TiB).
   * `managedBootDisk.ManagedDisk.Spec.Type`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
   * `managedBootDisk.ManagedDisk.Spec.SourceImageFamily.ImageFamily`: Public image that Nebius AI Cloud supports. For the list of available public images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).
   * `managedSecondaryDisk.AttachMode`: Write permission of the additional disk. The only supported value is `READ_WRITE`.
   * `managedSecondaryDisk.DeviceId`: User-defined ID for mounting the additional disk to the VM.
   * `managedSecondaryDisk.ManagedDisk.Name`: Name of a new additional VM-managed disk.
   * `managedSecondaryDisk.ManagedDisk.Spec.SizeGibibytes`: Size of the additional disk in gibibytes.
   * `managedSecondaryDisk.ManagedDisk.Spec.Type`: Disk type of the additional disk.
   * `managedFilesystem.AttachMode`: Write permission of the filesystem. The only supported value is `READ_WRITE`.
   * `managedFilesystem.MountTag`: Tag for mounting the filesystem to the VM.
   * `managedFilesystem.ExistingFilesystem.Id`: ID of the filesystem created earlier.
   * `Spec.CloudInitUserData` (optional): Configuration of VM users in the [cloud-init](https://cloud-init.io/) format.
   * `managedNetwork.SubnetId`: ID of the subnet to attach the VM to.
   * `managedNetwork.IpAddress`: Private IP address settings.
   * `managedNetwork.PublicIpAddress`: Public IP address settings. In the example, an empty `PublicIPAddress` assigns a dynamic public IP address.
   * `Spec.Hostname` (optional): Hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md). By default, the FQDN has the `<VM_ID>.<VM_network_ID>.compute.internal.` format.
   * `Spec.ReservationPolicy.Policy` (optional): Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/compute/virtual-machines/reservations.md) and run your VM based on them.
   * `Spec.RecoveryPolicy` (optional): Defines what Compute does with the VM after it is preempted or fails.
   * `Spec.Preemptible.OnPreemption` (optional; for preemptible VMs only): Specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.
   * `Spec.PricingModel` (optional; for preemptible VMs): `FollowsSpotPrice` accepts the current spot price without setting a maximum spot price. To set a maximum spot price, use `SpotPricingPolicy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

**Python SDK**

1. (Optional) If you want to attach a filesystem to your VM, create this filesystem:

   ```python theme={null}
   filesystem_service = FilesystemServiceClient(sdk)
   filesystem_operation = await filesystem_service.create(
       CreateFilesystemRequest(
           metadata=ResourceMetadata(name="<filesystem_name>"),
           spec=FilesystemSpec(
               block_size_bytes=4096,
               type=FilesystemSpec.FilesystemType.NETWORK_SSD,
               size_gibibytes=10,
           ),
       ),
   )
   await filesystem_operation.wait()
   ```

   For more information about filesystem creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

   You don't need to create disks for the VM in advance. You can create them along with the VM. Such disks are called [VM-managed](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). They are tied to the VM lifecycle.

2. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a GPU cluster for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

   Create a GPU cluster:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   gpu_cluster_operation = await gpu_cluster_service.create(
       CreateGpuClusterRequest(
           metadata=ResourceMetadata(
               name="<GPU_cluster_name>",
           ),
           spec=GpuClusterSpec(
               infiniband_fabric="<fabric>",
           ),
       ),
   )
   await gpu_cluster_operation.wait()
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

3. (Optional) Create a [service account](https://docs.nebius.com/iam/service-accounts/manage.md) that will perform actions on behalf of the VM:

   ```python theme={null}
   service_account_service = ServiceAccountServiceClient(sdk)
   service_account_operation = await service_account_service.create(
       CreateServiceAccountRequest(
           metadata=ResourceMetadata(
               name="<service_account_name>",
           ),
           spec=ServiceAccountSpec(),
       ),
   )
   await service_account_operation.wait()
   service_account_id = service_account_operation.resource_id
   ```

4. Create the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   managed_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<VM_name>"),
           spec=InstanceSpec(
               service_account_id=service_account_id,
               stopped=<True|False>,
               resources=ResourcesSpec(
                   platform="<platform>",
                   preset="<preset>",
               ),
               gpu_cluster=InstanceGpuClusterSpec(
                   id=gpu_cluster_id,
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   managed_disk=ManagedDisk(
                       name="<boot_disk_name>",
                       spec=DiskSpec(
                           type=DiskSpec.DiskType.NETWORK_SSD,
                           source_image_family=(
                               SourceImageFamily(
                                   image_family="<image_family>",
                               )
                           ),
                           size_gibibytes=<size>,
                       ),
                   ),
                   device_id="<user_defined_ID>",
               ),
               secondary_disks=[
                   AttachedDiskSpec(
                       attach_mode=(
                           AttachedDiskSpec.AttachMode.READ_WRITE
                       ),
                       managed_disk=ManagedDisk(
                           name="managed-secondary-disk",
                           spec=DiskSpec(
                               type=(
                                   DiskSpec.DiskType.NETWORK_SSD
                               ),
                               size_gibibytes=10,
                           ),
                       ),
                       device_id="device-2",
                   ),
               ],
               filesystems=[
                   AttachedFilesystemSpec(
                       attach_mode=(
                           AttachedFilesystemSpec.AttachMode.READ_WRITE
                       ),
                       existing_filesystem=ExistingFilesystem(
                           id=filesystem_id,
                       ),
                       mount_tag="<filesystem_tag>",
                   ),
               ],
               cloud_init_user_data=user_data,
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
               hostname="<FQDN_hostname>",
               reservation_policy=ReservationPolicy(
                   policy=ReservationPolicy.Policy.FORBID,
               ),
               recovery_policy=InstanceRecoveryPolicy.FAIL,
               preemptible=PreemptibleSpec(
                   on_preemption=(
                       PreemptibleSpec.PreemptionPolicy.STOP
                   ),
               ),
               follows_spot_price=FollowsSpotPriceSpec(),
           ),
       ),
   )
   await managed_vm_operation.wait()
   ```

   The code contains the following parameters:

   * `metadata.name`: VM's name.
   * `spec.service_account_id` (optional): Service account associated with the VM.
   * `spec.stopped` (optional): If you want to create a VM but not launch it, specify the `True` value. The VM will remain in the `Stopped` status.
   * `spec.resources.platform`: [VM platform](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.resources.preset`: VM preset. Depends on the chosen platform.
   * `spec.gpu_cluster.id` (optional): ID of the GPU cluster created earlier.
   * `spec.boot_disk.attach_mode`: Write permission of the boot disk. The only supported value is `READ_WRITE`.
   * `spec.boot_disk.managed_disk.name`: Name of the [VM-managed boot disk](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks) that you create along with the VM.
   * `spec.boot_disk.managed_disk.spec.type`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
   * `spec.boot_disk.managed_disk.spec.source_image_family.image_family`: Public image that Nebius AI Cloud supports. For the list of available public images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).
   * `spec.boot_disk.managed_disk.spec.size_gibibytes`: Disk size in gibibytes. Maximum boot disk size is 30,720 GiB (30 TiB).
   * `spec.boot_disk.device_id` (optional): User-defined ID for mounting the boot disk to the VM. The default value is `disk-n` where `n` is an integer index. A `virtio-` prefix is added to the specified (or default) device ID.
   * `spec.secondary_disks[].attach_mode`: Write permission of the additional disk. The only supported value is `READ_WRITE`.
   * `spec.secondary_disks[].managed_disk.name`: Name of a new additional VM-managed disk.
   * `spec.secondary_disks[].managed_disk.spec.type`: Disk type of the additional disk.
   * `spec.secondary_disks[].managed_disk.spec.size_gibibytes`: Size of the additional disk in gibibytes.
   * `spec.secondary_disks[].device_id`: User-defined ID for mounting the additional disk to the VM.
   * `spec.filesystems[].attach_mode`: Write permission of the filesystem. The only supported value is `READ_WRITE`.
   * `spec.filesystems[].existing_filesystem.id`: ID of the filesystem created earlier.
   * `spec.filesystems[].mount_tag`: Tag for mounting the filesystem to the VM.
   * `spec.cloud_init_user_data` (optional): Configuration of VM users in the [cloud-init](https://cloud-init.io/) format.
   * `spec.network_interfaces[].subnet_id`: ID of the subnet to attach the VM to.
   * `spec.network_interfaces[].ip_address`: Private IP address settings.
   * `spec.network_interfaces[].public_ip_address`: Public IP address settings. In the example, an empty `PublicIPAddress` assigns a dynamic public IP address.
   * `spec.hostname` (optional): Hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md). By default, the FQDN has the `<VM_ID>.<VM_network_ID>.compute.internal.` format.
   * `spec.reservation_policy.policy` (optional): Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/compute/virtual-machines/reservations.md) and run your VM based on them.
   * `spec.recovery_policy` (optional): Defines what Compute does with the VM after it is preempted or fails.
   * `spec.preemptible.on_preemption` (optional; for preemptible VMs only): Specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.
   * `spec.follows_spot_price` (optional; for preemptible VMs): Accepts the current spot price without setting a maximum spot price. To set a maximum spot price, use `spec.spot_pricing_policy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

**JavaScript SDK**

1. (Optional) If you want to attach a filesystem to your VM, create this filesystem:

   ```ts theme={null}
   const filesystemCreateService = new FilesystemService(sdk);
   const filesystemOperation =
     await filesystemCreateService.create(
       CreateFilesystemRequest.create({
         metadata: ResourceMetadata.create({
           name: "<filesystem_name>",
         }),
         spec: FilesystemSpec.create({
           blockSizeBytes: 4096,
           type: FilesystemSpec_FilesystemType.NETWORK_SSD,
           size: {
             $case: "sizeGibibytes",
             sizeGibibytes: 10,
           },
         }),
       }),
     ).result;
   await filesystemOperation.wait();
   ```

   For more information about filesystem creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

   You don't need to create disks for the VM in advance. You can create them along with the VM. Such disks are called [VM-managed](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks). They are tied to the VM lifecycle.

2. (Optional) If you create a VM with 8 GPUs (for example, for training models), use a GPU cluster for the VM. InfiniBand™ in the cluster allows you to accelerate tasks that require high-performance computing (HPC) power. A single VM without InfiniBand™ cannot perform these tasks as quickly.

   Create a GPU cluster:

   ```ts theme={null}
   const gpuClusterCreateService = new GpuClusterService(sdk);
   const gpuClusterOperation =
     await gpuClusterCreateService.create(
       CreateGpuClusterRequest.create({
         metadata: ResourceMetadata.create({
           name: "<GPU_cluster_name>",
         }),
         spec: GpuClusterSpec.create({
           infinibandFabric: "<fabric>",
         }),
       }),
     ).result;
   await gpuClusterOperation.wait();
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

3. (Optional) Create a [service account](https://docs.nebius.com/iam/service-accounts/manage.md) that will perform actions on behalf of the VM:

   ```ts theme={null}
   const serviceAccountCreateService =
     new ServiceAccountService(sdk);
   const serviceAccountOperation =
     await serviceAccountCreateService.create(
       CreateServiceAccountRequest.create({
         metadata: ResourceMetadata.create({
           name: "<service_account_name>",
         }),
         spec: ServiceAccountSpec.create({}),
       }),
     ).result;
   await serviceAccountOperation.wait();
   const serviceAccountId =
     serviceAccountOperation.resourceId();
   ```

4. Create the VM:

   ```ts theme={null}
   const managedVmService = new InstanceService(sdk);
   const managedVmOperation = await managedVmService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "<VM_name>",
       }),
       spec: InstanceSpec.create({
         serviceAccountId,
         stopped: <true|false>,
         resources: ResourcesSpec.create({
           platform: "<platform>",
           size: {
             $case: "preset",
             preset: "<preset>",
           },
         }),
         gpuCluster: InstanceGpuClusterSpec.create({
           id: gpuClusterId,
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           deviceId: "<user_defined_ID>",
           type: {
             $case: "managedDisk",
             managedDisk: ManagedDisk.create({
               name: "<boot_disk_name>",
               spec: DiskSpec.create({
                 type: DiskSpec_DiskType.NETWORK_SSD,
                 source: {
                   $case: "sourceImageFamily",
                   sourceImageFamily: SourceImageFamily.create({
                     imageFamily: "<image_family>",
                   }),
                 },
                 size: {
                   $case: "sizeGibibytes",
                   sizeGibibytes: <size>,
                 },
               }),
             }),
           },
         }),
         secondaryDisks: [
           AttachedDiskSpec.create({
             attachMode:
               AttachedDiskSpec_AttachMode.READ_WRITE,
             deviceId: "device-2",
             type: {
               $case: "managedDisk",
               managedDisk: ManagedDisk.create({
                 name: "managed-secondary-disk",
                 spec: DiskSpec.create({
                   type: DiskSpec_DiskType.NETWORK_SSD,
                   size: {
                     $case: "sizeGibibytes",
                     sizeGibibytes: 10,
                   },
                 }),
               }),
             },
           }),
         ],
         filesystems: [
           AttachedFilesystemSpec.create({
             attachMode:
               AttachedFilesystemSpec_AttachMode.READ_WRITE,
             mountTag: "<filesystem_tag>",
             type: {
               $case: "existingFilesystem",
               existingFilesystem: ExistingFilesystem.create({
                 id: filesystemId,
               }),
             },
           }),
         ],
         cloudInitUserData: userData,
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
         hostname: "<FQDN_hostname>",
         reservationPolicy: ReservationPolicy.create({
           policy: ReservationPolicy_Policy.FORBID,
         }),
         recoveryPolicy: InstanceRecoveryPolicy.FAIL,
         preemptible: PreemptibleSpec.create({
           onPreemption:
             PreemptibleSpec_PreemptionPolicy.STOP,
         }),
         pricingModel: {
           $case: "followsSpotPrice",
           followsSpotPrice: FollowsSpotPriceSpec.create({}),
         },
       }),
     }),
   ).result;
   await managedVmOperation.wait();
   ```

   The code contains the following parameters:

   * `metadata.name`: VM's name.
   * `spec.serviceAccountId` (optional): Service account associated with the VM.
   * `spec.stopped` (optional): If you want to create a VM but not launch it, specify the `true` value. The VM will remain in the `Stopped` status.
   * `spec.resources.platform`: [VM platform](https://docs.nebius.com/compute/virtual-machines/types.md).
   * `spec.resources.size.preset`: VM preset. Depends on the chosen platform.
   * `spec.gpuCluster.id` (optional): ID of the GPU cluster created earlier.
   * `spec.bootDisk.attachMode`: Write permission of the boot disk. The only supported value is `READ_WRITE`.
   * `spec.bootDisk.deviceId` (optional): User-defined ID for mounting the boot disk to the VM. The default value is `disk-n` where `n` is an integer index. A `virtio-` prefix is added to the specified (or default) device ID.
   * `spec.bootDisk.type.managedDisk.name`: Name of the [VM-managed boot disk](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks) that you create along with the VM.
   * `spec.bootDisk.type.managedDisk.spec.type`: [Disk type](https://docs.nebius.com/compute/storage/types.md#network-ssd-disks).
   * `spec.bootDisk.type.managedDisk.spec.source.sourceImageFamily.imageFamily`: Public image that Nebius AI Cloud supports. For the list of available public images, see [Boot disk images for Compute virtual machines](https://docs.nebius.com/compute/storage/boot-disk-images.md).
   * `spec.bootDisk.type.managedDisk.spec.size.sizeGibibytes`: Disk size in gibibytes. Maximum boot disk size is 30,720 GiB (30 TiB).
   * `spec.secondaryDisks[].attachMode`: Write permission of the additional disk. The only supported value is `READ_WRITE`.
   * `spec.secondaryDisks[].deviceId`: User-defined ID for mounting the additional disk to the VM.
   * `spec.secondaryDisks[].type.managedDisk.name`: Name of a new additional VM-managed disk.
   * `spec.secondaryDisks[].type.managedDisk.spec.type`: Disk type of the additional disk.
   * `spec.secondaryDisks[].type.managedDisk.spec.size.sizeGibibytes`: Size of the additional disk in gibibytes.
   * `spec.filesystems[].attachMode`: Write permission of the filesystem. The only supported value is `READ_WRITE`.
   * `spec.filesystems[].mountTag`: Tag for mounting the filesystem to the VM.
   * `spec.filesystems[].type.existingFilesystem.id`: ID of the filesystem created earlier.
   * `spec.cloudInitUserData` (optional): Configuration of VM users in the [cloud-init](https://cloud-init.io/) format.
   * `spec.networkInterfaces[].subnetId`: ID of the subnet to attach the VM to.
   * `spec.networkInterfaces[].ipAddress`: Private IP address settings.
   * `spec.networkInterfaces[].publicIpAddress`: Public IP address settings. In the example, an empty `PublicIPAddress` assigns a dynamic public IP address.
   * `spec.hostname` (optional): Hostname for the VM's [FQDN](https://docs.nebius.com/compute/virtual-machines/fqdn.md). By default, the FQDN has the `<VM_ID>.<VM_network_ID>.compute.internal.` format.
   * `spec.reservationPolicy.policy` (optional): Policy for reservation usage. You can use [reservations of capacity resources](https://docs.nebius.com/compute/virtual-machines/reservations.md) and run your VM based on them.
   * `spec.recoveryPolicy` (optional): Defines what Compute does with the VM after it is preempted or fails.
   * `spec.preemptible.onPreemption` (optional; for preemptible VMs only): Specifies what happens when the VM is preempted. The only supported value is `STOP`: Compute stops the VM without deleting or restarting it.
   * `spec.pricingModel.followsSpotPrice` (optional; for preemptible VMs): Accepts the current spot price without setting a maximum spot price. To set a maximum spot price, use `spec.pricingModel.spotPricingPolicy` with the ID of a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) instead.

## Examples

### Create a VM without an additional disk or filesystem

**CLI**

To create a VM, run the following command:

```bash theme={null}
nebius compute instance create \
   --name <VM_name> \
   --resources-platform <platform> \
   --resources-preset <preset> \
   --boot-disk-managed-disk-name managed-boot-disk \
   --boot-disk-managed-disk-type network_ssd \
   --boot-disk-managed-disk-size-gibibytes 10 \
   --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-driverless \
   --boot-disk-attach-mode READ_WRITE \
   --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {}, "subnet_id": "<subnet_ID>"}]'
```

The VM is provided with a dynamic public IPv4 address.

For more information about the command parameters, see [Create a VM](#create-a-vm).

**Terraform**

1. Create a VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name      = "<VM_name>"
     parent_id = "<project_ID>"
     resources = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       managed_disk = {
         name = "managed-boot-disk"
         spec = {
           type                = "NETWORK_SSD"
           size_gibibytes      = 10
           source_image_family = {
             image_family = "ubuntu24.04-driverless"
           }
         }
       }
       attach_mode = "READ_WRITE"
     }
     network_interfaces = [
       {
         name       = "eth0"
         ip_address = {}
         public_ip_address = {}
         subnet_id = "<subnet_ID>"
       }
     ]
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the configuration parameters, see [Create a VM](#create-a-vm).

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a VM:

```go theme={null}
simpleBootDisk := &compute.AttachedDiskSpec{
    AttachMode: compute.AttachedDiskSpec_READ_WRITE,
    Type: &compute.AttachedDiskSpec_ManagedDisk{
        ManagedDisk: &compute.ManagedDisk{
            Name: "managed-boot-disk",
            Spec: &compute.DiskSpec{
                Size: &compute.DiskSpec_SizeGibibytes{
                    SizeGibibytes: 10,
                },
                Type: compute.DiskSpec_NETWORK_SSD,
                Source: &compute.DiskSpec_SourceImageFamily{
                    SourceImageFamily: &compute.SourceImageFamily{
                        ImageFamily: "ubuntu24.04-driverless",
                    },
                },
            },
        },
    },
}
simpleNetwork := &compute.NetworkInterfaceSpec{
    Name:            "eth0",
    SubnetId:        subnetID,
    IpAddress:       &compute.IPAddress{},
    PublicIpAddress: &compute.PublicIPAddress{},
}
simpleVMOperation, err := sdk.Services().Compute().V1().
    Instance().Create(
        ctx,
        &compute.CreateInstanceRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<VM_name>",
            },
            Spec: &compute.InstanceSpec{
                Resources: &compute.ResourcesSpec{
                    Platform: "<platform>",
                    Size: &compute.ResourcesSpec_Preset{
                        Preset: "<preset>",
                    },
                },
                BootDisk: simpleBootDisk,
                NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                    simpleNetwork,
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = simpleVMOperation.Wait(ctx); err != nil {
    return err
}
```

The VM is provided with a dynamic public IPv4 address.

For more information about the code parameters, see [Create a VM](#create-a-vm).

**Python SDK**

Create a VM:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
simple_vm_operation = await instance_service.create(
    CreateInstanceRequest(
        metadata=ResourceMetadata(name="<VM_name>"),
        spec=InstanceSpec(
            resources=ResourcesSpec(
                platform="<platform>",
                preset="<preset>",
            ),
            boot_disk=AttachedDiskSpec(
                attach_mode=(
                    AttachedDiskSpec.AttachMode.READ_WRITE
                ),
                managed_disk=ManagedDisk(
                    name="managed-boot-disk",
                    spec=DiskSpec(
                        type=DiskSpec.DiskType.NETWORK_SSD,
                        source_image_family=(
                            SourceImageFamily(
                                image_family=(
                                    "ubuntu24.04-driverless"
                                ),
                            )
                        ),
                        size_gibibytes=10,
                    ),
                ),
            ),
            network_interfaces=[
                NetworkInterfaceSpec(
                    name="eth0",
                    subnet_id=subnet_id,
                    ip_address=IPAddress(),
                    public_ip_address=PublicIPAddress(),
                ),
            ],
        ),
    ),
)
await simple_vm_operation.wait()
```

The VM is provided with a dynamic public IPv4 address.

For more information about the code parameters, see [Create a VM](#create-a-vm).

**JavaScript SDK**

Create a VM:

```ts theme={null}
const simpleVmService = new InstanceService(sdk);
const simpleVmOperation = await simpleVmService.create(
  CreateInstanceRequest.create({
    metadata: ResourceMetadata.create({
      name: "<VM_name>",
    }),
    spec: InstanceSpec.create({
      resources: ResourcesSpec.create({
        platform: "<platform>",
        size: {
          $case: "preset",
          preset: "<preset>",
        },
      }),
      bootDisk: AttachedDiskSpec.create({
        attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
        type: {
          $case: "managedDisk",
          managedDisk: ManagedDisk.create({
            name: "managed-boot-disk",
            spec: DiskSpec.create({
              type: DiskSpec_DiskType.NETWORK_SSD,
              source: {
                $case: "sourceImageFamily",
                sourceImageFamily: SourceImageFamily.create({
                  imageFamily: "ubuntu24.04-driverless",
                }),
              },
              size: {
                $case: "sizeGibibytes",
                sizeGibibytes: 10,
              },
            }),
          }),
        },
      }),
      networkInterfaces: [
        NetworkInterfaceSpec.create({
          name: "eth0",
          subnetId,
          ipAddress: IPAddress.create({}),
          publicIpAddress: PublicIPAddress.create({}),
        }),
      ],
    }),
  }),
).result;
await simpleVmOperation.wait();
```

The VM is provided with a dynamic public IPv4 address.

For more information about the code parameters, see [Create a VM](#create-a-vm).

### Create a VM with an additional disk

**CLI**

Create a VM, its boot disk and an additional disk together:

```bash theme={null}
nebius compute instance create \
  --name <VM_name> \
  --resources-platform <platform> \
  --resources-preset <preset> \
  --boot-disk-managed-disk-name managed-boot-disk \
  --boot-disk-managed-disk-type network_ssd \
  --boot-disk-managed-disk-size-gibibytes 10 \
  --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-driverless \
  --boot-disk-attach-mode READ_WRITE \
  --secondary-disks "[{\"attach_mode\": \"READ_WRITE\", \"device_id\": \"device-1\", \"managed_disk\": { \"name\": \"managed-secondary-disk\", \"spec\": { \"type\": \"network_ssd\", \"size_gibibytes\": 10 }}}]" \
  --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {}, "subnet_id": "<subnet_ID>"}]'
```

The VM is provided with a dynamic public IPv4 address.

For more information about the command parameters, see [Create a VM](#create-a-vm).

**Terraform**

1. Create a VM, its boot disk and an additional disk together:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name      = "<VM_name>"
     parent_id = "<project_ID>"
     resources = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       managed_disk = {
         name = "managed-boot-disk"
         spec = {
           type                = "NETWORK_SSD"
           size_gibibytes      = 10
           source_image_family = {
             image_family = "ubuntu24.04-driverless"
           }
         }
       }
       attach_mode = "READ_WRITE"
     }
     secondary_disks = [
       {
         managed_disk = {
           name = "managed-additional-disk"
           spec = {
             type           = "<disk_type>"
             size_gibibytes = <size>
           }
         }
         attach_mode = "READ_WRITE"
         device_id = "device-1"
       }
     ]
     network_interfaces = [
       {
         name       = "eth0"
         ip_address = {}
         public_ip_address = {}
         subnet_id = "<subnet_ID>"
       }
     ]
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the configuration parameters, see [Create a VM](#create-a-vm).

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a VM, its boot disk and an additional disk together:

```go theme={null}
additionalBootDisk := &compute.AttachedDiskSpec{
    AttachMode: compute.AttachedDiskSpec_READ_WRITE,
    Type: &compute.AttachedDiskSpec_ManagedDisk{
        ManagedDisk: &compute.ManagedDisk{
            Name: "managed-boot-disk",
            Spec: &compute.DiskSpec{
                Size: &compute.DiskSpec_SizeGibibytes{
                    SizeGibibytes: 10,
                },
                Type: compute.DiskSpec_NETWORK_SSD,
                Source: &compute.DiskSpec_SourceImageFamily{
                    SourceImageFamily: &compute.SourceImageFamily{
                        ImageFamily: "ubuntu24.04-driverless",
                    },
                },
            },
        },
    },
}
additionalDisk := &compute.AttachedDiskSpec{
    AttachMode: compute.AttachedDiskSpec_READ_WRITE,
    DeviceId:   "device-1",
    Type: &compute.AttachedDiskSpec_ManagedDisk{
        ManagedDisk: &compute.ManagedDisk{
            Name: "managed-secondary-disk",
            Spec: &compute.DiskSpec{
                Size: &compute.DiskSpec_SizeGibibytes{
                    SizeGibibytes: <size>,
                },
                Type: compute.DiskSpec_NETWORK_SSD,
            },
        },
    },
}
additionalNetwork := &compute.NetworkInterfaceSpec{
    Name:            "eth0",
    SubnetId:        subnetID,
    IpAddress:       &compute.IPAddress{},
    PublicIpAddress: &compute.PublicIPAddress{},
}
additionalVMOperation, err := sdk.Services().Compute().V1().
    Instance().Create(
        ctx,
        &compute.CreateInstanceRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<VM_name>",
            },
            Spec: &compute.InstanceSpec{
                Resources: &compute.ResourcesSpec{
                    Platform: "<platform>",
                    Size: &compute.ResourcesSpec_Preset{
                        Preset: "<preset>",
                    },
                },
                BootDisk: additionalBootDisk,
                SecondaryDisks: []*compute.AttachedDiskSpec{
                    additionalDisk,
                },
                NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                    additionalNetwork,
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = additionalVMOperation.Wait(ctx); err != nil {
    return err
}
```

The VM is provided with a dynamic public IPv4 address.

For more information about the code parameters, see [Create a VM](#create-a-vm).

**Python SDK**

Create a VM, its boot disk and an additional disk together:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
additional_vm_operation = await instance_service.create(
    CreateInstanceRequest(
        metadata=ResourceMetadata(name="<VM_name>"),
        spec=InstanceSpec(
            resources=ResourcesSpec(
                platform="<platform>",
                preset="<preset>",
            ),
            boot_disk=AttachedDiskSpec(
                attach_mode=(
                    AttachedDiskSpec.AttachMode.READ_WRITE
                ),
                managed_disk=ManagedDisk(
                    name="managed-boot-disk",
                    spec=DiskSpec(
                        type=DiskSpec.DiskType.NETWORK_SSD,
                        source_image_family=(
                            SourceImageFamily(
                                image_family=(
                                    "ubuntu24.04-driverless"
                                ),
                            )
                        ),
                        size_gibibytes=10,
                    ),
                ),
            ),
            secondary_disks=[
                AttachedDiskSpec(
                    attach_mode=(
                        AttachedDiskSpec.AttachMode.READ_WRITE
                    ),
                    managed_disk=ManagedDisk(
                        name="managed-secondary-disk",
                        spec=DiskSpec(
                            type=(
                                DiskSpec.DiskType.NETWORK_SSD
                            ),
                            size_gibibytes=<size>,
                        ),
                    ),
                    device_id="device-1",
                ),
            ],
            network_interfaces=[
                NetworkInterfaceSpec(
                    name="eth0",
                    subnet_id=subnet_id,
                    ip_address=IPAddress(),
                    public_ip_address=PublicIPAddress(),
                ),
            ],
        ),
    ),
)
await additional_vm_operation.wait()
```

The VM is provided with a dynamic public IPv4 address.

For more information about the code parameters, see [Create a VM](#create-a-vm).

**JavaScript SDK**

Create a VM, its boot disk and an additional disk together:

```ts theme={null}
const additionalVmService = new InstanceService(sdk);
const additionalVmOperation =
  await additionalVmService.create(
    CreateInstanceRequest.create({
      metadata: ResourceMetadata.create({
        name: "<VM_name>",
      }),
      spec: InstanceSpec.create({
        resources: ResourcesSpec.create({
          platform: "<platform>",
          size: {
            $case: "preset",
            preset: "<preset>",
          },
        }),
        bootDisk: AttachedDiskSpec.create({
          attachMode:
            AttachedDiskSpec_AttachMode.READ_WRITE,
          type: {
            $case: "managedDisk",
            managedDisk: ManagedDisk.create({
              name: "managed-boot-disk",
              spec: DiskSpec.create({
                type: DiskSpec_DiskType.NETWORK_SSD,
                source: {
                  $case: "sourceImageFamily",
                  sourceImageFamily: SourceImageFamily.create({
                    imageFamily: "ubuntu24.04-driverless",
                  }),
                },
                size: {
                  $case: "sizeGibibytes",
                  sizeGibibytes: 10,
                },
              }),
            }),
          },
        }),
        secondaryDisks: [
          AttachedDiskSpec.create({
            attachMode:
              AttachedDiskSpec_AttachMode.READ_WRITE,
            deviceId: "device-1",
            type: {
              $case: "managedDisk",
              managedDisk: ManagedDisk.create({
                name: "managed-secondary-disk",
                spec: DiskSpec.create({
                  type: DiskSpec_DiskType.NETWORK_SSD,
                  size: {
                    $case: "sizeGibibytes",
                    sizeGibibytes: <size>,
                  },
                }),
              }),
            },
          }),
        ],
        networkInterfaces: [
          NetworkInterfaceSpec.create({
            name: "eth0",
            subnetId,
            ipAddress: IPAddress.create({}),
            publicIpAddress: PublicIPAddress.create({}),
          }),
        ],
      }),
    }),
  ).result;
await additionalVmOperation.wait();
```

The VM is provided with a dynamic public IPv4 address.

For more information about the code parameters, see [Create a VM](#create-a-vm).

### Create a VM with a filesystem

**CLI**

1. Create a filesystem:

   ```bash theme={null}
   nebius compute filesystem create \
     --name <filesystem_name> \
     --size-gibibytes 10 \
     --type network_ssd \
     --block-size-bytes 4096
   ```

   Save the filesystem ID from the output `metadata.id` parameter.

   > [!WARNING]
   >
   > [Mount filesystems](https://docs.nebius.com/compute/storage/use.md#shared-filesystems) after you create the VM. Otherwise, the filesystems are not attached to the VM.

2. Create the VM:

   ```bash theme={null}
   nebius compute instance create \
     --name <VM_name> \
     --stopped=<true|false> \
     --resources-platform <platform> \
     --resources-preset <preset> \
     --boot-disk-managed-disk-name managed-boot-disk \
     --boot-disk-managed-disk-type network_ssd \
     --boot-disk-managed-disk-size-gibibytes 10 \
     --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-driverless \
     --boot-disk-attach-mode READ_WRITE \
     --filesystems '[{"existing_filesystem": {"id": "<filesystem_ID>"}, "attach_mode": "READ_WRITE", "mount_tag": "<filesystem_tag>"}]' \
     --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {}, "subnet_id": "<subnet_ID>"}]'
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the command parameters, see [Create a VM](#create-a-vm).

**Terraform**

1. Create a filesystem:

   ```hcl theme={null}
   resource "nebius_compute_v1_filesystem" "my_filesystem" {
     name             = "<filesystem_name>"
     parent_id        = "<project_ID>"
     size_gibibytes   = 10
     type             = "NETWORK_SSD"
     block_size_bytes = 4096
   }
   ```

   For more information, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

   > [!WARNING]
   >
   > [Mount filesystems](https://docs.nebius.com/compute/storage/use.md#shared-filesystems) after you create the VM. Otherwise, the filesystems are not attached to the VM.

2. Create the VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name      = "<VM_name>"
     parent_id = "<project_ID>"
     resources = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       managed_disk = {
         name = "managed-boot-disk"
         spec = {
           type                = "NETWORK_SSD"
           size_gibibytes      = 10
           source_image_family = {
             image_family = "ubuntu24.04-driverless"
           }
         }
       }
       attach_mode = "READ_WRITE"
     }
     filesystems = [
       {
         existing_filesystem = {
           id = nebius_compute_v1_filesystem.my_filesystem.id
         }
         attach_mode = "READ_WRITE"
         mount_tag   = "<filesystem_tag>"
       }
     ]
     network_interfaces = [
       {
         name       = "eth0"
         ip_address = {}
         public_ip_address = {}
         subnet_id = "<subnet_ID>"
       }
     ]
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the configuration parameters, see [Create a VM](#create-a-vm).

3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Create a filesystem:

   ```go theme={null}
   filesystemOperation, err := sdk.Services().Compute().V1().
       Filesystem().Create(
           ctx,
           &compute.CreateFilesystemRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<filesystem_name>",
               },
               Spec: &compute.FilesystemSpec{
                   Size: &compute.FilesystemSpec_SizeGibibytes{
                       SizeGibibytes: 10,
                   },
                   BlockSizeBytes: 4096,
                   Type:           compute.FilesystemSpec_NETWORK_SSD,
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = filesystemOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   > [!WARNING]
   >
   > [Mount filesystems](https://docs.nebius.com/compute/storage/use.md#shared-filesystems) after you create the VM. Otherwise, the filesystems are not attached to the VM.

2. Create the VM:

   ```go theme={null}
   filesystemBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "managed-boot-disk",
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 10,
                   },
                   Type: compute.DiskSpec_NETWORK_SSD,
                   Source: &compute.DiskSpec_SourceImageFamily{
                       SourceImageFamily: &compute.SourceImageFamily{
                           ImageFamily: "ubuntu24.04-driverless",
                       },
                   },
               },
           },
       },
   }
   attachedFilesystem := &compute.AttachedFilesystemSpec{
       AttachMode: compute.AttachedFilesystemSpec_READ_WRITE,
       MountTag:   "<filesystem_tag>",
       Type: &compute.AttachedFilesystemSpec_ExistingFilesystem{
           ExistingFilesystem: &compute.ExistingFilesystem{
               Id: filesystemID,
           },
       },
   }
   filesystemNetwork := &compute.NetworkInterfaceSpec{
       Name:            "eth0",
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   filesystemVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<VM_name>",
               },
               Spec: &compute.InstanceSpec{
                   Stopped: <true|false>,
                   Resources: &compute.ResourcesSpec{
                       Platform: "<platform>",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "<preset>",
                       },
                   },
                   BootDisk: filesystemBootDisk,
                   Filesystems: []*compute.AttachedFilesystemSpec{
                       attachedFilesystem,
                   },
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       filesystemNetwork,
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = filesystemVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

**Python SDK**

1. Create a filesystem:

   ```python theme={null}
   filesystem_service = FilesystemServiceClient(sdk)
   filesystem_operation = await filesystem_service.create(
       CreateFilesystemRequest(
           metadata=ResourceMetadata(name="<filesystem_name>"),
           spec=FilesystemSpec(
               block_size_bytes=4096,
               type=FilesystemSpec.FilesystemType.NETWORK_SSD,
               size_gibibytes=10,
           ),
       ),
   )
   await filesystem_operation.wait()
   ```

   > [!WARNING]
   >
   > [Mount filesystems](https://docs.nebius.com/compute/storage/use.md#shared-filesystems) after you create the VM. Otherwise, the filesystems are not attached to the VM.

2. Create the VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   filesystem_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<VM_name>"),
           spec=InstanceSpec(
               stopped=<True|False>,
               resources=ResourcesSpec(
                   platform="<platform>",
                   preset="<preset>",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   managed_disk=ManagedDisk(
                       name="managed-boot-disk",
                       spec=DiskSpec(
                           type=DiskSpec.DiskType.NETWORK_SSD,
                           source_image_family=(
                               SourceImageFamily(
                                   image_family=(
                                       "ubuntu24.04-driverless"
                                   ),
                               )
                           ),
                           size_gibibytes=10,
                       ),
                   ),
               ),
               filesystems=[
                   AttachedFilesystemSpec(
                       attach_mode=(
                           AttachedFilesystemSpec.AttachMode.READ_WRITE
                       ),
                       existing_filesystem=ExistingFilesystem(
                           id=filesystem_id,
                       ),
                       mount_tag="<filesystem_tag>",
                   ),
               ],
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await filesystem_vm_operation.wait()
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

**JavaScript SDK**

1. Create a filesystem:

   ```ts theme={null}
   const filesystemCreateService = new FilesystemService(sdk);
   const filesystemOperation =
     await filesystemCreateService.create(
       CreateFilesystemRequest.create({
         metadata: ResourceMetadata.create({
           name: "<filesystem_name>",
         }),
         spec: FilesystemSpec.create({
           blockSizeBytes: 4096,
           type: FilesystemSpec_FilesystemType.NETWORK_SSD,
           size: {
             $case: "sizeGibibytes",
             sizeGibibytes: 10,
           },
         }),
       }),
     ).result;
   await filesystemOperation.wait();
   ```

   > [!WARNING]
   >
   > [Mount filesystems](https://docs.nebius.com/compute/storage/use.md#shared-filesystems) after you create the VM. Otherwise, the filesystems are not attached to the VM.

2. Create the VM:

   ```ts theme={null}
   const filesystemVmService = new InstanceService(sdk);
   const filesystemVmOperation =
     await filesystemVmService.create(
       CreateInstanceRequest.create({
         metadata: ResourceMetadata.create({
           name: "<VM_name>",
         }),
         spec: InstanceSpec.create({
           stopped: <true|false>,
           resources: ResourcesSpec.create({
             platform: "<platform>",
             size: {
               $case: "preset",
               preset: "<preset>",
             },
           }),
           bootDisk: AttachedDiskSpec.create({
             attachMode:
               AttachedDiskSpec_AttachMode.READ_WRITE,
             type: {
               $case: "managedDisk",
               managedDisk: ManagedDisk.create({
                 name: "managed-boot-disk",
                 spec: DiskSpec.create({
                   type: DiskSpec_DiskType.NETWORK_SSD,
                   source: {
                     $case: "sourceImageFamily",
                     sourceImageFamily: SourceImageFamily.create({
                       imageFamily: "ubuntu24.04-driverless",
                     }),
                   },
                   size: {
                     $case: "sizeGibibytes",
                     sizeGibibytes: 10,
                   },
                 }),
               }),
             },
           }),
           filesystems: [
             AttachedFilesystemSpec.create({
               attachMode:
                 AttachedFilesystemSpec_AttachMode.READ_WRITE,
               mountTag: "<filesystem_tag>",
               type: {
                 $case: "existingFilesystem",
                 existingFilesystem: ExistingFilesystem.create({
                   id: filesystemId,
                 }),
               },
             }),
           ],
           networkInterfaces: [
             NetworkInterfaceSpec.create({
               name: "eth0",
               subnetId,
               ipAddress: IPAddress.create({}),
               publicIpAddress: PublicIPAddress.create({}),
             }),
           ],
         }),
       }),
     ).result;
   await filesystemVmOperation.wait();
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

### Create a VM with local SSD disks

> [!NOTE]
>
> Local SSD disks are available only for supported platforms and presets. For details, see [Availability](https://docs.nebius.com/compute/storage/local-disks.md#availability).

**CLI**

To create a VM with local SSD disks, run the following command:

```bash theme={null}
nebius compute instance create \
  --name <VM_name> \
  --stopped=<true|false> \
  --resources-platform <platform> \
  --resources-preset <preset> \
  --boot-disk-managed-disk-name managed-boot-disk \
  --boot-disk-managed-disk-type network_ssd \
  --boot-disk-managed-disk-size-gibibytes 10 \
  --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-driverless \
  --boot-disk-attach-mode READ_WRITE \
  --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {}, "subnet_id": "<subnet_ID>"}]' \
  --local-disks-passthrough-group-requested=true
```

This adds ephemeral local storage to the VM.

The example creates a private IPv4 address and doesn't assign a public IPv4 address. For more information about the command parameters, see [Create a VM](#create-a-vm).

**Terraform**

1. Create the VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name      = "<VM_name>"
     parent_id = "<project_ID>"
     resources = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       managed_disk = {
         name = "managed-boot-disk"
         spec = {
           type                = "NETWORK_SSD"
           size_gibibytes      = 10
           source_image_family = {
             image_family = "ubuntu24.04-driverless"
           }
         }
       }
       attach_mode = "READ_WRITE"
     }
     network_interfaces = [
       {
         name       = "eth0"
         ip_address = {}
         public_ip_address = {}
         subnet_id = "<subnet_ID>"
       }
     ]
     local_disks = {
       passthrough_group = {
         requested = true
       }
     }
   }
   ```

   This provides a VM with ephemeral local storage.

   The example creates a private IPv4 address and doesn't assign a public IPv4 address. For more information about the configuration parameters, see [Create a VM](#create-a-vm).

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

Create a VM with local SSD disks:

```go theme={null}
localBootDisk := &compute.AttachedDiskSpec{
    AttachMode: compute.AttachedDiskSpec_READ_WRITE,
    Type: &compute.AttachedDiskSpec_ManagedDisk{
        ManagedDisk: &compute.ManagedDisk{
            Name: "managed-boot-disk",
            Spec: &compute.DiskSpec{
                Size: &compute.DiskSpec_SizeGibibytes{
                    SizeGibibytes: 10,
                },
                Type: compute.DiskSpec_NETWORK_SSD,
                Source: &compute.DiskSpec_SourceImageFamily{
                    SourceImageFamily: &compute.SourceImageFamily{
                        ImageFamily: "ubuntu24.04-driverless",
                    },
                },
            },
        },
    },
}
localDiskNetwork := &compute.NetworkInterfaceSpec{
    Name:            "eth0",
    SubnetId:        subnetID,
    IpAddress:       &compute.IPAddress{},
    PublicIpAddress: &compute.PublicIPAddress{},
}
passthroughRequest := &compute.PassthroughGroupRequest{
    Requested: true,
}
localDiskRequest := &compute.LocalDisksSpec_PassthroughGroup{
    PassthroughGroup: passthroughRequest,
}
localDiskVMOperation, err := sdk.Services().Compute().V1().
    Instance().Create(
        ctx,
        &compute.CreateInstanceRequest{
            Metadata: &common.ResourceMetadata{
                Name: "<VM_name>",
            },
            Spec: &compute.InstanceSpec{
                Stopped: <true|false>,
                Resources: &compute.ResourcesSpec{
                    Platform: "<platform>",
                    Size: &compute.ResourcesSpec_Preset{
                        Preset: "<preset>",
                    },
                },
                BootDisk: localBootDisk,
                NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                    localDiskNetwork,
                },
                LocalDisks: &compute.LocalDisksSpec{
                    Request: localDiskRequest,
                },
            },
        },
    )
if err != nil {
    return err
}
if _, err = localDiskVMOperation.Wait(ctx); err != nil {
    return err
}
```

This adds ephemeral local storage to the VM.

The example creates a private IPv4 address and doesn't assign a public IPv4 address. For more information about the code parameters, see [Create a VM](#create-a-vm).

**Python SDK**

Create a VM with local SSD disks:

```python theme={null}
instance_service = InstanceServiceClient(sdk)
local_disk_vm_operation = await instance_service.create(
    CreateInstanceRequest(
        metadata=ResourceMetadata(name="<VM_name>"),
        spec=InstanceSpec(
            stopped=<True|False>,
            resources=ResourcesSpec(
                platform="<platform>",
                preset="<preset>",
            ),
            boot_disk=AttachedDiskSpec(
                attach_mode=(
                    AttachedDiskSpec.AttachMode.READ_WRITE
                ),
                managed_disk=ManagedDisk(
                    name="managed-boot-disk",
                    spec=DiskSpec(
                        type=DiskSpec.DiskType.NETWORK_SSD,
                        source_image_family=(
                            SourceImageFamily(
                                image_family=(
                                    "ubuntu24.04-driverless"
                                ),
                            )
                        ),
                        size_gibibytes=10,
                    ),
                ),
            ),
            network_interfaces=[
                NetworkInterfaceSpec(
                    name="eth0",
                    subnet_id=subnet_id,
                    ip_address=IPAddress(),
                    public_ip_address=PublicIPAddress(),
                ),
            ],
            local_disks=LocalDisksSpec(
                passthrough_group=PassthroughGroupRequest(
                    requested=True,
                ),
            ),
        ),
    ),
)
await local_disk_vm_operation.wait()
```

This adds ephemeral local storage to the VM.

The example creates a private IPv4 address and doesn't assign a public IPv4 address. For more information about the code parameters, see [Create a VM](#create-a-vm).

**JavaScript SDK**

Create a VM with local SSD disks:

```ts theme={null}
const localDiskVmService = new InstanceService(sdk);
const localDiskVmOperation =
  await localDiskVmService.create(
    CreateInstanceRequest.create({
      metadata: ResourceMetadata.create({
        name: "<VM_name>",
      }),
      spec: InstanceSpec.create({
        stopped: <true|false>,
        resources: ResourcesSpec.create({
          platform: "<platform>",
          size: {
            $case: "preset",
            preset: "<preset>",
          },
        }),
        bootDisk: AttachedDiskSpec.create({
          attachMode:
            AttachedDiskSpec_AttachMode.READ_WRITE,
          type: {
            $case: "managedDisk",
            managedDisk: ManagedDisk.create({
              name: "managed-boot-disk",
              spec: DiskSpec.create({
                type: DiskSpec_DiskType.NETWORK_SSD,
                source: {
                  $case: "sourceImageFamily",
                  sourceImageFamily: SourceImageFamily.create({
                    imageFamily: "ubuntu24.04-driverless",
                  }),
                },
                size: {
                  $case: "sizeGibibytes",
                  sizeGibibytes: 10,
                },
              }),
            }),
          },
        }),
        networkInterfaces: [
          NetworkInterfaceSpec.create({
            name: "eth0",
            subnetId,
            ipAddress: IPAddress.create({}),
            publicIpAddress: PublicIPAddress.create({}),
          }),
        ],
        localDisks: LocalDisksSpec.create({
          request: {
            $case: "passthroughGroup",
            passthroughGroup:
              PassthroughGroupRequest.create({
                requested: true,
              }),
          },
        }),
      }),
    }),
  ).result;
await localDiskVmOperation.wait();
```

This adds ephemeral local storage to the VM.

The example creates a private IPv4 address and doesn't assign a public IPv4 address. For more information about the code parameters, see [Create a VM](#create-a-vm).

### Create a VM with standalone boot and additional disks

By default, when you create a VM, its disks are created along with this VM. Such disks are called [VM-managed](https://docs.nebius.com/compute/storage/types.md#vm-managed-and-standalone-disks): their lifecycle is tied to the VM, so when you delete the VM, its disks are deleted along with it.

Alternatively, if you already have a disk or you want to keep the disk after the VM deletion, create a standalone disk first and attach it to the VM afterward.

To create standalone disks and a VM with them, do the following:

**CLI**

1. Create a boot disk:

   ```bash theme={null}
   nebius compute disk create \
     --name <boot_disk_name> \
     --size-gibibytes 50 \
     --type network_ssd \
     --source-image-family-image-family ubuntu24.04-cuda13.0 \
     --block-size-bytes 4096
   ```

   Save the disk ID from the output `metadata.id` parameter.

   For more information about disk creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Create an additional disk:

   ```bash theme={null}
   nebius compute disk create \
     --name <additional_disk_name> \
     --size-gibibytes 10 \
     --type network_ssd \
     --block-size-bytes 4096
   ```

   Save the disk ID from the output `metadata.id` parameter.

   > [!WARNING]
   >
   > After you create the VM, [mount the additional disks](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these disks.

3. Create a VM:

   ```bash theme={null}
   nebius compute instance create \
     --name <VM_name> \
     --resources-platform <platform> \
     --resources-preset <preset> \
     --boot-disk-existing-disk-id <boot_disk_ID> \
     --boot-disk-attach-mode read_write \
     --boot-disk-device-id <user_defined_ID> \
     --secondary-disks "[{\"existing_disk\": {\"id\": \"<additional_disk_ID>\"}, \"attach_mode\": \"READ_WRITE\", \"device_id\": \"device-1\"}]" \
     --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {}, "subnet_id": "<subnet_ID>"}]'
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the command parameters, see [Create a VM](#create-a-vm).

**Terraform**

1. Create a boot disk by using the following configuration:

   ```hcl theme={null}
   resource "nebius_compute_v1_disk" "my_boot_disk" {
     name                = "<boot_disk_name>"
     parent_id           = "<project_ID>"
     size_gibibytes      = "50"
     type                = "NETWORK_SSD"
     source_image_family = {
       image_family = "ubuntu24.04-cuda13.0"
     }
     block_size_bytes = 4096
   }
   ```

   Set the `parent_id` to your [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).

   For more information, see [Volume parameters](https://docs.nebius.com/compute/storage/manage.md#volume-parameters).

2. Create an additional disk:

   ```hcl theme={null}
   resource "nebius_compute_v1_disk" "my_additional_disk" {
     name             = "<additional_disk_name>"
     parent_id        = "<project_ID>"
     size_gibibytes   = "10"
     type             = "NETWORK_SSD"
     block_size_bytes = 4096
   }
   ```

   > [!WARNING]
   >
   > After you create the VM, [mount the additional disks](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these disks.

3. Create a VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name       = "<VM_name>"
     parent_id  = "<project_ID>"
     resources  = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       existing_disk = {
         id = nebius_compute_v1_disk.my_boot_disk.id
       }
       attach_mode = "READ_WRITE"
     }
     secondary_disks = [
       {
         existing_disk = {
           id = nebius_compute_v1_disk.my_additional_disk.id
         }
         attach_mode = "READ_WRITE"
         device_id   = "<user_defined_ID>"
       }
     ]
     network_interfaces = [
       {
         name              = "eth0"
         ip_address        = {}
         public_ip_address = {}
         subnet_id         = "<subnet_ID>"
       }
     ]
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the configuration parameters, see [Create a VM](#create-a-vm).

4. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

5. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Create a boot disk:

   ```go theme={null}
   bootDiskOperation, err := sdk.Services().Compute().V1().
       Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<boot_disk_name>",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 50,
                   },
                   BlockSizeBytes: 4096,
                   Type:           compute.DiskSpec_NETWORK_SSD,
                   Source: &compute.DiskSpec_SourceImageFamily{
                       SourceImageFamily: &compute.SourceImageFamily{
                           ImageFamily: "ubuntu24.04-cuda13.0",
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = bootDiskOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   For more information about disk creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Create an additional disk:

   ```go theme={null}
   addDiskOperation, err := sdk.Services().Compute().V1().
       Disk().Create(
           ctx,
           &compute.CreateDiskRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<additional_disk_name>",
               },
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 10,
                   },
                   BlockSizeBytes: 4096,
                   Type:           compute.DiskSpec_NETWORK_SSD,
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = addDiskOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   > [!WARNING]
   >
   > After you create the VM, [mount the additional disks](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these disks.

3. Create a VM:

   ```go theme={null}
   standaloneNetwork := &compute.NetworkInterfaceSpec{
       Name:            "eth0",
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   standaloneAttachMode := compute.AttachedDiskSpec_READ_WRITE
   standaloneVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<VM_name>",
               },
               Spec: &compute.InstanceSpec{
                   Resources: &compute.ResourcesSpec{
                       Platform: "<platform>",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "<preset>",
                       },
                   },
                   BootDisk: &compute.AttachedDiskSpec{
                       AttachMode: standaloneAttachMode,
                       DeviceId:   "<user_defined_ID>",
                       Type: &compute.AttachedDiskSpec_ExistingDisk{
                           ExistingDisk: &compute.ExistingDisk{
                               Id: bootDiskID,
                           },
                       },
                   },
                   SecondaryDisks: []*compute.AttachedDiskSpec{
                       {
                           AttachMode: standaloneAttachMode,
                           DeviceId:   "<user_defined_ID>",
                           Type: &compute.AttachedDiskSpec_ExistingDisk{
                               ExistingDisk: &compute.ExistingDisk{
                                   Id: additionalDiskID,
                               },
                           },
                       },
                   },
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       standaloneNetwork,
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = standaloneVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

**Python SDK**

1. Create a boot disk:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   boot_disk_operation = await disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(name="<boot_disk_name>"),
           spec=DiskSpec(
               block_size_bytes=4096,
               type=DiskSpec.DiskType.NETWORK_SSD,
               source_image_family=SourceImageFamily(
                   image_family="ubuntu24.04-cuda13.0",
               ),
               size_gibibytes=50,
           ),
       ),
   )
   await boot_disk_operation.wait()
   ```

   For more information about disk creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Create an additional disk:

   ```python theme={null}
   disk_service = DiskServiceClient(sdk)
   additional_disk_operation = await disk_service.create(
       CreateDiskRequest(
           metadata=ResourceMetadata(
               name="<additional_disk_name>",
           ),
           spec=DiskSpec(
               block_size_bytes=4096,
               type=DiskSpec.DiskType.NETWORK_SSD,
               size_gibibytes=10,
           ),
       ),
   )
   await additional_disk_operation.wait()
   ```

   > [!WARNING]
   >
   > After you create the VM, [mount the additional disks](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these disks.

3. Create a VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   standalone_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<VM_name>"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="<platform>",
                   preset="<preset>",
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=AttachedDiskSpec.AttachMode.READ_WRITE,
                   existing_disk=ExistingDisk(id=boot_disk_id),
                   device_id="<user_defined_ID>",
               ),
               secondary_disks=[
                   AttachedDiskSpec(
                       attach_mode=(
                           AttachedDiskSpec.AttachMode.READ_WRITE
                       ),
                       existing_disk=ExistingDisk(
                           id=additional_disk_id,
                       ),
                       device_id="<user_defined_ID>",
                   ),
               ],
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await standalone_vm_operation.wait()
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

**JavaScript SDK**

1. Create a boot disk:

   ```ts theme={null}
   const bootDiskCreateService = new DiskService(sdk);
   const bootDiskOperation = await bootDiskCreateService.create(
     CreateDiskRequest.create({
       metadata: ResourceMetadata.create({
         name: "<boot_disk_name>",
       }),
       spec: DiskSpec.create({
         blockSizeBytes: 4096,
         type: DiskSpec_DiskType.NETWORK_SSD,
         source: {
           $case: "sourceImageFamily",
           sourceImageFamily: SourceImageFamily.create({
             imageFamily: "ubuntu24.04-cuda13.0",
           }),
         },
         size: {
           $case: "sizeGibibytes",
           sizeGibibytes: 50,
         },
       }),
     }),
   ).result;
   await bootDiskOperation.wait();
   ```

   For more information about disk creation, see [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md).

2. Create an additional disk:

   ```ts theme={null}
   const additionalDiskCreateService = new DiskService(sdk);
   const additionalDiskOperation =
     await additionalDiskCreateService.create(
       CreateDiskRequest.create({
         metadata: ResourceMetadata.create({
           name: "<additional_disk_name>",
         }),
         spec: DiskSpec.create({
           blockSizeBytes: 4096,
           type: DiskSpec_DiskType.NETWORK_SSD,
           size: {
             $case: "sizeGibibytes",
             sizeGibibytes: 10,
           },
         }),
       }),
     ).result;
   await additionalDiskOperation.wait();
   ```

   > [!WARNING]
   >
   > After you create the VM, [mount the additional disks](https://docs.nebius.com/compute/storage/use.md#how-to-mount-volumes-to-vms) to it. Otherwise, the VM's operating system does not recognize these disks.

3. Create a VM:

   ```ts theme={null}
   const standaloneVmService = new InstanceService(sdk);
   const standaloneVmOperation =
     await standaloneVmService.create(
       CreateInstanceRequest.create({
         metadata: ResourceMetadata.create({
           name: "<VM_name>",
         }),
         spec: InstanceSpec.create({
           resources: ResourcesSpec.create({
             platform: "<platform>",
             size: {
               $case: "preset",
               preset: "<preset>",
             },
           }),
           bootDisk: AttachedDiskSpec.create({
             attachMode:
               AttachedDiskSpec_AttachMode.READ_WRITE,
             deviceId: "<user_defined_ID>",
             type: {
               $case: "existingDisk",
               existingDisk: ExistingDisk.create({
                 id: bootDiskId,
               }),
             },
           }),
           secondaryDisks: [
             AttachedDiskSpec.create({
               attachMode:
                 AttachedDiskSpec_AttachMode.READ_WRITE,
               deviceId: "<user_defined_ID>",
               type: {
                 $case: "existingDisk",
                 existingDisk: ExistingDisk.create({
                   id: additionalDiskId,
                 }),
               },
             }),
           ],
           networkInterfaces: [
             NetworkInterfaceSpec.create({
               name: "eth0",
               subnetId,
               ipAddress: IPAddress.create({}),
               publicIpAddress: PublicIPAddress.create({}),
             }),
           ],
         }),
       }),
     ).result;
   await standaloneVmOperation.wait();
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

### Create a VM within a GPU cluster

If you want to create a VM with 8 GPUs (for example, for training models), create a GPU cluster for the VM. By using InfiniBand™, the cluster accelerates tasks that require high-performance computing (HPC) power.

**CLI**

1. Create a GPU cluster:

   ```bash theme={null}
   nebius compute gpu-cluster create \
     --name <GPU_cluster_name> \
     --infiniband-fabric <fabric>
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

   Save the cluster ID from the output `metadata.id` parameter.

2. Create a VM:

   ```bash theme={null}
   nebius compute instance create \
     --name <VM_name> \
     --resources-platform <platform> \
     --resources-preset <preset> \
     --boot-disk-managed-disk-name managed-boot-disk \
     --boot-disk-managed-disk-type network_ssd \
     --boot-disk-managed-disk-size-gibibytes 40 \
     --boot-disk-managed-disk-source-image-family-image-family ubuntu24.04-cuda13.0 \
     --boot-disk-attach-mode READ_WRITE \
     --network-interfaces '[{"name": "eth0", "ip_address": {}, "public_ip_address": {}, "subnet_id": "<subnet_ID>"}]' \
     --gpu-cluster-id <GPU_cluster_ID>
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the command parameters, see [Create a VM](#create-a-vm).

**Terraform**

1. Create a GPU cluster:

   ```hcl theme={null}
   resource "nebius_compute_v1_gpu_cluster" "my_gpu_cluster" {
     name              = "<GPU_cluster_name>"
     parent_id         = "<project_ID>"
     infiniband_fabric = "<fabric>"
   }
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

2. Create a VM:

   ```hcl theme={null}
   resource "nebius_compute_v1_instance" "my_vm" {
     name      = "<VM_name>"
     parent_id = "<project_ID>"
     resources = {
       platform = "<platform>"
       preset   = "<preset>"
     }
     boot_disk = {
       managed_disk = {
         name = "managed-boot-disk"
         spec = {
           type                = "NETWORK_SSD"
           size_gibibytes      = 40
           source_image_family = {
             image_family = "ubuntu24.04-cuda13.0"
           }
         }
       }
       attach_mode = "READ_WRITE"
     }
     network_interfaces = [
       {
         name       = "eth0"
         ip_address = {}
         public_ip_address = {}
         subnet_id = "<subnet_ID>"
       }
     ]
     gpu_cluster = {
       id = nebius_compute_v1_gpu_cluster.my_gpu_cluster.id
     }
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the configuration parameters, see [Create a VM](#create-a-vm).

3. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

4. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Create a GPU cluster:

   ```go theme={null}
   gpuClusterOperation, err := sdk.Services().Compute().V1().
       GpuCluster().Create(
           ctx,
           &compute.CreateGpuClusterRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<GPU_cluster_name>",
               },
               Spec: &compute.GpuClusterSpec{
                   InfinibandFabric: "<fabric>",
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = gpuClusterOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

2. Create a VM:

   ```go theme={null}
   clusterBootDisk := &compute.AttachedDiskSpec{
       AttachMode: compute.AttachedDiskSpec_READ_WRITE,
       Type: &compute.AttachedDiskSpec_ManagedDisk{
           ManagedDisk: &compute.ManagedDisk{
               Name: "managed-boot-disk",
               Spec: &compute.DiskSpec{
                   Size: &compute.DiskSpec_SizeGibibytes{
                       SizeGibibytes: 40,
                   },
                   Type: compute.DiskSpec_NETWORK_SSD,
                   Source: &compute.DiskSpec_SourceImageFamily{
                       SourceImageFamily: &compute.SourceImageFamily{
                           ImageFamily: "ubuntu24.04-cuda13.0",
                       },
                   },
               },
           },
       },
   }
   clusterNetwork := &compute.NetworkInterfaceSpec{
       Name:            "eth0",
       SubnetId:        subnetID,
       IpAddress:       &compute.IPAddress{},
       PublicIpAddress: &compute.PublicIPAddress{},
   }
   clusterVMOperation, err := sdk.Services().Compute().V1().
       Instance().Create(
           ctx,
           &compute.CreateInstanceRequest{
               Metadata: &common.ResourceMetadata{
                   Name: "<VM_name>",
               },
               Spec: &compute.InstanceSpec{
                   Resources: &compute.ResourcesSpec{
                       Platform: "<platform>",
                       Size: &compute.ResourcesSpec_Preset{
                           Preset: "<preset>",
                       },
                   },
                   GpuCluster: &compute.InstanceGpuClusterSpec{
                       Id: gpuClusterID,
                   },
                   BootDisk: clusterBootDisk,
                   NetworkInterfaces: []*compute.NetworkInterfaceSpec{
                       clusterNetwork,
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = clusterVMOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

**Python SDK**

1. Create a GPU cluster:

   ```python theme={null}
   gpu_cluster_service = GpuClusterServiceClient(sdk)
   gpu_cluster_operation = await gpu_cluster_service.create(
       CreateGpuClusterRequest(
           metadata=ResourceMetadata(
               name="<GPU_cluster_name>",
           ),
           spec=GpuClusterSpec(
               infiniband_fabric="<fabric>",
           ),
       ),
   )
   await gpu_cluster_operation.wait()
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

2. Create a VM:

   ```python theme={null}
   instance_service = InstanceServiceClient(sdk)
   cluster_vm_operation = await instance_service.create(
       CreateInstanceRequest(
           metadata=ResourceMetadata(name="<VM_name>"),
           spec=InstanceSpec(
               resources=ResourcesSpec(
                   platform="<platform>",
                   preset="<preset>",
               ),
               gpu_cluster=InstanceGpuClusterSpec(
                   id=gpu_cluster_id,
               ),
               boot_disk=AttachedDiskSpec(
                   attach_mode=(
                       AttachedDiskSpec.AttachMode.READ_WRITE
                   ),
                   managed_disk=ManagedDisk(
                       name="managed-boot-disk",
                       spec=DiskSpec(
                           type=DiskSpec.DiskType.NETWORK_SSD,
                           source_image_family=(
                               SourceImageFamily(
                                   image_family="ubuntu24.04-cuda13.0",
                               )
                           ),
                           size_gibibytes=40,
                       ),
                   ),
               ),
               network_interfaces=[
                   NetworkInterfaceSpec(
                       name="eth0",
                       subnet_id=subnet_id,
                       ip_address=IPAddress(),
                       public_ip_address=PublicIPAddress(),
                   ),
               ],
           ),
       ),
   )
   await cluster_vm_operation.wait()
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

**JavaScript SDK**

1. Create a GPU cluster:

   ```ts theme={null}
   const gpuClusterCreateService = new GpuClusterService(sdk);
   const gpuClusterOperation =
     await gpuClusterCreateService.create(
       CreateGpuClusterRequest.create({
         metadata: ResourceMetadata.create({
           name: "<GPU_cluster_name>",
         }),
         spec: GpuClusterSpec.create({
           infinibandFabric: "<fabric>",
         }),
       }),
     ).result;
   await gpuClusterOperation.wait();
   ```

   To select the fabric, see [InfiniBand™ fabrics](https://docs.nebius.com/compute/clusters/gpu/index.md#infiniband-fabrics).

2. Create a VM:

   ```ts theme={null}
   const clusterVmService = new InstanceService(sdk);
   const clusterVmOperation = await clusterVmService.create(
     CreateInstanceRequest.create({
       metadata: ResourceMetadata.create({
         name: "<VM_name>",
       }),
       spec: InstanceSpec.create({
         resources: ResourcesSpec.create({
           platform: "<platform>",
           size: {
             $case: "preset",
             preset: "<preset>",
           },
         }),
         gpuCluster: InstanceGpuClusterSpec.create({
           id: gpuClusterId,
         }),
         bootDisk: AttachedDiskSpec.create({
           attachMode: AttachedDiskSpec_AttachMode.READ_WRITE,
           type: {
             $case: "managedDisk",
             managedDisk: ManagedDisk.create({
               name: "managed-boot-disk",
               spec: DiskSpec.create({
                 type: DiskSpec_DiskType.NETWORK_SSD,
                 source: {
                   $case: "sourceImageFamily",
                   sourceImageFamily: SourceImageFamily.create({
                     imageFamily: "ubuntu24.04-cuda13.0",
                   }),
                 },
                 size: {
                   $case: "sizeGibibytes",
                   sizeGibibytes: 40,
                 },
               }),
             }),
           },
         }),
         networkInterfaces: [
           NetworkInterfaceSpec.create({
             name: "eth0",
             subnetId,
             ipAddress: IPAddress.create({}),
             publicIpAddress: PublicIPAddress.create({}),
           }),
         ],
       }),
     }),
   ).result;
   await clusterVmOperation.wait();
   ```

   The VM is provided with a dynamic public IPv4 address.

   For more information about the code parameters, see [Create a VM](#create-a-vm).

## "Not enough resources" error

Sometimes, demand for virtual machines and GPUs in certain [Nebius AI Cloud regions](https://docs.nebius.com/overview/regions.md) might be higher than the available supply. When this happens, you might see a "Not enough resources" error when creating or restarting VMs in the affected region.

For more details, see ["Not enough resources" error for virtual machines in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/not-enough-resources.md).

## See also

* [Private and public IP addresses of Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/network.md)
* [InfiniBand™ networking for Compute virtual machines with GPUs](https://docs.nebius.com/compute/clusters/gpu/index.md)
* [Types of storage volumes in Compute](https://docs.nebius.com/compute/storage/types.md)
* [Managing Compute volumes](https://docs.nebius.com/compute/storage/manage.md)
* [Attaching and mounting Compute volumes to VMs](https://docs.nebius.com/compute/storage/use.md)

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
