# Mountpoint for Amazon S3: Mounting buckets as local filesystems

Source: https://docs.nebius.com/object-storage/interfaces/mountpoint-s3

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Mountpoint for Amazon S3: Mounting buckets as local filesystems

[Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3) is an open-source client for mounting S3 buckets as local filesystems. You can use Mountpoint for Amazon S3 to mount Object Storage buckets to your local machines, and to resources in Nebius AI Cloud (Compute virtual machines, Kubernetes clusters) and other cloud providers.

## Use cases and limitations

Mountpoint for Amazon S3 is optimized for specific use cases like machine learning training which often involve reading large datasets with high throughput. For example, it is a good fit for data lake applications that read large objects without using other filesystem features like locking or POSIX permissions, or write objects sequentially from a single node. Mountpoint for Amazon S3 achieves this by parallelizing requests, both to each single file and to multiple files. Tests in Nebius AI Cloud show that Mountpoint for Amazon S3 can show performance that is close to clients that natively implement S3 APIs.

> [!WARNING]
>
> Mountpoint for Amazon S3 doesn't implement all features of a POSIX filesystem. This means certain file operations, such as file locks, directory renaming, symlinks, hardlinks and full control over file modes, owners and groups, are not fully supported or may behave differently than expected in a traditional filesystem. If your applications require these features or collaborative editing across multiple instances and users, use [Compute shared filesystems](https://docs.nebius.com/compute/storage/types.md#shared-filesystems).

