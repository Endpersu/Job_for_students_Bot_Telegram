import sqlite3

def create_database():
    with sqlite3.connect('users.db') as db:
        db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
        ''')
        db.commit()

def add_user(user_id, username):
    with sqlite3.connect('users.db') as db:
        db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        db.commit()

def get_users():
    with sqlite3.connect('users.db') as db:
        cursor = db.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    
def print_users():
    with sqlite3.connect('users.db') as db:
        cursor = db.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        
        if not rows:
            print("Нет пользователей в базе данных.")
        else:
            print("Список пользователей:")
            for user in rows:
                print(f"User ID: {user[0]}, Username: {user[1]}")

if __name__ == "__main__":
    print_users()