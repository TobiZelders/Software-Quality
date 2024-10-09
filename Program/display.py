from db import get_role, add_user, authenticate
from security.log import log_activity
from menus.member import member_menu


def main_menu():
    add_user("super_admin","Admin_123", "super-admin", "Tobias", "Zelders")
    add_user("1", "1", "super-admin", "T", "Z")
    add_user("2", "2", "system-admin", "T", "Z")
    add_user("3", "3", "consultant", "T", "Z")

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
    if authenticate(username, password):
        print(f"Welcome {username}!")
        log_activity(username, "Logged in", False)
        role = get_role(username)
        if role == "consultant":
            consultant_menu(username, role)
        elif role == "system-admin":
            system_administrator(username, role)
        elif role == "super-admin":
            super_administrator(username, role)
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