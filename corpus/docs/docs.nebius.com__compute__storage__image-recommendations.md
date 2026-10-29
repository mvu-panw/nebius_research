# Recommendations for configuring custom images in Compute

Source: https://docs.nebius.com/compute/storage/image-recommendations

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Recommendations for configuring custom images in Compute

If you work with [custom images](https://docs.nebius.com/compute/storage/custom-disk-images.md), we recommend optimizing them so your boot disks and virtual machines (VMs) work with higher productivity and speed. When you create a VM based on a custom image, this VM doesn't include some of the settings that a VM based on a public image includes. You can add these settings to your custom-image VM and optimize it.

The additional settings aren't required for every custom image, but we recommend them for at least production-oriented images unless you have workload-specific reasons for not using these settings.

## Install the monitoring agent by Nebius AI Cloud

The [monitoring agent](https://docs.nebius.com/observability/agents/monitoring-agent.md) is installed by default on VMs with public images. If you use a custom image, install the agent to collect and view [metrics for the VM](https://docs.nebius.com/compute/monitoring/virtual-machines.md).

To install the monitoring agent, [connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) and then run the following commands:

```bash theme={null}
sudo curl https://dr.nebius.cloud/public.gpg -o /etc/apt/keyrings/nebius-public.gpg.pub

echo deb [signed-by=/etc/apt/keyrings/nebius-public.gpg.pub] https://dr.nebius.cloud/ stable main | sudo tee /etc/apt/sources.list.d/nebius-public.list

sudo apt-get update
sudo apt-get install -y nebius-observability-agent nebius-observability-agent-updater
```

## Collect serial logs

To collect and view [serial logs](https://docs.nebius.com/compute/monitoring/serial-logs.md) of a VM on a custom image, configure the VM's [GRUB](https://en.wikipedia.org/wiki/GNU_GRUB) to initialize and use a serial port. GRUB is a boot loader package that boots an operating system and kernel configuration.

To configure GRUB for Ubuntu-based disk images:

1. [Connect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

2. In the `/etc/default/grub` file, add the following line:

   ```text theme={null}
   GRUB_CMDLINE_LINUX="console=tty1 console=ttyS0"
   ```

3. Update GRUB:

   ```bash theme={null}
   update-grub
   ```

4. Reboot the VM: disconnect from it, and [stop and start it](https://docs.nebius.com/compute/virtual-machines/stop-start.md#how-to-stop-and-start-vms-manually).

## Change sysctl settings

Apply the recommended `sysctl` settings to improve the networking and kernel characteristics of the VM. To do so, connect to the VM and update the following settings in two files:

* File `/etc/sysctl.d/30-network.conf`

  ```text theme={null}
  # Decrease default tcp keepalive time
  net.ipv4.tcp_keepalive_time = 120
  net.ipv4.tcp_keepalive_intvl = 60
  net.ipv4.tcp_keepalive_probes = 4
  # Make conntrack more liberal to tcp out of window packets to prevent
  # spurious connection resets when masquerading is in use
  net.netfilter.nf_conntrack_tcp_be_liberal = 1
  ```

* File `/etc/sysctl.d/90-kernel.conf`

  ```text theme={null}
  kernel.panic = 10
  kernel.printk = 7 4 1 7
  ```

## Adjust the virtiofs settings

To speed up reading from volumes and writing to them, adjust the `virtiofs` settings. Connect to the VM and run the Bash script below. The script increases the `read_ahead_kb` value to improve the performance of the VM volumes.

```bash theme={null}
#!/usr/bin/env bash
set -euo pipefail

install -d /usr/local/bin
install -d /etc/udev/rules.d

cat > /usr/local/bin/tune_virtiofs_bdi.sh <<'EOF'
#!/usr/bin/env bash

kernel="${1:-}"

while read -r dev on mp type fs opts; do
    dev=$(/bin/mountpoint -d "$mp")
    if [[ "$fs" == "virtiofs" ]]; then
        if [[ "$kernel" == "$dev" ]]; then
            exit 0
        fi
    fi
done < <(mount | grep virtiofs)

exit 1
EOF

chmod +x /usr/local/bin/tune_virtiofs_bdi.sh

cat > /etc/udev/rules.d/99-virtiofs.rules <<'EOF'
SUBSYSTEM=="bdi", ACTION=="add", PROGRAM="/usr/local/bin/tune_virtiofs_bdi.sh $kernel", ATTR{read_ahead_kb}="8192"
EOF
```

## Enable failure reporting by using pvpanic

The `pvpanic` tool allows the guest OS kernel to report panic and crash events to the hypervisor. This helps with failure detection and troubleshooting.

To start using `pvpanic` on Ubuntu, connect to the VM and install the package:

```bash theme={null}
sudo apt-get install -y linux-image-generic
```
