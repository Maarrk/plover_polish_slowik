import argparse


def add_common_arguments(parser: argparse.ArgumentParser):
    """Dodaje argumenty wspólne dla różnych skryptów
    """
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='wypisuj więcej informacji w trakcie działania')
    parser.add_argument('-i', '--input',
                        help='plik słownika do przeszukania')
    # parser.add_argument('-o', '--output',
    #                     help='folder z wynikami', default='wyniki')
    parser.add_argument('-L', '--max-length', type=int,
                        help='maksymalna liczba sylab zrostka', default=2)
    parser.add_argument('--separator',
                        help='znak rozdzielający sylaby', default='=')


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """Umożliwia jednoczesne wyświetlanie domyślnych wartości i ręczne łamanie linii w opisie
    """
    pass
