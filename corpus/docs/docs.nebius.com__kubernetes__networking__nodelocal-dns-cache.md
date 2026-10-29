# Setting up NodeLocal DNSCache with Cilium network policy controller in Managed Service for Kubernetes®

Source: https://docs.nebius.com/kubernetes/networking/nodelocal-dns-cache

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Setting up NodeLocal DNSCache with Cilium network policy controller in Managed Service for Kubernetes®

To improve the DNS performance in a Managed Service for Kubernetes cluster, you can use the [NodeLocal DNSCache](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) feature. With this feature, a DNS caching agent runs on each cluster node to resolve DNS requests locally on the same nodes as the Pods.

In this tutorial, you will learn to configure a NodeLocal DNSCache for the [Cilium network policy controller](https://docs.cilium.io/en/stable/) by using [local redirect policy](https://docs.cilium.io/en/stable/network/kubernetes/local-redirect-policy/).

## Costs

Nebius AI Cloud charges you only for running a Managed Kubernetes cluster. For more details, see the [Managed Kubernetes pricing](https://docs.nebius.com/kubernetes/resources/pricing.md).

## Prerequisites

* [Create a Managed Service for Kubernetes cluster](https://docs.nebius.com/kubernetes/quickstart.md#create-a-cluster-and-a-node-group) if you have not done it before.
* [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [connect to the cluster](https://docs.nebius.com/kubernetes/quickstart.md#connect-to-the-cluster).

## Steps

### Prepare manifests for NodeLocal DNSCache and local redirect policy

1. Retrieve the service IP address for `coredns`:

   ```bash theme={null}
   kubectl get svc coredns -n kube-system -o jsonpath={.spec.clusterIP}
   ```

2. Create a manifest file named `node-local-dns.yaml`. In the `DaemonSet` specification (`spec.template.spec.containers.args`), replace the coredns\_IP\_address with the IP address of the `coredns` service you obtained in the previous step.

   > **node-local-dns.yaml**
   >
   > ```yaml theme={null}
   > ---
   > apiVersion: v1
   > kind: ServiceAccount
   > metadata:
   >   name: node-local-dns
   >   namespace: kube-system
   > ---
   > apiVersion: v1
   > kind: Service
   > metadata:
   >   name: node-local-dns-upstream
   >   namespace: kube-system
   >   labels:
   >     k8s-app: node-local-dns-upstream
   >     kubernetes.io/name: "NodeLocalDnsUpstream"
   >     kubernetes.io/cluster-service: "true"
   > spec:
   >   ports:
   >   - name: dns
   >     port: 53
   >     protocol: UDP
   >     targetPort: 53
   >   - name: dns-tcp
   >     port: 53
   >     protocol: TCP
   >     targetPort: 53
   >   selector:
   >     k8s-app: coredns
   > ---
   > apiVersion: v1
   > kind: ConfigMap
   > metadata:
   >   name: node-local-dns
   >   namespace: kube-system
   > data:
   >   Corefile: |
   >     cluster.local:53 {
   >       errors
   >       cache {
   >         success 9984 30
   >         denial 9984 5
   >       }
   >       reload
   >       loop
   >       bind 0.0.0.0
   >       forward . __PILLAR__CLUSTER__DNS__ {
   >         prefer_udp
   >       }
   >       prometheus :9253
   >       health
   >     }
   >     in-addr.arpa:53 {
   >       errors
   >       cache 30
   >       reload
   >       loop
   >       bind 0.0.0.0
   >       forward . __PILLAR__CLUSTER__DNS__ {
   >         prefer_udp
   >       }
   >       prometheus :9253
   >     }
   >     ip6.arpa:53 {
   >       errors
   >       cache 30
   >       reload
   >       loop
   >       bind 0.0.0.0
   >       forward . __PILLAR__CLUSTER__DNS__ {
   >         prefer_udp
   >       }
   >       prometheus :9253
   >     }
   >     .:53 {
   >       errors
   >       cache 30
   >       reload
   >       loop
   >       bind 0.0.0.0
   >       forward . __PILLAR__CLUSTER__DNS {
   >         prefer_udp
   >       }
   >       prometheus :9253
   >     }
   > ---
   > apiVersion: apps/v1
   > kind: DaemonSet
   > metadata:
   >   name: node-local-dns
   >   namespace: kube-system
   >   labels:
   >     k8s-app: node-local-dns
   > spec:
   >   updateStrategy:
   >     rollingUpdate:
   >       maxUnavailable: 10%
   >   selector:
   >     matchLabels:
   >       k8s-app: node-local-dns
   >   template:
   >     metadata:
   >       labels:
   >         k8s-app: node-local-dns
   >       annotations:
   >         prometheus.io/port: "9253"
   >         prometheus.io/scrape: "true"
   >     spec:
   >       priorityClassName: system-node-critical
   >       serviceAccountName: node-local-dns
   >       dnsPolicy: Default # Don't use cluster DNS.
   >       tolerations:
   >       - key: "CriticalAddonsOnly"
   >         operator: "Exists"
   >       - effect: "NoExecute"
   >         operator: "Exists"
   >       - effect: "NoSchedule"
   >         operator: "Exists"
   >       containers:
   >       - name: node-cache
   >         image: registry.k8s.io/dns/k8s-dns-node-cache:1.24.0
   >         resources:
   >           requests:
   >             cpu: 25m
   >             memory: 5Mi
   >         args: [ "-localip", "coredns_IP_address",
   >                 "-conf", "/etc/Corefile",
   >                 "-upstreamsvc", "node-local-dns-upstream",
   >                 "-skipteardown=true",
   >                 "-setupinterface=false",
   >                 "-setupiptables=false" ]
   >         securityContext:
   >           privileged: true
   >         ports:
   >         - containerPort: 53
   >           name: dns
   >           protocol: UDP
   >         - containerPort: 53
   >           name: dns-tcp
   >           protocol: TCP
   >         - containerPort: 9253
   >           name: metrics
   >           protocol: TCP
   >         livenessProbe:
   >           httpGet:
   >             path: /health
   >             port: 8080
   >           initialDelaySeconds: 60
   >           timeoutSeconds: 5
   >         volumeMounts:
   >         - mountPath: /run/xtables.lock
   >           name: xtables-lock
   >           readOnly: false
   >         - name: config-volume
   >           mountPath: /etc/coredns
   >         - name: kube-dns-config
   >           mountPath: /etc/kube-dns
   >       volumes:
   >       - name: xtables-lock
   >         hostPath:
   >           path: /run/xtables.lock
   >           type: FileOrCreate
   >       - name: kube-dns-config
   >         configMap:
   >           name: kube-dns
   >           optional: true
   >       - name: config-volume
   >         configMap:
   >           name: node-local-dns
   >           items:
   >             - key: Corefile
   >               path: Corefile.base
   > ```

   This manifest declares a DaemonSet for NodeLocal DNSCache and a service account, service and ConfigMap needed for its operation.

3. Create a manifest file named `node-local-dns-lrp.yaml`.

   > **node-local-dns-lrp.yaml**
   >
   > ```yaml theme={null}
   > ---
   > apiVersion: "cilium.io/v2"
   > kind: CiliumLocalRedirectPolicy
   > metadata:
   >   name: "node-local-dns"
   >   namespace: kube-system
   > spec:
   >   redirectFrontend:
   >     serviceMatcher:
   >       serviceName: coredns
   >       namespace: kube-system
   >       toPorts:
   >         - port: "53"
   >           name: dns
   >           protocol: UDP
   >         - port: "53"
   >           name: dns-tcp
   >           protocol: TCP
   >   redirectBackend:
   >     localEndpointSelector:
   >       matchLabels:
   >         k8s-app: node-local-dns
   >     toPorts:
   >       - port: "53"
   >         name: dns
   >         protocol: UDP
   >       - port: "53"
   >         name: dns-tcp
   >         protocol: TCP
   > ```

   This manifest declares a local redirect policy that directs DNS requests at the `node-local-dns` DaemonSet for resolution.

### Apply the manifests and create resources

1. Create resources for NodeLocal DNSCache:

   ```bash theme={null}
   kubectl apply -f node-local-dns.yaml
   ```

2. Create the local redirect policy:

   ```bash theme={null}
   kubectl apply -f node-local-dns-lrp.yaml
   ```

### Test NodeLocal DNSCache

#### Create a test environment

1. Create a manifest file named `dnsutils.yaml`.

   > **dnsutils.yaml**
   >
   > ```yaml theme={null}
   > ---
   > apiVersion: v1
   > kind: Pod
   > metadata:
   >   name: dnsutils
   >   namespace: default
   > spec:
   >   containers:
   >   - name: dnsutils
   >     image: registry.k8s.io/e2e-test-images/agnhost:2.9
   >     imagePullPolicy: IfNotPresent
   >   restartPolicy: Always
   > ```

2. Launch the `dnsutils` Pod:

   ```bash theme={null}
   kubectl apply -f dnsutils.yaml
   ```

3. Find out which node is running the `dnsutils` Pod:

   ```bash theme={null}
   kubectl get pod dnsutils -o wide
   ```

   The result looks like the following:

   ```bash theme={null}
   NAME       READY   STATUS    RESTARTS   AGE   IP             NODE                                 NOMINATED NODE   READINESS GATES
   dnsutils   1/1     Running   0          16s   10.57.100.14   computeinstance-xxxxxxxxx   <none>           <none>
   ```

   Once the Pod status is `Running`, get the ID of the node from the `NODE` column.

4. Use the ID of the node to find out the IP address of the Pod that runs NodeLocal DNSCache on this node:

   ```bash theme={null}
   export POD_IP_ADDRESS=$(kubectl get pod -o wide -n kube-system | grep 'node-local.*<computeinstance_node_id>' | awk '{print $6}')
   ```

#### Run tests

1. Get the values of the metrics for DNS requests before testing:

   ```bash theme={null}
   kubectl exec -ti dnsutils -- curl http://$POD_IP_ADDRESS:9253/metrics | grep coredns_dns_requests_total
   ```

   The result looks like the following:

   ```bash theme={null}
   # HELP coredns_dns_requests_total Counter of DNS requests made per zone, protocol and family.
   # TYPE coredns_dns_requests_total counter
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="cluster.local."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="in-addr.arpa."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="ip6.arpa."} 1
   ```

2. Run several DNS requests:

   ```bash theme={null}
   kubectl exec -ti dnsutils -- nslookup kubernetes &&
   kubectl exec -ti dnsutils -- nslookup kubernetes.default &&
   kubectl exec -ti dnsutils -- nslookup nebius.com
   ```

3. Now check the metrics again:

   ```bash theme={null}
   kubectl exec -ti dnsutils -- curl http://$POD_IP_ADDRESS:9253/metrics | grep coredns_dns_requests_total
   ```

   The values of the metrics should increase, for example:

   ```bash theme={null}
   # HELP coredns_dns_requests_total Counter of DNS requests made per zone, protocol and family.
   # TYPE coredns_dns_requests_total counter
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="A",view="",zone="."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="A",view="",zone="cluster.local."} 6
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="AAAA",view="",zone="."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="AAAA",view="",zone="cluster.local."} 2
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="cluster.local."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="in-addr.arpa."} 1
   coredns_dns_requests_total{family="1",proto="udp",server="dns://0.0.0.0:53",type="other",view="",zone="ip6.arpa."} 1
   ```

   If the tests don't show the expected metrics increase, there may be an error in your configuration.

#### Troubleshoot issues and inspect logs

* Check that the local redirect policy is enabled in the Cilium configuration:

  ```bash theme={null}
  kubectl get configmap cilium-config -n kube-system -o yaml | grep redirect
  ```

  The expected result is:

  ```bash theme={null}
  enable-local-redirect-policy: "true"
  ```

* Check that the `node-local-dns` local redirect policy declared [earlier](#prepare-manifests-for-nodelocal-dnscache-and-local-redirect-policy) is properly applied:

  ```bash theme={null}
  kubectl get ciliumlocalredirectpolicies -A
  ```

  The expected result is something like the following:

  ```bash theme={null}
  NAMESPACE     NAME           AGE
  kube-system   node-local-dns   3h18m
  ```

* Check the local redirect policy rules on any of the Cilium Pods:

  * Get the list of Cilium Pods:

    ```bash theme={null}
    kubectl -n kube-system get pod | grep '^cilium-[^o]'
    ```

  * Get the local redirect policy rules on one of these Pods:

    ```bash theme={null}
    kubectl exec -it <cilium-xxxxx> -n kube-system -- cilium-dbg lrp list
    ```

    The expected result is something like the following:

    ```bash theme={null}
    LRP namespace   LRP name       FrontendType              Matching Service
    kube-system     nodelocaldns   clusterIP + named ports   kube-system/coredns
                    |              coredns_IP_address:53/UDP -> 10.57.43.185:53(kube-system/node-local-dns-2cdjt),
                    |              coredns_IP_address:53/TCP -> 10.57.43.185:53(kube-system/node-local-dns-2cdjt),
    ```

* Check the contents of the `resolv.conf` file in the `dnsutils` Pod:

  ```bash theme={null}
  kubectl exec -ti dnsutils -- cat /etc/resolv.conf
  ```

  The expected result is something like the following:

  ```bash theme={null}
  search default.svc.cluster.local svc.cluster.local cluster.local
  nameserver coredns_IP_address
  options ndots:5
  ```

* Check DNS logs.

  To enable logs for Pods running DNS services, create a custom ConfigMap `coredns-custom.yaml` that contains a `log.override` key:

  ```yaml theme={null}
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: coredns-custom
    namespace: kube-system
  data:
    log.override: |
      log
  ```

  Apply the custom ConfigMap:

  ```bash theme={null}
  kubectl apply -f coredns-custom.yaml
  ```

  To enable logs for the `node-local-dns` service, edit the ConfigMap:

  ```bash theme={null}
  kubectl -n kube-system edit configmap node-local-dns
  ```

  Add the `log` config parameter within the `Corefile` section:

  ```bash theme={null}
      .:53 {
        log
        errors
  ```

  Now you can get the logs of the Pods running DNS services:

  ```bash theme={null}
  kubectl logs --namespace=kube-system -l k8s-app=coredns -f
  kubectl logs --namespace=kube-system -l k8s-app=node-local-dns -f
  ```

#### Delete testing resources

Delete the `dnsutils` Pod:

```bash theme={null}
kubectl delete -f dnsutils.yaml
```

## How to disable NodeLocal DNSCache

If you no longer want to use NodeLocal DNSCache in your cluster, you can disable it:

1. Delete the local redirect policy:

   ```bash theme={null}
   kubectl delete -f node-local-dns-lrp.yaml
   ```

2. Delete the resources you created for NodeLocal DNSCache:

   ```bash theme={null}
   kubectl delete -f node-local-dns.yaml
   ```

## How to delete the created resources\\

The Managed Kubernetes cluster you used in this tutorial is chargeable. If you do not need it, [delete this resource](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-delete-clusters), so Nebius AI Cloud does not charge for it.
