from flask import render_template, jsonify, request, after_this_request
from app.main.models import User, Room, BlacklistToken, UserSchema, RoomSchema
from flask_restful import Resource, reqparse
from app.db import db
from pymongo.errors import DuplicateKeyError
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt,
                                set_access_cookies, set_refresh_cookies,
                                unset_jwt_cookies)

# Like argparse, but for requests to these Resources.
parser = reqparse.RequestParser()
parser.add_argument('username',
                    help='This field cannot be blank',
                    required=True)
parser.add_argument('password',
                    help='This field cannot be blank',
                    required=True)

# For better serialization and stuff
user_schema = UserSchema()

EXPIRATION = 60 * 60 * 24 * 1  # One day


class AllUsers(Resource):
    # Get all docs from users table and return a list of usernames
    def get(self):
        cur = db.find_all({}, 'users')
        users = []
        for doc in cur:
            users.append(user_schema.dump(doc)['username'])
        return users

    def delete(self):
        User.delete()
        return {'message': 'deleted all users'}


class Register(Resource):
    def post(self):
        data = parser.parse_args()

        print('Register POST', data)
        # First, does the requested user account exist?
        new_user = User(data['username'])
        if not User.find_user(new_user):
            new_user.set_password(data['password'])
            db.create(user_schema.dump(new_user), 'users')
            # JWT stuff
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            response = {'success': data['username'], 'jwt_expiry': EXPIRATION}

            @after_this_request
            def cookie(response):
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                print(response, response.json)
                return response

            return response, 200

        else:
            return {'error': 'Username already exists'}, 500


class Login(Resource):
    def post(self):
        data = parser.parse_args()
        db_user = User.find_user(User(data['username']))
        if not db_user:
            return {
                'message': 'User {} doesn\'t exist'.format(data['username'])
            }, 500
        # same password?
        # print('****', user_schema.load(db_user))
        if user_schema.load(db_user).check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            response = {
                'message': 'Login successful',
                'jwt_expiry': EXPIRATION
            }

            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response, 200
        else:
            return {"message": "Login unsuccessful"}, 500


class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = BlacklistToken(jti)
            blacklisted_token.add()
            resp = {'message': 'Access token has been revoked'}
            unset_jwt_cookies(resp)
            return resp, 200
        except:
            return {
                'message': 'Something went wrong with access token on logout'
            }, 500


# class UserLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             blacklisted_token = BlacklistToken(jti)
#             blacklisted_token.add()
#             resp = {'message': 'Refresh token has been revoked'}
#             unset_jwt_cookies(resp)
#             return resp, 200
#         except:
#             return {
#                 'message': 'Something went wrong with refresh token on logout'
#             }, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        resp = {'refresh': True}
        set_access_cookies(resp, access_token)
        return resp, 200


class TestResource(Resource):
    @jwt_required
    def get(self):
        return {'answer': 42}, 200
