# Viewing logs of Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/monitoring/logs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Viewing logs of Soperator clusters

You can view logs of your Soperator cluster either [in a browser](#how-to-view-logs-in-a-browser) or directly [on the worker nodes](#how-to-view-log-files-on-a-worker-node).

## Prerequisites

1. [Connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md) to your cluster. You should see the SSH welcome message. For example:

   ```
   Welcome to Soperator cluster

   ...

   System information as of Thu May  8 10:43:02 UTC 2025:
   ...

   Slurm nodes:
     PARTITION   CPUS   MEMORY    GRES                                 NODES   NODELIST                  STATE   REASON
     main        128    1553408   gpu:nvidia_h100_80gb_hbm3:8(S:0-1)   2       worker-[0-1]              idle    none

   ...

   To open logs explorer in your browser:
     1. Execute this command on your local computer:
        `ssh -L 9428:vm-logs-victoria-logs-single-server.logs-system.svc:9428 -N <username>@<public_IP_address>`
     2. Open `localhost:9428/select/vmui` in your browser
   ...
   ```

2. Get the command to open monitoring dashboards from the instructions in the SSH welcome message. In the example above, it is `ssh -L 9428:vm-logs-victoria-logs-single-server.logs-system.svc:9428 -N <username>@<public_IP_address>`. The URL for your cluster might be different.

## How to view logs in a browser

1. On your local machine, run the command to open logs explorer that you got from the SSH welcome message. For example:

   ```bash theme={null}
   ssh -L 9428:vm-logs-victoria-logs-single-server.logs-system.svc:9428 -N <username>@<public_IP_address>
   ```

   In this command, specify the `username` and `public_IP_address` that you use to [connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md) to the cluster.

2. Open `localhost:9428/select/vmui` in your browser.

3. Explore the logs. You can use the [LogsQL](https://docs.victoriametrics.com/victorialogs/logsql/) language to write queries that filter the logs you want to review. For example:

   * Logs of the Slurm daemon that runs on the `worker-0` node:

     ```
     k8s.container.name: "slurmd" AND k8s.pod.name: "worker-0"
     ```

   * Logs of all Slurm controllers:

     ```
     kubernetes.container_name: "slurmctld"
     ```

   * Logs of Slurm daemons and controllers that relate to the job with the ID `123`:

     ```
     k8s.container.name: ~"slurmctld|slurmd" AND 123
     ```

   * Logs of the SSH daemon that runs on the `login-0` node:

     ```
     k8s.container.name: "sshd" AND k8s.pod.name: "login-0"
     ```

   * Errors in logs of Slurm daemons and controllers:

     ```
     k8s.container.name: ~"slurmctld|slurmd" AND "error"
     ```

## How to view log files on a worker node

1. [Connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-worker-nodes) to a worker node of your Soperator cluster.
2. View the logs of the Slurm daemon that runs on this node:

   ```bash theme={null}
   less /var/log/slurm/slurmd.log
   ```
