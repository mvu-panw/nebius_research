# How to manage federations in Nebius AI Cloud

Source: https://docs.nebius.com/iam/federations/manage

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# How to manage federations in Nebius AI Cloud

A [federation](https://docs.nebius.com/iam/overview.md#federations) connects your identity provider (IdP) to Nebius AI Cloud, allowing users from your organization to log in with [single sign-on (SSO)](https://docs.nebius.com/iam/federations/saml-sso.md).

In Nebius AI Cloud, you can create, activate, deactivate and delete federations, change their settings, and upload or delete attached certificates.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Make sure that you have access to your IdP admin portal and can get the SAML application metadata (login URL, identifier, certificate) required to create a federation.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to your IdP admin portal and can get the SAML application metadata (login URL, identifier, certificate) required to create a federation.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to your IdP admin portal and can get the SAML application metadata (login URL, identifier, certificate) required to create a federation.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to your IdP admin portal and can get the SAML application metadata (login URL, identifier, certificate) required to create a federation.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to your IdP admin portal and can get the SAML application metadata (login URL, identifier, certificate) required to create a federation.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to your IdP admin portal and can get the SAML application metadata (login URL, identifier, certificate) required to create a federation.

## Creating a federation

**Web console**

1. In the [web console](https://console.nebius.com), go to  **Administration** → **IAM**.

2. Go to the **Federations** tab.

3. Click **Create entity** → **Federation**.

4. Specify the IdP settings:

   * If you have an XML file with SAML metadata:

     1. Enter a federation name.
     2. Click **Upload file** and select the XML file with the SAML metadata from your IdP, then click **Continue**.
     3. On the page that opens, enter a name for the certificate in the **Certificates** section.

   * If you don't have an XML file, enter the SAML metadata manually:

     1. Enable **Manual mode** and enter a federation name.
     2. Under **Identity provider (IdP)**, specify the **SSO URL** and **Issuer** parameters from your IdP, then click **Continue**.
     3. On the page that opens, enter a certificate name, then either upload the PEM certificate file, or copy and paste the certificate body into the field.

5. Click **Create federation**.

**CLI**

1. To create a federation, run the following command:

   ```bash theme={null}
   nebius iam federation create \
     --name <federation_name> \
     --parent-id <tenant_ID> \
     --saml-settings-sso-url <URL_to_log_in> \
     --saml-settings-idp-issuer <application_identifier>
   ```

   The command contains the following parameters:

   * `--name`: Federation name.
   * `--parent-id`: [ID of the tenant](https://docs.nebius.com/iam/get-tenants.md#cli-2) in which you create the federation.
   * `--saml-settings-sso-url`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
   * `--saml-settings-idp-issuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

2. Copy and save the federation ID. It is returned in the `metadata.id` parameter of the command output.

3. After you create a federation, attach a certificate to it. Prepare the `federation-cert.json` file:

   ```json theme={null}
   {
     "metadata": {
       "parent_id": "<federation_ID>",
       "name": "<certificate_name>"
     },
     "spec": {
       "description": "certificate for a federation",
       "data": "-----BEGIN CERTIFICATE-----\n<certificate_body>\n-----END CERTIFICATE-----\n"
     }
   }
   ```

   If the certificate body is split into several lines in the source, paste the body as a single line in `federation-cert.json`.

4. Apply the certificate file:

   ```bash theme={null}
   nebius iam federation-certificate create --file federation-cert.json
   ```

**Terraform**

1. Create a federation:

   1. Prepare the following configuration file:

      ```hcl theme={null}
      resource "nebius_iam_v1_federation" "<federation_name>" {
        name      = "<federation_name>"
        parent_id = "<tenant_ID>"
        saml_settings = {
          sso_url    = "<URL_to_log_in>"
          idp_issuer = "<application_identifier>"
        }
      }
      ```

      The file contains the following parameters:

      * `name`: Federation name.
      * `parent_id`: [ID of the tenant](https://docs.nebius.com/iam/get-tenants.md#cli-2) in which you create the federation.
      * `saml_settings.sso_url`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
      * `saml_settings.idp_issuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

2. After you create a federation, attach a certificate to it:

   1. Prepare a certificate manifest in the same file where you store the `nebius_iam_v1_federation` resource:

      ```hcl theme={null}
      resource "nebius_iam_v1_federation_certificate" "certificate_for_<federation_name>" {
        parent_id   = nebius_iam_v1_federation.<federation_name>.id
        name        = "certificate"
        data        = file("${path.module}/certificate.pem")
        description = "certificate for a federation"
        depends_on  = [nebius_iam_v1_federation.<federation_name>]
      }
      ```

      In the resource, specify the federation name. Save your PEM certificate as `certificate.pem` in the Terraform working directory — the `file()` function reads the certificate from that file.

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

**Go SDK**

1. To create a federation, run the following code:

   ```go theme={null}
   federationOperation, err := sdk.Services().IAM().V1().
       Federation().Create(
           ctx,
           &iam.CreateFederationRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<tenant_ID>",
                   Name:     "<federation_name>",
               },
               Spec: &iam.FederationSpec{
                   Settings: &iam.FederationSpec_SamlSettings{
                       SamlSettings: &iam.SamlSettings{
                           SsoUrl:    "<URL_to_log_in>",
                           IdpIssuer: "<application_identifier>",
                       },
                   },
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = federationOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   The code contains the following parameters:

   * `Metadata.ParentId`: [ID of the tenant](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2) in which you create the federation.
   * `Metadata.Name`: Federation name.
   * `Spec.Settings.SamlSettings.SsoUrl`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
   * `Spec.Settings.SamlSettings.IdpIssuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

2. Copy and save the federation ID. It's returned by `federationOperation.ResourceID()`.

3. After you create a federation, attach a certificate to it:

   ```go theme={null}
   certificateOperation, err := sdk.Services().IAM().V1().
       FederationCertificate().Create(
           ctx,
           &iam.CreateFederationCertificateRequest{
               Metadata: &common.ResourceMetadata{
                   ParentId: "<federation_ID>",
               },
               Spec: &iam.FederationCertificateSpec{
                   Description: "certificate for a federation",
                   Data:        certificateData,
               },
           },
       )
   if err != nil {
       return err
   }
   if _, err = certificateOperation.Wait(ctx); err != nil {
       return err
   }
   ```

   In the code, set `Metadata.ParentId` to the federation ID from the previous step, and assign your PEM-encoded certificate body to the `certificateData` variable used in `Spec.Data`.

**Python SDK**

1. To create a federation, run the following code:

   ```python theme={null}
   federation_service = FederationServiceClient(sdk)
   federation_operation = await federation_service.create(
       CreateFederationRequest(
           metadata=ResourceMetadata(
               parent_id="<tenant_ID>",
               name="<federation_name>",
           ),
           spec=FederationSpec(
               saml_settings=SamlSettings(
                   sso_url="<URL_to_log_in>",
                   idp_issuer="<application_identifier>",
               ),
           ),
       ),
   )
   await federation_operation.wait()
   ```

   The code contains the following parameters:

   * `metadata.parent_id`: [ID of the tenant](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2) in which you create the federation.
   * `metadata.name`: Federation name.
   * `spec.saml_settings.sso_url`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
   * `spec.saml_settings.idp_issuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

2. Copy and save the federation ID. It's returned by `federation_operation.resource_id`.

3. After you create a federation, attach a certificate to it:

   ```python theme={null}
   cert_service = FederationCertificateServiceClient(sdk)
   certificate_operation = await cert_service.create(
       CreateFederationCertificateRequest(
           metadata=ResourceMetadata(parent_id="<federation_ID>"),
           spec=FederationCertificateSpec(
               description="certificate for a federation",
               data=certificate_data,
           ),
       ),
   )
   await certificate_operation.wait()
   ```

   In the code, set `metadata.parent_id` to the federation ID from the previous step, and assign your PEM-encoded certificate body to the `certificate_data` variable used in `spec.data`.

**JavaScript SDK**

1. To create a federation, run the following code:

   ```ts theme={null}
   const federationService = new FederationService(sdk);
   const federationOperation = await federationService.create(
     CreateFederationRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<tenant_ID>",
         name: "<federation_name>",
       }),
       spec: FederationSpec.create({
         settings: {
           $case: "samlSettings",
           samlSettings: SamlSettings.create({
             ssoUrl: "<URL_to_log_in>",
             idpIssuer: "<application_identifier>",
           }),
         },
       }),
     }),
   ).result;
   await federationOperation.wait();
   ```

   The code contains the following parameters:

   * `metadata.parentId`: [ID of the tenant](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2) in which you create the federation.
   * `metadata.name`: Federation name.
   * `spec.settings.samlSettings.ssoUrl`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
   * `spec.settings.samlSettings.idpIssuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

