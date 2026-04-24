from tkinter import ttk, constants, StringVar
from src.ui.widgets import BudgetPicker

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
