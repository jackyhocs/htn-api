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
        return {"message": "no"}, 200


class UserQuery(Resource):
    def get(self):
        return {"message": "no"}, 200


api.add_resource(User, '/users/<int:_id>')
api.add_resource(UserQuery, '/users/')

if __name__ == "__main__":
    app.run(debug=True)