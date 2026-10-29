# Configuring access to Google Cloud for Nebius AI Cloud workloads

Source: https://docs.nebius.com/iam/wif/configure

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuring access to Google Cloud for Nebius AI Cloud workloads

This guide explains how to configure access to Google Cloud resources for Nebius workloads using OpenID Connect (OIDC) ID tokens. The setup is based on [Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation). For details on how trust works from the Nebius side, see [Nebius workloads access to external resources overview](https://docs.nebius.com/iam/wif/index.md).

## Prerequisites

1. Create or select an existing Google Cloud project.

2. [Install and initialize the Google Cloud CLI](https://cloud.google.com/sdk/docs/install) and configure it to use the target Google Cloud project.

3. Install [jq](https://jqlang.github.io/jq/download/) to extract token values from JSON responses:

   ```bash Ubuntu theme={null}
   sudo apt-get install jq
   ```

   ```bash macOS theme={null}
   brew install jq
   ```

4. Make sure that you can create a Google Cloud workload identity federation (WIF) pool and OIDC provider and grant IAM access to the target resource in that project.

5. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md) for the workload in Nebius AI Cloud.

6. Configure the workload to authenticate as this service account:

   * For a virtual machine (VM), attach the service account to the VM and retrieve an IAM token from the [instance metadata service](https://docs.nebius.com/compute/virtual-machines/instance-metadata.md#getting-service-account-information).
   * If you cannot use the metadata service, [create an authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) for the service account or provide an IAM token to the workload by using your approved secret delivery method.

   Do not put service account authorized keys into container images, startup scripts, source code or logs.

7. Create a Google Cloud resource to test access to. This guide uses a Cloud Storage bucket.

## Configure Google Cloud trust

1. Set variables for the Google Cloud configuration:

   ```bash theme={null}
   export GCP_PROJECT_NUMBER="<GCP_project_number>"
   export GCP_BUCKET="<bucket_name>"
   export GCP_OBJECT="wif-test.txt"
   export WKID_POOL_ID="nebius-pool"
   export WKID_PROVIDER_ID="nebius"
   export NEBIUS_ISSUER="https://sts.nebius.com"
   ```

2. Create a Cloud Storage bucket and test object:

   ```bash theme={null}
   gcloud storage buckets create "gs://${GCP_BUCKET}" --location="eu"
   gcloud storage buckets update "gs://${GCP_BUCKET}" --uniform-bucket-level-access
   echo "Hello from workload identity test!" > "/tmp/${GCP_OBJECT}"
   gcloud storage cp "/tmp/${GCP_OBJECT}" "gs://${GCP_BUCKET}/${GCP_OBJECT}"
   rm "/tmp/${GCP_OBJECT}"
   ```

3. Create a Google Cloud workload identity pool:

   ```bash theme={null}
   gcloud iam workload-identity-pools create "${WKID_POOL_ID}" \
     --location="global" \
     --display-name="Nebius workloads pool" \
     --description="Nebius integration sample"
   ```

4. Register Nebius Security Token Service (STS) as an OIDC identity provider:

   ```bash theme={null}
   gcloud iam workload-identity-pools providers create-oidc "${WKID_PROVIDER_ID}" \
     --location="global" \
     --workload-identity-pool="${WKID_POOL_ID}" \
     --issuer-uri="${NEBIUS_ISSUER}" \
     --attribute-mapping="google.subject=assertion.sub"
   ```

   Google Cloud will use Nebius OIDC discovery to resolve Nebius STS metadata and signing keys.

## Exchange a Nebius access token for a Nebius ID token

1. In the Nebius workload, get a Nebius IAM `access_token`. For details, see [How to authenticate as a service account](https://docs.nebius.com/iam/service-accounts/authentication.md).

2. Export the access token and target audience:

   ```bash theme={null}
   export NEBIUS_ACCESS_TOKEN="<nebius_access_token>"
   export GCP_ALLOWED_AUDIENCE="//iam.googleapis.com/projects/${GCP_PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WKID_POOL_ID}/providers/${WKID_PROVIDER_ID}"
   ```

3. Exchange the Nebius `access_token` for a Nebius `id_token`:

   ```bash theme={null}
   export NEBIUS_ID_TOKEN=$(
     curl -sS -X POST "https://sts.nebius.com/oauth2/token/exchange" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
       --data-urlencode "requested_token_type=urn:ietf:params:oauth:token-type:id_token" \
       --data-urlencode "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
       --data-urlencode "subject_token=${NEBIUS_ACCESS_TOKEN}" \
       --data-urlencode "audience=${GCP_ALLOWED_AUDIENCE}" \
     | jq -r ".access_token"
   )
   ```

## Exchange the Nebius ID token for a Google access token

Exchange the Nebius `id_token` by using the Google STS token endpoint:

```bash theme={null}
export GOOGLE_ACCESS_TOKEN=$(
  curl -sS -X POST "https://sts.googleapis.com/v1/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
    --data-urlencode "requested_token_type=urn:ietf:params:oauth:token-type:access_token" \
    --data-urlencode "subject_token_type=urn:ietf:params:oauth:token-type:jwt" \
    --data-urlencode "subject_token=${NEBIUS_ID_TOKEN}" \
    --data-urlencode "audience=${GCP_ALLOWED_AUDIENCE}" \
    --data-urlencode "scope=https://www.googleapis.com/auth/cloud-platform" \
  | jq -r ".access_token"
)
```

## Verify the result

1. Try to read the test object:

   ```bash theme={null}
   curl -sS \
     -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" \
     "https://storage.googleapis.com/storage/v1/b/${GCP_BUCKET}/o/${GCP_OBJECT}?alt=media"
   ```

   If the Google Cloud principal does not have access to the bucket yet, Google Cloud returns an error similar to this:

   ```json theme={null}
   {
     "error": {
       "code": 403,
       "message": "Caller does not have storage.objects.list access to the Google Cloud Storage bucket. Permission 'storage.objects.list' denied on resource (or it may not exist)."
     }
   }
   ```

2. Grant the federated principal access to the bucket:

   ```bash theme={null}
   gcloud storage buckets add-iam-policy-binding "gs://${GCP_BUCKET}" \
     --role="roles/storage.objectViewer" \
     --member="principal://iam.googleapis.com/projects/${GCP_PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WKID_POOL_ID}/subject/<nebius_subject>"
   ```

   Replace `<nebius_subject>` with the `sub` claim value from the Nebius `id_token`.

3. Read the object again:

   ```bash theme={null}
   curl -sS \
     -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" \
     "https://storage.googleapis.com/storage/v1/b/${GCP_BUCKET}/o/${GCP_OBJECT}?alt=media"
   ```

   The result must be:

   ```text theme={null}
   Hello from workload identity test!
   ```

## Troubleshooting

### The workload cannot get a Nebius access token

Make sure that the workload has a Nebius service account attached or that the service account authorized key or IAM token is available inside the workload. For Compute VMs, see [Getting service account information](https://docs.nebius.com/compute/virtual-machines/instance-metadata.md#getting-service-account-information).

### The Nebius token exchange fails

Check that the `subject_token` value contains a valid Nebius IAM `access_token`, and that `audience` is the target system audience that will validate the resulting `id_token`.

### The Google token exchange fails

Check that the Google Cloud workload identity provider uses `https://sts.nebius.com` as the issuer URI, and that the Google STS `audience` value is the full provider resource name:

```text theme={null}
//iam.googleapis.com/projects/<GCP_project_number>/locations/global/workloadIdentityPools/<pool_ID>/providers/<provider_ID>
```

### The Google access token cannot read the resource

Check the Google Cloud IAM policy on the target resource. A successful token exchange only proves that Google Cloud trusts the Nebius identity assertion. It does not grant access to resources unless the federated principal has the required Google Cloud IAM role.
