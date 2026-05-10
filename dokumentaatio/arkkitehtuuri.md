# Arkkitehtuurikuvaus
## Rakenne
Sovelluksen rakenne noudattaa kerrosarkkitehtuuria: _ui_ vastaa käyttöliittymästä, _services_ sovelluslogiikasta ja _repositories_ tietojen pysyväistallennuksesta. _Entities_ sisältää luokat  **User**, **Entry** ja **Budget**, jotka kuvaavat sovelluksen käyttämiä tietokohteista. Koodin pakkausrakenne on seuraava:
```mermaid
classDiagram
     class ui
     class services
     class repositories
     class entities

     ui..>services
     services..>repositories
     services..>entities
     repositories..>entities
```
## Käyttöliittymä
Käyttöliittymä sisältää kolme päänäkymää:
- Kirjautuminen
<img width="370" height="221" alt="kirjautuminen" src="https://github.com/user-attachments/assets/7262fcf7-d170-4762-9ed7-d1cd437b0344" />

- Rekisteröityminen
<img width="400" height="221" alt="rekisteröityminen" src="https://github.com/user-attachments/assets/878aa60c-5767-4528-968b-a12acb028d93" />

- Etusivu (main)
<img width="318" height="289" alt="etusivu" src="https://github.com/user-attachments/assets/88a03324-86ea-432b-b915-d0fa09cd54dc" />

Etusivun alta avautuu viisi näkymää:
- Lisää budjetti
<img width="405" height="289" alt="lisääbudjetti" src="https://github.com/user-attachments/assets/26451f38-dd73-435a-b2bd-6be397e388b5" />

- Lisää tulo/meno
<img width="405" height="404" alt="lisäätulotaimeno" src="https://github.com/user-attachments/assets/63024131-675d-4fac-87e4-a77e5a6fcf94" />

- Listaa budjetit
<img width="611" height="321" alt="listaabudjetit" src="https://github.com/user-attachments/assets/ec8b35d7-0eb6-4c17-bf4c-5366fd93ccf9" />

- Etsi budjetti tulon tai menon kategorian perusteella
<img width="401" height="404" alt="etsi" src="https://github.com/user-attachments/assets/0e188e3e-e775-4c00-b7b8-86542df46cee" />

- Kirjaudu ulos

"Listaa budjetit" kohdasta voi avata budjetin tiedot, jonka jälkeen voi muokata budjettia tai poistaa budjetin:
<img width="705" height="307" alt="budjetintiedot" src="https://github.com/user-attachments/assets/a8554289-1a01-4323-a640-f127ac2b5999" />

Muokkaa budjettia:
<img width="401" height="263" alt="muokkaabudjettia" src="https://github.com/user-attachments/assets/191b4695-c05f-41ff-9073-f0587f97470c" />

Näkymiä on yhteensä 9, joista jokainen on toteutettu omana luokkanaan. Näkymistä yksi on aina kerrallaan näkyvissä, ja näyttämisestä vastaa _ui_-luokka. Käyttöliittymä on pyritty eristyttämään sovelluslogiikasta.

## Sovelluslogiikka
Sovelluksen loogisen tietomallin muodostavat **User** ja **Budget** -luokat sekä Budgetin sisältämän **Entry** luokan.
Luokat kuvaavat käyttäjiä, käyttäjien budjetteja ja budjettien meno-tulo-merkintöjä.
```mermaid
 classDiagram
      User "1" -- "*" Budget
      Budget "1" -- "*" Entry
      class User{
          username
          password
      }
      class Budget{
          id
          user_id
          name
          budget_period
          comment (optional)
          entries
      }
      class Entry{
          id
          entry_type: income/outcome
          amount
          category
      }
```

**BudgetService** vastaa budjetteihin ja tulo-meno-merkintöihin liittyvästä sovelluslogiikasta, ja tarjoaa metodeja kirjautuneelle käyttäjälle, kuten:
- `add_budget(self, name, budget_period, comment=None)`
- `delete_budget(self, index)`
- `add_entry(self, index, entry_type, amount, category)`
- `balance(self, index)`
- `filter_entries_by_category(self, category)`

**UserService** vastaa käyttäjiin liittyvistä toiminnallisuuksista, kuten rekisteröityminen ja kirjautuminen:
- `login(self, username: str, password: str)`
- `register(self, username: str, password: str)`

BudgetService käyttää tietojen pysyväistallennukseen *BudgetRepository* -luokkaa ja UserService käyttää *UserRepository* -luokkaa.

## Päätoiminnallisuus
Kuvataan Budjetti-sovelluksen toimintalogiikan päätoiminnallisuuksia sekvenssikaavioilla.

Kun sovellus aukeaa, jos käyttäjällä on jo käyttäjätunnus, hän voi täyttää suoraan tiedot käyttäjätunnukseen ja salasanaan ja painaa napista "kirjaudu", tai rekisteröityä sivun vasemmasta alakulmasta napista "rekisteröidy", joka vie rekisteröitymissivulle.

Tarkastellaan ensin käyttäjän kirjautumista:

### Käyttäjän kirjautuminen
```mermaid
sequenceDiagram
  actor User
  participant UI as LoginView
  participant UserService
  participant UserRepository

  User->>UI: click "Kirjaudu" button
  UI->>UserService: login("unnis", "salainen123!")
  UserService->>UserRepository: find_by_username("unnis")
  UserRepository-->>UserService: user
  UserService->>UserService: verify password
  UserService->>UserService: set current_user = user
  UserService-->>UI: current_user
  UI->>UI: show_menu()
```

### Käyttäjän rekisteröiminen (uusi käyttäjätunnus)
Kun halutaan rekisteröidä uusi käyttäjä, painetaan ensiksi avautuvan kirjautumissivun vasemmassa alareunassa nappia "Rekisteröidy", joka vie rekisteröitymissivulle, jossa tapahtuu seuraavaa:

```mermaid
sequenceDiagram
  actor User
  participant UI as RegisterView
  participant UserService
  participant UserRepository

  User->>UI: click "Rekisteröidy" button
  UI->>UserService: register("unnis", "salainen123!")
  UserService->>UserRepository: find_by_username("unnis")
  UserRepository-->>UserService: None
  UserService->>UserService: _validate_password(salainen123!)
  UserService->>UserService: _hash_password(salainen123!)
  UserService->>UserRepository: create("unnis", password(hash))
  UserRepository-->>UserService: user
  UserService-->>UI: user
  UI->>UI: message.set(Rekisteröinti onnistui. Voit kirjautua sisään.")
```
### Budjetin luominen
Kun halutaan luoda uusi budjetti, painetaan napista "Luo budjetti", jonka jälkeen tapahtuu seuraava:
```mermaid
sequenceDiagram
  actor User
  participant UI as AddBudgetView
  participant BudgetService
  participant BudgetRepository
  participant budget

  User->>UI: click "Tallenna"
  UI->>BudgetService: add_budget("kesän kuukausien budjetti", "2026", "budjetointi kesälle 2026")
  BudgetService->>BudgetService: get_current_username()
  BudgetService->>budget: Budget(id, "kesän kuukausien budjetti", "2026", "budjetointi kesälle 2026")
  BudgetService->>BudgetRepository: create(budget)
  BudgetRepository-->>BudgetService: budget
  BudgetService-->>UI: budget 
  UI->>UI: message.set(Budjetti "kesän kuukausien budjetti" lisätty."
```

