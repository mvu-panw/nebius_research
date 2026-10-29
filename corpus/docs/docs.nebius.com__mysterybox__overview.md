# About SecretStash

Source: https://docs.nebius.com/mysterybox/overview

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# About SecretStash

> [!NOTE]
>
> MysteryBox is now called SecretStash. The Nebius AI Cloud CLI, API and Terraform provider still use the `mysterybox` service identifier. Keep using `mysterybox` in scripts and manifests.

*SecretStash* is a Nebius AI Cloud service for centralized management of secrets. In the secrets, you can securely store sensitive information, such as API keys, passwords or certificates, in an encrypted form. SecretStash allows you to avoid hardcoding sensitive data, for example, in [Terraform manifests](https://docs.nebius.com/terraform-provider/index.md) or cloud-init scripts. As a result, you eliminate vulnerabilities and maintain compliance with security.

A typical workflow is to [create a secret](https://docs.nebius.com/mysterybox/secrets/create.md) in SecretStash and store sensitive information there. After that, you or a [service account](https://docs.nebius.com/iam/overview.md#accounts-and-members) uses this secret, for instance, in a script, CI/CD pipeline, runtime application or Terraform manifest.

## SecretStash use cases

SecretStash supports integration with different Nebius AI Cloud resources. For instance, you can operate with secrets when working with [Compute virtual machines](https://docs.nebius.com/compute/index.md) (VMs), containers or managed services.

Examples:

* On a Compute VM, you create a script that uses an API key for the application configuration or third-party API access. You save this API key to a SecretStash secret. A service account associated with the given VM launches the script and retrieves the secret with the API key.
* You [create an access key](https://docs.nebius.com/iam/service-accounts/access-keys.md) to authenticate a service account in [Object Storage](https://docs.nebius.com/object-storage/index.md), and you store the secret key in SecretStash.
* When you create a Serverless AI [job](https://docs.nebius.com/serverless/jobs/manage.md) or [endpoint](https://docs.nebius.com/serverless/endpoints/manage.md), you inject SecretStash secrets as environment variables so that API keys and other credentials are not hardcoded in job configs or CI scripts.
* Managed services of Nebius AI Cloud generate passwords and store them in SecretStash secrets.
* You [sync secrets with a Managed Service for Kubernetes® cluster](https://docs.nebius.com/mysterybox/kubernetes.md) as Kubernetes Secrets by using External Secrets Operator, so that applications in the cluster can read the secrets without hardcoding them in manifests.

## Secrets and versions

A *secret* is the main SecretStash resource that stores sensitive data. A secret is located in a [project](https://docs.nebius.com/iam/overview.md#projects), but user and service accounts can access the secret within the [region](https://docs.nebius.com/overview/regions.md) if the accounts have corresponding permissions. User and service accounts of different regions cannot access the secret.

A secret can have multiple versions. A *version* is a snapshot of stored data. You cannot modify this snapshot once it is [created](https://docs.nebius.com/mysterybox/secrets/create-version.md).

A secret has a *primary version*. When you retrieve a secret and do not specify a particular version, SecretStash provides you with the primary one. By default, this is the latest version unless you [explicitly set the primary version](https://docs.nebius.com/mysterybox/secrets/make-version-primary.md).

Every version contains the *payload* of a secret. The payload consists of one or several key-value pairs. When you create a secret, you put data there in the key-value format. A key identifies the entry, and a value contains sensitive data that can be in the form of a string or a binary file.
