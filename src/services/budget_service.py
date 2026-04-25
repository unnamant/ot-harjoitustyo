from src.entities.budget import Budget, Entry

class BudgetService:
    """Budjetin ja tulojen sekä menojen ovelluslogiikasta vastaava luokka."""

    def __init__(self, budget_repository, get_current_username):
        """Luokan konstruktori, joka ottaa parametrina budjettirepositorion ja funktion,
        joka palauttaa nykyisen käyttäjätunnuksen."""

        self._budget_repository = budget_repository
        self._get_current_username = get_current_username

    def add_budget(self, name, budget_period, comment=None):
        """Luo uuden budjetin nykyiselle käyttäjälle ja palauttaa luodun budjetin."""

        user_id = self._require_user()
        return self._budget_repository.create(user_id, Budget(None, name, budget_period, comment))

    def list_budgets(self):
        """Hakee kaikki nykyisen käyttäjän budjetit ja palauttaa ne listana."""

        user_id = self._require_user()
        budgets = self._budget_repository.list_by_user(user_id)

        for b in budgets:
            b.entries = self._budget_repository.list_by_budget(b.id)
        return budgets

    def delete_budget(self, index):
        """Poistaa budjetin indeksin perusteella nykyisen käyttäjän budjeteista."""

        budgets = self.list_budgets()
        if not 0 <= index < len(budgets):
            return False
        user_id = self._require_user()
        return self._budget_repository.delete(user_id, budgets[index].id)

    def edit_budget(self, index, name, budget_period, comment):
        """§Muokkaa budjetin tietoja indeksin perusteella nykyisen käyttäjän budjeteista."""

        budgets = self.list_budgets()
        if not 0 <= index < len(budgets):
            return False
        user_id = self._require_user()
        budget_id = budgets[index].id
        self._budget_repository.delete(user_id, budget_id)
        return (
            self._budget_repository.create(user_id, Budget(budget_id, name, budget_period, comment))
        )

    def add_entry(self, index, entry_type, amount, category):
        """Lisää tulon tai menon indeksin perusteella budjettiin nykyisen käyttäjän budjeteista."""

        budgets = self.list_budgets()
        budget = budgets[index]
        return self._budget_repository.add(budget.id, Entry(None, entry_type, amount, category))

    def list_entries(self, index):
        """Hakee kaikki tulot ja menot indeksin perusteella budjetista
        nykyisen käyttäjän budjeteista ja palauttaa ne listana."""

        budgets = self.list_budgets()
        return budgets[index].entries

    def income_total(self, index):
        """Laskee ja palauttaa tulot yhteensä indeksin perusteella
        budjetista nykyisen käyttäjän budjeteista."""

        return self.list_budgets()[index].income_total()

    def expense_total(self, index):
        """Laskee ja palauttaa menot yhteensä indeksin perusteella
        budjetista nykyisen käyttäjän budjeteista."""

        return self.list_budgets()[index].expense_total()

    def balance(self, index):
        """Laskee ja palauttaa saldon indeksin perusteella
        budjetista nykyisen käyttäjän budjeteista."""

        return self.list_budgets()[index].balance()

    def filter_entries_by_category(self, category):
        """Suodattaa ja hakee kaikki tulot ja menot kategorian perusteella
        nykyisen käyttäjän budjeteista ja palauttaa ne listana."""

        user_id = self._require_user()
        return self._budget_repository.filter_by_category_for_user(user_id, category)

    def _require_user(self):
        """Apumetodi, joka hakee nykyisen käyttäjätunnuksen ja varmistaa,
        että käyttäjä on kirjautunut sisään."""

        username = self._get_current_username()
        if not username:
            raise ValueError("Kirjaudu sisään ensin.")
        return username
