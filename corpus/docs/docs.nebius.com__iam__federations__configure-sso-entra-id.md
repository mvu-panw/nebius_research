# Configuring single sign-on in Microsoft Entra ID

Source: https://docs.nebius.com/iam/federations/configure-sso-entra-id

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuring single sign-on in Microsoft Entra ID

In this tutorial, you'll learn to configure SSO in Nebius AI Cloud with [Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/whatis).

To configure SSO, you need access to two systems:

* Nebius AI Cloud, where you create and configure a federation.
* Microsoft Entra ID, where you create an application, make it available to the users for whom you configure SSO, and connect the application to the federation.

After the federation and application are set up, users can sign in to Nebius AI Cloud by using their Microsoft Entra ID credentials.

## Costs

This tutorial doesn't include any chargeable resources. The infrastructure you create is free of charge.

## Prerequisites

**Web console**

1. [Create a Microsoft Entra account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount\&WT.mc_id=A261C142F). You can create it for free.
2. Make sure that this account has at least the [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) and [User Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator) roles. Otherwise, [assign them](https://learn.microsoft.com/en-us/entra/fundamentals/users-assign-role-azure-portal#assign-roles).
3. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**CLI**

1. [Install and configure](https://docs.nebius.com/cli/install.md) the Nebius AI Cloud CLI.
2. [Create a Microsoft Entra account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount\&WT.mc_id=A261C142F). You can create it for free.
3. Make sure that this account has at least the [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) and [User Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator) roles. Otherwise, [assign them](https://learn.microsoft.com/en-us/entra/fundamentals/users-assign-role-azure-portal#assign-roles).
4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Terraform**

1. [Install and configure](https://docs.nebius.com/terraform-provider/install.md) the Nebius AI Cloud provider for Terraform.
2. [Create a Microsoft Entra account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount\&WT.mc_id=A261C142F). You can create it for free.
3. Make sure that this account has at least the [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) and [User Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator) roles. Otherwise, [assign them](https://learn.microsoft.com/en-us/entra/fundamentals/users-assign-role-azure-portal#assign-roles).
4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Go SDK**

1. [Install and initialize the Nebius SDK for Go](https://docs.nebius.com/sdk/go/install-auth.md).
2. [Create a Microsoft Entra account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount\&WT.mc_id=A261C142F). You can create it for free.
3. Make sure that this account has at least the [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) and [User Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator) roles. Otherwise, [assign them](https://learn.microsoft.com/en-us/entra/fundamentals/users-assign-role-azure-portal#assign-roles).
4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**Python SDK**

1. [Install and initialize the Nebius SDK for Python](https://docs.nebius.com/sdk/python/install-auth.md).
2. [Create a Microsoft Entra account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount\&WT.mc_id=A261C142F). You can create it for free.
3. Make sure that this account has at least the [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) and [User Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator) roles. Otherwise, [assign them](https://learn.microsoft.com/en-us/entra/fundamentals/users-assign-role-azure-portal#assign-roles).
4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

**JavaScript SDK**

1. [Install and initialize the Nebius SDK for JavaScript](https://docs.nebius.com/sdk/javascript/install-auth.md).
2. [Create a Microsoft Entra account](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount\&WT.mc_id=A261C142F). You can create it for free.
3. Make sure that this account has at least the [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator) and [User Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator) roles. Otherwise, [assign them](https://learn.microsoft.com/en-us/entra/fundamentals/users-assign-role-azure-portal#assign-roles).
4. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.

## Steps

### Create an application in Microsoft Entra ID

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com/).

2. [Create an enterprise application](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal#add-an-enterprise-application):

   1. In the **Browse Microsoft Entra Gallery** window, click **Create your own application**.
   2. In the window that opens, specify the application name and select the option **Integrate any other application you don't find in the gallery (Non-gallery)**.

3. [Create and assign user accounts](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-assign-users) to the application.

4. [Enable SSO](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso#enable-single-sign-on) for the application. On the **SAML-based Sign-on** page, in the **Basic SAML Configuration** section specify the following parameters:

   * **Identifier (Entity ID)**: `https://auth.eu.nebius.com/saml2/rp/federation-id`.
   * **Reply URL (Assertion Consumer Service URL)**: `https://auth.nebius.com/login/saml2/provider/federation-id`.

   > [!NOTE]
   >
   > The two values use different domain names: `auth.eu.nebius.com` and `auth.nebius.com`.

   `federation-id` is used temporarily until you [create a federation](#create-a-federation-in-nebius-ai-cloud) and get its ID. After that, replace `federation-id` with the actual value.

### Download the application certificate from Microsoft Entra

In the Microsoft Entra admin center, download an autogenerated base64 certificate. Find the certificate in the **Manage** → **Single sign-on** section, in the **Certificate (Base64)** field.

For more information, see the [Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/tutorial-manage-certificates-for-federated-single-sign-on#autogenerated-certificate-for-gallery-and-non-gallery-applications) documentation.

### Create a federation in Nebius AI Cloud

1. To create a federation:

   **Web console**

   1. In the sidebar, go to  **Administration** → **IAM**.

   2. Click **Create entity** and select **Federation**.

   3. Enable **Manual mode** and enter your federation name.

   4. Specify the following parameters under **Identity provider (IdP)**:

      * **SSO URL**: Login URL from Microsoft Entra ID.
      * **Issuer**: Microsoft Entra Identifier.

      To get these values:

      1. Open the application page in the Microsoft Entra admin center.
      2. Go to the **Manage** → **Single sign-on** section.
      3. Copy the values of the **Login URL** and **Microsoft Entra Identifier** fields.

   5. Enter a name for your certificate.

   6. Upload the certificate file that you obtained in the [previous step](#download-the-application-certificate-from-microsoft-entra) and click **Create federation**.

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

      * `--saml-settings-sso-url`: Login URL from Microsoft Entra ID.

      * `--saml-settings-idp-issuer`: Microsoft Entra Identifier.

        To get values for `--saml-settings-sso-url` and `--saml-settings-idp-issuer`:

        1. Open the application page in the Microsoft Entra admin center.
        2. Go to the **Manage** → **Single sign-on** section.
        3. Copy the values of the **Login URL** and **Microsoft Entra Identifier** fields.

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
         idp_issuer = "<Microsoft_Entra_Identifier>"
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

      * `saml_settings.sso_url`: Login URL from Microsoft Entra ID.

      * `saml_settings.idp_issuer`: Microsoft Entra Identifier.

        To get values for `saml_settings.sso_url` and `saml_settings.idp_issuer`:

        1. Open the application page in the Microsoft Entra admin center.
        2. Go to the **Manage** → **Single sign-on** section.
        3. Copy the values of the **Login URL** and **Microsoft Entra Identifier** fields.

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
      * `Spec.Settings.SamlSettings.SsoUrl`: Login URL from Microsoft Entra ID.
      * `Spec.Settings.SamlSettings.IdpIssuer`: Microsoft Entra Identifier.

        To get values for `Spec.Settings.SamlSettings.SsoUrl` and `Spec.Settings.SamlSettings.IdpIssuer`:

        1. Open the application page in the Microsoft Entra admin center.
        2. Go to the **Manage** → **Single sign-on** section.
        3. Copy the values of the **Login URL** and **Microsoft Entra Identifier** fields.

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
      * `spec.saml_settings.sso_url`: Login URL from Microsoft Entra ID.
      * `spec.saml_settings.idp_issuer`: Microsoft Entra Identifier.

        To get values for `spec.saml_settings.sso_url` and `spec.saml_settings.idp_issuer`:

        1. Open the application page in the Microsoft Entra admin center.
        2. Go to the **Manage** → **Single sign-on** section.
        3. Copy the values of the **Login URL** and **Microsoft Entra Identifier** fields.

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
      * `spec.settings.samlSettings.ssoUrl`: Login URL from Microsoft Entra ID.
      * `spec.settings.samlSettings.idpIssuer`: Microsoft Entra Identifier.

        To get values for `spec.settings.samlSettings.ssoUrl` and `spec.settings.samlSettings.idpIssuer`:

        1. Open the application page in the Microsoft Entra admin center.
        2. Go to the **Manage** → **Single sign-on** section.
        3. Copy the values of the **Login URL** and **Microsoft Entra Identifier** fields.

   2. Copy and save the federation ID. It is available as `federationOperation.resourceId()` after the operation completes.

2. Change the SAML settings of the application in the Microsoft Entra admin center:

   1. Open the application page.
   2. Go to the **Manage** → **Single sign-on** section.
   3. In the fields **Identifier (Entity ID)** and **Reply URL (Assertion Consumer Service URL)**, replace the `federation-id` part of the values with the copied federation ID.

### Add a certificate to the federation

> [!NOTE]
>
> If you used the [web console](https://console.nebius.com) to create a federation, you can skip this part and proceed to the [next step](#log-in-to-nebius-ai-cloud).

Add the certificate you obtained in the [previous step](#download-the-application-certificate-from-microsoft-entra) to the federation:

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

   Specify the certificate body from the downloaded file and the federation ID.

   In this file, the certificate body is split into several lines. Paste it as a single line in `federation-cert.json`.
2. Apply the certificate file:

   ```bash theme={null}
   nebius iam federation-certificate create --file federation-cert.json
   ```

**Terraform**

1. Prepare a certificate manifest in the same directory where you store the `nebius_iam_v1_federation` resource:
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
   Specify the federation name, ID and the certificate body.
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
   * `certificateData`: The certificate that you downloaded from Microsoft Entra ID. This value is passed as `Spec.Data`.
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
   * `certificate_data`: The certificate that you downloaded from Microsoft Entra ID. This value is passed as `spec.data`.
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
   * `certificateData`: The certificate that you downloaded from Microsoft Entra ID. This value is passed as `spec.data`.
   * `spec.description`: Description of the certificate.

### Log in to Nebius AI Cloud

1. Open the [Nebius AI Cloud web console](https://console.nebius.com).
2. Click **Get started with SSO**.
3. Enter the federation ID and click **Sign in**.
4. In the **Contact details** window that opens:

   1. Specify your name and email.
   2. Confirm that you agree with the [Nebius AI Cloud Terms of Use](https://docs.nebius.com/legal/terms-of-use.md).
   3. Click **Continue**.

A successful login means that you have correctly configured the federation and application in Nebius AI Cloud and Microsoft Entra ID.

### Assign administrator rights for the new account

After your first login to the new federation, a new user account is created in the tenant.

To complete the setup and grant the new user account access to the platform, add it to a group with admin rights in Nebius AI Cloud:

1. Log out of your new account in the [web console](https://console.nebius.com).
2. Log in to your main Nebius AI Cloud account.
3. Go to  **Administration** → **IAM** → **Users** and [add](https://docs.nebius.com/iam/authorization/groups/members.md) the new user to the relevant admin group.
