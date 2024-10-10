import sqlite3
import hashlib
import os
from security.encryption import encrypt, decrypt, deterministic_encryption

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
                        member_id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gender TEXT NOT NULL,
                        weight REAL NOT NULL,
                        address TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        registration_date TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        username TEXT NOT NULL,
                        activity TEXT NOT NULL,
                        suspicious INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

def add_user(username, password, role, first_name, last_name):
    e_username = hash_data(username)
    password_hash = hash_data(password)
    e_role = hash_data(role)
    e_first_name = encrypt(first_name)
    e_last_name = encrypt(last_name)

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, DATE())',
                   (e_username, password_hash, e_role, e_first_name, e_last_name))
    conn.commit()
    conn.close()

def get_role(username, role):
    found_user_role = ""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()
    for i in data:
        if verify_data(i[1], username):
            found_user_role = i[3]
            break
    return verify_data(found_user_role, role)

def search_member(query):
    # Connect to SQLite database
    conn = create_connection()
    cursor = conn.cursor()

    # Prepare the search query to search all fields
    search_query = f"%{query}%"

    # Query the database
    cursor.execute('''
       SELECT * FROM members
       WHERE member_id LIKE ? OR
             first_name LIKE ? OR
             last_name LIKE ? OR
             address LIKE ? OR
             email LIKE ? OR
             phone LIKE ?
       ''', (search_query, search_query, search_query, search_query, search_query, search_query))

    # Fetch all matching rows
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    return results

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

def delete_table_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

    display_all_info()

def hash_data(data):
    """
    This function will return a hash of the provided password

    When storing the hashed password we should also store salt to be able to verify later
    advised format = salt:hashed_password

    :param data: provided data by user (recommended to first use regex)
    :return: hashed data
    """

    byte_data = data.encode()
    salt = os.urandom(16)
    iterations = 500_000
    hash_name = 'sha256'
    derived_key_length = None

    result = hashlib.pbkdf2_hmac(hash_name, byte_data, salt, iterations, derived_key_length)

    return f"{salt.hex()}:{result.hex()}"
    #return hashlib.sha256(password.encode()).hexdigest()

def verify_data(stored_data, input_data):
    """
    Verifies data provided by user with stored data in database

    :param stored_data: hashed password stored in database
    :param input_data: un-hashed password provided by user
    :return: Boolean based on if the provided hashed data matches hashed data saved in database
    """

    salt = stored_data.split(':')[0]
    hashed_data = stored_data.split(':')[1]

    salt = bytes.fromhex(salt)
    hashed_data = bytes.fromhex(hashed_data)

    input_data = input_data.encode()
    hash_name = 'sha256'
    iterations = 500_000
    derived_key_length = None

    new_hashed_data = hashlib.pbkdf2_hmac(hash_name, input_data, salt, iterations, derived_key_length)

    return new_hashed_data == hashed_data

def reverse_data(stored_data, input_data):
    salt = stored_data.split(':')[0]
    salt = bytes.fromhex(salt)

    input_data = input_data.encode()
    hash_name = 'sha256'
    iterations = 500_000
    derived_key_length = None

    new_hashed_data = hashlib.pbkdf2_hmac(hash_name, input_data, salt, iterations, derived_key_length)

    return new_hashed_data

def authenticate(username, password):
    found_user_password = ""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()
    for i in data:
        if verify_data(i[1], username):
            found_user_password = i[2]
            break
    return verify_data(found_user_password, password)

'''
def authenticate(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username=?', (hash_data(username),))
    data = cursor.fetchone() # Its not getting data - i think because we are encrypting data and it will encrypt differently again, you can test
    conn.close()
    return verify_data(data[0], password)
'''

def quick_auth(user_role, role):
    return False if user_role != role else True