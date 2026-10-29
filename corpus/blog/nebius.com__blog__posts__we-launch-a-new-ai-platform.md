# We’re launching a new Nebius platform built from the ground up

Source: https://nebius.com/blog/posts/we-launch-a-new-ai-platform

Skip to main content

When we first launched Nebius, we started by using what we had learned from building a general public cloud, which helped us get up and running quickly. Now we see better ways to do things, so we have built a brand new, efficient and user-friendly AI cloud platform.

Our new platform features a faster storage backend, support for new GPUs and our latest ML services, better observability and a more intuitive UI. With a strong focus on AI needs, it provides enthusiasts and ML practitioners with robust, functional environments for their ambitious initiatives. By the way, we sometimes call it Newbius, the new Nebius, you know.

### Faster storage for better performanceFaster storage for better performance

Storage is crucial — especially for ML training. To better support AI workloads, we’ve made technical tweaks and low-level upgrades to our file storage, boosting performance to up to 100 GBps and 1M IOPS for aggregated read operations. Here’s what’s changed:

- 

We increased filesystem throughput by removing architectural bottlenecks in its internal structure.

- 

Our file storage now has higher read throughput and lower latency thanks to extending the minimum data chunk size. These improvements reduce IO to CPU, freeing up computational resources.

- 

We redesigned the way files and their metadata are transferred to the Filestore, making it faster with parallel downloading.

- 

Optimized settings now allow for faster work with PyTorch DataLoader.

These changes ensure seamless data streaming during model training and prevent disruptions when saving checkpoints, uploading model code or sharing model weights across cluster nodes.

### New GPUs, new possibilitiesNew GPUs, new possibilities

The new platform allows access to NVIDIA H200 Tensor Core GPUs, which are coming to our server racks these days. Stay tuned to learn more about these offerings.

Figure 1. The NVIDIA HGX H200 supercomputing platform. For reference

We’ve also implemented several network changes defining how our cloud communicates with our physical sites, paving the way for the smooth integration of new data centers into our infrastructure.

### Easier access to ML servicesEasier access to ML services

We’ve recently launched two new managed services to improve our customer’s ML operations: Managed Spark™ and Managed MLflow. Both are now available on our new console.

Managed Service for Apache Spark is a fully managed data processing engine designed to simplify and accelerate data engineering and ML workloads. Apache Spark is renowned for its speed and ease of use in big data processing.

Managed Service for MLflow is a fully managed, industry-leading tool for managing the ML lifecycle. It collects and stores key metrics and parameters of machine learning iterations, tracks experiment runs and helps distill the best-performing models for further deployment.

Figure 2. Managed MLflow parameters on the new cloud platform

### Improved observabilityImproved observability

We’ve made significant improvements to observability on the new platform. You now have real-time access to key hardware metrics on service dashboards. There’s no need to connect external tools like Grafana — everything you need is at your fingertips.

Figure 3. Monitoring dashboard for GPU metrics

For example, you can monitor GPU parameters such as GPU utilization, memory utilization, frame buffer usage, SM clock, memory clock and more. Additionally, we’ve developed a dashboard for our object storage, displaying the key bucket parameters like read requests, modify requests, traffic, object count, space by object type and total bucket size.

### A more intuitive user experienceA more intuitive user experience

Our UI changes reflect a focus on what’s important. We’ve restructured cloud entities in the new console to make the overall experience smoother and more intuitive, with fewer distractions and clicks required to get things done.

Additionally, we’ve added quick access to support and documentation, enabling our users to spend less time on service configuration and troubleshooting.

### Self-service GPU cloud for AI enthusiastsSelf-service GPU cloud for AI enthusiasts

At Nebius, we’re building a future-proof cloud platform for everyone. We understand how frustrating waiting lists and limited GPU availability can be — they can disrupt product roadmaps, production momentum and stakeholder expectations.

Our goal is to democratize access to modern GPUs for all AI and ML enthusiasts, regardless of company size or industry. With our in-house LLM R&D team, custom hardware design of servers and racks, profound engineering expertise and strong vendor partnerships, we’ve created a unique, self-service approach to GPU infrastructure. Now, you can sign in and gain faster access to GPUs with minimal commitments, reducing time-to-value and strengthening the competitive edge of your AI endeavors.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

## See also

### 

Introducing Nebius AI Studio: Achieve fast, flexible inference today

Our new platform not only allows application builders to use generative AI without significant effort but does so at a fraction of the cost. Our goal is to democratize access to cutting-edge AI technologies, enabling businesses of all sizes to innovate and compete in the AI space.

September 30, 2024
4 mins to read

### 

In-house AI R&D: Nebius’ secret ingredient for truly AI‑centric cloud

It wouldn’t be possible for us to build a machine-learning platform without advancing in the field ourselves.

July 29, 2024
9 mins to read

### 

Nebius launches its first availability zone in France

Our Paris availability zone will be one of the first in Europe to offer NVIDIA H200 Tensor Core GPUs. This is just the beginning as we continue to expand our operational capacity to meet fast-growing demand for high-quality infrastructure and the latest GPUs from AI builders around the world.

September 25, 2024
2 mins to read

Sign in to save this post
Sign In
