import sqlite3
import hashlib
import os

from security.encryption import encrypt, decrypt
from security.general_security import generate_membership_id

def create_connection():
    conn = sqlite3.connect('unique_meal.db')
    return conn

def is_valid_table_name(table):
    return table.isidentifier()

def quick_auth(user_role, role):
    return False if user_role != role else True

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username_hash TEXT UNIQUE NOT NULL,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL,
                        role_hash TEXT NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        registration_date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        weight TEXT NOT NULL,
                        address TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        registration_date TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        seen INTEGER NOT NULL,
                        username TEXT NOT NULL,
                        activity TEXT NOT NULL,
                        suspicious INTEGER NOT NULL)''')
    conn.commit()
    conn.close()
    add_user("super_admin", "Admin_123", "super-admin", "Tobias", "Zelders")
    add_user("1", "1", "super-admin", "T", "Z")
    add_user("2", "2", "system-admin", "T", "Z")
    add_user("3", "3", "consultant", "T", "Z")

def add_user(username, password, role, first_name, last_name):
    h_username = hash_data(username)
    e_username = encrypt(username)
    password_hash = hash_data(password)
    h_role = hash_data(role)
    e_role = encrypt(role)
    e_first_name = encrypt(first_name)
    e_last_name = encrypt(last_name)

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (username_hash, username, password_hash, role_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, DATE())',
                   (h_username, e_username, password_hash, h_role, e_role, e_first_name, e_last_name))
    conn.commit()
    conn.close()

def add_member(first_name, last_name, age, gender, weight, address, email, phone):
    member_id = generate_membership_id()
    e_first_name = encrypt(first_name)
    e_last_name = encrypt(last_name)
    e_address = encrypt(address)
    e_email = encrypt(email)
    e_phone = encrypt(phone)

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO members (id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, DATE())',
                   (member_id, e_first_name, e_last_name, age, gender, weight, e_address, e_email, e_phone))
    conn.commit()
    conn.close()


def delete_member(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members WHERE id = ?', (member_id,))
    conn.commit()
    conn.close()

    print(f'Member with ID {member_id} has been deleted.')

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

def delete_table_log():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()

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

def update_password(username, new_password):
    new_password_hash = hash_data(new_password)
    conn = sqlite3.connect('your_database.db')  # replace 'your_database.db' with your actual database name
    cursor = conn.cursor()

    # Update the password for the given username
    cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', (new_password_hash, hash_data(username)))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f'Password for user "{username}" has been updated.')

def verify_data(stored_data, input_data):
    """
    Verifies data provided by user with stored data in database

    :param stored_data: hashed password stored in database
    :param input_data: un-hashed password provided by user
    :return: Boolean based on if the provided hashed data matches hashed data saved in database
    """
    try:
        salt = stored_data.split(':')[0]
        hashed_data = stored_data.split(':')[1]
    except:
        print("no match")
        return False

    salt = bytes.fromhex(salt)
    hashed_data = bytes.fromhex(hashed_data)

    input_data = input_data.encode()
    hash_name = 'sha256'
    iterations = 500_000
    derived_key_length = None

    new_hashed_data = hashlib.pbkdf2_hmac(hash_name, input_data, salt, iterations, derived_key_length)

    return new_hashed_data == hashed_data

def get_data_from_table(table):
    if is_valid_table_name(table):
        query = f'SELECT * FROM {table}'
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    else:
        #log suspicious @
        print("Invalid table : " + table)

def get_columns(table):
    """
    This function will return the column names within a table

    :param table: the table from where you want the column names from
    :return: column names found within a table
    """
    if is_valid_table_name(table):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(f'PRAGMA table_info({table})')
        data = cursor.fetchall()
        conn.close()
        column_names = [row[1] for row in data]
        return column_names
    else:
        #log suspicious @
        print("Invalid table : " + table)

def get_column_data(table, column):
    if is_valid_table_name(table):
        query = f'SELECT id, {column} FROM {table}'
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    else:
        #log suspicious @
        print("Invalid table : " + table)

def authenticate(username, password):
    e_u = encrypt(username)
    print(e_u)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username=?', (e_u,))
    data = cursor.fetchone()
    conn.close()
    return verify_data(data[0], password)

def check_data_from_column(table, where_column, get_column, input_w_column, input_g_column):
    """
    This function will first search within the specified table for the where column. The where column can be username (so where username is...)
    Than you can search based on username and you to test that user on specific data. The get column is that varialbe (so where username is . get role)
    Than we can check with user input if this is actually true or not.

    :param table: to specify in what table you would like to search
    :param where_column: to specify in what column you would like to search within the table
    :param get_column: to specify what variable you would like to retrieve from the table
    :param input_g_column: user input for where column
    :param input_w_column: user input for get column
    :return: Boolean if the values are found within the database.
    """
    table_data = get_data_from_table(table) # error here
    columns = get_columns(table)
    found_get_variable = ""
    c_index = 0
    v_index = 0

    for c1 in columns:
        if c1 == where_column:
            break
        c_index = c_index + 1

    for c2 in columns:
        if c2 == get_column:
            break
        v_index = v_index + 1

    for i in table_data:
        if verify_data(i[c_index], input_w_column):
            found_get_variable = i[v_index]
            break
    return verify_data(found_get_variable, input_g_column)

def get_exact_data_from_column(table, where_column, get_column, input_w_column, input_g_column):
    """
    This function will first search within the specified table for the where column. The where column can be username (so where username is...)
    Than you can search based on username and you to test that user on specific data. The get column is that varialbe (so where username is . get role)
    Than we can check with user input if this is actually true or not.

    :param table: to specify in what table you would like to search
    :param where_column: to specify in what column you would like to search within the table
    :param get_column: to specify what variable you would like to retrieve from the table
    :param input_g_column: user input for where column
    :param input_w_column: user input for get column
    :return: Boolean if the values are found within the database.
    """
    table_data = get_data_from_table(table) # error here
    columns = get_columns(table)
    found_get_variable = ""
    c_index = 0
    v_index = 0

    found_data = []

    for c1 in columns:
        if c1 == where_column:
            break
        c_index = c_index + 1

    for c2 in columns:
        if c2 == get_column:
            break
        v_index = v_index + 1

    for i in table_data:
        if verify_data(i[c_index], input_w_column):
            if verify_data(i[v_index], input_g_column):
                found_data.append(i)

    return found_data

def get_logs():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_members():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    users = cursor.fetchall()
    conn.close()
    return users