from src.initialize_database import initialize_database

def build():
    """Funktio, joka rakentaa sovelluksen tietokannan ja alustaa tarvittavat taulukot."""
    initialize_database()

if __name__ == "__main__":
    build()
