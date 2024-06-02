import sqlite3

def create_connection():
    conn = sqlite3.connect('unique_meal.db')
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        registration_date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gender TEXT NOT NULL,
                        weight REAL NOT NULL,
                        address TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        registration_date TEXT NOT NULL,
                        member_id TEXT UNIQUE NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        username TEXT NOT NULL,
                        activity TEXT NOT NULL,
                        suspicious INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


def display_all_info():
    conn = create_connection()
    cursor = conn.cursor()

    print("\nUsers:")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)

    print("\nMembers:")
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    for member in members:
        print(member)

    print("\nLogs:")
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    for log in logs:
        print(log)

    conn.close()
