from typing import TextIO, Optional
import xml.etree.ElementTree as ET


def open_ods(filename: str, table_index=0, column='A', skiprows=0) -> TextIO:
    raise NotImplementedError()


def parse_content(content_file: TextIO, table_index: Optional[int] = None, column_index: Optional[int] = None) -> list[list[list[str]]]:
    # Regex for changing namespaces to dictionary
    # xmlns:([a-z]+)="([\w:.]+)"\s+
    # '$1': '$2',\n
    ns = {'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
          'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
          'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0', }

    tree = ET.parse(content_file)
    root = tree.getroot()
    sheet = root.find('office:body', ns).find('office:spreadsheet', ns)
    return [[[
        cell.find('text:p', ns).text
        for cell in row.findall(f'table:table-cell{"[" + str(column_index + 1) + "]" if column_index is not None else ""}', ns)]
        for row in table.findall('table:table-row', ns)]
        for table in sheet.findall(f'table:table{"[" + str(table_index + 1) + "]" if table_index is not None else ""}', ns)
    ]
