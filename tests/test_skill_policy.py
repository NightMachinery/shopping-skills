import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillPolicyTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding='utf-8')

    def test_amazon_required_for_every_comparison(self):
        skill = self.read('skills/shopping-compare/SKILL.md')
        self.assertIn('ALWAYS search Amazon.de', skill)
        self.assertIn('amazon-free', skill)

    def test_amazon_has_delivery_and_bulk_checks(self):
        skill = self.read('skills/amazon-free/SKILL.md')
        for word in ('Prime', 'multipack', 'return', 'seller', 'stock'):
            self.assertIn(word, skill.lower() if word == 'return' else skill)

    def test_quality_gates_exist(self):
        skill = self.read('skills/shopping-compare/SKILL.md')
        for word in ('delivered_unit_cost', 'sold-out', 'checkout-confirmed', 'Not verified'):
            self.assertIn(word, skill)

    def test_user_link_not_published_as_example(self):
        files = [self.read('README.md'), self.read('skills/keepa-free/SKILL.md'),
                 self.read('skills/amazon-free/SKILL.md')]
        for body in files:
            self.assertIsNone(re.search(r'https?://amzn\.eu/d/[A-Za-z0-9]{6,}', body))
            self.assertNotIn('tag=not-for-logging', body)

    def test_gitignore_covers_transactional_data(self):
        ignore = self.read('.gitignore')
        for glob in ('offers*.json', '*.har', '.env', '*cookie*.json'):
            self.assertIn(glob, ignore)


if __name__ == '__main__':
    unittest.main()
