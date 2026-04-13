import unittest

from src.initialize_database import drop_tables, create_tables
from src.database_connection import get_database_connection

from src.repositories.budget_repository import budget_repository
from src.entities.budget import Budget, Entry
from src.repositories.user_repository import user_repository
from src.entities.user import User

class TestTodoRepository(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        drop_tables(self.connection)
        create_tables(self.connection)

        user_repository.create(User("testuser", "testpassword"))

    def test_create(self):
        budget_repository.create("testuser", Budget(None, "Budjetti 1", "21.4.", ""))

        budgets = budget_repository.list_by_user("testuser")
        self.assertEqual(len(budgets), 1)

    def test_find_all(self):
        budget_repository.create("testuser", Budget(None, "Budjetti 1", "21.4.", ""))
        budget_repository.create("testuser", Budget(None, "Budjetti 2", "syyskuu", ""))
        
        budgets = budget_repository.find_all()
        self.assertEqual(len(budgets), 2)

    def test_delete(self):
        budget = budget_repository.create("testuser", Budget(None, "Budjetti 1", "21.4.", ""))

        budgets = budget_repository.find_all()
        self.assertEqual(len(budgets), 1)

        budget_repository.delete("testuser", budget.id)
        budgets = budget_repository.find_all()
        self.assertEqual(len(budgets), 0)

    def test_add(self):
        budget = budget_repository.create("testuser", Budget(None, "Budjetti 1", "21.4.", ""))
        budget_repository.add(budget.id, Entry(0, "tulo", "2000", "palkka"))

        entries = budget_repository.list_by_budget(budget.id)
        self.assertEqual(len(entries), 1)

    def test_filter_by_category_for_user(self):
        budget1 = budget_repository.create("testuser", Budget(None, "Budjetti 1", "21.4.", ""))
        budget2 = budget_repository.create("testuser", Budget(None, "Budjetti 2", "syyskuu", ""))

        budget_repository.add(budget1.id, Entry(0, "tulo", "2000", "palkka"))
        budget_repository.add(budget1.id, Entry(0, "meno", "200", "ruoka"))
        budget_repository.add(budget2.id, Entry(0, "meno", "100", "ruoka"))

        finds = budget_repository.filter_by_category_for_user("testuser", "ruoka")
        self.assertEqual(len(finds), 2)