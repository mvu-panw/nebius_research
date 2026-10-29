# Managing jobs in Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/jobs/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing jobs in Soperator clusters

You can use Slurm commands to view and manage jobs in your Soperator cluster. To run these commands, [connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) to the cluster's login node.

## How to view job list and details

### Jobs in queue

To list all jobs that are currently in the queue, use the [squeue](https://slurm.schedmd.com/squeue.html) command. You can use various parameters to specify the output format:

* `--long` to include more details. For example:

  ```bash theme={null}
  squeue --long
  ```

  Output example:

  ```bash theme={null}
  JOBID PARTITION     NAME     USER    STATE       TIME TIME_LIMI  NODES NODELIST(REASON)
    837      main test-job     user  RUNNING       0:11 UNLIMITED      2 worker-[0-1]
  ```

* `--Format` to customize output columns and their width. For example:

  ```bash theme={null}
  squeue --Format "JobID:8,Partition:10,Name,UserName,State:16,TimeUsed:8,NumNodes:6,ReasonList"
  ```

  Output example:

  ```bash theme={null}
  JOBID   PARTITION NAME             USER            STATE           TIME    NODES NODELIST(REASON)
  837     main      test-job         user            RUNNING         0:05    2     worker-[0-1]
  ```

* `--steps` to show job steps, that is, sets of tasks within a job. For example:

  ```bash theme={null}
  squeue --steps
  ```

  Output example:

  ```bash theme={null}
  Tue Apr 29 16:23:39 2025
           STEPID     NAME PARTITION   USER      TIME NODELIST
            837.0     test      main   user      1:26 worker-[0-1]
        837.batch    batch      main   user      1:27 worker-1
  ```

### All jobs

The `squeue` command doesn't list completed or failed jobs. To get the full details of all recently run jobs, use the [scontrol](https://slurm.schedmd.com/scontrol.html) command:

```bash theme={null}
scontrol show jobs | less
```

Output example:

```bash theme={null}
JobId=<job_ID> JobName=<job_name>
   UserId=<user>(1001) GroupId=<user_group>(1001) MCS_label=N/A
   Priority=1 Nice=0 Account=(null) QOS=normal
   JobState=RUNNING Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=00:00:38 TimeLimit=UNLIMITED TimeMin=N/A
   SubmitTime=2025-04-30T15:51:21 EligibleTime=2025-04-30T15:51:21
   AccrueTime=2025-04-30T15:51:21
   StartTime=2025-04-30T15:51:21 EndTime=Unknown Deadline=N/A
   PreemptEligibleTime=2025-04-30T15:51:21 PreemptTime=None
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2025-04-30T15:51:21 Scheduler=Main
   Partition=main AllocNode:Sid=login-0:919915
   ReqNodeList=(null) ExcNodeList=(null)
   NodeList=worker-[0-1]
   BatchHost=worker-1
   NumNodes=2 NumCPUs=256 NumTasks=2 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
   ReqTRES=cpu=2,mem=3034G,node=2,billing=2
   AllocTRES=cpu=256,mem=3034G,node=2,billing=256
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryNode=1517G MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=NO Contiguous=0 Licenses=(null) Network=(null)
   Command=<script.sh>
   WorkDir=<directory>
   StdErr=<error.log>
   StdIn=/dev/null
   StdOut=<output.log>

JobId=<another_job_ID> ...
...
```

By default, this command shows the jobs finished in the last 24 hours. The output is limited to 10,000 jobs. To find out how many jobs are displayed for your cluster, run the following command:

```bash theme={null}
scontrol show config | grep -E "MaxJobCount|MinJobAge"
```

Output for default settings:

```bash theme={null}
MaxJobCount             = 10000
MinJobAge               = 86400 sec
```

To list all jobs that were run on the cluster, use the [sacct](https://slurm.schedmd.com/sacct.html) command.

### Jobs and processes that run on specific nodes

To get the list of jobs running on particular nodes, run the following command:

```bash theme={null}
squeue --nodelist="worker-[0-1]"
```

Change the `--nodelist` parameter value to include the nodes that you need.

Output example:

```bash theme={null}
JOBID PARTITION   NAME     USER ST       TIME  NODES NODELIST(REASON)
  837      main   test     user  R       0:05      2 worker-[0-1]
```

To get the job processes that are currently running on a given worker node, [connect](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-worker-nodes) to this node and use `scontrol listpids`. Run the following command:

```bash theme={null}
ssh worker-0
scontrol listpids
```

Output example:

```bash theme={null}
PID      JOBID    STEPID   LOCALID GLOBALID
992342   933      0        0       1
992333   933      0        -       -
```

### Full details and batch script of a job

To get the full details of a job, run the following command:

```bash theme={null}
scontrol show job <job_ID>
```

Output example:

```bash theme={null}
JobId=<job_ID> JobName=<job_name>
   UserId=<user>(1001) GroupId=<user_group>(1001) MCS_label=N/A
   Priority=1 Nice=0 Account=(null) QOS=normal
   JobState=RUNNING Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=00:00:38 TimeLimit=UNLIMITED TimeMin=N/A
   SubmitTime=2025-04-30T15:51:21 EligibleTime=2025-04-30T15:51:21
   AccrueTime=2025-04-30T15:51:21
   StartTime=2025-04-30T15:51:21 EndTime=Unknown Deadline=N/A
   PreemptEligibleTime=2025-04-30T15:51:21 PreemptTime=None
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2025-04-30T15:51:21 Scheduler=Main
   Partition=main AllocNode:Sid=login-0:919915
   ReqNodeList=(null) ExcNodeList=(null)
   NodeList=worker-[0-1]
   BatchHost=worker-1
   NumNodes=2 NumCPUs=256 NumTasks=2 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
   ReqTRES=cpu=2,mem=3034G,node=2,billing=2
   AllocTRES=cpu=256,mem=3034G,node=2,billing=256
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryNode=1517G MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=NO Contiguous=0 Licenses=(null) Network=(null)
   Command=<script.sh>
   WorkDir=<directory>
   StdErr=<error.log>
   StdIn=/dev/null
   StdOut=<output.log>
```

You can also retrieve the batch script used to run the job:

```bash theme={null}
scontrol write batch_script <job_ID>
```

This command creates a `slurm-<job_ID>.sh` file with the contents of the script.

### Job states

You can see the current job state in the `STATE` column when you list jobs with `squeue` or in the `JobState` parameter when you get job details with `scontrol show job(s)`. Some of the common job states include:

| Job state | Description |
| - | - |
| `PD` `PENDING` | The job is waiting for resource allocation. |
| `R` `RUNNING` | The job is currently running. |
| `S` `SUSPENDED` | The job execution was [suspended](#suspend-and-resume-a-job). |
| `CD` `COMPLETED` | The job has been completed successfully (processes on all nodes finished with a zero exit code). |
| `RQ` `REQUEUED` | The job is being [requeued](#requeue-a-job). |

For a complete list of all possible job states, see the [Slurm documentation](https://slurm.schedmd.com/squeue.html#SECTION_JOB-STATE-CODES).

## How to manage jobs

The `scontrol` command lets you manage the jobs in the queue.

### Suspend and resume a job

You can suspend a job, which means that the job processes are terminated, but resource allocations are retained. Run the following command:

```bash theme={null}
scontrol suspend <job_ID>
```

The job is returned to the queue and waits in `SUSPENDED` status until you manually resume it:

```bash theme={null}
scontrol resume <job_ID>
```

The job is resumed and continues execution.

### Requeue a job

You can requeue a job, which means that the job is terminated and returned to the queue. It restarts automatically when the resources are available. Run the following command to requeue a job:

```bash theme={null}
scontrol requeue <job_ID>
```

> [!WARNING]
>
> A requeued job keeps the same job ID. If your job writes some data at paths that depend only on the job ID, the data from the previous attempt may be overwritten by the requeued job.

In Soperator clusters, some failed jobs are requeued by default. To check this setting for your cluster, run the following command:

```bash theme={null}
scontrol show config | grep JobRequeue
```

Output for default settings:

```bash theme={null}
JobRequeue       = 1
```

You may want to prevent a requeued job from being scheduled again automatically. To requeue a running job and put it on hold until you explicitly allow it to be scheduled, run the following command:

```bash theme={null}
scontrol requeuehold <job_ID>
```

To requeue and put on hold a job that hasn't started yet, run the following command:

```bash theme={null}
scontrol hold <job_ID>
```

To allow the job to be scheduled again as soon as there are available resources, run the following command:

```bash theme={null}
scontrol release <job_ID>
```

### Cancel a job

You can cancel job execution. Run the following command:

```bash theme={null}
scontrol cancel <job_ID>
```

The job is terminated and all resources are freed.