See [Mountpoint file system behavior](https://github.com/awslabs/mountpoint-s3/blob/main/doc/SEMANTICS.md) for a detailed description of Mountpoint for Amazon S3's behavior and POSIX support and how they could affect your application. To troubleshoot file operations that may not be supported by Mountpoint for Amazon S3, see the [troubleshooting documentation](https://github.com/awslabs/mountpoint-s3/blob/main/doc/TROUBLESHOOTING.md).

## Installing and mounting buckets

### Prerequisites

1. Make sure you are in a [group](https://docs.nebius.com/iam/authorization/groups/index.md) that has the `admin` role within your tenant or project; for example, the default `admins` group. You can check this in the [Administration → IAM](https://console.nebius.com/iam) section of the web console.
2. [Create a service account](https://docs.nebius.com/iam/service-accounts/manage.md) and [add it to a group](https://docs.nebius.com/iam/authorization/groups/members.md) that grants the required level of access, for example, the [default](https://docs.nebius.com/iam/authorization/groups.md#default-groups) `viewers` or `editors` group.
3. [Create an access key pair](https://docs.nebius.com/iam/service-accounts/access-keys.md) for the service account and save the key ID and the secret key.

> **Example**
>
> **CLI**
>
> The following commands create a service account, add it to the default `viewers` group and create an access key for it. Specify your tenant and project IDs in the commands:
>
> * `TENANT_ID`: [Tenant ID](https://docs.nebius.com/iam/get-tenants.md#cli-2).
> * `PROJECT_ID`: [Project ID](https://docs.nebius.com/iam/manage-projects.md#cli-3).
>
> ```bash theme={null}
> TENANT_ID=<tenant-...>
> PROJECT_ID=<project-...>
>
> export SA_ID=$(nebius iam service-account create \
>   --parent-id "$PROJECT_ID" \
>   --name s3-mountpoint \
>   --format jsonpath='{.metadata.id}')
>
> export VIEWERS_ID=$(nebius iam group get-by-name \
>   --parent-id "${TENANT_ID}" \
>   --name 'viewers' \
>   --format jsonpath='{.metadata.id}')
> nebius iam group-membership create \
>   --parent-id "$VIEWERS_ID" \
>   --member-id "$SA_ID"
>
> export ACCESS_KEY_ID=$(nebius iam v2 access-key create \
>   --parent-id "$PROJECT_ID" \
>   --name "s3-mountpoint" \
>   --account-service-account-id "$SA_ID" \
>   --description "Amazon S3 Mountpoint CSI Driver" \
>   --format jsonpath='{.metadata.id}')
> export AWS_ACCESS_KEY_ID=$(nebius iam v2 access-key get \
>   --id "${ACCESS_KEY_ID}" \
>   --format json \
>   | jq -r '.status.aws_access_key_id')
> export AWS_SECRET_ACCESS_KEY=$(nebius iam v2 access-key get \
>   --id "${ACCESS_KEY_ID}" \
>   --format json \
>   | jq -r '.status.secret')
> ```

### Local and virtual machines

> [!NOTE]
>
> Mountpoint for Amazon S3 is only available for Linux operating systems.

To mount an Object Storage bucket on your local machine or a Compute VM:

1. Install Mountpoint for Amazon S3:

   **RPM-based (Fedora, CentOS, RHEL, etc.)**

   ```bash theme={null}
   wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
   sudo yum install -y ./mount-s3.rpm
   ```

   **DEB-based (Ubuntu, Debian)**

   ```bash theme={null}
   wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.deb
   sudo apt-get install -y ./mount-s3.deb
   ```

   For more installation instructions and details, see [Getting started](https://github.com/awslabs/mountpoint-s3/tree/main?tab=readme-ov-file#getting-started) and [Installing Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3/blob/main/doc/INSTALL.md) in Mountpoint for Amazon S3 documentation.

2. Create a credentials file, `~/.aws/credentials`, with your access key pair:

   ```bash theme={null}
   cat <<EOF > ~/.aws/credentials
   [default]
   aws_access_key_id=<key_ID>
   aws_secret_access_key=<secret_key>
   ```

   This ensures that the credentials are persistent between shell sessions. If you have the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables defined, they override `~/.aws/credentials`. For more details, see [AWS credentials](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md#aws-credentials) in Mountpoint for Amazon S3 documentation.

3. Mount the bucket:

   ```bash theme={null}
   mount-s3 <bucket_name> <directory> \
     --region <region> \
     --endpoint-url https://storage.<region>.nebius.cloud:443 \
     --maximum-throughput-gbps 10000 --max-threads 64
   ```

   Replace the following values:

   * `<bucket_name>`: Name of your bucket.
   * `<directory>`: Path to the directory on your machine where the bucket should be mounted.
   * `--region`: [Nebius AI Cloud region](https://docs.nebius.com/overview/regions.md) where the parent project of your bucket is located. To get the region of a project, go to the [web console](https://console.nebius.com) and then expand the list of tenants; the region, for example `eu-north1`, is displayed next to the project's name.
   * `--endpoint-url`: Object Storage endpoint in the region. All the endpoints have the `https://storage.<region>.nebius.cloud:443` format. For example, for buckets in the `eu-north1` region, the endpoint is `https://storage.eu-north1.nebius.cloud:443`.

   `--maximum-throughput-gbps 10000` and `--max-threads 64` are recommended performance settings. For more details, see [Performance](#performance).

   You can add more parameters to the command, for example, `--foreground` to run Mountpoint for Amazon S3 in the foreground instead of the background. For more details, see [Configuring Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md).

### Kubernetes clusters

> [!WARNING]
>
> Before making any changes to a production environment, [contact support](https://console.nebius.com/support/create-ticket) or your personal manager.

1. [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and configure it to work with your cluster. For Managed Kubernetes clusters in Nebius AI Cloud, see [How to connect to Managed Service for Kubernetes® clusters using kubectl](https://docs.nebius.com/kubernetes/connect.md).

2. Create a Kubernetes Secret with your access key pair:

   ```bash theme={null}
   kubectl create secret generic aws-secret \
     --namespace kube-system \
     --from-literal "key_id=<key_id>" \
     --from-literal "access_key=<secret_key>"
   ```

3. [Install Helm](https://helm.sh/docs/intro/install/).

4. Install the Mountpoint for Amazon S3 CSI Driver:

   ```bash theme={null}
   helm repo add aws-mountpoint-s3-csi-driver https://awslabs.github.io/mountpoint-s3-csi-driver
   helm repo update
   helm upgrade --install aws-mountpoint-s3-csi-driver \
     --namespace kube-system \
     aws-mountpoint-s3-csi-driver/aws-mountpoint-s3-csi-driver
   ```

   For more installation details and instructions, see [Installing Mountpoint for Amazon S3 CSI Driver](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/docs/INSTALL.md).

5. Create a PersistentVolume (PV):

   ```bash theme={null}
   REGION=<region>
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: s3-mountpoint
   spec:
     capacity:
       storage: 1Ti                     # Required by Kubernetes but effectively ignored
     accessModes:
       - ReadOnlyMany                   # Supported modes: ReadOnlyMany, ReadWriteMany
     storageClassName: ""               # Empty string required for static provisioning
     mountOptions:
       - endpoint-url https://storage.$REGION.nebius.cloud:443
       - region $REGION
       - maximum-throughput-gbps 10000  # raises max throughput as default limit is 1.25 GB/s (10 Gbps)
       - max-threads 64                 # raises max-threads as default is 16
       - allow-other                    # without this, only root can read
     csi:
       driver: s3.csi.aws.com           # Required
       volumeHandle: <volume_handle>    # Must be unique per volume
       volumeAttributes:
         bucketName: <bucket_name>
   EOF
   ```

   Replace the following values:

   * `REGION`: [Nebius AI Cloud region](https://docs.nebius.com/overview/regions.md) where the parent project of your bucket is located. To get the region of a project, go to the [web console](https://console.nebius.com) and then expand the list of tenants; the region, for example `eu-north1`, is displayed next to the project's name.

   * `.spec.accessModes`: List of [access modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) supported by the PV. Supported modes are `ReadOnlyMany` (multiple nodes can mount the PV as read-only) and `ReadWriteMany` (multiple nodes can mount the PV as read-write).

     > [!NOTE]
     >
     > If your application requires the `ReadWriteMany` mode, [contact support](https://console.nebius.com/support/create-ticket) before creating the PV.

   * `.spec.csi.volumeHandle`: String that identifies the PV. The volume handle must be unique for each volume in your cluster.

   * `.spec.csi.volumeAttributes.bucketName`: Name of your bucket.

   `.spec.mountOptions.maximum-throughput-gbps` and `.spec.mountOptions.max-threads` are recommended performance settings. For more details, see [Performance](#performance).

6. Create a PersistentVolumeClaim (PVC):

   ```bash theme={null}
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: s3-mountpoint
     namespace: soperator
   spec:
     accessModes:
       - ReadOnlyMany     # Must match the access modes of your PV
     storageClassName: "" # Empty string required for static provisioning
     resources:
       requests:
         storage: 1Ti          # Required by Kubernetes but effectively ignored
     volumeName: s3-mountpoint # Must match the name of your PV
   EOF
   ```

   `.spec.accessModes` and `.spec.volumeName` must match the access modes and the name of your PV, respectively.

7. Use the PVC to mount the PV to your Pod:

   ```bash theme={null}
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: storage-test-app
   spec:
     volumes:
       - name: bucket
         persistentVolumeClaim:
           claimName: s3-mountpoint # Must match the name of your PVC
     containers:
       - name: app
         image: centos
         command: ["/bin/sh"]
         args: ["-c", "while true; do echo $(date -u) >> /data/out.txt; sleep 5; done"]
         volumeMounts:
           - name: bucket
             mountPath: /data
   EOF
   ```

## Performance

To optimize performance when mounting buckets, you can configure the following parameters:

### maximum-throughput-gbps

The `--maximum-throughput-gbps` parameter raises the maximum throughput limit. The default limit is 1.25 GB/s (10 Gbps). For example, to set it to 10000 Gbps:

```bash theme={null}
mount-s3 bucket ./bucket --maximum-throughput-gbps 10000
```

In Kubernetes, specify this in the `mountOptions` of your PersistentVolume:

```yaml theme={null}
mountOptions:
  - maximum-throughput-gbps 10000
```

### max-threads

The `--max-threads` parameter raises the maximum number of threads. The default is 16. For example, to set it to 64:

```bash theme={null}
mount-s3 bucket ./bucket --max-threads 64
```

In Kubernetes, specify this in the `mountOptions` of your PersistentVolume:

```yaml theme={null}
mountOptions:
  - max-threads 64
```

### metadata-ttl

The `--metadata-ttl` parameter controls how long metadata is cached. Consider setting it to 120 seconds for better performance. For example:

```bash theme={null}
mount-s3 bucket ./bucket --metadata-ttl 120
```

For more information, see the [official documentation](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md#metadata-cache).

### UNSTABLE\_MOUNTPOINT\_MAX\_PREFETCH\_WINDOW\_SIZE

If you need to maximize the throughput within a single file, you can set the `UNSTABLE_MOUNTPOINT_MAX_PREFETCH_WINDOW_SIZE` environment variable. For example:

```bash theme={null}
UNSTABLE_MOUNTPOINT_MAX_PREFETCH_WINDOW_SIZE=8589934592 mount-s3 bucket ./bucket
```

> [!WARNING]
>
> This feature is unstable and not recommended for default use, as it can lead to uncontrollable memory consumption.
