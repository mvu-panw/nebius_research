# Configuring single sign-on in Okta

Source: https://docs.nebius.com/iam/federations/configure-sso-okta

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuring single sign-on in Okta

In this tutorial, you'll learn to configure SSO in Nebius AI Cloud with [Okta](https://www.okta.com/).

To configure SSO, you need access to two systems:

* Nebius AI Cloud, where you create and configure a federation.
* Okta, where you create an application, make it available to the users for whom you configure SSO, and connect the application to the federation.

After the federation and application are set up, users can sign in to Nebius AI Cloud by using their Okta credentials.

## Costs

This tutorial doesn't include any chargeable resources. The infrastructure you create is free of charge.

## Prerequisites

**Web console**

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. [Create an Okta account](https://www.okta.com/free-trial/).

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create an Okta account](https://www.okta.com/free-trial/).

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create an Okta account](https://www.okta.com/free-trial/).

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create an Okta account](https://www.okta.com/free-trial/).

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create an Okta account](https://www.okta.com/free-trial/).

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
3. [Create an Okta account](https://www.okta.com/free-trial/).

## Steps

### Create an application in Okta

1. Sign in to the Okta admin console.

2. [Create and configure a new application](https://help.okta.com/oie/en-us/content/topics/apps/apps_app_integration_wizard_saml.htm):

   1. Go to **Applications** → **Applications** and click **Create App Integration**.

   2. In the window that opens, select **SAML 2.0** and click **Next**.

   3. On the **General settings** step, enter a name in the **App name** field. You can optionally upload a logo for your app.

   4. Click **Next** to proceed to the **Configure SAML** step and specify the following parameters:

      * **Single sign-on URL**: `https://auth.nebius.com/login/saml2/provider/federation-id`
      * **Audience URI (SP Entity ID)**: `https://auth.eu.nebius.com/saml2/rp/federation-id`
      * **Name ID format**: `Unspecified`
      * **Application username**: `Okta username`

        > [!NOTE]
        >
        > `federation-id` is used temporarily until you [create a federation](#create-a-federation-in-nebius-ai-cloud) and get its ID. After that, replace `federation-id` with the actual value.

   5. Click **Next** to proceed to the **Feedback** step and select the **This is an internal app that we have created** checkbox next to **App type**.

   6. Click **Finish** to create the application.

3. [Create users](https://help.okta.com/oie/en-us/content/topics/users-groups-profiles/usgp-add-users.htm), [assign users to a group](https://help.okta.com/oie/en-us/content/topics/users-groups-profiles/usgp-assign-group-people.htm) and then [assign the group to your application](https://help.okta.com/oie/en-us/content/topics/users-groups-profiles/usgp-assign-app-group.htm).

### Download the IdP metadata file from Okta

1. Go to your application page in the Okta admin console.

2. Switch to the **Sign On** tab and find the **SAML Signing Certificates** section.

3. Click **Actions** → **View IdP metadata** next to the currently active certificate.

   If there are no active certificates, click **Generate new certificate** to create one.

4. On the browser tab that opens, save the XML file with metadata (for example, by using **Command** + **S** on macOS or **Ctrl** + **S** on Windows).

   To download the certificate without metadata, use **Actions** → **Download certificate**.

### Create a federation in Nebius AI Cloud

1. To create a federation:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.

   2. Click **Create entity** and select **Federation**.

   3. Enter your federation name and click **Upload file**.

   4. Select the XML file you saved in the [previous step](#download-the-idp-metadata-file-from-okta) and click **Continue**.

   5. Enter a name for your certificate in the **Certificates** section and click **Create federation**.

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

      * `--parent-id`: The ID of the tenant where you are going to create a federation.

        To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

      * `--name`: The federation name.

      * `--user-account-auto-creation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `--saml-settings-sso-url`: Okta login URL.

      * `--saml-settings-idp-issuer`: Okta identifier.

        To get values for `--saml-settings-sso-url` and `--saml-settings-idp-issuer`:

        1. Open the XML file with metadata that you saved in the [previous step](#download-the-idp-metadata-file-from-okta).

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
          idp_issuer = "<Okta_identifier>"
        }
      }

      output "federation_id" {
        description = "ID of the created federation"
        value = nebius_iam_v1_federation.<federation_name>.id
      }
      ```

      The file contains a resource with federation settings and an output that returns the federation ID. The resource contains the following parameters:

      * `name`: The federation name.

      * `parent_id`: The ID of the tenant where you are going to create a federation.

        To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

      * `user_account_auto_creation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `saml_settings.sso_url`: Okta login URL.

      * `saml_settings.idp_issuer`: Okta identifier.

        To get values for `saml_settings.sso_url` and `saml_settings.idp_issuer`:

        1. Open the XML file with metadata that you saved in the [previous step](#download-the-idp-metadata-file-from-okta).

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

      * `Metadata.ParentId`: The ID of the tenant where you are going to create a federation.

        To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

      * `Metadata.Name`: The federation name.

      * `Spec.UserAccountAutoCreation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `Spec.Settings.SamlSettings.SsoUrl`: Okta login URL.

      * `Spec.Settings.SamlSettings.IdpIssuer`: Okta identifier.

        To get values for `Spec.Settings.SamlSettings.SsoUrl` and `Spec.Settings.SamlSettings.IdpIssuer`:

        1. Open the XML file with metadata that you saved in the [previous step](#download-the-idp-metadata-file-from-okta).

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

      * `metadata.parent_id`: The ID of the tenant where you are going to create a federation.

        To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

      * `metadata.name`: The federation name.

      * `spec.user_account_auto_creation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `spec.saml_settings.sso_url`: Okta login URL.

      * `spec.saml_settings.idp_issuer`: Okta identifier.

        To get values for `spec.saml_settings.sso_url` and `spec.saml_settings.idp_issuer`:

        1. Open the XML file with metadata that you saved in the [previous step](#download-the-idp-metadata-file-from-okta).

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

      * `metadata.parentId`: The ID of the tenant where you are going to create a federation.

        To get the tenant ID, go to the [web console](https://console.nebius.com) and expand the list of tenants. Next to the tenant’s name, click  → **Copy tenant ID**.

      * `metadata.name`: The federation name.

      * `spec.userAccountAutoCreation`: When the user signs in to Nebius AI Cloud via SSO, their account is automatically created in the tenant with the configured federation.

      * `spec.settings.samlSettings.ssoUrl`: Okta login URL.

      * `spec.settings.samlSettings.idpIssuer`: Okta identifier.

        To get values for `spec.settings.samlSettings.ssoUrl` and `spec.settings.samlSettings.idpIssuer`:

        1. Open the XML file with metadata that you saved in the [previous step](#download-the-idp-metadata-file-from-okta).

        2. In the `EntityDescriptor` element, find the `entityID` attribute and use its value for `spec.settings.samlSettings.idpIssuer`.

        3. In one of the `SingleSignOnService` elements, find the `Location` parameter and use its value for `spec.settings.samlSettings.ssoUrl`.

   2. Copy and save the federation ID. It is available as `federationOperation.resourceId()` after the operation completes.

2. Update the SAML settings of your application in the Okta admin console:

   1. Open the application page and go to the **General** tab.
   2. In the **SAML Settings** section, click **Edit** and go to the **Configure SAML** step.
   3. In the fields **Single sign-on URL** and **Audience URI (SP Entity ID)**, replace the `federation-id` part of the values with the copied federation ID.

### Add a certificate to the federation

> [!NOTE]
>
> If you used the [web console](https://console.nebius.com) to create a federation, you can skip this part and proceed to the [next step](#log-in-to-nebius-ai-cloud).

Add the certificate from the metadata file you obtained in the [previous step](#download-the-idp-metadata-file-from-okta) to the federation:

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

   Specify the federation ID and the certificate body from the downloaded XML file.

   In this file, the certificate body is stored in the `X509Certificate` element. Paste it as a single line to `federation-cert.json`.

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
   * Certificate body from the downloaded XML file

     In this file, the certificate body is stored in the `X509Certificate` element.

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
   * `certificateData`: The certificate body from the `X509Certificate` element of the downloaded metadata file, wrapped in `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`. This value is passed as `Spec.Data`.
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
   * `certificate_data`: The certificate body from the `X509Certificate` element of the downloaded metadata file, wrapped in `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`. This value is passed as `spec.data`.
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
   * `certificateData`: The certificate body from the `X509Certificate` element of the downloaded metadata file, wrapped in `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`. This value is passed as `spec.data`.
   * `spec.description`: Description of the certificate.

### Log in to Nebius AI Cloud

1. Open the [Nebius AI Cloud web console](https://console.nebius.com).
2. Click **Get started with SSO**.
3. Enter the federation ID and click **Sign in**.
4. In the **Contact details** window that opens:

   1. Specify your name and email.
   2. Confirm that you agree with the [Nebius AI Cloud Terms of Use](https://docs.nebius.com/legal/terms-of-use.md).
   3. Click **Continue**.

A successful login means that you have correctly configured the federation and application in Nebius AI Cloud and Okta.

### Assign administrator rights for the new account

After your first login to the new federation, a new user account is created in the tenant.

To complete the setup and grant the new user account access to the platform, add it to a group with admin rights in Nebius AI Cloud:

1. Log out of your new account in the [web console](https://console.nebius.com).
2. Log in to your main Nebius AI Cloud account.
3. Go to  **Administration** → **IAM** → **Users** and [add](https://docs.nebius.com/iam/authorization/groups/members.md) the new user to the relevant admin group.
