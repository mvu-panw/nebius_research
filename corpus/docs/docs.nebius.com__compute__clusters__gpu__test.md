# How to test a GPU cluster physical state in Compute

Source: https://docs.nebius.com/compute/clusters/gpu/test

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to test a GPU cluster physical state in Compute

In this article, you will learn how to test the physical state of the InfiniBand™ connection.

The guides below will help you to check that  InfiniBand connections are established between GPUs in a GPU cluster.

## Testing the port state

1. [Connect to the VM using SSH](https://docs.nebius.com/compute/virtual-machines/connect.md).

2. In the VM's shell, run `ibstatus` command that displays operational information about InfiniBand network devices.

   Result:

   ```bash theme={null}
   Infiniband device 'mlx5_0' port 1 status:
      default gid:    fe80:0000:0000:0000:****:****:****:03c5
      base lid:    0x***
      sm lid:      0x*
      state:       4: ACTIVE
      phys state:  5: LinkUp
      rate:     400 Gb/sec (4X NDR)
      link_layer:  InfiniBand

   Infiniband device 'mlx5_1' port 1 status:
      default gid:    fe80:0000:0000:0000:****:****:****:03c6
      base lid:    0x***
      sm lid:      0x*
      state:       4: ACTIVE
      phys state:  5: LinkUp
      rate:     400 Gb/sec (4X NDR)
      link_layer:  InfiniBand
   ...
   ```

3. For each device in the result, check the physical state (`phys state`): it should be `LinkUp`.

## Testing network performance

You can also emulate the network activity by sending some data from GPUs on one VM to GPUs on another:

1. Install the [perftest](https://github.com/linux-rdma/perftest) package on each one of the test VMs:

   ```bash theme={null}
   sudo apt install perftest
   ```

2. [Connect to the first VM using SSH](https://docs.nebius.com/compute/virtual-machines/connect.md).

3. Run `ib_send_bw --report_gbits`.

4. Copy the first VM's [private IP address](https://docs.nebius.com/compute/virtual-machines/network.md).

5. [Connect to the second VM using SSH](https://docs.nebius.com/compute/virtual-machines/connect.md).

6. Run `ib_send_bw <first_VM_IP_address> --report_gbits`.

In the commands output, you should see non-zero values for the bytes sent, average bandwith speed, and average message rate. The bandwidth peak speed might not reach the theoretical maximum 400 Gbps.

Example:

```text theme={null}
+--------------------------------------------------------------------------------+
| #bytes   #iterations   #BW peak[Gb/sec]   #BW average[Gb/sec]   #MsgRate[Mpps] |
+--------------------------------------------------------------------------------+
| 65536    1000          360.39             359.91                0.686466       |
+--------------------------------------------------------------------------------+
```

## See also

* [InfiniBand™ networking for Compute virtual machines with GPUs](https://docs.nebius.com/compute/clusters/gpu/index.md)
* [How to create a virtual machine in Nebius AI Cloud](https://docs.nebius.com/compute/virtual-machines/manage.md)

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
