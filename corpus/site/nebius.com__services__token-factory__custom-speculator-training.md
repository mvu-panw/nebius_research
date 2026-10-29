# Custom Speculator Training, Token Factory by Nebius

Source: https://nebius.com/services/token-factory/custom-speculator-training

Skip to main content

## Throughput on real traffic

A drafter trained on your distribution raises the acceptance rate where it matters. Tokens-per-second improves on the prompt shapes your product actually serves, not on a benchmark someone else picked.

## Predictable tail latency

Acceptance rate is about predictability as much as speed. A workload-matched drafter tightens the gap between median and tail latency on the traffic your system sees every day.

## Unit economics that scale

Fewer GPU-seconds per request. The lever moves where it matters most: at the volume where successful pilots become expensive steady state.

## How the workflow works

## Step 1: Bring your data

Prepare datasets in Data Lab. Attach S3-compatible files in place, query production logs, and merge them with the synthetic seed datasets we ship for the priority launch models. Or upload curated JSONL directly through the Post-training console or the Files API.

## Step 2: Train

Pick a base model, point at the dataset, run a job from the Post-training page. Preset hyperparameters cover the common case. Full hyperparameter control — decoding heads, loss type, learning rate, scheduler, drafter type — is there for teams that want to tune.

## Step 3: Deploy

The trained drafter lands in Custom Weights and deploys on a Dedicated Endpoint alongside the base model. Solutions engineers review the first deploy — a deliberate human-in-the-loop on the part of the stack that affects how your product feels.

## Step 4: Measure and retrain

Acceptance rate, TPS, and end-to-end latency sit alongside the rest of your serving metrics. When the workload changes materially, retrain. The cadence becomes part of how you operate the model.

## Train better drafters from real data

## Train on production data

Use Data Lab to inspect inference logs, isolate the failure cases that matter, and assemble a workload-shaped training set. Bring data from S3-compatible storage without copying it into a separate store.
View documentation

## Tune without rewriting your stack

Start from preset hyperparameters or open up the full configuration surface — decoding heads, loss function, scheduler, drafter type. Built on Papyrax, our production training framework.
Read the training guide

## Deploy on a Dedicated Endpoint

The trained drafter deploys alongside the base model with the same isolation, region, and SLO rules as the rest of your endpoint. Acceptance rate, TPS, and end-to-end latency stream into the same dashboards.
Start with a solutions engineer

## Documentation and guides

Read the docs, walkthroughs, and research that explain how Custom Speculator Training works end to end.

## From production data to drafter

Step-by-step guide from dataset preparation in Data Lab to a deployed custom drafter on a Dedicated Endpoint.
Learn more

## LK Losses and the research behind it

The loss function we use directly optimizes draft-token acceptance rate instead of proxying through KL divergence. Paper, code, and the SpecForge contribution.
Learn more

## Operating in production

How to measure acceptance rate and TPS, decide when to retrain, and roll new drafters into a running endpoint without disrupting serving.
Learn more

## 

One workspace for model improvement

Custom Speculator Training plugs into a Token Factory loop that’s already running. Post-training has been live since December 2025. Data Lab v2 launched in May 2026 with S3 import and the dataset merge workflow. RL Platform v1 entered private preview in early June. Custom Speculator is the moment the loop closes — customers shape both model behavior and serving behavior on their own data, in one platform.
Get started

## Built on open research

Our team’s work on LK Losses introduces a loss function that directly optimizes draft-token acceptance rate instead of proxying it through KL divergence.

Across model sizes from 8B to 685B parameters, LK Losses show consistent acceptance-rate gains over KL-trained baselines. The implementation is open in our SpecForge contribution and the LK-Speculators model family on Hugging Face.

The training pipeline runs on Papyrax, the same distributed training framework powering Post-training since December 2025.
Talk to sales

## Questions and answers

How much faster will my workload get?

It’s workload-dependent. The gain depends on how concentrated your prompt distribution is, how much your generic drafter is leaving on the table today, and how much production data you can train on. The honest answer is that a workload-shaped drafter raises the acceptance-rate ceiling that a generic drafter sets — we’ll scope a real number with you on a sample of your data.

What models does this support at launch?

At launch, training is supported for Eagle 3, Nebius-optimized Eagle 3 (TF_eagle3), and MTP (Multi-Token Prediction). Broader arbitrary-model support is on the roadmap.

Where does the training data come from?

Two paths.

- 

Bring your own training data through Data Lab (S3 import in place, query production logs, merge with synthetic seed data) or directly via the Files API or Post-training console upload.

- 

Start with the synthetic seed datasets we ship for the priority launch models, then add your own data once you’ve seen the flow.

Where do I start the training job?

From the Post-training page in Token Factory.

How is deployment handled?

At launch, our solutions engineers review the first deploy. Custom drafters affect the serving path; we want a human in the loop the first time. DE self-serve speculator deployment is on the roadmap as a separate release.

Can we keep our data isolated?

Yes — same isolation rules as the rest of your Token Factory account. Encrypted at rest and in transit, isolated per tenant, audit-logged. Data Lab attaches S3-compatible files in place without copying raw data. Region selection follows your Dedicated Endpoint region.

Is Custom Speculator a standalone product?

No. Custom Speculator Training is part of Token Factory and is most valuable when paired with Data Lab (data preparation), Post-training (training), and Dedicated Endpoints (serving).

How is it priced?

Metered in tokens, the same way SFT is, with t-shirt-sized SKUs based on the parameter range of the base model.

## Train the draft model for your workload
Get startedTalk to sales

## More to know

Documentation​
Launch blog​
LK Losses research​
