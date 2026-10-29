# Syncing SecretStash secrets with Managed Service for Kubernetes® clusters by using External Secrets Operator

Source: https://docs.nebius.com/mysterybox/kubernetes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Syncing SecretStash secrets with Managed Service for Kubernetes® clusters by using External Secrets Operator

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

Applications in a Managed Service for Kubernetes cluster often read credentials, such as API keys or passwords, from Kubernetes Secrets. Instead of creating these Secrets manually or storing their values in manifests and CI/CD pipelines, you can keep the values in SecretStash and sync them with the cluster by using [External Secrets Operator](https://external-secrets.io/latest/provider/nebius-mysterybox/) (ESO). ESO reads a SecretStash secret, writes its payload to a Kubernetes Secret and updates it when you add a new [primary version](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions) in SecretStash.

In this tutorial, you will grant a service account access to a secret, install ESO, set up authentication for ESO and sync the secret with your cluster.

## Costs

Nebius AI Cloud only charges for running a Managed Kubernetes cluster. For more details, see [Managed Kubernetes pricing](https://docs.nebius.com/kubernetes/resources/pricing.md) and [SecretStash pricing](https://docs.nebius.com/mysterybox/resources/pricing.md).

## Prerequisites

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Check that your project ID is saved in the Nebius AI Cloud CLI profile configuration:
   ```bash theme={null}
   cat ~/.nebius/config.yaml
   ```
3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
4. [Create a Managed Kubernetes cluster](https://docs.nebius.com/kubernetes/clusters/manage.md) with at least one node group and [connect to it using kubectl](https://docs.nebius.com/kubernetes/connect.md).
5. [Install Helm](https://helm.sh/docs/intro/install/).
6. [Create a secret](https://docs.nebius.com/mysterybox/secrets/create.md) in SecretStash. The examples use a secret with the `password` key.

## Steps

Run all commands in the same terminal session. Some commands save values, such as resource IDs, to environment variables. The `kubectl` commands that you run later read these variables and pass their values to the Kubernetes manifests, so you don't need to copy the values manually.

### Grant a Nebius AI Cloud service account access to the secret

ESO reads the secret on behalf of a Nebius AI Cloud service account. This service account needs the `mysterybox.payload-viewer` role for the secret.

> [!WARNING]
>
> Creating a secret or a version of a secret does not automatically grant you access to view payloads in that secret or version. The `editor` role is enough to create a secret or a version, but viewing payloads requires the `mysterybox.payload-viewer` role, which is a sub-role of `admin` but not `editor`.

1. Get the ID of the secret and save it to an environment variable:

   ```bash theme={null}
   export SECRET_ID=$(nebius mysterybox secret get-by-name \
     --parent-id <project_ID> \
     --name <secret_name> \
     --format jsonpath='{.metadata.id}')
   ```

   Make sure that the variable isn't empty: run `echo $SECRET_ID`. If the output is empty, check the secret name and the project ID.

2. Create a service account and save its ID to an environment variable:

   ```bash theme={null}
   export SA_ID=$(nebius iam service-account create \
     --name <service_account_name> \
     --format jsonpath='{.metadata.id}')
   ```

3. Create a [custom group](https://docs.nebius.com/iam/authorization/groups.md#custom-groups) for the service account and save the group ID to an environment variable:

   ```bash theme={null}
   export GROUP_ID=$(nebius iam group create \
     --parent-id <project_ID> \
     --name <group_name> \
     --format jsonpath='{.metadata.id}')
   ```

4. Grant the `mysterybox.payload-viewer` role for the secret to the group:

   ```bash theme={null}
   nebius iam access-permit create \
     --parent-id $GROUP_ID \
     --resource-id $SECRET_ID \
     --role mysterybox.payload-viewer
   ```

   To grant access to all secrets in the project, specify the project ID in `--resource-id` instead of the secret ID.

5. Add the service account to the group:

   ```bash theme={null}
   nebius iam group-membership create \
     --parent-id $GROUP_ID \
     --member-id $SA_ID
   ```

### Install ESO

1. Add the ESO Helm repository:

   ```bash theme={null}
   helm repo add external-secrets https://charts.external-secrets.io
   helm repo update
   ```

2. Install ESO 2.10.0 or later with its custom resource definitions:

   ```bash theme={null}
   helm install external-secrets external-secrets/external-secrets \
     --namespace external-secrets --create-namespace \
     --version ">=2.10.0" \
     --set installCRDs=true
   ```

3. Make sure that the ESO Pods are running:

   ```bash theme={null}
   kubectl get pods -n external-secrets
   ```

   All Pods should have the `Running` status.

### Create a namespace

1. Specify a name for the namespace and save it to an environment variable:

   ```bash theme={null}
   export K8S_NAMESPACE=<namespace>
   ```

   The `kubectl` commands that you run later create the Kubernetes resources in this namespace, including the Kubernetes Secret with the synced values. Pods can only use Secrets from their own namespace. If the workloads that need the secret already run in a namespace, specify its name and skip the next step.

2. Create the namespace:

   ```bash theme={null}
   kubectl create namespace $K8S_NAMESPACE
   ```

### Set up authentication and connect ESO to SecretStash

ESO can authenticate in SecretStash using one of the following methods:

* *Workload identity federation* (recommended): ESO exchanges a short-lived token of a Kubernetes ServiceAccount for an [access token](https://docs.nebius.com/iam/authorization/access-tokens.md) of the Nebius AI Cloud service account. You don't need to store long-lived credentials in the cluster.
* Service account credentials: ESO uses an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) of the Nebius AI Cloud service account. You store the key in a Kubernetes Secret.

For either method, you create a *SecretStore*: a Kubernetes [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) that ESO adds to your cluster. A SecretStore tells ESO how to authenticate in SecretStash. For more details, see the [ESO documentation](https://external-secrets.io/latest/api/secretstore/).

Set up one of the authentication methods and create a SecretStore for it:

**Workload identity (recommended)**

1. Create the `mysterybox-reader` ServiceAccount together with a Role and a RoleBinding. ESO requests tokens for this ServiceAccount through the Kubernetes TokenRequest API, and the Role and RoleBinding allow this:

   ```bash theme={null}
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: mysterybox-reader
     namespace: $K8S_NAMESPACE
   ---
   # Allows creating tokens for the mysterybox-reader ServiceAccount
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     name: external-secrets-token-request
     namespace: $K8S_NAMESPACE
   rules:
     - apiGroups: [""]
       resources: ["serviceaccounts/token"]
       resourceNames: ["mysterybox-reader"]
       verbs: ["create"]
   ---
   # Grants the Role to the ESO controller
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: allow-eso-to-request-token
     namespace: $K8S_NAMESPACE
   subjects:
     - kind: ServiceAccount
       name: external-secrets
       namespace: external-secrets
   roleRef:
     kind: Role
     name: external-secrets-token-request
     apiGroup: rbac.authorization.k8s.io
   EOF
   ```

   In the RoleBinding, `external-secrets` is the name and namespace of the ESO controller's ServiceAccount when you install ESO as shown above.

   If you installed ESO with a different Helm release name or namespace, get the ServiceAccount name by running `kubectl get serviceaccounts -n <ESO_namespace>`.

2. Get the ID of your Managed Kubernetes cluster:

   ```bash theme={null}
   nebius mk8s cluster get-by-name \
     --name <cluster_name> \
     --format jsonpath='{.metadata.id}'
   ```

3. Create *federated credentials*. They let a workload outside Nebius AI Cloud, here the `mysterybox-reader` ServiceAccount in your cluster, get access tokens of a Nebius AI Cloud service account. To create them, run the following command:

   ```bash theme={null}
   nebius iam federated-credentials create \
     --parent-id <project_ID> \
     --name <federated_credentials_name> \
     --subject-id $SA_ID \
     --oidc-provider-issuer-url https://oidc.mk8s.api.nebius.cloud/<cluster_ID> \
     --federated-subject-id system:serviceaccount:$K8S_NAMESPACE:mysterybox-reader
   ```

   The command contains the following parameters:

   * `--parent-id`: ID of the project.
   * `--subject-id`: ID of the Nebius AI Cloud service account whose access tokens the ServiceAccount gets. The command takes the ID from the `SA_ID` variable.
   * `--oidc-provider-issuer-url`: URL of the cluster's OpenID Connect (OIDC) issuer. Replace `<cluster_ID>` with the ID that you got in the previous step. For more details, see [Using an OIDC public endpoint in Managed Kubernetes clusters](https://docs.nebius.com/kubernetes/networking/oidc-public-endpoint.md).
   * `--federated-subject-id`: Kubernetes ServiceAccount in the `system:serviceaccount:<namespace>:<ServiceAccount_name>` format. The command uses the `mysterybox-reader` ServiceAccount in the namespace from the `K8S_NAMESPACE` variable.

   Nebius AI Cloud then accepts the tokens that your cluster issues for this ServiceAccount and exchanges them for access tokens of the service account.

4. Create the SecretStore. The command passes the service account ID from the `SA_ID` variable to `iamServiceAccountID`:

   ```bash theme={null}
   kubectl apply -f - <<EOF
   apiVersion: external-secrets.io/v1
   kind: SecretStore
   metadata:
     name: mysterybox
     namespace: $K8S_NAMESPACE
   spec:
     provider:
       nebiusmysterybox:
         apiDomain: api.nebius.cloud:443
         auth:
           workloadIdentity:
             serviceAccountRef:
               name: mysterybox-reader
             iamServiceAccountID: $SA_ID
   EOF
   ```

5. Make sure that the SecretStore is valid:

   ```bash theme={null}
   kubectl get secretstore mysterybox -n $K8S_NAMESPACE
   ```

   In the output, the `STATUS` column should show `Valid`. To validate the SecretStore, ESO gets an access token for the service account, so this status also confirms that the federated credentials and the RoleBinding work. Don't proceed until the SecretStore has the `Valid` status. If it doesn't, see [Troubleshooting](#troubleshooting).

**Service account credentials**

> [!WARNING]
>
> Don't generate the credentials file or create the Kubernetes Secret with the credentials by using Terraform: Terraform saves the private key of the service account in its state, and anyone who can read the state can use the key to act as the service account.

For more details, see the [Terraform documentation](https://developer.hashicorp.com/terraform/language/state/sensitive-data).

1. Generate an authorized key for the service account and save the credentials to a file:

   ```bash theme={null}
   nebius iam auth-public-key generate \
     --service-account-id $SA_ID \
     --output ~/.nebius/$SA_ID-credentials.json
   ```

   The command creates a key pair, uploads the public key to the service account and writes the credentials, including the private key, to the output file. To limit how long the key remains valid, add the `--expires-at` parameter with the expiration time in RFC 3339 format, for example, `--expires-at 2027-01-31T23:59:59Z`. For more details, see [How to use authorized keys](https://docs.nebius.com/iam/service-accounts/authorized-keys.md).

   If a credentials file with this name already exists, delete it before you run the command. The command doesn't fully overwrite an existing file, and ESO rejects the result with the `invalid subject credentials: malformed JSON` error.

2. Store the credentials in a Kubernetes Secret:

   ```bash theme={null}
   kubectl create secret generic mysterybox-sa-credentials \
     -n $K8S_NAMESPACE \
     --from-file=credentials.json=$HOME/.nebius/$SA_ID-credentials.json
   ```

3. Create the SecretStore. The command refers to the Kubernetes Secret that you created in the previous step:

   ```bash theme={null}
   kubectl apply -f - <<EOF
   apiVersion: external-secrets.io/v1
   kind: SecretStore
   metadata:
     name: mysterybox
     namespace: $K8S_NAMESPACE
   spec:
     provider:
       nebiusmysterybox:
         apiDomain: api.nebius.cloud:443
         auth:
           serviceAccountCredsSecretRef:
             name: mysterybox-sa-credentials
             key: credentials.json
   EOF
   ```

4. Make sure that the SecretStore is valid:

   ```bash theme={null}
   kubectl get secretstore mysterybox -n $K8S_NAMESPACE
   ```

   In the output, the `STATUS` column should show `Valid`. To validate the SecretStore, ESO gets an access token for the service account, so this status also confirms that the authorized key in the Kubernetes Secret works. Don't proceed until the SecretStore has the `Valid` status. If it doesn't, see [Troubleshooting](#troubleshooting).

### Sync the secret with the cluster

An *ExternalSecret* is another ESO custom resource. It tells ESO which SecretStash secret to read and which Kubernetes Secret to write it to. For more details, see the [ESO documentation](https://external-secrets.io/latest/api/externalsecret/).

1. Create the ExternalSecret. The command passes the secret ID from the `SECRET_ID` variable to `key`:

   ```bash theme={null}
   kubectl apply -f - <<EOF
   apiVersion: external-secrets.io/v1
   kind: ExternalSecret
   metadata:
     name: app-credentials
     namespace: $K8S_NAMESPACE
   spec:
     # How often ESO checks the secret for changes
     refreshInterval: 1h
     secretStoreRef:
       kind: SecretStore
       name: mysterybox
     target:
       # Name of the Kubernetes Secret that ESO creates
       name: app-credentials
       creationPolicy: Owner
     dataFrom:
       - extract:
           key: $SECRET_ID
   EOF
   ```

   With `dataFrom.extract`, every key of the secret payload becomes a key in the Kubernetes Secret. To sync only some keys, replace `dataFrom` with `data` and add an entry with `property` for each key:

   ```yaml theme={null}
     data:
       - secretKey: password # Key in the Kubernetes Secret
         remoteRef:
           key: $SECRET_ID
           property: password # Key in the secret payload
   ```

   If you don't specify `property`, ESO writes the whole payload as JSON to the Kubernetes Secret key.

2. Make sure that ESO has synced the secret:

   ```bash theme={null}
   kubectl get externalsecret app-credentials -n $K8S_NAMESPACE
   ```

   The result looks like the following:

   ```text theme={null}
   NAME              STORETYPE     STORE        REFRESH INTERVAL   STATUS         READY   LAST SYNC
   app-credentials   SecretStore   mysterybox   1h                 SecretSynced   True    5s
   ```

   If the status isn't `SecretSynced`, see [Troubleshooting](#troubleshooting).

3. Check the keys of the Kubernetes Secret:

   ```bash theme={null}
   kubectl get secret app-credentials -n $K8S_NAMESPACE -o jsonpath='{.data}'
   ```

   The output contains the keys of the secret payload with base64-encoded values.

Your workloads can now use the `app-credentials` Kubernetes Secret, for example, as environment variables or a mounted volume.

By default, ESO syncs the primary version of the secret. When you [make another version primary](https://docs.nebius.com/mysterybox/secrets/make-version-primary.md), ESO updates the Kubernetes Secret within the interval set in `refreshInterval`.

To sync a specific version instead, add `version: <version_ID>` under `remoteRef` or `extract`. To get the version ID, [list the versions of the secret](https://docs.nebius.com/mysterybox/secrets/get.md#how-to-get-a-list-of-versions). For example, to pin the version in the ExternalSecret that you created:

```yaml theme={null}
  dataFrom:
    - extract:
        key: $SECRET_ID
        version: <version_ID>
```

If you sync only some keys, add `version` to each entry:

```yaml theme={null}
  data:
    - secretKey: password
      remoteRef:
        key: $SECRET_ID
        property: password
        version: <version_ID>
```

When a version is pinned, ESO doesn't pick up a new primary version until you change `version` in the ExternalSecret and apply it again.

## Troubleshooting

If the ExternalSecret doesn't have the `SecretSynced` status, get the details of the error:

```bash theme={null}
kubectl describe externalsecret app-credentials -n $K8S_NAMESPACE
```

Check the `Events` section of the output and the following possible causes:

* **Nothing is reconciled:** Make sure that the ESO Pods are running and the ESO custom resource definitions are installed:

  ```bash theme={null}
  kubectl get pods -n external-secrets
  kubectl get crds | grep external-secrets.io
  ```

* **The SecretStore isn't found:** Make sure that the SecretStore and the ExternalSecret are in the same namespace and that `secretStoreRef.name` matches the SecretStore name.

* **The SecretStore isn't valid with workload identity federation:** Make sure that the issuer URL and the `system:serviceaccount:<namespace>:mysterybox-reader` subject in the federated credentials match your cluster and ServiceAccount, and that the RoleBinding refers to the ESO controller's ServiceAccount.

* **The SecretStore isn't valid with service account credentials:** Get the details by running `kubectl describe secretstore mysterybox -n $K8S_NAMESPACE`.

  * If the events contain `Public Key not exists, expired or deactivated`, the authorized key has expired or been deleted. Delete the old credentials file, generate new credentials and recreate the `mysterybox-sa-credentials` Kubernetes Secret. ESO caches access tokens, so the SecretStore can stay valid for several hours after the key stops working.
  * If the events contain `invalid subject credentials: malformed JSON`, delete the credentials file, generate the credentials again and recreate the Kubernetes Secret.

* **Access is denied:** Make sure that the service account is in a group with the `mysterybox.payload-viewer` role for the secret or its project.

* **The payload is empty or has unexpected keys:** Check the payload of the secret:

  ```bash theme={null}
  nebius mysterybox payload get --secret-id mbsec-*** --version-id mbsecver-***
  ```

  Keys that you specify in `property` must match the keys of the payload.

* **A Kubernetes resource has an empty namespace or ID:** If you opened a new terminal session when configuring the sync of secrets, the environment variables aren't set. Set `K8S_NAMESPACE`, `SA_ID` and `SECRET_ID` again, then delete and recreate the affected resources.
