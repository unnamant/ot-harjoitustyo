from tkinter import ttk, constants, StringVar
from src.ui.widgets import BudgetPicker

class ListBudgetsView:
    """Käyttöliittymäluokka, joka vastaa budjettien listauksen näkymästä."""

    def __init__(self, root, app, handle_back, show_budget):
        """Luokan konstruktori, joka alustaa näkymän ja sen komponentit.
        
        Args:
            root: Tkinterin juurikomponentti, johon näkymä asetetaan.
            app: Sovelluksen päälogiikkaa tarjoava olio, jonka metodeja näkymä käyttää.
            handle_back: Funktio, joka kutsutaan, kun käyttäjä haluaa palata edelliseen näkymään.
            show_budget: Funktio, joka kutsutaan, kun käyttäjä haluaa avata budjetin tarkemmat tiedot. 
            Funktio saa parametrinaan budjetin indeksin budjettilistassa.
        """
        self._root = root
        self._app = app
        self._handle_back = handle_back
        self._handle_open_budget = show_budget

        self._picker = None
        self._frame = None
        self._message = StringVar()
        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
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
    """Käyttöliittymäluokka, joka vastaa yksittäisen budjetin tietojen näyttämisestä."""

    def __init__(self, root, app, budget_index, handle_back, handle_edit, handle_delete_budget):
        """Luokan konstruktori, joka alustaa näkymän ja sen komponentit.
        
        Args:
            root: Tkinterin juurikomponentti, johon näkymä asetetaan.
            app: Sovelluksen päälogiikkaa tarjoava olio, jonka metodeja näkymä käyttää.
            budget_index: Näytettävän budjetin indeksi budjettilistassa.
            handle_back: Funktio, joka kutsutaan, kun käyttäjä haluaa palata edelliseen näkymään.
            handle_edit: Funktio, joka kutsutaan, kun käyttäjä haluaa muokata budjettia.
            Funktio saa parametrinaan budjetin indeksin budjettilistassa.
            handle_delete_budget: Funktio, joka kutsutaan, kun käyttäjä haluaa poistaa budjetin.
            Funktio saa parametrinaan budjetin indeksin budjettilistassa.
        """
        self._root = root
        self._app = app
        self._budget_index = budget_index
        self._handle_back = handle_back
        self._handle_edit = handle_edit
        self._handle_delete_budget = handle_delete_budget

        self._frame = None
        self._initialize()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        budget = self._app.list_budgets()[self._budget_index]
        entries = self._app.list_entries(self._budget_index)

        ttk.Label(master=self._frame, text=f"{budget.name} ({budget.budget_period})").grid(row=0, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Label(master=self._frame, text=f"{budget.comment}").grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)

        if entries:
            text = "\n".join([f"{e.entry_type} {e.amount}€ ({e.category})" for e in entries])
        else:
            text = "Ei tuloja/menoja."

        balance = self._app.balance(self._budget_index)

        ttk.Label(master=self._frame, text=text, justify=constants.LEFT).grid(row=2, column=0, sticky=constants.W, padx=5, pady=5)

        ttk.Label(
            master=self._frame,
            text=f"Saldo: {balance} €"
        ).grid(row=3, column=0, sticky=constants.W, padx=5, pady=5)

        ttk.Button(master=self._frame, text="Muokkaa budjettia", command=self._handle_edit).grid(row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Poista budjetti", command=self._handle_delete_budget).grid(row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=4, column=2, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)
        self._frame.grid_columnconfigure(1, weight=1, minsize=200)
        self._frame.grid_columnconfigure(2, weight=1, minsize=200)
