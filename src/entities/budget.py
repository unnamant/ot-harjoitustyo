class Entry:
    """
        type: Tulo vai meno
        amount: Tulon/menon määrä
        category: Kategoria, mihin tulo/meno kuuluu
    """

    def __init__(self, type: str, amount: float, category: str):
        self.type = type
        self.amount = amount
        self.category = category


class Budget:
    def __init__(self, name: str, budget_period: str, comment: str = None):
        """
            name: Budjetin nimi
            budget_period: Mille ajalle budjetti on tehty 
            comment: Vapaaehtoinen kommentti budjettiin
        """
        self.name = name
        self.budget_period = budget_period
        self.comment = comment
        self.entries: list[Entry] = []

    def income_total(self):
        return sum(b.amount for b in self.entries if b.type == "tulo")

    def expense_total(self):
        return sum(b.amount for b in self.entries if b.type == "meno")

    def balance(self):
        return self.income_total() - self.expense_total()
