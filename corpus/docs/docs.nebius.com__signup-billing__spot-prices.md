# Getting spot prices in Nebius AI Cloud

Source: https://docs.nebius.com/signup-billing/spot-prices

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting spot prices in Nebius AI Cloud

Spot prices of preemptible GPU platforms and their history are public. You can view them via the Nebius website, the web console or the API. Use spot prices to estimate the cost of preemptible resources, to choose a region where a GPU platform price is lower or to set the max price for a [pricing policy](https://docs.nebius.com/signup-billing/manage-pricing-policy.md).

Each price is set for one GPU hour on a GPU platform in a region. The website, the web console and the API show the history for up to 30 days.

For information about how spot prices are set and charged, see [Spot pricing and pricing policies](https://docs.nebius.com/signup-billing/pricing-policy.md).

## Prerequisites

You don't need a Nebius AI Cloud account to view spot prices on the website or to get them by using the API.

To get spot prices by using the Nebius AI Cloud CLI, [install and configure](https://docs.nebius.com/cli/install.md) it.

## How to get current spot prices

**Website**

1. Open the [Spot Preemptible VM prices](https://nebius.com/spot-prices) page on the Nebius website.

2. (Optional) Filter the page by GPU platform:

   * To view the prices of one GPU platform, select it in the **All GPUs** list.
   * To view the prices of GPU platforms that match a search query, enter the query in **Search GPUs**. For example, enter `B` to view the prices of B300 and B200.

3. Check the current spot prices:

   * In the **Explore live prices per GPU platform** section, the cards show the lowest price per GPU hour for each GPU platform, the region where this price is available and how the price changed over the last day. In this section:

     * To view the change over the last 7 or 30 days, select **7 days** or **30 days**.
     * To view the price at a specific time, hover over the chart in the card.
     * To compare the prices of a GPU platform in all regions, select its card. This opens the **Price history** section.

   * In the **All live prices** section, the table shows the price of each GPU platform in each region and the time since when the price is effective. To find a GPU platform or region, use the search. To sort the table, click a column name.

**Web console**

1. Open the [web console](https://console.nebius.com).
2. In the **Preemptible VM spot prices** section, check the cards. Each card shows the lowest spot price per GPU hour for a GPU platform and the region where this price is available.

   The section only shows GPU platforms that have available capacity in at least one region of your projects. The capacity data comes from the [capacity advisor](https://docs.nebius.com/compute/virtual-machines/capacity-advisor.md).

To create a VM on one of these GPU platforms, click  on its card.

To view the prices in all regions and their history, click **View all prices**. The [Spot Preemptible VM prices](https://nebius.com/spot-prices) page opens on the Nebius website.

**CLI**

Run the following command:

```bash theme={null}
nebius billing v1alpha1 spot-price list --all
```

`--all` returns the prices of all SKUs at once. To get the results page by page, use `--page-size` and `--page-token` instead.

The output contains one item for each SKU: the SKU ID, product name, region, GPU platform, price and the time when the price took effect.

**REST API**

Send a `GET` request to `https://api.nebius.cloud/billing/v1alpha1/spot-price`. The request doesn't require authentication. For the API reference, see [SpotPriceService](https://api.nebius.cloud/openapi#/nebius.billing.v1alpha1.SpotPriceService).

Example request:

```bash theme={null}
curl https://api.nebius.cloud/billing/v1alpha1/spot-price
```

Query parameters:

| Parameter | Required | Description |
| - | - | - |
| `pageSize` | No | Maximum number of items in the response. If you don't specify the parameter or set it to 0, the value is 100. |
| `pageToken` | No | Token from `nextPageToken` of the previous response. |

The response contains one item for each SKU, sorted by region and then by SKU ID. Each SKU is a GPU platform in a region. Each item contains the following fields:

* `skuId`: SKU ID. You can use this ID to get the [spot price history](#how-to-get-spot-price-history) of the SKU.
* `productTitle`: Product name, for example, `Preemptible NVIDIA® B200 NVLink`.
* `region`: Region name, for example, `eu-north1`. For the list of regions, see [Regions](https://docs.nebius.com/overview/regions.md).
* `computeInstance.platform`: GPU platform ID, for example, `gpu-b200-sxm`. For the list of GPU platforms, see [Types of virtual machines and GPUs](https://docs.nebius.com/compute/virtual-machines/types.md#gpu-types).
* `price.value`, `price.currency` and `price.unitTitle`: Price for one unit, its currency and unit, for example, `2.89`, `usd` and `GPU hour`. For information about how spot prices are charged, see [How spot pricing works](https://docs.nebius.com/signup-billing/pricing-policy.md#how-spot-pricing-works).
* `effectiveTime`: Time when the price took effect.

The response also contains `snapshotTime`, the time when the prices were taken. If the prices were taken at different times, `snapshotTime` is the earliest of them.

Example response:

```json theme={null}
{
  "items": [
    {
      "skuId": "sku-e00***",
      "productTitle": "Preemptible NVIDIA® H200 NVLink",
      "region": "eu-north1",
      "computeInstance": {
        "platform": "gpu-h200-sxm"
      },
      "price": {
        "value": "2.89",
        "currency": "usd",
        "unitTitle": "GPU hour"
      },
      "effectiveTime": "2026-10-16T05:56:00Z"
    }
  ],
  "snapshotTime": "2026-10-16T06:07:25.400147Z"
}
```

If the response contains a non-empty `nextPageToken`, pass it in `pageToken` to get the next page.

**gRPC API**

Call the `List` method of `SpotPriceService` at `pricing-policies.billing-cpl.api.nebius.cloud:443`. The request doesn't require authentication. For the service definition, see [spot\_price\_service.proto](https://github.com/nebius/api/blob/main/nebius/billing/v1alpha1/spot_price_service.proto).

For example, use [grpcurl](https://docs.nebius.com/grpc-api/calls/invoke-methods.md):

```bash theme={null}
grpcurl pricing-policies.billing-cpl.api.nebius.cloud:443 \
  nebius.billing.v1alpha1.SpotPriceService/List
```

Request fields:

| Field | Required | Description |
| - | - | - |
| `pageSize` | No | Maximum number of items in the response. If you don't specify the field or set it to 0, the value is 100. |
| `pageToken` | No | Token from `nextPageToken` of the previous response. |

The response contains one item for each SKU, sorted by region and then by SKU ID. Each SKU is a GPU platform in a region. Each item contains the following fields:

* `skuId`: SKU ID. You can use this ID to get the [spot price history](#how-to-get-spot-price-history) of the SKU.
* `productTitle`: Product name, for example, `Preemptible NVIDIA® B200 NVLink`.
* `region`: Region name, for example, `eu-north1`. For the list of regions, see [Regions](https://docs.nebius.com/overview/regions.md).
* `computeInstance.platform`: GPU platform ID, for example, `gpu-b200-sxm`. For the list of GPU platforms, see [Types of virtual machines and GPUs](https://docs.nebius.com/compute/virtual-machines/types.md#gpu-types).
* `price.value`, `price.currency` and `price.unitTitle`: Price for one unit, its currency and unit, for example, `2.89`, `usd` and `GPU hour`. For information about how spot prices are charged, see [How spot pricing works](https://docs.nebius.com/signup-billing/pricing-policy.md#how-spot-pricing-works).
* `effectiveTime`: Time when the price took effect.

The response also contains `snapshotTime`, the time when the prices were taken. If the prices were taken at different times, `snapshotTime` is the earliest of them.

Example response:

```json theme={null}
{
  "items": [
    {
      "skuId": "sku-e00***",
      "productTitle": "Preemptible NVIDIA® H200 NVLink",
      "region": "eu-north1",
      "computeInstance": {
        "platform": "gpu-h200-sxm"
      },
      "price": {
        "value": "2.89",
        "currency": "usd",
        "unitTitle": "GPU hour"
      },
      "effectiveTime": "2026-10-16T05:56:00Z"
    }
  ],
  "snapshotTime": "2026-10-16T06:07:25.400147Z"
}
```

If the response contains a non-empty `nextPageToken`, pass it in `pageToken` to get the next page.

## How to get spot price history

**Website**

1. On the [Spot Preemptible VM prices](https://nebius.com/spot-prices) page, go to the **Price history** section.
2. Select up to two GPU platforms and the regions. By default, the chart shows all GPU platforms and regions.
3. Select the time range: **1 day**, **7 days** or **30 days**.
4. (Optional) To highlight a region in the chart, select it under the chart. To hide a region, click **×** next to it.

**Web console**

1. In the [web console](https://console.nebius.com/billing), go to  **Billing** → **Pricing**.
2. Switch to the **Pricing history** tab.
3. Select the time range: **30d**, **7d** or **1d**.
4. In the **Platform** list, select the GPU platform.
5. (Optional) To view the prices in specific regions, select them in the **All regions** list. By default, the chart shows all regions.
6. (Optional) To view the prices at a specific time, hover over the chart.

**CLI**

Run the following command:

```bash theme={null}
nebius billing v1alpha1 spot-price list-series \
  --filters-start-time <start_time> \
  --aggregation-granularity granularity_hour_1 \
  --aggregation-method method_avg_price \
  --all
```

In this command:

* `--filters-start-time`: Start of the time interval, for example, `2026-10-14T00:00:00Z`. It must be within the last 30 days.
* `--aggregation-granularity`: Length of a time step: `granularity_minute_15` for 15 minutes or `granularity_hour_1` for 1 hour. You can use 15-minute steps if the time interval is 7 days or shorter.
* `--aggregation-method`: How the price of a time step is calculated: `method_first_price` for the first price in the step, `method_last_price` for the last price or `method_avg_price` for the mean of the prices. The mean is not weighted by time.
* `--all`: Returns the series of all SKUs at once. To get the results page by page, use `--page-size` and `--page-token` instead.

You can also specify the following parameters:

* `--filters-end-time`: End of the time interval, exclusive. The default value is the current time.
* `--filters-sku-ids`: Up to 100 SKU IDs. To get the SKU IDs, [get the current spot prices](#how-to-get-current-spot-prices). By default, the output contains all SKUs.

The output contains one series for each SKU: the SKU ID, product name, region, GPU platform, currency, unit and prices at time steps, from the oldest to the newest.

**REST API**

Send a `GET` request to `https://api.nebius.cloud/billing/v1alpha1/spot-price/list-series`. The request doesn't require authentication. For the API reference, see [SpotPriceService](https://api.nebius.cloud/openapi#/nebius.billing.v1alpha1.SpotPriceService).

Example request:

```bash theme={null}
curl --get https://api.nebius.cloud/billing/v1alpha1/spot-price/list-series \
  --data-urlencode "filters.startTime=<start_time>" \
  --data-urlencode "filters.endTime=<end_time>" \
  --data-urlencode "aggregation.granularity=GRANULARITY_HOUR_1" \
  --data-urlencode "aggregation.method=METHOD_AVG_PRICE" \
  --data-urlencode "pageSize=1"
```

To get the history of specific GPU platforms and regions, get their SKU IDs from the response for [current spot prices](#how-to-get-current-spot-prices), and then pass these IDs in `filters.skuIds`. Specify the parameter once for each ID.

Query parameters:

| Parameter | Required | Description |
| - | - | - |
| `filters.startTime` | Yes | Start of the time interval. It must be within the last 30 days. |
| `filters.endTime` | No | End of the time interval, exclusive. The default value is the current time. For example, the interval from 12:00 to 15:00 with `GRANULARITY_HOUR_1` returns the points at 13:00, 14:00 and 15:00. |
| `filters.skuIds` | No | Up to 100 SKU IDs. If you don't specify the parameter, the response contains all SKUs. |
| `aggregation.granularity` | Yes | Length of a time step:<ul><li>`GRANULARITY_MINUTE_15`: 15 minutes. Allowed if the time interval is 7 days or shorter.</li><li>`GRANULARITY_HOUR_1`: 1 hour.</li></ul> |
| `aggregation.method` | Yes | How the price of a time step is calculated:<ul><li>`METHOD_FIRST_PRICE`: The first price in the step.</li><li>`METHOD_LAST_PRICE`: The last price in the step.</li><li>`METHOD_AVG_PRICE`: The mean of the prices in the step. The mean is not weighted by time.</li></ul> |
| `pageSize` | No | Maximum number of series in the response. If you don't specify the parameter or set it to 0, the value is 100. |
| `pageToken` | No | Token from `nextPageToken` of the previous response. |

The response contains one series for each SKU, sorted by region and then by SKU ID. Each series contains the following fields:

* `skuId`, `productTitle`, `region`, `computeInstance`, `currency` and `unitTitle`: The same as in the response for current spot prices.
* `points`: Prices at time steps, from the oldest to the newest. Each point contains the following fields:

  * `value`: Price for the time step.
  * `timestamp`: End of the time step. For example, the point for the step from 12:00 to 13:00 has the `timestamp` of 13:00.

The response also contains `snapshotTime`, the time when the prices were taken. If the prices were taken at different times, `snapshotTime` is the earliest of them.

Example response for the interval from 12:00 to 15:00 with `GRANULARITY_HOUR_1` and `pageSize` set to 1:

```json theme={null}
{
  "items": [
    {
      "skuId": "sku-e00***",
      "productTitle": "Preemptible NVIDIA® H200 NVLink",
      "region": "eu-north1",
      "computeInstance": {
        "platform": "gpu-h200-sxm"
      },
      "currency": "usd",
      "unitTitle": "GPU hour",
      "points": [
        {
          "timestamp": "2026-10-15T13:00:00Z",
          "value": "2.89"
        },
        {
          "timestamp": "2026-10-15T14:00:00Z",
          "value": "2.89"
        },
        {
          "timestamp": "2026-10-15T15:00:00Z",
          "value": "3.05"
        }
      ]
    }
  ],
  "nextPageToken": "WyJl***",
  "snapshotTime": "2026-10-16T06:07:38.079172Z"
}
```

`pageSize` limits the number of series, it doesn't affect points. If the response contains a non-empty `nextPageToken`, pass it in `pageToken` to get the next page.

If the request parameters are invalid, the API returns the `400` HTTP status code with the `Request validation error` message. The `violations` list in the response contains the invalid parameter and one of the following messages:

* `Must be within the last 30 days`: `filters.startTime` is more than 30 days ago.
* `A time interval longer than 7 days allows only GRANULARITY_HOUR_1`: You use `GRANULARITY_MINUTE_15` for a time interval longer than 7 days.
* `Field required`: A required parameter is missing, for example, `aggregation`.

Example response for `filters.startTime` that is more than 30 days ago:

```json theme={null}
{
  "code": 3,
  "message": "Request validation error",
  "details": [
    {
      "@type": "type.googleapis.com/nebius.common.v1.ServiceError",
      "code": "BadRequest",
      "badRequest": {
        "violations": [
          {
            "field": "filters",
            "message": "Must be within the last 30 days"
          }
        ]
      }
    }
  ]
}
```

For more information about errors, see [Errors in the REST API](https://docs.nebius.com/rest-api/errors.md).

**gRPC API**

Call the `ListSeries` method of `SpotPriceService` at `pricing-policies.billing-cpl.api.nebius.cloud:443`. The request doesn't require authentication. For the service definition, see [spot\_price\_service.proto](https://github.com/nebius/api/blob/main/nebius/billing/v1alpha1/spot_price_service.proto). For example, use [grpcurl](https://docs.nebius.com/grpc-api/calls/invoke-methods.md):

```bash theme={null}
grpcurl -d '{
    "filters": {"startTime": "<start_time>", "endTime": "<end_time>"},
    "aggregation": {"granularity": "GRANULARITY_HOUR_1", "method": "METHOD_AVG_PRICE"},
    "pageSize": 1
  }' \
  pricing-policies.billing-cpl.api.nebius.cloud:443 \
  nebius.billing.v1alpha1.SpotPriceService/ListSeries
```

To get the history of specific GPU platforms and regions, get their SKU IDs from the response for [current spot prices](#how-to-get-current-spot-prices), and then pass these IDs in `filters.skuIds`.

Request fields, where a dot separates a nested object and its field:

| Field | Required | Description |
| - | - | - |
| `filters.startTime` | Yes | Start of the time interval. It must be within the last 30 days. |
| `filters.endTime` | No | End of the time interval, exclusive. The default value is the current time. For example, the interval from 12:00 to 15:00 with `GRANULARITY_HOUR_1` returns the points at 13:00, 14:00 and 15:00. |
| `filters.skuIds` | No | Up to 100 SKU IDs. If you don't specify the field, the response contains all SKUs. |
| `aggregation.granularity` | Yes | Length of a time step:<ul><li>`GRANULARITY_MINUTE_15`: 15 minutes. Allowed if the time interval is 7 days or shorter.</li><li>`GRANULARITY_HOUR_1`: 1 hour.</li></ul> |
| `aggregation.method` | Yes | How the price of a time step is calculated:<ul><li>`METHOD_FIRST_PRICE`: The first price in the step.</li><li>`METHOD_LAST_PRICE`: The last price in the step.</li><li>`METHOD_AVG_PRICE`: The mean of the prices in the step. The mean is not weighted by time.</li></ul> |
| `pageSize` | No | Maximum number of series in the response. If you don't specify the field or set it to 0, the value is 100. |
| `pageToken` | No | Token from `nextPageToken` of the previous response. |

The response contains one series for each SKU, sorted by region and then by SKU ID. Each series contains the following fields:

* `skuId`, `productTitle`, `region`, `computeInstance`, `currency` and `unitTitle`: The same as in the response for current spot prices.
* `points`: Prices at time steps, from the oldest to the newest. Each point contains the following fields:

  * `value`: Price for the time step.
  * `timestamp`: End of the time step. For example, the point for the step from 12:00 to 13:00 has the `timestamp` of 13:00.

The response also contains `snapshotTime`, the time when the prices were taken. If the prices were taken at different times, `snapshotTime` is the earliest of them.

Example response for the interval from 12:00 to 15:00 with `GRANULARITY_HOUR_1` and `pageSize` set to 1:

```json theme={null}
{
  "items": [
    {
      "skuId": "sku-e00***",
      "productTitle": "Preemptible NVIDIA® H200 NVLink",
      "region": "eu-north1",
      "computeInstance": {
        "platform": "gpu-h200-sxm"
      },
      "currency": "usd",
      "unitTitle": "GPU hour",
      "points": [
        {
          "timestamp": "2026-10-15T13:00:00Z",
          "value": "2.89"
        },
        {
          "timestamp": "2026-10-15T14:00:00Z",
          "value": "2.89"
        },
        {
          "timestamp": "2026-10-15T15:00:00Z",
          "value": "3.05"
        }
      ]
    }
  ],
  "nextPageToken": "WyJl***",
  "snapshotTime": "2026-10-16T06:07:38.079172Z"
}
```

`pageSize` limits the number of series, it doesn't affect points. If the response contains a non-empty `nextPageToken`, pass it in `pageToken` to get the next page.

If the request fields are invalid, the method returns the `InvalidArgument` status with the `Request validation error` message. The error details contain the invalid field and one of the following messages:

* `Must be within the last 30 days`: `filters.startTime` is more than 30 days ago.
* `A time interval longer than 7 days allows only GRANULARITY_HOUR_1`: You use `GRANULARITY_MINUTE_15` for a time interval longer than 7 days.
* `Field required`: A required field is missing, for example, `aggregation`.

For more information about errors, see [Errors in the gRPC API](https://docs.nebius.com/grpc-api/errors.md).

## See also

* [Spot pricing and pricing policies](https://docs.nebius.com/signup-billing/pricing-policy.md)
* [Managing pricing policies](https://docs.nebius.com/signup-billing/manage-pricing-policy.md)
* [Preemptible virtual machines](https://docs.nebius.com/compute/virtual-machines/preemptible.md)
* [Compute pricing](https://docs.nebius.com/compute/resources/pricing.md)
