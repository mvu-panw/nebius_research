# Compugen: Predicting immune features for cancer therapies

Source: https://nebius.com/customer-stories/compugen

Skip to main content

## Long story shortLong story short

Compugen is looking for immuno-oncology drug targets using massive single‑cell and tumor multi-omics datasets. Their team used Nebius AI Cloud to train a unique model for spatial immune features prediction, enabling deeper analysis across vast proprietary libraries. This will help uncover previously invisible immune patterns and aid promising solutions to move from code to clinic more efficiently.

## CompugenCompugen

Compugen lives by the motto “from code to cure” and is headquartered in Israel. The biotech company uses a proprietary AI engine to discover new immuno-oncology drug targets that can help patients who don’t respond to existing therapies. Compugen’s researchers turn complex biology into data problems they can solve with advanced ML, and scan vast tumor datasets for hidden patterns that reveal new immune resistance pathways.

## ContentsContents

Body’s own cancer defenses

Unigen™ platform

Spatial data

TLS prediction model

## Body’s own cancer defenses

From the 19th‑century Coley’s toxins to novel checkpoint inhibitors, medicine has repeatedly explored ways to mobilize patients’ own defenses against cancer. Unlike chemotherapy, which broadly attacks rapidly dividing cells, immunotherapies activate the immune system by using antibodies, T-cells and vaccines that destroy tumors and keep cancer under control even after treatment stops.

While the advances of immuno‑oncology are promising, it has so far only scratched the surface, delivering long‑lasting benefit to a subset of patients and much work remains to broaden its impact across numerous cancer types. Expanding that reach by discovering new immune resistance pathways is the mission of Israeli biotech pioneer Compugen, whose entire strategy is built on a drug target discovery engine called Unigen™.

Unigen™ is an AI-powered platform that integrates multi‑omics, single‑cell and spatial data in a cloud‑based environment, turning complex tumor biology into structured problems that models can learn from. The engine operates as a flexible “code‑to‑cure” loop platform, where insights from preclinical and clinical studies continuously enrich a proprietary knowledge base to refine predictions.

The collaboration with Compugen began at Nebius Academy, where students helped prototype a novel AI workflow. Then, Nebius’ MLOps-optimized stack and NVIDIA GPUs were used to train Compugen’s model that predicts spatial features linked to a better immunotherapy response. The new model, built with Nebius’ academic and tech support, will become part of Unigen™ and help advance cancer research through deeper analysis of tumor–immune interactions.

## Unigen™ platform

Tumors are influenced by thousands of genes, secreted signals and cell-to-cell interactions; the data describing these factors is enormous and growing exponentially. By applying AI and ML to this big data problem, Compugen aims to discover patterns and drug targets that no single experiment or human intuition would easily find.

Unigen™ first builds a harmonized multi‑omics picture of tumors and their immune microenvironments, using AI tools to clean, align and quality‑control very heterogeneous datasets. Machine‑learning models then search this space for statistical patterns that suggest new immune checkpoints, drug–target pairs and pathways associated with response or resistance. Compugen combines classical ML with more recent approaches such as graph‑based models for cell–cell interaction and LLM-style tools to query its knowledge base for promising targets.

Model sizes range from 50 million to 3 billion parameters, often trained or fine-tuned on noisy, high-dimensional biological data. This is computationally intensive work, made more challenging by long protein sequences, large single-cell matrices and the need to iterate quickly on different architectures and hyperparameters. In silico hits are then vetted by human experts who design experiments to validate them, closing the loop between computation and biology.

Compugen’s two lead drugs in clinical trials, the checkpoint inhibitors COM701 and COM902, target immune “brakes” called PVRIG and TIGIT that sit on T-cells inside tumors. When cancer cells activate these receptors, T-cells stop fighting and the tumor grows unchecked. By blocking PVRIG and TIGIT, the drugs aim to reactivate exhausted T-cells so they can kill cancer again.

A sequence of Compugen’s COM902 was licensed to AstraZeneca to form part of their investigational drug called rilvegostomig, currently being tested in multiple Phase 3 studies. Another of Compugen’s investigational drugs, called GS-0321 (COM503), was licensed to Gilead. The key innovation is that Unigen™ discovered these drug targets computationally by analyzing thousands of tumor samples, rather than through traditional trial‑and‑error.

The technical bottlenecks for Unigen™ pipelines are evident: GPU memory limits, training time and data throughput. Large protein language models can quickly exhaust VRAM once they go past 500 million parameters. Some open‑source single‑cell RNA models can also demand the most powerful GPUs, with one epoch on a 100K-cell dataset ranging from 20 seconds to 20 minutes.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Spatial data

