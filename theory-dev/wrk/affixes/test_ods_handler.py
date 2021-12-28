import unittest
import io
from ods_handler import *


class OdsTest(unittest.TestCase):
    def make_content_file(self, tables):
        sheet_prefix = '''<?xml version="1.0" encoding="UTF-8"?>
            <office:document-content
                xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
            ><office:body><office:spreadsheet>'''

        sheet_suffix = '''</office:spreadsheet></office:body></office:document-content>'''

        content_file = io.StringIO()
        content_file.write(sheet_prefix + tables + sheet_suffix)
        content_file.seek(0)
        return content_file

    def test_content_simple(self):
        content_file = self.make_content_file(
            '''<table:table>
                <table:table-row>
                    <table:table-cell>
                        <text:p>Cell text</text:p>
                    </table:table-cell>
                </table:table-row>
            </table:table>''')
        self.assertEqual(parse_content(content_file), [[['Cell text']]])

    def test_content_square_table(self):
        content_file = self.make_content_file(
            '''<table:table>
                <table:table-row>
                    <table:table-cell>
                        <text:p>A1</text:p>
                    </table:table-cell>
                    <table:table-cell>
                        <text:p>B1</text:p>
                    </table:table-cell>
                </table:table-row>
                <table:table-row>
                    <table:table-cell>
                        <text:p>A2</text:p>
                    </table:table-cell>
                    <table:table-cell>
                        <text:p>B2</text:p>
                    </table:table-cell>
                </table:table-row>
            </table:table>''')
        self.assertEqual(parse_content(content_file),
                         [[['A1', 'B1'],
                           ['A2', 'B2']]])
        content_file.seek(0)
        self.assertEqual(parse_content(content_file, column_index=0),
                         [[['A1'],
                           ['A2']]])
        content_file.seek(0)
        self.assertEqual(parse_content(content_file, column_index=1),
                         [[['B1'],
                           ['B2']]])

    def test_content_multiple_tables(self):
        content_file = self.make_content_file(
            '''<table:table>
                <table:table-row>
                    <table:table-cell>
                        <text:p>T0</text:p>
                    </table:table-cell>
                </table:table-row>
            </table:table>
            <table:table>
                <table:table-row>
                    <table:table-cell>
                        <text:p>T1</text:p>
                    </table:table-cell>
                </table:table-row>
            </table:table>''')
        self.assertEqual(parse_content(content_file),
                         [[['T0']], [['T1']]])
        content_file.seek(0)
        self.assertEqual(parse_content(content_file, table_index=0),
                         [[['T0']]])
        content_file.seek(0)
        self.assertEqual(parse_content(content_file, table_index=1),
                         [[['T1']]])


if __name__ == '__main__':
    unittest.main()
