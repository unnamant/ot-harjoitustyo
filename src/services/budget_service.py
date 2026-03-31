from src.entities.budget import Budget, Entry

class BudgetService:
    def __init__(self):
        self.budgets: list[Budget] = []

    def add_budget(self, name, budget_period, comment=None):
        budget = Budget(name, budget_period, comment)
        self.budgets.append(budget)

    def list_budgets(self):
        return self.budgets
    
    def delete_budget(self, index):
        if 0 <= index < len(self.budgets):
            self.budgets.pop(index)
            return True
        return False

    def add_entry(self, index, type, amount, category):
        self.budgets[index].entries.append(Entry(type, amount, category))
    
    def income_total(self, index):
        return self.budgets[index].income_total()

    def expense_total(self, index):
        return self.budgets[index].expense_total()

    def balance(self, index):
        return self.budgets[index].balance()

    def filter_entries_by_category(self, category):
        results = []
        for b in self.budgets:
            for e in b.entries:
                if e.category == category:
                    results.append((b, e))
        return results