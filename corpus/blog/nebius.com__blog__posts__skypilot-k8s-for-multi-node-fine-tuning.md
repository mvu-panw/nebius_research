# Using SkyPilot and Kubernetes for multi-node fine-tuning of Llama

Source: https://nebius.com/blog/posts/skypilot-k8s-for-multi-node-fine-tuning

Skip to main content

# IntroductionIntroduction

This tutorial guides you through setting up distributed multi-node fine-tuning of LLMs using our Managed Kubernetes and SkyPilot. You’ll learn how to:

- 

Deploy a Kubernetes cluster optimized for AI training.

- 

Set up distributed fine-tuning of LLMs.

- 

Monitor training progress and resources.

The benefits of this approach include reduced operational overhead, improved scalability and performance, cost-effective resource utilization and simple management of training jobs and resources.

Managed Service for Kubernetes is a fully managed container orchestration service that simplifies deploying and scaling containerized applications. It handles infrastructure management, supports AI workloads and provides easy-to-use logging and monitoring. This allows ML teams to focus on core tasks rather than managing infrastructure. One of our previous blog posts elaborates on this idea.

SkyPilot is an open-source framework for running machine learning and batch jobs on any cloud or Kubernetes cluster. It simplifies deploying and managing AI workloads by abstracting infrastructure complexities. Key features include automatic cloud selection, managed spot instances and easy scaling of distributed tasks. Built on Ray, SkyPilot enables seamless distributed training across multiple nodes. Its integration with Kubernetes allows running tasks on both cloud and on-premises clusters, offering a comprehensive solution for efficient and cost-effective AI workload management.

# Video versionVideo version

If you prefer video tutorials, check out this guide’s version I’ve recorded for YouTube:

# PrerequisitesPrerequisites

- 

Create a Nebius account.

- 

Clone the Solution Library repository:

git clone https://github.com/nebius/nebius-solution-library.git
cd nebius-solution-library/k8s-training

- Install required tools:

- Nebius’ CLI:

curl -sSL https://storage.ai.nebius.cloud/nebius/install.sh | bash
exec -l $SHELL

- 

jq:

- 

macOS: brew install jq

- 

Debian-based distributions: sudo apt install jq -y

- 

socat and netcat:

- 

macOS: brew install socat netcat

- 

Debian-based distributions: sudo apt install socat netcat-openbsd -y

- 

Create a Hugging Face account and obtain developer API token.

- 

(Optional) Create a Weights & Biases account and get an API key.

- 

Request access to the Llama-3.1-8B model, as it’s gated (i.e., not available publicly until access is granted by Meta).

- 

Install SkyPilot with Kubernetes support:

pip install "skypilot[kubernetes]"

# Step 1: Deploy the Kubernetes ClusterStep 1: Deploy the Kubernetes Cluster

The Nebius Solution Library provides a complete Terraform configuration for provisioning a Kubernetes cluster optimized for AI training. The configuration includes:

- 

Cluster setup with networking.

- 

Storage configuration (shared filesystem / GlusterFS).

- 

Monitoring stack (Grafana, Prometheus, Loki).

- 

The necessary operators.

1. Configure your deployment by updating the terraform.tfvars file with your project, subnet IDs, SSH key and node presets:

# Cloud environment and network
parent_id = "your-project-id"
subnet_id = "your-subnet-id"
ssh_user_name = "your-username"
ssh_public_key = {
path = "~/.ssh/id_rsa.pub"
}

# Nodes
cpu_nodes_count = 1
cpu_nodes_preset = "16vcpu-64gb"
gpu_nodes_count = 2
gpu_nodes_preset = "8gpu-128vcpu-1600gb"

# Storage
enable_filestore = true
filestore_disk_size = 5 * 1024 * 1024 * 1024 * 1024 # 5TB
filestore_block_size = 4096

Unless you change the node settings, the number of nodes of each type will be the same as in the code block above. For more detailed info about available VM types, visit this docs page.

2. Initialize and deploy using the provided environment script:

# Initialize the environment and set access tokens 
source ./environment.sh

# Initialize Terraform and deploy the cluster
terraform init
terraform apply # this will take a while

Observe the created resources in the console:

Kubernetes cluster

Node groups

3. Configure kubectl config after deployment and check the K8s context:

$ nebius mk8s v1 cluster get-credentials \
--id $(cat terraform.tfstate | jq -r '.resources[] | select(.type == "nebius_mk8s_v1_cluster") | .instances[].attributes.id') --external
$ kubectl config current-context
...
nebius-mk8s-k8s-training-<...>
...

4. Verify cluster status:

