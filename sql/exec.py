import os
import sqlite3

DB_FILE = '../database.sqlite3'
SQL_FILES_EXTENSIONS = '.sql'

db = sqlite3.connect(DB_FILE)
sql_files = [f for f in os.listdir('.') if f.endswith(SQL_FILES_EXTENSIONS)]
for sql_file in sorted(sql_files):
    with open(sql_file) as f:
        for command in f.read().split(';'):
            try:
                db.execute(command)
            except sqlite3.IntegrityError:
                print('WARNING - This command cannot be executed due to IntegrityError - {}'.format(command.strip()))
            except sqlite3.OperationalError:
                print('ERROR - This command raised OperationalError - '.format(command.strip()))
db.commit()
db.close()
