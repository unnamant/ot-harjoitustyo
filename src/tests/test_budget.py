import unittest
from src.services.budget_service import BudgetService


class TestBudgetService(unittest.TestCase):

    def setUp(self):
        self.app = BudgetService()

    def test_add_budget(self):
        self.app.add_budget("Budjetti 1", "21.4.", "")

        budgets = self.app.list_budgets()
        self.assertEqual(len(budgets), 1)

    def test_add_entry(self):
        self.app.add_budget("Budjetti 1", "21.4.", "")

        self.app.add_entry(0, "tulo", 1000, "palkka")
        self.app.add_entry(0, "meno", 200, "ruoka")

        self.assertEqual(self.app.income_total(0), 1000)
        self.assertEqual(self.app.expense_total(0), 200)
        self.assertEqual(self.app.balance(0), 800)

    def test_delete_budget(self):
        self.app.add_budget("Budjetti 1", "21.4.", "")

        result = self.app.delete_budget(0)
        self.assertTrue(result)
        self.assertEqual(len(self.app.budgets), 0)
