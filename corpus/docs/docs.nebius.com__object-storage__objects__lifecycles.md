# Lifecycle rules for objects in Object Storage

Source: https://docs.nebius.com/object-storage/objects/lifecycles

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Lifecycle rules for objects in Object Storage

Object Storage supports two types of lifecycle rules: expiration lifecycle rules and transition lifecycle rules.

## Expiration lifecycle rules

When *expiration lifecycle rules* apply, Object Storage deletes objects and their versions in a bucket once they expire. For example, you can configure a rule that deletes objects a week after their upload to a bucket.

Besides deleting objects, you can also use expiration rules to delete non-current versions of objects and to abort multipart uploads that remain stale for a long time. Expiration rules are the most effective method for these purposes.

Use expiration rules when you want to clean up objects and versions that you do not need anymore. This can help you save bucket space, pay less for storage and stay within [quotas](https://docs.nebius.com/object-storage/resources/quotas-limits.md).

If you need to operate with certain objects, you can filter them. For instance, you can only delete objects that have a certain prefix in their name, have certain tags, or that do or do not exceed the specified size limit.

### Automatic deletion of incomplete uploads

For buckets created on or after November 9, 2026, Object Storage automatically deletes incomplete multipart uploads after 30 days. To change this behavior, [create an expiration lifecycle rule](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-expiration-lifecycle-rules) to abort incomplete multipart uploads according to your preferred pattern. Creating such a rule disables the default automatic deletion, even if you set the rule status to disabled.

## Transition lifecycle rules

When *transition lifecycle rules* apply, Object Storage changes the [storage class](https://docs.nebius.com/object-storage/storage-classes.md) of objects. For example, you can automatically downgrade from Enhanced Throughput to the Standard or Intelligent class when you no longer need higher bandwidth and lower latency. As a result, you pay less.

One of the following conditions can trigger the storage class switch:

* A specified date has arrived.
* A specified number of days has passed since the *object upload*.
* A specified number of days has passed since the *last access* to the object.

### Last-access lifecycle rules

A *last-access lifecycle rule* is a transition lifecycle rule that triggers the switch of the storage class if a certain number of days has passed since the last access to the object. Object Storage considers an object to be accessed if data was retrieved or copied from this object by using [S3 methods](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html), such as `GetObject`, `HeadObject`, `GetObjectTagging`, `CopyObject` and `UploadPartCopy`.

Object Storage considers these methods only if they were executed successfully. If there was an error, such as a permission denied or a connection broken, Object Storage doesn't detect the object access.

For last-access lifecycle rules, you can filter the S3 methods and user agents to detect the timestamp of the object's last access. For example, you can configure a filter that allows Object Storage to detect the last access only if the `CopyObject` method was executed by using the `rclone` user agent.

Filters apply to all last-access lifecycle rules. You configure them at the bucket level.

By default, no filters apply. All S3 methods (GetObject, HeadObject, GetObjectTagging, CopyObject and UploadPartCopy.) and user agents are included.

## How Object Storage triggers a lifecycle rule

After you [configure a lifecycle rule](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md), Object Storage checks every night (approximately after midnight UTC) whether a condition for expiration or transition is met. If it is, Object Storage triggers a rule.

### Limitations in triggering a last-access lifecycle rule

Last-access lifecycle rules have several limitations related to triggering a rule:

* The calculation precision of the last object access is 12 hours. Because of this, the transition to a different storage class may occur not the day the condition is met but the day after that.

* The service may opt not to consider a too-recent access of an object that was made several hours or minutes ago. For instance, if the object data was retrieved less than an hour ago, but the previous object access was a long time ago, a lifecycle rule can still apply.

* The service calculates the number of days since the moment you enable a lifecycle rule with the `days_since_last_access` [parameter](https://docs.nebius.com/object-storage/objects/configure-lifecycle-rules.md#how-to-configure-transition-lifecycle-rules). Imagine that an object has not been accessed within six months, and you create and enable a rule today with `days_since_last_access = 7`. In this case, the rule will apply after seven days; the rule will not consider the previous six months.

* Rarely, Object Storage can switch a storage class even if an object was accessed.

## Changes in charging when lifecycle rules apply

The service changes the [billing charges](https://docs.nebius.com/object-storage/resources/pricing.md) in the following way:

* When an expiration rule is triggered, charging for the used space stops only after objects are deleted. The occupied space on a bucket is recalculated with each object deleted.
* When a transition rule is triggered, the service starts charging for a new storage class only after the transition is finished. The charging is recalculated with each object that has the storage class switched.
