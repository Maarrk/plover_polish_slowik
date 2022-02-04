# Teoria Słowik dla Spectra Lexer

Żeby móc iterować teorię, chcemy ją zapisać w sposób zrozumiały dla skryptów i potem automagicznie wygenerować większość słownika. Zamiast opracowywać nowy format, tu będą dane kompatybilne z wtyczką [Spectra Lexer](https://github.com/fourshade/spectra_lexer). Format reguł ma [formalny opis](https://github.com/fourshade/spectra_lexer/blob/master/doc/rules_format.txt).

## Uruchamianie

Żeby używać Spectra Lexer w normalnym oknie Plover z tymi zasadami trzeba wygenerować polski indeks i ręcznie go załadować do wtyczki. Na razie szybciej jest uruchamiać ją samodzielnie (opcje z `http` są dlatego że zdarzają się problemy z Qt w tym trybie).

```
spectra_lexer http --http-port=8888 --keymap=assets/key_layout.cson --rules=assets/rules.cson --board-defs=assets/board_defs.cson --translations=wyniki/spektralny-slowik.json --index=wyniki/index.json
```
