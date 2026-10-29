# World models: Request latency model serving with 42.5% more video at 5.5x the latency

Source: https://nebius.com/blog/posts/serving-world-models-latency-node-throughput

Skip to main content

Serving NVIDIA Cosmos 3 Super as eight single-GPU replicas on one NVIDIA HGX B200 node produced 42.5% more valid video per node-hour than one replica spanning all 8 GPUs, but at 5.5 times the mean request latency: 378.1 seconds versus 68.5. At the same hourly node price, that is 30% lower node cost per video-second.

We measured the text-to-video generator path of NVIDIA Cosmos 3 Super (nvidia/Cosmos3-Super), served through vLLM-Omni, across four serving topologies on NVIDIA HGX B200 and NVIDIA HGX H200 nodes on Nebius AI Cloud.

## Video-generation benchmarks need a node-level output metricVideo-generation benchmarks need a node-level output metric

A video-generation serving benchmark needs two metrics: request latency and node throughput. LLM inference stacks, such as those behind coding assistants, are typically optimized for time to first token and tokens per second. A synchronous video endpoint returns nothing until the clip is generated, encoded, and delivered as a finished file, so request latency runs from dispatch to the completed file.

NVIDIA’s Cosmos accelerates synthetic video generation and dataset augmentation workflows for robotics and autonomous systems. Because these workflows generate many clips, request latency tells only part of the story. A serving benchmark also needs to measure how much valid video the node produces over the full job. We define node throughput as technically validated video-seconds per node-hour.

We calculate node throughput by adding the duration of every clip that passes the validation gate, dividing that total by the job’s wall-clock time, and scaling the result to one hour. The clock starts when the first request is sent and stops when the final request finishes. Failed or rejected attempts add no video-seconds, but their time still counts toward the wall clock and lowers throughput.

A clip passes the gate only if the request succeeds and the resulting MP4 is non-empty, decodes fully, has the expected shape, and clears the blank-frame and frozen-frame checks. This gate confirms file integrity and basic motion. A separate quality evaluation is needed to judge prompt adherence, visual quality, temporal consistency, physical plausibility, realism, and training utility.

## Comparable benchmarks require a defined control setComparable benchmarks require a defined control set

Latency and node-throughput results are comparable only when the benchmark controls are clear. Video generation introduces many variables that can change both metrics, including the model, prompt, output shape, sampling settings, software stack, request schedule, timing boundary, and validation gate. For this benchmark, we fixed the model, software, input, and generation settings:

- 

Model: nvidia/Cosmos3-Super at one pinned revision

- 

Software: the vllm/vllm-omni:cosmos3 container (vLLM 0.25.0), pinned by digest

- 

Input: one fixed prompt and negative prompt, with three fixed random seeds used equally

- 

Generation: BF16, 1280 × 720 output, 189 frames at 24 frames per second, 35 denoising steps, and guardrails disabled

For each topology run, we sent 24 measured requests, each generating one clip from that prompt. Each replica completed one warmup request, then processed one request at a time. The measured window included routing, generation, MP4 encoding, and time spent waiting for the last replica to finish, and excluded startup, model loading, and warmup.

Our public benchmark method provides the exact workload, validation gate, model revision, container digest, software stack, and host configuration behind these runs. The full HGX B200 and HGX H200 records together contain 408 attempts, including the concurrency tests and repeat runs. All 408 passed the video-validation checks, so the gate did not change the throughput reported here.

## Serving topology controls how the node divides workServing topology controls how the node divides work

A serving topology specifies how many replicas run on the node, which GPUs each replica uses, and how each replica is parallelized. We tested four topologies, each using all 8 GPUs with a different replica count and parallel configuration.

The 8-GPU replica uses the layout the NVIDIA Cosmos 3 Super model card recommends for 8-GPU nodes, combining CFG parallelism, Ulysses-SP, and HSDP. The 4-GPU and 2-GPU replicas use tensor parallelism, as NVIDIA’s published Cosmos 3 benchmarks do for multi-GPU runs. Within a multi-GPU replica, each parallelism method divides a different part of the work:

- 

Tensor parallelism (TP) shards supported diffusion transformer (DiT) weights across GPUs. In these vLLM-Omni layouts, the text encoder remains replicated.

- 

Classifier-free guidance (CFG) parallelism runs the positive and negative guidance branches on separate GPUs.

- 

Ulysses sequence parallelism (Ulysses-SP) splits the video-token sequence across GPUs and redistributes attention tensors through all-to-all communication.

- 

Hybrid Sharded Data Parallel (HSDP) shards model weights across GPUs and gathers them as needed during each forward pass.

Figure 1. Every replica ran in its own vLLM-Omni container with a separate endpoint and a non-overlapping set of GPUs.

vLLM-Omni implements these layouts through its diffusion parallelism methods. A multi-GPU replica can lower per-request latency or pool enough GPU memory to serve a single request. Additional replicas let the node process more independent requests at once, while multi-GPU replicas add communication overhead between GPUs.

## Benchmark results: higher-output topologies had higher latencyBenchmark results: higher-output topologies had higher latency

Both platforms showed the same ordering: topologies with more replicas delivered more total video output but had higher request latency.

