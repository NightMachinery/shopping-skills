---
name: refurbished-de
description: Sweep professional refurbishers and refurbished marketplaces in Germany, checking prices, condition, returns and warranties for exact device variants.
---
# Germany refurbished market sweep
Use the provider directory at `data/refurbishers_de.json` and `scripts/shop_search.py`.
1. Match exact model/generation, capacity, RAM, color, configuration, keyboard, grade and battery requirements.
2. Run `python3 scripts/shop_search.py "iPhone 15 Pro 256GB" --sources refurb --category phones --all --format json` from repository root; laptops use `--category laptops`.
3. Search **each relevant provider** independently, first normally via the site or browser, then public indexed search if blocked. Keep a per-provider status: verified match / no match seen / indexed-only / blocked / unsearched.
4. Include direct German refurbishers, professional seller marketplaces, manufacturer outlets and comparison aggregators. Marketplace listing must have a professional seller. Avoid private listings. Deduplicate the same underlying seller offer.
5. Extract exact product link, listed price, Germany shipping, seller, real stock, cosmetic grade, battery health if specified, warranty offered, statutory rights distinction, returns, VAT status and timestamp.
6. Do not rank unlike products as equivalent: check German QWERTZ keyboards, battery health, charger, lock status, parts/defects, OS, model generation, region and condition.
7. Cross-check the leading refurbished offers against verified NEW total prices from Idealo and Geizhals.
8. Output cheapest acceptable, strongest warranty and best value with direct links, costs and uncertainties. State provider coverage count and blocked providers. Indexed search results alone cannot prove live availability. No paid APIs required.
9. If a page blocks access, report it; no CAPTCHA or authentication bypass. Catalogue is a broad research starting point, not a guarantee that every German retailer exists in it.

## Mandatory checkout and returns audit
For EVERY shortlisted offer report **total delivered price in Germany** = item price + delivery + unavoidable payment, handling, service and tax charges; list each component and explicitly label anything unverified. Never rank offers by headline price alone. Separate coupon, membership, minimum basket, pick-up, financing and payment-method constraints.
Report the **return period in calendar days**, what triggers its start, whether it is statutory withdrawal or an additional shop policy, the **return shipping fee/payer**, whether a label is supplied, restocking/handling costs and any relevant exclusion or deduction. Show the refund method and deadline if verifiable. Report seller/manufacturer warranty duration separately from statutory consumer rights. If unknown, write "Not verified", never assume free returns or a 30-day window.
Prioritize a transparent result format per offer: retailer; exact model/condition; item price; delivery; mandatory fees; delivered total; return days; return-postage responsibility/cost; deductions; warranty duration; source URL; verification time.
## Local store value check
Before calling an online offer the best deal, consider suitable physical-store or click-and-collect alternatives in Germany: dm, Rossmann, Müller, Decathlon, Edeka, REWE, Kaufland, Aldi, Lidl, MediaMarkt, Saturn and category-specific local retailers. Only check genuinely relevant stores for the product. Factor in local shelf price, in-store offers, loyalty-app coupon conditions, pack size/unit price, pickup availability and practical travel cost. If local availability or prices cannot be verified, label them as a possible better-value lead, not a confirmed cheaper offer. Do not assume delivery and physical pickup cost the same. If a local shop offers a cheaper practical total or much easier/free returns, clearly flag it.
