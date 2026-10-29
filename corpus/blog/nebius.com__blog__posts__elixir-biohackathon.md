# Advancing Confidential Computing and cross-border bioinformatics at the ELIXIR BioHackathon

Source: https://nebius.com/blog/posts/elixir-biohackathon

Skip to main content

Broadening the scientific use of genomic data is essential to foster life science breakthroughs worldwide. Ongoing efforts in the genomics community have explored how confidential computing and attested TLS (aTLS) can safeguard sensitive biomedical workflows with verifiable privacy guarantees and cross-cloud interoperability, but progress remains fragmented.

By bringing together leading bioinformaticians and computational biologists from academia and industry in the ELIXIR BioHackathon, the BioHackCloud project catalyzed concrete breakthroughs in that direction. Enabled by Nebius AI Cloud and an ecosystem of partners, the project emerges as a reference implementation for a standards-based, federated cloud platform grounded in the Global Alliance for Genomics and Health (GA4GH)’s open framework to broaden the responsible use of genomic data.

The BioHackCloud project achieved key milestones in 2024 enabled by high-performance, secure-by-design infrastructure provided by Nebius AI Cloud:

- 

Attested TLS (aTLS) proof of concept — extending the TLS handshake with verifiable trusted execution environment (TEE) attestation. The extension allows BioHackCloud users to independently verify the trustworthiness of a specific software running in the processing environment and confirm that execution occurs in hardware-enforced memory isolation, protecting and streamlining data access, code and model weights in life science multi-cloud federated compute and AI inference workflows.

- 

Private LLM inference — delivering confidential access to complete LLM capabilities through an OpenAI-compatible API served by an open-source inference engine and model. This easily replicable setup enables private-mode processing across different models or datasets.

- 

Confidential task execution — enabling researchers to safely deploy bioinformatics workflows in multi-cloud environments via ELIXIR TESK, a Kubernetes-native implementation of the GA4GH Task Execution Service (TES) API, with independent verification of runtime integrity across TEEs ensuring robust regulatory alignment.

- 

Exploratory deployments with Soperator — Nebius’ open-source Slurm-on-Kubernetes operator — streamlined GPU resource management for high-performance life science workloads. Combined with the GA4GH unified interface for accessing genomic data and analysis tools, initial deployments demonstrated potential for broader academic adoption.

Designed to ensure the highest security standards by default, Nebius operates a distributed network of high-performance data centers across European countries and the US, soon expanding to the UK. Backed by deep ML expertise and supported by 24/7 solution architects, Nebius’ vertically integrated AI infrastructure is uniquely positioned to enable the responsible handling of health-related data across borders.

# ELIXIR and GA4GH: crucial developments in 2025ELIXIR and GA4GH: crucial developments in 2025

ELIXIR integrates bioinformatics resources across Europe and connects scientists from over 240 research institutes in 21 countries to amplify life science impact on public health, the environment and the economy. By organizing the BioHackathon every year, ELIXIR helps develop an open-source service infrastructure and software ecosystem that makes biomedical data and tools easier to find, access, integrate, and reuse.

In line with ELIXIR’s strategic priorities, the BioHackCloud’s collaborative efforts to advance standards-based, interoperable infrastructure catalyzed key developments in 2025:

### Refocusing ELIXIR On Cloud using the GA4GH TES standardRefocusing ELIXIR On Cloud using the GA4GH TES standard

Jointly provisioned by six nodes across Europe, the ELIXIR On Cloud initiative — a key BioHackCloud partner — focused its efforts on the GA4GH Task Execution Service (TES) standards-based ecosystem, helping advance a federated infrastructure for privacy-preserving computations.

ELIXIR On Cloud deployments across Europe, including in Germany, are becoming an important part of the European Open Science Cloud (EOSC). Within the new EOSC United project, ELIXIR On Cloud stands next to Galaxy as a flagship example of how open standards can power secure, cross-border bioinformatics.

### The TRE Open Suite projectThe TRE Open Suite project

A new initiative under the GA4GH implementation forum (GIF), the TRE Open Suite project was recently established to bridge policy frameworks, IETF standards and technical rollout strategies for a broader implementation of the aTLS verification chain, advancing measurable trust in federated bioinformatics.

