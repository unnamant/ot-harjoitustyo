from tkinter import ttk, constants

from src.services.user_service import UserService
from src.services.budget_service import BudgetService

from src.ui.login import LoginView
from src.ui.register import RegisterView
from src.ui.edit import EditBudgetView
from src.ui.add_budget import AddBudgetView
from src.ui.delete import DeleteBudgetView
from src.ui.list_budgets import ListBudgetsView, BudgetDetailsView
from src.ui.add_entry import AddEntryView
from src.ui.balance import BalanceView
from src.ui.search_by_category import SearchByCategoryView

# Github Copilotilla generoitua koodia, jota on kuitenkin muokattu toimivaksi ja paremmaksi.
# Koodi generoitu alkuperäisen tekstikäyttöliittymä-koodin pohjalta.

class UI:
    """Pääkäyttöliittymäluokka, joka vastaa sovelluksen eri näkymien hallinnasta ja vuorovaikutuksesta käyttäjän kanssa."""

    def __init__(self, root, user_service: UserService, budget_service: BudgetService):
        """Luokan konstruktori, joka alustaa sovelluksen tietokantayhteyden, palvelut ja näkymät.
        
        Args:
            root: Tkinterin juurikomponentti, johon näkymät asetetaan.
            user_service: Käyttäjään liittyviä toimintoja tarjoava palvelu.
            budget_service: Budjettiin liittyviä toimintoja tarjoava palvelu.
        """

        self._root = root
        self._current_view = None
        self._user_service = user_service
        self._app = budget_service

    def start(self):
        """Käynnistää sovelluksen näyttämällä kirjautumisnäkymän."""
        self._show_login()

    def _show_login(self):
        """Näyttää kirjautumisnäkymän."""
        self._hide_current_view()
        self._current_view = LoginView(self._root, self._user_service, self._show_menu, self._show_register)
        self._current_view.pack()

    def _handle_logout(self):
        """Käsittelee uloskirjautumisen ja näyttää kirjautumisnäkymän."""
        self._user_service.logout()
        self._show_login()

    def _show_register(self):
        """Näyttää rekisteröitymisnäkymän."""
        self._hide_current_view()
        self._current_view = RegisterView(self._root, self._user_service, self._show_login)
        self._current_view.pack()

    def _hide_current_view(self):
        """Tuhoaa nykyisen näkymän, jos sellainen on olemassa."""
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_menu(self):
        """Näyttää päävalikon näkymän."""
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
        """Näyttää budjetin lisäämisen näkymän."""
        self._hide_current_view()
        self._current_view = AddBudgetView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_add_entry(self):
        """Näyttää tulon tai menon lisäämisen näkymän."""
        self._hide_current_view()
        self._current_view = AddEntryView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_list_budgets(self):
        """Näyttää budjettien listauksen näkymän."""
        self._hide_current_view()
        self._current_view = ListBudgetsView(self._root, self._app, self._show_menu, self._show_budget)
        self._current_view.pack()

    def _show_delete_budget(self, index):
        """Käsittelee budjetin poistamisen indeksin perusteella ja näyttää päävalikon."""
        self._app.delete_budget(index)
        self._show_list_budgets()

    def _show_budget(self, budget_index):
        """Näyttää budjetin yksityiskohtien näkymän indeksin perusteella."""
        self._hide_current_view()
        self._current_view = BudgetDetailsView(
            self._root,
            self._app,
            budget_index,
            handle_back = self._show_list_budgets,
            handle_edit = lambda: self._show_edit_budget(budget_index),
            handle_delete_budget = lambda: self._show_delete_budget(budget_index)
        )
        self._current_view.pack()

    def _show_balance(self):
        """Näyttää budjetin saldon näkymän."""
        self._hide_current_view()
        self._current_view = BalanceView(self._root, self._app, self._show_menu)
        self._current_view.pack()

    def _show_search_by_category(self):
        """Näyttää budjettien hakemisen kategorian perusteella näkymän."""
        self._hide_current_view()
        self._current_view = SearchByCategoryView(self._root, self._app, self._show_menu, self._show_budget)
        self._current_view.pack()

    def _show_edit_budget(self, budget_index):
        """Näyttää budjetin muokkaamisen näkymän indeksin perusteella."""
        self._hide_current_view()
        self._current_view = EditBudgetView(self._root, self._app, budget_index, handle_back=lambda: self._show_budget(budget_index))
        self._current_view.pack()

class MenuView:
    """Käyttöliittymäluokka, joka vastaa päävalikon näkymästä ja sen komponenteista."""

    def __init__(self, root, handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance, handle_logout, handle_search_by_category):
        """Luokan konstruktori, joka alustaa näkymän ja sen komponentit."""
        self._root = root
        self._frame = None
        self._initialize(handle_add_budget, handle_add_entry, handle_list_budgets, handle_delete_budget, handle_show_balance, handle_logout, handle_search_by_category)

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
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
        ttk.Button(master=self._frame, text="Kirjaudu ulos", command=handle_logout).grid(
            row=5, column=0, sticky=(constants.E, constants.W), padx=5, pady=5
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)
