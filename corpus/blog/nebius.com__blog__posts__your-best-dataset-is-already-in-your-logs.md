# Data Lab: Your best dataset is already in your logs

Source: https://nebius.com/blog/posts/your-best-dataset-is-already-in-your-logs

Skip to main content

Every team building AI products eventually reaches the same moment.

The first model version ships. Users start interacting with it. The product begins generating the only signal that really matters: real prompts, real outputs, real failure modes and real edge cases. The raw material for a better next model is finally there, but momentum soon slows down.

The logs sit in one system. Existing datasets sit in another. Someone exports rows, cleans them with scripts, reshapes them for training, uploads them somewhere else and tries to reconnect the result back to deployment. By the time that loop closes, the insight that started it is already old.

Data Lab, launching today in Nebius Token Factory, is built to close that gap.

## Training is no longer the bottleneck. Iteration isTraining is no longer the bottleneck. Iteration is

Getting a model job to run is no longer the hardest part for most teams. Access to GPUs is better than it was. Fine-tuning and post-training workflows are more standardized. The operational problem has moved.

The hard part now is deciding what should go into the next model version, and doing it fast enough that learning compounds.

Teams still lose time finding the right production examples, isolating the behavior that needs improvement and feeding curated data back into the next training cycle without rebuilding the workflow every time. This is where many AI teams get stuck: not on compute, but on iteration. Solving training helps a team run a job, while solving iteration helps them build a system that gets better over time.

## The highest-value training signal usually already existsThe highest-value training signal usually already exists

For most teams, the best data for the next cycle does not come from a benchmark assembled far from the product. It comes from the product itself.

Production logs show where the model is strong, where it drifts, which prompts keep recurring, which outputs fail and what “good enough” looks like in context. They reflect the workload you are actually running.

The problem is that most stacks still treat this signal as something to observe, not something to reuse. Teams can inspect it, count it, maybe alert on it. Turning it into model-improvement input is still too manual, too fragmented and too slow.

## What Data Lab doesWhat Data Lab does

Data Lab adds a workspace to Token Factory for turning that signal, plus any existing data you already have, into reusable datasets for post-training.

In practice: explore inference logs and existing datasets in one place, filter down to the behavior that matters, create a reusable dataset and move directly into post-training inside Token Factory. No rebuilding the pipeline each time.

The point is not to make one cleanup project slightly easier. It is to make model iteration repeatable.

## Why moving data slows the loop downWhy moving data slows the loop down

Most enterprise teams do not get stuck on the idea of improving the model. They get stuck when the workflow requires another copy of production data.

Once data has to be exported into a second vendor-managed environment, the process gets heavier. Security review enters the critical path. Ownership gets fuzzier. Another copy has to be tracked, secured and explained. None of that improves the model. It just slows the loop down.

That is why S3 support matters. Teams can connect S3-compatible files where they already live instead of treating data movement as the price of admission: metadata-first, no raw-data copy and the underlying data stays in the storage system your team already controls.

For enterprise teams, that is not a minor convenience. It is often the difference between a workflow that gets adopted and one that stalls before the next training run.

## What ships with Data LabWhat ships with Data Lab

- 

One workspace for inference logs and existing datasets, with explore and filter in a single place

- 

Reusable dataset creation from production signal you already have, without manual exports or glue code

- 

S3-connected workflows that attach files where they live, metadata-first, with no raw-data copy

- 

A direct bridge into post-training inside Token Factory, so the loop closes.

## The shiftThe shift

For a long time, AI infrastructure conversations focused on whether teams could train or serve models efficiently, which made sense when access to compute was the main constraint.

Once a model is live, the more important question is how quickly a team can learn from real usage and feed that learning back into the system. The best dataset often arrives after launch, and the real test is whether your platform lets you use it.

- Get started with Data Lab

- Read the documentation

- Contact sales

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Dylan Bristot
Product Marketing, Token Factory

Contents

- Training is no longer the bottleneck. Iteration is

- The highest-value training signal usually already exists

- What Data Lab does

- Why moving data slows the loop down

- What ships with Data Lab

- The shift

Sign in to save this post
Sign In
