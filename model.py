import json
from dao import UserDao


class UserModel:
    _dao = None
    _collection = None

    def __init__(self, collection: dict = {}):
        self._dao        = UserDao
        self._collection = collection
        self.id          = collection.get('id', 0)
        self.name        = collection.get('name', "")
        self.picture     = collection.get('picture', "")
        self.company     = collection.get('company', "")
        self.email       = collection.get('email', "")
        self.phone       = collection.get('phone', "")
        self.latitude    = collection.get('latitude', 0)
        self.longitude   = collection.get('longitude', 0)
        self.skills      = json.loads(collection.get('skills', '{}'))

    def get_fields(self):
        dict = self.__dict__
        dict.pop('_dao', None)
        dict.pop('_collection', None)

        return dict

    def get_by_id(self, _id):
        user = self._dao.get_by_id(_id)

        return UserModel(user)

    def get_all_users(self):
        users = self._dao.get_all_users()

        user_collection = [{"count": len(users)}]

        for user in users:
            user_collection.append(UserModel(user).get_fields())

        return user_collection

    def delete_user(self, _id):
        self._dao.delete_user(_id)

    def update_user(self, _id, payload):
        user = self._dao.update_user(_id, payload)

        return UserModel(user)

    def find_skill_by_params(self, payload):
        skills = self._dao.find_skill_by_params(payload)

        return skills
