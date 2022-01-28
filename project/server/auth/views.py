import json
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

from sqlalchemy.ext.declarative import DeclarativeMeta


auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json(); print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

class UserIndexAPI(MethodView):
    def get(self):
        # user_info = jsonify(User.query.all())
        # return  user_info
        return json.dumps(User.query.all(), cls=AlchemyEncoder)

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
user_index_view = UserIndexAPI.as_view('user_index_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

auth_blueprint.add_url_rule(
    '/users/index',
    view_func=user_index_view,
    methods=['GET']
)

# Cite from https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json?noredirect=1&lq=1
class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
