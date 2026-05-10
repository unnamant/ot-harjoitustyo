# Testausdokumentti
Ohjelmaa on testattu automatisoiduilla yksikkö- ja integraatiotesteillä (pytest) sekä lisäksi manuaalisesti käyttöliittymän kautta järjestelmätasolla.

Automatisoidut testit ajetaan pytestillä, ja testejä varten käytetään erillistä testitietokantaa (test-database.sqlite), jotta testiajo ei muuta kehitystietokantaa.

## Yksikkö- ja integraatiotestaus
### Sovelluslogiikka
Sovelluslogiikasta vastaavaa `BudgetService`-luokkaa testataan `TestBudgetService`-testiluokalla ja käyttäjistä vastaavaa `UserService`-luokkaa `TestUserService`-testiluokalla.
Testejä varten on olemassa `FakeUserRepository` ja `FakeBudgetRepository` -luokat, jotka tallentavat tietoa muistiin pysyväistallennuksen sijaan.

### Pysyväistallennus
Repositorio-luokkaa `BudgetRepository` testataan `TestBudgetRepository`-testiluokalla ja `UserRepository`-luokkaa `TestUserRepository`-testiluokalla.
Repositorio-luokkia testataan erillisellä SQLite-testitietokannalla `test-database.sqlite`, jonka nimi on määritelty `.env.test`-tiedostossa.

### Testauskattavuus
<img width="881" height="511" alt="image" src="https://github.com/user-attachments/assets/2a88c24e-c176-4f01-a39a-0c388d770161" />

Sovelluksesta jäi yksittäisiä tilanteita testaamatta, kuten budjetin muokkaus ja virheelliset syötteet esimerkiksi kirjautuessa tai rekisteröityessä.
