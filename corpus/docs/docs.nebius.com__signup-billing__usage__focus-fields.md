# FOCUS fields

Source: https://docs.nebius.com/signup-billing/usage/focus-fields

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# FOCUS fields

This reference explains the fields in Nebius AI Cloud usage exports. For the official definitions of FinOps Open Cost and Usage Specification (FOCUS) fields, see the [FOCUS Column Library](https://focus.finops.org/focus-columns/?version=v1-2). Nebius uses the standard FOCUS field names for FOCUS-defined fields and does not rename them in the export.

## FOCUS-defined fields

This table lists the FOCUS-defined fields that Nebius currently exports.

| Field | Description | Data type | Nullable |
| - | - | - | - |
| `BilledCost` | Cost used as the basis for invoicing after discounts are applied. | `double` | No |
| `BillingAccountId` | Identifier of the billing account. | `string` | No |
| `BillingAccountName` | Display name of the Nebius billing account. | `string` | Yes |
| `BillingAccountType` | Nebius billing account type, for example `individual` or `company`. | `string` | No |
| `BillingCurrency` | Currency in which the charge was billed. | `string` | No |
| `BillingPeriodEnd` | Exclusive end of the billing period. | `timestamp` | No |
| `BillingPeriodStart` | Inclusive start of the billing period. | `timestamp` | No |
| `ChargeCategory` | Highest-level classification of the charge, for example `Usage`, `Adjustment`, `Tax` or `Credit`, and this column has a [deviation](https://docs.nebius.com/signup-billing/usage/focus-conformance.md#deviations). | `string` | No |
| `ChargeClass` | Indicates whether the row is a correction to an earlier billing period. | `string` | Yes |
| `ChargeDescription` | Description of the Nebius charge, for example `Used space in Standard Storage` or `Network SSD disk`. | `string` | Yes |
| `ChargeFrequency` | How often the charge occurs, for example `Usage-Based` or `One-Time`. | `string` | No |
| `ChargePeriodEnd` | Exclusive end of the charge period. | `timestamp` | No |
| `ChargePeriodStart` | Inclusive start of the charge period. | `timestamp` | No |
| `CommitmentDiscountCategory` | Whether the commitment discount is based on usage or spend. This column has a [deviation](https://docs.nebius.com/signup-billing/usage/focus-conformance.md#deviations). | `string` | Yes |
| `CommitmentDiscountId` | Identifier of the commitment discount. | `string` | Yes |
| `CommitmentDiscountName` | Display name of the commitment discount. | `string` | Yes |
| `CommitmentDiscountQuantity` | Purchased or accounted commitment amount in commitment units. | `double` | Yes |
| `CommitmentDiscountStatus` | Whether the row reflects used or unused committed amount. | `string` | Yes |
| `CommitmentDiscountType` | Nebius-defined type of commitment discount. | `string` | Yes |
| `CommitmentDiscountUnit` | Unit used to measure the commitment discount quantity. | `string` | Yes |
| `ConsumedQuantity` | Metered usage amount for the consumed SKU. This column has a [known industry limitation](https://docs.nebius.com/signup-billing/usage/focus-conformance.md#known-industry-limitations). | `double` | Yes |
| `ConsumedUnit` | Unit used to measure consumed usage. | `string` | Yes |
| `ContractedCost` | Cost calculated from the contracted unit price and pricing quantity. | `double` | No |
| `ContractedUnitPrice` | Agreed unit price before commitment discounts and other discounts. | `double` | Yes |
| `EffectiveCost` | Amortized cost after discounts and applicable prepaid purchases. This column has a [deviation](https://docs.nebius.com/signup-billing/usage/focus-conformance.md#deviations). | `double` | No |
| `InvoiceIssuerName` | Name of the entity that issues the invoice in Nebius. | `string` | No |
| `ListCost` | Cost calculated from list unit price and pricing quantity. | `double` | No |
| `ListUnitPrice` | Published unit price before discounts. | `double` | Yes |
| `PricingCategory` | Pricing model used for the charge, for example `Standard`, `Committed` or `Other`. | `string` | Yes |
| `PricingCurrency` | Currency in which the Nebius resource or service was priced. | `string` | Yes |
| `PricingCurrencyContractedUnitPrice` | Contracted unit price expressed in pricing currency. | `double` | Yes |
| `PricingCurrencyEffectiveCost` | Effective cost expressed in pricing currency. | `double` | Yes |
| `PricingCurrencyListUnitPrice` | List unit price expressed in pricing currency. | `double` | Yes |
| `PricingQuantity` | Quantity rated for pricing. | `double` | Yes |
| `PricingUnit` | Unit used to determine unit prices after pricing rules are applied. | `string` | Yes |
| `ProviderName` | Name of the provider that made the Nebius service available, for example `Nebius B.V.`. | `string` | No |
| `PublisherName` | Name of the entity that published the Nebius service, for example `Nebius B.V.`. | `string` | No |
| `RegionId` | Nebius region identifier, for example `eu-north1`. | `string` | Yes |
| `RegionName` | Nebius region identifier, for example `eu-north1`. | `string` | Yes |
| `ResourceId` | Identifier of the resource. | `string` | Yes |
| `ResourceName` | Display name of the resource. | `string` | Yes |
| `ResourceType` | Type of Nebius resource the charge applies to, for example `storagebucket`, `computedisk` or `computeinstance`. | `string` | Yes |
| `ServiceCategory` | Highest-level Nebius service classification, for example `Storage` or `Management and Governance`. | `string` | No |
| `ServiceName` | Name of the Nebius service, for example `Object Storage` or `Billing`. | `string` | No |
| `SkuId` | Unique identifier of the SKU. | `string` | Yes |
| `SkuMeter` | What the Nebius SKU measures, for example `Object Storage Usage`, `Block Volume Usage` or `Compute Usage`. | `string` | Yes |
| `SkuPriceDetails` | Additional properties associated with the SKU price. | `map<string, string>` | Yes |
| `SkuPriceId` | Unique identifier of the SKU price. | `string` | Yes |
| `Tags` | Cost allocation labels that show how costs are distributed between different groups of resources. | `map<string, string>` | Yes |

## Nebius-specific fields

Fields that start with `x_` are Nebius-specific extensions and are not part of the FOCUS specification.

| Nebius field | Description | Data type | Nullable |
| - | - | - | - |
| `x_ContainerId` | Identifier of the Nebius resource hierarchy container, such as a project. | `string` | No |
| `x_ContainerName` | Display name of the Nebius resource hierarchy container, for example a project such as `default-project`. | `string` | No |
| `x_TrialId` | Identifier of the Nebius trial associated with the charge, if any. | `string` | Yes |
| `x_ContractPriceId` | Identifier of the Nebius contract price, if any, applied when calculating `ContractedCost`. | `string` | Yes |
| `x_UsageBasedDiscountIds` | Identifiers of usage-based discounts applied when calculating `ContractedCost`. | `array` | Yes |
