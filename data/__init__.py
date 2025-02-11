import os
import sys
import sqlite3
from pathlib import Path
from data.setup_database import Database

os.environ['db_name'] = str(Path(__file__).resolve().parents[1]) + r'\airline_manager.db'
os.environ['test_io_table'] = 'temp_notes'
os.environ['io_table'] = 'notes'
os.environ['username'] = 'mikla'


try:
    Database().setup_database()

except sqlite3.OperationalError:
    print(
        'Программа не может получить доступ к БД '
        'и будет закрыта...')
    sys.exit(1)