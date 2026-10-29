# Decoding nature: Rebuilding coral reefs with Wildflow

Source: https://nebius.com/customer-stories/wildflow

Skip to main content

## Long story shortLong story short

Wildflow builds foundation models for biodiversity to enable repeatable, in-depth ecosystem monitoring at scale. Starting with coral reefs, Wildflow’s AI-ready 3D reconstruction pipeline relies on Nebius AI Cloud’s Serverless capabilities to skip infrastructure hurdles and turn TBs of raw footage, acoustics and environmental data into high-fidelity, web-based digital twins that track ecosystem change to accelerate restoration initiatives.

Wildflow combines ML research and ecology expertise to scale environmental protection with AI. Building on the exponential growth of sensor and robotics data, Wildflow aims to extend this ecosystem modeling framework to all major Earth biomes within 8 years — deepening our understanding of complex ecosystem dynamics to demonstrate human impact and help rebuild endangered biomes.

## ContentsContents

Optimizing 3D reconstruction with flexible compute

Ultra-detailed graphics at speed

Fast storage for high fidelity

Adaptive chunking to push GPU efficiency

Submarine street view to support AI analysis

Modeling nature: Analyzing multimodal data to encode biodiversity

Conservation at scale: A roadmap for global ecosystem modeling

Coral reefs are among the most vibrant ecosystems on Earth — and the most vulnerable to human activity. As 90% of coral reefs face severe degradation by 2050 according to the Intergovernmental Panel on Climate Change (IPCC), Wildflow provides restoration teams with scalable digital tools to accelerate their impact. Propelled by the rapid growth in oceanic data availability, Wildflow is building AI models to encode biodiversity and lay the groundwork for coordinated action at scale.

Powered by Nebius, Wildflow’s 3D reconstruction pipeline digitally recreates coral reefs from terabytes of underwater footage and environmental data in partnership with over 20 research institutes globally. Beyond virtual diving expeditions that allow researchers to track key reef health metrics, the digital twins will enable Wildflow to model complex reef dynamics and detect complex ecological patterns, helping scientists flag degradation signals faster and more consistently across vast areas.

The spatially aware, high-fidelity digital twins are available for real-time online exploration in a “Google Maps for coral reefs” format, as described by founder Sergei Nozdrenkov — who also led AI-enabled biodiversity initiatives at X, Google’s Moonshot Factory.

With a flexible setup in Nebius AI Cloud, Wildflow can quickly deploy high-performing compute to match evolving development cycles and maximize throughput from every GPU hour. Our elastic infrastructure also keeps their multi-stage 3D reconstruction pipeline running steadily at full resolution without compromising cost efficiency.

“With Nebius, we can easily spin up HPC virtual machines on demand. With fast, persistent storage, large datasets move across the pipeline without overhead. Overall, it’s the best cloud we’ve worked with, ” said Sergei Nozdrenkov, founder of Wildflow.

By developing foundation models able to interpret sensor, acoustics, DNA and biogeochemistry data at scale, Wildflow aims to amplify our potential to protect and rebuild biodiversity. The digital twins set the foundation for Wildflow to model ecosystem processes such as predator-prey dynamics, population growth and coral spawning patterns to inform targeted restoration interventions, secure funding opportunities and encourage large-scale adoption of proven conservation methods.

## Optimizing 3D reconstruction with flexible compute

Wildflow’s 3D reconstruction pipeline is designed to reliably process terabytes of data without sacrificing visual fidelity or spatial accuracy. While chunking and tiling steps for 3D training are GPU-intensive, other stages depend on CPU processing, like camera positioning estimations.

Purpose-built to power varying workloads, Nebius Serverless AI lets Wildflow run each job with its own container image without worrying about cluster setup or overprovisioning costs. With Serverless Jobs, Wildflow matches GPU capacity to their AI lifecycle, seamlessly scaling from a handful of jobs to over 20 running in parallel, with agents helping automate the workflow. “We would have saved a lot of time and resources had we used Nebius from day one”, Nozdrenkov said.

Backed by Nebius' high-performance infrastructure, Wildflow optimized every stage of the reconstruction pipeline to accelerate 3D generation and prepare for AI model development.

## Ultra-detailed graphics at speed

Delivering photorealistic visuals for web-based exploration from any angle, on any device requires real-time rendering. With a custom 3D Gaussian Splatting (3DGS) architecture, Wildflow recreates complex environments at much lower computational costs than alternative computer vision methods.

By distributing millions of small, programmable ellipses as dense point clouds in a virtual space, this cutting-edge technique encodes color, defines opacity and reconstructs surfaces much faster for a browser-friendly experience.

With a 3DGS pipeline, Wildflow relies on Nebius AI Cloud to piece together terabytes of environmental data and raw footage from GoPro cameras, mobile phones and even robots — like autonomous or remotely operated vehicles — into topographically aware, precisely georeferenced digital twins.

## Fast storage for high fidelity

To replicate underwater scenes all the way to the polyp, Wildflow must move TB-scale datasets swiftly through preprocessing, alignment, reconstruction and rendering stages. Any lags can result in IO bottlenecks, inconsistent rendering and quality loss.

Designed to scale AI workloads, Nebius’ shared filesystems let Wildflow retain full-resolution imagery across the pipeline, delivering the fine ecological details needed for reliable environmental monitoring. High-speed storage also prevents costly delays and lets the startup fully leverage high-throughput infrastructure.

## Adaptive chunking to push GPU efficiency

Reef landscapes must be split into smaller scenes to fit GPU memory, but what’s the optimal number of chunks to maximize returns on infrastructure? With too many patches, a lot of compute is spent processing little data, but oversizing tiles risks compromising visual quality.

