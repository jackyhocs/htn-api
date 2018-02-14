import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('users.db')
conn.row_factory = dict_factory
c = conn.cursor()

p = c.execute("SELECT * FROM USERS WHERE id=:id", {'id': 5})
print(p.fetchone())

c.close()