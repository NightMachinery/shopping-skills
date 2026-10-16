import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/shop_search.py'
SPEC = importlib.util.spec_from_file_location('shop_search', SCRIPT)
s = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s)

class DiscoveryTests(unittest.TestCase):
    def test_amazon_discovery(self):
        rows = s.build_entries('Synthetic model', ['amazon', 'idealo'])
        self.assertEqual([r['source'] for r in rows], ['amazon', 'idealo'])
        self.assertIn('site:amazon.de', rows[0]['search_query'])
        self.assertEqual(rows[0]['status'], 'not checked')

    def test_default_includes_amazon(self):
        completed = subprocess.run([sys.executable, str(SCRIPT), 'Synthetic product',
                                    '--format', 'json'], check=True,
                                    capture_output=True, text=True)
        data = json.loads(completed.stdout)
        self.assertEqual(data['providers'][0]['source'], 'amazon')
        self.assertTrue(data['generated'] > 2)

    def test_no_fake_prices(self):
        self.assertTrue(all('price' not in r for r in s.build_entries('Synthetic product', ['amazon'])))

if __name__ == '__main__':
    unittest.main()
