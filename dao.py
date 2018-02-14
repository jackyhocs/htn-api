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
        try:
            c.execute("SELECT * FROM USERS WHERE id=:id", {'id': _id})
            user = c.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e

        if not user:
            print("data error")
            raise sqlite3.DataError
        return user

    @classmethod
    def get_all_users(cls):
        try:
            c.execute("SELECT * FROM USERS")
            users = c.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e
        return users

    @classmethod
    def delete_user(cls, _id):
        with conn:
            try:
                c.execute("DELETE from USERS WHERE id = :id",
                      {'id': _id})
                deleted = c.execute("SELECT changes()")
            except sqlite3.Error as e:
                raise sqlite3.DatabaseError from e

            if not deleted:
                raise sqlite3.DataError


'''
c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
     c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})
        c.execute("DELETE from USERS WHERE id = :id",
                  {'id': _id})
'''