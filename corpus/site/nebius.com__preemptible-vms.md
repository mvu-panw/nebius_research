# Preemptible VMs with Spot pricing

Source: https://nebius.com/preemptible-vms

Skip to main content

## Unlock GPU capacity for flexible workloads

Move work that can wait or restart into lower-price windows, such as experiments, queued jobs and other workloads with flexible timing.

## Plan with transparent, market-driven pricing

Benefit from rates that respond to demand and available capacity to decide when and where to run.

## Choose the price that works for your requirement

Set a maximum price per GPU-hour or follow the current spot price, choosing the approach that fits your workload’s priorities.

## Live Spot Preemptible VM prices
Access market-driven prices across GPU platforms and regions.View all live spot prices

## Two ways to run

## Set your maximum price

For workloads where price is the priority

- Define the highest price per GPU-hour you’re willing to pay.

- Run when the spot price is at or below your limit and capacity is available, paying the applicable spot price.

- Your VM stops if the market price exceeds your limit.

## Follow the market price

To avoid price-triggered interruptions

- Accept the current spot price as it changes.

- Avoid stops triggered by a maximum-price threshold.

- Your VM will only stop when capacity is needed elsewhere.

Note that both options use preemptible capacity. Setting a higher maximum or following the price does not reserve GPUs or guarantee continuous runtime.

## Built for work that can pause and resume

## Experiment and evaluate

Test model configurations, compare approaches and run evaluations without requiring a fixed completion time.

## Process data

Run queued preprocessing, transformation and other GPU jobs that can retry or resume after interruption.

## Fine-tune with checkpoints

Use spot capacity for shorter fine-tuning jobs or workflows designed to save progress and recover.

## Run batch inference

Process offline inference jobs that can be retried and do not need an immediate response.

## 

Access now in three steps

- 

Choose your GPU and region where capacity is available

- 

Set your maximum price or follow the market

- 

Launch your workload

## Get started

Access GPU capacity at market-driven prices, with complete control over what you’re willing to pay.
Get startedRead the docsRead the blog

## Frequently asked questions

Does spot pricing apply to all Preemptible VMs?

Yes. All Preemptible Virtual Machines on the Nebius AI Cloud will with dynamic spot pricing. You’ll see “preemptible” in the console and documentation.

How often can the price change?

Spot prices are dynamic and may increase or decrease based on available capacity, cluster utilization, customer demand and customer pricing preferences. Current spot prices are displayed in the price calculator in the Nebius AI Cloud console and may vary during active use, including as frequently as every 15 minutes.

Does my maximum price limit my total bill?

No. It limits the spot price per GPU-hour. Total charges depend on GPU count, runtime and other billable resources.

What happens when my Preemptible VM is interrupted?

The Preemptible VM stops. Data on attached persistent volumes is retained, but data on local SSDs is lost. Save progress regularly to persistent storage.

Will my VM restart automatically?

Standalone preemptible VMs do not restart automatically. Restart them manually or arrange automation, subject to capacity and your pricing policy. Managed services have their own recovery behavior.

Do charges continue after a VM stops?

Retained resources, such as attached storage, can continue to incur charges until you delete them.

Which GPU models are available with spot pricing?

Spot pricing supports NVIDIA H100, H200, B200, B300 and RTX PRO 6000 GPUs. Supported configurations and available capacity vary by region. Check the Nebius console for current options and prices.

How does spot pricing compare with other Nebius pricing options?

Spot prices vary by GPU type, region and demand. Visit our GPU pricing page to compare pricing options and choose the right fit for your workload, including instances for workloads that require predictable capacity or cannot tolerate interruption.
