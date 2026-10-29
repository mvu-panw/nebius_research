# Converge Bio: Advancing single-cell research

Source: https://nebius.com/customer-stories/converge-bio

Skip to main content

## Long story shortLong story short

Converge Bio is redefining precision medicine by combining single-cell RNA sequencing with large language models to unlock patient-level therapeutic insights. With Nebius’ AI-native infrastructure, they’ve trained a full-transcriptome foundation model (Converge-SC) capable of processing 20,000+ genes per cell — delivering state-of-the-art accuracy, explainability and speed for drug discovery and clinical development.

Converge Bio is at the forefront of integrating Generative AI with biological data. The company’s mission is to empower biotech and pharmaceutical companies to discover and develop more effective drugs faster, utilizing the power of LLMs specifically trained on biological languages.

## ContentsContents

Converge-SC

Training and deployment

Built-in explainability

Results

Why Nebius

Impact

Single-cell RNA sequencing (scRNA-seq) is ushering in a new era of biomedical research by enabling scientists to study gene expression at the resolution of individual cells. It has the potential to reshape drug discovery, disease modeling and precision medicine — particularly in fields like oncology and immunology.

Yet despite this promise, most foundational AI models struggle with the complexity and volume of scRNA-seq data. They typically operate at the cellular level only, limiting their ability to capture patient-specific insights. Many tokenize gene expression values, losing the numerical fidelity essential for accurate biological interpretation. In addition, current models can only handle 200–1,200 genes at a time, a fraction of the full transcriptome, and require cumbersome workarounds to scale to patient-level use cases.

## Converge-SC

Converge Bio, a biotech company based in Tel Aviv, has developed Converge-SC, a LLM specifically designed to interpret single-cell data with high resolution and biological explainability.

Unlike traditional models, Converge-SC processes the entire transcriptome — more than 20,000 genes per cell — thanks to a 30K context length. It retains raw numerical gene expression values, allowing for more accurate and granular analysis without reducing input data to tokens. Crucially, it was engineered from the ground up to operate at the patient level, enabling robust responder/non-responder analysis and more precise insights into therapeutic response.

The model was trained on over 36 million cells, primarily sourced from open datasets like cellxgene, totaling more than 2TB and trillions of tokens. A rigorous preprocessing pipeline addressed batch effects, sequencing variability and data quality — using both raw and curated data to maximize generalization.

Converge-SC leverages an encoder-only Transformer architecture with rotary positional embeddings, adapted to support continuous gene expression values. It preserves the numerical meaning of expression magnitudes while still capturing gene semantics through tokenized inputs.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Training and deployment

It took over 7,000 hours of compute to train Converge-SC. Optimization strategies included distributed data parallel (DDP), fully sharded data parallel (FSDP), tensor parallelism and quantization to ensure efficient scaling across multiple GPUs. The model is freely available on Hugging Face for academic use, and Converge Bio offers tailored deployment pathways for enterprise and clinical settings. Ease-of-use was a core focus, and the model integrates smoothly into existing biotech and pharma R&D pipelines.

## Built-in explainability

A key differentiator of Converge-SC is its native explainability. The team conducted extensive ablation studies and trained the model on masked gene and expression prediction tasks to reinforce biological interpretability. The model provides gene-level attribution within specific cell types, enabling researchers to understand the “why” behind predictions and interpret biological drivers of disease progression or drug resistance.

By analyzing both gene identity and expression level in tandem, Converge-SC acts as both a predictive engine and a tool for discovery.

## Results

Converge-SC outperformed SC-GPT and other baseline models across several key benchmarks, including:

- 

Patient disease classification

- 

Solid tumor binary classification

- 

Cell type classification

- 

Perturbation prediction

Its state-of-the-art performance has made it easier for researchers to extract meaningful insights from complex biological datasets. The model is being released on Hugging Face, allowing for seamless integration into biotech and pharma R&D workflows.

## Why Nebius

To develop a model of this scale, Converge Bio required an AI infrastructure provider that could handle massive computational demands reliably and efficiently. The team specifically benefited from:

- 

A user-friendly platform that reduced operational overhead

- 

End-to-end infrastructure support throughout model training

- 

Rapid responsiveness to technical challenges and scaling needs

- 

An AI-native environment built specifically for life sciences research

With Nebius, the team was free to focus entirely on scientific innovation — without being distracted by infrastructure complexity. The level of expertise and support was instrumental in pushing the boundaries of what’s possible in computational biology.

## Impact

Converge Bio’s work with Nebius has resulted in one of the most advanced single-cell models available today. By enabling whole-transcriptome analysis and patient-level reasoning, Converge-SC is advancing drug discovery, personalizing therapeutic strategies and transforming how researchers interact with biological data. Together, Converge Bio and Nebius are setting a new standard for how AI infrastructure can empower breakthroughs in precision medicine.

## More exciting stories

## 

Simulacra AI

Simulacra AI is combining ab initio quantum chemistry with deep learning to build a scalable large wavefunction model (LWM) to generate high-accuracy datasets for drug and material discovery pipelines.
Read the story

## 

SynthLabs

Synthlabs significantly simplified their training infrastructure setup using TractoAI serverless platform. Synthlabs research engineers leveraged TractoAI distributed offline inference capability to accelerate the release of the first open source reasoning dataset.
Read the story

## 

Unum

In our field, effective partnerships that harness complementary strengths can drive significant breakthroughs. Such is the case with the collaboration between Nebius and Unum, an AI research lab known for developing compact and efficient AI models.
Read the story

## Start your journey today
Make it my experience

## Explore the platform

Get started​
Pricing​
Docs​
