import backup
import db
import member
from db import check_data_from_column, get_columns
from security.log import log_activity, check_unseen_sus_logs, see_logs, get_logs, set_seen_all_logs
from users import get_user_list
from member import search_member
import security.regex
from getpass import getpass




def main_menu():
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
    while True:
        username = input("█████████████████████████████████████\n█ [0] Exit                          █\n█████████████████████████████████████\nUsername:").strip()
        if username == '0':
            break
        elif security.regex.username_regex(username):
            break
        else:
            print("Username needs to have between 8 and 10 characters\nMust start with a letter or underscore \nCan contain : letters, numbers, underscores, apostrophes and periods")
    while True:
        password = input("█████████████████████████████████████\n█ [0] Exit                          █\n█████████████████████████████████████\nPassword:").strip()
        if password == '0':
            break
        elif security.regex.password_regex(password):
            break
        else:
            print("Password needs to be between 12 and 30 characters\n○ must be no longer than 30 characters\n Can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%&_-+=`|\(){}[]:;'<>,.?/\nmust have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character")
    password = input("Password: ").strip()#
    if check_data_from_column('users', 'username_hash', 'password_hash', username, password): # authentication
        print(f"Welcome {username}!")
        log_activity(username, "Logged in", False)

        if check_data_from_column('users', 'username_hash', 'role_hash', username, 'consultant'):
            consultant_menu(username, "consultant")

        elif check_data_from_column('users', 'username_hash', 'role_hash', username, 'system-admin'):
            system_administrator_menu(username, "system-admin")

        elif check_data_from_column('users', 'username_hash', 'role_hash', username, 'super-admin'):
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
            while True:
                new_password = input(
                    "█████████████████████████████████████\n█ [0] Exit                          █\n█████████████████████████████████████\nPlease enter new password:")
                if new_password == '0':
                    break
                elif security.regex.password_regex(new_password):
                    db.update_password()
                else:
                    print("Invalid password please try again")
        elif choice == '2':
            member_menu(username, role)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def system_administrator_menu(username, role):
    while True:
        sus_logs = check_unseen_sus_logs()
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
        if choice == '1':
            while True:
                new_password = input("█████████████████████████████████████\n█ [0] Exit                          █\n█████████████████████████████████████\nPlease enter new password:")
                if new_password == '0':
                    break
                elif security.regex.password_regex(new_password):
                    db.update_password()
                else:
                    print("Invalid password please try again")
        elif choice == '2':
            display_data(username, role, get_user_list(), "USER LIST")
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

def super_administrator_menu(username, role):
    while True:
        sus_logs = check_unseen_sus_logs()
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
            display_data(username, role, get_user_list(), "USER LIST")
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

#-------------------------------------------------------------- MEMBER ------------------------------------------------



