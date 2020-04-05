from flask import render_template, jsonify, request
from app.main.models import User, Room, BlacklistToken, UserSchema, RoomSchema
from flask_restful import Resource, reqparse
from app.db import db
from pymongo.errors import DuplicateKeyError
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# Like argparse, but for requests to these Resources.
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username',
                         help='This field cannot be blank',
                         required=True)
auth_parser.add_argument('password',
                         help='This field cannot be blank',
                         required=True)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')

room_parser = reqparse.RequestParser()
room_parser.add_argument('owner',
                         help='This field cannot be blank',
                         required=True)
room_parser.add_argument('room_name',
                         help='This field cannot be blank',
                         required=True)
room_parser.add_argument('stuff')

# For better serialization and stuff
user_schema = UserSchema()


class Users(Resource):
    def get(self):
        url_args = None
        try:
            url_args = user_parser.parse_args()
        except Exception as err:
            print('Users GET parse req err', err)
            return {'error': 'parse req err'}, 500

        # Get all users or 1 user?
        usr = url_args.get('username')
        if usr:
            try:
                user = db.find({'username': usr})
                return user_schema.dump(user), 200
            except Exception as err:
                print('Users GET find err', err)
                return {'error': 'could not find ' + usr}, 500
        else:
            cursor = db.find_all({}, 'users')
            users = []
            for doc in cursor:
                users.append(user_schema.dump(doc))
            return users, 200

    def delete(self):
        url_args = None
        try:
            url_args = user_parser.parse_args()
        except Exception as err:
            print('Users DEL parse req err', err)
            return {'error': 'parse req err'}, 500

        usr = url_args.get('username')
        print('here', url_args)
        msg = None
        if usr:
            print('here')
            try:
                db.delete({"username": usr})
                msg = {'success': 'deleted user ' + usr}, 200
            except Exception as err:
                msg = {'error': 'could not deletee user' + usr}, 500
        else:
            db.reset()
            msg = {'message': 'deleted all users'}, 200

        return msg


class Room(Resource):
    # Add a room for a user
    # @jwt_required
    def post(self):
        url_args = None
        json_data = None
        try:
            url_args = room_parser.parse_args()
            json_data = request.get_json()
        except Exception as err:
            print('AddRoom POST err', err)

        print('AddRoom POST', url_args, json_data)
        db_user = User.find_user(url_args['owner'])
        if not db_user:
            return {
                'message': 'User {} doesn\'t exist'.format(url_args['owner'])
            }
        user = user_schema.load(db_user)
        stuffs = json_data['stuff']
        res = user.add_room(url_args['room_name'], stuffs)

        if res:
            return {'success': url_args['room_name'] + ' added!'}, 200
        else:
            return {"error": "failed to add room"}, 500


class Stuff(Resource):
    def post(self):
        url_args = None
        json_data = None
        try:
            url_args = room_parser.parse_args()
            json_data = request.get_json()
        except Exception as err:
            print('AddStuff POST err', err)

        print('AddStuff POST', url_args, json_data)
        # User should already have room to add items to
        selector = {
            "username": url_args['owner'],
            "rooms": {
                "$elemMatch": {
                    "name": url_args['room_name']
                }
            }
        }
        res = db.find(selector)
        print("res", res, type(res))
        if res:
            stuff = json_data['stuff']
            print('stuff', stuff)
            current_stuff = res['rooms'][0]['stuff']
            print('current_stuff', current_stuff)
            current_stuff.update(stuff)
            print('current_stuff after update', current_stuff)
            db.update(selector, {"$set": {"rooms.0.stuff": current_stuff}})


class Register(Resource):
    def post(self):
        url_args = None
        try:
            url_args = auth_parser.parse_args()
        except Exception as err:
            print('Register POST parse req err', err)
            return {'error': 'parse req err'}, 500

        print('Register POST', url_args)
        uname = url_args['username']
        # First, does the requested user account exist?
        if not User.find_user(uname):
            new_user = User(uname)
            new_user.set_password(url_args['password'])
            db.create(user_schema.dump(new_user), 'users')
            # JWT stuff
            access_token = create_access_token(identity=uname)
            refresh_token = create_refresh_token(identity=uname)
            return {
                'success': uname + ' added!',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'error': 'Username already exists'}, 500


class Login(Resource):
    def post(self):
        url_args = None
        try:
            url_args = auth_parser.parse_args()
        except Exception as err:
            print('Login POST parse req err', err)
            return {'error': 'parse req err'}, 500

        uname = url_args['username']
        db_user = User.find_user(uname)
        if not db_user:
            return {'message': 'User {} doesn\'t exist'.format(uname)}
        # same password?
        # print('****', user_schema.load(db_user))
        if user_schema.load(db_user).check_password(url_args['password']):
            access_token = create_access_token(identity=uname)
            refresh_token = create_refresh_token(identity=uname)
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {"message": "Login unsuccessful"}


class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = BlacklistToken(jti)
            blacklisted_token.add()

            return {'message': 'Access token has been revoked'}, 200
        except:
            return {
                'message': 'Something went wrong with access token on logout'
            }, 500


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = BlacklistToken(jti)
            blacklisted_token.add()
            return {'message': 'Refresh token has been revoked'}, 200
        except:
            return {
                'message': 'Something went wrong with refresh token on logout'
            }, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class TestResource(Resource):
    @jwt_required
    def get(self):
        return {'answer': 42}
