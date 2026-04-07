# Githubin Copilotilla generoitua koodia oman tekstikäyttöliittymä koodin pohjalta

from tkinter import ttk, constants, StringVar, Listbox, END

class PeriodPicker:
    """Graafinen korvike ask_period_key():lle.
    - Päivä: syötetään Entryyn
    - Kuukausi: valitaan Combobox-listasta (kirjoitettu muoto)
    - Vuosi: syötetään Entryyn
    """

    def __init__(self, master):
        self._type_var = StringVar(value="Kuukausi")
        self._value_var = StringVar()
        self._month_var = StringVar(value="tammikuu")

        self._frame = ttk.Frame(master=master)

        ttk.Label(self._frame, text="Ajanjakso").grid(
            row=0, column=0, sticky=constants.W, padx=5, pady=5
        )

        self._type = ttk.Combobox(
            self._frame,
            textvariable=self._type_var,
            values=["Päivä", "Kuukausi", "Vuosi"],
            state="readonly",
            width=12,
        )
        self._type.grid(row=0, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        self._type.bind("<<ComboboxSelected>>", self._update_inputs)

        self._value_label = ttk.Label(self._frame, text="")
        self._value_label.grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)

        # Entry (päivä/vuosi)
        self._value_entry = ttk.Entry(self._frame, textvariable=self._value_var)
        self._value_entry.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        # Combobox (kuukausi)
        self._month_combo = ttk.Combobox(
            self._frame,
            textvariable=self._month_var,
            values=[
                "tammikuu", "helmikuu", "maaliskuu", "huhtikuu",
                "toukokuu", "kesäkuu", "heinäkuu", "elokuu",
                "syyskuu", "lokakuu", "marraskuu", "joulukuu",
            ],
            state="readonly",
        )
        self._month_combo.grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._frame.grid_columnconfigure(1, weight=1, minsize=220)

        self._update_inputs()

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)

    def _update_inputs(self, _event=None):
        t = self._type_var.get()

        if t == "Kuukausi":
            self._value_label.configure(text="Valitse kuukausi")
            self._value_entry.grid_remove()
            self._month_combo.grid()
        elif t == "Päivä":
            self._value_label.configure(text="Anna päivä")
            self._month_combo.grid_remove()
            self._value_entry.grid()
        else:
            self._value_label.configure(text="Anna vuosi")
            self._month_combo.grid_remove()
            self._value_entry.grid()
    def get_period_key(self) -> str | None:
        t = self._type_var.get()

        if t == "Kuukausi":
            month = self._month_var.get().strip()
            return month or None

        value = self._value_var.get().strip()
        return value or None

class BudgetPicker:
    """GUI-vastine show_budgets_and_choose_index()-funktiolle."""
    def __init__(self, master, app):
        self._app = app
        self._frame = ttk.Frame(master=master)

        ttk.Label(self._frame, text="Valitse budjetti").grid(row=0, column=0, sticky=constants.W, padx=5, pady=5)

        self._listbox = Listbox(self._frame, height=7)
        self._listbox.grid(row=1, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=1, minsize=380)

        self.refresh()

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)

    def refresh(self):
        self._listbox.delete(0, END)
        budgets = self._app.list_budgets()
        for b in budgets:
            self._listbox.insert(END, b.name)

    def get_selected_index(self) -> int | None:
        selection = self._listbox.curselection()
        if not selection:
            return None
        return int(selection[0])