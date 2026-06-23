# Pricing

## Pricing Ladder

The initial public ladder is simple:

| Plan | Price | Intended buyer | Included license |
|---|---:|---|---|
| Starter | $10/month | solo trial or light personal use | 1 seat / 1 device |
| Pro | $29/month | main solo professional user | 1 seat / 2 devices |
| Office | $50/month | small office starter plan | 3 seats or 3 devices |

The core ladder is $10 / $29 / $50. It should stay consistent across product, sales, and docs until customer interviews prove a different structure is needed.

If an internal note refers to a "0 / 9 / 0" ladder, this scaffold treats it as shorthand for the same three-tier Starter / Pro / Office ladder from the source docs. It is not a fourth pricing proposal and should not override the documented $10 / $29 / $50 prices.

## Seat and Device Licensing

Licensing should be understandable without SaaS jargon:

- A seat is a person who can sign in and use the product.
- A device is a registered Windows app installation.
- Plans include a seat/device allowance.
- The app checks license status at login and periodically after.
- Users should be able to release an old device and register a new one.

This protects the business from simple app sharing while still fitting small professional offices.

## LLM Included by Default

The default subscription includes LLM usage. Customers should not need to bring an API key or choose a model provider.

The product should manage:

- provider selection
- low-cost model routing for routine tasks
- fallback routing when a provider fails
- usage metering
- soft limits for abnormal use
- cost visibility inside the admin system

User-facing copy should say that AI usage is included for normal professional workflows, subject to fair-use limits.

## BYOK Policy

BYOK is an advanced option only.

It may be useful for:

- firms that already have approved provider contracts
- users who require a specific model account
- high-volume users who want direct cost control
- enterprise or regulated deployments

BYOK should not appear in the default onboarding path. It can live behind an advanced settings screen or a higher-support sales flow.

## Early Pricing Risks

- $10 may be too low if LLM usage is heavy.
- $50 may need clearer seat/device language before small offices buy it.
- Unlimited wording can create cost exposure.
- BYOK can confuse the target user if presented too early.

## Pricing Validation Questions

- Does the accountant or lawyer understand the plan from the pricing table alone?
- Does Office feel like a small-office plan rather than an enterprise plan?
- Does included LLM usage reduce onboarding friction?
- Do users accept seat/device limits as fair for installed desktop software?
