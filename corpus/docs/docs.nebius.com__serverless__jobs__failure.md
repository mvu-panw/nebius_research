# Debugging failed Devlabs, jobs and endpoints

Source: https://docs.nebius.com/serverless/jobs/failure

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Debugging failed Devlabs, jobs and endpoints

If a job, endpoint or Devlab created from a custom image fails, gets canceled or returns an error, Serverless AI deletes the underlying virtual machine (VM) and boot disk to avoid costs. In this case, you can't connect to the deployment and debug it. To keep the VM alive for debugging, run the deployment with a "sleep-on-fail" wrapper.

> [!WARNING]
>
> For Devlabs created from a template (`--template`), you can't override the container command or arguments. You cannot add the "sleep-on-fail" wrapper in that mode. Use this approach only for Devlabs created from a custom image (`--image`).

## Keep the VM alive on failure

To keep the VM alive for debugging when a job, endpoint or Devlab created from a custom image fails, use `bash -lc` and append a long sleep if the main command fails. Add the following parameters when creating the resource:

**CLI**

```bash theme={null}
nebius ai <devlab|job|endpoint> create \
  ... \
  --container-command bash \
  --args "-lc '<your_main_command> || (echo FAILED; sleep 86400)'"
```

**REST API**

Add the following parameters to the `spec` object in the body of the request that creates a job, an endpoint or a Devlab created from a custom image:

```json theme={null}
{
  "containerCommand": "bash",
  "args": "-lc \"<your_main_command> || (echo FAILED; sleep 86400)\""
}
```

Replace `<your_main_command>` with the actual command you want to run.

When you use this wrapper, the deployment behaves as follows:

* If the main command succeeds, the resource exits normally.
* If the main command fails, the resource keeps running for 24 hours. During this time, you can connect to the underlying VM via SSH and debug.

> [!TIP]
>
> Use `sleep 3600` for one hour if you want a shorter debug window.

## Connect to the container by using SSH

You can connect to the container of a deployment in the following ways:

**Directly**

To connect to the container by using SSH, you should [create a Devlab](https://docs.nebius.com/serverless/devlabs/manage.md#how-to-create-a-devlab), [create a job](https://docs.nebius.com/serverless/jobs/manage.md#how-to-create-a-job) or [create an endpoint](https://docs.nebius.com/serverless/endpoints/manage.md#how-to-create-an-endpoint) with at least one `--ssh-key`.

To run a shell inside the container for debugging, run `nebius ai devlab ssh <devlab_ID>`, `nebius ai job ssh <job_ID>` or `nebius ai endpoint ssh <endpoint_ID>`. A shell starts in the container.

You can add the following parameters to these commands:

* `-i` or `--identity-file`: Identity file for SSH authentication. Default: your SSH key.
* `-s` or `--shell`: Shell to run inside the container. Default: `sh`.

For example, to use `bash` and a specific key, run:

* For the Devlab:

  ```bash theme={null}
  nebius ai devlab ssh <devlab_ID> -i ~/.ssh/id_rsa -s bash
  ```

* For the job:

  ```bash theme={null}
  nebius ai job ssh <job_ID> -i ~/.ssh/id_rsa -s bash
  ```

* For the endpoint:

  ```bash theme={null}
  nebius ai endpoint ssh <endpoint_ID> -i ~/.ssh/id_rsa -s bash
  ```

After you run the command, a shell inside the container is automatically opened.

**Through the underlying VM**

1. Get the Devlab, job or endpoint ID:

   ```bash theme={null}
   nebius ai <devlab|job|endpoint> list
   ```

2. Get the public IP address of the VM:

   * For the Devlab:

     ```bash theme={null}
     nebius ai devlab get <devlab_ID> \
       --format json | jq -r '.status.instances[0].public_ip'
     ```

     You can get the IP address of the VM only while the Devlab is running. When the Devlab is stopped or deleted, its compute resources (including the VM) are released; therefore, you can't get the IP address of the VM.

   * For the job:

     ```bash theme={null}
     nebius ai job get <job_ID> \
       --format jsonpath='{.status.instances[0].public_ip}'
     ```

     You can get the IP address of the VM only while the job is running. When the job is complete or failed, its resources (including the VM) are released; therefore, you can't get the IP address of the VM.

   * For the endpoint:

     ```bash theme={null}
     nebius ai endpoint get <endpoint_ID> \
       --format jsonpath='{.status.instances[0].public_ip}'
     ```

3. Connect to the VM via SSH by using the `nebius` username and the copied IP address:

   ```bash theme={null}
   ssh nebius@<VM_IP_address>
   ```

4. Find the running container. From the VM, run:

   ```bash theme={null}
   sudo docker ps
   ```

5. Copy the container ID. For example, `aijob-<job_ID>-job-1`.

6. Open a shell inside the container:

   ```bash theme={null}
   sudo docker exec -it <container_ID> /bin/bash
   ```

## Run tests inside the container

After you [connected to the container](#connect-to-the-container-by-using-ssh):

* Check currently running processes:

  ```bash theme={null}
  ps aux
  ```

  You can identify which processes used the most computing resources, check if the script was running as expected and see when the processes started.

* Check if GPUs are accessible:

  ```bash theme={null}
  nvidia-smi
  ```

  This test helps confirm whether the GPUs were allocated correctly and whether the Devlab, job or endpoint workloads could use them.
