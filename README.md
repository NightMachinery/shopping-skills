# shopping-skills

Free, portable AI agent skills for comparing online, Amazon, and physical-store shopping options, with a focus on **Germany**. No paid price-comparison API is required. Current prices still require permitted browser or web-search access; indexed snippets may be stale.

## Skills

- [shopping-compare](skills/shopping-compare/SKILL.md): Orchestrates mandatory Amazon, competitor and appropriate local-store checks; normalizes final payable total, price per quantity, returns and availability.
- [amazon-free](skills/amazon-free/SKILL.md): Amazon.de first-party and marketplace research, Prime versus non-Prime shipping, bulk sizes, fulfillment and return terms. Invoked for every general product comparison, even without an Amazon link.
- [keepa-free](skills/keepa-free/SKILL.md): Amazon ASIN extraction from product or short links and best-effort visual price-history inspection. The unofficial graph-image route may be unavailable.
- [idealo-free](skills/idealo-free/SKILL.md): German prices and offer comparisons through the ordinary consumer website, search listings, or user-visible saved pages.
- [geizhals-free](skills/geizhals-free/SKILL.md): German electronics retailer price research and historic price context.
- [local-store-de](skills/local-store-de/SKILL.md): Local dm, Rossmann, Müller, grocery, sports and electronics offers; click-and-collect and unit prices.
- [refurbished-de](skills/refurbished-de/SKILL.md): Research directory of [professional refurbished providers](data/refurbishers_de.json) in Germany, including warranty, device condition, delivery and returns.

## Essential comparison standards

A strong recommendation requires **both** real purchase cost and product suitability:

1. Always search **Amazon.de**, even when the query came from a physical shop or price-comparison site. Search different container sizes, multipacks, and professional sellers. Account for delivery convenience as a real advantage.
2. Compare identical or genuinely comparable products. For packaged goods always show **purchased quantity**, item cost per L/kg/item, **delivered cost per L/kg/item**, and **minimum payable basket**. The best per-unit buy may not be the cheapest small purchase.
3. Delivered total includes actual product price, shipping and other mandatory checkout fees less only discounts whose eligibility is verified. Never presume free delivery, Amazon Prime membership, or a coupon. If shipping is unknown the delivered total stays **Not verified**.
4. Cross-check availability against current product pages, branch stock, catalogue pages and (where accessible) checkout. A sold-out or contradicted listing must not win; index-only results are tentative. Report which retailers were blocked or not checked.
5. Include the return window in days, return postage costs, restrictions (especially unsealed hygiene goods), relevant deductions, and seller warranty separate from statutory rights. When missing, say **Not verified**.
6. Flag local-store or collection advantages when justified, including price per unit and transport convenience. Do not assume local stock or app-coupon eligibility.

## Privacy

**Never put an actual user's short Amazon URL, tracked/affiliate link, product shortlist, geographic location, postal code, checkout data, subscription status, cookies or identifiers into this public repository, examples, tests or commit messages.** Public examples use synthetic non-real identifiers. The Amazon URL helper canonicalizes links and omits tracking query strings. Conduct offer research per-user at runtime; keep repository code and docs generic. Do not commit local offer JSON or logs.

## Installation

Each skill folder under `skills/` contains an independent `SKILL.md`. Copy the folders to `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex), or configure the agent to read this repository. Keep the repository checkout accessible when using helpers from `scripts/` or the provider directory.

## CLI helpers

Python 3.9+ standard library only; no API keys needed.

```bash
# Synthetic identifier in documentation only:
python3 skills/keepa-free/scripts/keepa_lookup.py B0EXAMPLE1 --marketplace de

# Search-discovery links (not live offer or stock verification):
python3 scripts/shop_search.py "Example model 256GB" --sources idealo geizhals refurb --all

# Audit local JSON offer evidence supplied to the agent, never commit that input:
python3 scripts/offer_math.py --file ./offers.json

# Run offline regression tests:
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/keepa-free/tests -v
```

Example synthetic JSON for the offer math helper (not a live price):

```json
{"offers":[{"name":"Example liquid","merchant":"Sample Store","unit":"ml","quantity_per_pack":250,"packs":2,"item_total":"11.00","shipping":"3.95","mandatory_fees":"0","availability":"user-reported"}]}
```

Input keys `shipping` and `mandatory_fees` must be explicitly supplied to compute the checkout total; missing values are **not** assumed to be zero. Evidence levels matter: user-reported, indexed-only and blocked offers are not presented as confirmed purchase options.

## Limits

Keepa's official Graph Image API is paid. The unofficial public graph-image address is not guaranteed to work. Amazon and price-comparison websites may restrict automated access. This repo supplies browser-and-search research workflows and offline helpers; it does not bypass authentication, CAPTCHAs, paywalls or other access controls. Do not invent prices, returns policies, stock or full retailer coverage.

## License

MIT. Independent project, not affiliated with the merchants or comparison services referenced here.
