# How Simulacra AI is transforming quantum chemistry

Source: https://nebius.com/customer-stories/simulacra-ai

Skip to main content

## Long story shortLong story short

Simulacra AI is combining ab initio quantum chemistry with deep learning to build a scalable large wavefunction model (LWM) to generate high-accuracy datasets for drug and material discovery pipelines. Utilizing Nebius’ distributed compute infrastructure, they have pushed beyond what is currently possible to combine the accuracy of quantum mechanics with the speed and efficiency of AI-driven predictions.

Simulacra AI is a research-driven startup building the next generation of AI4Science models that simulate molecular interactions at the quantum level to supercharge drug discovery.

## ContentsContents

Ab initio foundation wave-function model

Scaling challenges and compute infrastructure

Custom AI training framework

Selling high-fidelity molecular property data

Redefining computational chemistry with AI

Simulacra AI is transforming the field of quantum chemistry with machine learning models that predict electron behaviour in molecules. This is critical for understanding chemical reactions, material properties, and drug design.

By combining ab initio quantum chemistry with deep learning, Simulacra AI is building a scalable wave-function foundation model for molecular systems that can generate high-accuracy datasets for drug and material discovery pipelines.

Current protocols employed in the industry involve:

- 

Quantum chemistry calculations, which are expensive and poorly scalable with system size.

- 

Traditional methods such as Density Functional Theory (DFT), which is arguably fast but not accurate, or post-Hartree-Fock (HF) methods such as Coupled Cluster (CC) theory, which are accurate but with an enormous computational cost as system size grows.

- 

Neural networks such as machine learning interatomic potentials (MLIP), approximate quantum solutions but require enormous amounts of high-quality labeled training data.

To solve these problems, Simulacra AI has developed a bottom-up deep learning approach for molecular simulations which leverages the state-of-the-art distributed compute infrastructure from Nebius to push beyond what is currently possible.

## Ab initio foundation wave-function model

Currently, Simulacra AI is focused on pre-training an ab initio foundation wave-function model, which they call large wavefunction models (LWM). Taking from the scalability lessons learnt in the well-developed LLMs research field, LWMs are ML models that incorporate first-principles quantum mechanics to predict electron behaviour on a large scale, without the need for any labelled data. This approach provides the best of both worlds: the accuracy of quantum mechanics with the speed and efficiency of AI-driven predictions.

Instead of running full quantum chemistry calculations for every new molecule, Simulacra AI’s pre-trained models generalize across molecular structures, reducing computational costs while maintaining high fidelity.

Unlike traditional ab initio methods, where calculations scale poorly with system size, neural networks trained with the goal of optimizing the underlying wave function can bypass these limitations. This breakthrough allows users to achieve “gold standard” quantum mechanical accuracy for large, complex molecules without the exponential computational cost of traditional post-HF methods such as CC.

The eventual goal is to build billion parameters LWMs and infrastructure for computing highly accurate quantum chemistry properties, including time dynamics into the underlying modelled equations.

## Scaling challenges and compute infrastructure

Simulacra AI needed to scale its model beyond the 10M parameter limit, which required a distributed training framework capable of handling large datasets and model architectures. Traditional deep learning approaches, such as data parallelism, are not sufficient for LWMs. Instead, model partitioning (sharding) is required.

The key challenges included:

- 

Handling large-scale training on JAX: Frequent updates break existing implementations, requiring constant maintenance.

- 

Implementing single program multiple data (SPMD) partitioning: This ensures that model weights, data, and molecular geometries are distributed across processing units.

- 

Computationally expensive differential operators: These are required for variational energy calculations in quantum chemistry.

- 

Managing PySCF orbital computations: PySCF needs recompilation for every new molecular geometry, slowing down training.

- 

Reducing compilation times: JIT compilation could take 2+ hours, making rapid iteration difficult.

## Let us build pipelines of the same complexity for you
Our dedicated solution architects will examine all your specific requirements and build a solution tailored specifically for you.
Talk to an expert

## Custom AI training framework

To address these challenges, Simulacra AI built its own distributed AI framework with support for:

- 

SPMD model partitioning: Simulacra AI splits both data and model weights across multiple GPUs. This allows them to scale beyond 100M parameters, where increasing GPU count results in larger models, not just faster training.

- 

Custom equivariant neural networks: Built on Equinox with Clifford group representations, ensuring that models respect SE (3) symmetry which is important in the context of molecular properties computation.

- 

Optimization with natural conjugate gradient descent: Given the complexity of variational energy calculations, standard optimizers are not effective. Simulacra AI developed a natural conjugate gradient optimizer, fully integrated with SPMD partitioning.

- 

Ahead-of-time (AOT) compilation and caching: Instead of recompiling models dynamically, Simulacra AI caches precomputed steps, reducing compilation time from 2+ hours to just minutes.

- 

Precomputed orbitals datasets: Instead of recalculating reference electron orbitals every time, results are stored and retrieved when necessary, improving efficiency.

This compute-first approach allows Simulacra AI to train models (20M parameters) significantly larger than publicly available SOTA benchmarks while maintaining efficiency.

## Selling high-fidelity molecular property data

Rather than commercializing the AI model itself, Simulacra AI will focus on selling the high-fidelity molecular properties data it generates. These datasets can serve various purposes such as input for the parametrisation of both classical and machine-learning molecular dynamics force fields, DFT machine learning functionals and direct quantum mechanical property prediction, to name a few.

This enables researchers and industries — including pharmaceuticals, materials science, and chemical engineering — to:

- 

Accelerate discovery by leveraging high-quality quantum chemistry data.

- 

Optimize proprietary molecular models with greater accuracy.

- 

Reduce reliance on costly, compute-heavy quantum simulations by using AI-driven precomputed datasets.

This strategy aligns with the needs of industries that require precise quantum chemistry calculations but may not have the infrastructure to train large-scale models from scratch.

## Redefining computational chemistry with AI

By leveraging distributed computing and AI-first molecular simulation, Simulacra AI is transforming how research in materials science, pharmaceuticals, and chemical engineering is conducted. Their data-driven approach enables:

- 

More accurate property computation and molecular-dynamics simulations, accelerating and improving the quality of material design and drug discovery.

- 

Faster training cycles, thanks to optimized model compilation and caching.

- 

Scalability beyond traditional quantum mechanical methods, unlocking solutions previously computationally infeasible.

Their compute-first approach, leveraging distributed GPUs, model parallelism, and ahead-of-time optimization, represents a significant shift in computational chemistry and AI-driven material and molecular chemistry.

## More exciting stories

## 

Recraft

Recraft, recently funded in a round led by Khosla Ventures and former GitHub CEO Nat Friedman, is the first generative AI model built for designers. Featuring 20 billion parameters, the model was trained from scratch on Nebius.
Read the story

## 

Dubformer

Dubformer is a secure AI dubbing and end-to-end localization solution that guarantees broadcast quality in over 70 languages. The company manages two of its most resource-intensive tasks on Nebius: ML itself and the deployment of models.
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
