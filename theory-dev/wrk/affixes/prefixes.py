#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
from arguments import CustomFormatter, add_common_arguments
from find_affixes import find_affixes


def main():  # Zamyka w sobie całe działanie skryptu, żeby można było importować pozostałe elementy
    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter,
        description='Znajduje przedrostki w słowniku podzielonym na sylaby',
        epilog="""Przedrostki spełniają następujące warunki:
  - Składają się z ciągu jednej lub więcej sylab
  - Rozpoczynają dane słowo
  - Pozostała część słowa po usunięciu przedrostka także występuje w słowniku""")
    add_common_arguments(parser)
    parser.add_argument('-o', '--output',
                        help='wynikowy plik z przedrostkami', default='wyniki/przedrostki.txt')
    args = parser.parse_args()

    if args.input is None:
        args.input = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'data/slownik-testowy-przedrostki.txt')

    if args.verbose:
        print('Opcje: ', args)

    # Utwórz folder na wyniki jeśli nie istnieje
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    prefixes_found_count = 0
    with open(args.input, 'r') as file_in:
        with open(args.output, 'w') as file_out:
            prefixes = find_affixes(False, file_in, args.separator,
                                    args.max_length, args.verbose)

            # Posortuj klucze według wartości dla nich, malejąco
            common_prefixes = sorted(prefixes, key=prefixes.get, reverse=True)

            file_out.write('\n'.join(common_prefixes))
            print(f'Zapisano {len(prefixes)} przedrostków do {args.output}')


if __name__ == '__main__':
    main()
