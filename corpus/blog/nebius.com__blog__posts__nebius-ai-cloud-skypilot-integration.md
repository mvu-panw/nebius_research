# Nebius AI Cloud is now integrated with SkyPilot

Source: https://nebius.com/blog/posts/nebius-ai-cloud-skypilot-integration

Skip to main content

We’re excited to announce our integration with SkyPilot, an open-source framework that simplifies running AI and batch workloads across cloud platforms. This collaboration enables direct access to Nebius AI Cloud resources via SkyPilot. If you’re already using SkyPilot or considering it as a solution for your workloads, you can now conveniently use our AI Cloud through the same interface. It’s yet another way to access Nebius — alongside our API, CLI, Terraform recipes and others.

# What is SkyPilot?What is SkyPilot?

SkyPilot is a framework designed to optimize GPU availability and reduce costs when running AI workloads. It provides unified access to cloud resources through simple configuration files.

# How to use SkyPilot with Nebius AI CloudHow to use SkyPilot with Nebius AI Cloud

Setting up SkyPilot with Nebius AI Cloud is straightforward:

### Configure Nebius accessConfigure Nebius access

- 

Set up and configure Nebius CLI.

- 

Download the setup script nebius-setup.sh:

wget https://raw.githubusercontent.com/nebius/nebius-solution-library/refs/heads/main/skypilot/nebius-setup.sh

- Run the following commands:

chmod +x nebius-setup.sh 
./nebius-setup.sh

- You’ll be prompted to choose a Nebius tenant and project id from a list.

### Install SkyPilotInstall SkyPilot

Install SkyPilot with Nebius support:

pip install "skypilot-nightly[nebius]"

### Run your first jobRun your first job

Create a simple YAML configuration file named sky.yaml:

resources:
 cloud: nebius
 accelerators: H100:1
 region: eu-north1

file_mounts:
 /my_data:
 source: nebius://my-nebius-bucket # must be unique; replace with your own bucket name
 
setup: |
 echo "Setup will be executed on every `sky launch` command on all nodes"
 
run: |
 echo "Run will be executed on every `sky exec` command on all nodes"
 echo "Do we have GPUs?"
 nvidia-smi 
 echo "Do we have data?"
 ls -l /my_data

Launch your job:

$ sky launch -c sky-test sky.yaml
YAML to run: sky.yaml
Considered resources (1 node):
--------------------------------------------------------------------------------------------------------------
CLOUD INSTANCE vCPUs Mem(GB) ACCELERATORS REGION/ZONE COST ($) CHOSEN
--------------------------------------------------------------------------------------------------------------
Nebius gpu-h100-sxm_8gpu-128vcpu-1600gb 128 1600 H100:8 eu-north1 23.60 ✔
--------------------------------------------------------------------------------------------------------------

Launching a new cluster 'sky-test'. Proceed? [Y/n]: Y
⚙︎ Launching on Nebius eu-north1.
└── Instance is up.
✓ Cluster launched: sky-test. View logs: sky api logs -l sky-2025-02-27-11-36-07-257438/provision.log

⚙︎ Syncing files.
✓ Setup detached.

⚙︎ Job submitted, ID: 1
├── Waiting for task resources on 1 node.
└── Job started. Streaming logs... (Ctrl-C to exit log streaming; job will not be killed)
...
(setup pid=3800) Setup will be executed on every command on all nodes
(task, pid=3800) Command 'sky' not found, but can be installed with:
(task, pid=3800) sudo apt install beneath-a-steel-sky
(task, pid=3800) Run will be executed on every command on all nodes
(task, pid=3800) Do we have GPUs?
(task, pid=3800) Mon Mar 24 12:35:14 2025
(task, pid=3800) +-----------------------------------------------------------------------------------------+
(task, pid=3800) | NVIDIA-SMI 550.127.08 Driver Version: 550.127.08 CUDA Version: 12.4 |
(task, pid=3800) |-----------------------------------------+------------------------+----------------------|
(task, pid=3800) | GPU Name Persistence-M | Bus-Id Disp.A | Volatile Uncorr. ECC |
(task, pid=3800) | Fan Temp Perf Pwr:Usage/Cap | Memory-Usage | GPU-Util Compute M. |
(task, pid=3800) | | | MIG M. |
(task, pid=3800) |=========================================+========================+======================|
(task, pid=3800) | 0 NVIDIA H100 80GB HBM3 On | 00000000:8A:00.0 Off | 0 |
(task, pid=3800) | N/A 27C P0 67W / 700W | 1MiB / 81559MiB | 0% Default |
(task, pid=3800) | | | Disabled |
(task, pid=3800) +-----------------------------------------+------------------------+----------------------+

(task, pid=3800) +-----------------------------------------------------------------------------------------+
(task, pid=3800) | Processes: |
(task, pid=3800) | GPU GI CI PID Type Process name GPU Memory Usage |
(task, pid=3800) |=========================================================================================|
(task, pid=3800) | No running processes found |
(task, pid=3800) +-----------------------------------------------------------------------------------------+

