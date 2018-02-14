from flask import Flask, Blueprint
from flask_restful import Api, Resource
from config import SQLiteConfig
from model import UserModel

app = Flask(__name__)
app.config.from_object(SQLiteConfig)
app.register_blueprint(Blueprint('user', __name__), url_prefix='/api')
api = Api(app)


class User(Resource):
    def get(self, _id):
        user_model = UserModel()
        user = user_model.get_by_id(_id)
        return user.get_fields(), 200

    def delete(self, _id):
        user_model = UserModel()
        user_model.delete_user(_id)
        return {}, 204

class UserQuery(Resource):
    def get(self):
        user_model = UserModel()
        users = user_model.get_all_users()
        return users, 200


api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserQuery, '/users/')

if __name__ == "__main__":
    app.run(debug=True)