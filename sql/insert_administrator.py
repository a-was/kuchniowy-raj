from getpass import getpass
import sqlite3

from werkzeug.security import generate_password_hash

db = sqlite3.connect('../database.sqlite3')
cursor = db.cursor()

username_checked = False
while not username_checked:
    username = input('Nick: ')
    cursor.execute("SELECT username FROM users WHERE username LIKE ?", (username, ))
    if cursor.fetchone():
        print('This username is taken, please pick another one')
    else:
        username_checked = True

password = getpass('Password: ')
if password == getpass('Confirm password: '):
    cursor.execute("""
        INSERT INTO users (username, password, role_id) 
        VALUES (?, ?, 
        (SELECT role_id FROM roles WHERE name LIKE 'Administrator') ) 
    """, (username, generate_password_hash(password)))
    db.commit()
    print('Administrator added')
else:
    print('Passwords does not match!')
db.close()
