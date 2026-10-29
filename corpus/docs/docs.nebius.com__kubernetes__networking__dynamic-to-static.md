# How to convert a dynamically assigned public IP address to a reusable allocation

Source: https://docs.nebius.com/kubernetes/networking/dynamic-to-static

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to convert a dynamically assigned public IP address to a reusable allocation

When you [expose a Kubernetes® service](https://docs.nebius.com/kubernetes/clusters/load-balancer.md) in your Managed Service for Kubernetes cluster by using a load balancer, the system automatically creates an allocation with a reserved public IP address and the `nebius.com/managed-by: mk8s` label. However, if the service is deleted, this allocation is also removed by default.

To retain the allocated public IP address and reuse it in future, convert the system-managed allocation into a persistent one and manually link it to your service by using an annotation.

## Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has at least the `editor` role within your tenant or project; for example, the default `editors` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

2. Install [jq](https://jqlang.github.io/jq/) to extract IDs and tokens from the JSON data returned by the Nebius AI Cloud CLI:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

3. [Create a Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/quickstart.md#create-a-cluster-and-a-node-group) if you have not done it before.

4. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [connect to the cluster](https://docs.nebius.com/kubernetes/quickstart.md#connect-to-the-cluster).

## How to convert a dynamic IP address

1. Get the public IP address of your load balancer:

   ```bash theme={null}
   kubectl get svc nginx
   ```

   Copy the IP address from the `EXTERNAL-IP` column.

2. Get the ID of the allocation associated with the IP address:

   ```bash theme={null}
   nebius vpc allocation list --format json | jq -r '
     .items[]
     | select(
         .status.details.allocated_cidr == "<external_IP>/32"
         and .metadata.labels["nebius.com/managed-by"] == "mk8s"
       )
     | .metadata.id'
   ```

   Specify the IP address that you copied in the previous step.

   Alternatively, list all allocations by using the [nebius vpc allocation list](https://docs.nebius.com/cli/reference/vpc/allocation/list.md) command. In the output, look for a block that contains the matching IP address under `status.details.allocated_cidr` and a `labels` field containing `nebius.com/managed-by: mk8s`.

   Copy the allocation ID. It has the `vpcallocation-***` format.

3. To detach the allocation from automatic deletion, remove system-managed labels of this allocation:

   1. Open the editor to edit the allocation:

      ```bash theme={null}
      nebius vpc allocation edit <allocation_ID>
      ```

      Specify the ID that you copied in the previous step. For details on using the `edit` command, see [How to edit resources via the Nebius AI Cloud CLI](https://docs.nebius.com/cli/edit.md).

   2. In the editor, delete all labels from the `labels` list:

      ```yaml theme={null}
      ...
      labels: {}
      ...
      ```

   3. Save the changes and close the editor.

   Now, the allocation is user-managed, so it will remain even if the associated service is deleted.

4. Update your Kubernetes load balancer manifest (for example, [service.yaml](https://docs.nebius.com/kubernetes/clusters/load-balancer.md#how-to-set-up-a-load-balancer)) with the following annotation:

   ```yaml theme={null}
   metadata:
     annotations:
       nebius.com/load-balancer-allocation-id: <allocation_ID>
   ```

5. Apply the updated manifest:

   ```bash theme={null}
   kubectl apply -f service.yaml
   ```

Now, the public IP allocation is preserved and can be reused if you re-create the service or replace it with another one.

For more information, see [Load balancers types](https://docs.nebius.com/kubernetes/clusters/load-balancer.md#load-balancers-types).