$ kubectl get nodes
NAME STATUS ROLES AGE VERSION
computeinstance-e00ng3cbtwew4arngx Ready <none> 24h v1.30.1
computeinstance-e00p0sf1f19a06q9nz Ready <none> 24h v1.30.1

$ kubectl get pods -A
NAMESPACE NAME READY STATUS RESTARTS AGE
csi-mounted-fs-path csi-mounted-fs-path-plugin-jxbb9 5/5 Running 0 7h31m
csi-mounted-fs-path csi-mounted-fs-path-plugin-v84l2 5/5 Running 0 7h31m
default llama31-8ad1-9ee6-worker 1/1 Running 0 7h22m
default llama31-8ad1-head 1/1 Running 0 7h22m
gpu-operator gpu-feature-discovery-l9dk8 1/1 Running 0 24h
gpu-operator gpu-feature-discovery-r7pl5 1/1
...

5. Verify access to the cluster and availability using SkyPilot:

$ sky check kubernetes 
$ sky show-gpus --cloud kubernetes
Kubernetes GPUs
GPU QTY_PER_NODE TOTAL_GPUS TOTAL_FREE_GPUS 
H100 1, 2, 3, 4, 5, 6, 7, 8 16 16

# Step 2: Set up the training environmentStep 2: Set up the training environment

1. Create a working directory (preferably outside the nebius-solution-library repository):

mkdir llama-finetuning
cd llama-finetuning
mkdir configs

2. Create the SkyPilot task configuration file (task.yaml):

# LoRA finetuning Meta Llama 3.1 on any of your own infra.
# To finetune an 8B model: 
# sky launch task.yaml -c llama31 --env HF_TOKEN --env WANDB_API_KEY --env MODEL_SIZE=8B

envs:
MODEL_SIZE: 
HF_TOKEN:
DATASET: "yahma/alpaca-cleaned"
WANDB_API_KEY:

resources:
cloud: kubernetes
accelerators: H100:8
num_nodes: 2

# Mount host path to the pod
# https://github.com/nebius/nebius-solution-library/tree/main/k8s-training is mounting 
# the shared filestore to /mnt/data, so we need to mount the same path in the pod
experimental:
 config_overrides:
 kubernetes:
 pod_config:
 spec:
 containers:
 - volumeMounts:
 - mountPath: /mnt/data
 name: data-volume
 volumes:
 - name: data-volume
 hostPath:
 path: /mnt/data
 type: Directory

file_mounts:
 /configs: ./configs

setup: |
 pip install torch torchvision torchao torchtune wandb
 tune download meta-llama/Meta-Llama-3.1-${MODEL_SIZE}-Instruct \
 --hf-token $HF_TOKEN \
 --output-dir /tmp/Meta-Llama-3.1-${MODEL_SIZE}-Instruct \
 --ignore-patterns "original/consolidated*" 

run: |
 tune run --nproc_per_node $SKYPILOT_NUM_GPUS_PER_NODE \
 lora_finetune_distributed \
 --config /configs/${MODEL_SIZE}-lora.yaml \
 dataset.source=$DATASET

 # Save outputs to persistent storage
 mkdir -p /mnt/data/$MODEL_SIZE-lora-output
 rsync -Pavz /tmp/Meta-Llama-3.1-.!!!.82c6c3cd-87ff-4be3-bf15-a96eb3e1cdc5.!!!.MODEL_SIZE-lora-output
 rm -rf /tmp/Meta-Llama-3.1-${MODEL_SIZE}-Instruct

The tutorial uses Torchtune for the fine-tuning process. This is a PyTorch-native library for distributed training, which offers:

- 

PyTorch implementations of popular LLMs from the Llama, Gemma, Mistral, Phi and Qwen model families.

- 

Hackable training recipes for full fine-tuning: LoRA, QLoRA, DPO, PPO, QAT, knowledge distillation, and more.

- 

Out-of-the-box memory efficiency, performance improvements and scaling with the latest PyTorch APIs.

- 

YAML configs for training, evaluation, quantization or inference recipes.

- 

Built-in support for many popular dataset formats and prompt templates.

3. Copy the LoRA configuration to configs/8B-lora.yaml:

## configs/8B-lora.yaml
# Tokenizer
tokenizer:
 _component_: torchtune.models.llama3.llama3_tokenizer
 path: /tmp/Meta-Llama-3.1-8B-Instruct/original/tokenizer.model
 
# Model Arguments
model:
 _component_: torchtune.models.llama3_1.lora_llama3_1_8b
 lora_attn_modules: ['q_proj', 'v_proj']
 apply_lora_to_mlp: False
 apply_lora_to_output: False
 lora_rank: 8
 lora_alpha: 16
 
