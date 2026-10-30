"""Simple SQLite backup: python scripts/backup_db.py
Schedule it with cron / PythonAnywhere "Tasks" for automatic backups."""
import os
import shutil
from datetime import datetime

base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src = os.path.join(base, 'blog.db')
dst_dir = os.path.join(base, 'backups')
os.makedirs(dst_dir, exist_ok=True)
if os.path.exists(src):
    dst = os.path.join(dst_dir, f"blog_{datetime.now():%Y%m%d_%H%M%S}.db")
    shutil.copy2(src, dst)
    print('Backup created:', dst)
else:
    print('No database found at', src)
