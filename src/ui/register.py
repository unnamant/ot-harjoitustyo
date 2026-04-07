from tkinter import ttk, constants, StringVar

class RegisterView:
    def __init__(self, root, user_service, handle_back_to_login):
        self._root = root
        self._user_service = user_service
        self._handle_back_to_login = handle_back_to_login

        self._username = StringVar()
        self._password = StringVar()
        self._message = StringVar()

        self._frame = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        ttk.Label(self._frame, text="Rekisteröityminen").grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        ttk.Label(self._frame, text="Uusi käyttäjätunnus").grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(self._frame, textvariable=self._username).grid(row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Label(self._frame, text="Salasana").grid(row=2, column=0, sticky=constants.W, padx=5, pady=5)
        ttk.Entry(self._frame, textvariable=self._password, show="*").grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        ttk.Button(self._frame, text="Luo tunnus", command=self._register).grid(row=3, column=0, sticky=(constants.E, constants.W), padx=5, pady=5)
        ttk.Button(self._frame, text="Takaisin", command=self._handle_back_to_login).grid(row=3, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._message_label = ttk.Label(self._frame, textvariable=self._message)
        self._message_label.grid(row=4, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5) 

        self._frame.grid_columnconfigure(1, weight=1, minsize=250)

    def _register(self):
        try:
            self._user_service.register(self._username.get(), self._password.get())
            self._message.set("Rekisteröinti onnistui. Voit kirjautua sisään.")
            self._message_label.configure(foreground="green")
        except ValueError as e:
            self._message.set(str(e))
            self._message_label.configure(foreground="red")
