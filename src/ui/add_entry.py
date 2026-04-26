from tkinter import ttk, constants, StringVar
from src.ui.widgets import BudgetPicker

class AddEntryView:
    """Käyttöliittymäluokka, joka vastaa tulojen ja menojen lisäämisen näkymästä."""

    def __init__(self, root, app, handle_back):
        """Luokan konstruktori, joka alustaa näkymän ja sen komponentit."""
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
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
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
        ttk.Entry(master=self._frame, textvariable=self._amount).grid(row=3, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, text="Kategoria").grid(row=4, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(master=self._frame, textvariable=self._category).grid(row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Tallenna", command=self._submit).grid(row=5, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=5, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, textvariable=self._message).grid(row=6, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

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
