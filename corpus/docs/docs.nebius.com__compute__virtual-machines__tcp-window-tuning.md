# Tuning TCP window sizes on Linux virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/tcp-window-tuning

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Tuning TCP window sizes on Linux virtual machines

TCP throughput depends on how much unacknowledged data a sender and receiver can keep in flight. On long-distance or high-latency connections, the default Linux TCP buffer limits can constrain a single flow before the network link is saturated.

This article shows how to increase TCP receive and send window limits on a Linux virtual machine (VM) in Nebius AI Cloud.

Use this tuning if your workload transfers large amounts of data over connections with both:

* High bandwidth
* Noticeable round-trip latency

Typical examples include:

* Cross-region replication
* Large model or dataset transfers
* Long-lived TCP sessions that need higher per-flow throughput

If your traffic is short-lived, latency-sensitive, or limited by the application rather than the network path, this tuning may have little effect.

## Recommended values

The following settings increase the maximum TCP buffer sizes while keeping default behavior unchanged:

```text theme={null}
net.ipv4.tcp_rmem = 4096 131072 268435456
net.ipv4.tcp_wmem = 4096 16384 268435456
net.core.rmem_max = 536870912
net.core.wmem_max = 536870912
net.ipv4.tcp_adv_win_scale = 1
```

These values keep the minimum and default TCP buffer settings close to the Linux defaults, while increasing the maximum values for high-bandwidth links.

The recommended maximum TCP window targets a single flow of about 3 Gbit/s over a 300 ms round-trip-time path. That bandwidth-delay product is about 108 MB, which is rounded up to 128 MiB and then doubled to account for the effect of `net.ipv4.tcp_adv_win_scale=1`.

> [!WARNING]
>
> Larger TCP buffers can increase memory consumption under heavy connection fan-out. Verify available memory before applying this tuning on smaller VMs or on hosts with many simultaneous high-throughput flows.

## How to tune TCP window sizes

### Prerequisites

Make sure that:

1. The VM runs Linux.
2. You can connect to the VM by using SSH. For more information, see [How to connect to virtual machines in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/connect.md).
3. You have `sudo` privileges on the VM.

### Apply the changes

1. Connect to the VM:

   ```bash theme={null}
   ssh <username>@<VM_IP_address>
   ```

2. Create a sysctl configuration file:

   ```bash theme={null}
   sudo tee /etc/sysctl.d/90-nebius-tcp-window.conf >/dev/null <<'EOF'
   net.ipv4.tcp_rmem = 4096 131072 268435456
   net.ipv4.tcp_wmem = 4096 16384 268435456
   net.core.rmem_max = 536870912
   net.core.wmem_max = 536870912
   net.ipv4.tcp_adv_win_scale = 1
   EOF
   ```

3. Apply the configuration:

   ```bash theme={null}
   sudo sysctl --system
   ```

### Verify the configuration

Check that the VM reports the configured values:

```bash theme={null}
sysctl \
  net.ipv4.tcp_rmem \
  net.ipv4.tcp_wmem \
  net.core.rmem_max \
  net.core.wmem_max \
  net.ipv4.tcp_adv_win_scale
```

Expected output:

```text theme={null}
net.ipv4.tcp_rmem = 4096 131072 268435456
net.ipv4.tcp_wmem = 4096 16384 268435456
net.core.rmem_max = 536870912
net.core.wmem_max = 536870912
net.ipv4.tcp_adv_win_scale = 1
```

If your application still does not reach the expected throughput, check the end-to-end path for other limits such as application-level buffer sizing, rate limiting, packet loss or congestion on the remote side.

### Roll back the changes

To remove the configuration:

```bash theme={null}
sudo rm /etc/sysctl.d/90-nebius-tcp-window.conf
sudo sysctl --system
```

After rollback, the VM uses the remaining sysctl configuration from the operating system image and any other files in `/etc/sysctl.d`.
