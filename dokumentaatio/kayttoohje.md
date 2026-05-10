# Budget-sovelluksen käyttöohje
## Viimeisin release
 [Loppupalautus](../../../releases/latest)

Ohjeet:
1. Lataa lähdekoodi zip-muodossa koneellesi yllä olevasta linkistä
2. Siirry kansioon, missä lähdekoodi sijaitsee
3. Pura zip-paketti seuraavalla komennolla:
```bash
unzip ot-harjoitustyo-Loppupalautus.zip
```
4. Katso alta ohjeet sovelluksen riippuvuuksien asennukseen ja käynnistykseen
## Konfigurointi
Tallennukseen käytettävän tiedoston nimeä voi halutessaan muokata käynnistyshakemistossa ".env". Tiedosto luodaan automaattisesti _data_-hakemistoon, jos sitä ei vielä ole. Tiedosto on seuraavassa muodossa:
```
DATABASE_FILENAME=database.sqlite
```
## Sovelluksen asennus ja käynnistys
Asenna riippuvuudet komennolla:

```bash
poetry install
```
Suorita vaadittavat alustustoimenpiteet komennolla:
```bash
poetry run invoke build
```
Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```
