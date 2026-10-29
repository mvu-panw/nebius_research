# Managing maintenance in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/maintenance/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing maintenance in Managed Service for Kubernetes®

[Maintenance in Managed Service for Kubernetes](https://docs.nebius.com/kubernetes/maintenance/index.md) is scheduled automatically when Nebius AI Cloud issues a maintenance event. However, you also have an option to [launch maintenance manually](#how-to-launch-maintenance-manually-in-managed-kubernetes).

You can only do that if a maintenance event is issued for a given node. You can [check the event](#how-to-check-that-a-maintenance-event-is-issued) upfront, before you proceed with the manual maintenance launch.

## How to check that a maintenance event is issued

1. [Connect](https://docs.nebius.com/kubernetes/connect.md) to your Managed Kubernetes cluster.

2. Get the node ID:

   ```bash theme={null}
   kubectl get nodes -o name
   ```

   Output:

   ```text theme={null}
   node/computeinstance-***
   node/computeinstance-***
   ...
   ```

   The node ID is `computeinstance-***`.

3. Check that a maintenance event is issued and the time that it is scheduled for:

   ```bash theme={null}
   kubectl describe node <node_ID> | grep -A 10 "Conditions:"
   ```

   If the event is issued, the command shows the `NebiusMaintenanceScheduled` [Kubernetes condition](https://kubernetes.io/docs/reference/node/node-status/#condition). For example:

   ```text theme={null}
   Conditions:
     Type                         Status   LastHeartbeatTime                 LastTransitionTime                Reason                 Message
     ----                         ------   -----------------                 ------------------                ------                 -------
     NebiusMaintenanceScheduled   True     Wed, 08 Aug 2025 14:28:31 +0200   Wed, 08 Aug 2025 14:28:31 +0200   MaintenanceScheduled   Node scheduled for urgent maintenance, SLA deadline is 2025-08-13T12:26:00Z
     ...
   ```

   In the `Message` column, the command shows the SLA deadline: the latest time the maintenance event should take place.

## How to launch maintenance manually in Managed Kubernetes

1. [Connect](https://docs.nebius.com/kubernetes/connect.md) to your Managed Kubernetes cluster.
2. [Make sure](#how-to-check-that-a-maintenance-event-is-issued) that a maintenance event is issued.
3. Change the maintenance event time:

   ```bash theme={null}
   kubectl label node <node_ID> \
     nebius.com/perform-maintenance=<true|certain_time> \
     --overwrite
   ```

   If you want to start the node drain and the maintenance as soon as possible, set the `true` value for the `nebius.com/perform-maintenance` Kubernetes label.

   Alternatively, you can set a specific time for the maintenance. For a specific time, make sure that the following conditions are met:

   * The time should not be in the past. If you set a time in the past, the `true` value applies instead, and the node drain starts as soon as possible.
   * The time should be at least five minutes earlier than the SLA deadline. Otherwise, the time is ignored, and the `true` value applies.

   Managed Kubernetes supports the following two formats for the time value:

   * Unix time in seconds, for example, `1262304000`.

     This format implies the UTC timezone by default.

   * [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) modified for Kubernetes labels:

     * Use a full stop `.` as a separator, instead of a colon `:`.
     * Use the `_hh.mm` format to specify a UTC+N timezone (for example, `_02.00` for UTC+2).
     * Use the `-hh.mm` format to specify a UTC-N timezone (for example, `-03.00` for UTC-3).

     You may opt not to specify a timezone in the value. In this case, Managed Kubernetes uses the UTC timezone by default.

     Examples of RFC 3339 values:

     | **Time in a given timezone** | **Value** | **Time in UTC** |
     | - | - | - |
     | June 12, 2025, 8:05 UTC-2 | `2025-06-12T08.05.00-02.00` | June 12, 2025, 10:05 UTC, `2025-06-12T10.05.00` |
     | June 12, 2025, 8:05 UTC+2 | `2025-06-12T08.05.00_02.00` | June 12, 2025, 6:05 UTC, `2025-06-12T06.05.00` |

## How to postpone node drain for CPU Pods

For CPU Pods, Managed Kubernetes doesn't wait for the Pods to finish before draining the node. If you want Managed Kubernetes to wait for your CPU Pods, assign the `nebius.com/defer-maintenance-node-drain: "true"` Kubernetes label to the Pods. For more information about how postponing node drain works, see [Postponing node drain](https://docs.nebius.com/kubernetes/maintenance/index.md#postponing-node-drain).

To postpone the node drain for CPU Pods:

1. [Connect](https://docs.nebius.com/kubernetes/connect.md) to your Managed Kubernetes cluster.

2. Add the Kubernetes label to the Pods:

   * To add the label to new Pods when you're creating them, include the label in the configuration:

     ```yaml theme={null}
     template:
       metadata:
         labels:
           app: <app_name>
           nebius.com/defer-maintenance-node-drain: "true"
     ```

   * To apply the label to existing Pods, run:

     ```bash theme={null}
     kubectl label pods -l app=<app_name> \
       nebius.com/defer-maintenance-node-drain=true
     ```

   `app=<app_name>` is used to identify Pods. If they use a different identifying label, use that label in the selector.

3. Check that the label is assigned to the Pods:

   ```bash theme={null}
   kubectl get pods -l app=<app_name> \
     -L nebius.com/defer-maintenance-node-drain
   ```

   This command lists the Pods with `app=<app_name>` and displays `true` for the `nebius.com/defer-maintenance-node-drain` Kubernetes label in an additional column. For example:

   ```text theme={null}
   NAME         READY   STATUS    RESTARTS   AGE     DEFER-MAINTENANCE-NODE-DRAIN
   test-pod     1/1     Running   0          2m17s   true
   ```

   If the label was not added successfully, the last column is empty.