Moving from one 8-GPU replica to eight single-GPU replicas raised node throughput by 42.5% on Blackwell and 25.7% on Hopper. Mean request latency was 5.5 times as high on Blackwell and 6.3 times as high on Hopper.

Figure 2. Each point is one 24-request run on one node. The table below lists the exact values.

 | Topology
 | HGX B200 mean latency (s)
 | HGX B200 valid video-s/node-h
 | HGX H200 mean latency (s)
 | HGX H200 valid video-s/node-h

 | 1 replica × 8 GPUs
 | 68.5
 | 413.6
 | 123.3
 | 229.9

 | 2 replicas × 4 GPUs
 | 121.5
 | 466.3
 | 230.0
 | 245.6

 | 4 replicas × 2 GPUs
 | 212.4
 | 529.0
 | 416.5
 | 271.4

 | 8 replicas × 1 GPU
 | 378.1
 | 589.4
 | 779.0
 | 289.1

The Blackwell and Hopper runs used the same software stack and workload. Besides the GPU model and its memory capacity, the nodes differed in VBIOS, host CPU, and host memory, so the absolute performance gap compares complete systems, with the GPU as one of several parts that changed.

### More concurrency added latencyMore concurrency added latency

On Blackwell, with two requests in flight per replica, vLLM-Omni still ran one generation at a time and queued the second request. Node throughput rose by only 0.4% to 3.2%, below the 5% threshold we set in advance for a meaningful gain, while mean request latency increased by 32.9% to 48.8%.

For this workload and runtime, one request in flight per replica therefore delivered nearly the same node throughput at lower latency. The public HGX B200 results contain the per-topology deltas and repeat measurements.

## Run the benchmark on Nebius AI CloudRun the benchmark on Nebius AI Cloud

The open-source Nebius Physical AI Workbench runs this benchmark’s workload and four topologies on Nebius AI Cloud, with one workflow file for HGX B200 and one for HGX H200. Each workflow confirms the GPU type before measuring, reserves one full 8-GPU node, runs each topology in turn, and writes every request record and generated clip to object storage. We ran a complete HGX B200 benchmark with the Workbench and matched the published node throughput within 2.65% in all 10 tests, including the two-request and repeat runs. The Workbench’s request scheduling and timing boundary differ from our published method, so treat its latency as a separate measurement: with two requests in flight per replica, its mean latency ran 21% to 26% above our published values.

## Choose your topology based on the jobChoose your topology based on the job

For batch synthetic-data generation, where total output matters more than the wait for any one clip, eight single-GPU replicas produced the most valid video per node-hour. For interactive experiences, where a user waits for each clip to play, one 8-GPU replica returned each 720p, 189-frame video fastest, in a mean of 68.5 seconds on HGX B200. For a latency budget in between, run the most replicas whose mean latency fits it. Keep one request in flight per replica: on HGX B200, a second raised mean latency by up to 48.8% for at most 3.2% more throughput on this runtime. The ordering held on HGX H200, but absolute numbers differ by platform, so benchmark your own model and workload shape before committing a fleet.

Run the benchmark on Nebius AI Cloud with the Nebius Physical AI Workbench.

## AcknowledgmentsAcknowledgments

We thank NVIDIA’s Cosmos and performance teams for their input on benchmark controls and topology terminology.

Watch the NVIDIA and Nebius teams discuss these benchmarks on YouTube, including when extra replicas help and how to validate generated clips.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Stewart Tong
Director, Physical AI GTM

Timothy Le
Principal Technology Strategist - Physical AI

Contents

- Video-generation benchmarks need a node-level output metric

- Comparable benchmarks require a defined control set

- Serving topology controls how the node divides work

- Benchmark results: higher-output topologies had higher latency

- Run the benchmark on Nebius AI Cloud

- Choose your topology based on the job

## See also

### 

Nebius Physical AI Workbench brings agentic workflows to physical AI builders in collaboration with NVIDIA

Customers using Nebius Physical AI Workbench report up to 40% less engineering time with AI agents operating robotics workflows directly. Built in collaboration with NVIDIA and open source on GitHub, it runs data generation, simulation, training, and evaluation in one place. This release adds NVIDIA Cosmos Data Factory and a sim-to-real workflow co-designed with Sereact for Zalando returns.

October 21, 2026
5 mins to read

### 

Nebius Rated Platinum in SemiAnalysis ClusterMAX™ 3.0

SemiAnalysis has named Nebius a Platinum AI cloud provider, the top tier of its ClusterMAX™ 3.0 rating. The rating is based on live testing of production clusters: burn-ins, storage under concurrent load, and automated failure recovery on real NVIDIA GB300 and NVIDIA HGX B300 hardware. This post covers what the testing found and why it matters for teams choosing where to run production AI.

September 23, 2026
7 mins to read

### 

NVIDIA retail AI blueprints, now running on Nebius

Nebius has collaborated with NVIDIA to bring two retail AI blueprints to production on Nebius infrastructure: the NVIDIA Agentic Commerce Blueprint and the NVIDIA Retail Catalog Enrichment Blueprint for automated product content. Both are open-source reference architectures built on NVIDIA NIMs that retailers and developers can customize and deploy today with a 1-click deployment on Nebius AI Cloud.

June 5, 2026
5 mins to read

Sign in to save this post
Sign In
