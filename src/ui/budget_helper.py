def ask_period_key() -> str:
    print("Valitse budjetin ajanjakso:")
    print("1) Päivä")
    print("2) Kuukausi")
    print("3) Vuosi")
    choice = input("Valitse (1-3): ")

    if choice == "1":
        day = input("Anna päivä: ").strip()
        return day

    if choice == "2":
        month = input("Anna kuukausi (esim. muodossa syyskuu): ")
        return month

    if choice == "3":
        year = input("Anna vuosi: ")
        return year
    
    elif choice not in ["1", "2", "3"]:
        print("Virhe: valitse 1, 2 tai 3.")
        return ask_period_key()
    
def show_budgets_and_choose_index(app, prompt: str = "Valitse budjetti indeksin mukaan: ") -> int | None:
    budgets = app.list_budgets()
    if not budgets:
        print("Ei budjetteja. Lisää budjetti ensin.")
        return None

    for i, b in enumerate(budgets):
        print(f"{i}. {b.name} ({b.budget_period})")

    try:
        index = int(input(prompt))
    except ValueError:
        print("Virhe: anna numero.")
        return None

    if index < 0 or index >= len(budgets):
        print("Virhe: indeksi ei ole listassa.")
        return None

    return index