from src.entities.user import User
from src.database_connection import get_database_connection

def get_user_by_row(row):
    return User(row["username"], row["password"]) if row else None

class UserRepository:
    """Käyttäjään liittyvien tietokantaoperaatioiden toteutusluokka"""

    def __init__(self, connection):
        """Luokan konstruktori, joka ottaa parametrina tietokantayhteyden."""

        self._connection = connection

    def find_all(self):
        """Hakee kaikki käyttäjät tietokannasta ja palauttaa ne listana."""

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        return [get_user_by_row(row) for row in rows]

    def find_by_username(self, username: str):
        """Hakee tietokannasta käyttäjän
        käyttäjätunnuksen perusteella ja palauttaa sen User-oliona,
        tai None jos käyttäjää ei löydy."""

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()

        return get_user_by_row(row)

    def create(self, user: User):
        """Luo uuden käyttäjän tietokantaan ja palauttaa luodun User-olion."""

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, user.password)
        )
        self._connection.commit()

        return user

user_repository = UserRepository(get_database_connection())