2. Copy and save the federation ID. It's returned by `federationOperation.resourceId()`.

3. After you create a federation, attach a certificate to it:

   ```ts theme={null}
   const createCertificateService =
     new FederationCertificateService(sdk);
   const certificateOperation = await createCertificateService.create(
     CreateFederationCertificateRequest.create({
       metadata: ResourceMetadata.create({
         parentId: "<federation_ID>",
       }),
       spec: FederationCertificateSpec.create({
         description: "certificate for a federation",
         data: certificateData,
       }),
     }),
   ).result;
   await certificateOperation.wait();
   ```

   In the code, set `metadata.parentId` to the federation ID from the previous step, and assign your PEM-encoded certificate body to the `certificateData` variable used in `spec.data`.

For more information, see examples for specific IdPs in [Configuring SSO with identity providers](https://docs.nebius.com/iam/federations/saml-sso.md).

## Changing federation settings

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.

2. Go to the **Federations** tab.

3. Next to the federation, click  → **Configure**.

4. Update federation settings:

   * **Name**: Federation name.
   * **SSO URL**: Login URL from your IdP.
   * **Issuer**: Your IdP identifier string.

5. Click **Save changes** to apply the new settings.

**CLI**

To change federation settings, run the following command:

```bash theme={null}
nebius iam federation update <federation_ID> \
  --name <new_federation_name> \
  --saml-settings-sso-url <URL_to_log_in> \
  --saml-settings-idp-issuer <application_identifier>
```

You can change the following parameters:

* `--name`: Federation name.
* `--saml-settings-sso-url`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
* `--saml-settings-idp-issuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

> **How to get the federation ID**
>
> ```bash theme={null}
> nebius iam federation list --parent-id <tenant_ID>
> ```
>
> The ID is specified in the `.items.metadata.id` parameter.

**Terraform**

1. Modify the manifest with the deployed federation:

   ```hcl theme={null}
   resource "nebius_iam_v1_federation" "<federation_name>" {
     name          = "<new_federation_name>"
     saml_settings = {
       sso_url    = "<URL_to_log_in>"
       idp_issuer = "<application_identifier>"
     }
   }
   ```

   You can change the following parameters:

   * `name`: Federation name.
   * `saml_settings.sso_url`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
   * `saml_settings.idp_issuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

The SDK has no partial update call, so to change federation settings, get the federation, modify the parameters you want to change, then send the updated metadata and spec back:

```go theme={null}
federationForUpdate, err := sdk.Services().IAM().V1().
    Federation().Get(
        ctx,
        &iam.GetFederationRequest{Id: "<federation_ID>"},
    )
if err != nil {
    return err
}
federationForUpdate.GetMetadata().Name = "<new_federation_name>"
federationForUpdate.GetSpec().GetSamlSettings().SsoUrl =
    "<URL_to_log_in>"
federationForUpdate.GetSpec().GetSamlSettings().IdpIssuer =
    "<application_identifier>"
updateFederationOperation, err := sdk.Services().IAM().
    V1().Federation().Update(
        ctx,
        &iam.UpdateFederationRequest{
            Metadata: federationForUpdate.GetMetadata(),
            Spec:     federationForUpdate.GetSpec(),
        },
    )
if err != nil {
    return err
}
if _, err = updateFederationOperation.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameters:

* `Id` in `GetFederationRequest`: Federation ID. Use the ID you saved when [creating the federation](#creating-a-federation).
* `Metadata.Name`: Federation name.
* `Spec.SamlSettings.SsoUrl`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
* `Spec.SamlSettings.IdpIssuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

> **How to get the federation ID**
>
> ```go theme={null}
> listedFederations, err := sdk.Services().IAM().V1().
>     Federation().List(
>     ctx,
>     &iam.ListFederationsRequest{ParentId: "<tenant_ID>"},
> )
> if err != nil {
>     return err
> }
> fmt.Println(listedFederations)
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listedFederations.GetItems()[i].GetMetadata().GetId()`.

**Python SDK**

The SDK has no partial update call, so to change federation settings, get the federation, modify the parameters you want to change, then send the updated metadata and spec back:

```python theme={null}
federation_service = FederationServiceClient(sdk)
federation = await federation_service.get(
    GetFederationRequest(id="<federation_ID>"),
)
if federation.metadata is None or federation.spec is None:
    raise ValueError("federation resource is incomplete")
if federation.spec.saml_settings is None:
    raise ValueError("federation SAML settings are missing")
federation.metadata.name = "<new_federation_name>"
federation.spec.saml_settings.sso_url = "<URL_to_log_in>"
federation.spec.saml_settings.idp_issuer = "<application_identifier>"
update_federation_operation = await federation_service.update(
    UpdateFederationRequest(
        metadata=federation.metadata,
        spec=federation.spec,
    ),
)
await update_federation_operation.wait()
```

The code contains the following parameters:

* `id` in `GetFederationRequest`: Federation ID. Use the ID you saved when [creating the federation](#creating-a-federation).
* `metadata.name`: Federation name.
* `spec.saml_settings.sso_url`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
* `spec.saml_settings.idp_issuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

> **How to get the federation ID**
>
> ```python theme={null}
> federation_service = FederationServiceClient(sdk)
> listed_federations = await federation_service.list(
>     ListFederationsRequest(parent_id="<tenant_ID>"),
> )
> print(listed_federations)
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listed_federations.items[i].metadata.id`.

**JavaScript SDK**

The SDK has no partial update call, so to change federation settings, get the federation, modify the parameters you want to change, then send the updated metadata and spec back:

```ts theme={null}
const updateFederationService = new FederationService(sdk);
const federationForUpdate = await updateFederationService.get(
  GetFederationRequest.create({
    id: "<federation_ID>",
  }),
);
if (!federationForUpdate.metadata ||
    !federationForUpdate.spec) {
  throw new Error("federation resource is incomplete");
}
if (federationForUpdate.spec.settings?.$case !==
    "samlSettings") {
  throw new Error("federation SAML settings are missing");
}
federationForUpdate.metadata.name = "<new_federation_name>";
federationForUpdate.spec.settings.samlSettings.ssoUrl =
  "<URL_to_log_in>";
federationForUpdate.spec.settings.samlSettings.idpIssuer =
  "<application_identifier>";
const updateFederationOperation =
  await updateFederationService.update(
    UpdateFederationRequest.create({
      metadata: federationForUpdate.metadata,
      spec: federationForUpdate.spec,
    }),
  ).result;
await updateFederationOperation.wait();
```

The code contains the following parameters:

* `id` in `GetFederationRequest`: Federation ID. Use the ID you saved when [creating the federation](#creating-a-federation).
* `metadata.name`: Federation name.
* `spec.settings.samlSettings.ssoUrl`: URL of the page that opens when a federated user logs in. For example, Microsoft Entra ID calls it **Login URL**.
* `spec.settings.samlSettings.idpIssuer`: Identifier of your SAML application. For example, Microsoft Entra ID calls it **Microsoft Entra Identifier**.

> **How to get the federation ID**
>
> ```ts theme={null}
> const listFederationService = new FederationService(sdk);
> const listedFederations = await listFederationService.list(
>   ListFederationsRequest.create({
>     parentId: "<tenant_ID>",
>   }),
> );
> console.log(listedFederations);
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listedFederations.items[i].metadata?.id`.

## Changing federation certificates

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.

2. Go to the **Federations** tab and open the federation whose certificate you want to change.

3. On the **Certificates** tab, rename or delete a certificate.

   > [!WARNING]
   >
   > A federation cannot function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

4. To add a new certificate:
   1. Click **Attach certificate**.
   2. Enter a certificate name, then either upload the PEM certificate file, or copy and paste the certificate body into the field.
   3. Click **Attach certificates**.

**CLI**

When changing federation certificates, you can rename, add or delete a certificate.

* Rename a certificate:

  ```bash theme={null}
  nebius iam federation-certificate update <certificate_ID> --name <new_certificate_name>
  ```

* Delete a certificate:

  ```bash theme={null}
  nebius iam federation-certificate delete <certificate_ID>
  ```

  > [!WARNING]
  >
  > A federation cannot function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

For information about adding a new certificate, see [Creating a federation](#creating-a-federation).

> **How to get the certificate ID**
>
> ```bash theme={null}
> nebius iam federation-certificate list-by-federation --federation-id <federation_ID>
> ```
>
> The ID is specified in the `.items.metadata.id` parameter.

**Terraform**

When changing federation certificates, you can rename, add or delete a certificate:

* To rename a certificate, update the `name` parameter in the `nebius_iam_v1_federation_certificate` resource.
* To delete a certificate, remove the `nebius_iam_v1_federation_certificate` resource from the configuration file.

  > [!WARNING]
  >
  > A federation cannot function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

For information about adding a new certificate, see [Creating a federation](#creating-a-federation).

**Go SDK**

When changing federation certificates, you can rename or delete a certificate.

* Rename a certificate. The SDK has no partial update call, so get the certificate, change its `Metadata.Name`, then send the updated metadata and spec back:

  ```go theme={null}
  certificate, err := sdk.Services().IAM().V1().
      FederationCertificate().Get(
          ctx,
          &iam.GetFederationCertificateRequest{
              Id: "<certificate_ID>",
          },
      )
  if err != nil {
      return err
  }
  certificate.GetMetadata().Name = "<new_certificate_name>"
  updateCertificateOperation, err := sdk.Services().IAM().
      V1().FederationCertificate().Update(
          ctx,
          &iam.UpdateFederationCertificateRequest{
              Metadata: certificate.GetMetadata(),
              Spec:     certificate.GetSpec(),
          },
      )
  if err != nil {
      return err
  }
  if _, err = updateCertificateOperation.Wait(ctx); err != nil {
      return err
  }
  ```

* Delete a certificate:

  ```go theme={null}
  deleteCertificateOperation, err := sdk.Services().IAM().
      V1().FederationCertificate().Delete(
          ctx,
          &iam.DeleteFederationCertificateRequest{
              Id: "<certificate_ID>",
          },
      )
  if err != nil {
      return err
  }
  if _, err = deleteCertificateOperation.Wait(ctx); err != nil {
      return err
  }
  ```

  > [!WARNING]
  >
  > A federation cannot function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

For information about adding a new certificate, see [Creating a federation](#creating-a-federation).

> **How to get the certificate ID**
>
> ```go theme={null}
> listedFederationCertificates, err := sdk.Services().IAM().
>     V1().FederationCertificate().ListByFederation(
>         ctx,
>         &iam.ListFederationCertificateByFederationRequest{
>             FederationId: "<federation_ID>",
>         },
> )
> if err != nil {
>     return err
> }
> fmt.Println(listedFederationCertificates)
> ```
>
> The response returns the certificate ID in each item's metadata, accessible as `listedFederationCertificates.GetItems()[i].GetMetadata().GetId()`.

**Python SDK**

When changing federation certificates, you can rename or delete a certificate.

* Rename a certificate. The SDK has no partial update call, so get the certificate, change its `metadata.name`, then send the updated metadata and spec back:

  ```python theme={null}
  cert_service = FederationCertificateServiceClient(sdk)
  certificate = await cert_service.get(
      GetFederationCertificateRequest(id="<certificate_ID>"),
  )
  if certificate.metadata is None or certificate.spec is None:
      raise ValueError("certificate resource is incomplete")
  certificate.metadata.name = "<new_certificate_name>"
  update_certificate_operation = await cert_service.update(
      UpdateFederationCertificateRequest(
          metadata=certificate.metadata,
          spec=certificate.spec,
      ),
  )
  await update_certificate_operation.wait()
  ```

* Delete a certificate:

  ```python theme={null}
  cert_service = FederationCertificateServiceClient(sdk)
  delete_certificate_operation = await cert_service.delete(
      DeleteFederationCertificateRequest(id="<certificate_ID>"),
  )
  await delete_certificate_operation.wait()
  ```

  > [!WARNING]
  >
  > A federation cannot function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

For information about adding a new certificate, see [Creating a federation](#creating-a-federation).

> **How to get the certificate ID**
>
> ```python theme={null}
> cert_service = FederationCertificateServiceClient(sdk)
> listed_federation_certificates = (
>     await cert_service.list_by_federation(
>     ListFederationCertificateByFederationRequest(
>         federation_id="<federation_ID>",
>     ),
>     )
> )
> print(listed_federation_certificates)
> ```
>
> The response returns the certificate ID in each item's metadata, accessible as `listed_federation_certificates.items[i].metadata.id`.

**JavaScript SDK**

When changing federation certificates, you can rename or delete a certificate.

* Rename a certificate. The SDK has no partial update call, so get the certificate, change its `metadata.name`, then send the updated metadata and spec back:

  ```ts theme={null}
  const updateCertificateService =
    new FederationCertificateService(sdk);
  const certificateForUpdate = await updateCertificateService.get(
    GetFederationCertificateRequest.create({
      id: "<certificate_ID>",
    }),
  );
  if (!certificateForUpdate.metadata ||
      !certificateForUpdate.spec) {
    throw new Error("certificate resource is incomplete");
  }
  certificateForUpdate.metadata.name = "<new_certificate_name>";
  const updateCertificateOperation =
    await updateCertificateService.update(
      UpdateFederationCertificateRequest.create({
        metadata: certificateForUpdate.metadata,
        spec: certificateForUpdate.spec,
      }),
    ).result;
  await updateCertificateOperation.wait();
  ```

* Delete a certificate:

  ```ts theme={null}
  const deleteCertificateService =
    new FederationCertificateService(sdk);
  const deleteCertificateOperation =
    await deleteCertificateService.delete(
    DeleteFederationCertificateRequest.create({
      id: "<certificate_ID>",
    }),
  ).result;
  await deleteCertificateOperation.wait();
  ```

  > [!WARNING]
  >
  > A federation cannot function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

For information about adding a new certificate, see [Creating a federation](#creating-a-federation).

> **How to get the certificate ID**
>
> ```ts theme={null}
> const listCertificateService =
>   new FederationCertificateService(sdk);
> const listedFederationCertificates =
>   await listCertificateService.listByFederation(
>   ListFederationCertificateByFederationRequest.create({
>     federationId: "<federation_ID>",
>   }),
> );
> console.log(listedFederationCertificates);
> ```
>
> The response returns the certificate ID in each item's metadata, accessible as `listedFederationCertificates.items[i].metadata?.id`.

## Deactivating a federation

When a federation is inactive, users who authenticate through that federation will not be able to sign in to Nebius AI Cloud until it's reactivated.

**Web console**

1. In the sidebar, go to  **Administration** → **IAM**.
2. Go to the **Federations** tab.
3. Next to the federation you want to deactivate, click  → **Deactivate**.

   To reactivate the federation, click  → **Activate**.

**CLI**

To deactivate a federation, run the following command:

```bash theme={null}
nebius iam federation deactivate --federation-id <federation_ID>
```

To activate a federation again, run the following command:

```bash theme={null}
nebius iam federation activate --federation-id <federation_ID>
```

A federation is active by default after you create it. Run the `activate` command only if you deactivated the federation earlier.

> **How to get the federation ID**
>
> ```bash theme={null}
> nebius iam federation list --parent-id <tenant_ID>
> ```
>
> The ID is specified in the `.items.metadata.id` parameter.

**Go SDK**

To deactivate a federation, run the following code:

```go theme={null}
deactivateFederationOperation, err := sdk.Services().IAM().
    V1().Federation().Deactivate(
        ctx,
        &iam.DeactivateFederationRequest{
            FederationId: "<federation_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = deactivateFederationOperation.Wait(ctx); err != nil {
    return err
}
```

To activate a federation again, run the following code:

```go theme={null}
activateFederationOperation, err := sdk.Services().IAM().
    V1().Federation().Activate(
        ctx,
        &iam.ActivateFederationRequest{
            FederationId: "<federation_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = activateFederationOperation.Wait(ctx); err != nil {
    return err
}
```

A federation is active by default after you create it. Run the activation code only if you deactivated the federation earlier.

> **How to get the federation ID**
>
> ```go theme={null}
> listedFederations, err := sdk.Services().IAM().V1().
>     Federation().List(
>     ctx,
>     &iam.ListFederationsRequest{ParentId: "<tenant_ID>"},
> )
> if err != nil {
>     return err
> }
> fmt.Println(listedFederations)
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listedFederations.GetItems()[i].GetMetadata().GetId()`.

**Python SDK**

To deactivate a federation, run the following code:

```python theme={null}
federation_service = FederationServiceClient(sdk)
deactivate_federation_operation = await federation_service.deactivate(
    DeactivateFederationRequest(
        federation_id="<federation_ID>",
    ),
)
await deactivate_federation_operation.wait()
```

To activate a federation again, run the following code:

```python theme={null}
federation_service = FederationServiceClient(sdk)
activate_federation_operation = await federation_service.activate(
    ActivateFederationRequest(
        federation_id="<federation_ID>",
    ),
)
await activate_federation_operation.wait()
```

A federation is active by default after you create it. Run the activation code only if you deactivated the federation earlier.

> **How to get the federation ID**
>
> ```python theme={null}
> federation_service = FederationServiceClient(sdk)
> listed_federations = await federation_service.list(
>     ListFederationsRequest(parent_id="<tenant_ID>"),
> )
> print(listed_federations)
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listed_federations.items[i].metadata.id`.

**JavaScript SDK**

To deactivate a federation, run the following code:

```ts theme={null}
const deactivateFederationService =
  new FederationService(sdk);
const deactivateFederationOperation =
  await deactivateFederationService.deactivate(
    DeactivateFederationRequest.create({
      federationId: "<federation_ID>",
    }),
  ).result;
await deactivateFederationOperation.wait();
```

To activate a federation again, run the following code:

```ts theme={null}
const activateFederationService =
  new FederationService(sdk);
const activateFederationOperation =
  await activateFederationService.activate(
    ActivateFederationRequest.create({
      federationId: "<federation_ID>",
    }),
  ).result;
await activateFederationOperation.wait();
```

A federation is active by default after you create it. Run the activation code only if you deactivated the federation earlier.

> **How to get the federation ID**
>
> ```ts theme={null}
> const listFederationService = new FederationService(sdk);
> const listedFederations = await listFederationService.list(
>   ListFederationsRequest.create({
>     parentId: "<tenant_ID>",
>   }),
> );
> console.log(listedFederations);
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listedFederations.items[i].metadata?.id`.

## Deleting a federation

> [!WARNING]
>
> Deleting a federation cannot be reversed.

**CLI**

To delete a federation, run the following command:

```bash theme={null}
nebius iam federation delete <federation_ID>
```

> **How to get the federation ID**
>
> ```bash theme={null}
> nebius iam federation list --parent-id <tenant_ID>
> ```
>
> The ID is specified in the `.items.metadata.id` parameter.

**Go SDK**

To delete a federation, run the following code:

```go theme={null}
deleteFederationOperation, err := sdk.Services().IAM().
    V1().Federation().Delete(
        ctx,
        &iam.DeleteFederationRequest{
            Id: "<federation_ID>",
        },
    )
if err != nil {
    return err
}
if _, err = deleteFederationOperation.Wait(ctx); err != nil {
    return err
}
```

The code contains the following parameter:

* `Id` in `DeleteFederationRequest`: Federation ID. Use the ID you saved when [creating the federation](#creating-a-federation).

> **How to get the federation ID**
>
> ```go theme={null}
> listedFederations, err := sdk.Services().IAM().V1().
>     Federation().List(
>     ctx,
>     &iam.ListFederationsRequest{ParentId: "<tenant_ID>"},
> )
> if err != nil {
>     return err
> }
> fmt.Println(listedFederations)
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listedFederations.GetItems()[i].GetMetadata().GetId()`.

**Python SDK**

To delete a federation, run the following code:

```python theme={null}
federation_service = FederationServiceClient(sdk)
delete_federation_operation = await federation_service.delete(
    DeleteFederationRequest(id="<federation_ID>"),
)
await delete_federation_operation.wait()
```

The code contains the following parameter:

* `id` in `DeleteFederationRequest`: Federation ID. Use the ID you saved when [creating the federation](#creating-a-federation).

> **How to get the federation ID**
>
> ```python theme={null}
> federation_service = FederationServiceClient(sdk)
> listed_federations = await federation_service.list(
>     ListFederationsRequest(parent_id="<tenant_ID>"),
> )
> print(listed_federations)
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listed_federations.items[i].metadata.id`.

**JavaScript SDK**

To delete a federation, run the following code:

```ts theme={null}
const deleteFederationService = new FederationService(sdk);
const deleteFederationOperation =
  await deleteFederationService.delete(
    DeleteFederationRequest.create({
      id: "<federation_ID>",
    }),
  ).result;
await deleteFederationOperation.wait();
```

The code contains the following parameter:

* `id` in `DeleteFederationRequest`: Federation ID. Use the ID you saved when [creating the federation](#creating-a-federation).

> **How to get the federation ID**
>
> ```ts theme={null}
> const listFederationService = new FederationService(sdk);
> const listedFederations = await listFederationService.list(
>   ListFederationsRequest.create({
>     parentId: "<tenant_ID>",
>   }),
> );
> console.log(listedFederations);
> ```
>
> The response returns the federation ID in each item's metadata, accessible as `listedFederations.items[i].metadata?.id`.
