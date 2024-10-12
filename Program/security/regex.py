import re

def username_regex(username):
    """
    Explanation
    Username Regex:

    ^: Start of the string.
    [a-zA-Z_]: The first character must be a letter (case-insensitive) or an underscore.
    [a-zA-Z0-9_\'\.]{7,9}$: The next 7 to 9 characters can be letters, numbers, underscores, apostrophes, or periods.
    re.IGNORECASE: Makes the regex.py case-insensitive.

    :param username: username to be checked
    :return: True or false based on if username matches regular expression or not
    """
    username_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_\'\.]{7,9}$', re.IGNORECASE)
    if username_regex.match(username):
        return True
    else:
        return False

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

def name_regex(name):
    name_regex = re.compile(r'^[A-Z][a-zA-Z\'\-]+ [A-Z][a-zA-Z\'\-]+$')
    if name_regex.match(name):
        return True
    else:
        return False

def age_regex(age):
    age_regex = re.compile(r'^(?:1[01][0-9]|120|[1-9]?[0-9])$')
    if age_regex.match(age):
        return True
    else:
        return False

def weight_regex(weight):
    weight_regex = re.compile(r'^(?:[1-9][0-9]{0,2}(?:\.[0-9])?|0\.[1-9])$')
    if weight_regex.match(weight):
        return True
    else:
        return False

def email_regex(email):
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if email_regex.match(email):
        return True
    else:
        return False

def phone_regex(phone):
    phone_regex = re.compile(r'^\+31-6-\d{8}$')
    if phone_regex.match(phone):
        return True
    else:
        return False

def address_regex(address, city_list):
    address_regex = re.compile(r'^[A-Z][a-zA-Z ]*, \d+, \d{4}[A-Z]{2}, ([A-Za-z]+)$')
    if address_regex.match(address):
        return True
    else:
        return False


def regex_tester(list, regex):
    for item in list:
        if regex(item):
            print(f"{item} is valid with regex.py : {regex}")
        else:
            print(f"{item} is invalid with regex.py : {regex}")

correct_usernames = ["user_one", "_user1234", "john.doe1", "user.123"]
incorrect_usernames = ["user1", "12345678", "longusername", ".user123"]
correct_passwords = ["StrongPass1!@#", "Abcdefghijkl1!", "12345aBcDeFg!@", "ValidPassw0rd!"]
incorrect_passwords = ["short1A!", "alllowercaseandlongenough", "ALLUPPERCASEANDLONGENOUGH1!", "MissingDigitAndSpecialChar", "NoSpecialChar1234"]

#regex_tester(correct_usernames, username_regex)
#regex_tester(incorrect_usernames, username_regex)
#regex_tester(correct_passwords, password_regex)
#regex_tester(incorrect_passwords, password_regex)