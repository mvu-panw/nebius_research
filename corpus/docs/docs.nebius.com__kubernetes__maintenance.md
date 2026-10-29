# Maintenance in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/maintenance

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Maintenance in Managed Service for Kubernetes®

The goal of the Managed Service for Kubernetes maintenance is to terminate a node as gracefully as possible. When a node termination is required, Nebius AI Cloud issues a maintenance event.

Maintenance events are triggered when software or hardware fails on the physical machines that host your nodes, or when Nebius AI Cloud runs planned maintenance. Software and hardware failures account for the vast majority of maintenance events.

Managed Kubernetes listens to maintenance events that underlying services launch. In particular, as every Kubernetes node represents a Compute virtual machine, Managed Kubernetes tracks [Compute maintenance events](https://docs.nebius.com/compute/virtual-machines/maintenance.md).

## How maintenance occurs

1. Nebius AI Cloud issues a maintenance event.

   When the event is issued, Managed Kubernetes assigns the `NebiusMaintenanceScheduled` [Kubernetes condition](https://kubernetes.io/docs/reference/node/node-status/#condition). You can [check the list of conditions](https://docs.nebius.com/kubernetes/maintenance/manage.md#how-to-check-that-a-maintenance-event-is-issued) to make sure that the service has issued the event.

2. The Managed Kubernetes service detects an event on a node.

   The service groups nodes into batches within a given node group. If a lot of maintenance events are expected in a Managed Kubernetes cluster, batches allow you to avoid stopping all nodes at once.

   The batch size equals either `1` or the value of the [maximum unavailable deployment strategy parameter](https://docs.nebius.com/kubernetes/node-groups/manage.md#node-group-parameters) if that value is greater than `1`. You can check the node group specifications:

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

3. To stop scheduling new Pods, Managed Kubernetes cordons the node.

4. The service waits for running GPU Pods and [labeled CPU Pods](#postponing-node-drain) to finish. If any of these Pods are still running one hour before the SLA deadline, the service stops waiting.

   The *SLA deadline* is the latest time the maintenance event should take place. You can check the SLA deadline [together with Kubernetes conditions](https://docs.nebius.com/kubernetes/maintenance/manage.md#how-to-check-that-a-maintenance-event-is-issued).

5. To remove existing Pods, Managed Kubernetes drains the node. The drain takes up to one hour.

6. Nebius AI Cloud stops the Compute VM (that is, the node).

7. Nebius AI Cloud starts the VM.

8. Managed Kubernetes uncordons the node and enables scheduling new Pods.

9. Managed Kubernetes removes the `NebiusMaintenanceScheduled` condition from the node.

After that, the node is considered to be healthy. Workloads can run on this node again.

## Manual launch of maintenance

The service runs maintenance automatically. However, you can launch it manually as well if a maintenance event is issued for your node. For more information, see [How to launch maintenance manually in Managed Kubernetes](https://docs.nebius.com/kubernetes/maintenance/manage.md#how-to-launch-maintenance-manually-in-managed-kubernetes).

## Postponing node drain

For GPU Pods, Managed Kubernetes waits until the Pods finish or until one hour before the SLA deadline, whichever happens first. Then, the service starts draining the node.

For CPU Pods, Managed Kubernetes doesn't wait for the Pods to finish. If you want Managed Kubernetes to wait for your CPU Pods, assign the `nebius.com/defer-maintenance-node-drain: "true"` Kubernetes label to the CPU Pods.

A continuously running Pod, such as a Pod managed by a DaemonSet, can't postpone the drain past the SLA deadline.

For more information, see [How to postpone node drain for CPU Pods](https://docs.nebius.com/kubernetes/maintenance/manage.md#how-to-postpone-node-drain-for-cpu-pods).
