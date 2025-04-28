import shutil
import datetime
import os

def backup_database():
    backup_dir = "/backup/"
    os.makedirs(backup_dir, exist_ok=True)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    shutil.copy("/app/database.db", f"{backup_dir}/backup-{date}.db")
