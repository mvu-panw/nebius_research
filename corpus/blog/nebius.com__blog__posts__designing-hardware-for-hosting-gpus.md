# Designing hardware for hosting AI-tailored GPUs

Source: https://nebius.com/blog/posts/designing-hardware-for-hosting-gpus

Skip to main content

The creation of machine learning models powering intelligent products and services hinges heavily on powerful graphics cards. The ongoing deep learning surge owes its success to brilliant network designs and incredibly rich datasets. However, none of this would’ve been possible without powerful hardware. How well this hardware is attuned to AI tasks is also becoming increasingly important.

For our Nebius AI project, the new AI-centric cloud platform, we design and assemble servers specifically tailored for hosting modern GPUs like the NVIDIA H100. But what obstacles emerge when creating hardware tailored for machine learning, and how exactly this equipment graces the workplace environment of an ML engineer? For answers, we need to delve into the basics.

Training-oriented node designed and assembled by Nebius

## What makes GPUs so great at AI/ML tasks in the first placeWhat makes GPUs so great at AI/ML tasks in the first place

GPUs, as we know them today, emerged during the gaming industry’s 3D boom. 3D games demand constant calculation and recalculation of millions of polygons, the building blocks of an object. General-purpose processors — CPUs — work sequentially. They achieve parallelism by adding more cores, but there’s a physical limit to how many can fit on one chip. In contrast, GPUs deploy numerous smaller cores, adept at handling small models like polygons. All these cores work in tandem, allowing simultaneous calculations of hundreds of objects. While CPUs boast lightning-fast, yet limited cache memory, GPUs offer more memory, although it’s slower. For computing arrays of tiny objects, volume trumps speed, ensuring data reaches all these smaller cores efficiently.

Such concepts are similarly relevant to the tasks required to build modern AI models. Machine learning uses vast datasets, and GPUs excel at processing these. The data is split into chunks and distributed between the many GPU cores for parallel processing. Such computations can span across thousands of GPUs, with data transferred over the network. This is where the sizable memory of GPUs comes in handy, allowing large data chunks to be housed on one card. This capability is the reason why AI and ML experts gravitated towards GPUs. Advanced networks also enable data transfer directly between devices, bypassing the CPU, courtesy of RDMA (Remote Direct Memory Access) technology. This innovation made it possible to interconnect numerous GPUs and form clusters. Around the same time as RDMA got the necessary routing capabilities, NVIDIA introduced NVlink. This GPU interconnect allows multiple GPUs to share a pool of memory and addresses, slashing data transfer times between cards and bypassing the CPU entirely. NVLink paved the way for a new GPU format, SXM, which we’ll explore next.

## Interfaces to connect GPUs, and which of them are relevant for AIInterfaces to connect GPUs, and which of them are relevant for AI

Originally, all GPUs were designed in the PCIe format, a standard still favored by gaming GPUs and used for inference — real-time data processing via a “distilled” model that resulted from machine learning. However, in 2016, NVIDIA unveiled the SXM architecture, in which up to eight GPUs communicate via NVLink on a single PCB. The company refers to such servers as DGX, and to their derivatives as HGX. The latter are SXM GPU–equipped servers fashioned by various OEM/ODM companies, Nebius included. SXM, DGX, and HGX are emerging as the go-to hardware for AI/ML.

But when handling ML models that are particularly large, one server might not be enough. A standout feature of DGX and HGX servers is their interconnect over the network. They can be meshed into clusters, where each server communicates with all others. This approach enables creating and scaling significant computational power — exactly what ML demands. Standalone GPUs are already optimized for decentralized calculations, and when interconnected, they radically outperform other hardware, such as CPUs or FPGAs.

## Designing a GPU-specific rackDesigning a GPU-specific rack

With GPUs, the documentation for new hardware often lags behind its release. And while bleeding-edge chips might be the talk of the tech world, barely anyone gets to see them in person. Even if you manage to get your hands on a few new HGXs, you’ll be hard-pressed to find more, as they’ll be back-ordered for years to come.

New GPUs are implicitly expected to be paired with state-of-the-art CPUs, RAM, and networks. Everyone’s chasing the latest tech: right now, that’s stuff like DDR5 memory, PCI Express 5.0, and the InfiniBand 400 ND. However, these can be as elusive as the GPUs. Cloud providers are in a never-ending race, always trying to predict and prepare for the next big leap. If they don’t, they risk falling behind as their offerings might not align with the rapidly evolving client expectations.

You might think, “Why not just pop the brand-new GPU into our last-gen server rack?” Well, nice as that would be, it’s not that simple: sometimes, even slight variations, like different form factors (SXM5 vs. PCIe), can make the new GPUs entirely incompatible with legacy systems. Take the NVIDIA A100, for instance: it demanded more power than its predecessors, which meant that we needed customized hardware to prevent overheating and also to achieve the most efficient design both in thermal and power usage. That’s how our previous generation of racks came to be. These A100-equipped machines now fuel several world-class supercomputers. But as we all know, tech is in a constant state of evolution. Outfitted with PCI Express gen 5, DDR5 memory, and cutting-edge processor cores, the NVIDIA H100 represents a significant leap forward. Yet, integrating this new GPU is no easy feat.

## Transitioning to the NVIDIA H100Transitioning to the NVIDIA H100

