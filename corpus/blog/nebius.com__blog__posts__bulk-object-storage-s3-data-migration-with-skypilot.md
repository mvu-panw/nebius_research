# Bulk Object Storage data migration with SkyPilot

Source: https://nebius.com/blog/posts/bulk-object-storage-s3-data-migration-with-skypilot

Skip to main content

Moving terabytes of data between S3 buckets sucks. It’s slow, it breaks halfway through and then you’re stuck wondering which files were actually migrated. I’ve been there — running a single-threaded script for days, only to have it fail at 87 percent completion. Then starting over because who has time to figure out which files transferred successfully? There’s got to be a better way.

Turns out, there is! It involves SkyPilot and a powerful tool called s5cmd. But before we dive in, let’s be clear: this is a cool hack for certain use cases more than it is a recommended production solution for data migration scenarios. In particular, there are limitations if there are extremely large files or datasets with millions of small files.

# The S3 migration problem we don’t talk aboutThe S3 migration problem we don’t talk about

Everyone’s moving data between clouds these days, but we don’t often talk about how painful it is. The standard approaches all have issues:

- 

AWS CLI: Kind of slow (try moving 50 TB with aws s3 sync and watch your hair turn gray) and, crucially, it doesn’t support cross-account transfers by using different profiles.

- 

Custom scripts: You’ll spend more time debugging edge cases than transferring data (especially for cross-account scenarios).

- 

Managed services (e.g., DataSync): Often expensive and/or vendor-locked.

What if we could distribute the work across multiple machines? That’s where SkyPilot comes in.

# SkyPilot + Nebius: New BFFsSkyPilot + Nebius: New BFFs

SkyPilot recently integrated with Nebius AI Cloud, giving us an easy way to spin up distributed compute resources. While primarily designed for AI workloads, it’s perfect for our data transfer needs.

The best part? While we’re focusing on Nebius as the target, this approach works with literally any S3-compatible storage. No vendor lock-in here!

A small note: there’s an awesome open-source project called Skyplane that was designed specifically for object storage transfers, but it’s been gathering digital dust for the last couple of years. Our approach is built on tools that are actively maintained.

# The secret sauce: s5cmd and RAM diskThe secret sauce: s5cmd and RAM disk

One of the biggest advantages of our approach is the ability to handle cross-account transfers easily.

Here’s the hack that makes this all work — a combination of:

- 

SkyPilot for orchestration: Manages cluster provisioning and distribution.

- 

s5cmd for transfers: A blazing fast S3 client.

- 

RAM disk for temporary storage: Eliminates disk I/O bottlenecks.

- 

GNU parallel: Efficiently manages concurrent transfers.

This approach gives us:

- 

Distributed workload across multiple nodes

- 

Parallel processing within each node

- 

Memory-speed temporary storage

- 

Error handling and post-transfer verification

# How it actually works (the nerdy details)How it actually works (the nerdy details)

Here’s the play-by-play of what happens:

- 

SkyPilot provisions your migration cluster on Nebius.

- 

Each node mounts a RAM disk for temporary storage.

- 

The head node lists all objects in the source bucket.

- 

That list gets evenly split (by count, not by size) into chunks among all worker nodes.

- 

Each node processes its chunk in parallel.

- 

Everything gets verified, with detailed reporting at the end.

Let’s look at some of the key code pieces that make this work:

# Mount RAM disk for temporary storage
sudo mount -t tmpfs -o size=8g tmpfs /mnt/ramdisk
mkdir -p /mnt/ramdisk/s3migration/temp

This is crucial — by using RAM instead of disk for temporary storage, we eliminate the I/O bottleneck that often plagues transfer operations.

The head node distributes work by splitting object lists:

# Split files by node using modulo on line number
for i in \
$(seq 0 \
$((NUM_NODES-1))); do
 awk -v node= \
 $i -v nodes= \
 $NUM_NODES 'NR % nodes == node' 
 $TEMP_DIR/filtered_objects.txt > 
 $TEMP_DIR/node_ \
 ${i}_objects.txt
 # ...
done

Then, each worker processes its assignments with high concurrency:

cat $TEMP_DIR/my_objects.txt | parallel -j \
$NUM_CONCURRENT process_object

