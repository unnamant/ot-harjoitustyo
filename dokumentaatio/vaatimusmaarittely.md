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
Käyttäjä voi valita tekeekö budjetoinnin:
- päivälle
  - esim. ateriat, hupi.
  - Käyttäjä valitsee kalenterista päivän, mille tekee suunnitelman
- kuukaudelle
  - esim. vuokra, laskut, ruoka, muut menot.
- vuodelle
  - esim. säästöt, laskut, menot, tulot.

Käyttäjä voi nähdä vain omat budjetoinnit.

Käyttäjä voi kirjautua ulos järjestelmästä.
## Perusversiota laajentavat jatkokehitysideat
Ajan salliessa perusversiota täydennetään esim. seuraavilla toiminnallisuuksilla:
- Käyttäjä voi merkitä, miten on pysynyt budjetissa/kuinka budjetointi on onnistunut
- Käyttäjä voi julkaista budjetointisuunnitelmansa muille käyttäjille julki
- Budjetointisuunnitelma laskee menot yhteensä
  - Kuukauden ja vuoden budjetoinnissa laskee menojen ja tulojen erotuksen esim. jos tiedossa kiinteä palkka
- Käyttäjät voivat kommentoida toisten julkisiin budjetointeihin