This reference implementation lays out a blueprint for a unified research system where bioinformaticians and institutions can deploy attestation capabilities and connect through domain-specific accounts. Credentials-based access enables data and compute centers to be discoverable across multiple institutions. Project outcomes are expected to be successively integrated into the BioHackCloud over the next three years, during and in between upcoming BioHackathon events.

# Looking ahead: the 2025 ELIXIR BioHackathon and beyondLooking ahead: the 2025 ELIXIR BioHackathon and beyond

Hosted in Berlin from November 3–7, the 2025 ELIXIR BioHackathon is set to amplify the BioHackCloud collaboration. The project aims to deepen its privacy and security frameworks by expanding ephemeral file encryption with short-lived, run-scoped keys. As part of the TRE Open Suite project, the BioHackCloud is set to showcase a new attested TLS (aTLS) implementation aligned with the latest IETF — internet-draft for remote attestation with exported authenticators, released as fully open source and delivered as an extensible GA4GH-SDK plugin.

To ground the work in real-world impact, the BioHackCloud team will publish reproducible, open source demonstrators, informed by industry use cases and co-developed with contributors from BostonGene and Amaros AI. By documenting patterns, limits and best practices for privacy-preserving, auditable AI, the BioHackCloud plans to embed privacy-by-design, verifiable runtime integrity and audit-ready provenance into federated workflows.

Beyond the event series, the BioHackCloud is shaping up to serve as a sandbox for technological exploration, where both academia and industry experts can trial use cases in genomics, AI and high-performance bioinformatics.

Enabled by Nebius and a network of partners, the first nodes to go live will remain continuously available after the 2025 ELIXIR BioHackathon as an open testbed to accelerate adoption, experimentation and cross-cloud interoperability — all rooted in the GA4GH open standards and robust security guidelines essential to future-proof scientific collaboration.

## Acknowledgements

 Alexander Kanitz (Pacific Analytics PTY LTD and ELIXIR Switzerland) and Pavel Nikonorov (GENXT) co-led this collaboration, with the contribution of Gordon J. Köhn and Ivan Topolsky (ETH Zürich), Javed Habib (Pacific Analytics PTY LTD), Viktória Spišaková (Masaryk University), Liisa Lado-Villar (CSC – IT Center for Science), Hirotaka Suetake (The University of Tokyo/Sator Inc.), Emre Balsever (ELIXIR Sweden/NBIS/AIDA Data Hub), Paula Iborra de Toledo (Barcelona Supercomputing Center), Vincent Emonet (SIB Swiss Institute of Bioinformatics), Nerses Shahbazyan (BostonGene), Davit Shahnazaryan and Davit Harutyunyan (Amaros AI). GENXT led the confidential computing workstream and Pacific Analytics contributed towards the adoption of Soperator within the ELIXIR ecosystem. We acknowledge contributions from Jonathan Tedds (ELIXIR Hub) and a range of contributors to the ELIXIR On Cloud ecosystem through the ELIXIR Compute Platform and GA4GH Driver Project on Cloud and AAI. 

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Pavel Nikonorov
Co-Founder, Board Member at GENXT

Contents

- 

ELIXIR and GA4GH: crucial developments in 2025

- Refocusing ELIXIR On Cloud using the GA4GH TES standard

- The TRE Open Suite project

- 

Looking ahead: the 2025 ELIXIR BioHackathon and beyond

## See also

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

### 

From genome analysis to quantum chemistry: Nebius powers the next generation of biotech research with NVIDIA

As part of NVIDIA GTC Paris at VivaTech, Nebius has announced deeper integration of the NVIDIA AI Enterprise software suite. This includes NVIDIA BioNeMo, a collection of tools, applications, generative AI solutions, and pre-trained microservices (NVIDIA NIM) designed squarely for the biopharma sector.

June 25, 2025
5 mins to read

### 

Supercharging startups: Nebius accelerates AI-native innovation with NVIDIA

Nebius AI Cloud is collaborating with NVIDIA Inception, a leading program for AI startups with over 22,000 members, to accelerate AI startup innovation. Nebius’ AI Lift program — announced at NVIDIA GTC 2025 — offers eligible NVIDIA Inception members up to $150,000 in cloud credits, access to AI technical expertise and support and a range of other exclusive benefits.

April 9, 2025
3 mins to read

Sign in to save this post
Sign In
