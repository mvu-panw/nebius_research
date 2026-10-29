# Configuring single sign-on with a SAML identity provider

Source: https://docs.nebius.com/iam/federations/configure-sso-saml

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuring single sign-on with a SAML identity provider

In this tutorial, you'll learn to configure single sign-on (SSO) in Nebius AI Cloud with an identity provider that supports SAML 2.0.

The names of settings and sections depend on the identity provider, but the SAML values that Nebius AI Cloud requires are the same.

To configure SSO, you need access to two systems:

* Nebius AI Cloud, where you create and configure a federation.
* An identity provider, where you create a SAML application, make it available to the users for whom you configure SSO and connect it to the federation.

After the federation and SAML application are set up, users can sign in to Nebius AI Cloud by using their identity provider credentials.

## Costs

This tutorial doesn't include any chargeable resources. The infrastructure you create is free of charge.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. Make sure that you have access to an identity provider that supports SAML 2.0 and permissions to create and configure SAML applications.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to an identity provider that supports SAML 2.0 and permissions to create and configure SAML applications.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to an identity provider that supports SAML 2.0 and permissions to create and configure SAML applications.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to an identity provider that supports SAML 2.0 and permissions to create and configure SAML applications.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to an identity provider that supports SAML 2.0 and permissions to create and configure SAML applications.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. Make sure that you have access to an identity provider that supports SAML 2.0 and permissions to create and configure SAML applications.

## Steps

### Create a SAML application in the identity provider

1. Sign in to your identity provider's admin console.

