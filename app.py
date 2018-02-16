from flask import Flask, Blueprint
from flask_restful import Api, Resource
from config import SQLiteConfig
from model import UserModel
from sqlite3 import DatabaseError, IntegrityError, DataError
from validation import validate_payload, user_put_schema

app = Flask(__name__)
app.config.from_object(SQLiteConfig)
app.register_blueprint(Blueprint('user', __name__), url_prefix='/api')
api = Api(app)


class User(Resource):
    def get(self, _id):
        user_model = UserModel()
        try:
            user = user_model.get_by_id(_id)
        except DataError:
            return {"message": "User with ID {} does not exist".format(_id)}, 404
        except (DatabaseError, IntegrityError):
            return {"message": "Internal Server Error"}, 500
        except Exception as e:
            return {"message": "Exception : {}".format(str(e))}, 500

        return user.get_fields(), 200

    def delete(self, _id):
        user_model = UserModel()
        try:
            user_model.delete_user(_id)
        except DataError:
            return {"message": "User with ID {} does not exist".format(_id)}, 404
        except (DatabaseError, IntegrityError):
            return {"message": "Internal Server Error"}, 500
        except Exception as e:
            return {"message": "Exception : {}".format(str(e))}, 500

        return {}, 204

    @validate_payload(user_put_schema)
    def put(self, _id, **kwargs):
        payload = kwargs.get('payload', None)
        user_model = UserModel()
        try:
            user = user_model.update_user(_id, payload)
        except DataError:
            return {"message": "User with ID {} does not exist".format(_id)}, 404
        except (DatabaseError, IntegrityError):
            return {"message": "Internal Server Error"}, 500
        except Exception as e:
            return {"message": "Exception : {}".format(str(e))}, 500

        return user.get_fields(), 200


class UserQuery(Resource):
    def get(self):
        user_model = UserModel()
        try:
            users = user_model.get_all_users()
        except DataError:
            return {"message": "User with ID {} does not exist".format(_id)}, 404
        except (DatabaseError, IntegrityError):
            return {"message": "Internal Server Error"}, 500
        except Exception as e:
            return {"message": "Exception : {}".format(str(e))}, 500
        return users, 200


api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserQuery, '/users/')

if __name__ == "__main__":
    app.run(debug=True)