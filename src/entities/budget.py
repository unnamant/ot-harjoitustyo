class Entry:
    """
        type: Tulo vai meno
        amount: Tulon/menon määrä
        category: Kategoria, mihin tulo/meno kuuluu
    """

    def __init__(self, entry_id: int, entry_type: str, amount: float, category: str):
        self.id = entry_id
        self.entry_type = entry_type
        self.amount = amount
        self.category = category


class Budget:
    def __init__(self, budget_id: int, name: str, budget_period: str, comment: str = None):
        """
            name: Budjetin nimi
            budget_period: Mille ajalle budjetti on tehty 
            comment: Vapaaehtoinen kommentti budjettiin
        """
        self.id = budget_id
        self.name = name
        self.budget_period = budget_period
        self.comment = comment
        self.entries: list[Entry] = []

    def income_total(self):
        return sum(e.amount for e in self.entries if e.entry_type == "tulo")

    def expense_total(self):
        return sum(e.amount for e in self.entries if e.entry_type == "meno")

    def balance(self):
        return self.income_total() - self.expense_total()
