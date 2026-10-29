# Nebius-UCSF Collab Helps Adapt Key Protein Modeling Tool for Modern GPU Clouds

Source: https://nebius.com/blog/posts/ucsf-collab-protein-modeling-tool

Skip to main content

Bioscience seeks to unravel the structure of protein complexes that drive nearly every cellular process. Open-source tools and data banks are essential for accelerating advances in this field. With support from Nebius AI Cloud and a Nebius Academy fellowship, researchers at the University of California, San Francisco are adapting widely used protein modeling software to modern GPU cloud platforms, expanding access and impact for the scientific community.

# Fellowship for frontier computational biologyFellowship for frontier computational biology

Nebius AI Cloud and Nebius Academy, the company’s education and research hub, award fellowships to researchers, boosting their work in AI and related fields — often through joint projects with leading academic institutions, like the University of California, San Francisco.

One of UCSF’s most significant achievements is advancing global collaboration in protein modeling. UCSF’s Dr. Benjamin Webb, a Nebius fellow, is a key developer behind the Integrative Modeling Platform (IMP), an open-source tool for the analysis of large protein complexes.

IMP is used by scores of scientists worldwide. It allows blending diverse experimental data to build high-quality models of molecules of life: proteins, nucleic acids like DNA or RNA and their complexes. The resulting models drive discoveries in medicine, biology and drug design, leading to a deeper understanding of how molecular machines actually work.

The grant from Nebius and its expert technical guidance support a critical transition for UCSF’s software, adapting it to modern GPUs and cloud infrastructure and accelerating research in medicine and biotechnology. It also helps UCSF researchers develop the world’s leading 3D biomolecular structure archive, the Protein Data Bank.

# IMP: blending data from diverse toolsIMP: blending data from diverse tools

For the general public, UCSF is a leading hospital, renowned for pioneering research into temperature receptors (2021 Nobel Prize), the identification of oncogenes that opened the door to targeted cancer therapies, and the discovery of prions, which reshaped our understanding of conditions like Alzheimer’s disease (1997 Nobel Prize).

For computational biologists, UCSF is also the home of IMP — the software that has become essential for deciphering structures too large or intricate for any single laboratory method. The platform enables scientists to combine data from multiple experimental sources like cryo-electron microscopy or mass spectrometry — to generate and refine models.

“The protein complexes we’re looking at in the lab are enormously large from a structural biology perspective. You just don’t know what these things look like from one method alone, ” Benjamin Webb says. One example is the nuclear pore complex, a huge gateway that controls the movement of molecules between the cell’s nucleus and its cytoplasm.

Where traditional approaches revealed only isolated pieces, integrative modeling makes it possible to reconstruct the full nuclear pore complex and map how its components fit and function together.

# From CPU to GPUFrom CPU to GPU

From the start, the team made IMP open source, reflecting the need for transparency in methods and data handling. The software was written in C++ with a lightweight Python interface and designed to run integrative modeling simulations on CPUs, typically across many cores in parallel.

For large assemblies like the nuclear pore complex, this required substantial computational power, with jobs running on as many as a thousand CPU cores in independent but coordinated sampling protocols such as replica exchange. “More and more, we were starting to look at how we can use GPUs to accelerate that, ” Webb said.

The lab is now actively working to port core IMP algorithms — especially the scoring functions — into Python libraries optimized for modern platforms (like JAX), aiming to allow rapid scaling from CPUs to GPUs and cloud clusters.

Collaboration with enterprise engineers through the Nebius grant is helping the team optimize its software for multi-platform compatibility and build more robust and cloud-ready modules. “We have chemists, we have biologists, but we are not professional software engineers. It’s really useful for us to partner with a company that has more understanding of how the code works on different platforms, ” Webb noted.

Nebius will provide its clusters for a full-scale IMP test once the software upgrade is complete. Moving towards GPU-enabled and cloud-adapted IMP will make it accessible to more scientists and allow modeling of even larger complexes without the limits of academic compute clusters.

# Updating the largest protein bankUpdating the largest protein bank

Ultimately, the lab sees IMP’s upgrade as fundamental to tackling the biggest questions in structural biology — and hopes these advances will ripple across the biotech research community.

This closely aligns with recent advances in next-gen data resources. Two recent articles in Nucleic Acids Research and the Journal of Molecular Biology, co-authored by Nebius fellow Dr. Webb, highlight an important update of a leading biomolecular structure databank — an effort that helps millions of scientists and students in their studies of complex biomolecules.

The planet’s oldest and largest Protein Data Bank (PDB) holds more than 240,000 3D entries that help scientists understand how large macromolecular machines influence cellular functions. Researchers have used PDB’s 3D data to reveal the structure and function of critically important molecules — including hemoglobin, DNA polymerase, insulin and the coronavirus spike protein. PDB data also featured centrally in the development of COVID-19 vaccines and remains essential in designing new therapies for Alzheimer’s. Famous AI systems like AlphaFold, which predict protein structures from sequence data, were only made possible by decades of open PDB data.

The articles detail the recent addition and validation of new integrative structure models, like the ones generated with IMP, into the main PDB archive. Now, all biomolecular structure models, including those built from multiple methods, are fully searchable, visualizable and validated.

Looking ahead, PDB’s unified data archive does more than support today’s research: it lays the groundwork for a new generation of AI-driven models that will transform molecular biology. By bringing together integrative structures and those solved using a single technique, researchers hope to unlock smarter, more powerful tools for understanding biomolecules in their native context and not only in the test tube.

The robust, cloud-based infrastructure for the protein modeling revolution is already in place.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Nebius team

Contents

- Fellowship for frontier computational biology

- IMP: blending data from diverse tools

- From CPU to GPU

- Updating the largest protein bank

## See also

### 

Nebius AI at the frontiers of physics and maths

In today’s guest post, Ananyo Bhattacharya, Chief Science Writer at the London Institute for Mathematical Sciences, details projects by researchers at LIMS, all based on Nebius infrastructure. We’re honored to host these under our Research Grant program.

August 1, 2024
4 mins to read

### 

Advancing confidential computing and cross-border bioinformatics at the ELIXIR BioHackathon

Open-source, global-scale infrastructure is crucial to accelerate scientific innovation. Developed in the ELIXIR BioHackathon and enabled by Nebius, the BioHackCloud project is designed as a reference implementation for a standards-based, federated multi-cloud platform — having successfully demonstrated an Attested TLS proof of concept for private LLM inference and confidential task execution.

September 2, 2025
5 mins to read

### 

Introducing self-service NVIDIA Blackwell GPUs in Nebius AI Cloud

NVIDIA HGX B200 instances are now publicly available as self-service AI clusters in Nebius AI Cloud. This means anyone can access NVIDIA Blackwell — the latest generation of NVIDIA’s accelerated computing platform — with just a few clicks and a credit card.

August 12, 2025
2 mins to read

Sign in to save this post
Sign In
