from tkinter import ttk, constants, StringVar

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
        self._current_view = ListBudgetsView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_delete_budget(self):
        self._hide_current_view()
        self._current_view = DeleteBudgetView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_balance(self):
        self._hide_current_view()
        self._current_view = BalanceView(self._root, self._app, self._show_menu)
        self._current_view.pack()


class MenuView:
    def __init__(self, root, handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance):
        self._root = root
        self._frame = None
        self._initialize(handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance)

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self, handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance):
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
        ttk.Button(master=self._frame, text="Poista budjetti", command=handle_delete_budget).grid(
            row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Näytä saldo", command=handle_show_balance).grid(
            row=5, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=320)


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

        ttk.Button(master=self._frame, text="Tallenna", command=self._submit).grid(row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

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
    def __init__(self, root, app, handle_back):
        self._root = root
        self._app = app
        self._handle_back = handle_back
        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Budjetit").grid(row=0, column=0, sticky=constants.W, padx=5, pady=5)

        budgets = self._app.list_budgets()
        text = "\n".join([f"{i}. {b.name} {b.budget_period}" for i, b in enumerate(budgets)]) or "Ei budjetteja."

        ttk.Label(master=self._frame, text=text, justify=constants.LEFT).grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=1, minsize=320)


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
        ).grid(row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(
            master=self._frame,
            text="Takaisin",
            command=self._handle_back
        ).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

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

        ttk.Button(master=self._frame, text="Laske", command=self._submit).grid(row=2, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

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
            row=5, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(
            row=5, column=1, sticky=(constants.E, constants.W), padx=5, pady=5
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