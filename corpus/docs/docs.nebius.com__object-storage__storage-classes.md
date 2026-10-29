# Storage classes in Object Storage

Source: https://docs.nebius.com/object-storage/storage-classes

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Storage classes in Object Storage

Object Storage provides *storage classes* that control the cost and speed of storing and processing objects in storage, depending on desired access patterns. You can set the default storage class for each bucket and explicitly upload an object to a specific class.

The following storage classes are available:

* **Enhanced Throughput** (`ENHANCED_THROUGHPUT` for CLIs and tools) for storage that requires high bandwidth and low latency access.
* **Intelligent** (`INTELLIGENT`) for automatic cost savings on rarely accessed data.
* **Standard** (`STANDARD`) for general storage needs. Default option for new buckets.

> [!TIP]
>
> You can set up [lifecycle rules](https://docs.nebius.com/object-storage/objects/lifecycles.md#transition-lifecycle-rules) to transition objects between classes.

## Enhanced Throughput storage class

The Enhanced Throughput storage class differs from the Intelligent and Standard classes in the following ways:

* Unthrottled upload and download speed for Enhanced Throughput. In contrast, the upload and download speed for objects of the Intelligent and Standard classes is limited to 20 GBps per tenant in each [region](https://docs.nebius.com/overview/regions.md). The same limit applies when a transition lifecycle rule moves objects to or from the other classes. This means that during lifecycle transitions, the upload/download speed via the S3 API may be reduced.

* 2x latency improvement (on larger objects) and up to 10x throughput improvement per GiB of stored data compared to the Intelligent and Standard classes (when the bucket and the client are in the same Nebius AI Cloud region).

* You pay a higher price for storage size, but all operations and data egress are free. See the detailed cost breakdown in [Pricing in Object Storage](https://docs.nebius.com/object-storage/resources/pricing.md).

You may find the Enhanced Throughput storage class useful in the following scenarios:

* Stream processed datasets or model weights to GPU.
* Write or read checkpoints.
* Provide a destination for an extract, transform and load process (ETL) that requires high throughput.

## Intelligent storage class

The Intelligent storage class automatically optimizes storage costs for large datasets that haven't been accessed for a long time. Use this class when you can't predict which data you will access frequently and which rarely.

This class includes two *tiers*: Warm and Cold. All data is stored under the Warm tier by default. If you don't access some objects within 30 days, Object Storage automatically switches their tier to Cold. In practice, this often happens up to 48 hours earlier.

When the tier changes, the service doesn't transfer objects anywhere else. They remain in the same location, and their storage performance also stays the same. The only difference between the tiers is the [price](https://docs.nebius.com/object-storage/resources/pricing.md#storing-data) — the Cold tier costs less.

Object Storage considers an object of the Intelligent class to be accessed when you:

* Invoke the `CopyObject`, `UploadPartCopy` or `GetObject` [S3 methods](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html).

  Other methods don't affect the tier. For example, `HeadObject`, `GetObjectTagging` and `PutObjectTagging`.

* Download an object.

* Copy object data.

* Upload a new object version.

Once you access an object, the number of days for the switch is reset. For objects in the Cold tier, the tier switches to Warm once you access the object.

To determine what tier an object currently has, use the `HeadObject` method in the AWS API.

> [!WARNING]
>
> The Warm tier always applies to objects less than 180 KiB and to incomplete multipart uploads. They are not eligible for automatic tiering.
