# Behind SWE-rebench: Infrastructure to collect massive datasets of SWE tasks and evaluate agents at scale

Source: https://nebius.com/blog/posts/infrastructure-behind-swe-rebench

Skip to main content

Software engineering agents demonstrate strong coding capabilities and have rapidly become a major focus of research. However, large-scale experimentation with such agents remains technically challenging because each SWE task requires an executable software environment that involves building and running containers. These workloads quickly exceed single-machine capacity and demand distributed orchestration.

Nebius’ AI R&D team has been conducting research on SWE agents for over a year. During this period, we developed the infrastructure required to support experimentation at scale, including pipelines to collect and build datasets of SWE task instances (such as SWE-bench and SWE-rebench) and pipelines to run and evaluate various agent configurations on these large datasets. This capability has enabled the creation of the swe-rebench.com leaderboard as well as massive datasets of SWE task instances, such as nebius/SWE-rebench and nebius/SWE-bench-extra.

To foster broader progress in the field, we are beginning to share this scalable infrastructure with the research community. As an initial step, we are releasing support for TractoAI as a drop-in backend for SWE-bench eval in our swe-rebench/SWE-bench-fork, which is capable of evaluating thousands of SWE task instances per hour.

# SWE agents and their evaluationSWE agents and their evaluation

SWE agents first emerged in late 2023 and have since undergone nearly two years of rapid development. Notable examples include SWE-agent, OpenHands, Anthropic’s Claude Code, and OpenAI’s Codex.

In essence, an SWE agent is an LLM that is given access to a container with source code and tools such as a bash terminal, web search, and a browser — much like a human software engineer, but powered by an LLM. The agent runs in a loop: it generates a command (action) via the LLM, executes the command in a container, and feeds the output (observation) back to the LLM. The resulting sequence of actions and observations (a trajectory) is recorded for downstream analytics and training.

To compare the quality of SWE agents, we need reliable and automated methods to measure their performance. One widely adopted approach, first introduced in the SWE-bench paper [1], uses unit tests to automatically evaluate whether an agent’s solution is correct. Such (problem, test set) pairs can be mined from resolved GitHub issues, where the problem corresponds to the issue itself, and the tests can be extracted from the pull request that resolved it.

That is, the evaluation procedure is:

def eval_agent(agent, issue) -> bool:
 # run agent
 container = build_container(issue.repo, issue.base_commit)
 agent.run(container, issue.description)
 agent_patch = container.collect_patch()
 
 # evaluate agent's patch
 test_container = build_container(issue.repo, issue.base_commit)
 test_container.apply_patch(issue.test_patch)
 test_container.apply_patch(agent_patch)
 test_result = test_container.run(issue.test_command)
 return test_result.success

# Research ideas face the single-host limitResearch ideas face the single-host limit

We started our research on SWE agents back in mid-2024. Our ideas focused on scaling the training dataset [2] and on test-time compute scaling via search methods [3]. From an infrastructure perspective, this required pipelines to collect and build large datasets of SWE tasks, as well as a scalable runtime capable of running and evaluating SWE agents on this large dataset in a reasonable amount of time.

We began with the open-source implementations of SWE-bench (for data collection and evaluation) and SWE-agent (as the baseline agent) [5]. However, it quickly became clear that these implementations were not scalable, i.e., they were bound to a single machine:

- Data collection and preparation scripts lacked a distributed backend.

- Only local Docker was used to build images and run containers.

We needed to scale beyond a single machine to meet the demands of multiple researchers and iterate fast enough.

# Scaling beyond a single hostScaling beyond a single host

- To move beyond a single machine, we needed infrastructure that could:

- Mine and process vast amounts of GitHub data.

- Build thousands of Docker images for SWE tasks.

- Orchestrate thousands of agent runs and evaluations in parallel.

- Efficiently store and utilize the resulting data for downstream tasks.

### Treating codebases as executable dataTreating codebases as executable data

At first glance, the tasks above seem to come from DevOps — and that’s true. Historically, tasks such as code packaging, testing, and deployment have been part of the DevOps domain. But what makes it different now can be phrased as “cattle vs. pets” in DevOps terms:

- Normally, software engineers work with a relatively small number of repositories, each maintained carefully, treated more like a pet.

- By contrast, for SWE agents, repositories are data, counted in thousands and treated more like cattle.

