# Helical: Redefining drug discovery at the application layer

Source: https://nebius.com/customer-stories/helical

Skip to main content

## Long story shortLong story short

Helical builds Virtual AI Labs for researchers to distill months of wet lab tests into hours of AI-driven experiments, enabling more innovative therapeutics to reach patients faster. Trained on Nebius in just a few weeks, Helical’s flagship model — Helix-mRNA — combines Mamba-2, transformers and codon-aware tokenization to capture subtle biological signals and quickly adjust to experimental contexts across therapeutic areas, amplifying innovation in core drug development processes.

Helical helps pharma and biotech companies reach scientific breakthroughs faster by scaling virtual experimentation. By relying on Nebius’ purpose-built clusters with reliable connectivity and storage integration, Helical closes the gap between foundation models and scientific outcomes — delivering post-trainings and alignment capabilities for production-ready models at scale, designed for quick personalization to domain-specific datasets.

## ContentsContents

Designing a foundation model to accelerate mRNA-based therapies

Dual-stage training: ensuring robust performance and quick adaptability

Engineering a hybrid architecture to model complex mRNA dynamics

Towards more comprehensive models, available at scale

Beyond accelerating drug discovery pipelines, AI-driven simulations allow researchers to identify drug targets with higher therapeutic potential, optimize molecules for more efficient treatments and enable scientific breakthroughs in fewer experiments to help new therapies reach patients faster. Helical is at the forefront of this transformation, developing the application layer for pharma and biotech companies to achieve discovery milestones in hours of virtual experiments, saving months of costly wet lab cycles.

Powered by our AI Cloud, Helical builds in silico labs to enhance DNA, RNA and single-cell research, hosting open source and proprietary foundation models on a single platform to streamline large-scale simulations. With Nebius’ readily available, state-of-the-art infrastructure, Helical trains and aligns production-ready models in weeks instead of months, delivering easily customizable models that quickly adapt to experimental datasets.

In this case study, we’ll introduce Helical’s flagship model, Helix-mRNA — and cover how its codon-aware tokenization, dual-stage training strategy and hybrid architecture design allows it to outperform baseline models across all clinically relevant predictions, capturing subtle biological signals other approaches miss.

## Designing a foundation model to accelerate mRNA-based therapies

As the molecule that holds DNA’s instructions for cells to produce essential proteins, messenger RNA (mRNA) is at the core of breakthrough treatments from rapid-response vaccines to precision medicine. To help researchers develop mRNA drug structures, a foundation model must accurately predict its stability, degradation rates and protein production efficiency — a complex challenge given the delicate balance of cellular-level biological pathways.

To unlock precise and clinically relevant predictions, Helical designed its flagship model, Helix-mRNA, to process extremely long sequences efficiently while retaining structural and biological information on a granular level. With Nebius’ purpose-built HPC clusters and expert support tailored for life sciences applications, Helical confidently deploys distributed training runs to scale model development and post-trainings.

Liberated from operational bottlenecks, Helical concentrates on innovative approaches to model more accurate mRNA simulations and advance therapeutic development:

- 

Codon-aware tokenization: Nucleotides are the building blocks of mRNA, encoding genetic instructions for protein production. Inside a cell, these instructions are read by ribosomes in sequences of three nucleotides — called codons — to assemble proteins. Helical deployed a single-nucleotide tokenization approach with codon separation to ensure the strings’ structural and biological properties are preserved in computations, improving Helix-mRNA’s predictions.

- 

Non-coding regions: Beyond assembly instructions, mRNA contains Untranslated regions (UTRs) that also play a critical role in regulating protein production. Overlooked by most models, UTRs markers are integrated into Helix-mRNA’s granular tokenization, helping researchers design more efficient and stable therapeutic molecules.

- 

Long-context handling: mRNA sequence length can add up to thousands of nucleotides, with relevant biological information scattered in different parts of the sequence. To yield more accurate predictions, Helix-mRNA was designed to handle extremely long sequences of up to 16,384 tokens, accounting for long-range dependencies critical for downstream applications.

- 

From human to viral biology: Trained on diverse mRNA sequences from viruses, plants, fungi, humans and different animals, Helix-mRNA draws on evolutionary features across different phyla and distinct pathogen genomic patterns to infer insights on core biological processes — ensuring strong model performance for most applications while enabling quick use case specialization.

## Dual-stage training: ensuring robust performance and quick adaptability

What makes Helix-mRNA a key enabler of biotech innovation is its adaptability — built as a strong generalist model, it’s easily tuned to experimental datasets in just a few clicks. By tailoring predictions to targeted biological properties, Helix-mRNA delivers significant performance gains in specialized applications.

The backbone of this versatility is Helical’s dual-stage training strategy. Accelerated by Nebius' HPC clusters with low-latency interconnectivity and integrated file storage, Helical can easily and confidently deploy large-scale distributed training workflows that enable model personalization at the edge, dramatically improving performance for clinically significant use cases.

- 

Base training: First, the model was trained on diverse mRNA datasets covering a broad range of species — building a strong foundation for the model to grasp sequence architectures and genomic patterns. By easily deploying 16 GPUs in Nebius AI Cloud, the company expedited the 500-million-parameter model base pre-training in just 10 days.

- 

Post-Training: To enhance Helix-mRNA’s performance for human-specific tasks, Helical aligned the model on high-quality, human sequences. A series of similar targeted runs aligned the model on different phyla, such as relevant viruses and fungi. Completed in just 36 hours each on Nebius AI-centric Cloud, these specialization runs enable Helix’ quick adaptation to new datasets. This second-stage alignment illustrates how Helical’s platform enables an open-ended spectrum of specializations, where models can be continuously adapted to new therapeutic areas, modalities datasets.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Engineering a hybrid architecture to model complex mRNA dynamics

Helical combined state-of-the-art neural architectures — Mamba-2, MLP and attention layers — to efficiently process long mRNA sequences and capture information in granular detail. While state-space layers encode key information across different sequence positions, MLP and attention mechanisms ensure context is preserved throughout for improved predictions.

Its newest version outperformed previous ones across all benchmark predictions, especially in critical tasks for clinical applications — increasing predictive accuracy by 146% for paired mRNA-ribosome measurements and delivering a 52.5% more precise mRNA half-life correlation.

## Towards more comprehensive models, available at scale

Helical’s next steps in redefining early discovery at the application layer focus on scaling its post-training capabilities. Development plans for Helix-mRNA include a larger, next-generation version of the current 500-million-parameter model, designed to optimize molecular design and maximize therapeutic potential.

Looking ahead, Helical also aims to expand its open core platform and make a broader range of models more widely available within its Virtual AI Lab. As ambitions grow, Helical can count on Nebius as a trusted partner for seamless provisioning of cutting-edge infrastructure to expedite model development, enable new levels of personalization and ultimately scale virtual discovery across life sciences and healthcare.

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
