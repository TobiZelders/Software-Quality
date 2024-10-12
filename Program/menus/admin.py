from db import quick_auth

def admin_menu(username, role):
    quick_auth(role, "system-admin")
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1] Add admin                     █
█ [2] Modify admin                  █    
█ [3] Delete admin                  █
█ [4] Reset admin password          █
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
            break
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")