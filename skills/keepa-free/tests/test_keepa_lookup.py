import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/keepa_lookup.py'
SPEC = importlib.util.spec_from_file_location('keepa_lookup', SCRIPT)
k = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(k)


class KeepaLookupTests(unittest.TestCase):
    def test_plain_asin(self):
        r = k.resolve('B0EXAMPLE1')
        self.assertEqual(r['marketplace'], 'de')
        self.assertEqual(r['amazon_url'], 'https://www.amazon.de/dp/B0EXAMPLE1')

    def test_full_link_strips_tracking_parameters(self):
        r = k.resolve('https://www.amazon.de/dp/B0EXAMPLE1?tag=not-for-logging&x=1')
        self.assertNotIn('tag=', str(r))
        self.assertEqual(r['asin'], 'B0EXAMPLE1')

    def test_short_link_returns_anonymized_url(self):
        with patch.object(k, '_capture_redirect', return_value='https://amazon.de/gp/aw/d/B0EXAMPLE1?tag=private-value'):
            r = k.resolve('https://amzn.eu/d/<SHORT_CODE>')
        self.assertEqual(r['amazon_url'], 'https://www.amazon.de/dp/B0EXAMPLE1')
        self.assertNotIn('private', str(r))

    def test_shortener_does_not_choose_marketplace(self):
        with patch.object(k, '_capture_redirect', return_value='https://www.amazon.fr/dp/B0EXAMPLE1'):
            r = k.resolve('https://amzn.eu/d/<SHORT_CODE>')
        self.assertEqual(r['marketplace'], 'fr')
        self.assertIn('#!product/4-', r['keepa_url'])

    def test_nonamazon_domain_rejected(self):
        with self.assertRaises(ValueError):
            k.resolve('https://evil.example/dp/B0EXAMPLE1')

    def test_only_https(self):
        with self.assertRaises(ValueError):
            k.resolve('http://amazon.de/dp/B0EXAMPLE1')

    def test_userinfo_rejected(self):
        with self.assertRaises(ValueError):
            k.resolve('https://a:password@amazon.de/dp/B0EXAMPLE1')

    def test_query_asin(self):
        r = k.resolve('https://amazon.de/something?asin=B0EXAMPLE1&tag=sensitive')
        self.assertEqual(r['asin'], 'B0EXAMPLE1')
        self.assertNotIn('sensitive', str(r))

    def test_nonamazon_redirect_rejected(self):
        with patch.object(k, '_capture_redirect', return_value='https://evil.example/dp/B0EXAMPLE1'):
            with self.assertRaises(ValueError):
                k.resolve('https://amzn.eu/d/<SHORT_CODE>')

    def test_multi_pack_marketplace(self):
        r = k.resolve('B0EXAMPLE1', 'co.uk')
        self.assertEqual(r['marketplace'], 'co.uk')
        self.assertIn('domain=co.uk', r['chart_candidate'])

    def test_invalid_asin_rejected(self):
        with self.assertRaises(ValueError):
            k.resolve('https://www.amazon.de/dp/bad')


if __name__ == '__main__':
    unittest.main()
