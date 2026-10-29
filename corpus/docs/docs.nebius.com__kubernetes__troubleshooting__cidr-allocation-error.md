# "Unable to allocate CIDR from the pool" error

Source: https://docs.nebius.com/kubernetes/troubleshooting/cidr-allocation-error

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# "Unable to allocate CIDR from the pool" error

When you create a Managed Service for Kubernetes® cluster, it may get stuck in the `Provisioning` status with the following error:

```text theme={null}
"rpc error: code = FailedPrecondition desc = Unable to allocate private
ipv4 cidr /32 from the pool. Please verify the availability of the cidrs
and retry the allocation."
```

This error usually indicates that there is not enough CIDR space available for IP address allocation. Possible causes:

* [Quota for IP addresses is exceeded](#quota-for-ip-addresses-is-exceeded)
* [Selected subnet is too small](#selected-subnet-is-too-small)
* [CIDR block is too large](#cidr-block-is-too-large)

## Quota for IP addresses is exceeded

You may not have enough free [quota](https://docs.nebius.com/vpc/resources/quotas-limits.md) for the IP addresses the cluster requires.

To find out if that is the case, get and compare the following information:

* See the complete list of required allocations in [Network requirements for Managed Service for Kubernetes® clusters](https://docs.nebius.com/kubernetes/networking/requirements.md).
* Check your free quota on the [Administration → Limits → Quotas](https://console.nebius.com/quotas) page in the web console.

To fix this, use one of the following solutions:

* Remove unused resources to free up quota.
* Request a quota increase on the **Administration** → **Limits** → **Quotas** page.

## Selected subnet is too small

The [subnet](https://docs.nebius.com/vpc/overview.md#subnet) you specified during cluster creation may not have enough CIDR blocks.

To find out if that is the case, get and compare the following information:

* See the complete list of required allocations in [Network requirements for Managed Service for Kubernetes® clusters](https://docs.nebius.com/kubernetes/networking/requirements.md).
* Get the subnet metadata:

  **CLI**

  ```bash theme={null}
  nebius vpc subnet get --id <subnet_ID>
  ```

  To find the available CIDR blocks, check the `cidr` values in the `spec.ipv4_private_pools.pools.cidrs` list in the response.

  **Go SDK**

  ```go theme={null}
  subnet, err := sdk.Services().VPC().V1().
      Subnet().Get(
          ctx,
          &vpc.GetSubnetRequest{
              Id: "<subnet_ID>",
          },
      )
  if err != nil {
      return err
  }
  fmt.Println(subnet)
  ```

  To find the available CIDR blocks, check the `Cidr` values in the `Spec.Ipv4PrivatePools.Pools.Cidrs` list in the response.

  **Python SDK**

  ```python theme={null}
  subnet_service = SubnetServiceClient(sdk)
  subnet = await subnet_service.get(
      GetSubnetRequest(id="<subnet_ID>"),
  )
  print(subnet)
  ```

  To find the available CIDR blocks, check the `cidr` values in the `spec.ipv4_private_pools.pools.cidrs` list in the response.

  **JavaScript SDK**

  ```ts theme={null}
  const subnetService = new SubnetService(sdk);
  const subnet = await subnetService.get(
    GetSubnetRequest.create({
      id: "<subnet_ID>",
    }),
  );
  console.log(subnet);
  ```

  To find the available CIDR blocks, check the `cidr` values in the `spec.ipv4PrivatePools.pools.cidrs` list in the response.

To fix this, use one of the following solutions:

* Add a [pool](https://docs.nebius.com/vpc/overview.md#pool) with more CIDR blocks to the subnet.
* Use another, larger subnet for your cluster.

## CIDR block is too large

If you specified a CIDR block for Kubernetes services that is too large, no free blocks for other control plane requirements may be left in the subnet.

To find out if that is the case, get and compare the following information:

* Get the subnet metadata:

  **CLI**

  ```bash theme={null}
  nebius vpc subnet get --id <subnet_ID>
  ```

  To find the available CIDR blocks, check the `cidr` values in the `spec.ipv4_private_pools.pools.cidrs` list in the response.

  **Go SDK**

  ```go theme={null}
  subnet, err := sdk.Services().VPC().V1().
      Subnet().Get(
          ctx,
          &vpc.GetSubnetRequest{
              Id: "<subnet_ID>",
          },
      )
  if err != nil {
      return err
  }
  fmt.Println(subnet)
  ```

  To find the available CIDR blocks, check the `Cidr` values in the `Spec.Ipv4PrivatePools.Pools.Cidrs` list in the response.

  **Python SDK**

  ```python theme={null}
  subnet_service = SubnetServiceClient(sdk)
  subnet = await subnet_service.get(
      GetSubnetRequest(id="<subnet_ID>"),
  )
  print(subnet)
  ```

  To find the available CIDR blocks, check the `cidr` values in the `spec.ipv4_private_pools.pools.cidrs` list in the response.

  **JavaScript SDK**

  ```ts theme={null}
  const subnetService = new SubnetService(sdk);
  const subnet = await subnetService.get(
    GetSubnetRequest.create({
      id: "<subnet_ID>",
    }),
  );
  console.log(subnet);
  ```

  To find the available CIDR blocks, check the `cidr` values in the `spec.ipv4PrivatePools.pools.cidrs` list in the response.

* Check the value of the `spec.kube_network.service_cidrs` parameter that you set during cluster creation.

To fix this, use one of the following solutions:

* Specify a smaller block for services in the `spec.kube_network.service_cidrs` parameter.
* Add a [pool](https://docs.nebius.com/vpc/overview.md#pool) with more CIDR blocks to the subnet.
* Use another, larger subnet for your cluster.
