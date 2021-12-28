import unittest
import io
from find_affixes import find_affixes


class AffixTester(unittest.TestCase):
    def setUp(self):
        self.text_file = io.StringIO()

    def set_file(self, text: str):
        self.text_file.write(text)


class TestPrefixes(AffixTester):
    def test_no_word(self):
        self.set_file('''ka=mień
ka=za=nie
kla=wia=tu=ra''')
        self.assertEqual(find_affixes(False, self.text_file), {})

    def test_simple(self):
        self.set_file('''prze=wa=ga
wa=ga''')
        self.assertEqual(find_affixes(False, self.text_file), {'prze': 1})

    def test_comment(self):
        self.set_file('''#nad=wa=ga
prze=wa=ga
wa=ga''')
        self.assertEqual(find_affixes(False, self.text_file), {'prze': 1})

    def test_multiple(self):
        self.set_file('''ko=pać
prze=ko=pać
prze=wa=ga
wa=ga''')
        self.assertEqual(find_affixes(False, self.text_file), {'prze': 2})

    def test_length(self):
        self.set_file('''prze=wa=ga
wa=ga
an=ty=wi=rus
wi=rus
czer=wo=no=wło=sy
wło=sy''')
        self.assertEqual(find_affixes(False, self.text_file, max_length=1), {'prze': 1})
        self.assertEqual(find_affixes(False, self.text_file, max_length=2), {'prze': 1, 'an=ty': 1})
        self.assertEqual(find_affixes(False, self.text_file, max_length=3), {'prze': 1, 'an=ty': 1, 'czer=wo=no': 1})


class TestSuffixes(AffixTester):
    def test_simple(self):
        self.set_file('''bar
bar=ka''')
        self.assertEqual(find_affixes(True, self.text_file), {'ka': 1})

if __name__ == '__main__':
    unittest.main()
