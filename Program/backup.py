import os
import shutil
from datetime import datetime

backup_files = ['private_key.pem', 'public_key.pem', 'unique_meal.db']
backup_folder = 'backups'

def backup():
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_subfolder = f'backups/backup_{timestamp}'
    os.makedirs(backup_subfolder)

    for file in backup_files:
        if os.path.isfile(file):
            shutil.copy(file, backup_subfolder)
            print(f"Copied '{file}' to '{backup_folder}'.")
        else:
            print(f"'{file}' is not a valid file.")

    return backup_subfolder

def restore(backup_subfolder):
    path = f'backups/{backup_subfolder}'

    if not os.path.exists(path) or not os.path.isdir(path):
        print(f"Backup folder '{backup_subfolder}' not found!")
        return

    delete_existing_files(backup_files, '')

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        if os.path.isfile(file_path):
            original_location = file_name
            shutil.copy(file_path, original_location)
            print(f"Restored {file_path}")

def delete_existing_files(file_names, directory):
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"File not found: {file_path}")

def get_backup_list():
    backup_list = []
    if not os.path.exists(backup_folder) or not os.path.isdir(backup_folder):
        print(f"Backup folder not found!")
        return backup_list

    for folder in os.listdir(backup_folder):
        backup_list.append(folder)

    return backup_list


