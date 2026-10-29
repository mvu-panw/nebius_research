# Using an OIDC public endpoint in Managed Service for Kubernetes® clusters

Source: https://docs.nebius.com/kubernetes/networking/oidc-public-endpoint

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Using an OIDC public endpoint in Managed Service for Kubernetes® clusters

All Managed Service for Kubernetes clusters expose a public OpenID Connect (OIDC) discovery endpoint. External systems can use this endpoint to independently verify workload identities using [JSON Web Tokens (JWT)](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#json-web-token-authentication) that Kubernetes issues automatically.

You can use this endpoint to let an external service trust your Managed Kubernetes cluster workloads.

## OIDC endpoints

For every cluster, Managed Kubernetes exposes the following endpoints at `https://oidc.mk8s.api.nebius.cloud`:

| Endpoint | Description |
| - | - |
| `GET /<cluster_ID>/.well-known/openid-configuration` | The OIDC discovery document for the cluster. |
| `GET /<cluster_ID>/openid/v1/jwks` | The JSON Web Key Set (JWKS) containing the public keys used to verify the tokens issued by the cluster. |

Both endpoints are accessible without authentication, so any OIDC-compatible service can fetch them directly.

## How to get a cluster's OIDC endpoint URLs

1. Get the ID of your cluster by its name:

   ```bash theme={null}
   nebius mk8s cluster get-by-name \
      --name <cluster_name> --format jsonpath='{.metadata.id}'
   ```

2. Replace `<cluster_ID>` with your cluster ID in the endpoint URLs:

   ```text theme={null}
   https://oidc.mk8s.api.nebius.cloud/<cluster_ID>/.well-known/openid-configuration
   https://oidc.mk8s.api.nebius.cloud/<cluster_ID>/openid/v1/jwks
   ```

3. Use these URLs when you register an OIDC identity provider or configure workload identity federation.