def member_menu(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1] See members                   █
█ [2] Add member                    █
█ [3] Modify member                 █
█ [4] Search member                 █
{"█ [5] Delete member                 █" if role == "system-admin" or role == "super-admin" else "█                                   █"}
█ [0] Exit                          █
█████████████████████████████████████
        """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            members = member.see_members(db.get_members())
            display_data(username, role, members, "MEMBERS")
        elif choice == '2':
            add_member_menu(username, role)
        elif choice == '3':
            break
        elif choice == '4':
            category = display_select_data(username, role, get_columns('members'), "SEARCH CATEGORY")
            found_members = search_member_menu(username, role, category)
            display_data(username, role, found_members, "FOUND MEMBERS")
        elif choice == '5' and (role == "system-admin" or role == "super-admin"):
            delete_member_menu(username, role)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def add_member_menu(username, role):
    m_first_name = m_last_name = m_age = m_gender = m_weight = m_address = m_email = m_phone = ""
    street_name = house_number = zip_code = city = ""
    street_name_b = house_number_b = zip_code_b = city_b = False

    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}   
█████████████████████████████████████
█ ADD MEMBER        
█████████████████████████████████████
█ [1] First name    :{m_first_name}                    
█ [2] Last name     :{m_last_name}                
█ [3] Age           :{m_age}                 
█ [4] Gender        :{m_gender}                 
█ [5] Weight        :{m_weight}                 
█ [6] Address       :{m_address}                 
█ [7] Email         :{m_email}                 
█ [8] Phone         :{m_phone}  
█ [9] Confirm                       █               
█ [0] Exit                          █
█████████████████████████████████████
            """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            i = input("First name :")
            if security.regex.name_regex(i):
                m_first_name = i
            else:
                print("Invalid name")
        elif choice == '2':
            i = input("Last name :")
            if security.regex.name_regex(i):
                m_last_name = i
            else:
                print("Invalid name")
        elif choice == '3':
            i = input("Age :")
            if security.regex.age_regex(i):
                m_age = i
            else:
                print("Invalid age")
        elif choice == '4':
            i = input("Gender [M or F] :")
            if i.upper() == "M" or i == "F".upper():
                m_gender = i.upper()
            else:
                print("Invalid gender")
        elif choice == '5':
            i = input("Weight in kg :")
            if security.regex.weight_regex(i):
                m_weight = i
        elif choice == '6':
            while True:
                print(f"""
█████████████████████████████████████
█ ADD MEMBER - ADDRESS       
█████████████████████████████████████
█ [1] Street name       :{street_name}                    
█ [2] House number      :{house_number}                
█ [3] Zip code          :{zip_code}       
█      
█ Choose city from: Rotterdam, Amsterdam, Eindhoven, Utrecht, Groningen, Breda, Tilburg, Nijmegen, Almere
█ [4] City              :{city}
█ [5] Confirm Adress
█ [0] Exit                          █
█████████████████████████████████████
                """)
                address_choice = input("Enter choice :")
                if address_choice == "1":
                    i = input("Street name:")
                    if security.regex.street_name_regex(i):
                        street_name = i
                    else:
                        print("Invalid street name")
                elif address_choice == "2":
                    i = input("House number :")
                    if security.regex.house_number_regex(i):
                        house_number = i
                    else:
                        print("Invalid house number")
                elif address_choice == "3":
                    i = input("Zip code :")
                    if security.regex.zip_code_regex(i):
                        zip_code = i
                    else:
                        print("Invalid zip code")
                elif address_choice == "4":
                    i = input("City :")
                    if security.regex.verify_city(i):
                        city = i
                    else:
                        print("Invalid city choose from : Rotterdam, Amsterdam, Eindhoven, Utrecht, Groningen, Breda, Tilburg, Nijmegen, Almere")
                elif address_choice == "5":
                    address_list = [street_name, house_number, zip_code, city]
                    count = 0
                    for a in address_list:
                        if len(a) > 0:
                            count = count + 1
                    if count == 4:
                        m_address = ' '.join(string for string in address_list)
                        break
                    else:
                        print(f"Invalid address, Please provide all information")
                elif address_choice == "0":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == '7':
            i = input("Email (some@email.example):")
            if security.regex.email_regex(i):
                m_email = i
            else:
                print("Invalid email")
        elif choice == '8':
            i = input("Phone number : +31-6-")
            if security.regex.phone_regex(i):
                m_phone = "+31-6-"+i
            else:
                print("Invalid Phone number")
        elif choice == '9':
            temp = [m_first_name, m_last_name,  m_age, m_gender, m_weight, m_address, m_email, m_phone]
            count = 0
            for m in temp:
                if len(m) > 0:
                    count = count + 1
            if count == 8:
                db.add_member(m_first_name, m_last_name,  m_age, m_gender, m_weight, m_address, m_email, m_phone)
                break
            else:
                print(f"Member is missing data")

        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def search_member_menu(username, role, category):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ SEARCHING MEMBER ON : {category}
█ [0] Exit                          █
█████████████████████████████████████
            """)
        choice = input(f"Enter {category} to find user: ").strip() # NEEED TO ADD REGEX based on CATEGORY!!!!!!!!!!!!!! AND MAYBE LOG SUS
        if choice != '0':
            found_members = search_member(category, choice)
            found_member_list = member.see_members(found_members)
            return found_member_list
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def delete_member_menu(username, role):
    category = display_select_data(username, role, get_columns('members'), "SEARCH CATEGORY")
    members = search_member_menu(username, role, category)
    member_to_be_deleted = display_select_data(username, role, members, "DELETE MEMBER")
    if member_to_be_deleted == "":
        pass
    else:
        db.delete_member(member_to_be_deleted[0])

def modify_member_menu(username, role):
    pass

#------------------------------------------------------------------------------------------------------------------------------------------


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
                return data[i_choice-1]
            else:
                print("Invalid choice. Please try again.")
        elif choice == '0':
            return ""
        else:
            print("Invalid choice. Please try again.")
