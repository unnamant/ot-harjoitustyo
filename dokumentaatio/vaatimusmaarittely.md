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
- [x] Käyttäjä voi valita budjetoinnin ajan: päivä, kuukausi tai vuosi
- [x] Käyttäjä lisää tuloja ja menoja budjettiin (nimi, kategoria, summa, tyyppi)
- [x] Käyttäjä näkee tulojen ja menojen eron.
- Budjetin tiedot avautuvat "listaa budjetit" kohdassa

- [x] Käyttäjä voi nähdä vain omat budjetoinnit.

Käyttäjä voi kirjautua ulos järjestelmästä.
## Perusversiota laajentavat jatkokehitysideat
Ajan salliessa perusversiota täydennetään esim. seuraavilla toiminnallisuuksilla:
- Käyttäjä voi merkitä, miten on pysynyt budjetissa/kuinka budjetointi on onnistunut
- Käyttäjä voi julkaista budjetointisuunnitelmansa muille käyttäjille julki
- Käyttäjät voivat kommentoida toisten julkisiin budjetointeihin
