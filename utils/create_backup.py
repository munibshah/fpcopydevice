import os
import shutil
import json
import datetime


def create_backup(folder_name='output'):
    if not os.path.exists(folder_name):
        print(f"Folder '{folder_name}' does not exist.")
        return
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{timestamp}.zip"
    
    shutil.make_archive(backup_name.replace('.zip', ''), 'zip', folder_name)
    
    print(f"Backup created: {backup_name}")