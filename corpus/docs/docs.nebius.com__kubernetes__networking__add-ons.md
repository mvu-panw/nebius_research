# Networking add-ons in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/networking/add-ons

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Networking add-ons in Managed Service for Kubernetes®

Managed Service for Kubernetes clusters have the following networking add-ons installed by default:

* [CoreDNS](https://coredns.io/) is a cluster DNS server.
* [Cilium](https://www.cilium.io/) is a networking solution that provides security and observability.

The add-ons are configured and maintained by Managed Service for Kubernetes, to ensure consistent cluster operation. The configuration of these add-ons is not exposed via API and there are only limited options to customize them:

* For CoreDNS, [use a custom ConfigMap](#coredns).
* For Cilium, [edit the default ConfigMap](#cilium).

Do not use `helm upgrade` to customize, as the changes it makes may be rolled back immediately.

## CoreDNS

**CoreDNS** is a flexible DNS server for Kubernetes clusters. It replaces kube-dns to handle service discovery and name resolution within the cluster.

To view the current CoreDNS configuration, run the following command:

```bash theme={null}
kubectl get configmap -n kube-system coredns -o yaml
```

Do not use `kubectl edit configmap` to make changes to this configuration, because the Managed Service for Kubernetes overwrites the default ConfigMap. Instead, use a custom ConfigMap:

1. Create a custom ConfigMap `coredns-custom.yaml`. It should contain the keys with the `.override` and `.server` extensions.

   * `.override` keys allow you to add plugins to the default [Server Block](https://coredns.io/manual/configuration/#server-blocks) of CoreDNS. You cannot override the parameters already specified in the default ConfigMap.
   * `.server` keys allow you to specify additional Server Blocks for CoreDNS.

   An example of a custom ConfigMap:

   ```yaml theme={null}
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: coredns-custom
     namespace: kube-system
   data:
     log.override: |
       log
     custom.server: |
       example.io:8053 {
         forward . 8.8.8.8
       }
   ```

   This ConfigMap:

* Adds the `log` plug-in to start logging at the system level.
* Creates a new Server Block for the `example.io` domain. All requests directed to `example.io` at port 8053 should be forwarded to another DNS server at `8.8.8.8`.

See the CoreDNS documentation for more information on the [Corefile parameters](https://coredns.io/2017/07/23/corefile-explained/) and the list of [available plug-ins](https://coredns.io/plugins/).

1. Apply the custom configuration:

   ```bash theme={null}
   kubectl apply -f coredns-custom.yaml
   ```

## Cilium

**Cilium** ensures that only specific services and traffic can access certain [Pods](https://docs.nebius.com/kubernetes/components.md#pod). For example:

* Some [Pods](https://docs.nebius.com/kubernetes/components.md#pod) might contain sensitive data, and Cilium enforces rules that only certain internal services or authorized users are allowed to access it.
* If a [node](https://docs.nebius.com/kubernetes/components.md#node) requires restricted access, Cilium ensures that only internal services with proper credentials or traffic with specific labels are allowed.

Also, Cilium provides observability into traffic between [Pods](https://docs.nebius.com/kubernetes/components.md#pod) and [nodes](https://docs.nebius.com/kubernetes/components.md#node), to optimize network paths and enforce network security policies.

To make changes to Cilium configuration, run the following command:

```bash theme={null}
kubectl edit configmap -n kube-system cilium-config
```

> **See more information on ConfigMap parameters**
>
> For more information about available ConfigMap parameters, see the Cilium documentation that matches your cluster's Cilium version:
>
> 1. Get the Cilium version used in your cluster:
>    ```bash theme={null}
>    helm status -n kube-system cilium
>    ```
>
> 2. In the command output, copy the link to the version documentation (remove `/gettinghelp` if present).
>
> 3. Open the following page for your version:
>
>    ```bash theme={null}
>    <docs_link>/network/kubernetes/configuration/#configmap-options
>    ```
>
>    For example, see [https://docs.cilium.io/en/v1.16/network/kubernetes/configuration/#configmap-options](https://docs.cilium.io/en/v1.16/network/kubernetes/configuration/#configmap-options) for Cilium version v1.16.

### Integration with Istio

To make [Istio](https://istio.io/latest/) work with a Cilium-enabled Managed Kubernetes cluster, do the following:

1. [Install Istio](https://istio.io/latest/docs/setup/install/).

2. In the Cilium ConfigMap, set the `bpf-lb-sock-hostns-only` parameter to `true`:

   ```bash theme={null}
   kubectl -n kube-system patch configmap cilium-config \
     --type merge \
     -p='{"data":{"bpf-lb-sock-hostns-only":"true"}}'

   kubectl -n kube-system rollout restart ds/cilium
   ```

3. Wait until all Cilium Pods are restarted.

> **See more information on Istio integration**
>
> For more information on Istio integration, see the Cilium documentation that matches your cluster's Cilium version:
>
> 1. Get the Cilium version used in your cluster:
>
>    ```bash theme={null}
>    helm status -n kube-system cilium
>    ```
>
> 2. In the command output, copy the link to the version documentation (remove `/gettinghelp` if present).
>
> 3. Open the following page for your version:
>
>    ```bash theme={null}
>    <docs_link>/network/servicemesh/istio/
>    ```
>
>    For example, see [https://docs.cilium.io/en/v1.16/network/servicemesh/istio/](https://docs.cilium.io/en/v1.16/network/servicemesh/istio/) for Cilium version v1.16.

### Host firewall

If your Managed Kubernetes cluster was created on or after April 17, 2025, [Cilium's host firewall](https://docs.cilium.io/en/latest/security/host-firewall/) is already enabled on the cluster. You can check the creation dates of your clusters in the [web console](https://console.nebius.com/mk8s).

If your cluster is older, you need to enable the host firewall manually:

1. [Connect to the cluster](https://docs.nebius.com/kubernetes/connect.md).
2. Run the script that enables the host firewall:

   > **enable\_cilium\_host\_firewall.sh**
   >
   > ```bash theme={null}
   > #!/usr/bin/env bash
   >
   > set -euo pipefail
   >
   > # This script ensures that Cilium Host Firewall feature is enabled if all nodes run with the "set-name" feature.
   >
   > kubectl_args=("$@")
   >
   > cluster_name=$(kubectl "${kubectl_args[@]}" config current-context)
   >
   > current_value=$(
   >   kubectl "${kubectl_args[@]}" get configmap cilium-config \
   >     -n kube-system \
   >     -o jsonpath='{.data.enableHostFirewall}' \
   >     2>/dev/null || echo ""
   > )
   >
   > if [[ "$current_value" == "true" ]]; then
   >   echo "Cilium Host Firewall feature is already enabled in cluster \"$cluster_name\". Nothing to do."
   >   exit 0
   > fi
   >
   > echo "Verifying that every node has \"set-name\": \"eth0\" in network-data"
   > for node_ref in $(kubectl "${kubectl_args[@]}" get nodes -o name); do
   >   echo "Inspecting $node_ref"
   >   node_name="${node_ref#node/}"
   >   output=$(
   >     kubectl "${kubectl_args[@]}" debug "$node_ref" \
   >       --profile=general \
   >       --image=busybox \
   >       -i -- \
   >       chroot /host sh -c \
   >         'if grep -q "\"set-name\": \"eth0\"" /var/lib/cloud/instance/network-config.json 2>/dev/null; then
   >            echo OK
   >          else
   >            echo BAD
   >          fi' 2>&1 \
   >       | grep -Eo 'OK|BAD'
   >   )
   >
   >   echo "Cleaning up debug pod"
   >   kubectl "${kubectl_args[@]}" delete $(kubectl "${kubectl_args[@]}" get pod -o name | grep node-debugger-"$node_name") 2>/dev/null
   >
   >   if [[ "$output" != "OK" ]]; then
   >     echo "ERROR: $node_ref does not have \"set-name\": \"eth0\" in network-data."
   >     echo "Ensure that all node groups are upgraded with the following command:"
   >     echo "  nebius mk8s node-group upgrade --latest-infra-version"
   >     exit 1
   >   fi
   > done
   >
   > echo -e "\nAll nodes verified. Enabling Cilium Host Firewall"
   > kubectl "${kubectl_args[@]}" patch configmap cilium-config -n kube-system \
   >   --type=merge \
   >   --patch $'data:\n  enable-host-firewall: "true"'
   >
   > echo "Patched cilium-config ConfigMap; new enable-host-firewall value:"
   > kubectl "${kubectl_args[@]}" get configmap cilium-config -n kube-system \
   >   -o yaml \
   >   | sed -n 's/^[[:space:]]*enable-host-firewall:.*/&/p'
   >
   > echo "Restarting Cilium DaemonSet to pick up the new config"
   > kubectl "${kubectl_args[@]}" -n kube-system rollout restart daemonset cilium
   >
   > echo -e "\nDone"
   > ```

## How the add-ons affect autoscaling node groups

Both CoreDNS and Cilium can run on one node, but it's optimal to run on two. If your cluster has at least one node group with [autoscaling](https://docs.nebius.com/kubernetes/node-groups/autoscaling.md), this node group may scale up just to ensure that there are two nodes to run CoreDNS and Cilium, even if there is no workload.

> [!TIP]
>
> If you have GPU node groups in your cluster, also create a CPU node group with at least two nodes (or with autoscaling). In this case, when there are no tasks to perform, CoreDNS and Cilium can run on CPU nodes, so that the GPU node group can scale down and save you the costs.
