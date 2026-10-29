# Authentication in the Nebius AI Cloud gRPC API

Source: https://docs.nebius.com/grpc-api/auth

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Authentication in the Nebius AI Cloud gRPC API

For authentication, use an [access token](https://docs.nebius.com/iam/authorization/access-tokens.md). Include it in the HTTP header `Authorization: Bearer <access_token>`.

The authentication process differs for a [user account and a service account](https://docs.nebius.com/iam/overview.md#accounts-and-members).

## Authentication for a user account

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.

2. Create an access token:

   ```bash theme={null}
   nebius iam get-access-token
   ```

   An access token is valid for 12 hours. After it expires, create a new one.

3. Add the token to your API request. For example:

   ```bash theme={null}
   grpcurl -H "Authorization: Bearer <access_token>" \
      cpl.iam.api.nebius.cloud:443 \
      nebius.iam.v1.ProfileService/Get
   ```

## Authentication for a service account

To authenticate a service account, create an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) for it and then convert this key into an access token by using a [JSON Web Token (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token). Next, use the obtained access token for authentication.

### Prepare a service account

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md) if you haven't already.
3. [Add the service account to a group](https://docs.nebius.com/iam/authorization/groups/members.md) to grant it necessary permissions. In most cases, a group with the `editor` role should be enough; add the account to a group with the `admin` role only if you want to manage group memberships of other accounts through the API. Learn more about [groups](https://docs.nebius.com/iam/authorization/groups/index.md) and their [permissions](https://docs.nebius.com/iam/authorization/roles.md).

### Prepare an authorized key

1. Create an authorized key:

   ```bash theme={null}
   openssl genrsa -out private.pem 4096 && \
   openssl rsa -in private.pem -outform PEM -pubout -out public.pem
   ```

   This command creates the `public.pem` and `private.pem` key files in a local directory.

2. Upload the key to the service account profile:

   **Web console**

   1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM**.
   2. Open the **Service accounts** tab.
   3. Open the page of the required service account.
   4. Click  **Upload authorized key**.
   5. Click  **Attach file** and then select `public.pem`.
   6. (Optional) Set an expiration date.
   7. Click **Upload key**.

   The key is displayed on the **Authorized keys** tab.

   **CLI**

   ```bash theme={null}
   nebius iam auth-public-key create \
     --account-service-account-id <service_account_ID> \
     --data "$(cat <path/to/public.pem>)" \
     --expires-at <date_and_time>
   ```

   The command contains the following parameters:

   * `--account-service-account-id`: Service account ID. To get it, run `nebius iam service-account list` or `nebius iam service-account get-by-name --name <service_account_name>`.
   * `--data`: Contents of the `public.pem` file created earlier.
   * `--expires-at` (optional): Expiration date of the authorized key.

   > **Output example**
   >
   > ```yaml theme={null}
   > metadata:
   >    created_at: "2025-08-22T09:37:07.023669Z"
   >    id: publickey-***
   >    parent_id: project-***
   > spec:
   >    account:
   >       service_account:
   >          id: serviceaccount-***
   >    data: |
   >       -----BEGIN PUBLIC KEY-----
   >       ...
   >       -----END PUBLIC KEY-----
   >    expires_at: "2025-12-31T02:30:59Z"
   > status:
   >    algorithm: RSA
   >    fingerprint: a4c4***
   >    key_size: 4096
   >    state: ACTIVE
   > ```

3. Copy and save the account ID and the authorized key ID. You need them for the JWT.

### Create a JWT

1. [Install jwt-cli](https://github.com/mike-engel/jwt-cli?tab=readme-ov-file#installation), the CLI for JWT management.
2. Create the JWT:

   ```bash theme={null}
   jwt encode \
      --alg RS256 \
      --kid <authorized_key_ID> \
      --iss <service_account_ID> \
      --sub <service_account_ID> \
      --exp="$(date --date="+5minutes" +%s 2>/dev/null || date -v+5M +%s)" \
      --secret @<path_to_private.pem>
   ```

   In the command, specify the copied authorized key ID and the service account ID. Also, specify the current path to the `private.pem` file created earlier.

   The command returns the JWT as a string. Use this value in the token exchange request.

   The JWT is based on the RS256 signing algorithm and expires five minutes after its creation. The lifetime is short because the JWT is only used to create an access token.

### Get an access token

1. To exchange the JWT for an access token, send the following API request:

   ```bash theme={null}
   grpcurl -d '{
                  "grantType": "urn:ietf:params:oauth:grant-type:token-exchange",
                  "requestedTokenType": "urn:ietf:params:oauth:token-type:access_token",
                  "subjectToken": "<JWT>",
                  "subjectTokenType": "urn:ietf:params:oauth:token-type:jwt"
               }' \
      tokens.iam.api.nebius.cloud:443 \
      nebius.iam.v1.TokenExchangeService/Exchange
   ```

   Specify the JWT in the request.

   The output is the following:

   ```json theme={null}
   {
      "accessToken": "<access_token>",
      "issuedTokenType": "urn:ietf:params:oauth:token-type:access_token",
      "tokenType": "Bearer",
      "expiresIn": "43200"
   }
   ```

   The access token expires 12 hours after its creation. The `expiresIn` value from the output is specified in seconds.

2. Add the token to your API request. For example:

   ```bash theme={null}
   grpcurl -H "Authorization: Bearer <access_token>" \
      cpl.iam.api.nebius.cloud:443 \
      nebius.iam.v1.ProfileService/Get
   ```
