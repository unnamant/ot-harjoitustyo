from src.services.budget_service import BudgetService
from src.ui.budget_helper import ask_period_key, show_budgets_and_choose_index


def main():
    app = BudgetService()

    while True:
        print()
        print("1) Lisää budjetti")
        print("2) Lisää budjettiin tulo tai meno")
        print("3) Listaa budjetit")
        print("4) Poista budjetti")
        print("5) Näytä tulot")
        print("6) Näytä menot")
        print("7) Näytä saldo")
        print("8) Suodata budjetit menon tai tulon kategorian mukaan")
        print("0) Lopeta")

        command = input("Valitse toiminto: ")

        if command == "1":
            name = input("Nimi: ")
            budget_period = ask_period_key()
            comment = input("Kommentti (valinnainen): ")
            app.add_budget(name, budget_period, comment)

        elif command == "2":
            index = show_budgets_and_choose_index(app)
            if index is None:
                continue

            type = input("Tulo vai meno?: ").strip().lower()
            if type not in ["tulo", "meno"]:
                print("Virhe: anna 'tulo' tai 'meno'.")
                continue
            amount = float(input("Määrä: "))
            if amount < 0:
                print("Virhe: määrä ei voi olla negatiivinen.")
                continue

            category = input("Kategoria: ").strip()

            app.add_entry(index, type, amount, category)

        elif command == "3":
            budgets = app.list_budgets()
            if not budgets:
                print("Ei budjetteja.")
                continue
            for i, b in enumerate(budgets):
                print(f"{i}. {b.name} {b.budget_period}")

        elif command == "4":
            index = show_budgets_and_choose_index(app)
            if index is None:
                continue
            app.delete_budget(index)

        elif command == "5":
            index = show_budgets_and_choose_index(app)
            if index is None:
                continue
            print(f"Tulot yhteensä: {app.income_total(index)} €")

        elif command == "6":
            index = show_budgets_and_choose_index(app)
            if index is None:
                continue
            print(f"Menot yhteensä: {app.expense_total(index)} €")

        elif command == "7":
            index = show_budgets_and_choose_index(app)
            if index is None:
                continue
            print(f"Saldo: {app.balance(index)} €")

        elif command == "8":
            category = input("Anna kategoria: ").strip().lower()
            results = app.filter_entries_by_category(category)
            if not results:
                print("Ei tuloksia.")
                continue
            for b, e in results:
                print(
                    f"{b.name} ({b.budget_period}): {e.type} {e.amount} € {e.category}")

        elif command == "0":
            print("Lopetetaan ohjelma.")
            break