In practice, this means existing DevOps technologies are designed to provide the best experience while working with a small set of repositories, whereas SWE agents need “batch DevOps”.

Meanwhile, machine learning has always dealt with data and data processing, and distributed systems have been built to process data on a large scale. Nonetheless, the use case of SWE agents introduces new challenges due to the executable nature of the data.

- Code repositories introduce a new data type; they need to be stored in tables and processed at scale using nontrivial and filesystem-intensive operations such as filter files, git log.

- Data processing systems often use containers to isolate operations, and identical containers are used to process all rows. By contrast, building and running containers for SWE tasks either implies using different container images for different SWE tasks or a container-in-container setup, which is nontrivial from an isolation perspective.

- Container images require a special type of storage — container registries — that is not typically a part of data processing systems.

In addition, agent execution on a set of SWE tasks introduces another set of challenges. For each SWE task, a sophisticated execution graph can be imagined. For instance, run an agent end to end N times and then perform best-of-N selection, or apply various search methods (e.g., beam search, Monte Carlo tree search) that require spawning up to K environment instances (containers) at each agent step.

### Building upon a robust stack: Kubernetes and TractoAIBuilding upon a robust stack: Kubernetes and TractoAI

Nebius AI R&D already had battle-tested large-scale infrastructure for LLM pre- and post-training: Kubernetes and TractoAI.

- We used Kubernetes + Volcano to orchestrate multi-node LLM training across 100+ machines.

- We used TractoAI — a web-scale data processing platform — to collect, process, and stream petabytes of data.

We found it possible to reuse this proven stack for SWE agents too. We ended up using:

- Kubernetes to orchestrate agent runs, as Kubernetes provides proper scheduling flexibility and scalability.

- TractoAI for everything else: to collect SWE tasks, build container images, evaluate agent solutions, and store agent trajectories. As a data processing platform, TractoAI is meant for data processing tasks, and it also comes with a built-in container registry needed to store container images of SWE tasks.

Below, we provide some technical details and challenges on both parts.

### Using Kubernetes to run agentsUsing Kubernetes to run agents

In practice, running an agent on a set of SWE tasks means running a script like: python run_agent.py --dataset nebius/SWE-rebench-leaderboard --llm Qwen3-Coder --max-threads 32 --runtime docker. This script reads a dataset of SWE tasks and spawns up to max-threads in parallel to process it. For every SWE task, the agent spawns an environment — a container with the proper Docker image — and then starts the action-observation loop.

We needed to support a scalable and flexible implementation of runtime. Since we already managed a Kubernetes cluster to run training and inference jobs, adding Kubernetes as a scalable agent runtime was a reasonable next step. It also enabled us to benefit from large GPU machines in our cluster, since their CPU and memory resources were underutilized, and we could deploy agents next to training and inference runs.

We ended up running up to 8,000 agent pods in parallel on our Kubernetes cluster, although it required engineering to make it robust.

#### Being in charge of the podsBeing in charge of the pods

A Pod is a minimal building block in Kubernetes, yet engineers rarely have to use it directly. Instead, Kubernetes offers built-in abstractions for common types of workloads: Deployment, DaemonSet, Job, etc. Each type of workload comes with its own controller that is responsible for managing its Pods and the lifecycle of the workload.

Nonetheless, in our case, we had to manage individual Pods directly in the scope of run_agent.py, and we used the Kubernetes SDK for Python for this. Although creating and deleting a Pod is not an issue, certain aspects were tricky:

- 

Proper timeouts on Pod state transitions. If an image for some SWE task is missing in the registry, the corresponding Pod may remain indefinitely in the Pending phase, effectively deadlocking the entire agent run. To prevent this, we introduced proper timeouts on Pod state transitions. While kubectl get pod displays rich Pod statuses (e.g., ContainerCreating, ErrImagePull), these are not actual Kubernetes API fields — they are inferred by kubectl at runtime from combinations of pod.status fields [source code]. Since the Kubernetes Python SDK does not provide this inference logic, we reimplemented it ourselves to track Pod progress accurately and apply the correct timeouts.

- 

Pod attribution. We run thousands of agent environment Pods in parallel, which belong to tens of agent runs across different experiments by multiple researchers. To keep the system explainable, we set various labels upon Pod creation (e.g., parent-pod, instance-id, airflow-run-id). Later, these labels are used for analytics and utility jobs.

- 

