import hashlib
import re
from src.entities.user import User
from src.repositories.user_repository import UserRepository

class InvalidCredentialsError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass

class UserService:
    """Käyttäjään liittyvistä toiminnoista vastaava luokka."""
    def __init__(self, user_repository = UserRepository):
        self._user_repository = user_repository
        self._current_user: User

    def current_user(self):
        return self._current_user

    def logout(self):
        self._current_user = None

    def register(self, username: str, password: str):
        if len(username) <= 3:
            raise InvalidCredentialsError("Käyttäjätunnuksen tulee olla yli 3 merkkiä pitkä")

        if self._user_repository.find_by_username(username):
            raise UsernameAlreadyExistsError("Käyttäjätunnus on jo käytössä")

        self._validate_password(password)

        user = User(username, self._hash_password(password))
        self._user_repository.create(user)
        return user

    def login(self, username: str, password: str):
        user = self._user_repository.find_by_username(username)
        if not user:
            raise InvalidCredentialsError("Käyttäjätunnus on väärä tai sitä ei ole")
        if user.password != self._hash_password(password):
            raise InvalidCredentialsError("Väärä salasana")

        self._current_user = user
        return user

    def _validate_password(self, password: str):
        if len(password) <= 8:
            raise InvalidCredentialsError("Salasanan tulee olla yli 8 merkkiä pitkä")

        if not re.search(r"\d", password):
            raise InvalidCredentialsError("Salasanan täytyy sisältää ainakin yksi numero")

        if not re.search(r"[^a-zA-Z0-9]", password):
            raise InvalidCredentialsError("Salasanan täytyy sisältää ainakin yksi erikoismerkki.")

    def _hash_password(self, password: str):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

user_service = UserService()
