from src.entities.budget import Budget, Entry

class BudgetService:
    def __init__(self, budget_repository, get_current_username):
        self._budget_repository = budget_repository
        self._get_current_username = get_current_username

    def add_budget(self, name, budget_period, comment=None):
        user_id = self._require_user()
        budget_period = Budget(None, name, budget_period, comment)
        return self._budget_repository.create(user_id, budget_period)

    def list_budgets(self):
        user_id = self._require_user()
        budgets = self._budget_repository.list_by_user(user_id)

        for b in budgets:
            b.entries = self._budget_repository.list_by_budget(b.id)
        return budgets

    def delete_budget(self, index):
        budgets = self.list_budgets()
        if not 0 <= index < len(budgets):
            return False
        user_id = self._require_user()
        return self._budget_repository.delete(user_id, budgets[index].id)

    def add_entry(self, index, entry_type, amount, category):
        budgets = self.list_budgets()
        budget = budgets[index]
        return self._budget_repository.add(budget.id, Entry(None, entry_type, amount, category))

    def income_total(self, index):
        return self.list_budgets()[index].income_total()

    def expense_total(self, index):
        return self.list_budgets()[index].expence_total()

    def balance(self, index):
        return self.list_budgets()[index].balance()

    def filter_entries_by_category(self, category):
        user_id = self._require_user()
        finds = self._budget_repository.filter_by_category_for_user(user_id, category)
        budgets = {b.id: b for b in self.list_budgets()}
        results = []
        for budget_id, entry in finds:
            results.append((budgets[budget_id], entry))
        return results

    def _require_user(self):
        username = self._get_current_username()
        if not username:
            raise ValueError("Kirjaudu sisään ensin.")
        return username
