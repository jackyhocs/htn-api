import sqlite3
import json
from collections import namedtuple

connUsers = sqlite3.connect('users.db')
cUsers = connUsers.cursor()

# USERS TABLE
cUsers.execute("""CREATE TABLE USERS (
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

connSkills = sqlite3.connect('skills.db')
cSkills = connSkills.cursor()

#SKILLS TABLE
cSkills.execute("""CREATE TABLE SKILLS (
  skill TEXT,
  num_users INTEGER,
  total_rating INTEGER,
  avg_rating FLOAT
)""")

with open('users.json', 'r') as data_file:
    users = json.loads(data_file.read())
    i = 0
    skillsSet = {}
    Skill = namedtuple('Skill', ['num_users', 'total_rating'])
    for user in users:
        #Inserts each user
        cUsers.execute("INSERT INTO USERS VALUES(:id ,:name, :picture, :company, :email, :phone, :latitude, :longitude, :skills)",
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
        for skill in user['skills']:
            #builds an object storing all of the skills and scores of the users
            skill_name = skill['name']
            skill_rating = skill['rating']
            if skill_name in skillsSet:
                num = getattr(skillsSet[skill_name], 'num_users')
                rating = getattr(skillsSet[skill_name], 'total_rating')
                skillsSet[skill_name] = Skill(num + 1, rating + skill_rating)
            else:
                skillsSet[skill_name] = Skill(1, skill_rating)

    # inserts the user's skills in to the skills table
    for k, v in skillsSet.items():
        num_users = getattr(v, 'num_users')
        total_rating = getattr(v, 'total_rating')
        cSkills.execute("INSERT INTO SKILLS VALUES(:skill, :num_users, :total_rating, :avg_rating)",
                        {
                            'skill': k,
                            'num_users': num_users,
                            'total_rating': total_rating,
                            'avg_rating': total_rating/num_users
                        })
connSkills.commit()
connUsers.commit()

connSkills.close()
connUsers.close()