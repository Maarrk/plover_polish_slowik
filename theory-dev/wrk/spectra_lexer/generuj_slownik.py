#!/usr/bin/env python3
import argparse
import json
import os
import re
from typing import Dict

from cson import CommentRemover


class Zasada:
    def __init__(self, klawisze: str, litery: str, flagi: str) -> None:
        self.klawisze = klawisze
        self.litery = litery
        self.referencyjna = 'REFERENCE' in flagi

    def __str__(self) -> str:
        return f'Zasada: "{self.klawisze}" -> "{self.litery}"'


with open('assets/rules.cson') as zasady_cson:
    zasady_json = CommentRemover(zasady_cson)
    # for i, linia in enumerate(zasady_json):
    #     print(f'{i}\t{linia}', end='')
    # zasady_json.seek(0)
    zasady = json.load(zasady_json)
    # print(zasady)

    # Zmień słownik list na słownik obiektów
    for id in zasady:
        # Nazwy zmiennych zgodne z spectra_lexer/doc/rules_format.txt
        keys, letters, alt, flags, info = tuple(zasady[id])
        zasady[id] = Zasada(keys, letters, flags)

    zasady: Dict[str, Zasada]  # Informacja dla edytora kodu jaki to ma typ

    słowa = []

    # Inna zasada w tekście: ciąg dowolnych znaków wewnątrz nawiasów
    inna_zasada = re.compile(r'\(([^()]+)\)')

    for id, zasada in zasady.items():
        if zasada.referencyjna:
            continue  # Nie twórz dla niej nowego słowa

        tekst = zasada.litery
        # Podmień odwołania do innych zasad na tekst
        while inna_zasada.search(tekst):
            m = inna_zasada.search(tekst)  # Szczegóły znalezionej innej zasady
            # Obsługa składni: (litery|id)
            podmiana = m.group(1).split('|')[0] \
                if '|' in m.group(1) else zasady[m.group(1)].litery
            tekst = tekst[:m.start()] + podmiana + tekst[m.end():]

        słowa.append((zasada.klawisze, tekst))

    # Posortuj słowa według kolejności klawiszy
    KOLEJNOŚĆ = '#XFZSKTPVLR-JE~*IAUCRLBSGTWOY'
    słowa = sorted(słowa, key=lambda słowo:
                   [KOLEJNOŚĆ.index(k) for k in słowo[0]])

    linie = [f'"{klawisze}": "{tekst}"' for klawisze, tekst in słowa]

    os.makedirs('wyniki', exist_ok=True)
    with open('wyniki/spektralny-slowik.json', 'w') as slownik:
        slownik.write('{\n' + ',\n'.join(linie) + '\n}')
