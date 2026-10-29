# Exposing services with load balancers

Source: https://docs.nebius.com/kubernetes/clusters/load-balancer

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Exposing services with load balancers

You can expose a [Kubernetes service](https://kubernetes.io/docs/concepts/services-networking/service/) in your Managed Service for Kubernetes cluster using a *load balancer*. The load balancer receives traffic on a public or private IP address, depending on how you [set it up](#how-to-set-up-a-load-balancer), and distributes the traffic between the service's Pods automatically.

> [!WARNING]
>
> **Requirements to connect to a VM with private IP address**
>
> To connect to a Managed Service for Kubernetes cluster from a Compute VM using a [private IP address](https://docs.nebius.com/compute/virtual-machines/network.md#private-ip) or another cluster using a private load balancer, both must be in the same [network](https://docs.nebius.com/vpc/overview.md#network) and [region](https://docs.nebius.com/overview/regions.md). They can use different subnets, [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) and [routing tables](https://docs.nebius.com/vpc/overview.md#routing-table).

## Prerequisites

Before you start setting up a load balancer, you need to [create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) and [connect to it](https://docs.nebius.com/kubernetes/connect.md) using kubectl.

## Load balancers types

By default, load balancers are created with public IP addresses. To expose your service on a private IP address instead, add `nebius.com/load-balancer-type: internal` to the annotations of the service.

> [!NOTE]
>
> To retain an IP address that was automatically allocated to a load balancer and reuse it after deleting or recreating the service, follow the [How to convert a dynamically assigned public IP address to a reusable allocation](https://docs.nebius.com/kubernetes/networking/dynamic-to-static.md) guide.

If you have created an IP address allocation ([example for public IP addresses](https://docs.nebius.com/compute/virtual-machines/network.md#public-ip-addresses)) and want to use it to allocate an IP address to a load balancer, add its ID to the service annotation `nebius.com/load-balancer-allocation-id`. The allocation type (public or private) must match the load balancer type.

The load balancer listener is created in the control plane subnet of the cluster. The allocation that you specify in `nebius.com/load-balancer-allocation-id` must belong to this subnet.

The table below explains how these two annotations work together:

| Type is `internal` | Allocation ID is set | Result |
| - | - | - |
| Yes | Yes | Load balancer gets a **private** IP address from the **provided** allocation |
| Yes | No | Load balancer gets a **private** IP address from a **new** allocation |
| No | Yes | Load balancer gets a **public** IP address from the **provided** allocation |
| No | No | Load balancer gets a **public** IP address from a **new** allocation |

To allocate a public IP address from a specific IP pool, add the pool ID to the `nebius.com/load-balancer-pool-id` service annotation. When this annotation is set, the IP address is allocated from the specified pool instead of the default user subnet pool. For more information about IP pools, see the [Virtual Networks overview](https://docs.nebius.com/vpc/overview.md#pool).

```yaml theme={null}
annotations:
  nebius.com/load-balancer-pool-id: "<pool_ID>"
```

## Limitations

* Managed Service for Kubernetes doesn't support load balancer services that set `externalTrafficPolicy` to `Local`.

* Load balancers don't support PROXY protocol v1 or v2. There is no service annotation to enable it.

## How to set up a load balancer

**With a private IP address**

1. Create the manifest to set up the internal load balancer service with a private IP address (we will refer to it later as `service.yaml`):

   ```yaml theme={null}
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx
     annotations:
       nebius.com/load-balancer-type: "internal"
   spec:
     selector:
       app: nginx
     ports:
       - protocol: TCP
         port: 80
         targetPort: 80
     type: LoadBalancer
   ```

2. Create the manifest for nginx deployment (we will refer to it later as `deployment.yaml`):

   ```yaml theme={null}
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:latest
           ports:
           - containerPort: 80
   ```

3. Apply the configurations:

   ```bash theme={null}
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

4. Check the service and the allocated IP address:

   ```bash theme={null}
   kubectl get svc nginx
   ```

   You will receive an output like the one below:

   ```bash theme={null}
   NAME         TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
   nginx        LoadBalancer   10.158.250.188   192.168.0.112   80:30512/TCP   4s
   ```

**With a public IP address**

1. Create the manifest to set up the internal load balancer service with a public IP address (we will refer to it later as `service.yaml`):

   ```yaml theme={null}
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx
   spec:
     selector:
       app: nginx
     ports:
       - protocol: TCP
         port: 80
         targetPort: 80
     type: LoadBalancer
   ```

2. Create the manifest for nginx deployment (we will refer to it later as `deployment.yaml`):

   ```yaml theme={null}
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:latest
           ports:
           - containerPort: 80
   ```

3. Apply the configurations:

   ```bash theme={null}
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

4. Check the service and the allocated IP address:

   ```bash theme={null}
   kubectl get svc nginx
   ```

   You will see an output like the one below:

   ```bash theme={null}
   NAME    TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
   nginx   LoadBalancer   10.158.105.48   195.242.8.219   80:30816/TCP   13s
   ```

5. Use the `EXTERNAL-IP` from the previous command output to connect to the service from outside of the Kubernetes cluster:

   ```bash theme={null}
   curl -i <EXTERNAL-IP>
   ```

   You will see an output like the one below:

   ```bash theme={null}
   HTTP/1.1 200 OK
   Server: nginx/1.27.1
   ```
