from db import add_user, from_table_where_column_get_variable
from security.log import log_activity
from menus.member import member_menu


def main_menu():
    add_user("super_admin","Admin_123", "super-admin", "Tobias", "Zelders")
    add_user("1", "1", "super-admin", "T", "Z")
    add_user("2", "2", "system-admin", "T", "Z")
    add_user("3", "3", "consultant", "T", "Z")
    failed_login_attempts = 0
    max_failed_login_attempts = 3

    while True:
        print("""
+█-█-█-█-█-█-█-█-█-█-█-█-█-█+
|         MAIN MENU         |
+█-█-█-█-█-█-█-█-█-█-█-█-█-█+
| [1] Login                 |
| [0] Exit                  |
+█-█-█-█-█-█-█-█-█-█-█-█-█-█+
""")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            login()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if from_table_where_column_get_variable('users', 'username', 'password_hash', username, password): # authentication
        print(f"Welcome {username}!")
        log_activity(username, "Logged in", False)

        if from_table_where_column_get_variable('users', 'username', 'role', username, 'consultant'):
            print("CONSULTANT CHECK")

        elif from_table_where_column_get_variable('users', 'username', 'role', username, 'system-admin'):
            print("SYSTEM ADMIN CHECK")

        elif from_table_where_column_get_variable('users', 'username', 'role', username, 'super-admin'):
            super_administrator(username, "super-admin")
    else:
        print("Invalid credentials.")
        log_activity(username, "Unsuccessful login", True)

def consultant_menu(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1] Update your password          █  
█ [2] Member menu                   █
█ [0] exit                          █
█████████████████████████████████████
        """)

        choice = input("Enter choice: ").strip()
        if choice == '1':
            break
        elif choice == '2':
            member_menu(username, role)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def system_administrator(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1] Update your password          █  
█ [2] User list                     █
█ [3] Consultant menu               █
█ [4] Member menu                   █
█ [5] Make backup                   █
█ [6] Restore backup                █   
█ [7] See logs                      █  
█ [0] Exit                          █
█████████████████████████████████████
            """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            break
        elif choice == '2':
            break
        elif choice == '3':
            break
        elif choice == '4':
            member_menu(username, role)
        elif choice == '5':
            break
        elif choice == '6':
            break
        elif choice == '7':
            break
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def super_administrator(username, role):

    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1] User list                     █
█ [2] Consultant menu               █
█ [3] Admin menu                    █
█ [4] Member menu                   █
█ [5] Make backup                   █
█ [6] Restore backup                █   
█ [7] See logs                      █  
█ [0] Exit                          █
█████████████████████████████████████
        """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            login()
        elif choice == '2':
            break
        elif choice == '3':
            break
        elif choice == '4':
            member_menu(username, role)
        elif choice == '5':
            break
        elif choice == '6':
            break
        elif choice == '7':
            break
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")