def consultant_menu(username, role):
    while True:
        print(f"""
█████████████████████████████████████
█ ROLE: {role} 
█ USER: {username}          
█████████████████████████████████████
█ [1]  Add consultant               █
█ [2]  Modify consultant            █    
█ [3]  Delete consultant            █
█ [4]  Reset consultant password    █
█ [0]  Exit                         █
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

