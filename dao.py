import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('users.db', check_same_thread=False)
conn.row_factory = dict_factory
c = conn.cursor()

class UserDao():
    @classmethod
    def get_by_id(cls, _id):
        c.execute("SELECT * FROM USERS WHERE id=:id", {'id': _id})
        return c.fetchone()

    @classmethod
    def get_all_users(cls):
        c.execute("SELECT * FROM USERS")
        return c.fetchall()

    @classmethod
    def delete_user(cls, _id):
        with conn:
            c.execute("DELETE from USERS WHERE id = :id",
                      {'id': _id})



'''
c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
     c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})
        c.execute("DELETE from USERS WHERE id = :id",
                  {'id': _id})
'''