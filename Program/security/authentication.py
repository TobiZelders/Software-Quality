
import hashlib
import os
from Program.db import create_connection

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

def authenticate(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM menus WHERE username=?', (username,))
    data = cursor.fetchone()
    conn.close()
    return verify_password(data[0], password)

