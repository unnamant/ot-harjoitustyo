# Arkkitehtuurikuvaus
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

Kun sovellus aukeaa, käyttäjä voi täyttää suoraan tiedot käyttäjätunnukseen ja salasanaan ja painaa napista "kirjaudu", tai rekisteröityä sivun vasemmasta alakulmasta napista "rekisteröidy", joka vie rekisteröitymissivulle.

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

