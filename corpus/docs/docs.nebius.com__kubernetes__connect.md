# How to connect to Managed Service for Kubernetes® clusters using kubectl

Source: https://docs.nebius.com/kubernetes/connect

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to connect to Managed Service for Kubernetes® clusters using kubectl

Use the public endpoint to connect to the cluster from the internet and the private endpoint to connect from a Compute virtual machine.

**From the internet**

1. Generate a kubeconfig file:

   ```bash theme={null}
   nebius mk8s cluster get-credentials \
     --id <cluster_ID> --external
   ```

2. Use kubectl:

   ```bash theme={null}
   kubectl cluster-info
   ```

> [!TIP]
>
> You can limit access to the public endpoint and only allow certain IP addresses to connect to the cluster. For more information, see [Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md).

**From a Compute VM**

> [!WARNING]
>
> **Requirements to connect to a VM with private IP address**
>
> To connect to a Managed Service for Kubernetes cluster from a Compute VM using a [private IP address](https://docs.nebius.com/compute/virtual-machines/network.md#private-ip) or another cluster using a private load balancer, both must be in the same [network](https://docs.nebius.com/vpc/overview.md#network) and [region](https://docs.nebius.com/overview/regions.md). They can use different subnets, [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) and [routing tables](https://docs.nebius.com/vpc/overview.md#routing-table).

1. Generate a kubeconfig file:

   ```bash theme={null}
   nebius mk8s cluster get-credentials \
     --id <cluster_ID> --internal
   ```

2. Use kubectl:

   ```bash theme={null}
   kubectl cluster-info
   ```
