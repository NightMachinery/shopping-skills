import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('offer_math', Path(__file__).resolve().parents[1] / 'scripts/offer_math.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def offer(**kw):
    base = dict(name='Synthetic liquid', merchant='Example', unit='ml', quantity_per_pack=100,
                packs=1, item_total='3.50', shipping='0', mandatory_fees='0',
                availability='checkout-confirmed')
    return dict(base, **kw)


class OfferMathTests(unittest.TestCase):
    def test_unit_price_one_bottle(self):
        r = m.normalize(offer())
        self.assertEqual(r['quantity'], '0.1')
        self.assertEqual(r['item_price_per_unit_eur'], '35.00')

    def test_bulk_undercuts_smaller_bottle(self):
        a = m.normalize(offer())
        b = m.normalize(offer(quantity_per_pack=500, item_total='12.00'))
        self.assertLess(float(b['delivered_price_per_unit_eur']), float(a['delivered_price_per_unit_eur']))

    def test_shipping_changes_unit_winner(self):
        bulk = m.normalize(offer(quantity_per_pack=500, item_total='12', shipping='6'))
        small = m.normalize(offer())
        self.assertGreater(float(bulk['delivered_price_per_unit_eur']), float(small['delivered_price_per_unit_eur']))

    def test_missing_shipping_is_not_free(self):
        r = m.normalize(offer(shipping=None))
        self.assertIsNone(r['delivered_total_eur'])
        self.assertEqual(r['ranking_status'], 'not-verifiable')

    def test_missing_fees_is_not_zero(self):
        r = m.normalize(offer(mandatory_fees=None))
        self.assertIsNone(r['delivered_price_per_unit_eur'])

    def test_not_in_stock_cannot_win(self):
        sold = offer(item_total='1', availability='sold-out')
        good = offer(item_total='4')
        report = m.audit([sold, good])
        self.assertEqual(report['confirmed_lowest_spend']['L']['delivered_total_eur'], '4.00')

    def test_user_reported_not_verified(self):
        r = m.normalize(offer(availability='user-reported'))
        self.assertEqual(r['ranking_status'], 'not-verifiable')

    def test_indexed_listing_not_verified(self):
        self.assertEqual(m.normalize(offer(availability='indexed-only'))['ranking_status'], 'not-verifiable')

    def test_listing_price_provisional(self):
        self.assertEqual(m.normalize(offer(availability='listing-in-stock'))['ranking_status'], 'provisional')

    def test_minimum_spend_differs_from_unit_value(self):
        a = offer(name='Small', item_total='3.50')
        b = offer(name='Big', quantity_per_pack=1000, item_total='13')
        r = m.audit([a,b])
        self.assertEqual(r['confirmed_lowest_spend']['L']['name'], 'Small')
        self.assertEqual(r['confirmed_lowest_unit']['L']['name'], 'Big')

    def test_packs_multiplied(self):
        r = m.normalize(offer(packs=4))
        self.assertEqual(r['quantity'], '0.4')

    def test_kg_vs_l_separate(self):
        r = m.audit([offer(),offer(unit='g',quantity_per_pack=250,item_total='3')])
        self.assertEqual(set(r['confirmed_lowest_unit']), {'L', 'kg'})

    def test_missing_amazon_not_masked(self):
        self.assertFalse(m.audit([offer()])['checked_amazon'])

    def test_amazon_detected(self):
        self.assertTrue(m.audit([offer(merchant='Amazon.de')])['checked_amazon'])

    def test_european_decimal_comma(self):
        self.assertEqual(m.normalize(offer(item_total='3,49'))['item_total_eur'], '3.49')

    def test_invalid_discount_rejected(self):
        with self.assertRaises(ValueError):
            m.normalize(offer(item_total='4',confirmed_discount='5'))

    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError):
            m.normalize(offer(quantity_per_pack=0))

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            m.normalize(offer(item_total='-1'))

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            m.normalize(offer(shipping='NaN'))


if __name__ == '__main__':
    unittest.main()
