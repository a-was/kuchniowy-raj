from getpass import getpass
import sqlite3

from werkzeug.security import generate_password_hash

db = sqlite3.connect('../database.sqlite3')
cursor = db.cursor()

nick_checked = False
while not nick_checked:
    nick = input('Nick: ')
    cursor.execute("SELECT nick FROM users WHERE nick LIKE ?", (nick, ))
    if cursor.fetchone():
        print('This nick is taken, please pick another one')
    else:
        nick_checked = True

password = getpass('Password: ')
if password == getpass('Confirm password: '):
    cursor.execute("""
        INSERT INTO users (nick, password, role_id) 
        VALUES (?, ?, 
        (SELECT role_id FROM roles WHERE name LIKE 'Administrator') ) 
    """, (nick, generate_password_hash(password)))
    db.commit()
    print('Administrator added')
else:
    print('Passwords does not match!')
db.close()
