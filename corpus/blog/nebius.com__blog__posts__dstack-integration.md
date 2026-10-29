# Announcing the integration between Nebius and dstack

Source: https://nebius.com/blog/posts/dstack-integration

Skip to main content

Traditional orchestration tools like Kubernetes and Slurm present challenges for ML teams. Kubernetes, with its low-level interface, can be difficult for AI workflows beyond inference, such as development and training, which often require custom setups. Slurm, optimized for training workloads, lacks support for other essential ML tasks, including dev environment management, cluster management and inference deployment.

dstack is an open-source container orchestration platform that bridges the gap between Kubernetes and Slurm, designed for ML teams to manage GPU workloads across GPU clouds and on-premises data centers.

# Getting started with dstack and NebiusGetting started with dstack and Nebius

### Setting up the serverSetting up the server

To use dstack with Nebius, configure your backend:

- Log in to your Nebius AI Cloud account.

- Navigate to Access and then select Service Accounts.

- Create a new service account, assign it to the editors group and then upload an authorized key.

Then, configure the backend via ~/.dstack/server/config.yml:

projects:
- name: main
 backends:
 - type: nebius
 creds:
 type: service_account
 service_account_id: serviceaccount-e002dwnbz81sbvg2bs
 public_key_id: publickey-e00fciu5rkoteyzo69
 private_key_file: ~/path/to/key.pem

Proceed with installing and starting the dstack server. You’ll need Python 3.10 or higher.

$ pip install "dstack[nebius]"
$ dstack server

Once the server is up, go ahead and initialize a project repo:

$ mkdir quickstart && cd quickstart
$ dstack init

Now, you can also use the dstack CLI to manage dev environments, tasks, services and fleets.

### Running a dev environmentRunning a dev environment

A dev environment lets you provision an instance and access it with your desktop IDE.

Create the following configuration file inside the repo:

type: dev-environment
name: vscode

# If `image` is not specified, dstack uses its default image
python: "3.11"
#image: dstackai/base:py3.13-0.7-cuda-12.1

ide: vscode

resources:
 gpu: L40S

Apply the configuration by using dstack apply:

$ dstack apply -f .dstack.yml

 # BACKEND REGION RESOURCES SPOT PRICE
 1 nebius eu-north1 8xCPU, 32GB, 1xL40S no $1.5484
 2 nebius eu-north1 16xCPU, 64GB, 1xL40S no $1.7468
 3 nebius eu-north1 16xCPU, 96GB, 1xL40S no $1.8172

Submit the run vscode? [y/n]: y

Launching `vscode`...
████████████████████████████████████████ 100%

To open in VS Code Desktop, use this link:
 vscode://vscode-remote/ssh-remote+vscode/workflow

Click the link, to access the dev environment by using your desktop IDE.

### Running a taskRunning a task

Now, imagine you’d like to run training on either a cluster or a single node. Below is an example of a multi-node task:

type: task
# The name is optional, if not specified, generated randomly
name: train-distrib

# The size of the cluster
nodes: 2

python: "3.12"

# Commands to run on each node
commands:
 - git clone https://github.com/pytorch/examples.git
 - cd examples/distributed/ddp-tutorial-series
 - pip install -r requirements.txt
 - torchrun
 --nproc-per-node=$DSTACK_GPUS_PER_NODE
 --node-rank=$DSTACK_NODE_RANK
 --nnodes=$DSTACK_NODES_NUM
 --master-addr=$DSTACK_MASTER_NODE_IP
 --master-port=12345
 multinode.py 50 10

resources:
 gpu: L40S
 shm_size: 16GB

If you apply it, dstack will automatically set up the cluster and run the script on each node, handling propagating system environment variables such as DSTACK_MASTER_NODE_IP, DSTACK_NODE_RANK, DSTACK_GPUS_PER_NODE.

The examples above are just two of the many features dstack provides. These include running services, managing fleets, volumes and more.

Check out dstack’s documentation for details.

## What’s next?

Sign up to Nebius AI Cloud​
Find dstack on GitHub​
Join dstack on Discord​

## Explore Nebius AI Cloud

Compute Cloud​
Managed Kubernetes​
Soperator​
Object Storage​

Nebius team

Contents

- Getting started with dstack and Nebius

- Setting up the server

- Running a dev environment

- Running a task

## See also

### 

Nebius and Outerbounds form strategic technology partnership through integration

We are excited to unveil our latest collaboration: Nebius AI Cloud, the ultimate cloud for AI innovators, and Outerbounds, an AI/ML platform powered by the popular open-source framework Metaflow, are now integrated as part of a broader technology partnership.

March 11, 2025
5 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

Nebius AI Cloud is now integrated with SkyPilot

We’re excited to announce our integration with SkyPilot, an open-source framework that simplifies running AI and batch workloads across cloud platforms. This collaboration enables direct access to Nebius AI Cloud resources via SkyPilot.

April 2, 2025
6 mins to read

Sign in to save this post
Sign In