Nebius provides scalable infrastructure built around powerful GPUs, making it a strong fit for workloads that push memory and training limits like the next generation of protein and single‑cell models.

Starting as an educational partnership at Nebius Academy, the collaboration with Compugen quickly expanded into full‑scale training on Nebius AI Cloud, turning a classroom prototype into a production-grade research model that focuses on tertiary lymphoid structures (TLS) — an important indicator of the patient’s immune potential.

TLS are clusters of immune cells that form in inflamed tissues, including some tumors. They are node-like structures whose presence in tumors has been correlated with better patient prognosis, because they indicate that the immune system has essentially set up a base camp near the tumor to mount an attack.

They show up in many solid cancers, including melanoma, lung, breast, liver and other tumors. In immunotherapy, patients whose tumors have TLS often respond better to treatments like checkpoint inhibitors. For example, in a recent bile duct cancer study, TLS‑positive patients had a 71% response rate to immunotherapy versus 0% for TLS-negative patients.

Traditionally, detecting TLS requires spatial information. Pathologists look at tumor slides and, through staining, identify these organized clusters of cells. Another method is scanning spatial transcriptomics data for TLS markers. However, the vast majority of tumor gene expression datasets don’t have spatial context.

Being able to infer TLS presence from non-spatial data is crucial to unlock this signal in non-annotated datasets. For patients, this opens the door to more accurate prediction of immunotherapy response, especially in cancer types where spatial pathology is rare or unavailable.

## TLS prediction model

Compugen built its TLS prediction model on top of modern single-cell foundation models, beginning with scGPT — a transformer trained to understand cellular language by predicting masked genes from the rest of a cell’s expression profile. That contextual understanding was strengthened by scGPT-Spatial and Nicheformer models, which added neighborhood-level awareness by learning not just what’s happening inside a cell, but also how the surroundings influence it.

To train the model, Compugen curated a dataset with spatial slides containing hundreds of thousands of cells with expression profiles for hundreds of genes. Experts manually annotated TLS regions. One challenge was TLS boundary cells, which often have mixed identity and are difficult to classify even for humans, making the dataset a strong test of model robustness.

The first model tier explicitly incorporated spatial coordinates. A graph neural network mapped how cells cluster in physical space, while scGPT embeddings captured each cell’s transcriptional identity. Merging these two signals produced a classifier that mirrors a pathologist’s perspective — recognizing TLS from both molecular patterns and cell-to-cell organization.

As many real-world datasets lack spatial information, Compugen also developed an end-to-end finetuned transformer variant that learned TLS signatures directly from expression data alone, without relying on coordinates. A final baseline with frozen scGPT weights confirmed how much value fine-tuning adds. Across all tiers, the conclusion was clear: spatial models are the gold standard, but the transcriptional signal alone is strong enough to generalize TLS detection to large non-spatial datasets.

Nebius provided its powerful GPUs to train the model with minimal overhead. “We like the straightforward interface and the competitive prices. The team seems to be very professional and motivated to help us. Plus, the company is primed to insert the most novel chips once they enter the market, ” Compugen’s Head of Computational Discovery Dr. Roy Granit said.

Compugen’s next step would be to integrate the models into the Unigen pipelines, so they can run the inference on all datasets. “There is currently no publicly available model that can make TLS predictions at the single-cell level, which gives us capabilities others lack” Granit said. “Nebius gave us powerful GPUs, a smooth interface and competitive pricing to train large-scale models on sensitive biological data. It’s a great match for AI in biotech”.

The company now aims to train additional models to predict other important spatial features that could reshape cancer immunotherapy and help save more patients’ lives.

## More exciting stories

## 

vLLM

Using Nebius’ infrastructure, vLLM — a leading open-source LLM inference framework — is testing and optimizing their inference capabilities in different conditions, enabling high-performance, low-cost model serving in production environments.
Read the story

## 

SGLang

SGLang, a pioneering LLM inference framework, teamed up with Nebius AI Cloud to supercharge DeepSeek R1’s performance for real-world use. The SGLang team achieved a 2× boost in throughput and markedly lower latency on one node.
Read the story

## 

London Institute for Mathematical Sciences

How well can LLMs abstract problem-solving rules and how to test such ability? Research by the London Institute for Mathematical Sciences, conducted using our infrastructure, helps to understand the causes of LLM imperfections.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