The verification step ensures nothing was lost:

# Compare counts
SOURCE_COUNT= \
$(wc -l < \
$TEMP_DIR/final_source_files.txt)
TARGET_COUNT= \
$(wc -l < \ 
$TEMP_DIR/final_target_files.txt)

if [ \
$SOURCE_COUNT -eq \ 
$TARGET_COUNT ]; then
 echo "✅ Migration completed successfully! Object counts match."

 # Even if counts match, check for differences in file lists
 if diff \ 
 $TEMP_DIR/source_keys.txt \
 $TEMP_DIR/target_keys.txt > \
 $TEMP_DIR/diff_output.txt; then
 echo "✅ All objects match between source and target buckets."
 else
 echo "⚠️ Warning: Although counts match, some objects differ between buckets."
 # ...
 fi
fi

# Getting started: A complete setup guideGetting started: A complete setup guide

Let’s walk through the entire setup process, step by step.

### Set up the Nebius CLI and credentialsSet up the Nebius CLI and credentials

First, you need to install the Nebius CLI. Then, download the Nebius setup script:

wget https://raw.githubusercontent.com/nebius/nebius-solution-library/refs/heads/main/skypilot/nebius-setup.sh
chmod +x nebius-setup.sh
./nebius-setup.sh

When prompted, select your Nebius tenant and project ID from the list. The script will create the required credentials expected by SkyPilot.

### Install SkyPilot with Nebius supportInstall SkyPilot with Nebius support

Next, install SkyPilot with Nebius integration:

pip install "skypilot-nightly[nebius]"

Verify it’s working:

sky check nebius
> Checking credentials to enable clouds for SkyPilot.
🎉 Enabled clouds 🎉
 Nebius [compute, storage]
Using SkyPilot API server: http://127.0.0.1:46580

### Download the migration script and SkyPilot YAMLDownload the migration script and SkyPilot YAML

Clone the repository with the migration scripts:

git clone https://github.com/nebius/nebius-solution-library.git
cd nebius-solution-library/skypilot/s3-migration

### Configure your credentialsConfigure your credentials

Ensure you have AWS credentials configured for both the source and target buckets:

# For source bucket (e.g., AWS)
aws configure --profile default
# For target bucket (Nebius)
aws configure --profile nebius

### Launch your transfer jobLaunch your transfer job

Now, you’re ready to launch:

export SOURCE_AWS_PROFILE=default
export SOURCE_ENDPOINT_URL=https://s3.us-east-1.amazonaws.com # change to your region
export SOURCE_BUCKET=s3://source-bucket

export TARGET_AWS_PROFILE=nebius
export TARGET_ENDPOINT_URL=https://storage.eu-north1.nebius.cloud:443 # change to your region
export TARGET_BUCKET=s3://target-bucket

sky launch -c migration s3_migration.yaml \
 --env SOURCE_AWS_PROFILE \
 --env SOURCE_ENDPOINT_URL \
 --env SOURCE_BUCKET \
 --env TARGET_AWS_PROFILE \
 --env TARGET_ENDPOINT_URL \
 --env TARGET_BUCKET

This will:

- 

Provision the specified resources on Nebius (by default, eight nodes with 16 CPUs each).

- 

Set up the environment with all dependencies.

- 

Mount your AWS credentials.

- 

Start the distributed transfer process with 16 concurrent transfers per node.

# Performance tuningPerformance tuning

You can adjust several parameters to optimize performance:

- 

Number of nodes: Change num_nodes: 8 in the YAML file, to scale out more.

- 

Concurrency: Modify NUM_CONCURRENT: 16, to control parallel transfers per node.

- 

RAM disk size: Adjust the size=8g in the mount command for larger files.

- 

CPUs per node: Change cpus: 16 in the Resource section.

For extremely large transfers (millions of files), consider changing the post-transfer verification to use sampling instead of checking every file, by modifying the script.

# Benchmark: ImageNet-scale transfer performanceBenchmark: ImageNet-scale transfer performance

To evaluate data transfer performance across clouds and regions, we recreated the 70 GB ImageNet-style dataset that was used in the original Skyplane benchmark. This synthetic dataset was generated by using the following command:

