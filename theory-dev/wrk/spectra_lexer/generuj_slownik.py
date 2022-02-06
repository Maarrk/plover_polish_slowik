#!/usr/bin/env python3
import argparse
import json
import os
import re
from typing import Any, Dict

from cson import CommentRemover


class Zasada:
    def __init__(self, klawisze: str, litery: str, flagi: str, numer_linii: int = 0) -> None:
        self.klawisze = klawisze
        self.litery = litery
        self.numer_linii = numer_linii

        # Wygeneruj wpis do słownika na tej podstawie
        self.f_słownik = 'DICT' in flagi
        # Zasada tylko do używania w innych zasadach, pownna mieć ~ w id
        self.f_referencyjna = 'REFERENCE' in flagi
        # Flaga UPPERCASE jest potrzebna żeby pogodzić generację słownika z lekserem dla literowania wielkich liter
        self.f_duże_litery = 'UPPERCASE' in flagi
        # Powoduje duplikat, ale nie zdecydowano jeszcze co z nim zrobić
        self.f_duplikat = 'DUPLICATE' in flagi

    def __str__(self) -> str:
        return f'Zasada: "{self.klawisze}" -> "{self.litery}"'

    def do_uzupełnienia(self) -> bool:
        return self.klawisze == ''


def jest_pusta_zasada(zasady: Dict[Any, Zasada]) -> bool:
    for zasada in zasady.values():
        if zasada.do_uzupełnienia():
            return True
    return False


def połącz_klawisze(*args: str) -> str:
    zestawy = list(args)
    kolejność = '#XFZSKTPVLR-JE~*IAUcrlbgtsgtwoy'

    indeksy = []
    for zestaw in zestawy:
        # Zamień prawą część na małe litery żeby szukać w indeksach
        strony = re.split(r'[\-JE~*IAU]+', zestaw)
        if len(strony) > 1:
            prawa: str = strony[-1]
            if len(prawa) > 0:
                zestaw = zestaw[:-len(prawa)] + prawa.lower()
        indeksy.extend([kolejność.index(k) for k in zestaw])

    indeksy = sorted(list(set(indeksy)))  # Posortowane bez powtórzeń
    wynik = ''.join([kolejność[i] for i in indeksy])
    if re.search(r'[JE~*IAU]', wynik):  # Por. system.py IMPLICIT_HYPHEN_KEYS
        wynik = wynik.replace('-', '')
    return wynik.upper()


