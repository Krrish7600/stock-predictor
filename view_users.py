import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# View all users
c.execute("SELECT * FROM users")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()