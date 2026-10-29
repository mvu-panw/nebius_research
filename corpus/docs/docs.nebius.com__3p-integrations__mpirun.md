# Running parallel jobs with MPIrun

Source: https://docs.nebius.com/3p-integrations/mpirun

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running parallel jobs with MPIrun

This guide explains how to use [Open MPI](https://docs.open-mpi.org/en/v5.0.6/index.html) and [MPIrun](https://docs.open-mpi.org/en/v5.0.6/man-openmpi/man1/mpirun.1.html) to run parallel jobs on Compute virtual machines (VMs) that have GPUs and are added to a GPU cluster.

The guide uses the [NCCL tests](https://github.com/NVIDIA/nccl-tests) developed by NVIDIA® as an example of a job that you can run with MPIrun. You can also run these tests by using Slurm, or [in a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/gpu/nccl-test.md) with a node group that has a GPU cluster attached.

## Costs

Nebius AI Cloud only charges you for running the virtual machines that make up your GPU cluster. For more details, see the [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md).

## Prerequisites

1. [Create](https://docs.nebius.com/compute/clusters/gpu/index.md#how-to-enable-infiniband-for-vms-with-gpus) a GPU cluster if you don't already have one.
2. [Create virtual machines](https://docs.nebius.com/compute/virtual-machines/manage.md) and add them to the cluster.

## Steps

### Install Open MPI on each VM in the cluster

For each VM in the GPU cluster:

1. [Get the VM's private IP address](https://docs.nebius.com/compute/virtual-machines/network.md).
2. [Connect to the VM through SSH](https://docs.nebius.com/compute/virtual-machines/connect.md).
3. Install the [Open MPI](https://www.open-mpi.org/) library on the VM:

   ```bash theme={null}
   sudo apt-get install openmpi-bin
   ```

### Build the tests on one of the VMs

Choose one of the VMs as the main VM – you will run the tests from it. Build the tests on the main VM:

1. Clone the NVIDIA repository with the tests:

   ```bash theme={null}
   git clone https://github.com/NVIDIA/nccl-tests
   ```

2. Build the tests with Open MPI:

   ```bash theme={null}
   cd nccl-tests
   MPI_HOME=/usr/lib/x86_64-linux-gnu/openmpi MPI=1  make
   ```

3. Copy the built binary file, `all_reduce_perf`, to the same directory on other VMs.

### Set up SSH connectivity between the VMs in the cluster

1. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

   When generating the key pair, don't configure a passphrase.

2. Copy the generated pair, `~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub`, to the same directory on each other VM.

3. On all other VMs, add the public key from the pair to the list of authorized keys:

   ```bash theme={null}
   cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
   ```

For more details, see the [Open MPI documentation](https://docs.open-mpi.org/en/v5.0.x/launching-apps/ssh.html).

### Run the tests

Run the tests from the main VM with the `mpirun` command:

```bash theme={null}
mpirun --host <IP_address_1>:8,<IP_address_2>:8,<IP_address_3>:8,<IP_address_4>:8 \
  --allow-run-as-root -np 32 \
  -mca pml ucx \
  ~/nccl-tests/build/all_reduce_perf -b 512M -e 8G -f 2 -g 1
```

Where:

* `IP_address_[1-4]`: IP address of the VM where you want to run the test.
* `:8`: Amount of GPUs on the VM.
* `-mca pml ucx`: Instruction for MPI communications to go through InfiniBand™ by using [UCX](https://openucx.org/). To use Ethernet instead, replace the parameter with `-mca btl_tcp_if_include eth0`. This doesn't affect InfiniBand data exchanges of the test itself.
* `~/nccl-tests/build/all_reduce_perf`: A path to the binary file that should be available on all VMs.

In the result, check the average bus bandwith. If its value is higher than 300 GB/s, the connection is stable.

Example:

```
...

#       size         count      type   redop    root     time   algbw   busbw #wrong     time   algbw   busbw #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)
   536870912     134217728     float     sum      -1   3674.4  146.11  283.09      0   3648.4  147.15  285.11      0
  1073741824     268435456     float     sum      -1   6411.6  167.47  324.47      0   6416.7  167.33  324.21      0
  2147483648     536870912     float     sum      -1    12735  168.62  326.71      0    12979  165.45  320.57      0
  4294967296    1073741824     float     sum      -1    25389  169.17  327.76      0    25598  167.79  325.09      0
  8589934592    2147483648     float     sum      -1    50979  168.50  326.47      0    50799  169.10  327.63      0
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 317.11
```

The average bus bandwith is not equal to the InfiniBand™ one as some of the NCCL operations it measures use NVLink. Nevertheless, it accurately estimates the connection.

## How to delete the created resources

The virtual machines that make up your GPU cluster are chargeable. If you don't need the VMs, delete them, so Nebius AI Cloud doesn't charge for them:

**Web console**

1. In the sidebar, go to  **Compute** → **Virtual machines**.
2. On the **Standalone VMs** tab, next to the virtual machine's name, click  → **Delete**.
3. Enter the VM name and confirm deletion.

**CLI**

Run the following command to delete the VM:

```bash theme={null}
nebius compute instance delete --id <VM_ID>
```

If you only know the name of the VM, run the following command:

```bash theme={null}
nebius compute instance delete --id \
  $(nebius compute instance get-by-name \
    --name=<VM_name> \
    --format jsonpath='{.metadata.id}')
```

If you don't know either the name or the ID of the VM, you can list all VMs in your project:

```bash theme={null}
nebius compute instance list
```

In the output, find the VM you need and get its ID, then use it in the deletion command.

***

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
