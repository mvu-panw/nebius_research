# The whole AI stack moves faster in the open

Source: https://nebius.com/blog/posts/the-whole-ai-stack-moves-faster-in-the-open

Skip to main content

Modern AI is built on open source: Linux runs its machines, Kubernetes orchestrates its infrastructure, PyTorch turns its research into working systems. And every large model in existence, open or closed, was pretrained on the open commons of open code, open datasets, Wikipedia. There is a certain irony in proprietary systems whose foundations are shared work.

For Nebius, open source is something more deliberate than an inheritance. This company was built on the conviction that the greatest threat in AI is a world where intelligence consolidates into a handful of models controlled by a handful of companies. As a business and as researchers, and simply as people, we want AI to stay competitive and diverse.

If only a few models become the default production choice, they don’t just shape the market. They shape the direction of research, infrastructure, and the choices available to everyone building on top of them.

The most consequential ideas in this field have always moved through open hands, and still do: on arXiv, Hugging Face, GitHub, and the public benchmarks where claims are tested. AI has always advanced through shared research.

For a long time, the models themselves were the exception, where choosing open weights meant accepting a capability gap. That is changing: Capable open-weight models now come from more labs every year, including some of the industry’s largest players — NVIDIA’s Nemotron family ships with open weights and much of its training data.

Open weights are not open source in the strict sense, but every increase in access expands what the community can inspect, reproduce, and improve.

## An open model is only one part of the stackAn open model is only one part of the stack

A model release is the visible part. Whether an open model is actually usable — fast, reliable, affordable to deploy — is decided by the layers around it. That is where the future of AI will be decided too: not in whether open weights exist, but in whether the system around them makes them competitive in production.

Most of Nebius’ engineering lives in those layers. We have no model of our own to favor; customers run open and closed models alike, and the choice stays theirs.

New open models arrive every few weeks, and we bring them onto our managed inference platform as their weights are published — often the same day — because testing the newest against your own work and switching when it wins is half the value of openness. We only win when builders do.

Making an open model the best version of itself is engineering: tuning kernels to a model’s architecture, preserving quality at lower precision, keeping latency predictable when an agent calls a model hundreds of times in a row.

I’ve spent much of my career building high-performance inference systems, including work at Clarifai that set independently verified serving performance records for open-weight models. Much of that engineering builds on the community’s own tools (the vLLM and SGLang inference engines). At Nebius, we contribute optimizations back, like Kvax, our open-source flash-attention implementation in JAX.

## Open research compoundsOpen research compounds

Serving open models well is half the work; keeping them worth serving is the other half. Our research organization exists to keep open-source AI competitive for real-world use.

The value of a published method is rarely its original result but what others do with it: The methods I published early in my career stopped being mine the moment they left the paper, rebuilt into the open frameworks everyone now trains with.

This year, our team at Nebius published LK losses, a training objective that improves speculative decoding, releasing the training data and draft-model weights alongside the paper. Months later, Moonshot’s Kimi K3 technical report described using the LK loss to fine-tune its own speculative draft model. A useful idea was able to travel — from a paper into a system its authors never touched, and out to everyone who now runs that model.

## Building in the openBuilding in the open

This has been Nebius’ design principle since the beginning. Our engineering heritage includes ClickHouse, one of the defining open-source infrastructure projects of the last decade. Supporting the open ecosystem means more than releasing code — research, education, and hardware are part of it too. We open-sourced Soperator, our Kubernetes operator for Slurm, and contributed our server hardware designs to the Open Compute Project.

We maintain SWE-Rebench, open leaderboards and datasets for AI software engineering cited by leading labs, and this year released the Nebius Agents Blueprint, an open playbook for taking agents from prototype to production. Echo, the AI agent built into our own console, runs on open models.

And through Nebius Academy and our Research Grants Program, we fund research from Laude Ventures' Slingshots program to UCSF’s open-source protein modelling work to Télécom SudParis' research into LLM toxicity and AI safety.

## More people can make it betterMore people can make it better

An open system is not automatically better; its advantage is that more people can work on it. A researcher can test new training objectives against an open model and an agent developer can tell whether an improvement came from the model, the harness, or the tools.

And when something fails, as every system does, more people can reproduce the failure, test a mitigation, and share the fix. Openness does not automatically make a system safe, just as secrecy does not make one secure, but it means more hands on every problem.

And the gains are not confined to open systems: proprietary models train with the same open frameworks and build on the same published methods. Open source moves the whole industry.

## Where this goesWhere this goes

A technological shift of this scale arrives a few times a century, and if its most capable systems concentrate in a few hands, everyone else builds on foundations they had no role in shaping and cannot examine.

Open models won’t replace proprietary ones; businesses will use both, just as nearly every organization, Nebius included, mixes open and proprietary code. Nor is openness the opposite of a business: the software industry has run profitable companies on open source for decades, and open-weight AI is already doing the same.

The point of openness is choice, not orthodoxy. A strong open ecosystem is what keeps scientific claims checkable and lets a good idea travel from whoever had it to whoever needs it.

None of this is guaranteed. It has to be built, and maintained, at every layer of the AI stack.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Matt Zeiler
SVP Research, Nebius

Contents

- An open model is only one part of the stack

- Open research compounds

- Building in the open

- More people can make it better

- Where this goes

## See also

### 

LK losses: Training speculative decoding draft models to directly maximize acceptance rate

We introduce LK losses — training objectives that directly optimize the acceptance rate for speculative decoding draft models. They are a drop-in replacement for KL divergence, with no computational overhead, and they work with any draft architecture and any target model size, to deliver consistent improvements in inference throughput across models ranging from 8B to 685B parameters. We are open-sourcing our trained draft models (LK-Speculators) and training datasets (Infinity-Instruct-Completions). An implementation of LK losses is also available as a pull request to SpecForge.

April 10, 2026
16 mins to read

### 

Introducing Managed Soperator: Your quick access to Slurm training

Managed Soperator, our fully managed Slurm-on-Kubernetes solution, is now available for everyone in self-service. It provides you with a ready-to-work Slurm training cluster, powered by modern hardware and delivered with all necessary pre-installed libraries and drivers — allowing you to start ML training immediately.

June 18, 2025
4 mins to read

### 

MLPerf® Inference v6.0: Top-tier AI performance on NVIDIA Blackwell and Blackwell Ultra

The results of our MLPerf® Inference v6.0 submission demonstrate Nebius’ ability to maximize efficiency for modern AI inference workloads on the latest NVIDIA Blackwell and Blackwell Ultra platforms.

April 1, 2026
14 mins to read

Sign in to save this post
Sign In
