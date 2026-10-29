# Nebius extends immediate access to NVIDIA Hopper GPUs

Source: https://nebius.com/blog/posts/extending-immediate-access-to-nvidia-hopper-gpus

Skip to main content

### Pushing limits for AI enthusiastsPushing limits for AI enthusiasts

We’ve collected and analyzed user requests over the last nine months since the launch of self-service access in April. We noticed that most users consume more GPU compute than we provide instantly available by default. From the user perspective, extending compute quotas is not difficult, but it brings additional friction and weakens the scalability potential. Moreover, the approval process takes time, which is critical in the world of competitive AI companies and valuable GPU compute.

We’ve estimated that increasing quotas accelerates resource access for about 80% of our self-service users. It also opens up possibilities and brings more freedom for those who need quick access to a side training environment or extra space for ML experiments. Whatever it is, we’ve got you covered.

### What’s newWhat’s new

This update introduces instant access to NVIDIA L40S GPUs and NVIDIA H200 GPUs, making them available via the console for everyone. Another major change is the availability of up to 16 NVIDIA H100 GPUs (2 nodes interconnected with NVIDIA Quantum InfiniBand). This significantly increases the range of workloads that can be launched right away.

We also increased quotas for RAM, CPU, and storage to better align with the introduced GPU configuration.

 | Compute resource 　　　　　　　　　　　 
 | Region
 | Before
 | After

 | NVIDIA H100 GPU
 | Mäntsälä (eu-north)
 | 8 GPUs
 | 16 GPUs

 | NVIDIA L40S GPU
 | Mäntsälä (eu-north)
 | 0
 | 2 GPUs

 | NVIDIA H200 GPU
 | Paris (eu-west)
 | 0
 | 8 GPUs

 | vCPU
 | All
 | 176
 | 400

 | RAM
 | All
 | 1750 GiB
 | 5000 GB

 | Shared Filesystem
 | All
 | 500 GB
 | 2 TB

 | Network disks*
 | All
 | 500 GB
 | 2 TB

 | Object Storage
 | All
 | 10 TB
 | 10 TB

﹡Default quota is not applied for Network HDDs and only covers SSD options.

Please note that default quotas are subject to change and might be adjusted based on compute availability in each specific region.

### Getting startedGetting started

These increased quotas are already in place for everyone. Sign up to the console and enter your billing details to get started. If your project needs a substantial amount of GPU compute from the start, contact us through the request form for a special offer.

Feel free to reach out to our customer support if you need any guidance on quotas or encounter any technical issues.

## Explore Nebius

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

Nebius opens pre-orders for NVIDIA Blackwell GPU-powered clusters

We are now accepting pre-orders for NVIDIA GB200 NVL72 and NVIDIA HGX B200 clusters to be deployed in our data centers in the United States and Finland from early 2025. Based on NVIDIA Blackwell, the architecture to power a new industrial revolution of generative AI, these new clusters deliver a massive leap forward over existing solutions.

December 4, 2024
3 mins to read

### 

Meet SDKs for Go and Python

Today, we are happy to announce that our SDKs for Go and Python are now generally available to all users. This major update in programmatic interfaces brings more flexibility for MLOps teams and AI developers.

January 24, 2025
2 mins to read

### 

DeepSeek R1 and V3: Chinese AI New Year started early

If you think New Year celebrations started on January 1, it depends on how you look at it — because in the AI world, the real fireworks went off in December with the release of DeepSeek V3. Now, DeepSeek R1 is lighting up the sky with open-source brilliance that’s making even the most entrenched Silicon Valley giants feel the heat.

January 27, 2025
5 mins to read

* “Python” and the Python logos are trademarks or registered trademarks of the Python Software Foundation, used by Nebius B.V. with permission from the Foundation.

Sign in to save this post
Sign In