Leaving aside fancy stuff like HGX, supercomputer configurations, and advanced interconnect, slotting the H100’s simpler PCIe form factor into a four-year-old server is doable, technically speaking. We’ve done it as an experiment, after a solid month of high-level software tweaks. But all this effort didn’t quite pay off. The bus connecting the GPUs to the CPUs was a bottleneck, and the server’s overall design constrained the much more sophisticated GPUs. Moving data around and getting it onto the GPU took longer, making tasks like AI training too much of a chore by today’s standards. With double the link speed, we were looking at transferring twice as much data both in and out.

But then there’s the electronics side of things. As we chase higher speeds, precise circuitry becomes our main concern. Modern PCBs blend novel materials and intricate components, adding layers of complexity to manufacturing, operation, and programming. Designing such advanced integrated circuitry demands in-depth, complex simulations.

Switching from PCI Express gen 4 to 5 comes with its own challenges. Interference we once brushed off as tolerable is now a deal-breaker. The complexity of motherboards increases as layer counts rise, and the benchmarks for material purity and quality grow more stringent.

Currently, we’re assembling an H100 GPU cluster using standard off-the-shelf HGX servers. Simultaneously, we’re developing our very own HGX design. To harness the H100’s full potential and allow it to operate at intended frequencies and modes, we’ve gone back to the drawing board with our rack design, placing the network front and center. Equally important, though, was to develop different solutions for specific AI tasks.

## Workload typesWorkload types

Our rack solutions are versatile and cater to a range high-end users. For supercomputer-grade tasks, we prioritize GPU power, rapid data delivery, and high interconnectivity. For use cases like MapReduce, it’s all about storage and CPU power. Finally, regular cloud computing demands replicated or non-replicated disks, along with constant connectivity and high redundancy.

We recognize that each data scientist or other specialist interested in AI cloud has unique requirements. Our goal is to cater to a broad spectrum of workloads, services, end-users, and any other specific needs, while still focusing on AI tasks, of course. We don’t believe in boundaries or saying, “We don’t need this kind of server.”

Now that we’re exploring the potential of GPUs for inference, we’re adding entirely new nodes to our lineup.

## Tailoring server solutions: training vs. inferenceTailoring server solutions: training vs. inference

Our latest rack generation presents two distinct node solutions: one custom-built for training and the other optimized for inference. One notable departure from the last gen is the internal placement of GPUs to address signal loss, speed reduction, and compatibility issues experienced when connecting GPUs externally.

#### The training-oriented nodeThe training-oriented node

Training AI models is a data-intensive process, with significant input and output. Here’s a simple breakdown: data enters the system, gets sifted through trillions of parameters, undergoes training across interconnected servers, and finally, you’re left with a refined model.

Given the massive throughput, speedy data transfer is key. Those bright green boxes you see? Those are the 400 GB/s network interface cards. With eight of them in each training node, we’re talking 3200 GB/s per server. These nodes communicate through a robust InfiniBand-powered network, ensuring seamless connectivity that is so essential for calculating large models.

On the top-right, you’ll find the H100 SXM5 board, NVIDIA’s brainchild, which we’ve discussed above. On top of this board are eight H100s themselves, connected to the motherboard. While universal pinout design has existed for a while, the connection approach here is uniquely ours.

The big advantage here is the ease with which multiple machines can snugly fit into a single rack, all wired up together.

#### The inference-oriented nodeThe inference-oriented node

After the training, comes inference. Once a model has been trained and stored in the GPU’s memory, it’s all set for smaller tasks like generating text or images based on prompts. In such scenarios, the GPU acts as a tool that swiftly applies your massive, multi-gigabyte model to a small data set: small input, small output.

The key concept here is distillation, which means streamlining the AI model while keeping it functional. A distilled model is tailored to specific tasks, requiring less computation due to the narrower task range.

Our inference-ready solution accommodates up to four standard PCIe GPUs — plenty enough to process a distilled model. This is a step up from our older servers that held just two GPUs. Thanks to PCI Express 5’s much higher bandwidth, we’ve doubled up. Notably, this node variant can operate independently, without needing to interconnect with other machines.

Inference tasks will soon be available as part of Nebius AI as we embrace the next generation of racks.

## Deploying the new version of racksDeploying the new version of racks

Let’s say we get a fresh batch of servers delivered to our data center. Within a few days, we can have dozens of them fully operational and actively serving users. This quick turnaround emphasizes our efficiency and flexibility. We can prepare our infrastructure well in advance, ensuring the newly arriving hardware is installed and deployed in a matter of days. For a client, whether they be an ML engineer or technical manager, it means fast scalability.

In the fast-paced world of GPUs, where a generation lasts two to three years, everyone is constantly awaiting the next big thing. Wasting six months just gearing up means losing out on a quarter of precious time.

While designing our hardware, we cover everything from mechanical parts to electronics. This enables us to be early adopters of any new solutions from manufacturers. Being part of early shipments and closely collaborating with vendors like NVIDIA throughout the design phase make us one of Europe’s pioneers in deploying such setups. This strategy places us in a unique position to offer Nebius AI. Our commitment to innovation, efficiency, and collaboration ensures we’re not just meeting today’s demands but also anticipating and shaping the future of GPU cloud solutions.

## Discover Nebius AI

Learn more​
Request access​

## Documentation

Go to the docs​

Nebius team

## Related links

More on Nebius AI​
Documentation​

Sign in to save this post
Sign In
