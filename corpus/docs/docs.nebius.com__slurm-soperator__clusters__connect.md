# Connecting to login and worker nodes

Source: https://docs.nebius.com/slurm-soperator/clusters/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Connecting to login and worker nodes

In Soperator clusters, all Slurm nodes are Kubernetes Pods. The main [types of Slurm nodes](https://slurm.schedmd.com/quickstart_admin.html#nodes) in Soperator clusters are the following:

* [Login nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#login-node) provide users with access to the cluster.
* [Worker nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#worker-node) execute Slurm jobs.
* [Controller nodes](https://docs.nebius.com/slurm-soperator/overview/architecture.md#controller-node) manage scheduling and orchestration.

You can connect to login and worker nodes.

## Prerequisites

Before you connect to nodes of a Soperator cluster for the first time, make sure that the following requirements are met:

1. [Get the public endpoint of the cluster](#get-the-public-endpoint-of-the-cluster).
2. [Create a user account](#create-a-user-account).
3. [(Optional) Establish a connection in Visual Studio Code](#optional-establish-a-connection-in-visual-studio-code).

### Get the public endpoint of the cluster

If you deployed the cluster in Managed Service for Soperator yourself, get the endpoint in the [web console](https://console.nebius.com):

1. In the sidebar, go to  **AI orchestration** → **Soperator**.
2. Under **General**, copy the public endpoint.

If you are using the Pro Solution for Soperator, get the endpoint from your personal manager.

### Create a user account

Contact the cluster administrator (the `root` user) to [create a user](https://docs.nebius.com/slurm-soperator/users/manage.md#how-to-create-a-user) for you. [Generate an SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md) and share your public SSH key with the administrator.

### (Optional) Establish a connection in Visual Studio Code

If you want to establish a connection in [Visual Studio Code](https://code.visualstudio.com/), do the following:

1. Install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension.
2. Open your `~/.ssh/config` file and add the following configuration:

   ```bash theme={null}
   Host slurm
     HostName <public_IP_address>
     User <username>
     IdentityFile ~/slurm_ed25519
   ```

## How to connect to login nodes

Connect to a login node, so you can run Slurm commands and manage data stored on the shared filesystem.

**Terminal**

By default, if a cluster has several login nodes, you connect to a random login node:

```bash theme={null}
ssh <username>@<public_endpoint> -i <path_to_private_key>
```

If you are working in the terminal, you can choose which login node to connect to.

> [!NOTE]
>
> If you use the [tmux](https://en.wikipedia.org/wiki/Tmux) terminal multiplexer, make sure to connect to the same node each time. `tmux` sessions are created on the node where they are started, so you can only access them on this node.

To connect to a particular login node, use the cluster public endpoint as a jump host and the name of the required node.

```bash theme={null}
ssh -J <username>@<public_endpoint> <username>@login-<number> -i <path_to_private_key>
```

Specify the parameters that were set during the user creation:

* Username. The administrator has the `root` username.
* Path to the private key.
* Exact name of the node you need to connect to, if you are connecting to a specific node (`login-<number>`). You can get the list of login nodes in your cluster from your personal manager.

Output example:

```text theme={null}
username@login-0:~$
```

Now, you can run Slurm commands, for example, `sinfo` to get a list of available Slurm nodes.

**VS Code**

To establish a connection, in VS Code, click  → **Connect to Host...** → **slurm**.

The configuration already includes your username and the cluster endpoint, so you do not need to enter them to connect.

Now, you can view and manage data in your cluster by using the VS Code interface.

## How to connect to worker nodes

Connect to a worker node, so you can monitor, observe and manage Slurm jobs. You can only connect to a specific worker node.

To establish a connection, do the following:

1. From your personal manager, get a list of worker nodes in your cluster. Usually, worker nodes are named as `worker-0`, `worker-1`, `worker-2`, depending on how many exist.
2. [Connect to a login node by using a terminal](#how-to-connect-to-login-nodes).
3. Connect to a specific worker node:

   ```bash theme={null}
   ssh worker-<number>
   ```

   For example, if you have `worker-0` and `worker-1`, specify one of these nodes.

   Output example:

   ```text theme={null}
   username@worker-0:~$
   ```

Now, you can [monitor system usage](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md) with various tools, such as `htop`, `nvtop` or `nvidia-smi`.

If you are working in the terminal, you can connect to a worker node directly by using the cluster public endpoint as a jump host and then connecting to the specific node by name.

**Terminal**

```bash theme={null}
ssh -J <username>@<public_endpoint> <username>@worker-<number> -i <path_to_private_key>
```

Enter the exact name of the node you need to connect to. In addition, specify the parameters that were set during the user creation:

* Username. The administrator has the `root` username.
* Path to the private key.

Output example:

```text theme={null}
username@worker-0:~$
```
