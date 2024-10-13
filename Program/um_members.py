import display
import db
import os
import backup
from security.encryption import init_rsa
import security.regex
import display

if not os.path.exists("public_key.pem") or not os.path.exists("private_key.pem"):
    init_rsa()

if not os.path.exists("unique_meal.db"):
    db.initialize_db()

    db.add_member("Test", "Member", "10", "M", "3.0", "Teststreet", "T@email.com", "+31-6-12345678")

db.add_member("Test", "Member", "10", "M", "3.0", "Teststreet", "T@email.com", "+31-6-12345678")


db.display_all_info()
display.main_menu()

"""
ERRORS:



TODO
1. Backups - backup zips
2. Make all menu's
3. Log every suspicious thing (checken)
4. Make regex for user input
5. Defend against brute force
"""

