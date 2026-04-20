import unittest
from src.entities.user import User

from src.services.user_service import (
    UserService,
    InvalidCredentialsError,
    UsernameExistsError
)

class FakeUserRepository:
    def __init__(self):
        self.users = []

    def create(self, user: User):
        self.users.append(user)
        return user
    
    def find_by_username(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def find_all(self):
        return self.users
    

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService(FakeUserRepository())

        self.username = "unnis"
        self.password = "salainen123!"

    def test_register(self):
        self.user = self.user_service.register(self.username, self.password)

        user = self.user_service._user_repository.find_by_username(self.username)
        self.assertEqual(user.username, self.username)

    def test_registration_with_invalid_username_and_password(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service.register("um", "virheellinen")
        )

    def test_login_with_valid_username_and_password(self):
        self.user = self.user_service.register(self.username, self.password)
        self.user_service.login(self.username, self.password)

        users = self.user_service._user_repository.find_all()
        self.assertEqual(len(users), 1)

    def test_login_with_invalid_username(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service.login(None, "")
        )

    def test_password_validation(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.user_service._validate_password("invalid")
        )

    def test_current_user_and_logout(self):
        self.user = self.user_service.register(self.username, self.password)
        self.user_service.login(self.username, self.password)

        self.assertEqual(self.user_service.current_user().username, self.username)

        self.user_service.logout()
        self.assertEqual(self.user_service.current_user(), None)
