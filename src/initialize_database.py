from src.database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS entries;
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS budgets;
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS users;
    ''')

    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')

    connection.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            budget_period TEXT NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)

    connection.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        budget_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('tulo','meno')),
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        FOREIGN KEY (budget_id) REFERENCES budgets(id)
    );
    """)

    connection.commit()

def initialize_database(connection):
    connection = get_database_connection()
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
