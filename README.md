# BudgetApp
*Budget-sovelluksella* käyttäjän on mahdollista pitää kirjaa **budjetoinnistaan**.

## Dokumentaatio

- [vaatimusmäärittely](https://github.com/unnamant/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)

- [työaikakirjanpito](https://github.com/unnamant/ot-harjoitustyo/blob/main/dokumentaatio/ty%C3%B6aikakirjanpito.md)

- [changelog](https://github.com/unnamant/ot-harjoitustyo/blob/main/dokumentaatio/changelog.md)

## Sovelluksen asennus ja käynnistys
Asenna riippuvuudet komennolla:

```bash
poetry install
```
Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```
### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu _htmlcov_-hakemistoon.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```