2. Create a SAML 2.0 application or client for Nebius AI Cloud.

   In the application settings, specify the following required parameters. The names of these parameters can differ depending on the identity provider:

   * **Service Provider (SP) Entity ID**, **Audience URI** or **Identifier**: `https://auth.eu.nebius.com/saml2/rp/federation-id`
   * **Assertion Consumer Service (ACS) URL**, **Reply URL** or **Single sign-on URL**: `https://auth.nebius.com/login/saml2/provider/federation-id`
   * **Name ID format**: `Unspecified`, if your identity provider requires this parameter.

   > [!NOTE]
   >
   > The two values use different domain names: `auth.eu.nebius.com` and `auth.nebius.com`.
   >
   > `federation-id` is used temporarily until you [create a federation](#create-a-federation-in-nebius-ai-cloud) and get its ID. After that, replace `federation-id` with the actual value.

3. If your identity provider lets you configure SAML response settings, use HTTP POST binding, include an AuthnStatement, enable signed responses or assertions and select the `RSA-SHA256` signature algorithm.

4. Make the application available to the users who need SSO access to Nebius AI Cloud.

### Get SAML settings from the identity provider

1. In the identity provider's admin console, open the SAML application or SAML configuration that you created in the [previous step](#create-a-saml-application-in-the-identity-provider).
2. Get the values that you need to create a federation:

   * To create the federation in the web console by uploading metadata, download or open the SAML metadata XML file.

     If the metadata opens in a browser tab, save the page as an XML file.

   * To create the federation manually in the web console, CLI, Terraform or SDK, copy the SSO URL and issuer from the application settings and download the SAML signing certificate. If your identity provider provides only a metadata XML file, use it to get the SSO URL, issuer and certificate body.

### Create a federation in Nebius AI Cloud

1. To create a federation:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.

   2. Click **Create entity** and select **Federation**.

   3. Enter your federation name.

   4. If you have a metadata file, click **Upload file**, select the XML file that you downloaded in the [previous step](#get-saml-settings-from-the-identity-provider) and click **Continue**.

   5. If you don't have a metadata file, enable **Manual mode** and specify the following parameters under **Identity provider (IdP)**:

      * **SSO URL**: Identity provider login URL.
      * **Issuer**: Identity provider issuer or identifier.

   6. Enter a name for your certificate in the **Certificates** section.

      If you created the federation in manual mode, upload the SAML signing certificate from your identity provider.

   7. Click **Create federation**.

      Copy the ID of the newly created federation.

   **CLI**

   1. Run the following command:

      ```bash theme={null}
      nebius iam federation create \
        --parent-id <tenant_ID> \
        --name <federation_name> \
        --user-account-auto-creation=true \
        --saml-settings-sso-url <login_URL> \
        --saml-settings-idp-issuer <identity_provider_identifier>
      ```

      The command contains the following parameters:

      * `--parent-id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).

      * `--name`: The federation name.

      * `--user-account-auto-creation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `--saml-settings-sso-url`: Identity provider login URL.

      * `--saml-settings-idp-issuer`: Identity provider issuer or identifier.

        Use the SSO URL and issuer that you copied from the application settings.

        If your identity provider provides only a metadata XML file, get the values from it:

        1. Open the XML file with metadata that you downloaded or opened in the [previous step](#get-saml-settings-from-the-identity-provider).

        2. In the `EntityDescriptor` element, find the `entityID` attribute and use its value for `--saml-settings-idp-issuer`.

        3. In one of the `SingleSignOnService` elements, find the `Location` parameter and use its value for `--saml-settings-sso-url`.

   2. Copy and save the federation ID. It is returned in the `metadata.id` field of the command output.

   **Terraform**

   1. Create the following configuration file:

      ```hcl theme={null}
      resource "nebius_iam_v1_federation" "<federation_name>" {
        name                       = "<federation_name>"
        parent_id                  = "<tenant_ID>"
        user_account_auto_creation = true
        saml_settings = {
          sso_url    = "<login_URL>"
          idp_issuer = "<identity_provider_identifier>"
        }
      }

      output "federation_id" {
        description = "ID of the created federation"
        value = nebius_iam_v1_federation.<federation_name>.id
      }
      ```

      The file contains a resource with federation settings and an output that returns the federation ID. The resource contains the following parameters:

      * `name`: The federation name.

      * `parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md).

      * `user_account_auto_creation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `saml_settings.sso_url`: Identity provider login URL.

      * `saml_settings.idp_issuer`: Identity provider issuer or identifier.

        Use the SSO URL and issuer that you copied from the application settings.

        If your identity provider provides only a metadata XML file, get the values from it:

        1. Open the XML file with metadata that you downloaded or opened in the [previous step](#get-saml-settings-from-the-identity-provider).

        2. In the `EntityDescriptor` element, find the `entityID` attribute and use its value for `saml_settings.idp_issuer`.

        3. In one of the `SingleSignOnService` elements, find the `Location` parameter and use its value for `saml_settings.sso_url`.

   2. Check that the configuration is correct:
      ```bash theme={null}
      terraform validate
      ```

   3. Apply the changes:
      ```bash theme={null}
      terraform apply
      ```

   4. Copy and save the federation ID. It is returned in the `terraform apply` output:

      ```text theme={null}
      Outputs:

      federation_id = "federation-e00*******"
      ```

   **Go SDK**

   1. Run the following code:

      ```go theme={null}
      federationOp, err := sdk.Services().IAM().V1().
          Federation().Create(
              ctx,
              &iam.CreateFederationRequest{
                  Metadata: &common.ResourceMetadata{
                      ParentId: "<tenant_ID>",
                      Name:     "<federation_name>",
                  },
                  Spec: &iam.FederationSpec{
                      UserAccountAutoCreation: true,
                      Settings: &iam.FederationSpec_SamlSettings{
                          SamlSettings: &iam.SamlSettings{
                              SsoUrl: "<login_URL>",
                              IdpIssuer: "<identity_provider_identifier>",
                          },
                      },
                  },
              },
          )
      if err != nil {
          return err
      }
      if _, err = federationOp.Wait(ctx); err != nil {
          return err
      }
      ```

      In the code, set the following parameters:

      * `Metadata.ParentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#go-sdk-2).
      * `Metadata.Name`: The federation name.
      * `Spec.UserAccountAutoCreation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.
      * `Spec.Settings.SamlSettings.SsoUrl`: Identity provider login URL.
      * `Spec.Settings.SamlSettings.IdpIssuer`: Identity provider issuer or identifier.

        Use the SSO URL and issuer that you copied from the application settings.

        If your identity provider provides only a metadata XML file, get the values from it:

        1. Open the XML file with metadata that you downloaded or opened in the [previous step](#get-saml-settings-from-the-identity-provider).

        2. In the `EntityDescriptor` element, find the `entityID` attribute and use its value for `Spec.Settings.SamlSettings.IdpIssuer`.

        3. In one of the `SingleSignOnService` elements, find the `Location` parameter and use its value for `Spec.Settings.SamlSettings.SsoUrl`.

   2. Copy and save the federation ID. It is available as `federationOp.ResourceID()` after the operation completes.

   **Python SDK**

   1. Run the following code:

      ```python theme={null}
      federation_service = FederationServiceClient(sdk)
      federation_operation = await federation_service.create(
          CreateFederationRequest(
              metadata=ResourceMetadata(
                  parent_id="<tenant_ID>",
                  name="<federation_name>",
              ),
              spec=FederationSpec(
                  user_account_auto_creation=True,
                  saml_settings=SamlSettings(
                      sso_url="<login_URL>",
                      idp_issuer="<identity_provider_identifier>",
                  ),
              ),
          ),
      )
      await federation_operation.wait()
      ```

      In the code, set the following parameters:

      * `metadata.parent_id`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#python-sdk-2).
      * `metadata.name`: The federation name.
      * `spec.user_account_auto_creation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.
      * `spec.saml_settings.sso_url`: Identity provider login URL.
      * `spec.saml_settings.idp_issuer`: Identity provider issuer or identifier.

        Use the SSO URL and issuer that you copied from the application settings.

        If your identity provider provides only a metadata XML file, get the values from it:

        1. Open the XML file with metadata that you downloaded or opened in the [previous step](#get-saml-settings-from-the-identity-provider).

        2. In the `EntityDescriptor` element, find the `entityID` attribute and use its value for `spec.saml_settings.idp_issuer`.

        3. In one of the `SingleSignOnService` elements, find the `Location` parameter and use its value for `spec.saml_settings.sso_url`.

   2. Copy and save the federation ID. It is available as `federation_operation.resource_id` after the operation completes.

   **JavaScript SDK**

   1. Run the following code:

      ```ts theme={null}
      const federationService = new FederationService(sdk);
      const federationOperation = await federationService.create(
        CreateFederationRequest.create({
          metadata: ResourceMetadata.create({
            parentId: "<tenant_ID>",
            name: "<federation_name>",
          }),
          spec: FederationSpec.create({
            userAccountAutoCreation: true,
            settings: {
              $case: "samlSettings",
              samlSettings: SamlSettings.create({
                ssoUrl: "<login_URL>",
                idpIssuer: "<identity_provider_identifier>",
              }),
            },
          }),
        }),
      ).result;
      await federationOperation.wait();
      ```

      In the code, set the following parameters:

      * `metadata.parentId`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#javascript-sdk-2).
      * `metadata.name`: The federation name.
      * `spec.userAccountAutoCreation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.
      * `spec.settings.samlSettings.ssoUrl`: Identity provider login URL.
      * `spec.settings.samlSettings.idpIssuer`: Identity provider issuer or identifier.

        Use the SSO URL and issuer that you copied from the application settings.

        If your identity provider provides only a metadata XML file, get the values from it:

        1. Open the XML file with metadata that you downloaded or opened in the [previous step](#get-saml-settings-from-the-identity-provider).

        2. In the `EntityDescriptor` element, find the `entityID` attribute and use its value for `spec.settings.samlSettings.idpIssuer`.

        3. In one of the `SingleSignOnService` elements, find the `Location` parameter and use its value for `spec.settings.samlSettings.ssoUrl`.

   2. Copy and save the federation ID. It is available as `federationOperation.resourceId()` after the operation completes.

2. Update the SAML settings of the application in your identity provider:

   1. Open the SAML application or client that you created in the [previous step](#create-a-saml-application-in-the-identity-provider).
   2. In the fields where you specified the Nebius AI Cloud SP entity ID and ACS URL, replace the `federation-id` part of the values with the copied federation ID.

### Add a certificate to the federation

Make sure the federation has the signing certificate from the identity provider:

**Web console**

If you created the federation in the web console, no extra certificate step is required.

To manage certificates for an existing federation:

1. In the sidebar, go to  **Administration** → **IAM**.
2. Go to the **Federations** tab and open the federation.
3. On the **Certificates** tab:

   * Rename or delete a certificate.

     > [!WARNING]
     >
     > A federation can't function correctly without at least one valid certificate. If you need to delete the only certificate attached to the federation, be sure to replace it with a new one.

   * Add a new certificate:

     1. Click **Attach certificate**.
     2. Enter a certificate name, then either upload the PEM certificate file, or copy and paste the certificate body into the field.
     3. Click **Attach certificates**.

**CLI**

1. Prepare the `federation-cert.json` file:

   ```json theme={null}
   {
      "metadata": {
         "parent_id": "<federation_ID>"
      },
      "spec": {
         "description": "certificate for a federation",
         "data": "-----BEGIN CERTIFICATE-----\n<certificate_body>\n-----END CERTIFICATE-----\n"
      }
   }
   ```

   Specify the federation ID and the certificate body from the downloaded metadata XML file or certificate file.

   In a metadata XML file, the certificate body is stored in the `X509Certificate` element. Paste it as a single line to `federation-cert.json`.

2. Apply the certificate file:

   ```bash theme={null}
   nebius iam federation-certificate create --file federation-cert.json
   ```

**Terraform**

1. Prepare the certificate file in the same directory where you [store](#create-a-federation-in-nebius-ai-cloud) the `nebius_iam_v1_federation` resource:

   ```hcl theme={null}
   resource "nebius_iam_v1_federation_certificate" "certificate-for-<federation_name>" {
      parent_id   = "<federation_ID>"
      name        = "certificate"
      data        = <<EOT
   -----BEGIN CERTIFICATE-----
   <certificate_body>
   -----END CERTIFICATE-----
   EOT
      description = "certificate for a federation"
      depends_on = [
         nebius_iam_v1_federation.<federation_name>
      ]
   }
   ```

   Specify the following:

   * Federation name
   * Federation ID
   * Certificate body from the downloaded metadata XML file or certificate file

     In a metadata XML file, the certificate body is stored in the `X509Certificate` element.

2. Check that the configuration is correct:
   ```bash theme={null}
   terraform validate
   ```

3. Apply the changes:
   ```bash theme={null}
   terraform apply
   ```

**Go SDK**

1. Run the following code:

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

   In the code, set the following parameters:

   * `Metadata.ParentId`: Federation ID that you obtained when [creating the federation](#create-a-federation-in-nebius-ai-cloud).
   * `certificateData`: The certificate body from the downloaded metadata XML file or certificate file, wrapped in `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`. This value is passed as `Spec.Data`.
   * `Spec.Description`: Description of the certificate.

**Python SDK**

1. Run the following code:

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

   In the code, set the following parameters:

   * `metadata.parent_id`: Federation ID that you obtained when [creating the federation](#create-a-federation-in-nebius-ai-cloud).
   * `certificate_data`: The certificate body from the downloaded metadata XML file or certificate file, wrapped in `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`. This value is passed as `spec.data`.
   * `spec.description`: Description of the certificate.

**JavaScript SDK**

1. Run the following code:

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

   In the code, set the following parameters:

   * `metadata.parentId`: Federation ID that you obtained when [creating the federation](#create-a-federation-in-nebius-ai-cloud).
   * `certificateData`: The certificate body from the downloaded metadata XML file or certificate file, wrapped in `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`. This value is passed as `spec.data`.
   * `spec.description`: Description of the certificate.

### Log in to Nebius AI Cloud

1. Open the [Nebius AI Cloud web console](https://console.nebius.com).
2. Click **Get started with SSO**.
3. Enter the federation ID and click **Sign in**.
4. In the **Contact details** window that opens:

   1. Specify your name and email.
   2. Confirm that you agree with the [Nebius AI Cloud Terms of Use](https://docs.nebius.com/legal/terms-of-use.md).
   3. Click **Continue**.

A successful login means that you have correctly configured the federation and the SAML application in Nebius AI Cloud and your identity provider.

### Assign administrator rights for the new account

After your first login to the new federation, a new user account is created in the tenant.

To complete the setup and grant the new user account access to the platform, add it to a group with admin rights in Nebius AI Cloud:

1. Log out of your new account in the [web console](https://console.nebius.com).
2. Log in to your main Nebius AI Cloud account.
3. Go to  **Administration** → **IAM** → **Users** and [add](https://docs.nebius.com/iam/authorization/groups/members.md) the new user to the relevant admin group.
