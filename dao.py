import sqlite3


conn = sqlite3.connect('users.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()


class UserDao():
    @classmethod
    def get_by_id(cls, _id) -> dict:
        try:
            c.execute("SELECT * FROM USERS WHERE id=:id", {'id': _id})
            user = c.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e

        if not user:
            raise sqlite3.DataError

        return dict(user)

    @classmethod
    def get_all_users(cls):
        try:
            c.execute("SELECT * FROM USERS")
            users = c.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError from e

        users_collection = [dict(user) for user in users]

        return users_collection

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

    @classmethod
    def update_user(cls, _id, payload):
        existing = cls.get_by_id(_id)
        existing.update(**payload)
        with conn:
            try:
                c.execute("UPDATE USERS SET name = :name, company = :company, \
                                email = :email, latitude = :latitude, longitude = :longitude,\
                                picture = :picture, skills = :skills, phone = :phone WHERE id = :id",
                          {
                              'name': existing['name'],
                              'picture': existing['picture'],
                              'company': existing['company'],
                              'email': existing['email'],
                              'phone': existing['phone'],
                              'latitude': existing['latitude'],
                              'longitude': existing['longitude'],
                              'skills': existing['skills'],
                              'id': _id
                          })
            except sqlite3.Error as e:
                raise sqlite3.DatabaseError from e

        return cls.get_by_id(_id)
