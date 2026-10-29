# Data deletion in Nebius AI Cloud

Source: https://docs.nebius.com/overview/data-deletion

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Data deletion in Nebius AI Cloud

Nebius follows several rules for keeping security logs and preserving your Nebius AI Cloud data if you delete it or your tenant is suspended. These rules depend on the particular case and the type of resource you are working with.

## Data in deleted resources

### Data on Compute disks and in shared filesystems

When a Compute disk or a shared filesystem is deleted, data stored on it is deleted immediately after the volume is deleted. It is not possible to recover the data after it is deleted. This applies regardless of whether the disk or shared filesystem is attached to a Compute virtual machine, a resource in another Nebius AI Cloud service such as a node in a Managed Service for Kubernetes® cluster or not attached to any resource.

### Data in Object Storage buckets

When an object is deleted from a bucket in Object Storage, it becomes immediately inaccessible and cannot be restored. The actual object data is then physically deleted from Nebius AI Cloud servers within 4 days.

Deleted objects cannot be restored unless [bucket versioning](https://docs.nebius.com/object-storage/buckets/versioning.md) is enabled.

Deleting a bucket is only possible when it is empty, that is, has no objects left in it.

For more details on object and bucket deletion, see [How to delete objects](https://docs.nebius.com/object-storage/objects/manage.md#how-to-delete-objects) and [How to delete buckets](https://docs.nebius.com/object-storage/buckets/manage.md#how-to-delete-buckets).

## Data in suspended tenants

Your tenant can be suspended, for example, if you have not set up billing for it or you have not paid for resources used. Resources and data in the suspended tenant are deleted 60 days after the suspension. It is not possible to restore the resources and data.

If you no longer wish to use Nebius AI Cloud, delete your resources and data.

## Technical and security logs

Actions performed on data and resources in Nebius AI Cloud are logged to help with responding to information security incidents and preventing fraud.

The log record of an action is stored for 24 months and deleted permanently afterward.
