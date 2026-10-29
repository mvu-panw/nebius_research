# Downloading data in Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/storage/download-data

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Downloading data in Soperator clusters

Tasks that run on a Soperator cluster need large amounts of data, for example, datasets and machine learning checkpoints. You can download the data either to the shared filesystem of your Soperator cluster or to a [bucket in Object Storage](https://docs.nebius.com/object-storage/overview.md).

You can use various tools to download data, depending on the size of data and the source of the download:

* To download data from other Slurm clusters via SSH:

  * For smaller files, like code, binaries or container images, use [rsync](#how-to-download-data-by-using-rsync).
  * For larger files, like datasets or ML checkpoints, use [rclone](#how-to-download-data-by-using-rclone).

* To download data to or from an Object Storage bucket or other S3-compatible storage:

  * For smaller files (up to 10 TiB), use [AWS CLI](#how-to-download-data-by-using-the-aws-cli).
  * For larger files (up to 100 TiB), use [rclone](#how-to-download-data-by-using-rclone).

## How to download data by using rsync

[Rsync](https://rsync.samba.org/) can transfer files via SSH between a Soperator cluster and a remote server. You can use `rsync` to migrate data from an external data source to a Soperator cluster.

Use `rsync` to download binaries, configuration files, container images or other small files. It is not intended for transferring large files.

Unlike other tools, `rsync` can preserve file permissions and ownerships. You can combine `rsync` with `rclone` to download the files with `rclone`, then update their permissions with `rsync`. For more information, see the [example](#example-with-rclone-and-rsync-combined) below.

You can transfer data with `rsync` [directly](#download-data-directly) or [within a Slurm job](#download-data-within-a-slurm-job).

### Download data directly

For example, to download a directory via SSH from a remote server to the shared filesystem of your Soperator cluster:

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) of your Soperator cluster.
2. Run the following command:

   ```bash theme={null}
   rsync -azP --no-sparse \
     -e "ssh -i <path/to/private/key>" \
     <username>@<remote_host>:<path/to/remote/directory> \
     <local/destination/path/>
   ```

   In this command, specify the following:

   * Private SSH key for the remote server
   * Username and host to connect to the remote server
   * Path to the remote directory with data
   * Path to the directory in the shared filesystem where the data should be downloaded

### Download data within a Slurm job

A Slurm job uses a worker node that has more processing resources than a login node. In addition, data transfer via a Slurm job continues even if your connection to a login node is interrupted.

To download data within a Slurm job:

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) of your Soperator cluster.

2. Create the `rsync_copy.batch` file in the shared filesystem of your Soperator cluster and paste the following contents into it:

   ```bash theme={null}
   #!/bin/bash

   #SBATCH -J "rsync_copy"
   #SBATCH --nodes=1
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=10G

   usage() {
     echo "usage: ${0} -f <from> -t <to> [-i <ssh-key>] [-h]" >&2
     echo "" >&2
     echo "Arguments <from> and <to> should follow the rsync syntax" >&2
     echo "For example:" >&2
     echo "  -f bob@89.168.111.222:/home/bob/remote/path/ -t /home/bob/local/path/" >&2
     echo "  -f /home/bob/files -t /home/alice/files" >&2
     echo "Argument <ssh-key> is required if either <from> or <to> is an SSH endpoint" >&2
     exit 1
   }

   while getopts f:t:i:h flag
   do
       case "${flag}" in
           f) COPY_FROM=${OPTARG};;
           t) COPY_TO=${OPTARG};;
           i) COPY_SSH_KEY=${OPTARG};;
           h) usage;;
           *) usage;;
       esac
   done

   if [ -z "${COPY_FROM}" ] || [ -z "${COPY_TO}" ]; then
       usage
   fi

   echo "Copy data from ${COPY_FROM} to ${COPY_TO}"
   srun --export=COPY_FROM,COPY_TO,COPY_SSH_KEY \
       rsync -azP --no-sparse \
         -e "ssh -i ${COPY_SSH_KEY}" \
         "${COPY_FROM}" \
         "${COPY_TO}"
     '

   echo "Done"
   ```

3. Run a job to transfer data:

   ```bash theme={null}
   sbatch rsync_copy.batch -- \
     -i <path/to/private/key> \
     -f <username>@<remote_host>:<path/to/remote/directory> \
     -t <local/destination/path/>
   ```

   In this command, specify the following:

   * Private SSH key for the remote server
   * Username and host to connect to the remote server
   * Path to the remote directory with data
   * Path to the directory in the shared filesystem where the data should be downloaded

## How to download data by using rclone

[Rclone](https://rclone.org/docs/) is a versatile tool for downloading or uploading data between various locations. It needs more configuration than `rsync`, but after the initial setup it allows you to download large amounts of data (10-100 TiB) fast.

To work with `rclone`, create the `~/.config/rclone/rclone.conf` configuration file on the machine from which you are running the commands. In this configuration file, create profiles for each remote location and specify in them information such as the address and type of the location, or credentials for connecting to it. For the full list of location types and possible settings for them, see the [rclone documentation](https://rclone.org/docs/).

After you configure `rclone` profiles for several remote locations, you can move data between these locations or to the local machine.

For example, to download data from an Object Storage bucket to a shared filesystem of a Soperator cluster:

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) of your cluster.

2. Create the `~/.config/rclone/rclone.conf` configuration file. For example, this file can have the following contents:

   ```ini theme={null}
   [s3mlperf]
   type = s3
   provider = AWS
   env_auth = false
   region = eu-north1
   no_check_bucket = true
   endpoint = https://storage.eu-north1.nebius.cloud
   acl = private
   bucket_acl = private
   ```

   This is a remote profile for an Object Storage bucket. Add more profiles for other locations if needed.

3. Create the `rclone_copy.batch` script that transfers data between remote locations that have `rclone` profiles configured, or to the shared filesystem of your Soperator cluster. Paste the following contents into the `rclone_copy.batch` file:

   ```bash theme={null}
   #!/bin/bash

   #SBATCH -J "rclone_copy"
   #SBATCH --nodes=1
   #SBATCH --cpus-per-task=64
   #SBATCH --mem=500G

   usage() {
     echo "usage: ${0} -f <from> -t <to> [-h]" >&2
     echo "" >&2
     echo "Arguments <from> and <to> should follow the rclone syntax" >&2
     echo "For example:" >&2
     echo "  -f my-s3-profile:s3-bucket/subpath -t /home/bob/local/path" >&2
     echo "  -f /home/bob/local/path -t my-ssh-profile:/home/bob/remote/path" >&2
     exit 1
   }

   while getopts f:t:h flag
   do
       case "${flag}" in
           f) COPY_FROM=${OPTARG};;
           t) COPY_TO=${OPTARG};;
           h) usage;;
           *) usage;;
       esac
   done

   if [ -z "${COPY_FROM}" ] || [ -z "${COPY_TO}" ]; then
       usage
   fi

   echo "Copy data from ${COPY_FROM} to ${COPY_TO}"
   srun --export=COPY_FROM,COPY_TO \
     bash -c '
       echo "Set umask so that new files have 666 permission"
       umask 000

       echo "Start rclone"
       rclone copy "${COPY_FROM}" "${COPY_TO}" --progress --links \
         --transfers=32 --buffer-size=128Mi \
         --multi-thread-streams=24 --multi-thread-chunk-size=128Mi \
         --multi-thread-cutoff=4Gi --multi-thread-write-buffer-size=128Mi \
         --checkers=24 --size-only \
         --update --use-server-modtime --fast-list \
         --s3-no-head-object --s3-chunk-size=32M \
         --sftp-chunk-size=120k --sftp-concurrency=64
     '

   echo "Done"
   ```

   The [rclone sync](https://rclone.org/commands/rclone_sync/) command synchronizes the contents of directories in two locations. To download data into an empty directory, you can also use [rclone copy](https://rclone.org/commands/rclone_copy/) or other [rclone subcommands](https://rclone.org/docs/#subcommands).

4. Run a job to download the data from the `slurm-mlperf-training` Object Storage bucket to the `mlperf-data` directory in the shared filesystem of your Soperator cluster:

   ```bash theme={null}
   sbatch rclone_copy.batch -- \
     -f s3mlperf:slurm-mlperf-training \
     -t /mlperf-data
   ```

   The job runs on one of the worker nodes and downloads the data to the shared filesystem, so that all nodes can access it.

### How to use several nodes for data download

`rclone` is a single-node utility and doesn't let you take full advantage of Slurm parallelism. However, to speed up large downloads, you can distribute the load manually. To do so, start several jobs by using the `rclone_copy.batch` script described above and specify a different subdirectory in each job. As the Soperator cluster has a shared filesystem, the downloaded data is available to all nodes.

## Example with rclone and rsync combined

`rclone` downloads files from a remote server faster than `rsync`. However, `rsync` can preserve file ownerships and permissions. You can combine these two instruments: download the files first with `rclone`, which is fast, then adjust permissions with `rsync`.

To download data from a remote location configured in the `rclone` configuration file to a local directory:

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) of your Soperator cluster.

2. Create the `~/.config/rclone/rclone.conf` configuration file. In this file, specify profiles for all remote locations that you are going to use.

3. Submit the job that runs the [rclone\_copy.batch](#how-to-download-data-by-using-rclone) script:

   ```bash theme={null}
   sbatch rclone_copy.batch \
     -f <remote_profile>:<path/to/remote/directory> \
     -t <local/target/directory>
   ```

   In this command, specify the following:

   * Name of the remote profile configured in `rclone.conf` and path to the remote directory with data
   * Path to the directory in the shared filesystem where the data should be downloaded

4. Get the job ID from the output of the last command:

   ```bash theme={null}
   Submitted batch job <rclone_job_ID>
   ```

5. Submit the job that runs the [rsync\_copy.batch](#how-to-download-data-by-using-rsync) script with the condition that it should start after the previous job completes:

   ```bash theme={null}
   sbatch rsync_copy.batch \
     --dependency=afterok:<rclone_job_ID> \
     -i <path/to/private/key> \
     -f <username>@<remote_host>:<path/to/remote/directory> \
     -t <local/target/directory>
   ```

   In this command, specify:

   * ID of the job running `rclone` that you obtained in the previous step
   * Private SSH key for the remote server
   * Username and host to connect to the remote server, and path to the remote directory with data
   * Path to the directory in the shared filesystem where the data should be downloaded

## How to download data by using the AWS CLI

The [AWS CLI](https://docs.aws.amazon.com/cli/latest/) allows you to download data from any S3-compatible storage, including buckets in Object Storage. You can use it for smaller amounts of data (no more than 10 TiB).

1. [Connect to a login node](https://docs.nebius.com/slurm-soperator/clusters/connect.md#how-to-connect-to-login-nodes) of your Soperator cluster.

2. Create the `aws_copy.batch` file with the following contents:

   ```bash theme={null}
   #!/bin/bash

   #SBATCH -J "aws_copy"
   #SBATCH --nodes=1
   #SBATCH --cpus-per-task=64
   #SBATCH --mem=500G

   srun aws s3 sync s3://<bucket_name>/[<prefix_for_object_keys>] <local/destination/path/>

   ```

3. Submit the `aws_copy.batch` job:

   ```bash theme={null}
   sbatch aws_copy.batch
   ```

For more information, see the [AWS CLI reference](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html).