Zombie Pods. Since we are in charge of Pod allocation, proper Pod cleanup is also on us. run_agent.py may exit abruptly and bypass graceful cleanup. Then, many agent Pods may become “zombies” and stay in Kubernetes indefinitely while also consuming resources. To overcome this, we deployed a simple cron job to find and delete zombie Pods based on the parent-pod label.

- 

Retries. In distributed systems such as Kubernetes, anything can go wrong: for example, a Pod may disappear because the node went down. Normally, engineers add retries to handle such cases. But since agent runs are stateful and depend on the specific internal state of a Pod, we added higher-level retries that would restart the whole run of an SWE task from the beginning.

- 

Monitoring. Kubernetes doesn’t have any built-in observability system, Pod logs disappear once a Pod is deleted, and Kubernetes events disappear quickly. At our scale, this made debugging and performance analysis nearly impossible without a proper monitoring stack. To address this, we integrated our Kubernetes cluster with the Grafana-based Nebius observability platform. We enabled centralized collection of Pod logs, Kubernetes events, and cluster state metrics via kube-state-metrics. We also configured kube-state-metrics to export our custom pod labels (such as parent-pod, instance-id, and airflow-run-id). In addition, we instrumented the agent runner itself with custom metrics and traces to track run progress. Using these data sources, we built Grafana dashboards that provide a unified view of both system-level and experiment-level activity.

- 

Resource tuning. To ensure maximal cluster utilization while avoiding OOMs and throttling, we tuned environment Pod resource requests and limits based on monitoring: requests are set to the median CPU/memory usage, and limits are set to reasonable values for development environments, like 4 CPUs and 16 GB of memory.

### Using TractoAI for everything elseUsing TractoAI for everything else

#### What is TractoAI?What is TractoAI?

TractoAI is a unified compute and data processing platform for AI. It implements the MapReduce paradigm for data processing: map operations transform data rows, and reduce operations aggregate them.

At the heart of TractoAI is Cypress — a distributed file system, and a data-aware scheduler. Cypress can store petabytes of data across multiple machines with proper data redundancy, and it also enables efficient storage of tabular data in its own internal format. The data-aware scheduler automatically splits data into chunks and chooses the proper level of parallelism for processing.

#### Mining SWE tasks with executable environmentsMining SWE tasks with executable environments

We utilized various features of TractoAI to implement the SWE-bench pipeline at scale. More details can be found in our SWE-rebench paper [4].

- 

Data collection. We run TractoAI map jobs to ingest GitHub Archive (~21 TB uncompressed), clone GitHub repositories with full history (~32K repositories for SWE-rebench, ~1 TB), and store everything as Tracto tables.

- 

Data processing. We implement a set of map and reduce operations to process, enrich, and filter the data: join issues to their linked pull requests, filter repositories with permissive licences, filter pull requests that introduce new tests, split each pull request into a solution patch and a test patch, compute task metadata, etc. These operations involve many filesystem-intensive operations, such as git log and git diff. By the end of this step, we have a set of SWE task candidates (~153K for SWE-rebench) that still require an executable environment.

- 

Execution validation. We need to build an executable environment for each SWE task and ensure its validity. Every repository has its own installation and testing recipe (e.g., what Python version to use, how to install dependencies, and how to run the tests). First, we run a map job that uses an LLM to extract the recipe for each repository. Then, we run a map job that uses Buildah to build a container for each SWE task according to the recipe and run the unit tests to assess environment validity. We verify that the set of failing/passing unit tests before and after the patch from the PR is applied matches the historical data. All logs and test statuses are written to tables. After this step, we end up with a set of valid SWE tasks with an executable environment (~21K for SWE-rebench).

- 

Image building and storage. We run a map job that uses buildah to build and push the container images for SWE tasks that passed execution validation. The images are stored in TractoAI’s built-in, fully functional container registry on top of the Cypress filesystem. This also means that images can be treated as data; for example, we can use yt list //home/registry/swe-rebench | wc -l (or yt get //home/registry/swe-rebench/@count) to count all SWE-rebench images.

We faced some challenges along the way:

- 

High disk I/O. During our experiments, we realized that disk I/O operations are a bottleneck for code repository data processing. To overcome this, we used an in-memory filesystem (tmpfs; tmpfs in YTsaurus) and unpacked code repositories into tmpfs mounts during data processing.

- 