with open('assets/rules.cson.in') as szablon_cson:
    linie_szablonu = szablon_cson.readlines()
    if not linie_szablonu[0].startswith('#'):
        raise ValueError(
            'Pierwsza linia w pliku szablonu musi być komentarzem')
        # Inaczej by mi się rozjechały numery linii po dodaniu pierwszej
    linie_szablonu[0] = \
        f'# UWAGA: Plik wygenerowany automatycznie na podstawie {"rules.cson.in"}\n'

    szablon_cson.seek(0)
    zasady_json = CommentRemover(szablon_cson)
    # for i, linia in enumerate(zasady_json):
    #     print(f'{i}\t{linia}', end='')
    # zasady_json.seek(0)
    try:
        zasady = json.load(zasady_json)
    except json.JSONDecodeError as e:
        zasady_json.seek(0)
        linie_json = zasady_json.readlines()
        print('------------')
        # lineno zaczyna się od 1
        print(linie_json[e.lineno - 3], end='')
        print(linie_json[e.lineno - 2], end='')
        print(linie_json[e.lineno - 1], end='')
        print(' '*(e.colno - 2), '^')
        print(linie_json[e.lineno + 0], end='')
        print(linie_json[e.lineno + 1], end='')
        print('------------')
        raise e

    # print(zasady)

    # Zmień słownik list na słownik obiektów
    for id in zasady:
        # Nazwy zmiennych zgodne z spectra_lexer/doc/rules_format.txt
        keys, letters, alt, flags, info = tuple(zasady[id])
        zasady[id] = Zasada(keys, letters, flags)

    zasady: Dict[str, Zasada]  # Informacja dla edytora kodu jaki to ma typ

    # Dopisz do zasad z której są linii
    for i, linia in enumerate(linie_szablonu):
        linia = linia.strip()
        if linia.startswith('"'):
            id = linia.split('"')[1]
            # Numery linii w pliku zaczynają się od 1
            zasady[id].numer_linii = i + 1

    # Inna zasada w tekście: ciąg dowolnych znaków wewnątrz nawiasów
    inna_zasada = re.compile(r'\(([^()]+)\)')

    # Złóż wszystkie zasady bez klawiszy z innych zasad
    # Możliwe że będzie konieczne kilka iteracji jeśli jest kilka poziomów definicji
    while True:
        zmieniono_zasadę = False  # Wykryj iteracje bez szans na ukończenie zadania

        for edytowane_id, zasada in zasady.items():
            if not zasada.do_uzupełnienia():
                continue

            użyte_id = set()
            tekst = zasada.litery
            while True:
                # Szczegóły znalezionej innej zasady
                m = inna_zasada.search(tekst)
                if not m:
                    break
                inne_id = m.group(1).split('|')[1] \
                    if '|' in m.group(1) else m.group(1)
                użyte_id.add(inne_id)
                # Obsługa składni: (litery|id), wstaw id w nawiasach
                podmiana = ('(' + inne_id + ')') \
                    if '|' in m.group(1) else zasady[m.group(1)].litery
                tekst = tekst[:m.start()] + podmiana + tekst[m.end():]

            użyte_id_do_uzupełnienia = {
                id for id in użyte_id if zasady[id].do_uzupełnienia()}

            if len(użyte_id_do_uzupełnienia) == 0:
                # Mamy wszystkie składowe, można utworzyć ten wpis
                utworzone_klawisze = połącz_klawisze(
                    *[zasady[id].klawisze for id in użyte_id])
                klawisze_szablonu = zasada.klawisze
                zasady[edytowane_id].klawisze = utworzone_klawisze
                definicja = linie_szablonu[zasada.numer_linii - 1]
                linie_szablonu[zasada.numer_linii - 1] = \
                    definicja.replace(
                        f'["{klawisze_szablonu}"', f'["{utworzone_klawisze}"')
                zmieniono_zasadę = True
                # print(f'Wygenerowano {zasady[edytowane_id]}')

        if not jest_pusta_zasada(zasady):
            break
        if not zmieniono_zasadę:
            pozostałe = [id for id, zasada in zasady.items()
                         if zasada.do_uzupełnienia()]
            raise ValueError(
                f'Nie udało się znaleźć klawiszy dla zasad: {", ".join(pozostałe)}')

    with open('wyniki/rules.cson', 'w') as zasady_cson:
        zasady_cson.writelines(linie_szablonu)

    słowa = []

    for id, zasada in zasady.items():
        if not zasada.f_słownik:
            continue  # Nie twórz dla niej nowego słowa

        tekst = zasada.litery
        # Podmień odwołania do innych zasad na tekst
        while True:  # Nie używam operatora := bo jest na razie zbyt świeży
            m = inna_zasada.search(tekst)  # Szczegóły znalezionej innej zasady
            if not m:
                break
            # Obsługa składni: (litery|id), wstaw litery
            podmiana = m.group(1).split('|')[0] \
                if '|' in m.group(1) else zasady[m.group(1)].litery
            tekst = tekst[:m.start()] + podmiana + tekst[m.end():]

        if zasada.f_duże_litery:
            tekst = tekst.upper()
        słowa.append((zasada.klawisze, tekst))

    # Posortuj słowa według kolejności klawiszy
    kolejność = '#XFZSKTPVLR-JE~*IAUCRLBSGTWOY'
    słowa = sorted(słowa, key=lambda słowo:
                   [kolejność.index(k) for k in słowo[0]])

    linie = [f'"{klawisze}": "{tekst}"' for klawisze, tekst in słowa]

    os.makedirs('wyniki', exist_ok=True)
    with open('wyniki/spektralny-slowik.json', 'w') as slownik:
        slownik.write('{\n' + ',\n'.join(linie) + '\n}')
