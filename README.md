# BudgetApp
*Budget-sovelluksella* käyttäjän on mahdollista pitää kirjaa **budjetoinnistaan**.
## Dokumentaatio

- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)

- [työaikakirjanpito](dokumentaatio/työaikakirjanpito.md)

- [changelog](dokumentaatio/changelog.md)

- [arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)

- [käyttöohje](dokumentaatio/kayttoohje.md)

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