checkpointer:
 _component_: torchtune.training.FullModelHFCheckpointer
 checkpoint_dir: /tmp/Meta-Llama-3.1-8B-Instruct/
 checkpoint_files: [
 model-00001-of-00004.safetensors,
 model-00002-of-00004.safetensors,
 model-00003-of-00004.safetensors,
 model-00004-of-00004.safetensors
 ]
 recipe_checkpoint: null
 output_dir: /tmp/Meta-Llama-3.1-8B-Instruct/
 model_type: LLAMA3
resume_from_checkpoint: False

# Dataset and Sampler
dataset:
 _component_: torchtune.datasets.alpaca_cleaned_dataset
seed: null
shuffle: True
batch_size: 2

# Optimizer and Scheduler
optimizer:
 _component_: torch.optim.AdamW
 weight_decay: 0.01
 lr: 3e-4
lr_scheduler:
 _component_: torchtune.modules.get_cosine_schedule_with_warmup
 num_warmup_steps: 100
 
loss:
 _component_: torch.nn.CrossEntropyLoss
 
# Training
epochs: 1
max_steps_per_epoch: null
gradient_accumulation_steps: 32

# Logging
output_dir: /tmp/lora_finetune_output
metric_logger:
 _component_: torchtune.training.metric_logging.WandBLogger
 project: llama3_lora
log_every_n_steps: 5
log_peak_memory_stats: False

# Environment
device: cuda
dtype: bf16
enable_activation_checkpointing: False

Config files for 70B and 405B models can be found here.

# Step 3: Launch fine-tuningStep 3: Launch fine-tuning

1. Set required environment variables:

export HF_TOKEN=your_huggingface_token
export WANDB_API_KEY=your_wandb_api_key
export MODEL_SIZE=8B
export DATASET="yahma/alpaca-cleaned"

2. Launch training using SkyPilot:

$ sky launch task.yaml -c llama31 \
--env HF_TOKEN \
--env WANDB_API_KEY \
--env MODEL_SIZE=8B

Task from YAML spec: task.yaml
I 10-24 18:46:41 optimizer.py:691] == Optimizer ==
I 10-24 18:46:41 optimizer.py:714] Estimated cost: $0.0 / hour
I 10-24 18:46:41 optimizer.py:714] 
I 10-24 18:46:41 optimizer.py:839] Considered resources (2 nodes):
I 10-24 18:46:41 optimizer.py:909] ----------------------------------------------------------------------------------------------------
I 10-24 18:46:41 optimizer.py:909] CLOUD INSTANCE vCPUs Mem(GB) ACCELERATORS REGION/ZONE COST ($) CHOSEN 
I 10-24 18:46:41 optimizer.py:909] ----------------------------------------------------------------------------------------------------
I 10-24 18:46:41 optimizer.py:909] Kubernetes 2CPU--8GB--8H100 2 8 H100:8 kubernetes 0.00 ✔ 
I 10-24 18:46:41 optimizer.py:909] ----------------------------------------------------------------------------------------------------
I 10-24 18:46:41 optimizer.py:909] 
Launching a new cluster 'llama31'. Proceed? [Y/n]: Y
I 10-24 18:46:53 cloud_vm_ray_backend.py:4327] Creating a new cluster: 'llama31' [2x Kubernetes(2CPU--8GB--8H100, {'H100': 8})].
I 10-24 18:46:53 cloud_vm_ray_backend.py:4327] Tip: to reuse an existing cluster, specify --cluster (-c). Run `sky status` to see existing clusters.
I 10-24 18:46:54 cloud_vm_ray_backend.py:1313] To view detailed progress: tail -n100 -f /Users/alexkim/sky_logs/sky-2024-10-24-18-46-36-728907/provision.log

# Step 4: Monitoring trainingStep 4: Monitoring training

- Optionally, access Grafana dashboards:

kubectl --namespace o11y port-forward service/grafana 8080:80

To access the Grafana dashboard, open your browser and go to http://localhost:8080 (default username and password: admin).

2. Monitor training logs:

sky logs llama31

3. Open Weights & Biases web UI and find your project.

We see two runs, because each training node logs its own run, and we have two nodes in our cluster.

You can customize the charts to show any plots that you care about such as loss function, disk utilization, etc.

# Step 5: (optional) Transfer the fine-tuned model to Object StorageStep 5: (optional) Transfer the fine-tuned model to Object Storage

To save the fine-tuned model, transfer files from sha to an S3-compatible Nebius’ Object Storage:

- 

SSH into the SkyPilot cluster: ssh llama31

- 

Inside the cluster, run:

# See https://docs.nebius.com/iam/service-accounts/access-keys/#configure
# on how to obtain the required credentials