Containers inside jobs. Since Tracto jobs use containers for isolation, building and running containers inside jobs turned out to be a tricky container-in-container case. So we chose buildah, a rootless and daemonless tool to build container images. We also configured buildah to use tmpfs mounts as image storage due to high disk I/O and enabled the VFS filesystem, as other filesystems are not available inside containers without additional privileges.

- 

Rate limits from artifact registries. Public artifact registries — such as pypi.org, hub.docker.com, and archive.ubuntu.com — have rate limits, and we quickly hit them during execution validation and image building. To overcome this, we used internal mirrors of these registries.

#### Evaluation of agent solutionsEvaluation of agent solutions

In our setup, agent execution and evaluation are different steps of the pipeline. Agent execution produces a trajectory and a patch, which we store in tables on TractoAI. The evaluation job outputs another table with the overall resolved mark, logs, test statuses, etc.

At its core, solution evaluation is the execution of unit tests with the agent-generated patch applied. Normally, we evaluate thousands of agent solutions per experiment. For instance, we run an agent 5+ times for each SWE task to get a better estimate of agent quality; for the SWE-bench Verified dataset (500 SWE tasks), this results in 2,500+ solutions to evaluate.

Historically, we made several attempts to implement evaluation at scale, treating it as a batch job. The most complicated part was using different container images to evaluate different rows.

- 

Initially, we used Kubernetes. Although Kubernetes doesn’t support setting different images per job index, we adapted Volcano jobs for this, with 1 task in a job = 1 SWE task. But we experienced issues with huge job specs that exceeded the etcd entry size limit, so we manually split the dataset into smaller batches and ran them in a thread pool. We also had to distribute inputs and collect outputs for each task manually. On top of this, such large jobs occupied the entire Kubernetes cluster and prevented other workloads from running.

- 

Later, we migrated to TractoAI: we used vanilla operations, which are similar to Volcano jobs, to implement a job with multiple tasks where each task has its own image. Then, TractoAI handled data I/O and fair-share scheduling for us, and it collected logs and metrics. But since one vanilla operation can’t contain more than 100 tasks, we still had to split the dataset into smaller batches and run several vanilla operations in a thread pool, which isn’t optimal.

- 

Finally, we switched to TractoAI map jobs, which allowed us to completely offload management of parallelism to TractoAI. To run SWE task containers inside TractoAI jobs, we used Podman, a rootless and daemonless tool to run containers.

#### Kubernetes vs. TractoAI experienceKubernetes vs. TractoAI experience

Although we preferred Kubernetes for agent runs due to its flexibility, we realized that certain features of TractoAI made our lives easier for evals:

- 

Unified UI. TractoAI’s UI bridges compute and data. It’s easy to view table contents, jump from a table to an operation that produced it, and see all jobs in an operation with their statuses and logs. While some UIs for Kubernetes exist, they must be deployed separately and are not that convenient for batch and data workloads.

- 

Built-in monitoring. TractoAI automatically records useful metrics and real-time job logs during operation execution, stores them, and displays them in the UI. Compared to our experience with Kubernetes, we had everything needed to debug our jobs from day one without extra effort.

- 

Fair-share scheduling. TractoAI manages operation parallelism and ensures fair resource distribution among all operations and users in the cluster. This was a huge difference over our initial attempt with Kubernetes for evaluations, where one massive eval job could take all cluster resources and prevent other eval jobs and agent runs from proceeding.

- 

Built-in SQL-like query language. Since we stored all run artifacts as tables on TractoAI, we were able to perform ad-hoc analysis of these large datasets through a built-in SQL-like query language called YQL.

All in all, TractoAI let us implement the SWE-bench pipeline at scale while staying within one system at all stages.

# Sharing our infrastructure with the communitySharing our infrastructure with the community

Once the infrastructure was built, turning research ideas into experiments became much easier. nebius/SWE-rebench (21.3K SWE tasks), nebius/SWE-bench-extra (6.38K tasks), nebius/SWE-agent-trajectories (80K agent trajectories), and swe-rebench.com are all built upon the described infrastructure.

To foster broader progress in the field, we are beginning to share this scalable infrastructure with the research community. As an initial step, we are releasing support for TractoAI as a drop-in backend for SWE-bench eval in our swe-rebench/SWE-bench-fork, which is capable of evaluating thousands of patches per hour.

