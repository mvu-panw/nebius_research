# Running Slurm batch jobs

Source: https://docs.nebius.com/slurm-soperator/jobs

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Running Slurm batch jobs

Slurm's main purpose is to run *batch jobs*. Batch jobs are limited in time and non-interactive.

To run a batch job, you should define it in a shell script which is also called a *batch script*, and then run the `sbatch` command to submit the script. After that, Slurm allocates the requested resources, forming a *job allocation* (also known as *job*), and then runs the script on one of the allocated worker nodes.

Batch scripts launch multi-node workloads by using `srun` commands, forming one or many *job steps*. A job step represents a separate unit of work within the job. The command that you pass to `srun` is executed in parallel on one or many worker nodes within the job allocation.

One instance of the running command (a Linux process) is called *task*. By default, `srun` starts one task per allocated worker node, but you can configure it in job step settings.

You can configure job settings in multiple ways, such as in `sbatch` and `srun` command parameters, special comments inside a batch script (`#SBATCH` directives) and environment variables.

## How to run a batch job

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes).

2. Create a batch script and name it, for example, `my_ml_job.sh`. Here is a basic example of a job script that runs your training application written in Python:

   ```bash theme={null}
   #!/bin/bash

   # Directives that define the job's settings
   #SBATCH --job-name=my_ml_job
   #SBATCH --output=%x_%j.out      # <job-name>_<job-id>.out
   #SBATCH --error=%x_%j.err       # <job-name>_<job-id>.err
   #SBATCH --time=01:00:00         # time limit = 1 hour
   #SBATCH --exclusive             # allocate all CPUs on nodes
   #SBATCH --gpus-per-node=8       # allocate 8 GPUs per node
   #SBATCH --ntasks-per-node=8     # launch 8 tasks in each job step by default

   # Commands that the batch script runs
   export CHECKPOINT_PATH="/mnt/data/gpt3/checkpoints"
   export DATA_PATH="/mnt/data/c4_data"
   export DTYPE="fp16"

   source .venv/bin/activate

   # Launch a job step on 4 nodes with 8 tasks per node, each pinned to 16 CPUs.
   srun --cpus-per-task=16 python train.py
   ```

   For more details about writing batch scripts, see [Job configuration](#job-configuration) and [Examples](#examples).

3. Prepare the environment on the login node.

   > [!NOTE]
   >
   > In Soperator clusters, all nodes [share a root filesystem](https://docs.nebius.com/slurm-soperator/overview/architecture.md), so files and dependencies that you set up on the login node automatically appear on other nodes.

   1. Make sure that the files that the script uses are on the login node: create them from scratch, [upload them from another machine](https://docs.nebius.com/slurm-soperator/storage/download-data.md) or copy their contents to files on the login node. The example above requires `train.py` to be in the same directory as the batch script.

   2. Install the script dependencies.

      > For example, if your workload uses Python packages listed in [requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files), create a Python [virtual environment](https://docs.python.org/3/library/venv.html) and install the packages into it:
      >
      > ```bash theme={null}
      > python -m venv .venv
      > source .venv/bin/activate
      > pip install -r requirements.txt
      > ```

      > [!TIP]
      >
      > You can make working with dependencies easier by turning your workload into a containerized job. For more details, see [Running jobs in containers in Soperator clusters](https://docs.nebius.com/slurm-soperator/jobs/containers/index.md).

   3. Make sure all files have suitable permissions.

4. Define the required environment variables. Usually, you can put your environment variables right in the batch script, but there are cases when it's more convenient to define them inside your login shell.

   > For example, if your workload uses [Weights & Biases](https://docs.wandb.ai/quickstart/) (W\&B), define an environment variable for your W\&B API key:
   >
   > ```bash theme={null}
   > export WANDB_API_KEY=<W&B_API_key>
   > ```

5. Submit the script to Slurm with `sbatch`, providing additional settings if needed.

   > For example, if you named your batch script `my_ml_job.sh` and you want to run the job on 4 worker nodes, run the following command:
   >
   > ```bash theme={null}
   > sbatch --nodes=4 my_ml_job.sh
   > ```

   The output contains the job ID, which you can use to [monitor the job's status](https://docs.nebius.com/slurm-soperator/monitoring/statuses.md):

   ```text theme={null}
   Submitted batch job 610
   ```

The job prints its standard and error outputs to the files specified in the script directives. In the example above, the name pattern for the job's standard output file is `output_%j.txt` where `%j` stands for the job ID (for more details about patterns, see the [Slurm documentation](https://slurm.schedmd.com/sbatch.html#SECTION_FILENAME-PATTERN)). You can print the file's current contents:

```bash theme={null}
cat output_<job_ID>.txt
```

If your job takes some time, you can stream the standard output rather than repeatedly printing it:

```bash theme={null}
tail -f output_<job_ID>.txt
```

## Job configuration

To define a job, you should configure its settings, and add the commands that it should run to its batch script.

### sbatch settings

`sbatch` settings configure job allocations and provide default values for corresponding `srun` settings.

You can configure `sbatch` settings in the following ways, from highest to lowest priority (for example, the value of a command parameter overrides the value of an input environment variable for the same setting):

1. **Command parameters**: `sbatch --time="02:00:00"`

   The `sbatch` command has parameters that work and behave like regular parameters of a Linux command. Use command parameters when you want to use different values for different job runs or to overwrite settings from other sources.

2. **Input environment variables**: `export SBATCH_TIMELIMIT="01:00:00"` in login shell, `/etc/profile` or `~/profile`

   Most (but not all) command parameters have corresponding input environment variables with the same meaning. Some of these environment variables have different names from their command parameters.

   > For example, the `--time` command parameter corresponds to the `SBATCH_TIMELIMIT` input environment variable.

   For the list of all environment variables, see the [Slurm documentation](https://slurm.schedmd.com/sbatch.html#SECTION_INPUT-ENVIRONMENT-VARIABLES).

   You can define them on different levels, from highest to lowest priority:

   1. **Session variables**: environment variables that you export in your login shell. They disappear after you reconnect to the cluster. Use session variables when you want to launch a few jobs with the same setting without keeping it forever.
   2. **User variables**: environment variables from `~/profile`. The login shell exports them every time *you* connect to the cluster; after that, session variables can override them. Use user variables to set your personal default values for settings.
   3. **Cluster variables**: environment variables from `/etc/profile`. The login shell exports them every time *any user* connects to the cluster; after that, user variables and then session variables can override them. Use cluster variables to set default values for all users.

3. **#SBATCH directives**: `#SBATCH --time="01:30:00"` in a batch script

   `#SBATCH` directives are special comments at the beginning of a batch script. Use `#SBATCH` directives to define settings that should apply to most runs of this particular job.

   > [!NOTE]
   >
   > All `#SBATCH` directives must appear at the beginning of the script. As soon as `sbatch` encounters the first line that does not start with `#` or consist of whitespace (spaces, tab characters, etc.), it interprets the rest of the file as commands and silently ignores misplaced `#SBATCH` directives.

4. **Slurm defaults**: `time="00:30:00"` in `~/.slurm/defaults`

   Slurm defaults are key-value pairs in the `~/.slurm/defaults`. These values apply only to you and are not applicable to other users. Use Slurm defaults when you need a low-priority default value, or a default value for a command parameter that does not have a corresponding input environment variable.

   > [!WARNING]
   >
   > `~/.slurm/defaults` defines settings for both `sbatch` and `srun`. Do not use them for settings that have the same name but different meaning for these commands; for example, `--exclusive` ([sbatch](https://slurm.schedmd.com/sbatch.html#OPT_exclusive), [srun](https://slurm.schedmd.com/srun.html#OPT_exclusive)).

#### Common sbatch settings

<table><thead><tr><td>**Command parameter**</td><td>**Description**</td><td>**Environment variable**</td><td>**#SBATCH directive**</td><td>**Slurm default**</td></tr></thead><tbody><tr><td>`--job-name=<name>` or `-J=<name>`</td><td>The name of your job.</td><td>`SBATCH_JOB_NAME`</td><td>`#SBATCH --job-name=<name>` or `#SBATCH -J=<name>`</td><td>`job-name=<name>` or `J=<name>`</td></tr><tr><td>`--nodes=<number>` or `-N=<number>`</td><td>The number of worker nodes to allocate for the job.</td><td>*N/A*</td><td>`#SBATCH --nodes=<number>` or `#SBATCH -N=<number>`</td><td>`nodes=<number>` or `N=<number>`</td></tr><tr><td>`--nodelist=<list>` or `-w=<list>`</td><td>The list of specific worker nodes to allocate for the job. For example, `--nodelist="worker-0,worker-2"` or `--nodelist="worker-[0-2,3]"`.</td><td>*N/A*</td><td>`#SBATCH --nodelist=<list>` or `#SBATCH -w=<list>`</td><td>`nodelist=<list>` or `w=<list>`</td></tr><tr><td>`--exclude=<list>` or `-x=<list>`</td><td>The list of worker nodes to exclude from the job allocation. For example, `--exclude="worker-3"` or `--nodelist="worker-[4-7]"`.</td><td>*N/A*</td><td>`#SBATCH --exclude=<list>` or `#SBATCH -x=<list>`</td><td>`exclude=<list>` or `x=<list>`</td></tr><tr><td>`--output=<filepath_pattern>` or `-o=<filepath_pattern>`</td><td>The path to the file for the job's standard output. The path can contain special replacement symbols; for example, `%j` is replaced by the job ID. For more details, see the [Slurm documentation](https://slurm.schedmd.com/sbatch.html#SECTION_FILENAME-PATTERN).</td><td>`SBATCH_OUTPUT`</td><td>`#SBATCH --output=<filepath_pattern>` or `#SBATCH -o=<filepath_pattern>`</td><td>`output=<filepath_pattern>` or `o=<filepath_pattern>`</td></tr><tr><td>`--error=<filepath_pattern>` or `-e=<filepath_pattern>`</td><td>The path to the file for the job's error output. The path can contain the replacement symbols as described for the `output` setting.</td><td>`SBATCH_ERROR`</td><td>`#SBATCH --error=<filepath_pattern>` or `#SBATCH -e=<filepath_pattern>`</td><td>`error=<filepath_pattern>` or `e=<filepath_pattern>`</td></tr><tr><td>`--time=<duration>` or `-t=<duration>`</td><td>The time limit for the job. When the job reaches the time limit, all its tasks (processes) are terminated. For example, `01:00` limits the job to one hour, and `1-00` limits the job to one day (24 hours).</td><td>`SBATCH_TIMELIMIT`</td><td>`#SBATCH --time=<duration>` or `#SBATCH -t=<duration>`</td><td>`time=<duration>` or `t=<duration>`</td></tr><tr><td>`--gpus-per-node=<number>`</td><td>The number of GPUs to allocate for the job on each worker node.</td><td>`SBATCH_GPUS_PER_NODE`</td><td>`#SBATCH --gpus-per-node=<number>`</td><td>`gpus-per-node=<number>`</td></tr><tr><td>`--ntasks-per-node=<number>`</td><td>The maximum number of tasks to run on each worker node. When you define resources for the job in per-task settings like `gpus-per-task`, `cpus-per-task`, etc., total resources in the job allocation are based on the value of `ntasks-per-node`.</td><td>*N/A*</td><td>`#SBATCH --ntasks-per-node=<number>`</td><td>`ntasks-per-node=<number>`</td></tr><tr><td>`--exclusive`</td><td>Allocates all CPUs on the allocated worker nodes to the job, preventing other jobs from using these nodes. This allows the total number of tasks of the job to be unlimited.</td><td>`SBATCH_EXCLUSIVE`</td><td>`#SBATCH --exclusive`</td><td>*N/A*</td></tr><tr><td>`--cpus-per-task=<number>` or `-c=<number>`</td><td>The number of CPUs to allocate for the job per task.</td><td>*N/A*</td><td>`#SBATCH --cpus-per-task=<number>` or `#SBATCH -c=<number>`</td><td>`cpus-per-task=<number>` or `c=<number>`</td></tr><tr><td>`--mem=<size>[<unit>]` or `-m=<size>[<unit>]`</td><td>The RAM size to allocate for the job on each worker node. For example, `mem=4G`. To allocate all available RAM, specify `mem=0`.</td><td>`SBATCH_MEM_PER_NODE`</td><td>`#SBATCH --mem=<size>[<unit>]` or `#SBATCH -m=<size>[<unit>]`</td><td>`mem=<size>[<unit>]` or `m=<size>[<unit>]`</td></tr><tr><td>`--partition=<name>` or `-p=<name>`</td><td>The Slurm partition to allocate nodes from.</td><td>`SBATCH_PARTITION`</td><td>`#SBATCH --partition=<name>` or `#SBATCH -p=<name>`</td><td>`partition=<name>` or `p=<name>`</td></tr><tr><td>`--account=<name>` or `-A=<name>`</td><td>The Slurm account name.</td><td>`SBATCH_ACCOUNT`</td><td>`#SBATCH --account=<name>` or `#SBATCH -A=<name>`</td><td>`account=<name>` or `A=<name>`</td></tr><tr><td>`--requeue`</td><td>Requeues the job automatically: restarts it (with the same ID) when its worker nodes fail or other, higher-priority jobs preempt them.</td><td>`SBATCH_REQUEUE`</td><td>`#SBATCH --requeue`</td><td>`requeue`</td></tr><tr><td>`--no-requeue`</td><td>Disables automatically requeuing the job (see `requeue`).</td><td>`SBATCH_NO_REQUEUE`</td><td>`#SBATCH --no-requeue`</td><td>`no-requeue`</td></tr><tr><td>`--dependency=<list>` or `-d=<list>`</td><td>Dependencies of the job. For example:\
<ul><li>`dependency=singleton` requires that the job only starts after other jobs with the same name and user are terminated. This means that at any moment, there can only be one job with this name and owned by this user.</li><li>`dependency=afterany:20:21` requires that the job only starts after the jobs with IDs 20 and 21 are terminated.</li></ul>For more details, see the [Slurm documentation](https://slurm.schedmd.com/sbatch.html#OPT_dependency).</td><td>*N/A*</td><td>`#SBATCH --dependency=<list>` or `#SBATCH -d=<list>`</td><td>`dependency=<list>` or `d=<list>`</td></tr><tr><td>`--parsable`</td><td>Changes the standard output of `sbatch` from `Submitted batch job <job_id>` to just `<job_id>`.</td><td>*N/A*</td><td>`#SBATCH --parsable`</td><td>`parsable`</td></tr><tr><td>`--verbose` or `-v`</td><td>Increases the verbosity of `sbatch`'s informational messages. For more verbosity, use the parameter, `#SBATCH` directive or Slurm default multiple times, or set the `SBATCH_DEBUG` environment variable to `2`, `3`, etc.</td><td>`SBATCH_DEBUG`</td><td>`#SBATCH --verbose` or `#SBATCH -v`</td><td>`verbose` or `v`</td></tr></tbody></table>

### Commands

The commands block of a batch script defines commands that the batch script runs.

Commands in a batch script are executed on one worker node. Typically, you would need to run your main computational commands on multiple worker nodes in parallel. To do that, use the `srun` command in the script.

> In the [example above](#how-to-run-a-batch-job), `srun python train.py` makes `python train.py` run in parallel. If it was just `python train.py`, the Python script would run on one worker node.

In commands, you can use the *output environment variables* set by [sbatch](https://slurm.schedmd.com/sbatch.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES) (general job details: ID, job allocation, launch node and worker nodes, etc.) and [srun](https://slurm.schedmd.com/srun.html#SECTION_OUTPUT-ENVIRONMENT-VARIABLES) (`sbatch`'s variables, plus details about the current job step and task: local and global ranks, world size, CPUs in use, etc.). For example:

* `SLURM_JOB_NODELIST` is the list of worker nodes allocated to the job; `SLURM_NNODES` is the number of the worker nodes.
* `SLURM_SUBMIT_DIR` is the directory where you executed `sbatch`.
* `SLURM_NODEID` is the node ID for each worker node.

## Examples

### Training with Hugging Face Accelerate

The following example uses [Hugging Face Accelerate](https://huggingface.co/docs/accelerate/index) to run a training workload (`train.py`) on two nodes with 8 GPUs each. It requires that you add Accelerate to `train.py`, as described in the [Accelerate documentation](https://huggingface.co/docs/accelerate/basic_tutorials/migration), and install it into your Python virtual environment (`pip install accelerate`).

`llm_training.sh`:

```bash theme={null}
#!/bin/bash

#SBATCH --job-name=llm_training
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --nodes=2
#SBATCH --gpus-per-node=8
#SBATCH --exclusive
#SBATCH --mem=0

# Get the hostname of worker node where this sbatch script runs,
# SLURMD_NODENAME is the Slurm output environment variable for sbatch.
MAIN_PROCESS_ADDR=$SLURMD_NODENAME
MAIN_PROCESS_PORT=12345

srun \
  --cpus-per-task=64 \
  --hint=nomultithread \
  bash -c 'accelerate launch \
    # SLURM_STEP_NUM_NODES is the number of worker nodes allocated for the step (2)
    --num_machines $SLURM_STEP_NUM_NODES \
    # SLURM_NODEID is the ID of the current worker node (0 or 1)
    --machine_rank $SLURM_NODEID \
    --main_process_ip $MAIN_PROCESS_ADDR \
    --main_process_port $MAIN_PROCESS_PORT \
    --num_processes $(($SLURM_STEP_NUM_NODES * $SLURM_GPUS_ON_NODE)) \
    train.py'
```

For `accelerate launch` parameters, see [Accelerate documentation](https://huggingface.co/docs/accelerate/package_reference/cli#accelerate-launch).

### Fine-tuning with PyTorch (torchrun)

The following example uses [PyTorch](https://pytorch.org/docs/stable/index.html) to fine-tune a model (`llama-3-8b`) on a sample dataset (`alpaca_dataset`). The job runs on three nodes with 8 GPUs each.

For the full example, including `finetuning.py` with added PyTorch and instructions to download the model and the dataset, see the [Multi-node LLM fine-tuning on Slurm](https://github.com/alex000kim/multi-node-llm-finetuning-slurm) repository on GitHub.

* `sbatch.sh`:

  ```bash theme={null}
  #!/bin/bash

  #SBATCH --job-name=llama-finetune
  #SBATCH --nodes=3
  #SBATCH --output=O-%x_%j.txt
  #SBATCH --error=E-%x_%j.txt
  #SBATCH --gres=gpu:8
  #SBATCH --cpus-per-task=120
  # Loads all environment variables into the job
  #SBATCH --export=ALL

  srun srun.sh
  ```

* `srun.sh`:

  ```bash theme={null}
  #!/bin/bash

  export GPUS_PER_NODE=8
  # Get the hostname of the first node from the list of the job's worker nodes
  # (SLURM_JOB_NODELIST, set by Slurm)
  HOST_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
  MAIN_PROCESS_PORT=12345

  echo "SLURM_NNODES=$SLURM_NNODES"
  echo "SLURM_NODEID=$SLURM_NODEID"
  echo "HOST_ADDR=$HOST_ADDR"
  echo "MAIN_PROCESS_PORT=$MAIN_PROCESS_PORT"

  source .venv/bin/activate

  torchrun --nnodes $SLURM_NNODES \
    --nproc_per_node $GPUS_PER_NODE \
    --master_addr $HOST_ADDR \
    --master_port $MAIN_PROCESS_PORT \
    --node_rank=$SLURM_NODEID \
    finetuning.py \
    --model_name ./llama-3-8b \
    --output_dir saved_peft_model \
    --use_peft \
    --peft_method lora \
    --enable_fsdp \
    --use_fast_kernels \
    --use_wandb \
    --dataset alpaca_dataset
  ```

  For details about `torchrun`, see the [PyTorch documentation](https://pytorch.org/docs/stable/elastic/run.html) and the source code of [torch.distributed.run](https://github.com/pytorch/pytorch/blob/main/torch/distributed/run.py) on GitHub.

### Containerized jobs

You can run containerized jobs with batch scripts by using special `srun` parameters. For example:

```bash theme={null}
srun --container-image="nvcr.io#nvidia/tensorflow:23.02-tf1-py3" \
  python -c "import tensorflow as tf; print (tf.__version__)"
```

For more details and examples, see [Running jobs in containers in Soperator clusters](https://docs.nebius.com/slurm-soperator/jobs/containers/index.md).
