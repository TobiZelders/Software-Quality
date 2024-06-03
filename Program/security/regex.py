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