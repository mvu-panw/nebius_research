# Usage data conformance with FOCUS

Source: https://docs.nebius.com/signup-billing/usage/focus-conformance

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Usage data conformance with FOCUS

Usage data that you [export from Nebius AI Cloud](https://docs.nebius.com/signup-billing/usage/export.md) is conformant with the [FinOps Open Cost and Usage Specification (FOCUS) 1.2](https://focus.finops.org/focus-specification/v1-2/). This article describes existing conformance gaps and their workarounds.

## Supported features

Nebius supports the following FOCUS-related capabilities:

| Capability | Support |
| - | - |
| Availability zones | No |
| Capacity reservations | No |
| Commitment discounts | Yes |
| Multi-currency pricing | Yes |
| Multiple billing account types | Yes |
| Multiple sub account types | No |
| Regions | Yes |
| Resource-based billing | Yes |
| SKU pricing | Yes |
| Sub accounts | No |
| Tags | No |
| Unit pricing | Yes |

A capability is a higher-level FOCUS feature that can map to one or more fields in the exported CSV. For example, the regions capability maps to `RegionId` and `RegionName`. For more information about the exported fields, see [FOCUS fields](https://docs.nebius.com/signup-billing/usage/focus-fields.md).

## Deviations

Usage data provided by Nebius AI Cloud has three deviations from the FOCUS specification. All three relate to [commitment discounts](https://docs.nebius.com/signup-billing/billing-models/committed-usage.md). Workarounds differ depending on the commitment discount type:

* **Resource-based**: a commitment to a predetermined amount of resource usage. Resource-based commitment discounts can be prepaid or postpaid.
* **Spend-based**: a commitment to a predetermined amount of spend. Spend-based rows have `BilledCost = 0`.

Each row in the table below describes the affected column, the specification requirement, the deviation and what you can do instead.

| Column | Specification | Deviation | Workaround |
| - | - | - | - |
| `CommitmentDiscountCategory` | `CommitmentDiscountCategory` must indicate whether the commitment discount identified in `CommitmentDiscountId` is based on a predetermined amount of spend or resource usage. Allowed values are `Spend` and `Usage`. | Spend-based commitments are not classified as a distinct commitment discount category. | Do not rely on `CommitmentDiscountCategory` to distinguish spend-based commitment discounts. **Spend-based:** for cost analysis, multiply `ConsumedQuantity` by the unit price from your contract instead of using `EffectiveCost`. |
| `ChargeCategory` | Purchases of commitment discounts must use `ChargeCategory = Purchase`. | Commitment discount purchases are not modeled as `ChargeCategory = Purchase` rows. **Resource-based:** postpaid commitment discounts appear as `ChargeCategory = Adjustment` rows. Prepaid commitment discounts are represented through amortized `EffectiveCost` on usage rows rather than as separate purchase rows. **Spend-based:** the commitment discount is not modeled as a separate purchase row. | **Resource-based:** for both postpaid and prepaid commitment discounts, `EffectiveCost` reflects the net cost after the commitment discount is applied. `Adjustment` rows do not include `CommitmentDiscountId` or `SkuId`, so you cannot programmatically link them to specific commitment discounts. To see how commitment discounts affect costs by service, use `EffectiveCost` on usage rows. Do not reconcile `Adjustment` rows to individual commitments. **Spend-based:** for cost analysis, multiply `ConsumedQuantity` by the unit price from your contract instead of using `EffectiveCost`. |
| `EffectiveCost` | Commitment discounts must be amortized. The sum of `EffectiveCost` for commitment usage and unused commitment discount rows must be equal to the `BilledCost` of the corresponding purchase. | Because commitment discount purchases are not modeled as `ChargeCategory = "Purchase"` rows (see deviation above), whether the original purchase amount matches the `EffectiveCost` sums cannot be verified. | This deviation prevents row-level amortization reconciliation against the original purchase. **Resource-based:** the commitment discount is reflected in `EffectiveCost` at the line-item level. For postpaid commitments, identify the total commitment value from `ChargeCategory = "Adjustment"` rows. For prepaid commitments, take the total of `EffectiveCost` at the line-item level. **Spend-based:** for cost analysis, multiply `ConsumedQuantity` by the unit price from your contract instead of using `EffectiveCost`. |

## Known industry limitations

Known industry limitations (KILs) are billing model constraints that affect multiple data providers and can be treated as exceptions. These limitations are excluded from the deviation count for FOCUS certification. For more information on KILs, see [KIL Exception Requests](https://www.finops.org/certification-for-organizations/finops-certified-focus-conformant/#Known-Industry-Limitations-Exception-Requests).

Usage data provided by Nebius AI Cloud has one KIL:

| Column | Specification | Limitation | Workaround |
| - | - | - | - |
| `ConsumedQuantity` | `ConsumedQuantity` represents actual consumption. | The value includes minimum billing increments. | **Cost analysis:** use `PricingQuantity`, not `ConsumedQuantity`. **Short-duration workloads:** expect `ConsumedQuantity` to overstate actual usage by up to the minimum increment. **Cross-provider comparison:** normalize to the largest minimum increment in the dataset. |
