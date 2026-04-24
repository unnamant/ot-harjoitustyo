# Budget-sovelluksen käyttöohje
## Viimeisin release
 [viikon 5 release](../../releases/latest)

Ohjeet:
1. Lataa lähdekoodi zip-muodossa koneellesi yllä olevasta linkistä
2. Siirry kansioon, missä lähdekoodi sijaitsee
3. Pura zip-paketti seuraavalla komennolla:
```bash
unzip ot-harjoitustyo-viikko5.1.zip
```
4. Katso alta ohjeet sovelluksen riippuvuuksien asennukseen ja käynnistykseen
## Konfigurointi
Tallennukseen käytettävien tiedostojen nimiä voi halutessaan konfiguroida käynnistyshakemistossa ".env". Tiedostot luodaan automaattisesti _data_-hakemistoon, jos niitä ei vielä ole. Tiedosto on seuraavassa muodossa:
```
BUDGETS_FILENAME=budgets.csv
DATABASE_FILENAME=database.sqlite
```
## Sovelluksen asennus ja käynnistys
Asenna riippuvuudet komennolla:

```bash
poetry install
```
Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```
