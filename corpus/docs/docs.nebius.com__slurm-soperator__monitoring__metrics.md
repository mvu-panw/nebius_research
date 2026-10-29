# Monitoring metrics of Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/monitoring/metrics

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoring metrics of Soperator clusters

You can monitor the performance of your Soperator cluster on preconfigured dashboards in Grafana®.

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

   No user jobs in the queue

   No other users are currently logged in

   To open monitoring dashboards in your browser:
     1. Execute this command on your local computer:
        `ssh -L 3000:metrics-grafana.monitoring-system.svc:80 -N <username>@<public_IP_address>`
     2. Open `localhost:3000` in your browser
   ...
   ```

2. Get the command to open monitoring dashboards from the instructions in the SSH welcome message. In the example above, it is `ssh -L 3000:metrics-grafana.monitoring-system.svc:80 -N <username>@<public_IP_address>`. The URL for your cluster might be different.

## How to view metrics in Grafana

1. On your local machine, run the command to open monitoring dashboards that you got from the SSH welcome message. For example:

   ```bash theme={null}
   ssh -L 3000:metrics-grafana.monitoring-system.svc:80 -N <username>@<public_IP_address>
   ```

   In this command, specify the `username` and `public_IP_address` that you use to [connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md) to the cluster. Optionally, change port `3000` if it is already in use on your local machine.

2. Open `localhost:3000` (or `localhost:<port>`) in your browser.

3. In the sidebar, select **Dashboards**. Review the metrics on these dashboards. For example, you can see the metrics of Slurm jobs and resource allocations.

## How to view metrics for worker nodes

The nodes of your Soperator cluster are Compute virtual machines. You can view their metrics on Monitoring [dashboards in the web console](https://docs.nebius.com/compute/monitoring/virtual-machines.md#explore-the-dashboard).

To find out the ID of the virtual machine for a worker node:

1. [Connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) to a login node of your Soperator cluster.

2. Run the following command:

   ```bash theme={null}
   scontrol show node worker-<number>
   ```

   Output example:

   ```bash theme={null}
   NodeName=worker-0 Arch=x86_64 CoresPerSocket=32
      CPUAlloc=0 CPUEfctv=128 CPUTot=128 CPULoad=0.97
      AvailableFeatures=(null)
      ActiveFeatures=(null)
      Gres=gpu:nvidia_h100_80gb_hbm3:8(S:0-1)
      NodeAddr=10.0.35.138 NodeHostName=worker-0 Version=24.05.5
      OS=Linux 5.15.0-133-generic #144-Ubuntu SMP Fri Feb 7 20:47:38 UTC 2025
      RealMemory=1553408 AllocMem=0 FreeMem=1421003 Sockets=2 Boards=1
      State=IDLE+DYNAMIC_NORM ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
      Partitions=main
      BootTime=2025-03-11T11:28:45 SlurmdStartTime=2025-03-11T12:39:23
      LastBusyTime=2025-05-08T13:42:21 ResumeAfterTime=None
      CfgTRES=cpu=128,mem=1517G,billing=128
      AllocTRES=
      CurrentWatts=0 AveWatts=0

      Extra={ "monitoring": "https://console.eu.nebius.com/project-e00x6706bdmd42yjyn/compute/instances/computeinstance-****/monitoring" }
      InstanceId=computeinstance-****
   ```

   Get the link from the `monitoring` parameter.

3. Open the link in your browser. There, you can view the dashboards for the virtual machine that runs the worker node.

***

*The Grafana Labs Marks are trademarks of Grafana Labs, and are used with Grafana Labs' permission. We are not affiliated with, endorsed or sponsored by Grafana Labs or its affiliates.*