As of 2025-09-28, our implementation assumes the use of prebuilt Docker images (such images are available for SWE-bench Verified and SWE-rebench Leaderboard at minimum). We also release a script to import third-party images into the TractoAI registry for better eval performance. In our benchmarks, a full run of SWE-bench Verified (500 tasks) on the self-service TractoAI cluster (console.tracto.ai) completed in approximately 18 minutes, though the exact duration depends on current cluster load.

# Nebius research credits programNebius research credits program

Nebius is committed to supporting academic innovation by giving researchers access to AI Cloud or Token Factory through the Nebius research credits program.

## ContributorsSimon Karasik＊, Ibragim Badertdinov, Maksim Nekrashevich, Anton Shevtsov, Andrei Andriushchenko, Filipp Fisin, Sergey Abramov, Yury Anapolskiy＊＊, Daria Litvintseva＊＊

＊Correspondence to sbkarasik@nebius.com 
＊＊Work done while at Nebius

## Citation information
Please cite as:

 | Karasik et al., "Behind SWE-rebench: Infrastructure to collect massive datasets of SWE tasks and evaluate agents at scale", Nebius blog, 2025.

BibTeX citation:

 | @article{karasik2025agentinfastructure,
   title={Behind SWE-rebench: Infrastructure to collect massive datasets of SWE tasks and evaluate agents at scale},
   author={Karasik, Simon and Badertdinov, Ibragim and Nekrashevich, Maksim and Shevtsov, Anton and Andriushchenko, Andrei and Fisin, Filipp and Abramov, Sergey and Anapolskiy, Yury, and Litvintseva, Daria} year={2025},
   year={2025},
   journal={Nebius blog},
   note={}
 }

## References

- Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2023). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? . ArXiv: arxiv.org/abs/2310.06770 ↵ 

- Badertdinov et al. (2024), "Scaling data collection for training software engineering agents". Nebius blog: nebius.com/blog/posts/scaling-data-collection-for-training-swe-agents. ↵ 

- Zainullina, K., Golubev, A., Trofimova, M., Polezhaev, S., Badertdinov, I., Litvintseva, D., Karasik, S., Fisin, F., Skvortsov, S., Nekrashevich, M., Shevtsov, A., & Yangel, B. (2025) Guided Search Strategies in Non-Serializable Environments with Applications to Software Engineering Agents. ArXiv: arxiv.org/abs/2505.13652 ↵ 

- Badertdinov, I., Golubev, A., Nekrashevich, M., Shevtsov, A., Karasik, S., Andriushchenko, A., Trofimova, M., Litvintseva, D., & Yangel, B. (2025). SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents. ArXiv: arxiv.org/abs/2505.20411 ↵ 

- Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., & Press, O. (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. ArXiv: arxiv.org/abs/2405.15793 ↵ 

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

#### See the contributors

Contents

- 

SWE agents and their evaluation

- 

Research ideas face the single-host limit

- 

Scaling beyond a single host

- 

Treating codebases as executable data

- 

Building upon a robust stack: Kubernetes and TractoAI

- 

Using Kubernetes to run agents

- 

Using TractoAI for everything else

- 

Sharing our infrastructure with the community

- 

Nebius research credits program

- 

Contributors

- 

Citation information

## See also

### 

SWE-rebench dataset: More than 21,000 verifiable tasks for SWE agents

Our AI R&D team announces the open-source release of the SWE-rebench dataset of more than 21,000 real-world, interactive software engineering tasks. For a detailed methodology and technical report, please see our accompanying paper on arXiv.

June 10, 2025
1 min to read

### 

Kvax: Fast and easy-to-use FlashAttention implementation for JAX

Today, we’re open-sourcing Kvax, our FlashAttention implementation based on JAX. Designed for efficient training with long sequences, Kvax supports context parallelism and optimized computation of document masks. It outperforms many other FlashAttention implementations in long-context training with dense packing, achieving state-of-the-art performance.

February 27, 2025
13 mins to read

### 

Nebius achieves NVIDIA Exemplar Status on NVIDIA H200 GPUs for training workloads

We’re proud to announce that Nebius is one of the first NVIDIA Cloud Partners to achieve NVIDIA Exemplar Status on NVIDIA H200 GPUs for training workloads. This recognition validates that Nebius meets NVIDIA’s rigorous standards for performance, resiliency, and scalability — addressing one of the most pressing challenges in AI infrastructure: ensuring consistent workload performance and predictable cost across clouds.

September 29, 2025
3 mins to read

Sign in to save this post
Sign In
