# Kubernetes® versions in Managed Service for Kubernetes

Source: https://docs.nebius.com/kubernetes/versions

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Kubernetes® versions in Managed Service for Kubernetes

You can configure the [Kubernetes version](https://kubernetes.io/releases/) that is used on your Managed Kubernetes clusters and node groups.

* **Clusters**: The Kubernetes version is used for [control plane components](https://kubernetes.io/docs/concepts/architecture/#control-plane-components). It is *required* when [creating a cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters).

* **Node groups**: The Kubernetes version is used for node components. It is *optional* when [creating a node group](https://docs.nebius.com/kubernetes/node-groups/manage.md#how-to-create-node-groups). By default, a node group uses the same Kubernetes version as its parent cluster. A node group cannot have a higher version than the cluster.

## Available Kubernetes versions

The following Kubernetes versions are currently supported for clusters and node groups:

* [1.36](https://kubernetes.io/releases/#release-v1-36): Recommended. New clusters use this version.
* [1.35](https://kubernetes.io/releases/#release-v1-35)
* [1.34](https://kubernetes.io/releases/#release-v1-34)
* [1.33](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.33.md), [1.32](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.32.md), [1.31](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.31.md) and [1.30](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.30.md): Not recommended as they reached end of life. These versions are supported for clusters created earlier, but we recommend upgrading to the newest version.

For the version deprecation policy and end-of-life timeline, see [Kubernetes® version deprecation policy in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/version-deprecation.md).

## Upgrading Kubernetes version

You can upgrade a cluster to a newer Kubernetes version manually; automatic upgrade is not supported. To do so, upgrade the control plane first and then the node groups. Node groups are not upgraded automatically together with the cluster, even if you created the cluster and node groups with the same version.

Consider possible downtimes during the upgrade:

* If the control plane is not highly available—that is, it has only one [etcd store](https://docs.nebius.com/kubernetes/components.md#etcd)—the cluster becomes unavailable during the control plane upgrade.
* When you upgrade a node group, the nodes are replaced one by one, according to the node group's [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters). If the maximum unavailable deployment strategy parameter is greater than `0`, some nodes might be unavailable during the upgrade. You can check the node group specifications:

  **CLI**

  ```bash theme={null}
  nebius mk8s node-group get --id <node_group_ID>
  ```

  **Go SDK**

  ```go theme={null}
  nodeGroup, err := sdk.Services().MK8S().V1().
      NodeGroup().Get(
          ctx,
          &mk8s.GetNodeGroupRequest{
              Id: "<node_group_ID>",
          },
      )
  if err != nil {
      return err
  }
  fmt.Println(nodeGroup)
  ```

  **Python SDK**

  ```python theme={null}
  node_group_service = NodeGroupServiceClient(sdk)
  node_group = await node_group_service.get(
      GetNodeGroupRequest(id="<node_group_ID>"),
  )
  print(node_group)
  ```

  **JavaScript SDK**

  ```ts theme={null}
  const nodeGroupService = new NodeGroupService(sdk);
  const nodeGroup = await nodeGroupService.get(
    GetNodeGroupRequest.create({
      id: "<node_group_ID>",
    }),
  );
  console.log(nodeGroup);
  ```

See detailed instructions in [Setting and upgrading Kubernetes® versions in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/manage-versions.md).
