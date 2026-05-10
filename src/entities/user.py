class User:
    def __init__(self, username: str, password: str):
        """
        username: Käyttäjätunnus, joka toimii käyttäjään liittyvänä identifikaattorina
        password: Käyttäjään liittyvä salasana, joka tarvitaan kirjautumiseen
        """
        self.username = username
        self.password = password
