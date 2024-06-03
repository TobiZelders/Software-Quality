import random
import datetime
from Program.db import create_connection
from Program.security.authentication import hash_password

def add_user(username, password, role, first_name, last_name):
    conn = create_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute('INSERT OR IGNORE INTO menus (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, DATE())',
                   (username, password_hash, role, first_name, last_name))
    conn.commit()
    conn.close()

def get_role(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM menus WHERE username=?', (username,))
    data = cursor.fetchone()[0]
    print(data)
    conn.close()
    return data

def is_integer(value):
    return isinstance(value, int)

def generate_membership_id():
    current_year = datetime.datetime.now().year
    short_year = current_year % 100
    middle_digits = [random.randint(0, 9) for _ in range(7)]
    partial_id = [int(digit) for digit in str(short_year)] + middle_digits
    checksum = sum(partial_id) % 10
    membership_id_list = partial_id + [checksum]
    membership_id_str = ''.join(map(str, membership_id_list))
    membership_id = int(membership_id_str)
    return membership_id

def check_membership_id(membership_id):
    membership_id_str = str(membership_id)

    # Length check
    if len(membership_id_str) != 10:
        return False

    # Year check
    registration_year_short = int(membership_id_str[:2])
    current_year = datetime.datetime.now().year
    current_year_short = current_year % 100
    if registration_year_short > current_year_short:
        return False

    # Checksum check
    first_nine_digits = [int(digit) for digit in membership_id_str[:9]]
    checksum_digit = int(membership_id_str[9])

    expected_checksum = sum(first_nine_digits) % 10

    if checksum_digit != expected_checksum:
        return False

    return True
