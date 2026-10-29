# Nebius AI Cloud changelog

Source: https://docs.nebius.com/changelog

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Nebius AI Cloud changelog

This article lists what has been added, updated, fixed or removed in Nebius AI Cloud services.

**October 19–25, 2026**

* *Added:* Spot prices of preemptible GPU platforms are now public. You can [view current spot prices and their history](https://docs.nebius.com/signup-billing/spot-prices.md) on the Nebius website or through the API without an account, or in the web console or CLI if you have an account. Price history is available for up to 30 days. Use it to choose a region with a lower price or to set the max price for a pricing policy.
* *Added:* You can now [restart Serverless AI endpoints](https://docs.nebius.com/serverless/maintenance/stop-start.md#endpoints) in the web console, CLI or API. A stopped or restarted endpoint keeps its public HTTPS URL and IP address, but data on its disk isn't preserved. Endpoints on preemptible VMs that Nebius AI Cloud stops get the `Preempted` [code](https://docs.nebius.com/serverless/lifecycle.md#endpoint-statuses), and you can start them again.
* *Updated:* Starting November 2, 2026, [support ticket priorities](https://docs.nebius.com/overview/support.md#priorities-and-response-times) are Medium (4 hours to first response) and Low (1 business day). Customers with a committed volume of services signed by November 1, 2026, keep the current priorities and response times for the duration of their contracts.
* *Updated:* Starting November 2, 2026, the [Managed Service for Kubernetes® SLA](https://docs.nebius.com/legal/sla-levels/managed-kubernetes.md) doesn't apply to clusters running a Kubernetes version that has reached end of life, or to unavailability caused by modifying preinstalled add-ons outside the public API. Nebius gives at least 30 days' notice before a supported version reaches end of life.
* *Updated:* Token Factory fees are now [post-paid](https://docs.nebius.com/legal/token-factory.md). For committed GPU capacity reservations, Nebius AI Cloud [stops your VMs](https://docs.nebius.com/legal/agreement.md) no earlier than one hour before the reservation ends.
* *Removed:* Standalone applications and Container VMs are no longer available. To run third-party software such as JupyterLab, ComfyUI and Qdrant, [deploy applications](https://docs.nebius.com/applications/index.md) on Managed Service for Kubernetes clusters. For hosted interactive environments without a cluster, use [Serverless AI Devlabs](https://docs.nebius.com/serverless/devlabs/manage.md).

**October 12–18, 2026**

* *Added:* [Cloud Shell](https://docs.nebius.com/cli/cloud-shell.md) is now available in preview. It's a browser-based terminal in the web console with the Nebius AI Cloud CLI, Terraform, Git and Python preinstalled, and the CLI is already authenticated with your user account. Sessions last up to one hour.
* *Added:* You can now [postpone node drain for CPU Pods](https://docs.nebius.com/kubernetes/maintenance/manage.md#how-to-postpone-node-drain-for-cpu-pods) during Managed Service for Kubernetes® maintenance. Assign the `nebius.com/defer-maintenance-node-drain: "true"` label to the Pods, and Managed Kubernetes waits for them to finish until one hour before the SLA deadline.
* *Added:* New tutorial: [receive webhooks in a private service](https://docs.nebius.com/tunnels/tutorials/webhook.md) by using Nebius Tunnels. Webhook providers such as GitHub, Stripe and Telegram can reach a handler on a VM without a public IP address or open inbound ports.
* *Updated:* Serverless AI is now [available](https://docs.nebius.com/overview/regions.md) in the `eu-south1` and `us-north1` regions.
* *Updated:* Nebius Tunnels is now available in all regions and has higher [traffic limits](https://docs.nebius.com/tunnels/resources/quotas-limits.md): 120 Mbps per tunnel, 600 Mbps per project and 8 Gbps per region, for inbound and outbound traffic combined. Client connection limits now apply to new connections per second. Managed public URLs of Serverless AI endpoints get [120 Mbps and 300 new connections per second](https://docs.nebius.com/serverless/endpoints/manage.md#traffic-and-connection-limits) per endpoint.
* *Updated:* The [quota](https://docs.nebius.com/object-storage/resources/quotas-limits.md#quotas) for the total size of objects in Enhanced Throughput storage is now 10 TiB in all regions.
* *Updated:* Serverless AI [jobs](https://docs.nebius.com/serverless/jobs/manage.md#how-to-create-a-job), [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md#how-to-create-an-endpoint) and [Devlabs](https://docs.nebius.com/serverless/devlabs/manage.md#how-to-create-a-devlab) require a container disk of at least 50 GiB for GPU workloads or 20 GiB for CPU-only workloads, or more if the container image requires it. Otherwise, the workloads can't launch.

**October 5–11, 2026**

* *Added:* Compute documentation now includes how to [change the preset of an existing VM](https://docs.nebius.com/compute/virtual-machines/update.md#preset) to give it more or fewer vCPUs and RAM. You need to stop the VM to change its preset.
* *Added:* You can now [use several shared filesystems](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md#how-to-use-several-shared-filesystems) with one CSI driver installation in Managed Service for Kubernetes®. Each filesystem gets its own storage class.
* *Added:* Serverless AI documentation now includes [traffic and connection limits](https://docs.nebius.com/serverless/endpoints/manage.md#traffic-and-connection-limits) of managed public URLs of endpoints per endpoint, project and region. When usage reaches a limit, responses may slow down.
* *Updated:* Starting October 8, 2026, preemptible VMs with NVIDIA B300, B200, H200, H100 and RTX PRO 6000 GPUs use [spot pricing](https://docs.nebius.com/compute/resources/pricing.md#price-changes-in-october-2026). Pricing tables show the minimum spot price. You can now [get the current spot price](https://docs.nebius.com/signup-billing/manage-pricing-policy.md#how-to-create-a-pricing-policy) for a platform and preset in the CLI before you create a pricing policy.
* *Updated:* For buckets created on or after November 9, 2026, Object Storage [automatically deletes incomplete multipart uploads](https://docs.nebius.com/object-storage/objects/lifecycles.md#automatic-deletion-of-incomplete-uploads) after 30 days. To change this behavior, create an expiration lifecycle rule that aborts incomplete multipart uploads.

**September 28 — October 4, 2026**

* *Added:* You can now [connect Wiz to Nebius AI Cloud](https://docs.nebius.com/3p-integrations/wiz.md) to scan the configuration of your Compute, Managed Service for Kubernetes®, Virtual Networks and Object Storage resources for misconfigurations.
* *Added:* The new `security-auditor` [security role](https://docs.nebius.com/iam/authorization/roles.md#security) grants read-only access to the configuration of resources across all services, without granting access to the data in them. Use it for third-party security and compliance platforms.
* *Added:* The new `ubuntu24.04-cuda13-latest` [boot disk image family](https://docs.nebius.com/compute/storage/boot-disk-images.md#images-for-gpu-vms) for GPU VMs is regularly updated to the latest GPU driver and CUDA 13.x versions. For fixed versions, use the stable `ubuntu24.04-cuda13.0` family.
* *Added:* The new `applicationtunnel.agent` [Nebius Tunnels role](https://docs.nebius.com/iam/authorization/roles.md#nebius-tunnels) lets service accounts connect tunnel agents to tunnels. You can now [run the Nebius Tunnels agent on a VM](https://docs.nebius.com/tunnels/tutorials/connect-vm.md) that authenticates by using the VM's attached service account, without creating or copying service account keys.
* *Updated:* Starting October 1, 2026, [Compute prices](https://docs.nebius.com/compute/resources/pricing.md#price-changes-in-october-2026) changed for VMs with NVIDIA B300, B200, H200 and H100 GPUs, for vCPUs and RAM on the Non-GPU AMD EPYC Genoa platform and for RAM on the Non-GPU Intel Ice Lake platform. Prices for [standalone applications](https://docs.nebius.com/applications/standalone/pricing.md#gpu-prices-from-october-1-2026) with NVIDIA H200 and H100 GPUs changed as well.
* *Updated:* Egress traffic from the Intelligent storage class in Object Storage is [free](https://docs.nebius.com/object-storage/resources/pricing.md) while it's less than three times the monthly average used storage capacity. When egress traffic reaches or exceeds this threshold, charges apply and bandwidth may be limited.
* *Updated:* The Nebius AI Cloud CLI [installation script](https://docs.nebius.com/cli/install.md) is now downloaded from `https://artifacts.nebius.cloud/cli/install.sh`.
* *Updated:* The [instance metadata service](https://docs.nebius.com/compute/virtual-machines/instance-metadata.md#how-to-access-imds) now returns `403 Forbidden` for requests containing the `X-Forwarded-For`, `X-Forwarded-Host`, `X-Real-IP` or `Forwarded` headers.
* *Updated:* You can now set the [disk block size](https://docs.nebius.com/kubernetes/storage/disk-over-csi.md#create-a-storage-class-for-custom-provisioning-optional) for disks provisioned over CSI in Managed Service for Kubernetes by setting the `disk_block_size_bytes` storage class parameter. Use a larger block size for disks over 16 TiB.
* *Updated:* [Nebius Observability Agent v1.0.9](https://docs.nebius.com/observability/resources/nebius-o11y-agent-changelog.md) now sends metrics from Managed Service for Kubernetes add-ons, such as Cilium and Hubble, to Observability Metrics.

**September 21–27, 2026**

* *Added:* [Spot pricing](https://docs.nebius.com/signup-billing/pricing-policy.md) now applies to preemptible VMs and services that run on them. Nebius sets a current spot price for each preemptible GPU platform, which can change every 15 minutes. When you create a preemptible resource, select a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md) to cap the maximum price, or choose **Follow spot price**. Resources that use a policy stop if the spot price exceeds the max price.
* *Added:* You can now use [cost allocation labels](https://docs.nebius.com/signup-billing/usage/cost-allocation-labels.md) to group Compute costs by service, application or team. Filter costs by label on the **Billing** → **Usage** page, or check the `Tags` column in [exported usage data](https://docs.nebius.com/signup-billing/usage/export.md).
* *Added:* You can now [collect journald logs from Managed Service for Kubernetes® node groups](https://docs.nebius.com/kubernetes/logs.md#how-to-enable-journald-logs) and view them in Observability Logs. The logs are disabled by default.
* *Added:* Kubernetes 1.36 is now [supported](https://docs.nebius.com/kubernetes/versions.md) in Managed Service for Kubernetes and is the recommended version for new clusters. Kubernetes 1.33 has reached end of life.
* *Added:* You can now set up [automatic restarts](https://docs.nebius.com/serverless/jobs/auto-restarts.md) for Serverless AI jobs. With `--restart-policy on-failure`, Serverless AI restarts the container when it exits with a non-zero code.
* *Updated:* The `us-north1`, `eu-south1` and `eu-west2` regions are now [public](https://docs.nebius.com/overview/regions.md#public-regions) and available to all Nebius users.
* *Updated:* Managed Service for Kubernetes node groups now use a default [drain timeout](https://docs.nebius.com/kubernetes/node-groups/manage.md#deployment-strategy-and-quotas) of 10 minutes. If a node isn't drained within this time, Managed Kubernetes force-drains and deletes it.
* *Updated:* You can now enable encryption for `NETWORK_SSD_NON_REPLICATED` and `NETWORK_SSD_IO_M3` disks provisioned [over CSI](https://docs.nebius.com/kubernetes/storage/disk-over-csi.md#create-a-storage-class-for-custom-provisioning-optional) by setting `encrypted: "true"` in a custom storage class.
* *Updated:* [Nebius Tunnels agent v1.2.0](https://docs.nebius.com/tunnels/resources/tunnels-agent-changelog.md) lets you configure connections to local services, keeps more idle connections for reuse and uses less CPU per forwarded request.

**September 14–20, 2026**

* *Added:* [DNS in Virtual Networks](https://docs.nebius.com/vpc/dns/overview.md) is now available. Create DNS zones attached to a network, add records that resolve only from workloads in that network and give your VMs stable internal endpoints under a domain name of your choosing.
* *Added:* The new `eu-south1` (Spain, Madrid) [private region](https://docs.nebius.com/overview/regions.md#private-regions) is now available. For the full list of available services, see [Availability of services per region](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region).
* *Added:* You can now connect a [SkyPilot cluster to third-party clouds](https://docs.nebius.com/3p-integrations/multi-cloud-skypilot.md) in Nebius AI Cloud. Provide credentials for Google Cloud, AWS or Runpod when you create or edit the cluster to run workloads across multiple clouds.
* *Added:* [Serverless AI Devlabs](https://docs.nebius.com/serverless/devlabs/manage.md) are now available as a new deployment type alongside jobs and endpoints. Devlabs run container images as interactive, browser-based development environments for coding, prototyping and debugging.
* *Updated:* Values of [shared filesystem specifications](https://docs.nebius.com/compute/storage/types.md#filesystem-specifications) have been revised and increased.

**September 7–13, 2026**

* *Added:* [Filesystem buckets](https://docs.nebius.com/object-storage/buckets/filesystem-buckets.md) in Object Storage are now available in preview. Attach an Object Storage bucket to an existing [shared filesystem](https://docs.nebius.com/compute/storage/types.md#shared-filesystems) to read or write the same data over both an S3-compatible API and the filesystem interface. Filesystem buckets are excluded from the [Object Storage SLA](https://docs.nebius.com/legal/sla-levels/storage.md) while in preview.
* *Added:* [Bucket inventory](https://docs.nebius.com/object-storage/buckets/inventory.md) in Object Storage is now available in preview in all [regions](https://docs.nebius.com/overview/regions.md). Schedule daily or weekly reports that list the objects in a bucket in CSV or Apache Parquet format and deliver them to a destination bucket for auditing, analytics or compliance workflows. See [how to configure bucket inventory](https://docs.nebius.com/object-storage/buckets/configure-inventory.md) for setup steps.
* *Added:* The new `uk-south2` (United Kingdom, London) [public region](https://docs.nebius.com/overview/regions.md#public-regions) is now available. For the full list of available services, see [Availability of services per region](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region).
* *Added:* New [virtual machine platform](https://docs.nebius.com/compute/virtual-machines/types.md) `gpu-rtx6000-a` brings NVIDIA® RTX PRO™ 6000 GPUs with Intel Granite Rapids to the `uk-south2` region. See [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md) for on-demand and preemptible rates.
* *Added:* New `2vcpu-8gb` [preset](https://docs.nebius.com/compute/virtual-machines/types.md) for the `cpu-d3` (Non-GPU AMD EPYC Genoa) platform, available in all regions.

**August 31 — September 6, 2026**

* *Added:* New guide: [Authenticate the Nebius AI Cloud CLI in environments without a browser](https://docs.nebius.com/cli/no-browser.md), such as Docker containers, CI/CD runners and dev containers. The guide covers service account authentication with an [authorized key](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) and user account authentication by opening an authorization link on another machine.
* *Added:* New tutorial: [Connecting to a virtual machine without a public IP address by using Nebius Tunnels](https://docs.nebius.com/tunnels/tutorials/connect-vm.md). Connect over SSH to a VM that stays isolated from the internet, without a bastion host or a VPN.
* *Added:* You can now inject small configuration files into containers when creating Serverless AI [jobs](https://docs.nebius.com/serverless/jobs/manage.md) and [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md) in the web console. In the **Files** section, upload files or create text files and specify the mount path in the container. Injected files are read-only and limited to 64 KiB each.
* *Updated:* Serverless AI, Managed Service for MLflow and Managed Service for PostgreSQL are now available in the `eu-west2` (France) [private region](https://docs.nebius.com/overview/regions.md#private-regions). See the [list of services](https://docs.nebius.com/overview/services.md) for regional availability.
* *Updated:* [Scraping metrics with Prometheus](https://docs.nebius.com/observability/metrics/prometheus.md) now uses regional endpoints in the format `read.monitoring.<region>.nebius.cloud` instead of the single `read.monitoring.api.nebius.cloud` endpoint. To scrape metrics from multiple regions, create a separate `scrape_config` job for each region.

**August 24–30, 2026**

* *Added:* You can now request plain [HTTP access to the Object Storage S3 API](https://docs.nebius.com/object-storage/http-access.md) for selected buckets and use `http://` instead of `https://` in the S3 API endpoint. Choose between the **Region-local** mode (access only from Nebius AI Cloud VMs in the bucket's region) and the **All** mode (access from any source). HTTP access reduces encryption-related overhead in request-heavy workloads, at the cost of unencrypted traffic.
* *Added:* Every Managed Service for Kubernetes® cluster now exposes a public [OIDC discovery endpoint](https://docs.nebius.com/kubernetes/networking/oidc-public-endpoint.md) and a JWKS endpoint at `https://oidc.mk8s.api.nebius.cloud`. External services can use them to verify workload identities from tokens that Kubernetes issues, for example when you configure workload identity federation.
* *Added:* You can now create SecretStash secrets directly from the web console when configuring **Secret environment variables** for Serverless AI [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md) and [jobs](https://docs.nebius.com/serverless/jobs/manage.md). In the CLI, the `--env-secret` parameter accepts `key=secret_selector` pairs, where `key` must match a payload key in the [SecretStash secret](https://docs.nebius.com/mysterybox/overview.md#secrets-and-versions).
* *Updated:* Object Storage data transfers now always apply [limits on request rate and bandwidth](https://docs.nebius.com/object-storage/transfer/limits.md). If you don't set the limits or set them to zero, the default values apply: 4000 requests per second and 50 GiB/s.
* *Updated:* Data transfers now support an explicit list of external storage services, including Alibaba Cloud OSS, AWS S3, Azure Blob Storage, Backblaze B2, Cloudflare R2, Google Cloud Storage, IBM Cloud Object Storage, MEGA S4, Oracle Cloud Infrastructure Object Storage, Supabase, T3 Tigris Data and Wasabi. Providers can be supported as a source, a destination or both, see [Supported external storage services](https://docs.nebius.com/object-storage/transfer/requirements.md#supported-external-storage-services) to learn more.
* *Updated:* The `nebius iam access-key` CLI command group is deprecated and will be removed on September 1, 2026. Use [`nebius iam v2 access-key`](https://docs.nebius.com/cli/reference/iam/v2/access-key) instead. All existing keys remain accessible through the new commands.
* *Updated:* The interactive [CLI configuration flow](https://docs.nebius.com/cli/configure.md) is simplified. `nebius profile create` no longer requires a project ID upfront: the CLI prompts you for the profile name, endpoints and authorization type, then lets you pick the tenant and project after you log in.
* *Removed:* The `READ_ONLY` attach mode is no longer supported when [attaching disks and shared filesystems](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms) to Compute virtual machines. The only supported value of `attach_mode` is `READ_WRITE`.

**August 17–23, 2026**

* *Added:* The new `us-north1` (Woodbury, Minnesota, US) [private region](https://docs.nebius.com/overview/regions.md#private-regions) is now available. It supports [Compute](https://docs.nebius.com/compute/index.md) with the NVIDIA® B300 NVLink and Non-GPU AMD EPYC Genoa [platforms](https://docs.nebius.com/compute/virtual-machines/types.md), [Object Storage](https://docs.nebius.com/object-storage/index.md), [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/index.md), [Container Registry](https://docs.nebius.com/container-registry/index.md), [Key Management Service](https://docs.nebius.com/kms/index.md) and other Nebius AI Cloud services.
* *Added:* Clusters and node groups in Managed Service for Kubernetes® now support [Kubernetes 1.35](https://kubernetes.io/releases/#release-v1-35). It is now the default and recommended [Kubernetes version in Nebius AI Cloud](https://docs.nebius.com/kubernetes/versions.md).
* *Added:* You can now manage Serverless AI [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md) and [jobs](https://docs.nebius.com/serverless/jobs/manage.md) through the [Nebius AI Cloud REST API](https://docs.nebius.com/rest-api/index.md), in addition to the web console and CLI. Each management page now includes ready-to-use `curl` examples for creating, listing, stopping, starting and deleting resources.
* *Added:* [Lifecycle and statuses of Serverless AI endpoints and jobs](https://docs.nebius.com/serverless/lifecycle.md) now documents every endpoint and job status (`PROVISIONING`, `RUNNING`, `ERROR`, `FAILED` and others), typical transitions, the 30-minute provisioning timeout and how to interpret `state_details` codes such as `StartFailed`, `ContainerFailed`, `TimeoutExceeded` and `NotEnoughResources`.
* *Added:* New `storage.bucket-policy-editor` [IAM role in Object Storage](https://docs.nebius.com/iam/authorization/roles.md#object-storage) grants permission to view and modify bucket policies without granting access to bucket contents.
* *Added:* [Object Storage data transfers](https://docs.nebius.com/object-storage/transfer/destination-objects.md#deleting-destination-objects) now support a delete strategy for destination objects. Set `enable_deletes_in_destination` to `true` when you create a transfer to remove destination objects that no longer have matching source objects, keeping the source and destination in sync (for example, for replication).
* *Added:* The [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md) can now be called through the Go, Python and JavaScript SDKs, in addition to the web console and CLI. Each interface returns the same list of resource availability information for a given platform and preset.
* *Updated:* You can now [delete all objects in an Object Storage bucket](https://docs.nebius.com/object-storage/objects/manage.md#deleting-all-objects): delete and recreate the bucket in the web console, use `s5cmd rm --all-versions` with `s3://<bucket>/*`, or loop `aws s3api delete-objects` in batches of 1000 keys including delete markers when versioning is enabled.
* *Updated:* You can now [create Key Management Service keys with Terraform](https://docs.nebius.com/kms/manage/create.md), in addition to the web console and CLI. The `nebius_kms_v1_symmetric_key` resource supports symmetric key creation, rotation period, description updates and deletion or restoration.
* *Updated:* Invitations are now managed on the **Users** tab in [IAM](https://docs.nebius.com/iam/authorization/add-users.md), which replaces the separate **Invitations** tab in the web console. When you invite a user, you can now assign groups in the same dialog. Filter the user list by **Status** (`Active`, `Invited`, `Expired`, `Blocked`) and use the menu next to a user to **Resend invitation** or **Delete invitation**.
* *Updated:* Serverless AI now provisions and manages its own underlying Compute virtual machines. For [Serverless AI jobs and endpoints](https://docs.nebius.com/serverless/overview.md) created after July 28, 2026, the VMs no longer appear on the **Job and endpoint VMs** tab of the Compute **Virtual machines** page. Only VMs from resources created before that date are still listed there.

**August 10–16, 2026**

* *Added:* New tutorials for [Nebius Tunnels](https://docs.nebius.com/tunnels/index.md): [deploy a large language model on a GPU VM](https://docs.nebius.com/tunnels/tutorials/llm.md) and [run JupyterLab on a VM](https://docs.nebius.com/tunnels/tutorials/jupyterlab.md), reaching each service from the internet through a tunnel while the VM itself has no public IP address.
* *Added:* Managed Service for Kubernetes® [CSI driver](https://docs.nebius.com/kubernetes/storage/filesystem-over-csi.md#install-the-csi-driver) for shared filesystems is now available as chart version `0.1.7`. The chart's `StorageClass` defaults to the `WaitForFirstConsumer` volume binding mode, which delays the provisioning of a `PersistentVolume` until a Pod using the `PersistentVolumeClaim` is created.
* *Added:* The new `x_UsageBasedDiscountIds` [FOCUS extension field](https://docs.nebius.com/signup-billing/usage/focus-fields.md) lists the usage-based discounts that were applied when calculating `ContractedCost` for a charge.
* *Updated:* [Audit Logs](https://docs.nebius.com/audit-logs/index.md) are now stored per region. When you [view](https://docs.nebius.com/audit-logs/events/view.md), [filter](https://docs.nebius.com/audit-logs/events/filter.md) or [export](https://docs.nebius.com/audit-logs/events/export.md) audit events, select the region in the web console or pass `--region` to the CLI.

**August 3–9, 2026**

* *Added:* The [Nebius AI Cloud REST API](https://docs.nebius.com/rest-api/index.md) is now available. It exposes the same resources and operations as the [gRPC API](https://docs.nebius.com/grpc-api/index.md) over HTTP/1.1 with JSON. See the [quickstart](https://docs.nebius.com/rest-api/quickstart.md), [authentication](https://docs.nebius.com/rest-api/authentication.md) and [API reference](https://docs.nebius.com/rest-api/reference.md) for details.
* *Added:* You can now let workloads running in Nebius AI Cloud [access resources in external clouds](https://docs.nebius.com/iam/wif/index.md) by exchanging a Nebius IAM access token for an [OpenID Connect](https://openid.net/developers/how-connect-works/) (OIDC) ID token through the Nebius Security Token Service (`https://sts.nebius.com`). Any platform that supports OIDC Discovery can validate the issued tokens. For an example with Google Cloud, see [Configuring access to Google Cloud for Nebius AI Cloud workloads](https://docs.nebius.com/iam/wif/configure.md).
* *Added:* You can now create [one-time billing exports](https://docs.nebius.com/signup-billing/usage/export.md#one-time-exports) in the web console under **Billing → Export → One-time exports**, in addition to the existing CLI flow.

**July 27 — August 2, 2026**

* *Added:* You can now run [Serverless Containers jobs](https://docs.nebius.com/serverless/jobs/manage.md) and [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md) on [preemptible VMs](https://docs.nebius.com/compute/virtual-machines/preemptible.md). Pass `--preemptible` when you create a job or endpoint to use a cheaper GPU VM that Compute can stop at any time.
* *Added:* [Object Storage bucket policy](https://docs.nebius.com/object-storage/buckets/bucket-policy.md) rules now support the `?` placeholder in `paths`. Each `?` matches exactly one character, so a pattern like `allowed?/*` grants access to prefixes such as `allowed1/`, `allowed2/` and `allowedA/`.
* *Added:* New tutorial: [Test data transfer speed with Warp](https://docs.nebius.com/object-storage/transfer/testing-transfer-speed.md). Generate a large test dataset in an Object Storage bucket and measure the maximum throughput of the Object Storage data transfer service.
* *Updated:* Compute virtual machines are now grouped in the web console into **Standalone VMs**, **Kubernetes nodes**, [**Container VMs**](https://docs.nebius.com/compute/virtual-machines/containers.md) and **Job and endpoint VMs** tabs on the **Virtual machines** page. "Containers over VMs" has been renamed to "Container VMs" across the console.
* *Removed:* The [free trial](https://docs.nebius.com/signup-billing/free-trial) program has been suspended as of July 13, 2026. New sign-ups are no longer accepted, and the sign-up flow no longer offers the trial option.

**July 20–26, 2026**

* *Added:* You can now set [project limits](https://docs.nebius.com/overview/limits/project-limits.md) (capacity allowance) on a [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md) to cap how many GPUs each project in your tenant can consume. See [Managing project limits](https://docs.nebius.com/overview/limits/manage-project-limits.md) for how to view, set, remove and disable limits from the web console or CLI.
* *Added:* Managed Service for Kubernetes® load balancer services now support the [`nebius.com/load-balancer-pool-id`](https://docs.nebius.com/kubernetes/clusters/load-balancer) annotation. Use it to allocate the load balancer's public IP address from a specific [Virtual Networks IP pool](https://docs.nebius.com/vpc/overview.md#pool) instead of the default subnet pool.
* *Updated:* MysteryBox is now called [SecretStash](https://docs.nebius.com/mysterybox/overview.md). The service, resources and functionality are unchanged; only the display name and [Terms of Use](https://docs.nebius.com/legal/specific-terms/secretstash.md) were updated.
* *Updated:* Creating a Compute virtual machine in the web console is now a step-by-step [wizard](https://docs.nebius.com/compute/virtual-machines/manage.md#how-to-create-vms) with **General**, **Compute**, **Storage** and other sections. If you have [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md), the **General** step lets you choose between a **Reserved VM** (capacity assured by your CBGs) or a **Pay-as-you-go VM**, and the **Compute** step exposes the full [reservation](https://docs.nebius.com/compute/virtual-machines/reservations.md) configuration, including **Switch to PAYG** behavior when a reservation is exhausted.

**July 13–19, 2026**

* *Added:* The new `eu-west2` (Paris, France) [private region](https://docs.nebius.com/overview/regions.md#private-regions) is now available. It supports [Compute](https://docs.nebius.com/compute/index.md) with the NVIDIA® B300 NVLink and Non-GPU AMD EPYC Genoa [platforms](https://docs.nebius.com/compute/virtual-machines/types.md), [Object Storage](https://docs.nebius.com/object-storage/index.md), [Managed Service for Kubernetes®](https://docs.nebius.com/kubernetes/index.md), [Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/index.md), [Container Registry](https://docs.nebius.com/container-registry/index.md) and other Nebius AI Cloud services.
* *Added:* The [serial console](https://docs.nebius.com/compute/virtual-machines/serial-console.md) is now available in preview. Use it to open a browser-based text session to a Compute virtual machine. Use it to troubleshoot a VM when network access is unavailable or to complete the first-boot setup on custom or third-party images before SSH is configured.
* *Added:* New tutorial: [generate, persist and query vector embeddings with LanceDB and Object Storage](https://docs.nebius.com/tutorials/lancedb-vector-embeddings.md). Use an Object Storage bucket as a serverless vector store for LanceDB over its S3-compatible API and run nearest-neighbor similarity searches for semantic search or retrieval-augmented generation.
* *Updated:* [Creating a Managed Service for Kubernetes® cluster](https://docs.nebius.com/kubernetes/clusters/manage.md#how-to-create-clusters) in the web console is now a multi-step flow. You can configure the cluster, add one or more node groups (including reservations from [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md)) and review a summary before the cluster is created.

**July 6–12, 2026**

* *Added:* You can now create [disk snapshots](https://docs.nebius.com/compute/storage/disk-snapshots.md) in Compute to capture a point-in-time copy of a disk. Use snapshots to back up disks before risky operations, clone disk state or restore data from a snapshot.
* *Added:* Managed Service for Kubernetes® node groups now integrate with [Virtual Networks security groups](https://docs.nebius.com/kubernetes/networking/security-groups.md). You can [attach security groups](https://docs.nebius.com/kubernetes/networking/assign-security-groups.md) to a node group and control traffic to and from the nodes.
* *Updated:* You can now [resize a disk](https://docs.nebius.com/postgresql/clusters/manage.md#how-to-modify-clusters) of a Managed Service for PostgreSQL® cluster without any need to create the cluster again. Disk size can only be increased, not decreased.

**June 29 — July 5, 2026**

* *Added:* Managed Service for Soperator now supports [ephemeral nodes](https://docs.nebius.com/slurm-soperator/capacity/ephemeral-nodes.md). You can release specific worker nodes from a Soperator cluster and reuse the same [capacity block group](https://docs.nebius.com/overview/limits/capacity-block-groups.md) for inference workloads in a separate Managed Service for Kubernetes® cluster, without taking down the entire Soperator cluster.
* *Added:* Serverless AI [endpoints](https://docs.nebius.com/serverless/endpoints/manage.md) now expose each HTTP port through a managed `https://` URL, and each TCP port through a managed `tls://<host>:443` URL — both encrypted. A public IP address is no longer required to reach an endpoint from the internet.
* *Added:* When you create a Serverless AI endpoint, you can now use the `--inject-file` option to [mount local files](https://docs.nebius.com/serverless/endpoints/manage.md) into the endpoint container at launch. Mounted files are read-only and limited to 64 KiB.
* *Added:* Object Storage [lifecycle rules](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md) can now filter objects by tags. Use tag-based filters to apply expiration and storage class transitions to a subset of objects in a bucket.
* *Added:* New tutorial: [run OpenMM molecular dynamics simulations as a Serverless AI job](https://docs.nebius.com/serverless/tutorials/openmm-molecular-dynamics.md). Package OpenMM in a Docker image, push it to Container Registry and run CUDA®-accelerated protein simulations that read and write results to an Object Storage bucket.
* *Updated:* Managed Service for Kubernetes now uses a new default [deployment strategy](https://docs.nebius.com/kubernetes/node-groups/manage.md#deployment-strategy-and-quotas) for node group updates: nodes are replaced one at a time (`max_unavailable=1`, `max_surge=0`), so rolling updates no longer require additional Compute quota by default. To keep the previous behavior of creating a replacement node before removing the existing one, set a non-zero surge value on the node group.

**June 22–28, 2026**

* *Added:* [Nebius Tunnels](https://docs.nebius.com/tunnels/index.md) is now available in preview. You can expose local HTTP and TCP services to the internet through an outbound agent connection, without opening inbound firewall ports.
* *Added:* You can now use [local SSD disks](https://docs.nebius.com/compute/storage/local-disks.md) for high-performance, low-latency ephemeral storage on supported Compute virtual machines, Managed Service for Kubernetes® node groups and Managed Service for Soperator clusters.
* *Added:* You can now use [budgets](https://docs.nebius.com/signup-billing/budgets.md) in Billing to track spending against a target amount and receive alerts when your costs cross configured thresholds.
* *Added:* Object Storage now supports the [Intelligent storage class](https://docs.nebius.com/object-storage/storage-classes.md#intelligent-storage-class). It automatically switches rarely accessed objects to a lower-cost tier while keeping objects in the same location and preserving storage performance.
* *Added:* Documentation now includes instructions about [how to share an object with a pre-signed URL](https://docs.nebius.com/object-storage/objects/manage.md#how-to-share-an-object-with-a-pre-signed-url) in Object Storage. Pre-signed URLs grant temporary download access without requiring the recipient to have Nebius AI Cloud credentials.
* *Added:* You can now [attach a stopped virtual machine's boot disk to another VM](https://docs.nebius.com/compute/virtual-machines/inspect-boot-disk.md) to inspect or repair it when the original VM does not start or you cannot connect to it.
* *Updated:* The `uk-south1` region is now [public](https://docs.nebius.com/overview/regions.md#public-regions). Services available in this region are listed in [Regions](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region).
* *Updated:* You can now create one-time [usage data exports](https://docs.nebius.com/signup-billing/usage/export.md#one-time-export) with the Nebius AI Cloud CLI. Use the exported FOCUS 1.2 CSV data for cost analysis and reporting in external tools.

**June 15–21, 2026**

* *Added:* The [Key Management Service](https://docs.nebius.com/kms.md) is now available to Nebius AI Cloud users. It enables you to issue and store cryptographic keys, so you can protect and secure your applications.
* *Added:* Clusters and node groups in Managed Service for Kubernetes® now support [Kubernetes 1.34](https://kubernetes.io/releases/#release-v1-34). It is now the default and recommended [Kubernetes version in Nebius AI Cloud](https://docs.nebius.com/kubernetes/versions.md).
* *Added:* If the control plane of your Managed Kubernetes cluster has a public IP address, you can now restrict network access to it by [specifying a list of allowed CIDR blocks](https://docs.nebius.com/kubernetes/networking/limit-access-to-public-endpoint.md) in the cluster's settings.
* *Updated:* Time series that you [ingest into the Observability service](https://docs.nebius.com/observability/metrics/ingest/index.md) can now have up to 37 labels, up from the previous limit of 28 labels.

**June 8–14, 2026**

* *Added:* A [free trial](https://docs.nebius.com/signup-billing/free-trial) is now available for individual users in the `eu-north1` region. The trial includes 30 days of access and \$5 in credit to explore the platform.
* *Added:* You can now use the [Nebius AI Cloud SDK for Go](https://docs.nebius.com/sdk/go) to interact with Nebius AI Cloud services from Go applications. Manage resources, handle authentication and call Nebius AI Cloud services without building API requests manually.
* *Added:* You can now [send traces directly to Nebius AI Cloud](https://docs.nebius.com/observability/traces/direct-ingest.md) from applications that use OpenTelemetry. Configure an OpenTelemetry exporter to write traces to a regional Tracing writer endpoint.

**June 1–7, 2026**

* *Added:* Documentation now includes instructions for [checking Object Storage performance by using Warp](https://docs.nebius.com/object-storage/performance/benchmark.md).
* *Updated:* You can now run `nebius ai create` to create a Serverless AI [endpoint](https://docs.nebius.com/serverless/quickstart/endpoints.md) or [job](https://docs.nebius.com/serverless/quickstart/jobs.md) through an interactive, step-by-step workflow. The command guides you through the required configuration options and pre-fills common values, making endpoint and job setup easier.

**May 25–31, 2026**

* *Updated:* Starting June 1, 2026, prices are updated for Compute virtual machines and for Standalone Applications with NVIDIA® B300, B200, H200 and H100 GPUs. To check prices before and from this date, see [Compute documentation](https://docs.nebius.com/compute/resources/pricing.md#prices) and [Standalone Applications documentation](https://docs.nebius.com/applications/standalone/pricing.md#computing-resources).
* *Added:* You can now [use Managed SkyPilot](https://docs.nebius.com/3p-integrations/skypilot-mk8s.md) to orchestrate and run AI workloads across Managed Service for Kubernetes® clusters. Managed SkyPilot selects the best cluster for running workloads, ensures fault tolerance and chases capacity for the required cluster when the capacity is insufficient.
* *Added:* Documentation now includes how data that you export from Nebius AI Cloud is [compliant with FinOps Open Cost and Usage Specification (FOCUS) 1.2](https://docs.nebius.com/signup-billing/usage/focus-conformance.md).
* *Added:* Documentation now describes how Compute [isolates InfiniBand™ traffic](https://docs.nebius.com/compute/clusters/gpu/index.md#isolation-and-security-of-infiniband-traffic) between GPU clusters by using InfiniBand partition keys.
* *Added:* Serverless documentation now includes video guides, for example, about how to [fine-tune a large language model](https://docs.nebius.com/serverless/tutorials/fine-tuning.md) (LLM) or how to [deploy an LLM](https://docs.nebius.com/serverless/tutorials/deploy-model.md).

**May 18–24, 2026**

* *Added:* You can now [import your own image into Compute](https://docs.nebius.com/compute/storage/import-image.md) from an Object Storage bucket. Upload a `.vmdk`, `.vhd`, `.raw` or `.qcow2` file to a bucket and create a custom image to launch boot disks and virtual machines from it.
* *Added:* Audit Logs supports [two roles](https://docs.nebius.com/iam/authorization/roles.md#audit-logs), `auditlogs.audit-event-viewer` and `auditlogs.audit-event-exporter`. They grant users granular access to view audit events and manage audit log exports.
* *Added:* [Topology-aware scheduling](https://docs.nebius.com/kubernetes/gpu/topology-aware-scheduling.md) is now available for GPU workloads in Managed Service for Kubernetes®. Nebius AI Cloud exposes InfiniBand™ topology information as node labels, so schedulers can place workloads on nodes that are physically closer in the network hierarchy. This improves communication performance.
* *Added:* Managed Kubernetes documentation now includes the default [kubeReserved values](https://docs.nebius.com/kubernetes/node-groups/kube-reserved.md) applied on worker nodes. For example, you can find out how the `memory` reservation is calculated for GPU nodes based on RAM size.
* *Added:* Object Storage now supports [object integrity checks](https://docs.nebius.com/object-storage/objects/manage.md#how-to-verify-object-integrity). When you upload an object to a bucket, send a checksum with your upload. Object Storage verifies the checksum and integrity of the object on receipt.
* *Added:* IAM documentation now includes instructions for [managing federations](https://docs.nebius.com/iam/federations/manage.md). You can create, activate and deactivate federations, change their settings, and upload or delete certificates.
* *Added:* CLI documentation now includes [filtering output with JSONPath](https://docs.nebius.com/cli/jsonpath-output.md). Use the `--format jsonpath='<expression>'` parameter to extract values such as a resource ID, name or IP address without post-processing the full output.
* *Added:* Object Storage now supports [data transfers](https://docs.nebius.com/object-storage/transfer/overview.md). Use them to replicate and back up your data from one bucket to another, or to migrate from a particular region or a third-party storage service.
* *Updated:* [Tax handling for companies](https://docs.nebius.com/signup-billing/payments/taxes.md) has changed. Reverse charge may now apply to companies that provide a valid VAT ID (EU, UAE, UK) or GSTIN (India, Singapore) in their billing setup. Individuals in Israel are now subject to Israeli VAT, like companies.
* *Removed:* [NVIDIA NIM™ microservices](https://docs.nebius.com/applications/standalone/nvidia-nim/index.md) for computational drug discovery are no longer available as standalone applications in Nebius AI Cloud.

**May 11–17, 2026**

* *Added:* You can now [access instance metadata from within a Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/instance-metadata.md) (VM) through the HTTP instance metadata service (IMDS). Retrieve instance details, labels, network and user data, service account tokens and live maintenance events without calling the Nebius AI Cloud API from outside the VM.
* *Updated:* The legacy `/mnt/cloud-metadata` mount on older VM images is deprecated and will be removed on September 30, 2026. Use the [HTTP instance metadata service](https://docs.nebius.com/compute/virtual-machines/instance-metadata.md) instead.
* *Updated:* The `ubuntu22.04-cuda12` and `ubuntu22.04-driverless` [boot disk image families](https://docs.nebius.com/compute/storage/boot-disk-images.md) will be deprecated on June 1, 2026. Existing disks remain available, but you can no longer create new disks from these families after that date. Migrate to Ubuntu 24.04 images before the deadline.
* *Updated:* When [setting up GPUs in Managed Kubernetes](https://docs.nebius.com/kubernetes/gpu/set-up.md), the `cuda12.4` driver preset (Ubuntu 22.04) is no longer available. Use `cuda12.8` or `cuda13.0` on Ubuntu 24.04.

**May 4–10, 2026**

* *Added:* You can now [create a Compute virtual machine and its disks together](https://docs.nebius.com/compute/virtual-machines/manage.md) in a single CLI command. These *managed disks* share the VM's lifecycle and are deleted automatically with it, which makes them a good fit for ephemeral workloads such as training jobs or inference clusters.
* *Added:* You can now [tune TCP window sizes on Linux virtual machines](https://docs.nebius.com/compute/virtual-machines/tcp-window-tuning.md) to improve per-flow throughput on high-bandwidth, high-latency connections.
* *Updated:* You can now set the [block size](https://docs.nebius.com/compute/storage/manage.md#volume-parameters) for a disk or shared filesystem when creating it in the web console, in addition to the CLI and Terraform provider.
* *Deprecated:* The `nebius storage v1alpha1 transfer` CLI commands and the `nebius_storage_v1alpha1_transfer` Terraform resource are deprecated and supported until 2026-06-01. Use the v1 data transfer API instead; existing transfers remain accessible through the v1 API. See the [CLI release notes](https://docs.nebius.com/cli/release-notes.md) and [Terraform provider release notes](https://docs.nebius.com/terraform-provider/reference/release-notes.md).

**April 27 – May 3, 2026**

* *Added:* The [NCCL Inspector](https://docs.nebius.com/slurm-soperator/monitoring/nccl-inspector) by NVIDIA® is now available on demand for Soperator clusters in Nebius AI Cloud. When enabled for a job, it collects per-communicator, per-collective performance metrics from NCCL operations and sends them to the Grafana® installation included with your cluster.
* *Added:* Soperator clusters now include built-in [health checks and an auto-healing system](https://docs.nebius.com/slurm-soperator/worker-nodes-health.md) for worker nodes. Critical GPU, RAM and network checks run on a schedule, and broken nodes are isolated and replaced automatically.
* *Added:* You can now configure single sign-on with [Okta](https://docs.nebius.com/iam/federations/configure-sso-okta.md).
* *Added:* Compute virtual machines now expose [maintenance reason codes](https://docs.nebius.com/compute/virtual-machines/maintenance-reasons.md) that explain why a maintenance event was triggered.
* *Added:* You can now [retrieve the public IPv4 CIDR blocks](https://docs.nebius.com/vpc/addressing/public-address-ranges.md) available for allocations in a project. The available ranges depend on the project region.
* *Added:* You can now collect diagnostic logs from [Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/logs.md) and from [Managed Kubernetes clusters](https://docs.nebius.com/kubernetes/troubleshooting/logs.md), including GPU, InfiniBand™ and node-level logs for troubleshooting.
* *Added:* A new [all-reduce NCCL performance test](https://docs.nebius.com/slurm-soperator/jobs/examples/nccl-all-reduce.md) is now included in Soperator. Use the pre-built single-node and multi-node versions to validate collective communication between GPUs over NVLink and InfiniBand and assess network performance.
* *Updated:* SkyPilot as a standalone application is now available in the `uk-south1` [region](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region).
* *Updated:* The [Observability Overview](https://docs.nebius.com/observability/index.md) page in the web console is now the new entrypoint for monitoring, providing information on firing alerts, key resource metrics and recent logs in a single view.

**April 20–26, 2026**

* *Added:* Compute disks and shared filesystems now support [deletion protection](https://docs.nebius.com/compute/storage/manage.md#deletion-protection). Enable it to prevent accidental deletion in automated environments such as CI/CD pipelines or Terraform configurations.
* *Added:* The Nebius AI Cloud CLI now supports an [interactive mode](https://docs.nebius.com/cli/interactive.md). To enable it, add `-i` or `--interactive` to a command. The CLI prompts for parameters step by step, validates each value and shows the resulting configuration before you apply it.
* *Added:* The [log export to Object Storage](https://docs.nebius.com/observability/logs/export.md) now supports the Nebius AI Cloud CLI.
* *Added:* You can now get a [list of public boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md#how-to-get-a-list-of-available-public-images) available in a given region. The list includes image families, recommended platforms and unsupported platforms for each image.
* *Added:* When Prometheus takes too long to retrieve metrics of large clusters, [shard and split their scraping jobs](https://docs.nebius.com/observability/metrics/prometheus.md#how-to-shard-large-scraping-jobs).
* *Updated:* The AWS CLI is now documented as a supported interface for [configuring lifecycle rules](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md) in Object Storage, alongside the Nebius AI Cloud interfaces.

**April 13–19, 2026**

* *Added:* The [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md) is now available in the web console. It shows GPU capacity availability across regions, platforms and presets so you can check where you can launch virtual machines before creating them.
* *Added:* You can now [monitor data plane events](https://docs.nebius.com/audit-logs/resources/quotas-limits.md#monitoring-data-plane-events) for Audit Logs in the web console. Graphs show processed events, quota usage and dropped events so you can detect when Object Storage activity approaches the quota.
* *Updated:* You can use the web console to create, configure and delete [Serverless AI endpoints](https://docs.nebius.com/serverless/endpoints/manage.md).
* *Updated:* You can manage [authorized keys for service accounts](https://docs.nebius.com/iam/service-accounts/authorized-keys.md) from the web console and the Terraform provider, in addition to the CLI.
* *Updated:* The [SkyPilot integration tutorial](https://docs.nebius.com/3p-integrations/skypilot.md) now includes instructions to use the Managed SkyPilot API Server, a standalone application available in the Nebius AI Cloud console.
* *Updated:* The [Nebius Service Health Status](https://status.nebius.com) page now displays all timestamps in UTC (GMT+00:00).

**April 6–12, 2026**

* *Added:* [Nebius Echo](https://docs.nebius.com/overview/nebius-echo.md), an AI assistant, is now available in the web console. It can explain services and features, inspect project resources and perform actions like creating or stopping virtual machines.
* *Added:* You can now view and [reschedule maintenance operations](https://docs.nebius.com/mlflow/maintenance.md) for Managed Service for MLflow clusters. The same capability is available for [Managed Service for PostgreSQL](https://docs.nebius.com/postgresql/maintenance.md).
* *Added:* A new [compute.instance-power-operator](https://docs.nebius.com/iam/authorization/roles.md#compute) IAM role lets you start and stop Compute virtual machines without granting broader Compute permissions.
* *Added:* You can now [query and stream logs directly from the Nebius AI Cloud CLI](https://docs.nebius.com/observability/logs/nebius-cli.md) using LogQL, without configuring external tools.
* *Updated:* [Object Storage monitoring](https://docs.nebius.com/object-storage/monitoring.md) now includes additional bucket metrics: space by storage class, object counts by storage class, API errors and transition lifecycle failures.
* *Updated:* Three new ML libraries — AutoKeras, auto-sklearn and TPOT — are now listed on the [third-party compatibility](https://docs.nebius.com/3p-integrations/compatibility.md) page.

**March 30 – April 5, 2026**

* *Added:* The [NVIDIA® RTX PRO™ 6000](https://docs.nebius.com/compute/virtual-machines/types.md) virtual machine platform is now available in the `us-central1` region. It features 96 GB of GDDR7 memory per GPU and comes in single-GPU and eight-GPU presets.
* *Added:* Serverless AI CLI commands now support [MysteryBox secrets](https://docs.nebius.com/cli/release-notes.md). You can pass secrets as environment variables, registry credentials or tokens when creating endpoints and jobs, without exposing sensitive values in plain text.
* *Updated:* You can now manage [capacity reservations](https://docs.nebius.com/compute/virtual-machines/reservations.md) for Compute virtual machines and [Managed Kubernetes node groups](https://docs.nebius.com/kubernetes/node-groups/reservations.md) in the web console. Previously, this required the CLI or Terraform provider.
* *Updated:* You can now [export logs](https://docs.nebius.com/observability/logs/export.md) directly from individual resource pages in the web console, in addition to the central Observability Logs page.
* *Updated:* The default retention period for [logs in Observability services](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-constraints) is now 14 days.

**March 23–29, 2026**

* *Added:* [Object versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) is available in Object Storage. When enabled, each update to an object creates a new version, which protects data from loss and allows you to restore previous versions.
* *Added:* You can now create [custom boot disk images](https://docs.nebius.com/compute/storage/custom-disk-images.md) to tailor images to your needs and create multiple virtual machines with custom disk architecture.
* *Added:* You can also create custom boot disk images by using the [Nebius Packer plug-in](https://docs.nebius.com/compute/storage/packer.md). Use it to pre-install packages to a disk, prepare versioned images and standardize environments across teams or workloads.
* *Added:* You can now use the [Nebius Terraform provider with Pulumi](https://docs.nebius.com/terraform-provider/pulumi.md) to declare your Nebius AI Cloud resources in the preferred programming language instead of using Terraform configuration.
* *Added:* You can now [export logs](https://docs.nebius.com/observability/logs/export.md) from Observability to an Object Storage bucket in JSON or Parquet format for long-term retention or analysis in external tools.
* *Updated:* You can now [attach and detach disks](https://docs.nebius.com/compute/storage/use.md#how-to-attach-volumes-to-vms) on running Compute virtual machines without stopping them first.

**March 16–22, 2026**

* *Added:* You can now [view logs for Managed Kubernetes clusters](https://docs.nebius.com/kubernetes/logs.md) in the web console, including optional audit logs and control plane component logs collected by default.
* *Added:* You can now [fine-tune a large language model with Serverless AI jobs](https://docs.nebius.com/serverless/tutorials/fine-tuning.md) by using Axolotl and LoRA, with Object Storage for checkpoints and adapter weights.
* *Added:* The NVIDIA B200 platform now includes a public [single-GPU preset](https://docs.nebius.com/compute/virtual-machines/types.md) (`1gpu-20vcpu-224gb`) in addition to the eight-GPU configuration.
* *Updated:* Managed Kubernetes now uses [Kubernetes 1.33](https://docs.nebius.com/kubernetes/versions.md) for new clusters and node groups. Older supported versions remain available for existing deployments, but are no longer recommended.
* *Updated:* [Preemptible virtual machines](https://docs.nebius.com/compute/virtual-machines/preemptible.md) are supported on all [GPU VM platforms](https://docs.nebius.com/compute/virtual-machines/types.md). [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md) now lists Israeli shekel (ILS) rates for preemptible VMs where that billing currency applies.
* *Updated:* You can now query logs only within the [Logs constraints](https://docs.nebius.com/observability/resources/quotas-limits.md#logs-constraints) time range, from three days in the past to one day ahead of the current time.

**March 9–15, 2026**

* *Added:* A new legal entity, [Nebius Israel Ltd.](https://docs.nebius.com/legal/dpa-il.md), is launched. Companies from Israel can now only pay by [bank transfers](https://docs.nebius.com/signup-billing/payments/bank-transfers.md) in Israeli shekels (ILS, ₪).
* *Added:* You can now configure single sign-on by using [Keycloak](https://docs.nebius.com/iam/federations/configure-sso-keycloak.md).
* *Updated:* GPU worker nodes in [Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/deploy/overview.md#managed-service-for-soperator) are only available if you have capacity block groups that reserve GPUs.

**March 2–8, 2026**

* *Added:* Virtual machines now support [secondary private IP addresses](https://docs.nebius.com/compute/virtual-machines/network.md#how-to-assign-a-secondary-private-ip-address-to-a-vm) that you can use as a backup option in case of incidents.
* *Added:* [Nebius VPN Gateway](https://docs.nebius.com/vpc/nebius-vpn-gateway.md), an open-source, VM-based IPsec gateway provided by Nebius Professional Services, is now available. You can deploy it to establish site-to-site VPN connectivity with external networks in other cloud providers or on-premises data centers.
* *Added:* Nebius AI Cloud now calculates [taxes](https://docs.nebius.com/signup-billing/payments/taxes.md#united-states) for the residents of Rhode Island in accordance with the United States tax law.
* *Updated:* For [viewing ingested traces from Managed Kubernetes clusters](https://docs.nebius.com/observability/traces/grafana.md) in Grafana®, the connection URL is now `https://read.tracing.api.nebius.cloud/projects/<project_ID>/tempo` instead of `https://read.tracing.api.nebius.cloud/tempo/<project_ID>`.

**February 23 – March 1, 2026**

* *Added:* [Managed Service for Soperator](https://docs.nebius.com/slurm-soperator/deploy/overview.md#nebius-ai-cloud-managed-solutions) is now generally available. You can create and manage Soperator clusters with just a few clicks.
* *Added:* You can now [collect journald logs from Compute virtual machines](https://docs.nebius.com/observability/logs/journald.md) and forward these logs to Logging.
* *Updated:* [Audit event export](https://docs.nebius.com/audit-logs/events/export.md) to Object Storage buckets is only supported in the `eu-north1` region.
* *Updated:* [Specifications](https://docs.nebius.com/compute/storage/types.md#filesystem-specifications) and [performance numbers](https://docs.nebius.com/compute/storage/types.md#filesystems-performance) for shared filesystems are actualized.

**February 16–22, 2026**

* *Added:* [Security groups](https://docs.nebius.com/vpc/security-groups/overview.md) are now available for Virtual Networks. You can use them as a firewall for your Compute virtual machines and control ingress and egress traffic with [security rules](https://docs.nebius.com/vpc/security-groups/manage.md).
* *Added:* New [Object Storage roles](https://docs.nebius.com/iam/authorization/roles.md) provide more granular access to buckets and objects. See the list of all [actions supported by Object Storage roles](https://docs.nebius.com/object-storage/supported-actions.md).
* *Added:* You can now specify a [service account when creating a Compute virtual machine](https://docs.nebius.com/compute/virtual-machines/manage.md) so that the VM performs actions on your behalf. This setting is available in the [Additional](https://docs.nebius.com/compute/virtual-machines/params.md#additional) section of the VM configuration.
* *Added:* You can now use [CLI exit codes](https://docs.nebius.com/cli/exit-codes.md) to interpret command failures and to automate scripts that depend on command outcomes.
* *Added:* You can now use [Mountpoint for Amazon S3](https://docs.nebius.com/object-storage/interfaces/mountpoint-s3.md) with Object Storage. Mount buckets as local filesystems on your machines or on Compute virtual machines and use the recommendations for use cases, limitations and performance.
* *Added:* You can now [deploy applications on containers over virtual machines](https://docs.nebius.com/compute/virtual-machines/applications.md). This option provides maximum performance tuning and direct control over infrastructure. See all available [deployment options](https://docs.nebius.com/applications/types.md).
* *Added:* [Network SSD NRD and Network SSD IO M3](https://docs.nebius.com/compute/storage/types.md#disk-types) boot disks now support [encryption](https://docs.nebius.com/compute/storage/types.md#encryption-of-disks), allowing you to securely store personal and other sensitive data, while reducing the risk of unauthorized access.
* *Updated:* [Applications](https://docs.nebius.com/applications.md) now have an updated interface that offers improved navigation and filtering, as well as unified product cards with multiple installation options in one place.
* *Updated:* Nebius AI Cloud may [automatically reduce quotas](https://docs.nebius.com/overview/quotas.md#automatic-quota-reduction) when usage stays low for a prolonged period. Users receive an email notification and have a grace period before the change applies.

**February 9–15, 2026**

* *Added:* In Serverless AI, you can now [debug failed jobs](https://docs.nebius.com/serverless/jobs/failure.md) by keeping the job's VM alive to connect via SSH.
* *Added:* [Single sign-on with JumpCloud](https://docs.nebius.com/iam/federations/configure-sso-jumpcloud.md) is now available. Users can sign in to Nebius AI Cloud with their JumpCloud credentials instead of a separate password.
* *Added:* You can now [export audit events to an Object Storage bucket](https://docs.nebius.com/audit-logs/events/export.md) for a specific time range. Use exported data for long-term retention, data portability or analysis in external tools.
* *Added:* You can now [collect traces](https://docs.nebius.com/observability/traces/ingest.md) with Nebius Observability Agent for Kubernetes and [view traces in Grafana](https://docs.nebius.com/observability/traces/grafana.md). Send traces from cluster applications via OTLP and explore them in Grafana with Tempo.
* *Updated:* We now recommend [GPU boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md#images-for-gpu-vms) with Ubuntu 24.04 and CUDA 12 or CUDA 13.0. The `ubuntu22.04-cuda12` image is not recommended and will be deprecated.
* *Updated:* When [setting up GPUs in Managed Kubernetes](https://docs.nebius.com/kubernetes/gpu/set-up.md), you can now choose between driver presets `cuda12.8`, `cuda13.0` and `cuda12.4`. You can also [change the driver preset](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-change-the-driver-preset) by updating the node group when you need a different driver or CUDA version.

**February 2–8, 2026**

* *Added:* [Serverless AI jobs and endpoints](https://docs.nebius.com/serverless/overview.md) are now available. You can use them to run AI workloads without any need to create and maintain infrastructure for them.
* *Added:* [Taxes](https://docs.nebius.com/signup-billing/payments/taxes.md) are now included in invoices for individuals from India, Singapore, the United Arab Emirates and the United Kingdom.

**January 26 – February 1, 2026**

* *Updated:* You can now use a Microsoft account to [log in to Nebius AI Cloud](https://docs.nebius.com/iam/log-in.md).

**January 19–25**

* *Added:* Object Storage now supports [logs](https://docs.nebius.com/object-storage/logs.md) of two types: control plane logs and data plane logs. By using them, you can get detailed information about actions on buckets and objects.

**January 5–11, 2026**

* *Added:* You can now use [capacity block groups](https://docs.nebius.com/overview/limits/capacity-block-groups.md) to [reserve GPUs](https://docs.nebius.com/compute/virtual-machines/reservations.md) for virtual machines. Capacity block groups and reservations ensure that you always have the computing resources necessary for your workloads and applications.
* *Added:* The [Managed Service for MLflow](https://docs.nebius.com/mlflow/index.md) is now available in the `me-west1` and `uk-south1` [regions](https://docs.nebius.com/overview/regions.md).
* *Added:* The [Managed Service for PostgreSQL](https://docs.nebius.com/postgresql/index.md) is now available in the `uk-south1` [region](https://docs.nebius.com/overview/regions.md).
* *Added:* Object Storage now supports the [Force storage class](https://docs.nebius.com/object-storage/buckets/manage.md#bucket-parameters) parameter for buckets. It overrides a storage class that you specify when you upload an object to a bucket.

**December 29–31, 2025**

* *Added:* You can now set up [billing data export](https://docs.nebius.com/signup-billing/usage/export.md) and automatically get usage data for cost analysis.

**December 15–21, 2025**

* *Updated:* The `me-west1` region is now [public](https://docs.nebius.com/overview/regions.md#public-regions). Services available in this region are listed in [Regions](https://docs.nebius.com/overview/regions.md#availability-of-services-per-region).

**December 1–7, 2025**

* *Updated:* The default [Compute quotas](https://docs.nebius.com/compute/resources/quotas-limits.md) on the numbers of NVIDIA B200 and NVIDIA H200 GPUs in the `us-central1` region per tenant are now zero, down from 32 and 16, respectively. This means that in tenants created after December 1, you need to [request a quota raise](https://docs.nebius.com/overview/quotas.md#change-quotas) before creating VMs with any number of these GPUs in `us-central1` projects. The change does not affect existing tenants.

**November 24–30, 2025**

* *Added:* Two new [virtual machine platforms](https://docs.nebius.com/compute/virtual-machines/types.md) are now available for Compute virtual machines, Managed Kubernetes nodes and other resources:

  * NVIDIA® B300 NVLink with Intel Granite Rapids (ID `gpu-b300-sxm`) is now available in the [private region](https://docs.nebius.com/overview/regions.md) `uk-south1`. It introduces NVIDIA B300 GPUs to Nebius AI Cloud.
  * NVIDIA® B200 NVLink with Intel Emerald Rapids (ID `gpu-b200-sxm-a`) is now available in the private region `me-west1`. This is the second platform with NVIDIA B200 GPUs; a platform with the same name (ID `gpu-b200-sxm`) is available in the public region `us-central1`.

* *Added:* When creating a [support ticket](https://docs.nebius.com/overview/support.md) in the [support center](https://console.nebius.com/support/create-ticket), you can now choose the topic of the ticket (technical, billing or digital rights). Available priority levels for technical tickets have also changed: the standard level is renamed medium, and new high and low levels are added to the existing levels. This helps us process your requests faster and more efficiently.

**November 17–23, 2025**

* *Added:* Four [NVIDIA NIM](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/) microservices are now available as [standalone applications](https://docs.nebius.com/applications/standalone/nvidia-nim/index.md). These microservices provide models from the NVIDIA BioNeMo Framework for computational drug discovery: [Boltz-2](https://build.nvidia.com/mit/boltz2/modelcard), [Evo 2](https://build.nvidia.com/arc/evo2-40b/modelcard), [GenMol](https://build.nvidia.com/nvidia/genmol-generate/modelcard) and [MolMIM](https://build.nvidia.com/nvidia/molmim-generate/modelcard).
* *Added:* The [NVIDIA Blueprint for generative virtual screening](https://github.com/NVIDIA-BioNeMo-blueprints/generative-virtual-screening) is now available as an [application for Managed Kubernetes](https://docs.nebius.com/applications/kubernetes/nvidia-blueprint-virtual-screening/index.md). The blueprint provides an AI-driven pipeline to design optimized small molecules efficiently.
* *Added:* You can now [delete empty projects](https://docs.nebius.com/iam/manage-projects.md#how-to-delete-a-project) that you no longer need, helping you keep your Nebius AI Cloud organized.

**November 10–16, 2025**

* *Updated:* You can now only delay a [maintenance event for Compute virtual machines](https://docs.nebius.com/compute/virtual-machines/maintenance.md) two times, up to seven days each time.
* *Added:* For residents of Texas and Washington, US, Nebius now [calculates taxes](https://docs.nebius.com/signup-billing/payments/taxes.md) in accordance with United States tax law and includes them in invoices.

**November 3–9, 2025**

* *Updated:* The default [Compute quota](https://docs.nebius.com/compute/resources/quotas-limits.md) on the number of NVIDIA H200 GPUs in the `us-central1` region per tenant is now 16, down from 32. The change does not affect existing tenants.
* *Updated:* When you [manually install the NVIDIA GPU Operator](https://docs.nebius.com/kubernetes/gpu/set-up.md#how-to-install-the-drivers-and-components-on-existing-node-groups) on your InfiniBand-interconnected Managed Kubernetes nodes, GPUDirect RDMA is now enabled by default.

**October 27–November 2, 2025**

* *Added:* Monitoring dashboards for Managed PostgreSQL clusters now include two new [connection pooler metrics](https://docs.nebius.com/postgresql/monitoring.md#connection-pooler), **Pooler clients active** and **Pooler clients waiting**.

**October 20–26, 2025**

* *Added:* Managed Kubernetes now supports Kubernetes 1.32. This version is selected for new clusters and node groups by default. See the [overview of Kubernetes versions](https://docs.nebius.com/kubernetes/versions.md).
* *Added:* The list of [roles](https://docs.nebius.com/iam/authorization/roles.md) has been extended. In addition to general roles (`admin`, `editor`, `viewer`, `auditor`), you can now assign new service roles to [custom groups](https://docs.nebius.com/iam/authorization/groups/index.md#custom-groups), allowing for more granular access to your resources. The new roles control access to Object Storage and MysteryBox resources, as well as Data Subject Requests to support.
* *Updated:* Starting October 22, usage of virtual machines and applications that use NVIDIA B200, H200 and H100 GPUs is recorded under new billing items that cover GPUs, vCPUs and RAM together rather than separately. Usage from October 1–21 is recalculated retroactively. This makes monitoring your usage simpler and does not affect your costs. [Learn more](https://docs.nebius.com/signup-billing/billing-changes-oct-2025).

**September 29–October 5, 2025**

* *Added:* You can now create [preemptible virtual machines](https://docs.nebius.com/compute/virtual-machines/preemptible.md) with NVIDIA B200 GPUs in the `us-central1` region.
* *Added:* You can now [create your own tenants](https://docs.nebius.com/iam/create-tenants.md) for dedicated billing and more resource isolation.
* *Removed:* New Managed MLflow clusters no longer support the `small` size. See the guide to [creating clusters](https://docs.nebius.com/mlflow/clusters/manage.md).

**September 22–28, 2025**

* *Updated:* Automatic security updates are now disabled by default in [boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md) for non-GPU virtual machines in Compute, in addition to GPU VMs, to prevent errors in running workloads. You can [enable them back](https://docs.nebius.com/compute/storage/automatic-updates.md).
* *Updated:* Computing resources of all Compute virtual machines are now eligible for [committed usage discounts](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md), as opposed to only VMs with NVIDIA H100 GPUs.

**September 15–21, 2025**

* *Added:* The [MysteryBox](https://docs.nebius.com/mysterybox/index.md) service is launched, allowing you to store sensitive data in an encrypted form to reuse them in your scripts, configuration files or applications.
* *Added:* You can now create [routing tables and routes](https://docs.nebius.com/vpc/routing/overview.md) to customize the routing of egress traffic and implement advanced networking scenarios, such as [custom NAT gateways](https://docs.nebius.com/vpc/routing/custom-nat-gateway.md) or segmented architectures.
* *Added:* Your [committed usage discounts](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md) are now grouped in orders that correspond to the agreement addendums that you sign.
* *Updated:* Automatic security updates are now disabled by default in [boot disk images](https://docs.nebius.com/compute/storage/boot-disk-images.md) for GPU virtual machines in Compute to prevent errors in running workloads. You can [enable them back](https://docs.nebius.com/compute/storage/automatic-updates.md).
* *Updated:* Default [Compute quotas](https://docs.nebius.com/compute/resources/quotas-limits.md) for GPU and non-GPU virtual machines are now separate, allowing new customers to create more VMs overall and control the remaining capacity in their projects more precisely.

**September 8–14, 2025**

* *Added:* You can now create Compute virtual machines with container images deployed on them: [containers over VMs](https://docs.nebius.com/compute/virtual-machines/containers.md). You can use images provided by Nebius AI Cloud or custom Docker images from public registries.
* *Added:* Two new [extensions for PostgreSQL](https://docs.nebius.com/postgresql/databases/extensions.md) are now available on all Managed Service for PostgreSQL clusters: [RUM](https://github.com/postgrespro/rum) offers enhanced full-text search, and [pg\_repack](https://github.com/reorg/pg_repack) allows you to remove bloat from tables and indexes.
* *Updated:* If you pay for Nebius AI Cloud services [by bank card](https://docs.nebius.com/signup-billing/payments/card.md), we can now suspend your account after one unsuccessful attempt to charge your card rather than after multiple attempts. Check regularly that your payment method is up to date.

**September 1–7, 2025**

* *Added:* Managed Kubernetes now performs [health checks](https://docs.nebius.com/kubernetes/maintenance/health-checks.md) on nodes, and automatically recovers nodes that are not ready or have issues with the boot disk or GPUs. You can [enable and disable](https://docs.nebius.com/kubernetes/maintenance/enable-disable-health-checks.md) these health checks.
* *Added:* Audit Logs now support [filtering events](https://docs.nebius.com/audit-logs/events/view.md) by more fields, so you can find events that occurred in a specific region, are associated with operations that have a specific status, etc.
* *Updated:* The navigation in the [web console](https://console.nebius.com) has undergone a major overhaul to group and present services and resources more clearly.
* *Updated:* The upload and download speed for the Standard [storage class](https://docs.nebius.com/object-storage/storage-classes.md) in Object Storage is now limited to 20 GBps per tenant in all regions.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*

*InfiniBand and InfiniBand Trade Association are registered trademarks of the InfiniBand Trade Association.*
