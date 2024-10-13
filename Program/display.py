import backup
from db import add_user, check_data_from_column
from security.log import log_activity, check_unseen_sus_logs, see_logs, get_logs, set_seen_all_logs
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
    if check_data_from_column('users', 'username', 'password_hash', username, password): # authentication
        print(f"Welcome {username}!")
        log_activity(username, "Logged in", False)

        if check_data_from_column('users', 'username', 'role', username, 'consultant'):
            consultant_menu(username, "consultant")

        elif check_data_from_column('users', 'username', 'role', username, 'system-admin'):
            system_administrator_menu(username, "system-admin")

        elif check_data_from_column('users', 'username', 'role', username, 'super-admin'):
            super_administrator_menu(username, "super-admin")
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

def system_administrator_menu(username, role):
    sus_logs = check_unseen_sus_logs()
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
{"█ [S] SUSPICIOUS ACTIVITY ALERT     █" if len(sus_logs) > 0 else "█                                   █"}
█ [1] Update your password          █  
█ [2] User list                     █
█ [3] Consultant menu               █
█ [4] Member menu                   █
█ [5] Backup menu
█ [6] See logs                      █  
█ [0] Exit                          █
█████████████████████████████████████
            """)
        choice = input("Enter choice: ").strip()
        if choice == 'S' or choice == 's':
            if len(sus_logs) > 0:
                sus_logs_decrypted = see_logs(sus_logs)
                display_data(username, role, sus_logs_decrypted, "SUSPICIOUS LOGS")
                set_seen_all_logs()
            else:
                print("Invalid choice. Please try again.")
        if choice == '1':
            break
        elif choice == '2':
            break
        elif choice == '3':
            break
        elif choice == '4':
            member_menu(username, role)
        elif choice == '5':
            r = backup_menu(username, role)
            if r == "restored":
                break
        elif choice == '6':
            see_logs(get_logs())
            set_seen_all_logs()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def super_administrator_menu(username, role):
    sus_logs = check_unseen_sus_logs()
    print(f"sus_logs length: {len(sus_logs)}")
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
{"█ [S] SUSPICIOUS ACTIVITY ALERT     █" if len(sus_logs) > 0 else "█                                   █"}
█ [1] User list                     █
█ [2] Consultant menu               █
█ [3] Admin menu                    █
█ [4] Member menu                   █
█ [5] Backup menu                   █
█ [6] See logs                      █  
█ [0] Exit                          █
█████████████████████████████████████
        """)
        choice = input("Enter choice: ").strip()
        if choice == 'S' or choice == 's':
            if len(sus_logs) > 0:
                sus_logs_decrypted = see_logs(sus_logs)
                display_data(username, role, sus_logs_decrypted, "SUSPICIOUS LOGS")
                set_seen_all_logs()
            else:
                print("Invalid choice. Please try again.")

        elif choice == '1':
            break
        elif choice == '2':
            break
        elif choice == '3':
            break
        elif choice == '4':
            member_menu(username, role)
        elif choice == '5':
            r = backup_menu(username, role)
            if r == "restored":
                break
        elif choice == '6':
            display_data(username, role, see_logs(get_logs()), "LOGS")
            set_seen_all_logs()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def backup_menu(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1]  Make backup                  █
█ [2]  Restore backup               █    
█ [0]  Exit                         █
█████████████████████████████████████        
        """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            save_file = backup.backup()
            print(f""" \n
+█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█+
|             BACKUP MADE:     
| {save_file}
+█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█-█+
            """)
        elif choice == '2':
            str_choice = display_select_data(username, role, backup.get_backup_list(), " RESTORE BACKUP \n NOTE: YOU WILL BE LOGGED OUT AFTER RESTORE IS COMPLETE")
            if str_choice != "":
                backup.restore(str_choice)
            return "restored"
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def display_data(username, role, data, menu_name):
    d_data = ""
    count = 1
    for i in data:
        d_data = f"{d_data}█ {count}) {i} \n"
        count = count + 1
    while True:
        print(f"""
*************************************
█ ROLE: {role} 
█ USER: {username}      
*************************************
█ --- {menu_name} ---
*************************************
{d_data}
█████████████████████████████████████
█ [0] Exit                          █
█████████████████████████████████████
        """)
        choice = input("Enter choice: ").strip()
        if choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def string_to_int(string):
    try:
        return int(string)
    except ValueError:
        return "Error: The provided string cannot be converted to an integer."

def display_select_data(username, role, data, menu_name):
    d_data = ""
    count = 1
    if len(data) == 0:
        print("No data found")
        return ""
    for i in data:
        d_data = f"{d_data}█ [{count}] {i} \n"
        count = count + 1
    while True:
        print(f"""
*************************************
█ ROLE: {role} 
█ USER: {username}      
*************************************
█ --- {menu_name} ---
*************************************
{d_data}
█ [0] Exit                          █
█████████████████████████████████████
        """)
        choice = input("Enter choice: ").strip()
        if is_integer(choice) and choice != '0':
            i_choice = string_to_int(choice)
            if 0 < i_choice <= len(data):
                return data[i_choice+1]
            else:
                print("Invalid choice. Please try again.")
        elif choice == '0':
            return ""
        else:
            print("Invalid choice. Please try again.")
