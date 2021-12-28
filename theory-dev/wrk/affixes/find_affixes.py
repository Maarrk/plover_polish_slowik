import typing

def find_affixes(suffix: bool, file_in: typing.TextIO, separator='=', max_length=2, verbose=False) -> dict:
    """Znajduje zrostki w słowach

    Parameters
    ----------
    suffix : bool
        Jeżeli True szuka przyrostków, jeżeli False szuka przedrostków
    file_in : typing.TextIO()
        plik ze słowem podzielonym na sylaby w każdej linii;
        linie rozpoczynające się od znaku kratki (#) są pomijane
    separator : str
        ciąg znaków rozdzielający sylaby, by default '='
    max_length : int
        maksymalna liczba sylab zrostka, by default 2
    verbose : bool, optional
        pisanie dodatkowych informacji do konsoli, by default False

    Returns
    -------
    dict
        liczba słów rozpoczynających się od danego zrostka
    """
    comment = '#'
    if verbose:
        print('Wczytywanie słów...')
    file_in.seek(0)
    words_in = set([line.strip()
                   for line in file_in if not line.startswith(comment)])
    if verbose:
        print('Unikalne słowa: ', words_in)

    # Zakładając unikalne słowa w pliku, tak mi wygodniej
    line_count = len(words_in)

    valid_affixes = dict()

    file_in.seek(0)  # Przewiń z powrotem na początek pliku
    for line_number, line in enumerate(file_in):
        if line.startswith(comment):
            continue  # Pomiń komentarze

        for length in range(1, max_length + 1):
            syllables = line.strip().split(separator)
            if len(syllables) <= length:
                continue  # Za krótkie słowo

            if suffix:  # Sufiks, przyrostek
                affix_candidate = separator.join(syllables[length:])
                rest_of_word = separator.join(syllables[:length])
            else:  # Prefiks, przedrostek
                affix_candidate = separator.join(syllables[:length])
                rest_of_word = separator.join(syllables[length:])

            if verbose:
                print(
                    f"{'Przyrostek' if suffix else 'Przedrostek'}: '{affix_candidate}', reszta słowa: '{rest_of_word}'", end=' ')

            if rest_of_word in words_in:
                if affix_candidate in valid_affixes:
                    valid_affixes[affix_candidate] += 1
                    if verbose:
                        print('zwiększona liczba wystąpień')
                else:
                    valid_affixes[affix_candidate] = 1
                    if verbose:
                        print('dopisany do wyników')

            elif verbose:
                print('pominięty, bo reszta nie jest słowem')

        if line_number % 10000 == 0 and line_number != 0:
            print(
                f'Sprawdzono {float(line_number) / float(line_count) * 100.0:5.2f}% linii ({line_number}/{line_count})')

    return valid_affixes
