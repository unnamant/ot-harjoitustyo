from tkinter import ttk, constants, StringVar, Listbox

from src.database_connection import get_database_connection
from src.initialize_database import initialize_database
from src.repositories.budget_repository import BudgetRepository
from src.repositories.user_repository import UserRepository
from src.services.budget_service import BudgetService
from src.services.user_service import UserService
from src.ui.widgets import PeriodPicker, BudgetPicker
from src.ui.login import LoginView
from src.ui.register import RegisterView

# Github Copilotilla generoitua koodia, jota on kuitenkin muokattu toimivaksi ja paremmaksi.
# Koodi generoitu alkuperäisen tekstikäyttöliittymä-koodin pohjalta.

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

        self._connection = get_database_connection()
        initialize_database(self._connection)

        self._user_repo = UserRepository(self._connection)
        self._budget_repo = BudgetRepository(self._connection)
        self._user_service = UserService(self._user_repo)

        self._app = BudgetService(
            self._budget_repo,
            get_current_username=lambda: self._user_service.current_user().username if self._user_service.current_user() else None
        )

    def start(self):
        self._show_login()

    def _show_login(self):
        self._hide_current_view()
        self._current_view = LoginView(self._root, self._user_service, self._show_menu, self._show_register)
        self._current_view.pack()

    def _handle_logout(self):
        self._user_service.logout()
        self._show_login()

    def _show_register(self):
        self._hide_current_view()
        self._current_view = RegisterView(self._root, self._user_service, self._show_login)
        self._current_view.pack()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_menu(self):
        self._hide_current_view()
        self._current_view = MenuView(
            self._root,
            handle_add_budget=self._show_add_budget,
            handle_add_entry=self._show_add_entry,
            handle_list_budgets=self._show_list_budgets,
            handle_delete_budget=self._show_delete_budget,
            handle_show_balance=self._show_balance,
            handle_logout=self._handle_logout,
            handle_search_by_category=self._show_search_by_category
        )
        self._current_view.pack()

    def _show_add_budget(self):
        self._hide_current_view()
        self._current_view = AddBudgetView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_add_entry(self):
        self._hide_current_view()
        self._current_view = AddEntryView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_list_budgets(self):
        self._hide_current_view()
        self._current_view = ListBudgetsView(self._root, self._app, self._show_menu, self._show_budget)
        self._current_view.pack()

    def _show_budget(self, budget_index):
        self._hide_current_view()
        self._current_view = BudgetDetailsView(
            self._root,
            self._app,
            budget_index,
            handle_back=self._show_list_budgets
        )
        self._current_view.pack()

    def _show_delete_budget(self):
        self._hide_current_view()
        self._current_view = DeleteBudgetView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_balance(self):
        self._hide_current_view()
        self._current_view = BalanceView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_search_by_category(self):
        self._hide_current_view()
        self._current_view = SearchByCategoryView(self._root, self._app, self._show_menu, self._show_budget)
        self._current_view.pack()

class MenuView:
    def __init__(self, root, handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance, handle_logout, handle_search_by_category):
        self._root = root
        self._frame = None
        self._initialize(handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance, handle_logout, handle_search_by_category)

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self, handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance, handle_logout, handle_search_by_category):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Budjettisovellus").grid(
            row=0, column=0, sticky=constants.W, padx=5, pady=5
        )

        ttk.Button(master=self._frame, text="Lisää budjetti", command=handle_add_budget).grid(
            row=1, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Lisää tulo/meno", command=handle_add_entry).grid(
            row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Listaa budjetit", command=handle_list_budgets).grid(
            row=3, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Etsi budjetti", command=handle_search_by_category).grid(
            row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Poista budjetti", command=handle_delete_budget).grid(
            row=5, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Näytä saldo", command=handle_show_balance).grid(
            row=6, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Kirjaudu ulos", command=handle_logout).grid(
            row=7, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)


