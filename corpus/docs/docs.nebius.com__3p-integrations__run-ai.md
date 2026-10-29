# Configuring a Managed Service for Kubernetes® cluster to work in Run:ai

Source: https://docs.nebius.com/3p-integrations/run-ai

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuring a Managed Service for Kubernetes® cluster to work in Run:ai

To optimize your ML/AI workloads, you can use the [Run:ai](https://www.run.ai) management platform. It dynamically allocates GPU resources, prevents idle GPUs and enables GPU sharing across multiple workloads and users, so that all resources are utilized. This guide explains how to configure your Nebius AI Cloud resources for use in Run:ai.

## Costs

Nebius AI Cloud charges you for the following billing items:

* [Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/resources/pricing.md).
* [Run:ai infrastructure](https://www.nvidia.com/en-us/software/run-ai/).
* (Optional) [Managed Service for PostgreSQL® cluster](https://docs.nebius.com/postgresql/resources/pricing.md).

## Prerequisites

1. [Get a Run:ai account token](https://docs.run.ai/v2.20/developer/rest-auth/#request-an-api-token).

2. Prepare the environment:

   1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

   2. [Install Terraform](https://developer.hashicorp.com/terraform/install).

   3. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and [Helm](https://helm.sh/docs/intro/install/).

   4. Install [jq](https://jqlang.github.io/jq/), to extract IDs and tokens from the JSON data returned by the Nebius AI Cloud CLI. For more details, see the [jq documentation](https://jqlang.github.io/jq/download/).

      ```bash Ubuntu theme={null}
      sudo apt-get install jq
      ```

      ```bash macOS theme={null}
      brew install jq
      ```

   5. Save the domain name you control to an environment variable:

      ```bash theme={null}
      export DOMAIN_NAME=<example.com>
      ```

## Steps

### Set up a Managed Kubernetes cluster

For this tutorial, a Managed Kubernetes cluster must have:

* A node group with at least three nodes. Each of these nodes must have a public IP address allocated.
* A mounted filesystem.
* NVIDIA® GPU Operator.

To create the necessary resources quickly, use the [k8s-training solution](https://github.com/nebius/nebius-solution-library/tree/main/k8s-training) for Terraform:

1. Clone the [nebius-solution-library](https://github.com/nebius/nebius-solution-library) repository from GitHub and go to the `k8s-training` directory:

   ```bash theme={null}
   git clone https://github.com/nebius/nebius-solution-library.git
   cd nebius-solution-library/k8s-training
   ```

2. Generate an [SSH key pair](https://docs.nebius.com/compute/virtual-machines/ssh-keys.md).

   If you use a custom file name to save the key pair, specify your public key path in [terraform.tfvars](https://github.com/nebius/nebius-solution-library/blob/main/k8s-training/terraform.tfvars#L5).

3. Load the environment variables:

   ```bash theme={null}
   source ./environment.sh
   ```

4. Initialize Terraform to download providers and modules:

   ```bash theme={null}
   terraform init
   ```

5. Set `enable_grafana` and `enable_prometheus` to `false`, `gpu_nodes_assign_public_ip` to `true` and enter your project settings in the `k8s-training/terraform.tfvars` file, or overwrite the values while applying the configuration:

   ```bash theme={null}
   terraform apply -var enable_grafana=false -var enable_prometheus=false \
     -var parent_id=<project_ID> -var subnet_id=<subnet_ID>  \
     -var region=<your_project_region> -var gpu_nodes_assign_public_ip=true
   ```

   The command contains the following parameters:

   * `parent_id`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#terraform-3).
   * `subnet_id`: [Subnet ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-subnet-id).
   * `region`: Project region. Displayed in the list of projects in the web console.

6. When the cluster and the nodes are ready, connect to the cluster:

   ```bash theme={null}
   nebius mk8s cluster get-credentials \
     --id "$(terraform output -json kube_cluster | jq -r '.id')" \
     --external
   kubectl cluster-info
   ```

### Configure KServe

[KServe](https://kserve.github.io/website/latest/) is an open-source framework for serving ML models on Kubernetes. KServe uses [Knative](https://knative.dev/docs/) for serverless deployment and the auto-scaling of ML models.

1. Knative can only run on nodes with public IP addresses. To ensure this, identify nodes without public IPs and cordon them.

   1. Identify nodes:

      ```bash theme={null}
      kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{" - InternalIP: "}{.status.addresses[?(@.type=="InternalIP")].address}{" - ExternalIP: "}{.status.addresses[?(@.type=="ExternalIP")].address}{"\n"}{end}'
      ```

      If you earlier created nodes without public IP addresses, they will have only `InternalIP` in the output.

   2. If the resulting list contains nodes with `InternalIP` only, cordon these nodes:

      ```bash theme={null}
      kubectl cordon <node_without_public_ip>
      ```

2. Install Knative:

   ```bash theme={null}
   kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.14.1/serving-crds.yaml
   kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.14.1/serving-core.yaml

   kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.14.0/kourier.yaml
   kubectl patch configmap/config-network \
     --namespace knative-serving \
     --type merge \
     --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'

   kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.14.1/serving-default-domain.yaml
   kubectl patch configmap/config-features \
     --namespace knative-serving \
     --type merge \
     --patch '{"data":{"kubernetes.podspec-schedulername":"enabled","kubernetes.podspec-affinity":"enabled","kubernetes.podspec-tolerations":"enabled","kubernetes.podspec-volumes-emptydir":"enabled","kubernetes.podspec-securitycontext":"enabled","kubernetes.podspec-persistent-volume-claim":"enabled","kubernetes.podspec-persistent-volume-write":"enabled","multi-container":"enabled","kubernetes.podspec-init-containers":"enabled"}}'
   ```

3. Check the result:

   ```bash theme={null}
   kubectl get jobs -n knative-serving
   kubectl get pods -n kourier-system
   ```

   Make sure that the `default-domain` job reaches the `Complete` status and the `3scale-kourier-gateway` pod is running.

### Install operators

1. Install the [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/trainer/legacy-v1/overview/) (also known as Kubeflow Trainer):

   ```bash theme={null}
   kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"
   kubectl delete customresourcedefinition mpijobs.kubeflow.org
   kubectl patch deployment training-operator -n kubeflow \
     --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args", "value": ["--enable-scheme=tfjob", "--enable-scheme=pytorchjob", "--enable-scheme=xgboostjob", "--enable-scheme=paddlejob"]}]'
   ```

2. Install the [MPI Operator](https://github.com/kubeflow/mpi-operator):

   ```bash theme={null}
   kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/v0.4.0/deploy/v2beta1/mpi-operator.yaml
   ```

### (Optional) Prepare nodes for installing other applications

If you cordoned nodes without public IP addresses during the [KServe installation](#configure-kserve), uncordon them:

```bash theme={null}
kubectl uncordon <node_without_public_ip>
```

### Set up nginx

1. Get the IP addresses of the nodes:

   ```bash theme={null}
   export INTERNAL_IPS=$(kubectl get nodes -o jsonpath='{range .items[*]}{.status.addresses[?(@.type=="InternalIP")].address}{","}{end}' | sed 's/,$//')
   export EXTERNAL_IPS=$(kubectl get nodes -o jsonpath='{range .items[*]}{.status.addresses[?(@.type=="ExternalIP")].address}{","}{end}' | sed 's/,$//')
   export IPS=$(echo "$INTERNAL_IPS,$EXTERNAL_IPS" | sed 's/,,*/,/g' | sed 's/^,//' | sed 's/,$//')
   ```

2. Install nginx:

   ```bash theme={null}
   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo update
   helm upgrade -i nginx-ingress ingress-nginx/ingress-nginx \
     --namespace nginx-ingress --create-namespace \
     --set controller.kind=DaemonSet \
     --set controller.service.externalIPs="{$IPS}"
   ```

3. In your DNS provider, link your domain name (`DOMAIN_NAME`) to the public IP address of one of the nodes.

### Install and configure Prometheus

```bash theme={null}
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack \
    -n monitoring --create-namespace --set grafana.enabled=false
```

### (Optional) Install cert-manager

1. If you don't have public TLS certificates, install cert-manager:

   ```bash theme={null}
   helm repo add jetstack https://charts.jetstack.io
   helm repo update
   helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace \
    --version v1.10.1 --set installCRDs=true \
    --set podDnsConfig.nameservers={"1.1.1.1"}
   ```

2. Create `certs.yaml` with the certificate resources. You will use it later when you [create a TLS secret](#create-resources):

   > **certs.yaml**
   >
   > ```yaml theme={null}
   > apiVersion: cert-manager.io/v1
   > kind: ClusterIssuer
   > metadata:
   >   name: letsencrypt-runai
   > spec:
   >   acme:
   >     server: https://acme-v02.api.letsencrypt.org/directory
   >     email: $EMAIL
   >     privateKeySecretRef:
   >       name: letsencrypt-runai
   >     solvers:
   >         - http01:
   >             ingress:
   >               class: nginx
   > ---
   > apiVersion: cert-manager.io/v1
   > kind: Certificate
   > metadata:
   >   name: runai-tls
   >   namespace: runai-backend
   > spec:
   >   secretName: runai-backend-tls
   >   issuerRef:
   >     name: letsencrypt-runai
   >     kind: ClusterIssuer
   >   commonName: $DOMAIN_NAME
   >   dnsNames:
   >     - $DOMAIN_NAME
   >   usages:
   >     - digital signature
   >     - key encipherment
   >     - server auth
   >   duration: 2160h  # 90 days (default for Let's Encrypt)
   >   renewBefore: 360h # Renew 15 days before expiration
   > ---
   > apiVersion: cert-manager.io/v1
   > kind: Certificate
   > metadata:
   >   name: runai-cluster-domain-tls
   >   namespace: runai
   > spec:
   >   secretName: runai-cluster-domain-tls-secret
   >   issuerRef:
   >     name: letsencrypt-runai
   >     kind: ClusterIssuer
   >   commonName: $DOMAIN_NAME
   >   dnsNames:
   >     - $DOMAIN_NAME
   >     - digital signature
   >     - key encipherment
   >     - server auth
   >   duration: 2160h  # 90 days (Let's Encrypt's default)
   >   renewBefore: 360h  # Renew 15 days before expiration
   > ```

### (Optional) Configure a Managed Service for PostgreSQL cluster

Setting up a Managed Service for PostgreSQL cluster is not strictly necessary for using Run:ai, but it's strongly recommended for production environments.

> [!WARNING]
>
> Create the Managed Service for PostgreSQL cluster in the same region as the [Managed Kubernetes cluster](#set-up-a-managed-kubernetes-cluster). This way they will have network connectivity between them.

1. [Install the postgresql package](https://docs.nebius.com/postgresql/quickstart.md#install-postgresql-package).

2. Create a Managed PostgreSQL cluster:

   ```bash theme={null}
   export PG_PASSWORD="<PostgreSQL_password>"
   nebius msp postgresql v1alpha1 cluster create \
       --name runai-backend-postgres \
       --network-id <network_ID> \
       --backup-backup-window-start "01:00:00" \
       --backup-retention-policy "7d" \
       --bootstrap-user-name "runai" \
       --bootstrap-user-password "$PG_PASSWORD" \
       --bootstrap-db-name "runai" \
       --config-version 16 \
       --config-pooler-config-pooling-mode "session" \
       --config-template-disk-type "network-ssd" \
       --config-template-disk-size-gibibytes 20 \
       --config-template-hosts-count 2 \
       --config-template-resources-platform "cpu-e2" \
       --config-template-resources-preset "4vcpu-16gb" \
       --config-postgresql-config-16-max-connections 320 \
       --config-public-access
   ```

   In this command, specify the [network ID](https://docs.nebius.com/vpc/networking/resources.md#how-to-get-a-network-id).

3. Configure the Managed Service for PostgreSQL cluster to work with Run:ai:

   ```bash theme={null}
   export PG_ENDPOINT=$(nebius msp postgresql v1alpha1 cluster get-by-name --name runai-backend-postgres --format jsonpath='{.status.connection_endpoints.private_read_write}')
   export SQL=$(cat <<EOF
   CREATE ROLE grafana WITH LOGIN PASSWORD '$PG_PASSWORD';
   ALTER USER grafana set search_path='grafana';
   GRANT grafana to runai;
   CREATE SCHEMA grafana authorization grafana;
   EOF
   )
   export PG_CONNECTION_STRING="postgresql://runai:$PG_PASSWORD@$PG_ENDPOINT/runai"
   psql $PG_CONNECTION_STRING -c "$SQL"
   ```

### Create resources

1. Create namespaces:

   ```bash theme={null}
   kubectl create ns runai-backend
   kubectl create ns runai
   ```

2. Use your email and the [token received from Run:ai](#prerequisites) to create a Kubernetes secret with Run:ai credentials:

   ```bash theme={null}
   export TOKEN="<your_run_ai_token>"
   export EMAIL="<your_email>"
   kubectl create secret docker-registry runai-reg-creds \
         --docker-server=https://runai.jfrog.io \
         --docker-username=self-hosted-image-puller-prod \
         --docker-password=$TOKEN \
         --docker-email=$EMAIL \
         --namespace=runai-backend
   ```

3. If you have not created a Managed Service for PostgreSQL cluster in [(Optional) Configure a Managed Service for PostgreSQL cluster](#optional-configure-a-managed-service-for-postgresql-cluster), create a password and save it to the `PG_PASSWORD` environment variable:

   ```bash theme={null}
   export PG_PASSWORD="<PostgreSQL_password>"
   ```

4. Create a Kubernetes secret with Managed Service for PostgreSQL credentials:

   ```bash theme={null}
   kubectl create secret generic postgresql-credentials -n runai-backend \
       --from-literal=postgres-password=$PG_PASSWORD \
       --from-literal=password=$PG_PASSWORD
   kubectl create secret generic grafana-postgresql-credentials -n runai-backend \
       --from-literal=user=grafana \
       --from-literal=password=$PG_PASSWORD
   ```

5. Create a TLS secret:

   **With cert-manager**

   Make sure that you set up `DOMAIN_NAME` and `EMAIL` variables, and run the following set of commands:

   ```bash theme={null}
   envsubst < certs.yaml | kubectl apply -f -

   kubectl wait --for=condition=Ready certificate/runai-tls -n runai-backend --timeout=300s
   ```

   **Without cert-manager**

   To be able to log in, upload your existing certificate:

   ```bash theme={null}
   kubectl create secret tls runai-backend-tls -n runai-backend \
       --cert /path/to/tls.crt --key /path/to/tls.key

   kubectl create secret tls runai-cluster-domain-tls-secret -n runai \
       --cert /path/to/tls.crt --key /path/to/tls.key
   ```

### Install Run:ai

#### Update CoreDNS configuration

Managed Kubernetes uses [Cilium](https://cilium.io/) as it provides eBPF-based networking, load balancing and security policies, and improves overall observability.

However, eBPF-based networking can conflict with [CoreDNS](https://coredns.io/) and cause DNS resolution failures. To ensure proper DNS resolution for Kubernetes services, create and apply a custom ConfigMap:

1. Create a custom ConfigMap `coredns-custom.yaml` that rewrites DNS queries to match your `$DOMAIN_NAME`:

   ```yaml theme={null}
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: coredns-custom
     namespace: kube-system
   data:
     custom.override: |
       rewrite name exact '$DOMAIN_NAME' nginx-ingress-ingress-nginx-controller.nginx-ingress.svc.cluster.local
   ```

2. Make sure that you set up the `DOMAIN_NAME` variable and run the following command:

   ```bash theme={null}
   envsubst < coredns-custom.yaml | kubectl apply -f -
   ```

#### Install control plane

**Without Managed PostgreSQL**

1. Install control plane:

   ```bash theme={null}
   helm repo add runai-backend https://runai.jfrog.io/artifactory/cp-charts-prod
   helm repo update
   helm upgrade -i runai-backend -n runai-backend runai-backend/control-plane \
     --version "~2.18.0" --set global.domain=$DOMAIN_NAME
   ```

2. Wait until all pods are ready. You can check their status by running the following command:

   ```bash theme={null}
   kubectl get pods
   ```

**With Managed PostgreSQL**

1. Install control plane:

   ```bash theme={null}
   helm repo add runai-backend https://runai.jfrog.io/artifactory/cp-charts-prod
   helm repo update
   helm upgrade -i runai-backend -n runai-backend runai-backend/control-plane   --version "~2.18.0" \
     --set global.domain=$DOMAIN_NAME \
     --set postgresql.enabled=false \
     --set global.postgresql.auth.host="$PG_ENDPOINT" \
     --set global.postgresql.auth.database=runai \
     --set global.postgresql.auth.username=runai \
     --set global.postgresql.auth.existingSecret="postgresql-credentials" \
     --set grafana.dbScheme=runai \
     --set grafana.db.existingSecret="grafana-postgresql-credentials"
   ```

2. Wait until all pods are ready. You can check their status by running the following command:

   ```bash theme={null}
   kubectl get pods
   ```

#### Create a Run:ai cluster

1. Go to `DOMAIN_NAME` in your browser.

2. Log in with the default credentials:
   * **Username:** `test@run.ai`
   * **Password:** `Abcd!234`

3. Immediately change the password in the interface.

4. Create a new cluster:
   1. In the interface, select the Run:ai version `2.18` and the **Same as the control plane** cluster location.
   2. Copy the provided command to install the cluster Helm chart.
   3. In your terminal, run the provided command.

You have now deployed Run:ai in the Managed Kubernetes cluster and you can work with it in the Run:ai web interface.

## How to delete the created resources

Some of the created resources are chargeable. If you don't need them, delete these resources, so Nebius AI Cloud doesn't charge for them:

* Delete installed operators:

  ```bash theme={null}
  kubectl delete -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"
  kubectl delete -f "githubusercontent.com/kubeflow/mpi-operator/v0.4.0/deploy/v2beta1/mpi-operator.yaml"
  ```

* Delete the Managed Kubernetes cluster:

  ```bash theme={null}
  terraform destroy -target=nebius_mk8s_v1_cluster.k8s-cluster
  ```

* [Delete the Managed PostgreSQL cluster](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-delete-clusters).

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
