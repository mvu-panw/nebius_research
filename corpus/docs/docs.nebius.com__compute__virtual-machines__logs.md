# How to collect diagnostic logs from Compute virtual machines

Source: https://docs.nebius.com/compute/virtual-machines/logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to collect diagnostic logs from Compute virtual machines

*Diagnostic logs* from Compute virtual machines (VMs) help you troubleshoot issues with VM operations, networking and workloads.

We strongly recommend collecting logs while the issue is still occurring, because they capture more information about the broken state than logs collected after the issue has been resolved.

## Types of logs

This guide describes how to collect the following types of logs for troubleshooting:

* GPU logs: `nvidia-bug-report.sh`.
* General system logs, including more context about system services and package versions: `sos report`.
* [NVIDIA® Mellanox®](https://www.nvidia.com/en-us/networking/management-software/) adapter (InfiniBand™/NVSwitch/Ethernet) logs: `sysinfo-snapshot`.

## Prerequisites

Make sure that you have configured [SSH access to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md).

## How to collect logs

1. [Connect to the VM by using SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

2. Generate GPU logs:

   ```bash theme={null}
   sudo nvidia-bug-report.sh
   ```

   This command usually runs for about five minutes and generates `nvidia-bug-report.log.gz` in the current working directory.

   If the command stops responding, run it in safe mode:

   ```bash theme={null}
   sudo nvidia-bug-report.sh --safe-mode
   ```

3. If you need more system information, generate general system logs:

   ```bash theme={null}
   sudo sos report --batch
   ```

   This command generates an archive in the following format: `/tmp/sosreport-<VM_ID>-<date>-<random_ID>.tar.gz`.

4. If you are troubleshooting Mellanox adapter issues, generate Mellanox adapter logs:

   ```bash theme={null}
   sudo /opt/nebius/sysinfo-snapshot
   ```

   This command generates an archive in the following format: `/tmp/sysinfo-snapshot-<VM_ID>-<date>-<random_ID>.tgz`.

## How to get generated log files

1. Check that the files were generated on your VM by running the following commands:

   * To check for GPU logs:

     ```bash theme={null}
     ls nvidia-bug-report.log.gz
     ```

   * To check for general system logs or Mellanox adapter logs:

     ```bash theme={null}
     ls /tmp
     ```

2. From your local shell, run the following command to copy the files from the VM to the current directory:

   ```bash theme={null}
   scp -i ~/.ssh/id_ed25519 <username>@<public_IP_address>:<remote_file_path> .
   ```

   In the command, specify the path to the generated file on the VM, for example: `nvidia-bug-report.log.gz`, `/tmp/sosreport-*.tar.gz` or `/tmp/sysinfo-snapshot-*.tgz`.

   If copying files from the `/tmp` directory fails due to a permission error, this usually means the generated file is owned by root. To fix this issue, proceed to the next step.

3. [Reconnect to the VM](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh) and set permissions to grant read access to non-root users. After that, you can rerun the `scp` command.

   > [!NOTE]
   >
   > If you successfully copied the generated log file, skip this step.

   ```bash theme={null}
   sudo chmod 644 <remote_file_path>
   ```

   In the command, set the `remote_file_path` to `/tmp/sosreport-*.tar.gz` or `/tmp/sysinfo-snapshot-*.tgz`.

4. Find the copied log files in your local directory.

## See also

* [How to inspect a VM and attach its boot disk to another VM](https://docs.nebius.com/compute/virtual-machines/inspect-boot-disk.md)
* [Support tickets: sending questions, bug reports and feature requests](https://docs.nebius.com/overview/support.md)

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
