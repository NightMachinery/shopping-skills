#!/usr/bin/env python3
"""Offline EUR price/quantity normalizer. Never requests webpages or stores inputs."""
import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

SIZES = {'ml': ('L', Decimal('0.001')), 'l': ('L', Decimal('1')),
         'g': ('kg', Decimal('0.001')), 'kg': ('kg', Decimal('1')),
         'count': ('item', Decimal('1'))}
STATES = {'checkout-confirmed', 'listing-in-stock', 'store-confirmed',
          'user-reported', 'indexed-only', 'sold-out', 'blocked', 'unsearched'}
CONFIRMED_STATES = {'checkout-confirmed', 'store-confirmed'}
UNAVAILABLE_STATES = {'sold-out', 'blocked', 'unsearched'}


def number(value, label, required=True):
    if value is None:
        if required:
            raise ValueError(f'{label} is required')
        return None
    if isinstance(value, bool):
        raise ValueError(f'{label} must be numeric')
    text = str(value).strip()
    if ',' in text and '.' not in text and text.count(',') == 1:
        text = text.replace(',', '.')
    try:
        result = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f'{label} must be numeric') from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f'{label} must be finite and nonnegative')
    return result


def money(n):
    return str(n.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) if n is not None else None


def normalize(offer):
    if not isinstance(offer, dict):
        raise ValueError('offer must be an object')
    unit = str(offer.get('unit', '')).strip().lower()
    if unit not in SIZES:
        raise ValueError('unit must be ml, l, g, kg or count')
    per_pack = number(offer.get('quantity_per_pack'), 'quantity_per_pack')
    if per_pack == 0:
        raise ValueError('quantity_per_pack must be positive')
    packs = offer.get('packs', 1)
    if isinstance(packs, bool) or not isinstance(packs, int) or packs <= 0:
        raise ValueError('packs must be a positive integer')
    item_total = number(offer.get('item_total'), 'item_total')
    # Missing shipping or fee information must never silently become zero.
    shipping = number(offer.get('shipping'), 'shipping', required=False)
    fees = number(offer.get('mandatory_fees'), 'mandatory_fees', required=False)
    discount = number(offer.get('confirmed_discount', 0), 'confirmed_discount')
    status = offer.get('availability', 'unsearched')
    if status not in STATES:
        raise ValueError('availability must use a documented evidence state')
    quantity_unit, factor = SIZES[unit]
    quantity = per_pack * packs * factor
    item_unit = item_total / quantity
    subtotal = item_total + shipping + fees if shipping is not None and fees is not None else None
    if subtotal is not None and discount > subtotal:
        raise ValueError('confirmed_discount exceeds subtotal')
    delivered = subtotal - discount if subtotal is not None else None
    result = {
        'name': offer.get('name'), 'merchant': offer.get('merchant'),
        'channel': offer.get('channel'),
        'quantity': str(quantity.normalize()), 'base_unit': quantity_unit,
        'availability': status, 'item_total_eur': money(item_total),
        'shipping_eur': money(shipping), 'mandatory_fees_eur': money(fees),
        'confirmed_discount_eur': money(discount),
        'item_price_per_unit_eur': money(item_unit),
        'delivered_total_eur': money(delivered),
        'delivered_price_per_unit_eur': money(delivered / quantity) if delivered is not None else None,
        'ranking_status': ('confirmed' if delivered is not None and status in CONFIRMED_STATES else
                           'provisional' if delivered is not None and status == 'listing-in-stock' else
                           'not-verifiable'),
    }
    return result


def audit(offers):
    rows = [normalize(offer) for offer in offers]
    confirmed = [r for r in rows if r['ranking_status'] == 'confirmed']
    provisional = [r for r in rows if r['ranking_status'] == 'provisional']
    def minimum(group, key):
        # Never silently compare different base units (litres vs kilograms/items).
        return {unit: min((r for r in group if r['base_unit'] == unit),
                          key=lambda r: Decimal(r[key]), default=None)
                for unit in sorted({r['base_unit'] for r in group})}
    return {'offers': rows,
            'confirmed_lowest_unit': minimum(confirmed, 'delivered_price_per_unit_eur'),
            'confirmed_lowest_spend': minimum(confirmed, 'delivered_total_eur'),
            'provisional_lowest_unit': minimum(provisional, 'delivered_price_per_unit_eur'),
            'checked_amazon': any((r.get('channel') or '').lower() in ('amazon', 'amazon.de') or
                                  (r.get('merchant') or '').lower().startswith('amazon') or
                                  (r.get('merchant') or '').lower().endswith('amazon.de')
                                  for r in rows if r['availability'] != 'unsearched')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', required=True, help='Offers JSON path, or - for stdin')
    args = parser.parse_args()
    try:
        if args.file == '-':
            document = json.load(sys.stdin)
        else:
            with open(args.file, encoding='utf-8') as handle:
                document = json.load(handle)
        offers = document.get('offers') if isinstance(document, dict) else document
        if not isinstance(offers, list):
            raise ValueError('JSON must be an array or an object containing an offers array')
        print(json.dumps(audit(offers), indent=2, ensure_ascii=False))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(status=2, message=f'Error: {exc}\n')


if __name__ == '__main__':
    main()
