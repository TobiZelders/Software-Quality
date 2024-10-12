
def consultant_menu(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1]  Backup                       █
█ [2]  Restore backup               █    
█ [0]  Exit                         █
█████████████████████████████████████        
        """)
        choice = input("Enter choice: ").strip()
        if choice == '1':
            break
        elif choice == '2':
            break
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

