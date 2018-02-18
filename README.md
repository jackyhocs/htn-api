# htn-api

First run:

`python dbsetup.py`

to generate the tables and insert the users

Then run:

`python app.py`

API endpoint: `127.0.0.1:5000`

# Libraries used:

Flask==0.12.2

Flask-Restful==0.3.6

voluptuous==0.9.3

Flask-SQLAlchemy==2.3.2

SQLAlchemy==1.1.9

# Implemented endpoints

`/users/<int:id>`
GET, PUT, DELETE

`/users/`
GET

`/skills/`
GET

```json
Payload fields
{
  "rating": INT,
  "frequency": INT,
  "skill": STRING
}
```
