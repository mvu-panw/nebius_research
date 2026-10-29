# Getting public IPv4 ranges

Source: https://docs.nebius.com/vpc/addressing/public-address-ranges

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting public IPv4 ranges

Public [allocations](https://docs.nebius.com/vpc/overview.md#allocation) use public IPv4 addresses from public pools in [Virtual Networks](https://docs.nebius.com/vpc/overview.md#default-virtual-networks-resources). The available public IPv4 range depends on the project [region](https://docs.nebius.com/overview/regions.md). This page explains how to get the public IPv4 [CIDR blocks](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_blocks) that are available for allocations in a project.

## Prerequisites

> [!TIP]
>
> You do not need to complete any prerequisites if you use the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to get public IPv4 ranges

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Networking** → **Virtual networks**.
2. If you have access to multiple projects, expand the list of projects and select the required project.
3. Click **Actions** → **View public CIDR blocks**.

   The **Public CIDR blocks** window shows the public IPv4 CIDR blocks that are available for allocations in the selected project and region.

**CLI**

1. [Get the ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) of the default network in the required project.

2. Get the ID of the default network's public pool:

   ```bash theme={null}
   nebius vpc network get --id <network_ID>
   ```

   The pool ID is specified in the `spec.ipv4_public_pools.pools.id` parameter of the output.

   If the default network contains several public pools, a public address can be allocated from any of these pools.

3. Get the CIDR blocks of the public pool:

   ```bash theme={null}
   nebius vpc pool get --id <pool_ID>
   ```

   The output looks like this:

   ```yaml theme={null}
   metadata:
     id: vpcpool-***
     parent_id: project-***
     name: default-public-pool
     resource_version: "2"
     created_at: "2025-07-21T16:21:38.791627Z"
     updated_at: "2025-07-21T16:46:45.356295Z"
   spec:
     source_pool_id: vpcpool-e00***
     version: IPV4
     visibility: PUBLIC
   status:
     state: READY
     cidrs:
       - 89.169.96.0/22
       - 89.169.102.0/23
       - 89.169.108.0/22
     scope_id: vpcscope-e00***
     assignment:
       networks:
         - vpcnetwork-e00***
   ```

   The output contains the following parameters:

   * `metadata.id`: The ID of the [public pool](https://docs.nebius.com/vpc/overview.md#pool).
   * `metadata.parent_id`: The project ID.
   * `metadata.name`: The name of the public pool.
   * `spec.source_pool_id`: The ID of the source pool for this public pool.
   * `spec.version`: The IP version of the pool.
   * `spec.visibility`: The pool visibility.
   * `status.state`: The current state of the public pool.
   * `status.cidrs`: The public IPv4 CIDR blocks that are available for allocations in the project. These addresses form the public IPv4 range from which Virtual Networks allocates public addresses.
   * `status.scope_id`: The ID of the scope associated with the public pool.
   * `status.assignment.networks`: The IDs of the networks that use this public pool.

**Go SDK**

1. [Get the ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) of the default network in the required project.

2. Get the ID of the default network's public pool:

   ```go theme={null}
   network, err := sdk.Services().VPC().V1().
       Network().Get(
           ctx,
           &vpc.GetNetworkRequest{
               Id: "<network_ID>",
           },
       )
   if err != nil {
       return err
   }
   fmt.Println(network)
   ```

   Set `Id` to the network ID. The pool ID is specified in `Spec.Ipv4PublicPools.Pools[].Id` of the response.

   If the default network contains several public pools, a public address can be allocated from any of these pools.

3. Get the CIDR blocks of the public pool:

   ```go theme={null}
   pool, err := sdk.Services().VPC().V1().
       Pool().Get(
           ctx,
           &vpc.GetPoolRequest{
               Id: "<pool_ID>",
           },
       )
   if err != nil {
       return err
   }
   fmt.Println(pool)
   ```

   Set `Id` to the pool ID. The `Status.Cidrs` field of the response contains the public IPv4 CIDR blocks that are available for allocations in the project. These addresses form the public IPv4 range from which Virtual Networks allocates public addresses.

**Python SDK**

1. [Get the ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) of the default network in the required project.

2. Get the ID of the default network's public pool:

   ```python theme={null}
   network_service = NetworkServiceClient(sdk)
   network = await network_service.get(
       GetNetworkRequest(id="<network_ID>"),
   )
   print(network)
   ```

   Set `id` to the network ID. The pool ID is specified in `spec.ipv4_public_pools.pools[].id` of the response.

   If the default network contains several public pools, a public address can be allocated from any of these pools.

3. Get the CIDR blocks of the public pool:

   ```python theme={null}
   pool_service = PoolServiceClient(sdk)
   pool = await pool_service.get(
       GetPoolRequest(id="<pool_ID>"),
   )
   print(pool)
   ```

   Set `id` to the pool ID. The `status.cidrs` field of the response contains the public IPv4 CIDR blocks that are available for allocations in the project. These addresses form the public IPv4 range from which Virtual Networks allocates public addresses.

**JavaScript SDK**

1. [Get the ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id) of the default network in the required project.

2. Get the ID of the default network's public pool:

   ```ts theme={null}
   const networkService = new NetworkService(sdk);
   const network = await networkService.get(
     GetNetworkRequest.create({
       id: "<network_ID>",
     }),
   );
   console.log(network);
   ```

   Set `id` to the network ID. The pool ID is specified in `spec.ipv4PublicPools.pools[].id` of the response.

   If the default network contains several public pools, a public address can be allocated from any of these pools.

3. Get the CIDR blocks of the public pool:

   ```ts theme={null}
   const poolService = new PoolService(sdk);
   const pool = await poolService.get(
     GetPoolRequest.create({
       id: "<pool_ID>",
     }),
   );
   console.log(pool);
   ```

   Set `id` to the pool ID. The `status.cidrs` field of the response contains the public IPv4 CIDR blocks that are available for allocations in the project. These addresses form the public IPv4 range from which Virtual Networks allocates public addresses.