class AddBudgetView:
    def __init__(self, root, app, handle_back):
        self._root = root
        self._app = app
        self._handle_back = handle_back

        self._name = StringVar()
        self._period_picker = None
        self._comment = StringVar()
        self._message = StringVar()

        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Lisää budjetti").grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        ttk.Label(master=self._frame, text="Nimi").grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(master=self._frame, textvariable=self._name).grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._period_picker = PeriodPicker(self._frame)
        self._period_picker.grid(row=2, column=0, columnspan=2, sticky=(constants.E, constants.W))

        ttk.Label(master=self._frame, text="Kommentti").grid(row=3, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(master=self._frame, textvariable=self._comment).grid(row=3, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Tallenna", command=self._submit).grid(row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, textvariable=self._message).grid(row=5, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

    def _submit(self):
        name = self._name.get().strip()

        period = self._period_picker.get_period_key()
        if not period:
            self._message.set("Virhe: ajanjakson arvo puuttuu.")
            return

        comment = self._comment.get().strip()

        if not name or not period:
            self._message.set("Virhe: nimi ja ajanjakso ovat pakollisia.")
            return

        self._app.add_budget(name, period, comment)
        self._message.set(f'Budjetti "{name}" lisätty.')


class ListBudgetsView:
    def __init__(self, root, app, handle_back, show_budget):
        self._root = root
        self._app = app
        self._handle_back = handle_back
        self._handle_open_budget = show_budget

        self._picker = None
        self._frame = None
        self._message = StringVar()
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _open(self):
        index = self._picker.get_selected_index()
        if index is None:
            self._message.set("Valitse budjetti listasta.")
            return
        self._handle_open_budget(index)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Budjetit").grid(row=0, column=0, sticky=constants.W, padx=5, pady=5)

        self._picker = BudgetPicker(self._frame, self._app)
        self._picker.grid(row=1, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        
        ttk.Button(master=self._frame, text="Avaa budjetti", command=self._open).grid(
        row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(
        row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)
        self._frame.grid_columnconfigure(1, weight=1, minsize=300)
    

class BudgetDetailsView:
    def __init__(self, root, app, budget_index, handle_back):
        self._root = root
        self._app = app
        self._budget_index = budget_index
        self._handle_back = handle_back

        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        budget = self._app.list_budgets()[self._budget_index]
        entries = self._app.list_entries(self._budget_index)

        ttk.Label(master=self._frame, text=f"{budget.name} ({budget.budget_period})").grid(
        row=0, column=0, sticky=constants.W, padx=5, pady=5)

        if entries:
            text = "\n".join([f"{e.entry_type} {e.amount}€ ({e.category})" for e in entries])
        else:
            text = "Ei tuloja/menoja."

        balance = self._app.balance(self._budget_index)

        ttk.Label(master=self._frame, text=text, justify=constants.LEFT).grid(
            row=1, column=0, sticky=constants.W, padx=5, pady=5
        )

        ttk.Label(
            master=self._frame,
            text=f"Saldo: {balance} €"
        ).grid(row=2, column=0, sticky=constants.W, padx=5, pady=5)

        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(
            row=3, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)

class SearchByCategoryView:
    def __init__(self, root, app, handle_back, handle_open_budget):
        self._root = root
        self._app = app
        self._handle_back = handle_back
        self._handle_open_budget = handle_open_budget

        self._category = StringVar()
        self._message = StringVar()

        self._results = []
        self._listbox = None
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Etsi tapahtumat tulon tai menon kategorian mukaan").grid(
            row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5
        )

        ttk.Label(master=self._frame, text="Kategoria").grid(
            row=1, column=0, sticky=constants.W, padx=5, pady=5
        )

        entry = ttk.Entry(master=self._frame, textvariable=self._category)
        entry.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        entry.bind("<Return>", lambda e: self._search())

        ttk.Button(master=self._frame, text="Hae", command=self._search).grid(
            row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        self._listbox = Listbox(master=self._frame, height=10)
        self._listbox.grid(row=3, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Avaa budjetti", command=self._open_selected_budget).grid(
            row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(
            row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        ttk.Label(master=self._frame, textvariable=self._message).grid(
            row=5, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5
        )

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

    def _search(self):
        category = self._category.get().strip()
        self._listbox.delete(0, "end")
        self._message.set("")
        self._results = []

        if not category:
            self._message.set("Anna kategoria.")
            return

        budgets = self._app.list_budgets()

        id_to_budget = {}
        for i, b in enumerate(budgets):
            if getattr(b, "id", None) is not None:
                id_to_budget[b.id] = (i, b)

        finds = self._app.filter_entries_by_category(category)

        if not finds:
            self._message.set("Ei osumia.")
            return


        self._results = []

        for budget_id, e in finds:
            budget_index = id_to_budget.get(budget_id, (None, None))[0]
            budget_obj = id_to_budget.get(budget_id, (None, None))[1]

            entry_type = getattr(e, "entry_type", getattr(e, "type", ""))
            budget_name = budget_obj.name if budget_obj else f"Budjetti #{budget_id}"

            self._results.append((budget_index, budget_id, e))
            self._listbox.insert("end", f"{budget_name}: {entry_type} {e.amount}€ ({e.category})")

        self._message.set(f"Löytyi {len(self._results)} tapahtumaa.")

    def _open_selected_budget(self):
        select = self._listbox.curselection()
        if not select:
            self._message.set("Valitse budjetti listasta.")
            return

        budget_index, budget_id, _ = self._results[select[0]]

        if budget_index is None:
            self._message.set(f"Budjettia (id={budget_id}) ei löydy budjettilistasta. Korjaa Budget.id list_budgets()-palautuksessa.")
            return

        self._handle_open_budget(budget_index)

class DeleteBudgetView:
    def __init__(self, root, app, handle_back):
        self._root = root
        self._app = app
        self._handle_back = handle_back
        self._picker = None
        self._message = StringVar()

        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(
            master=self._frame,
            text="Poista budjetti"
        ).grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        self._picker = BudgetPicker(self._frame, self._app)
        self._picker.grid(
            row=1, column=0, columnspan=2, sticky=(constants.E, constants.W)
        )

        ttk.Button(
            master=self._frame,
            text="Poista",
            command=self._submit
        ).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(
            master=self._frame,
            text="Takaisin",
            command=self._handle_back
        ).grid(row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, textvariable=self._message).grid(
            row=3, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)
        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

    def _submit(self):
        index = self._picker.get_selected_index()
        if index is None:
            self._message.set("Valitse budjetti listasta.")
            return

        self._app.delete_budget(index)
        self._picker.refresh()
        self._message.set(f'Budjetti poistettu.')

class BalanceView:
    def __init__(self, root, app, handle_back):
        self._root = root
        self._app = app
        self._handle_back = handle_back

        self._picker = None
        self._message = StringVar()

        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Näytä saldo").grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        self._picker = BudgetPicker(self._frame, self._app)
        self._picker.grid(
            row=1, column=0, columnspan=2, sticky=(constants.E, constants.W)
        )

        ttk.Button(master=self._frame, text="Laske", command=self._submit).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, textvariable=self._message).grid(row=3, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)
        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

    def _submit(self):
        index = self._picker.get_selected_index()
        if index is None:
            self._message.set("Valitse budjetti listasta.")
            return

        self._message.set(f"Saldo: {self._app.balance(index)} €")

class AddEntryView:
    def __init__(self, root, app, handle_back):
        self._root = root
        self._app = app
        self._handle_back = handle_back

        self._picker = None
        self._entry_type = StringVar()
        self._amount = StringVar()
        self._category = StringVar()
        self._message = StringVar()

        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Lisää tulo tai meno budjettiin").grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        self._picker = BudgetPicker(self._frame, self._app)
        self._picker.grid(row=1, column=0, columnspan=2, sticky=(constants.E, constants.W))

        ttk.Label(master=self._frame, text="Tyyppi").grid(row=2, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Combobox(
            master=self._frame,
            textvariable=self._entry_type,
            values=["tulo", "meno"],
            state="readonly"
        ).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, text="Määrä (€)").grid(row=3, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(master=self._frame, textvariable=self._amount).grid(
            row=3, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        ttk.Label(master=self._frame, text="Kategoria").grid(row=4, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(master=self._frame, textvariable=self._category).grid(
            row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        ttk.Button(master=self._frame, text="Tallenna", command=self._submit).grid(
            row=5, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(
            row=5, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        ttk.Label(master=self._frame, textvariable=self._message).grid(
            row=6, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5
        )

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

    def _submit(self):
        index = self._picker.get_selected_index()
        if index is None:
            self._message.set("Valitse budjetti listasta.")
            return

        entry_type = self._entry_type.get().strip().lower()
        if entry_type not in ("tulo", "meno"):
            self._message.set("Virhe: tyyppi pitää olla 'tulo' tai 'meno'.")
            return

        try:
            amount = float(self._amount.get().strip())
        except ValueError:
            self._message.set("Virhe: määrä pitää olla numero.")
            return

        if amount < 0:
            self._message.set("Virhe: määrä ei voi olla negatiivinen.")
            return

        category = self._category.get().strip()
        if not category:
            self._message.set("Virhe: kategoria puuttuu.")
            return

        self._app.add_entry(index, entry_type, amount, category)
        self._picker.refresh()

        if entry_type == "tulo":
            self._message.set("Tulo lisätty budjettiin.")
        else:
            self._message.set("Meno lisätty budjettiin.")