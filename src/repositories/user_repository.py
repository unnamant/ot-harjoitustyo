from src.entities.user import User

class UserRepository:
    def __init__(self):
        self._users = {}

    def find_all(self):
        return self._users
    
    def find_by_username(self, username: str):
        return self._users.get(username)

    def create(self, user: User):
        self._users[user.username] = user
        return user
    