Wildflow solved it with an algorithm that dynamically partitions each site at the lowest number of patches that yields the best possible information density — ensuring efficient rendering and training tasks on Nebius AI Cloud.

## Submarine street view to support AI analysis

Wildflow is on track to digitally recreate models from dozens of coral reef sites in partnership with over 20 research institutions around the world. In five years, hundreds of survey plots have been collected by academic partners including University College London (UCL), Derby University, the Lancaster University’s LEC Reefs research group, IPB University in Indonesia and the Australian Institute of Marine Science (AIMS).

Around 625 square meters in size, each survey plot is roughly half the size of an Olympic swimming pool and can be fully documented with 8,000 pictures from two GoPro cameras. To design the model, Wildflow estimates the reef’s 3D layout from 2D images captured from various angles with Structure from Motion (SfM) techniques — recreating the basis of underwater scenes in under a day with Nebius’ high-throughput infrastructure. To render the details while preserving spatial accuracy, scale and color fidelity with sub-centimeter resolution, the 3D Gaussian Splatting step takes just a few hours running on Nebius AI Cloud.

“Nebius lets us quickly process large 3D reef datasets without needing a full cluster setup, which makes high-quality monitoring accessible even with limited resources — helping scientists and restoration teams scale their work faster and more affordably”, Nozdrenkov emphasized.

In an experience akin to Google Street View, you can explore a restoration site in Indonesia’s Spermonde Archipelago by navigating Wildflow’s web-based prototype, including close-up views for the highest level of detail. This other demo lets scientists and enthusiasts dive into a nook of Australia’s colorful reefs — you can even count the polyp branchlets and lobes by zooming in.

Building on established field surveys, the digital twins unlock multimodal AI analysis to enhance long-term restoration planning and reef health monitoring. Wildflow’s 3D pipeline turns diver-collected footage into spatially consistent, full-resolution records at a fraction of the traditional processing time.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Modeling nature: Analyzing multimodal data to encode biodiversity

Combining deep expertise in ecology, machine learning and remote sensing, Wildflow’s 1-year vision is to train the first multimodal foundation models on diverse reef ecosystems globally. Their 3D reconstruction pipeline generates structured outputs, including camera poses, segmentation overlays and splats, all ready for foundation model training.

To unlock a more comprehensive understanding of the ecosystem, the training pipeline will be complemented with genomics, acoustics, satellite imagery and even hyperspectral imaging, alongside environmentally relevant indicators like temperature, salinity and oxygen levels.

The foundation model in development will help predict how localized interventions can strengthen reef communities by combining innovative AI capabilities:

- 

Delivering insights from sensor data: By automating species identification, area coverage assessments and disease detection with AI, restoration projects can define more precise risk mitigation strategies.

- 

Modeling ecosystem dynamics: An in-depth understanding of how the colorful polyps, booming biodiversity and dynamic lifecycles make up a thriving reef community is essential to accelerate conservation initiatives. Wildflow aims to model natural processes like population growth and predator-prey interactions for scientists to plan more effective, targeted environmental interventions.

- 

Measuring what nature gives us: Valuating specific ecosystem services is essential to help restoration teams demonstrate the economic returns only made possible by healthy reefs — a delicate ecosystem which harbors 25% of marine life and supports the livelihoods of hundreds of millions of people, according to the Global Coral Reef Monitoring Network’s latest estimates.

- 

Tracking what we give back to nature: A foundation model will make it easier to quantify our impact on coral reefs — both positive and negative. Wildflow plans to model the effects of conservation initiatives like marine protected areas or restoration projects, as well as the consequences of pollution, agricultural runoff and uncontrolled coastal development.

## Conservation at scale: A roadmap for global ecosystem modeling

Starting from coral reefs, Wildflow’s vision is to recreate other oceanic habitats within four years and model all Earth’s biomes with AI. Their solution is biome-agnostic by design, as its multimodal data capture, Structure-from-Motion reconstruction, and 3D Gaussian Splatting rendering pipeline can be applied to other endangered biomes. Wildflow’s eight-year goal is to develop a “digital nervous system for our planet”, able to deliver informed insights at scale to help design more efficient conservation initiatives and spread successful restoration methods across all ecosystems.

Beyond Wildflow’s own plans, the company actively contributes to AI model development worldwide. They shared over 350 GB of georeferenced GoPro footage and color-corrected imaging under an open-source license on Hugging Face to encourage people to build their own AI applications for coral reefs.

In the coming decades, Wildflow sees little limit to what humanity can achieve with compounding advances in AI-enhanced ecosystem modeling. The ability to accurately predict how targeted interventions will holistically affect complex biodiversity dynamics could unlock restoration goals beyond what we thought was possible. “Our goal is to be the first generation to leave nature better than we found it. By establishing a symbiotic relationship with our biosphere today, maybe one day we’ll even use that deep understanding to create a jungle out of a desert or terraform Mars, ” concludes Wildflow’s 16-year AI roadmap.

## More exciting stories

## 

Prima Mente

Prima Mente is building foundation models to uncover what’s happening in the brain without directly accessing it. With a 32-GPU reserved cluster in Nebius, Prima Mente amped up pre-training throughput by 12%, processing 1.19 million tokens/s on 16 nodes, a critical step in their goal toward scaling model size from 7B up beyond 100B parameters.
Read the story

## 

Stanford

CRISPR-GPT is an LLM-powered agent system developed by scientists from Stanford, Princeton and Google DeepMind, which automates gene-editing experiments, from CRISPR system selection to decision making when designing gene-editing RNA to data analysis.
Read the story

## 

TrialHub

TrialHub leverages RAG-optimized LLMs, semantic search and other advanced language modeling techniques to extract quantifiable insights from over 80,000 trusted medical sources. With Nebius’ expert support, TrialHub launched its 250-million vector database in days.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
