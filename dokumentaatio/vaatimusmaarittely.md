# Vaatimusmäärittely
## Sovelluksen tarkoitus
Sovelluksen tarkoituksena on antaa työkaluja käyttäjälle auttaakseen häntä pitämään huolta päivittäisestä, kuukausittaisesta ja/tai vuosittaisesta budjetoinnistaan.
## Budget-sovelluksen tarjoama toiminnallisuus (perusversio)
### Ennen kirjautumista
Rekisteröityminen:
- Käyttäjä voi luoda järjestelmään käyttäjätunnuksen
  - Käyttäjätunnuksen täytyy olla uniikki ja yli 3 merkkiä pitkä
  - Salasanan täytyy olla yli 8 merkkiä pitkä, sisältää ainakin yhden numeron ja yhden erikoismerkin

Kirjautuminen:
- Käyttäjä voi kirjautua järjestelmään
  - Jos käyttäjätunnusta ei ole tai se on väärin, järjestelmä ilmoittaa siitä
  - Jos salasana on väärin, järjestelmä ilmoittaa siitä
### Kirjautumisen jälkeen
- Käyttäjä voi valita budjetoinnin ajan: päivä, kuukausi tai vuosi
- Käyttäjä lisää tuloja ja menoja budjettiin (nimi, kategoria, summa, tyyppi)
- Käyttäjä näkee tulojen ja menojen eron.
- Budjetin tiedot avautuvat "listaa budjetit" kohdassa

Käyttäjä voi nähdä vain omat budjetoinnit.

Käyttäjä voi kirjautua ulos järjestelmästä.
## Perusversiota laajentavat jatkokehitysideat
Ajan salliessa perusversiota täydennetään esim. seuraavilla toiminnallisuuksilla:
- Käyttäjä voi merkitä, miten on pysynyt budjetissa/kuinka budjetointi on onnistunut
- Käyttäjä voi julkaista budjetointisuunnitelmansa muille käyttäjille julki
- Käyttäjät voivat kommentoida toisten julkisiin budjetointeihin
