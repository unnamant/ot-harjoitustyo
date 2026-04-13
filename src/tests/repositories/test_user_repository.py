import unittest
from src.repositories.user_repository import user_repository
from src.entities.user import User

from src.initialize_database import drop_tables, create_tables
from src.database_connection import get_database_connection

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.connection = get_database_connection()
        drop_tables(self.connection)
        create_tables(self.connection)

    def test_create(self):
        user_repository.create(User("testuser", "testpassword"))

        users = user_repository.find_all()
        
        self.assertEqual(len(users), 1)
    
    def test_find_by_username(self):
        user_repository.create(User("testuser", "testpassword"))

        user = user_repository.find_by_username(User("testuser", "testpassword").username)
        
        self.assertEqual(user.username, User("testuser", "testpassword").username)

    def test_find_all(self):
        user_repository.create(User("testuser", "testpassword"))
        user_repository.create(User("testuser2", "testpassword2"))
        users = user_repository.find_all()

        self.assertEqual(len(users), 2)
