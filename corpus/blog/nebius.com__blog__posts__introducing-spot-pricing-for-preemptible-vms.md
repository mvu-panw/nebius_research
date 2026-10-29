# Introducing spot pricing for preemptible VMs

Source: https://nebius.com/blog/posts/introducing-spot-pricing-for-preemptible-vms

Skip to main content

A virtualized compute environment creates opportunities for both cloud providers and their customers. One is preemptible VMs (PVMs): interruptible compute for non-critical workloads that runs on pre-allocated, temporarily idle capacity. For the GPU compute market, which is still dealing with a scarcity problem, this distribution model presents an elegant solution. Today, we’re introducing dynamic spot pricing for PVMs: an algorithm that reads available capacity and real-time demand signals from Nebius users to set the price automatically.

We launched preemptible VMs last year and they’ve become popular among our customers. Customers use PVMs to complete non-critical tasks like data processing, experimentation, and short fine-tuning jobs, significantly cutting their GPU compute costs. Despite their short-term nature, most of our users finish their jobs and shut down their VMs themselves, or the VM shuts down automatically if they use Serverless AI. In our experience, only a small fraction of PVM workloads are interrupted by capacity reclamation.

From our standpoint as a provider, the preemptible mechanism lets us prevent idle compute in a data center facility and produce more AI value from the same input of energy, resulting in improved efficiency and sustainability.

## The pricing conundrumThe pricing conundrum

A pressing question for us was how to price PVMs: high, to maximize revenue, or low enough to attract demand as fast as possible?

We decided neither of those answers was quite right. Instead, as an engineering-driven company, we built a dynamic pricing mechanism that reads user demand and assesses available capacity, and then uses these variables to set a spot price for preemptible VMs at that specific moment.

This mechanism gives customers visibility into PVM pricing trends. Armed with this information, our customers can adapt their consumption strategy according to their unique needs and workloads: they can either schedule workloads for the lowest-price periods, or prioritize capacity access over potential cost-saving advantages.

## How spot pricing worksHow spot pricing works

The spot pricing system aggregates information about existing capacity and demand signals from Nebius customers, then calculates a spot price for preemptible VMs on a specific GPU type in a specific region. The spot price changes over time, but always stays between a price floor and a price ceiling, where the ceiling is one cent below the current on-demand GPU-hour rate.

Recent spot price changes, up to 30 days back, are shown in the pricing history diagram. This view is intended to help customers identify typical demand and pricing patterns, so they can make informed decisions about how to time their future PVM consumption.

To see the current spot price, customers can simply create a compute instance and select a preemptible virtual machine. The price is currently updated up to every 15 minutes and is the same for every resource type that runs on preemptible capacity, including Kubernetes clusters and Serverless AI.

## Chase the best price or follow the trendChase the best price or follow the trend

Spot pricing gives Nebius AI Cloud users two strategies from which to choose.

Chase the best price: To adopt this strategy, the customer creates a pricing policy that sets a max price: the highest amount per GPU-hour they are willing to pay, based on GPU type and region (see Figure 3). When the spot price is at or below the max price, the workload runs and the user pays the spot price. If the spot price exceeds the max price, the instance is stopped, data is retained, and the PVM can be restarted once the price comes back below the desired max price. Standalone VMs don’t restart on their own: restart them manually, or automate this via Terraform, SDK, API, or CLI. Kubernetes restarts preemptible VMs in your clusters automatically.

Follow the trend: This strategy prioritizes maximizing the chances of keeping the workload running. If a customer chooses to follow the spot price rather than set a max price when creating a compute resource, that resource is charged at the dynamic spot price, and the customer loses access to their preemptible VM only due to maintenance events or if this capacity is reclaimed.

For full information on how pricing policies work for PVMs, explore our docs.

## Get ready for spot pricingGet ready for spot pricing

Preemptible VMs fit the way many AI teams and developers want to work today: fast iteration, quick experiments, ad hoc compute access, and shorter time to results at a lower cost. By setting the price of these VMs algorithmically, we add control and choice on top of that flexibility. Customers can prioritize access to capacity first and follow the spot price, or prioritize cost by setting a price ceiling that suits them.

You can start using preemptible VMs today, and the new tooling and settings are already available. Dynamic pricing itself takes effect on 8 October. If you already use preemptible resources, you’ll need to configure a price setting for them before that date. Look out for an email with more information.

Learn more about spot pricing in our documentation.

## Explore Nebius AI Cloud

Sign up​
Docs​

## Explore Nebius Token Factory

Sign up​
Docs and support​

Anton Smith
Product Director at Nebius

Contents

- The pricing conundrum

- How spot pricing works

- Chase the best price or follow the trend

- Get ready for spot pricing

## See also

### 

Exploring the cost of training an AI model on cloud infrastructure

Training machine learning models can cost anywhere from tens of thousands to millions of dollars depending on model size, dataset volume and infrastructure. In this article we look at the main cost components of training in the cloud, what drives the final bill and how to optimize spending without compromising results.

June 19, 2025
10 mins to read

### 

Visibility that drives elasticity: Introducing Capacity Blocks and Capacity Dashboard

Today, we’re expanding Nebius AI Cloud’s elasticity even further with the introduction of Capacity Blocks and Capacity Dashboard — two new capabilities that bring additional clarity to GPU capacity management and give users full confidence in the compute they rely on.

December 17, 2025
4 mins to read

### 

Nebius AI Cloud “Aether 3.6”: Operating production AI with more control, efficiency, and confidence

Introducing Aether 3.6. Our latest quarterly platform release responds to how AI teams now operate at scale and with maturity, delivering a smoother developer experience, a stronger security and compliance foundation, advances across our in-house storage portfolio, and natural-language control over your AI cloud.

June 24, 2026
14 mins to read

Sign in to save this post
Sign In
