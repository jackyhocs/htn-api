from functools import wraps
from flask import request
from voluptuous import Schema, REMOVE_EXTRA, All, Optional, Match, Email, Range, Coerce

SAFE_STRING = '^[a-zA-Z ]+$'
SKILLS_STRING='^[a-zA-Z +/]+$'
URL = '(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
PHONE = '^\+[0-9]+ \([0-9]{3}\) [0-9]{3}-[0-9]{4}$'


def _Skills(skills):
    if not isinstance(skills, list):
        raise TypeError('Invalid Skills, expected a list')
    for skill in skills:
        if not isinstance(skill['rating'], int):
            raise TypeError('Invalid Skills Rating, expected an INT')


_skills = Schema(_Skills)

user_put_schema = Schema({
    Optional('name'): All(str, Match(SAFE_STRING, msg="Invalid Name")),
    Optional('company'): All(str, Match(SAFE_STRING, msg="Invalid Company")),
    Optional('email'): All(Email(msg="Invalid Email")),
    Optional('latitude'): All(float, msg="Invalid Latitude"),
    Optional('longitude'): All(float, msg="Invalid Longitude"),
    Optional('picture'): All(str, Match(URL, msg="Invalid URL")),
    Optional('skills'): _skills,
    Optional('phone'): All(str, Match(PHONE, msg="Invalid Phone"))
}, extra=REMOVE_EXTRA)

skills_get_schema = Schema({
    Optional('skill'): All(str, Match(SKILLS_STRING, msg="Invalid Skill")),
    Optional('rating'): All(Coerce(int), Range(1, 10, True, True, msg="Invalid Rating: Out of range")),
    Optional('frequency'): All(Coerce(int), Range(1, msg="Invalid Frequency: Out of range")),
})


def validate_payload(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = request.get_json(silent=True)

            try:
                schema(payload)
            except Exception as e:
                return {"error": "Bad Request: Failed validation. {}".format(e)}, 400

            kwargs['payload'] = payload
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_params(schema, required=True):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            params = request.args
            if not params:
                params = request.get_json(silent=True) or {}

            if required and not params:
                return {"error": "Bad Request: Invalid Parameter Count."}, 400

            try:
                schema(params)
            except Exception as e:
                return {"error": "Bad Request: Failed validation. {}".format(e)}, 400
            return f(*args, **kwargs)
        return wrapper
    return decorator