import sqlite3
from abc import ABC

from Domain.users.persistance_interface import UserPersistenceInterface
from Domain.users.user import User
from Domain.users.factory import UserFactory


class UserPersistenceSqlite(UserPersistenceInterface, ABC):
    def get_all(self) -> list[User]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users_info = cursor.fetchall()
        factory = UserFactory()
        users = [factory.make_from_persistence(x) for x in users_info]
        return users

    def add(self, user: User):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}','{user.username}')")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)")
                else:
                    raise e
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}','{user.username}')")
            conn.commit()