for i in $(seq 1 1152); do 
 dd if=/dev/urandom of="dummy_file_$i.dat" bs=1M \
 count= $((70*1024/1152)) 
done

We then ran several transfer scenarios using S3-compatible endpoints and compared the timings with Skyplane’s published benchmarks.

### Test scenarios and resultsTest scenarios and results

 | Transfer type
 | Source
 | Target
 | Time

 | Intra-region (Nebius)
 | eu-north1
 | eu-north1
 | 26 sec

 | Inter-cloud
 | AWS us-east-1
 | Nebius eu-north1
 | 146 sec

 | Inter-cloud
 | Nebius eu-north1
 | AWS us-east-1
 | 53 sec

 | Skyplane (reference)
 | Various multi-cloud pairs
 | Various
 | ~19–28 sec

 | AWS DataSync (reference)
 | AWS to GCP/AWS
 | Various
 | ~300–422 sec

### ObservationsObservations

- 

Nebius intra-region performance is comparable to Skyplane’s fastest results, clocking in at just 26 seconds.

- 

Cross-cloud transfer from AWS to Nebius (across continents) completed in 2 minutes 26 seconds, significantly outperforming AWS DataSync, which took up to 7 minutes for similar long-haul transfers.

- 

Skyplane remains the top performer for optimized, cross-cloud transfers, but unfortunately it only supports AWS, GCP, Azure and Cloudflare. Since the project is stale, I doubt there’ll be support for other S3-compatible storage solutions anytime soon.

# Comparison to other optionsComparison to other options

 | Solution
 | What’s good
 | What’s not

 | Our s5cmd + SkyPilot solution
 | Distributed, works across clouds, performs post-migration verification
 | Requires some initial setup

 | Skyplane
 | Purpose-built for S3, extremely fast, uses compression and bandwidth tiering
 | Abandoned project

 | AWS DataSync
 | Managed service
 | AWS-specific and costs money

 | Manual S3 CLI
 | Simple, everybody knows it
 | Slow, no distribution, no cross-account support with different profiles

# The bottom lineThe bottom line

By combining SkyPilot, s5cmd and some clever distribution techniques, we have a data transfer solution that’s:

- 

Fully open-source

- 

Way faster than single-machine approaches

- 

Reliable with built-in verification

- 

Works with any S3-compatible storage

But remember: this is more of a cool hack than a recommended production solution for all scenarios — there are limitations.

Next time you need to move lots of data between object stores, give this approach a try if your use case fits. You can also use it with minimal changes to move data from external S3 to Nebius object storage.

The full code is available in the Nebius solution library repository. Clone it, improve it, let us know how it works for you!

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Alexander Kim
Cloud Solutions Consultant

Contents

- The S3 migration problem we don’t talk about

- SkyPilot + Nebius: New BFFs

- The secret sauce: s5cmd and RAM disk

- How it actually works (the nerdy details)

- Getting started: A complete setup guide

- Set up the Nebius CLI and credentials

- Install SkyPilot with Nebius support

- Download the migration script and SkyPilot YAML

- Configure your credentials

- Launch your transfer job

- Performance tuning

- Benchmark: ImageNet-scale transfer performance

- Test scenarios and results

- Observations

- Comparison to other options

- The bottom line

## See also

### 

Using SkyPilot and Kubernetes for multi-node fine-tuning of Llama 3.1

When adapting a large language model to your domain or specialized application, you want efficiency and a certain degree of simplicity. The setup of Managed K8s plus SkyPilot we’re going to run through today provides exactly that, albeit not as the only option. Meta Llama-3.1-8B is just an example here — you can apply a similar method to many other LLMs.

January 20, 2025
7 mins to read

### 

Orchestrating LLM fine-tuning on K8s with SkyPilot and MLflow

While many focus on the modeling aspects during LLM fine-tuning, efficiently managing compute and experiment tracking is equally crucial. This guide demonstrates how to effectively leverage SkyPilot and MLflow, two powerful open-source tools, to orchestrate LLM fine-tuning jobs.

January 15, 2025
7 mins to read

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

Sign in to save this post
Sign In
