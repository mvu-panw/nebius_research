# Deploying Soperator clusters

Source: https://docs.nebius.com/slurm-soperator/deploy/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying Soperator clusters

Nebius AI Cloud offers two managed Slurm solutions powered by Soperator: Managed Service for Soperator and Pro Solution for Soperator. You can also deploy Soperator manually on a Managed Service for Kubernetes® cluster or on other cloud platforms.

## Nebius AI Cloud managed solutions

If you share reserved GPU capacity between Soperator training workloads and inference in Managed Service for Kubernetes, see [Ephemeral nodes in Soperator](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md).

### Managed Service for Soperator

Managed Service for Soperator allows you to deploy a Soperator cluster in all [Nebius AI Cloud regions](https://docs.nebius.com/overview/regions.md) except for `us-north1` and `uk-south2`, with just a few clicks. The service takes care of the underlying infrastructure so that you can get started with Slurm and Soperator with minimum effort.

> [!NOTE]
>
> GPU worker nodes in Soperator are only available if you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md) that reserve GPUs.

For deployment steps, see [Creating and deleting Soperator clusters in Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/managed-soperator/manage.md). For pricing and quotas, see [Pricing in Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/managed-soperator/resources/pricing.md) and [Quotas in Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/managed-soperator/resources/quotas.md).

### Pro Solution for Soperator

Pro Solution for Soperator is an expert-run solution from Nebius for customized or enterprise-scale GPU workloads. Our team of high-performance computing experts assists you with deploying a Soperator cluster and your applications on it. Depending on the scope and nature of your usage, Pro Solution for Soperator offers contracts with reserved capacity and discounted pricing. To sign up for Pro Solution for Soperator, [contact sales](https://nebius.com/services/soperator#ai-contact-form).

## Self-deployment in Nebius AI Cloud

If you want to manually deploy a Soperator cluster in Nebius AI Cloud, you can use the [Terraform recipe](https://github.com/nebius/nebius-solution-library/tree/main/soperator) from the Nebius solution library. The recipe creates a [Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/index.md) cluster with Soperator and all additional Nebius AI Cloud resources, such as networks and shared filesystems. You can change settings in the recipe according to your needs.

## Self-deployment on other platforms and on-premises

You can install Soperator on any Kubernetes cluster that you deployed on a cloud platform or on-premises. For details, see [Soperator's GitHub repository](https://github.com/nebius/soperator/blob/main/docs/self-deploy.md).

> [!NOTE]
>
> Soperator has not been tested on platforms other than Nebius AI Cloud. If you experience a problem when installing or using it, create an [issue in the GitHub repository](https://github.com/nebius/soperator/issues).
