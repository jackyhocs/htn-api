import sqlite3
import json

conn = sqlite3.connect('users.db')
c = conn.cursor()
#
c.execute("""CREATE TABLE USERS (
  id INTEGER,
  name TEXT,
  picture TEXT,
  company TEXT,
  email TEXT,
  phone TEXT,
  latitude FLOAT,
  longitude FLOAT,
  skills TEXT
  )""")
'''
{"company":"Slambda",
"email":"elizawright@slambda.com",
"latitude":48.4862,
"longitude":-34.7754,
"name":"Jenna Luna",
"phone":"+1 (913) 504-2495",
"picture":"http://lorempixel.com/200/200/sports/8",
"skills":[{"name":"JS","rating":5},{"name":"Go","rating":5}]}
'''
with open('users.json', 'r') as data_file:
    users = json.loads(data_file.read())
    i = 0
    for user in users:
        c.execute("INSERT INTO USERS VALUES(:id ,:name, :picture, :company, :email, :phone, :latitude, :longitude, :skills)",
                  {
                      'id': i,
                      'name': user['name'],
                      'picture': user['picture'],
                      'company': user['company'],
                      'email': user['email'],
                      'phone': user['phone'],
                      'latitude': user['latitude'],
                      'longitude': user['longitude'],
                      'skills': json.dumps(user['skills']),
                   })
        i += 1
conn.commit()


# p = c.execute("SELECT * FROM USERS WHERE name=:name", {'name': "Jenna Luna"})
# print(p.fetchall())
conn.close()