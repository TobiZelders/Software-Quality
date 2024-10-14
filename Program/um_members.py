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


db.display_all_info()
display.main_menu()
