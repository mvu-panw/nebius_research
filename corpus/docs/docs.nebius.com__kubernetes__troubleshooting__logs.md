# How to collect diagnostic logs from Managed Service for Kubernetes® nodes

Source: https://docs.nebius.com/kubernetes/troubleshooting/logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to collect diagnostic logs from Managed Service for Kubernetes® nodes

Managed Service for Kubernetes [nodes](https://docs.nebius.com/kubernetes/components.md#node) are Compute virtual machines (VMs). *Diagnostic logs* from Managed Kubernetes nodes help you troubleshoot issues with VM operations, networking and workloads.

The procedure for collecting diagnostic logs depends on the GPU and access settings you configured when you [created the node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#regular-node-groups). We strongly recommend collecting logs while the issue is still occurring, because they capture more information about the broken state than logs collected after the issue has been resolved.

Determine which of the following cases applies to your environment, and follow the relevant procedure:

* Nodes that have one or more GPUs, without SSH configuration: [connect to the cluster with kubectl to start a debug session](#how-to-collect-logs-by-using-kubectl).
* Nodes that have one or more GPUs, with SSH configuration: [connect to the node with SSH to collect logs](#how-to-collect-logs-by-using-ssh).
* Nodes without GPUs: [contact our support team](#how-to-request-log-collection-from-support).

## Types of logs

This guide describes how to collect the following types of logs for troubleshooting:

* GPU logs: `nvidia-bug-report.sh`.
* General system logs, including more context about system services and package versions: `sos report`.
* [NVIDIA® Mellanox®](https://www.nvidia.com/en-us/networking/management-software/) adapter (InfiniBand™/NVSwitch/Ethernet) logs: `sysinfo-snapshot`.

## How to collect logs by using kubectl

If your nodes have GPUs and you have `kubectl` access to the cluster, but no SSH access to the nodes, do the following to collect the logs:

1. Connect to the cluster with [kubectl](https://docs.nebius.com/kubernetes/connect.md).

2. Start a debugging session for the required node and open an interactive shell in the debug container:

   ```bash theme={null}
   kubectl debug node/<node_ID> -it --image ubuntu --profile sysadmin -- bash
   ```

   In the command, specify:

   * `node_ID`: The node to debug. To get the nodes in the cluster, run:

     ```bash theme={null}
     kubectl get nodes
     ```

     Alternatively, in the [web console](https://console.nebius.com/), go to  **Compute** → **Virtual machines**. On the **Kubernetes nodes** tab, click  next to the node ID to copy it.

   * `--image`: Container image to use for the debug container. We recommend setting it to `ubuntu` to start a temporary debug container.

   * `--profile`: Set to `sysadmin` to use the built-in debugging profile. Refer to the [Kubernetes documentation](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_debug/) for more information.

   * `-it`: Starts an interactive terminal session in the debug container.

   * `bash`: Starts the Bash shell in the debug container.

   In the output, note the name of the temporary debug Pod that was created. You will need it in a later step.

3. Switch to the host filesystem:

   ```bash theme={null}
   chroot /host
   ```

4. Generate GPU logs:

   ```bash theme={null}
   nvidia-bug-report.sh
   ```

   This command usually runs for about five minutes and generates `nvidia-bug-report.log.gz` in the current working directory.

   If the command stops responding, run it in safe mode:

   ```bash theme={null}
   nvidia-bug-report.sh --safe-mode
   ```

5. If you need more system information, generate general system logs:

   ```bash theme={null}
   sos report --batch
   ```

   This command generates an archive in the following format: `/tmp/sosreport-<node_ID>-<date>-<random_ID>.tar.gz`.

6. If you are troubleshooting Mellanox adapter issues, generate Mellanox adapter logs:

   ```bash theme={null}
   /opt/nebius/sysinfo-snapshot
   ```

   This command generates an archive in the following format: `/tmp/sysinfo-snapshot-<node_ID>-<date>-<random_ID>.tgz`.

7. From your local shell, copy the generated log file(s) from the debug Pod:

   > [!WARNING]
   >
   > Don't exit the shell. This will terminate the debug Pod, and you will not be able to copy files from it. Instead, open a new terminal to run the `kubectl cp` command.

   ```bash theme={null}
   kubectl cp <debug_Pod_name>:/host/<generated_file_path> ./<local_file_name>
   ```

   In the command, specify:

   * `debug_Pod_name`: The name of the temporary debug Pod created when you ran `kubectl debug`.
   * `generated_file_path`: The path to the generated log file on the node, for example, `/tmp/sosreport-*.tar.gz`.
   * `local_file_name`: The name to save the file as on your local machine, for example, `/tmp/sosreport.tar.gz`.

## How to collect logs by using SSH

If your nodes have GPUs, and you have configured SSH access, do the following to collect the logs:

1. Connect to the node over SSH. Nodes are Compute VMs, therefore, you connect the same way you would [connect to a VM by using SSH](https://docs.nebius.com/compute/virtual-machines/connect.md#connect-to-the-vm-by-using-ssh).

2. Generate the logs as described in [How to collect logs](https://docs.nebius.com/compute/virtual-machines/logs.md#how-to-collect-logs).

3. Retrieve the generated log files as described in [How to get generated log files](https://docs.nebius.com/compute/virtual-machines/logs.md#how-to-get-generated-log-files).

## How to request log collection from support

If your nodes don't have GPUs, [create a support ticket](https://docs.nebius.com/overview/support.md) to get assistance with troubleshooting.

When you create the ticket, write that you give the support team explicit permission to access your logs.

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
