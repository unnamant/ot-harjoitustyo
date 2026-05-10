from src.entities.budget import Budget, Entry
from src.database_connection import get_database_connection

class BudgetRepository:
    """Vastaa budjettien ja niihin liittyvien tietojen tallentamisesta
    ja hakemisesta tietokannasta."""
    def __init__(self, connection):
        """Luokan konstruktori, joka ottaa parametrina tietokantayhteyden."""

        self._connection = connection

    def find_all(self):
        """Palauttaa listan kaikista budjeteista tietokannassa."""

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM budgets")
        rows = cursor.fetchall()

        return [
            Budget(r["id"], r["name"], r["budget_period"], r["comment"])
            for r in rows
        ]

    def create(self, user_id: int, budget: Budget):
        """Luo uuden budjetin tietokantaan ja palauttaa luodun budjetin, jossa on päivitetty id."""

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO budgets (user_id, name, budget_period, comment) VALUES (?, ?, ?, ?)",
            (user_id, budget.name, budget.budget_period, budget.comment)
        )
        self._connection.commit()

        return Budget(cursor.lastrowid, budget.name, budget.budget_period, budget.comment)

    def delete(self, user_id: int, budget_id: int):
        """Poistaa budjetin ja siihen liittyvät tulot ja menot tietokannasta."""

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
        """Palauttaa listan budjeteista, jotka kuuluvat tietylle käyttäjälle."""

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, name, budget_period, comment FROM budgets WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = cursor.fetchall()
        return [Budget(r["id"], r["name"], r["budget_period"], r["comment"]) for r in rows]

    def add(self, budget_id: int, entry: Entry):
        """Lisää uuden tulon tai menon tiettyyn budjettiin
        ja palauttaa luodun entryn, jossa on päivitetty id."""

        cursor = self._connection.cursor()

        cursor.execute(
            """INSERT INTO entries (budget_id, type, amount, category) 
            VALUES (?, ?, ?, ?)""",
            (budget_id, entry.entry_type, entry.amount, entry.category),
        )
        self._connection.commit()
        return Entry(cursor.lastrowid, entry.entry_type, entry.amount, entry.category)

    def update(self, user_id: int,  budget_id: int, budget: Budget):
        """Päivittää budjetin tietokannassa ja palauttaa päivitetyn budjetin."""

        cursor = self._connection.cursor()

        cursor.execute(
            """UPDATE budgets SET name = ?, budget_period = ?, comment = ? 
            WHERE id = ? AND user_id = ?""",
            (budget.name, budget.budget_period, budget.comment, budget_id, user_id)
        )

        self._connection.commit()
        return budget

    def list_by_budget(self, budget_id: int):
        """Palauttaa listan tuloista ja menoista, jotka kuuluvat tiettyyn budjettiin."""

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, type, amount, category FROM entries WHERE budget_id = ? ORDER BY id",
            (budget_id,),
        )
        rows = cursor.fetchall()
        return [Entry(r["id"], r["type"], r["amount"], r["category"]) for r in rows]

    def filter_by_category_for_user(self, username: str, category: str):
        """Palauttaa listan tuloista ja menoista,
        jotka kuuluvat tiettyyn kategoriaan ja käyttäjään."""

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
