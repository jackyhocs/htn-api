from flask import Flask, Blueprint
from flask_restful import Api, Resource, request
from config import SQLiteConfig
from model import UserModel
from sqlite3 import DatabaseError, IntegrityError, DataError
from validation import validate_payload, validate_params, user_put_schema, skills_get_schema

app = Flask(__name__)
app.config.from_object(SQLiteConfig)
app.register_blueprint(Blueprint('user', __name__), url_prefix='/api')
api = Api(app)


class User(Resource):
    def get(self, _id):
        '''
        Takes in an int as an id and returns the dictionary of the User
        :param _id:
        :return:
        Failure - Error codes: 500, 404
        Success - Dictionary: 200
        '''
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
        '''
        Takes in an int as an id and deletes the user with the id
        :param _id:
        :return:

        :param _id:
        :return:
        Failure - Error codes: 500, 404
        Success - No Content: 204
        '''
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
        '''
        Takes in an int as an id and updates the user with the validated payload
        :param _id:
        :return:
        Failure - Error codes: 500, 404
        Success - Dictionary: 200
        '''
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
        '''
        Returns a list of all users
        :return:
        Failure - Error codes: 500
        Success - List: 200
        '''
        user_model = UserModel()
        try:
            users = user_model.get_all_users()
        except (DatabaseError, IntegrityError):
            return {"message": "Internal Server Error"}, 500
        except Exception as e:
            return {"message": "Exception : {}".format(str(e))}, 500

        return users, 200


class SkillQuery(Resource):
    @validate_params(skills_get_schema)
    def get(self):
        '''
        Returns a list of skills that match the parameters entered by the user
        :return:
        Failure - Error codes: 500
        Success - List: 200
        '''
        params = request.args.to_dict()
        user_model = UserModel()
        try:
            skills = user_model.find_skill_by_params(params)
        except (DatabaseError, IntegrityError) as e:
            return {"message": "Internal Server Error {}".format(e)}, 500
        except Exception as e:
            return {"message": "Exception : {}".format(str(e))}, 500

        return skills, 200


api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserQuery, '/users/')
api.add_resource(SkillQuery, '/skills/')

if __name__ == "__main__":
    app.run(debug=True)
