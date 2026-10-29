# How to monitor job and node statuses in a Soperator cluster

Source: https://docs.nebius.com/slurm-soperator/monitoring/statuses

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to monitor job and node statuses in a Soperator cluster

In a Soperator cluster, Slurm nodes run as Kubernetes® Pods. You can monitor the nodes by using Slurm commands, which are listed in a [cheat sheet](https://github.com/nebius/nebius-solution-library/blob/main/docs/SLURM-Quick-reference.pdf).

For more information about monitoring an underlying Kubernetes cluster, see [Managed Service for Kubernetes® documentation](https://docs.nebius.com/kubernetes/monitoring.md).

To run the monitoring commands, [connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes).

## Cluster status

To list current worker nodes, run the following command:

```bash theme={null}
sinfo -Nel
```

This command returns a list of detailed information about the nodes. For more information about other parameters available for `sinfo`, see [Slurm documentation](https://slurm.schedmd.com/sinfo.html#SECTION_OPTIONS).

Output example:

```text theme={null}
NODELIST   NODES   PARTITION   STATE CPUS   S:C:T    MEMORY   TMP_DISK   WEIGHT   AVAIL_FE   REASON
worker-0       1       main*     idle 128   2:32:2   155340          0        1     (null)     none
worker-1       1       main*     idle 128   2:32:2   155340          0        1     (null)     none
```

Only worker nodes are listed in this view. If the node state has an asterisk next to it, for example, `idle*`, this means that the node did not respond and it is unavailable. The node goes `down` if it does not respond quickly. For more information about common node states, see [Node states](#node-states).

You can customize the columns in the `sinfo` output by using the `-o` parameter. For example, `sinfo -o "%20P %5D %14F %8z %10m %10d %11l %16f %N"` lists the partitions, gives you the total number of nodes and shows which nodes are free, how much memory is available and the time limits for jobs currently being executed. For more information about these parameters, see [Slurm documentation](https://slurm.schedmd.com/sinfo.html#OPT_format).

To get more information about a particular node, run the following command:

```bash theme={null}
scontrol show node <node_name>
```

### Node states

Some of the common node states include:

| Node state | Description | State causes |
| - | - | - |
| `idle` | The node is not currently running any jobs and is available for scheduling. | No jobs assigned yet. |
| `allocated` | The node is actively running one or more jobs. | A job has been assigned and is executing. |
| `mixed` | Some CPUs on the node are allocated to jobs, while others remain idle. | Partial job allocations. |
| `down` | The node is unavailable for use. | Hardware failure, maintenance or manual marking by an admin. |
| `drained` | The node is excluded from the scheduling pool for new jobs. Jobs submitted before the node was drained may run to completion. | Marked for draining manually or by Soperator health checks. |
| `unknown` | The node state cannot be determined. | Communication issues between the controller and the node. |
| `fail` | The node has failed and cannot execute jobs. | Critical hardware or software issues. |

For a complete list of all possible node states, see [Slurm documentation](https://slurm.schedmd.com/sinfo.html#SECTION_NODE-STATE-CODES).

### How to drain and resume a node

To drain a node (that is, stop scheduling more jobs and make the node unavailable), run the following command:

```bash theme={null}
scontrol update NodeName=<node_name> State=drain Reason="<reason>"
```

To resume a node that was drained, run the following command:

```bash theme={null}
scontrol update NodeName=<node_name> State=resume
```

## Job queue

To list all jobs currently running or pending (that is, waiting for resources), run the following command:

```bash theme={null}
squeue -a
```

To list all jobs currently running, run the following command:

```bash theme={null}
squeue -tR
```

Output example:

```text theme={null}
JOBID   PARTITION   NAME   USER        ST   TIME   NODES   NODELIST(REASON)
  116        main   nccl   test-user    R   0:17       1           worker-1
```

For pending jobs with the `PD` status, the `NODELIST(REASON)` column shows the reason why the job is pending. For more information about possible reasons for this status, see [Slurm documentation](https://slurm.schedmd.com/squeue.html#SECTION_JOB-REASON-CODES).

### Job details

To use the job ID to get more details about the job, run the following command:

```bash theme={null}
scontrol show job <job_ID>
```

### Completed job statistics

To get the details about the jobs already completed, run the following command:

```bash theme={null}
sacct -a
```

Output example:

```text theme={null}
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode
------------ ---------- ---------- ---------- ---------- ---------- --------
24            nccl_test       main       root         16  COMPLETED      0:0
24.0          nccl_test                  root         16  COMPLETED      0:0
```

For more information about additional parameters available for `sacct`, see [Slurm documentation](https://slurm.schedmd.com/sacct.html#SECTION_OPTIONS).
