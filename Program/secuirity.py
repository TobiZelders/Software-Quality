import random
import datetime
import hashlib
import os
import re
import cryptography
from db import create_connection

def username_regex(username):
    """
    Explanation
    Username Regex:

    ^: Start of the string.
    [a-zA-Z_]: The first character must be a letter (case-insensitive) or an underscore.
    [a-zA-Z0-9_\'\.]{7,9}$: The next 7 to 9 characters can be letters, numbers, underscores, apostrophes, or periods.
    re.IGNORECASE: Makes the regex case-insensitive.

    :param username: username to be checked
    :return: True or false based on if username matches regular expression or not
    """
    username_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_\'\.]{7,9}$', re.IGNORECASE)
    if username_regex.match(username):
        return True
    else:
        return False

correct_usernames = ["user_one", "_user1234", "john.doe1", "user.123"]
incorrect_usernames = ["user1", "12345678", "longusername", ".user123"]

'''
for username in correct_usernames:
    if username_regex(username):
        print(f"'{username}' is a valid username")
    else:
        print(f"'{username}' is an invalid username")

for username in incorrect_usernames:
    if username_regex(username):
        print(f"'{username}' is a valid username")
    else:
        print(f"'{username}' is an invalid username")
'''


def password_regex(password):
    """
    Explanation
    Password Regex:

    ^: Start of the string.
    (?=.*[a-z]): To ensure at least one lowercase letter.
    (?=.*[A-Z]): To ensure at least one uppercase letter.
    (?=.*\d): To ensure at least one digit.
    (?=.*[~!@#$%&_\-+=|(){}[]:;'<>,.?/])`: To ensure at least one special character.
    .{12,30}$: Ensures the length of the password is between 12 and 30 characters.

    :param password: password to be checked
    :return: True or false based on if password matches regular expression or not
    """
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/]).{12,30}$')
    if password_regex.match(password):
        return True
    else:
        return False

correct_passwords = ["StrongPass1!@#", "Abcdefghijkl1!", "12345aBcDeFg!@", "ValidPassw0rd!"]
incorrect_passwords = ["short1A!", "alllowercaseandlongenough", "ALLUPPERCASEANDLONGENOUGH1!", "MissingDigitAndSpecialChar", "NoSpecialChar1234"]

'''
for password in correct_passwords:
    if password_regex(password):
        print(f"'{password}' is a valid password")
    else:
        print(f"'{password}' is an invalid password")

for password in incorrect_passwords:
    if password_regex(password):
        print(f"'{password}' is a valid password")
    else:
        print(f"'{password}' is an invalid password")

'''

def hash_password(password):
    """
    This function will return a hash of the provided password

    When storing the hashed password we should also store salt to be able to verify later
    advised format = salt:hashed_password

    :param password: provided password by user (recommended to first use password_regex)
    :return: hashed password
    """

    byte_password = password.encode()
    salt = os.urandom(16)
    iterations = 500_000
    hash_name = 'sha256'
    derived_key_length = None

    result = hashlib.pbkdf2_hmac(hash_name, byte_password, salt, iterations, derived_key_length)

    return f"{salt.hex()}:{result.hex()}"
    #return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, input_password):
    """
    Verifies password provided by user with stored password in database

    :param stored_password: hashed password stored in database
    :param input_password: un-hashed password provided by user
    :return: Boolean based on if the provided hashed password matches hashed password saved in database
    """

    salt = stored_password.split(':')[0]
    hashed_password = stored_password.split(':')[1]

    salt = bytes.fromhex(salt)
    hashed_password = bytes.fromhex(hashed_password)

    input_password = input_password.encode()
    hash_name = 'sha256'
    iterations = 500_000
    derived_key_length = None

    new_hashed_password = hashlib.pbkdf2_hmac(hash_name, input_password, salt, iterations, derived_key_length)

    return new_hashed_password == hashed_password

def add_user(username, password, role, first_name, last_name):
    conn = create_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, DATE())',
                   (username, password_hash, role, first_name, last_name))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username=?', (username,))
    data = cursor.fetchone()
    conn.close()
    print('-------------')
    return verify_password(data[0], password)

def get_role(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE username=?', (username,))
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
