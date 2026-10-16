---
name: amazon-free
description: Always search Amazon.de as a shopping channel, including quantity variants, delivered total, Prime/non-Prime differences, availability, and returns. Use public browser/indexed information without paid Amazon APIs.
metadata:
  version: "1.0.0"
---

# Amazon Free: German Shopping Comparison

Invoke whenever another shopping skill is comparing purchasable goods, **even if the user has not provided an Amazon link**. Do not presume that dm/Rossmann, Idealo or Geizhals will find the cheapest usable quantity. Conversely do not assume Amazon is best because delivery is convenient.

## Research

1. Search Amazon.de for the exact product and suitable alternatives, using permitted ordinary web search (`site:amazon.de/dp/ "product model"`) or the agent's browser. Try brand name, exact model, GTIN/EAN and compatible bulk-pack variants. Amazon may block automated browsers; public search-index snippets are useful leads, not current pricing verification.
2. For supplied `amzn.eu`, `amzn.to` or `a.co` short URLs, invoke the shared `keepa-free/scripts/keepa_lookup.py` helper for header-based redirect resolution. It outputs a clean Amazon product URL without affiliate, referrer, session or tracking parameters. Never follow unrelated-domain redirects.
3. For each relevant offer identify exact seller and fulfiller (sold by Amazon, third party fulfilled by Amazon, or third-party shipping), condition, variant, volume per container, number of containers, total volume or number of pieces, item total, and listing status. Price per litre, kilogram or piece must be calculated from the *entire purchased quantity* rather than only the front-facing package size.
4. Search small singles AND larger containers/multipacks. A larger container may be better value per litre even if the upfront cost is higher, but flag expiry, storage and risk of waste. Don't confuse delivery fees with per-unit item cost.
5. Identify both **non-Prime** and **Prime** delivered totals when verifiable. Never assume the user has Prime. Report coupons, Subscribe & Save, add-on item restrictions, delivery subscriptions, minimum order values, preconditions and mandatory fees separately. Only count explicitly applicable discounts.
6. Verify deliverability and stock with an accessible current product page and, if available, cart/checkout. Product-page stock and indexed snippets may conflict: label the source and mark uncertainties. Never claim checkout confirmed without checking checkout.
7. Report return time frame in calendar days, cost/payer of return shipping, any product/seller-specific exception, unsealed hygiene restrictions, refund deductions, and separate warranty information. Don't assume all Amazon sellers offer the same return policy.
8. Use Keepa chart history only when actually readable; don't mistake graph history for current Amazon stock or price.
9. Keep the best legitimate Amazon candidate in the final shortlist and explicitly compare its delivered total, delivered unit cost, purchase minimum, convenience, availability and return economics against local shop / Idealo / Geizhals choices. If all Amazon sources are blocked, say **Amazon not verified**, never **no Amazon offers**.

## Evidence, safety and privacy

Use `checkout-confirmed`, `listing-in-stock`, `indexed-only`, `user-reported`, `sold-out` or `blocked` evidence labels. Do not invent Prime eligibility, fees, discounts, or current stock. Never publish specific user shopping URLs, product histories, postcode, local coordinates, account status, login cookies, checkout data or API tokens to a repository, issue, commit, public log or shared prompt template.

The skill is an independent research workflow, not an Amazon scraping service, and it requires no paid Amazon API.
