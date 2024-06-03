def member_menu(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1] Add member                    █
█ [2] Modify member                 █
█ [3] Search member                 █
{"█ [4] Delete member                 █" if role == "system-admin" or role == "super-admin" else "█                                   █"}
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
        elif choice == '4' and (role == "system-admin" or role == "super-admin"):
            break
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def add_member():
    pass

def modify_member():
    pass

def search_member():
    pass

def delete_member():
    pass