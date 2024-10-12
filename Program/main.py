import display
import db
import backup
from security.encryption import init_rsa

backup.backup()
backup.restore('backup_2024-10-12_20-53-28')
db.initialize_db()
#db.display_all_info()
display.main_menu()

"""
ERRORS:



TODO
1. Backups - backup restore
2. Make all menu's
3. Log every suspicious thing (checken)
4. Make regex for user input
5. Defend against brute force
"""

