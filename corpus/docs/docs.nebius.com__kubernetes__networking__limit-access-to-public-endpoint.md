# Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster

Source: https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Access restriction for a public endpoint of a Managed Service for Kubernetes® cluster

If a Managed Service for Kubernetes cluster has a public endpoint, one can access it from any IP address on the internet. You can limit this access and only allow certain IP addresses to reach the cluster. To do so, specify allowed CIDR blocks in the cluster configuration.

When you enable a public endpoint for a Managed Kubernetes cluster, Nebius AI Cloud allocates a public IP address and provisions a load balancer to the cluster. This load balancer routes traffic to the [control plane instances](https://docs.nebius.com/kubernetes/components.md#control-plane-components). With access restriction set for a public endpoint, the allowlist of IP addresses takes effect at the network interface level of those instances based on [security groups](https://docs.nebius.com/vpc/security-groups/overview.md).

The access restriction doesn't affect the private endpoint and internal traffic. The private endpoint remains open as before.

## Prerequisites

Set up the interface that you are going to use:

**CLI**

[Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

**Terraform**

[Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.

**Go SDK**

[Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).

**Python SDK**

[Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).

**JavaScript SDK**

[Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).

## How to set an allowlist to access a Managed Kubernetes cluster

Set allowed CIDR blocks when you create or update a cluster.

The CIDR blocks must follow the IPv4 format. Bits for hosts must be equal to zero. Examples of valid CIDR blocks:

* `192.168.0.0/24` where the last eight bits are allocated to hosts and equal to zero.
* `8.8.8.64/26` where the last six bits are allocated to hosts and equal to zero (64 in the decimal system is 01000000 in the binary system).

**CLI**

Pass each CIDR block as a separate `--control-plane-endpoints-public-endpoint-allowed-cidrs` parameter. To set an allowlist of CIDR blocks, do one of the following:

* Create a cluster with limited access to the public endpoint:

  ```bash theme={null}
  nebius mk8s cluster create \
    --control-plane-endpoints-public-endpoint=true \
    --control-plane-endpoints-public-endpoint-allowed-cidrs "203.0.113.0/24" \
    --control-plane-endpoints-public-endpoint-allowed-cidrs "198.51.100.128/25" \
    ...
  ```

* Update a cluster and restrict access to the public endpoint:

  ```bash theme={null}
  nebius mk8s cluster update <cluster_ID> \
    --control-plane-endpoints-public-endpoint-allowed-cidrs "203.0.113.0/24" \
    --control-plane-endpoints-public-endpoint-allowed-cidrs "198.51.100.128/25"
  ```

  The `update` command overwrites the list of CIDR blocks. If you added any CIDR blocks earlier and you want to preserve them, specify these CIDR blocks in the `update` command.

**Terraform**

List the CIDR blocks in the `allowed_cidrs` parameter of the cluster's public endpoint:

```hcl theme={null}
resource "nebius_mk8s_v1_cluster" "my_cluster" {
  ...
  control_plane = {
    ...
    endpoints = {
      public_endpoint = {
        allowed_cidrs = ["203.0.113.0/24", "198.51.100.128/25"]
      }
    }
  }
}
```

Applying the configuration overwrites the list of CIDR blocks. If you added any CIDR blocks earlier and you want to preserve them, keep these CIDR blocks in the configuration.

**Go SDK**

Set `AllowedCidrs` in `PublicEndpointSpec` when you create or update a cluster:

```go theme={null}
clusterToRestrict, err := sdk.Services().MK8S().V1().
    Cluster().Get(
        ctx,
        &mk8s.GetClusterRequest{
            Id: "<cluster_ID>",
        },
    )
if err != nil {
    return err
}
restrictSpec := clusterToRestrict.GetSpec()
if restrictSpec == nil ||
    restrictSpec.GetControlPlane() == nil {
    return fmt.Errorf("cluster control plane spec is missing")
}
restrictSpec.ControlPlane.Endpoints =
    &mk8s.ControlPlaneEndpointsSpec{
        PublicEndpoint: &mk8s.PublicEndpointSpec{
            AllowedCidrs: []string{
                "203.0.113.0/24",
                "198.51.100.128/25",
            },
        },
    }
restrictOperation, err := sdk.Services().MK8S().V1().
    Cluster().Update(
        ctx,
        &mk8s.UpdateClusterRequest{
            Metadata: clusterToRestrict.GetMetadata(),
            Spec:     restrictSpec,
        },
    )
if err != nil {
    return err
}
if _, err = restrictOperation.Wait(ctx); err != nil {
    return err
}
```

The update overwrites the list of CIDR blocks. If you added any CIDR blocks earlier and you want to preserve them, include these CIDR blocks in `AllowedCidrs`.

**Python SDK**

Set `allowed_cidrs` in `PublicEndpointSpec` when you create or update a cluster:

```python theme={null}
restrict_cluster_service = ClusterServiceClient(sdk)
cluster_to_restrict = await restrict_cluster_service.get(
    GetClusterRequest(id="<cluster_ID>"),
)
if cluster_to_restrict.spec is None:
    raise ValueError("cluster spec is missing")
if cluster_to_restrict.spec.control_plane is None:
    raise ValueError("cluster control plane spec is missing")
cluster_to_restrict.spec.control_plane.endpoints = (
    ControlPlaneEndpointsSpec(
        public_endpoint=PublicEndpointSpec(
            allowed_cidrs=[
                "203.0.113.0/24",
                "198.51.100.128/25",
            ],
        ),
    )
)
restrict_operation = await restrict_cluster_service.update(
    UpdateClusterRequest(
        metadata=cluster_to_restrict.metadata,
        spec=cluster_to_restrict.spec,
    ),
)
await restrict_operation.wait()
```

The update overwrites the list of CIDR blocks. If you added any CIDR blocks earlier and you want to preserve them, include these CIDR blocks in `allowed_cidrs`.

**JavaScript SDK**

Set `allowedCidrs` in `PublicEndpointSpec` when you create or update a cluster:

```ts theme={null}
const restrictClusterService = new ClusterService(sdk);
const clusterToRestrict = await restrictClusterService.get(
  GetClusterRequest.create({
    id: "<cluster_ID>",
  }),
);
if (!clusterToRestrict.spec?.controlPlane) {
  throw new Error("cluster control plane spec is missing");
}
clusterToRestrict.spec.controlPlane.endpoints =
  ControlPlaneEndpointsSpec.create({
    publicEndpoint: PublicEndpointSpec.create({
      allowedCidrs: ["203.0.113.0/24", "198.51.100.128/25"],
    }),
  });
const restrictOperation = await restrictClusterService.update(
  UpdateClusterRequest.create({
    metadata: clusterToRestrict.metadata,
    spec: clusterToRestrict.spec,
  }),
).result;
await restrictOperation.wait();
```

The update overwrites the list of CIDR blocks. If you added any CIDR blocks earlier and you want to preserve them, include these CIDR blocks in `allowedCidrs`.

For more information about other parameters, see [How to create and modify Managed Service for Kubernetes® clusters](https://docs.nebius.com/kubernetes/clusters/manage.md).
