from flask import Flask, Blueprint
from flask_restful import Api, Resource
from config import SQLiteConfig
from model import UserModel
from sqlite3 import DatabaseError, ProgrammingError, IntegrityError, DataError
from errors import ApiException

app = Flask(__name__)
app.config.from_object(SQLiteConfig)
app.register_blueprint(Blueprint('user', __name__), url_prefix='/api')
api = Api(app)


class User(Resource):
    def get(self, _id):
        user_model = UserModel()
        try:
            user = user_model.get_by_id(_id)
        except (DatabaseError, IntegrityError) as e:
            return "Internal Server Error", 500
        except DataError as e:
            return "User with ID {} does not exist".format(_id), 404

        return user.get_fields(), 200

    def delete(self, _id):
        user_model = UserModel()
        try:
            user_model.delete_user(_id)
        except (DatabaseError, IntegrityError) as e:
            return ApiException(
                message="Internal Server Error",
                status=500
            ).response()
        except DataError as e:
            return ApiException(
                message="User with ID {} does not exist".format(_id),
                status=404
            ).response()

        return {}, 204

class UserQuery(Resource):
    def get(self):
        user_model = UserModel()
        try:
            users = user_model.get_all_users()
        except (DatabaseError, IntegrityError) as e:
            return ApiException(
                message="Internal Server Error",
                status=500
            ).response()

        return users, 200


api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserQuery, '/users/')

if __name__ == "__main__":
    app.run(debug=True)