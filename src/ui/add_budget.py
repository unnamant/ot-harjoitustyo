from tkinter import ttk, constants, StringVar
from src.ui.widgets import PeriodPicker

class AddBudgetView:
    """Käyttöliittymäluokka, joka vastaa budjetin lisäämisen näkymästä."""

    def __init__(self, root, app, handle_back):
        """Luokan konstruktori, joka alustaa näkymän ja sen komponentit."""
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
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
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
