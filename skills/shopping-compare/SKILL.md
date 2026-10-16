---
name: shopping-compare
description: Compare real total checkout costs, per-unit value, availability, delivery and returns for German shopping. Always check Amazon as well as appropriate price comparators and physical stores.
metadata:
  version: "2.0.0"
---
# Shopping Compare: Germany

## Required research sweep
1. Clarify the *product*, exact model/size/quantity, intended use, and any important quality constraints. Do not assume a larger package is practical for the user.
2. **ALWAYS search Amazon.de** using `amazon-free`, even when the user did not supply an Amazon link and even when a local store looks cheaper. Check first-party and relevant professional third-party sellers, multiple pack sizes, bulk and multipack offers. A supplied Amazon link or unit price is an important lead and must never be silently dropped.
3. Check `idealo-free` and, when appropriate to the category, `geizhals-free` for competing online shops. Use `local-store-de` to check relevant local retailers such as dm, Rossmann, Müller and Decathlon. Compare `refurbished-de` only for suitable durable devices when professionally refurbished goods meet the user's needs.
4. For each channel write down what was actually checked, including dates, access failures and offers that appear sold out. If Amazon or another source blocks the agent, try an allowed public search-index result, user-provided product details, or a browser that the agent already controls. Do not pretend a blocked retailer has no relevant offers.
5. Search variants that can substantially change value: single bottle vs multipack, 100 mL vs 500 mL vs 1 L, larger packs, subscription options, seller differences. For personal-care consumables compare safe, suitable formulations rather than price alone. Separate product suitability from price ranking.

## Price normalization (mandatory)
For EVERY shortlisted offer show: product, merchant/seller, size of each container, pack count, **total purchased quantity**, headline **price per liter/kg/item**, and **effective price per liter/kg/item including delivery and mandatory fees**. Show the minimum payable order total too. Standardize package units (mL/L, g/kg, count); never compare package stickers as if sizes were equal.

`delivered_total = item_total + shipping + mandatory checkout/payment/service charges - discounts that are actually confirmed applicable`

`delivered_unit_cost = delivered_total / quantity_in_base_units`

Consider price and delivery separately for **Amazon Prime**, non-Prime, Subscribe & Save, vouchers and collection. Do not grant the user Prime or a coupon without evidence. If shipping or fees cannot be verified, mark the final total **Not verified**, and do not sort the offer as a confirmed cheapest total. A displayed per-unit price is not a delivered per-unit price. Distinguish the **lowest unit price** from the **lowest spend today**, convenience, freshness, return economics and suitability. Larger bottles may have expiry, waste or storage trade-offs.

An offline cross-checking tool is available: `python3 scripts/offer_math.py --file offers.json`. It does not scrape retailer data and requires explicit shipping inputs for a verified calculation.

## Availability and evidence (mandatory)
Use these evidence states consistently:
- `checkout-confirmed`: buyer-specific checkout/cart shows the final total and deliverable stock;
- `listing-in-stock`: currently accessible product page indicates availability, but checkout not tested;
- `store-confirmed`: branch and price specifically verified;
- `user-reported`: supplied link/price, not independently verified;
- `indexed-only`: search snippet without live stock confirmation;
- `sold-out`, `blocked`, `unsearched`.

**Before declaring any winner:** cross-check the current product listing against its retailer catalogue/search page when accessible; check variant and stock messages and checkout restrictions. An old indexed price, unavailable listing or page with contradictory stock status is NEVER a confirmed winner. If no live offer is verifiable, give a conditional ranking and state this upfront. Include observation date, exact product link, and evidence source for each candidate.

## Returns, fees and guarantees (mandatory)
For EVERY shortlisted offer report:
- Item total, shipping, mandatory fees, confirmed applicable discounts, **delivered total**;
- Return period in calendar days and when the clock starts; statutory online withdrawal vs any retailer extension;
- Return-shipping cost and who pays, return method, possible handling/restocking or hygiene-unsealing exclusions, relevant refund deductions and deadline if verified;
- Seller or manufacturer voluntary warranty period separately from statutory consumer rights;
- Restrictions such as sealed hygiene goods, pickup/in-store purchase differences, subscriptions or membership requirements.

Mark every unavailable field **Not verified**. Do not assume free returns, free shipping, a 30-day return window or Prime membership. For in-store purchases do not assume online-distance withdrawal rights apply.

## Decision output
Lead with best **usable deal**, best **effective per-unit cost**, lowest upfront spend and an explicit Amazon comparison; mention trade-offs, stock confidence, shipping convenience, return policy and any local-store advantage. Show checked and blocked sources, plus what would change the ranking. Do not overstate the certainty of inferences about health, product quality or durability.

## Privacy
Never write user-provided links (especially affiliate/short URLs), product selections, location, postal code, username, order history, account status, checkout data, cookies, tokens or other shopping-session details into public repositories, skill examples, tests, commits or logs. Use synthetic examples. Only publish reusable generic instructions and code. Redact query-string tracking parameters from any canonical Amazon URL you emit. Do not transmit user shopping data to third-party link resolvers without a clear need or consent.
