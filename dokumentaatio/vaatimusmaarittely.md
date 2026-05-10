# Vaatimusmäärittely
## Sovelluksen tarkoitus
Sovelluksen tarkoituksena on antaa työkaluja käyttäjälle auttaakseen häntä pitämään huolta päivittäisestä, kuukausittaisesta ja/tai vuosittaisesta budjetoinnistaan.
## Budget-sovelluksen tarjoama toiminnallisuus (perusversio)
### Ennen kirjautumista
Rekisteröityminen:
- [x] Käyttäjä voi luoda järjestelmään käyttäjätunnuksen
  - [x] Käyttäjätunnuksen täytyy olla uniikki ja yli 3 merkkiä pitkä
  - [x] Salasanan täytyy olla yli 8 merkkiä pitkä, sisältää ainakin yhden numeron ja yhden erikoismerkin

Kirjautuminen:
- [x] Käyttäjä voi kirjautua järjestelmään
  - [x] Jos käyttäjätunnusta ei ole tai se on väärin, järjestelmä ilmoittaa siitä
  - [x] Jos salasana on väärin, järjestelmä ilmoittaa siitä
### Kirjautumisen jälkeen
- [x] Käyttäjä voi luoda uuden budjetin:
  - [x] Käyttäjä nimeää budjetin haluamallaan tavalla   
  - [x] Käyttäjän tulee valita budjetille aika: päivä, kuukausi tai vuosi
  - [x] Käyttäjä voi halutessaan lisätä budjettiin kommentin
  - [x] Jos otsikkoa ei ole tai ajanjaksoa valittu, järjestelmä ilmoittaa siitä
- [x] Käyttäjä voi lisätä tuloja ja menoja budjettiin (nimi, kategoria, summa, tyyppi)
- [x] Käyttäjä näkee tulojen ja menojen eron
- [x] Budjetin tiedot avautuvat "listaa budjetit" kohdassa
- [x] Budjettia voi muokata "listaa budjetit" kohdassa
- [x] Käyttäjä voi suodattaa budjetteja (tulon tai menon kategorian mukaan)
- [x] Käyttäjä voi nähdä vain omat budjetoinnit
- [x] Käyttäjä voi kirjautua ulos sovelluksesta