aws configure set aws_access_key_id "${NEBIUS_ACCESS_KEY_ID}"
aws configure set aws_secret_access_key "${NEBIUS_SECRET_ACCESS_KEY}"
aws configure set region 'eu-north1'
aws configure set endpoint_url 'https://storage.eu-north1.nebius.cloud:443'
aws s3 cp /mnt/data/$MODEL_SIZE-lora-output \
 s3://your-nebius-bucket/$MODEL_SIZE-lora --recursive

Alternatively, this command could be added at the end of the run section of the SkyPilot task configuration for automatic upload post-training.

# Step 6: Clean upStep 6: Clean up

- 

Delete the SkyPilot cluster: sky down llama31

- 

Delete the Terraform cluster:

# ensure you're in the `nebius-solution-library/k8s-training` directory
terraform destroy

# Step 7: (optional) Serve your fine-tuned model on Nebius AI StudioStep 7: (optional) Serve your fine-tuned model on Nebius AI Studio

Note

Nebius AI Studio is now Nebius Token Factory: same platform, new name, more power for running AI at scale.

After fine-tuning your LLMs with LoRA adapters, you may need a platform to host them for scalable and efficient inference. Nebius AI Studio is designed specifically for this purpose. It provides the most cost-efficient inference of open-source models with per-token pricing on the market. Supporting more than 30 base models, Studio allows you to perform inference at any scale. The infrastructure automatically adapts to your needs based on your current load.

Nebius AI Studio includes a per-token inference feature for LoRA adapters, currently available in preview mode. You can request access to this feature via the Studio interface. Integrating this capability enables you to streamline the deployment of your fine-tuned models, guaranteeing both scalability and cost-effectiveness in production environments.

# Additional SkyPilot tipsAdditional SkyPilot tips

### 1. Checking SkyPilot job queue and cancelling jobs1. Checking SkyPilot job queue and cancelling jobs

To view the current job queue in SkyPilot:

$ sky queue
Fetching and parsing job queue...

Job queue of cluster llama31
ID NAME SUBMITTED STARTED DURATION RESOURCES STATUS LOG 
1 - 10 mins ago 10 mins ago 10m 11s 2x[H100:8] RUNNING ~/sky_logs/sky-2024-10-24-18-46-36-728907 

To cancel a specific job: sky cancel JOB_ID

### 2. SSH into master and worker nodes2. SSH into master and worker nodes

To SSH into the master node of a SkyPilot cluster:

ssh <CLUSTER_NAME>
# example
ssh llama31

To SSH into a specific worker node:

ssh <CLUSTER_NAME>-worker<WORKER_ID>
# example
ssh llama31-worker1

### 3. Using environment variables3. Using environment variables

Set environment variables in your SkyPilot tasks using the env field in the YAML configuration:

envs:
 MY_VAR: "my_value"
run: |
 echo $MY_VAR

SkyPilot exposes several environment variables that can be useful for distributed training:

- 

SKYPILOT_NODE_RANK: rank (an integer ID from 0 to num_nodes-1) of the node executing the task.

- 

SKYPILOT_NODE_IPS: a string of IP addresses of the nodes reserved to execute the task, where each line contains one IP address.

- 

SKYPILOT_NUM_NODES: number of nodes reserved for the task. Same value as echo $SKYPILOT_NODE_IPS | wc -l.

- 

SKYPILOT_NUM_GPUS_PER_NODE: the same as the count in accelerators: <name>:<count> (rounded up if a fraction).

- 

MASTER_ADDR: The IP address of the head node.

### 4. Mounting storage buckets4. Mounting storage buckets

And finally, SkyPilot supports mounting cloud storage buckets:

# Mount an existing S3 bucket
file_mounts:
 /my_data:
 source: s3://my-bucket/ # or gs://, https://

## Resources

Nebius docs​
Solution Library​
Finetune Llama 3.1 on Your Infra​
SkyPilot docs​

## Explore Nebius

Cloud log in​
Token Factory log in​
Support​

Alexander Kim
Cloud Solutions Consultant

## See also

### 

Orchestrating LLM fine-tuning on K8s with SkyPilot and MLflow

While many focus on the modeling aspects during LLM fine-tuning, efficiently managing compute and experiment tracking is equally crucial. This guide demonstrates how to effectively leverage SkyPilot and MLflow, two powerful open-source tools, to orchestrate LLM fine-tuning jobs.

January 15, 2025
7 mins to read

### 

Q4: Nebius cloud updates

After completing a full rewrite of our cloud from the ground up in October, we began improving the foundation that we brought to the market. The features and tools we have introduced since then span our entire range of cloud services, from Compute Cloud with NVIDIA accelerated computing in a new region, to managed MLOps solutions.

December 18, 2024
4 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