(task, pid=3800) Do we have data?
(task, pid=3800) total 377487364
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:21 file_1
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:25 file_10
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:26 file_11
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:26 file_12
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:21 file_2
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:22 file_3
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:22 file_4
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:23 file_5
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:23 file_6
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:24 file_7
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:24 file_8
(task, pid=3800) -rw-r--r-- 1 ubuntu ubuntu 32212254720 Mar 10 14:25 file_9
(task, pid=3800) drwxr-xr-x 2 ubuntu ubuntu 4096 Mar 24 12:35 joblogs

✓ Job finished (status: SUCCEEDED).

Here’s a brief overview of what SkyPilot just did:

- 

Provisioned a Nebius AI Cloud instance.

- 

Mounted the my-nebius-bucket cloud bucket to /my_data on the VM.

- 

Executed the setup and run commands to verify GPU availability and access to the mounted data.

For more details, check out our docs.

# Multi-node exampleMulti-node example

High-performance NVIDIA Quantum InfiniBand connections make Nebius AI Cloud ideal for distributed training. Here’s a sample configuration for testing network connectivity:

resources:
 cloud: nebius
 accelerators: H100:8
 region: eu-north1
 
num_nodes: 2
 
setup: |
 sudo apt install perftest -y
 
run: |
 MASTER_ADDR=(echo"(echo "(echo"SKYPILOT_NODE_IPS" | head -n1)
 if [ "${SKYPILOT_NODE_RANK}" == "0" ]; then
 ib_send_bw --report_gbits -n 1000 -F > /dev/null
 elif [ "${SKYPILOT_NODE_RANK}" == "1" ]; then
 echo "Testing connection to: $MASTER_ADDR"
 sleep 2 # Wait for master to start
 ib_send_bw $MASTER_ADDR --report_gbits -n 1000 -F
 fi

$ sky launch -c test-sky sky.yaml
YAML to run: sky.yaml
Running on cluster: test-sky
⚙︎ Launching on Nebius eu-north1.
...

(worker1, rank=1, pid=33870, ip=192.168.0.15) ----------------------------------------------------------------
(worker1, rank=1, pid=33870, ip=192.168.0.15) Send BW Test
(worker1, rank=1, pid=33870, ip=192.168.0.15) Dual-port : OFF Device : mlx5_0
(worker1, rank=1, pid=33870, ip=192.168.0.15) Number of qps : 1 Transport type : IB
(worker1, rank=1, pid=33870, ip=192.168.0.15) Connection type : RC Using SRQ : OFF
(worker1, rank=1, pid=33870, ip=192.168.0.15) PCIe relax order: ON
(worker1, rank=1, pid=33870, ip=192.168.0.15) ibv_wr* API : ON
(worker1, rank=1, pid=33870, ip=192.168.0.15) TX depth : 128
(worker1, rank=1, pid=33870, ip=192.168.0.15) CQ Moderation : 1
(worker1, rank=1, pid=33870, ip=192.168.0.15) Mtu : 4096[B]
(worker1, rank=1, pid=33870, ip=192.168.0.15) Link type : IB
(worker1, rank=1, pid=33870, ip=192.168.0.15) Max inline data : 0[B]
(worker1, rank=1, pid=33870, ip=192.168.0.15) rdma_cm QPs : OFF
(worker1, rank=1, pid=33870, ip=192.168.0.15) Data ex. method : Ethernet
(worker1, rank=1, pid=33870, ip=192.168.0.15) ----------------------------------------------------------------
(worker1, rank=1, pid=33870, ip=192.168.0.15) local address: LID 0x1334 QPN 0x0131 PSN 0xcdddde
(worker1, rank=1, pid=33870, ip=192.168.0.15) remote address: LID 0x132f QPN 0x0131 PSN 0x90f79b
(worker1, rank=1, pid=33870, ip=192.168.0.15) ----------------------------------------------------------------
(worker1, rank=1, pid=33870, ip=192.168.0.15) #bytes #iterations BW peak[Gb/sec] BW average[Gb/sec] MsgRate[Mpps]
(worker1, rank=1, pid=33870, ip=192.168.0.15) 65536 1000 361.82 361.67 0.689839
(worker1, rank=1, pid=33870, ip=192.168.0.15) ----------------------------------------------------------------

✓ Job finished (status: SUCCEEDED).

# Next stepsNext steps

We’re committed to further enhancing this integration and welcome your feedback. To learn more about SkyPilot’s features and capabilities, visit the SkyPilot documentation and a dedicated section on our docs.

## Explore Nebius AI Cloud

Compute Cloud​
Managed Kubernetes​
Object Storage​
Managed PostgreSQL​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Kim
Cloud Solutions Consultant

Alex Salikov
Head of External Solutions Department

## See also

### 

Nebius and Outerbounds form strategic technology partnership through integration

We are excited to unveil our latest collaboration: Nebius AI Cloud, the ultimate cloud for AI innovators, and Outerbounds, an AI/ML platform powered by the popular open-source framework Metaflow, are now integrated as part of a broader technology partnership.

March 11, 2025
5 mins to read

### 

JupyterLab®: The first app in our new service for AI development

Today, we’re excited to announce that JupyterLab is now available in our Standalone Applications service, running on NVIDIA GPUs on our cloud platform. This fully managed offering eliminates infrastructure complexities, allowing you to focus entirely on your AI and machine learning (ML) projects.

March 27, 2025
3 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
