from src.entities.budget import Budget, Entry
from src.database_connection import get_database_connection

class BudgetRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM budgets")
        rows = cursor.fetchall()

        return [
            Budget(r["id"], r["name"], r["budget_period"], r["comment"])
            for r in rows
        ]

    def create(self, username: str, budget: Budget):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO budgets (user_id, name, budget_period, comment) VALUES (?, ?, ?, ?)",
            (username, budget.name, budget.budget_period, budget.comment)
        )
        self._connection.commit()

        return Budget(budget.name, budget.budget_period, budget.comment, cursor.lastrowid)

    def delete(self, user_id: int, budget_id: int):
        cursor = self._connection.cursor()

        cursor.execute(
            "DELETE FROM entries WHERE budget_id = ?",
            (budget_id,),
        )
        cursor.execute(
            "DELETE FROM budgets WHERE id = ? AND user_id = ?",
            (budget_id, user_id),
        )
        self._connection.commit()
        return cursor.rowcount > 0

    def list_by_user(self, user_id: int):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, name, budget_period, comment FROM budgets WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = cursor.fetchall()
        return [Budget(r["id"], r["name"], r["budget_period"], r["comment"]) for r in rows]

    def add(self, budget_id: int, entry: Entry):
        cursor = self._connection.cursor()

        cursor.execute(
            """INSERT INTO entries (budget_id, type, amount, category) 
            VALUES (?, ?, ?, ?)""",
            (budget_id, entry.entry_type, entry.amount, entry.category),
        )
        self._connection.commit()
        return Entry(entry.entry_type, entry.amount, entry.category, cursor.lastrowid)

    def list_by_budget(self, budget_id: int):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, type, amount, category FROM entries WHERE budget_id = ? ORDER BY id",
            (budget_id,),
        )
        rows = cursor.fetchall()
        return [Entry(r["id"], r["type"], r["amount"], r["category"]) for r in rows]

    def filter_by_category_for_user(self, username: str, category: str):
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT b.id AS budget_id, e.id, e.type, e.amount, e.category
            FROM entries e
            JOIN budgets b ON b.id = e.budget_id
            WHERE b.user_id = ? AND LOWER(e.category) = LOWER(?)
            ORDER BY b.id, e.id
            """,
            (username, category),
        )
        rows = cursor.fetchall()
        return [
            (r["budget_id"], Entry(r["id"], r["type"], r["amount"], r["category"]))
            for r in rows
        ]

budget_repository = BudgetRepository(get_database_connection())
