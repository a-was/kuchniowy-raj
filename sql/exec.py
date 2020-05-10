import os
import sqlite3

DB_FILE = '../database.sqlite3'

db = sqlite3.connect(DB_FILE)
sql_files = [f for f in os.listdir('.') if f.endswith('.sql')]
for sql_file in sql_files:
    with open(sql_file) as f:
        for command in f.read().split(';'):
            command = command.strip()
            try:
                db.execute(command)
            except sqlite3.IntegrityError:
                print('WARNING - This command cannot be executed due to IntegrityError - {}'.format(command))
            db.commit()
db.close()
