import json


class UserModel:

    def __init__(self, collection=None):
        self.name = collection.get('name', None)
        self.picture = collection.get('picture', None)
        self.company = collection.get('company', None)
        self.email = collection.get('email', None)
        self.phone = collection.get('phone', None)
        self.country = collection.get('country', None)
        self.latitude = collection.get('latitude', None)
        self.longitude = collection.get('longitude', None)
        self.skills = collection.get('skills', None)

    def get_fields(self):
        return self.__dict__

    def get_by_id(self, id):
        return UserModel({"name": "hello"})

    def get_all_users(self):
        return UserModel({"name": "hello"})

    def update_user(self, id, payload):
        return UserModel({"name": "hello"})
