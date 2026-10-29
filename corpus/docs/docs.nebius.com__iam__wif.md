# Accessing external resources from Nebius AI Cloud workloads

Source: https://docs.nebius.com/iam/wif

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Accessing external resources from Nebius AI Cloud workloads

Most cloud providers allow configuring trust relationships with external identity providers by using industry-standard protocols such as OAuth 2.0, OpenID Connect (OIDC) and SAML. This enables secure authentication across cloud boundaries.

Nebius AI Cloud allows you to produce ID tokens for your workloads. You can use these tokens to set up trust relationships based on the [OIDC Discovery](https://openid.net/specs/openid-connect-discovery-1_0.html) mechanism.

## How it works

In the supported flow:

1. A workload runs in Nebius AI Cloud, for example, on a [Compute virtual machine (VM)](https://docs.nebius.com/compute/virtual-machines/manage.md).
2. The workload gets a Nebius IAM `access_token`.
3. The workload exchanges its Nebius access token for a signed ID token through Nebius Security Token Service (STS) `https://sts.nebius.com` by using the `/oauth2/token/exchange` endpoint and sends the token to the target system.
4. The target system evaluates the ID token against its trust policy and, if accepted, either authorizes the workload directly or issues short-lived credentials.
5. The workload uses the resulting authorization or credentials to access the external resource.

> **Nebius STS and token exchange endpoint**
>
> Nebius STS is an HTTP-based service that exchanges identity credentials for short-lived Nebius access tokens or OIDC ID tokens. Nebius STS also exposes an OIDC discovery endpoint at `/.well-known/openid-configuration`. Target systems use it to validate ID tokens issued by the service.
>
> The `/oauth2/token/exchange` endpoint is based on [OAuth 2.0 Token Exchange (RFC 8693)](https://datatracker.ietf.org/doc/html/rfc8693) and accepts the following parameters:
>
> | Parameter | Description |
> | - | - |
> | `grant_type` | Must be `urn:ietf:params:oauth:grant-type:token-exchange`. |
> | `requested_token_type` (optional) | The type of token to issue. The default is `urn:ietf:params:oauth:token-type:access_token`. |
> | `subject_token` | The token that represents the identity for which a new token is requested. This can be a self-signed JWT, an access token or a subject identifier. |
> | `subject_token_type` | The type of the subject token. |
> | `actor_token` (optional) | A token that represents the acting identity of the exchange flow, for example, an external JWT. |
> | `actor_token_type` (optional) | The type of the actor token. Required when `actor_token` is provided. |
> | `audience` (optional) | The intended audience of the issued token. Required for the system in which the token will be used. |
>
> Supported token types:
>
> | Token type | Description |
> | - | - |
> | `urn:ietf:params:oauth:token-type:access_token` | Nebius IAM access token. |
> | `urn:ietf:params:oauth:token-type:jwt` | Self-signed JWT for a service account, or an external JWT. |
> | `urn:nebius:params:oauth:token-type:subject_identifier` | Nebius IAM subject identifier. |
> | `urn:ietf:params:oauth:token-type:id_token` | Nebius IAM JWT-based ID token. |
>
> Nebius STS returns the issued token in the `access_token` field of the token exchange response for OAuth compatibility. To verify that you received an ID token, check that `issued_token_type` is `urn:ietf:params:oauth:token-type:id_token`.

## Supported flows

Any platform that supports OIDC Discovery can establish trust with this identity provider and validate the issued ID tokens. For an example of how such a trust relationship can be established with Google Cloud, see [Configuring access to Google Cloud for Nebius AI Cloud workloads](https://docs.nebius.com/iam/wif/configure.md).

## Security recommendations

* Never log raw Nebius IAM tokens, Nebius `id_token` values, external cloud access tokens or other short-lived credentials.
* Use dedicated audiences per destination, client and environment: for example, separate audiences for development, staging and production.

## Limitations

* The workload must be able to obtain a Nebius IAM `access_token`, for example through the instance metadata service, a service account authorized key or another supported [authentication method](https://docs.nebius.com/iam/service-accounts/authentication.md).
* The external platform must be able to reach `https://sts.nebius.com` to verify ID tokens by using the [OIDC Discovery](https://openid.net/specs/openid-connect-discovery-1_0.html) mechanism.
