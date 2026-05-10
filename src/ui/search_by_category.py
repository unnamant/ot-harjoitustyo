from tkinter import ttk, constants, StringVar, Listbox

class SearchByCategoryView:
    """Käyttöliittymäluokka, joka vastaa budjettien hakemisesta tulon tai menon kategorian perusteella."""

    def __init__(self, root, app, handle_back, handle_open_budget):
        """Luokan konstruktori, joka alustaa näkymän ja sen komponentit.
        
        Args:
            root: Tkinterin juurikomponentti, johon näkymä asetetaan.
            app: Sovelluksen päälogiikkaa tarjoava olio, jonka metodeja näkymä käyttää.
            handle_back: Funktio, joka kutsutaan, kun käyttäjä haluaa palata edelliseen näkymään.
            handle_open_budget: Funktio, joka kutsutaan, kun käyttäjä haluaa avata budjetin tarkemmat tiedot.
        """
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
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=10)

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(master=self._frame, text="Etsi tapahtumat tulon tai menon kategorian mukaan").grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        ttk.Label(master=self._frame, text="Kategoria").grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)

        entry = ttk.Entry(master=self._frame, textvariable=self._category)
        entry.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        entry.bind("<Return>", lambda e: self._search())

        ttk.Button(master=self._frame, text="Hae", command=self._search).grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._listbox = Listbox(master=self._frame, height=10)
        self._listbox.grid(row=3, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Avaa budjetti", command=self._open_selected_budget).grid(row=4, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back).grid(row=4, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(master=self._frame, textvariable=self._message).grid(row=6, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

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