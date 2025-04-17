import sqlite3

from loguru import logger


class Database:
    def __init__(self, db_name: str = "user.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_database()

    def create_database(self):
        with sqlite3.connect('users.db') as db:
            db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
            ''')
            db.commit()

    def add_user(self, user_id, username):
        with sqlite3.connect('users.db') as db:
            db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
            db.commit()
            logger.info('db.add_user()')

    def get_users(self):
        with sqlite3.connect('users.db') as db:
            cursor = db.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return rows

    def print_users(self):
        with sqlite3.connect('users.db') as db:
            cursor = db.execute("SELECT * FROM users")
            rows = cursor.fetchall()

            if not rows:
                print("Нет пользователей в базе данных.")
            else:
                print("Список пользователей:")
                for user in rows:
                    print(f"User ID: {user[0]}, Username: {user[1]}")
