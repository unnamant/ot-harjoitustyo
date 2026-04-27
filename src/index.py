from tkinter import Tk
from src.ui.ui import UI

from src.database_connection import get_database_connection
from src.initialize_database import initialize_database

from src.repositories.budget_repository import BudgetRepository
from src.repositories.user_repository import UserRepository

from src.services.budget_service import BudgetService
from src.services.user_service import UserService

def create_services():
    connection = get_database_connection()
    initialize_database(connection)

    user_repository = UserRepository(connection)
    budget_repository = BudgetRepository(connection)

    user_service = UserService(user_repository)
    budget_service = BudgetService(
        budget_repository,
        get_current_username=lambda: user_service.current_user().username
        if user_service.current_user()
        else None
    )

    return user_service, budget_service

def main():
    window = Tk()
    window.title("The Budget App")
    user_service, budget_service = create_services()

    ui = UI(window, user_service, budget_service)
    ui.start()
    window.mainloop()

if __name__ == "__main__":
    main()
