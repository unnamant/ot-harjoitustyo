import unittest
from src.entities.budget import Budget, Entry

from src.services.budget_service import BudgetService

class FakeBudgetRepository:
    def __init__(self):
        self.budgets = []
        self.entries = []

    def create(self, user_id: int, budget: Budget):
        new_budget = Budget(len(self.budgets) + 1, budget.name, budget.budget_period, budget.comment)
        new_budget.user_id = user_id
        self.budgets.append(new_budget)
        return new_budget
    
    def list_budgets(self):
        return self.budgets
    
    def list_by_user(self, user_id: int):
        return [b for b in self.budgets if b.user_id == user_id]
    
    def list_by_budget(self, budget_id: int):
        return [e for e in self.entries if e.budget_id == budget_id]

    def add(self, budget_id: int, entry: Entry):
        new_entry = Entry(len(self.entries) + 1, entry.entry_type, entry.amount, entry.category)
        new_entry.budget_id = budget_id
        self.entries.append(new_entry)
        return new_entry
    
    def delete(self, user_id: int, budget_id: int):
        self.budgets = [b for b in self.budgets if b.id != budget_id and user_id == b.user_id]
        self.entries = [e for e in self.entries if e.budget_id != budget_id]
        return True

class TestBudgetService(unittest.TestCase):
    def setUp(self):
        def get_current_username():
            return "testuser"
        
        self.budget_service = BudgetService(
            FakeBudgetRepository(),
            get_current_username
        )
    
    def test_add_budget(self):
        self.budget_service.add_budget("Budjetti 1", "21.4.", "")

        budgets = self.budget_service.list_budgets()
        self.assertEqual(len(budgets), 1)

    def test_add_entry_and_list_entries(self):
        self.budget_service.add_budget("Budjetti 1", "21.4.", "")

        self.budget_service.add_entry(0, "tulo", 1000, "palkka")
        self.budget_service.add_entry(0, "meno", 200, "ruoka")

        self.assertEqual(self.budget_service.income_total(0), 1000)
        self.assertEqual(self.budget_service.expense_total(0), 200)
        self.assertEqual(self.budget_service.balance(0), 800)
        self.assertEqual(len(self.budget_service.list_entries(0)), 2)

    def test_delete_budget(self):
        self.budget_service.add_budget("Budjetti 1", "21.4.", "")

        result = self.budget_service.delete_budget(0)
        self.assertTrue(result)
        self.assertEqual(len(self.budget_service.list_budgets()), 0)
        self.assertFalse(self.budget_service.delete_budget(0))
