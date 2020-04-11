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
                         required=True,
                         location='args')
room_parser.add_argument('room_name', location='args')
room_parser.add_argument('stuff', location='args')

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
        msg = None
        if usr:
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
    # Add/delete a room that may/may not contain stuff
    # @jwt_required
    def post(self):
        '''Adding a room
        '''
        url_args = None
        json_data = None
        try:
            url_args = room_parser.parse_args()
        except Exception as err:
            print('Room POST err', err)
            return {'error': 'parse req err'}, 500

        json_data = request.get_json()
        print('AddRoom POST', url_args, json_data)
        db_user = User.find_user(url_args['owner'])
        if not db_user:
            return {
                'error': 'User {} doesn\'t exist'.format(url_args['owner'])
            }, 500
        res = db_user.add_room(url_args['room_name'], json_data)

        if res:
            return {'success': url_args['room_name'] + ' added!'}, 200
        else:
            return {"error": "failed to add room"}, 500

    def delete(self):
        url_args = None
        try:
            url_args = room_parser.parse_args()
        except Exception as err:
            print('Room POST err', err)
            return {'error': 'parse req err'}, 500

        print('Room POST', url_args)

        room = url_args.get('room_name')
        msg = None
        if room:
            try:
                # only delete this room
                db.update({"username": url_args.get('owner')},
                          {"$pull": {
                              "rooms": {
                                  "name": room
                              }
                          }})
                msg = {'success': 'deleted user ' + usr}, 200
            except Exception as err:
                msg = {'error': 'could not deletee room ' + room}, 500

        else:
            # delete all rooms
            db.update({"username": url_args.get('owner')},
                      {"$set": {
                          "rooms": []
                      }})
            msg = {'message': 'deleted all rooms'}, 200

        return msg

    def patch(self):
        # Update room name
        room_parser.add_argument('room_name_old',
                                 help='This field cannot be blank',
                                 required=True)
        room_parser.add_argument('room_name_new',
                                 help='This field cannot be blank',
                                 required=True)
        url_args = None
        try:
            url_args = room_parser.parse_args()
        except Exception as err:
            print('Room POST err', err)
            return {'error': 'parse req err'}, 500

        print('Room PATCH', url_args)

        # Mongo does not support rename on embedded doc
        # in array.
        # Use $set
        # Current room
        curr_room_stuff = db.find({"username": url_args.get('owner')},
                                  projection={
                                      "_id": 1,
                                      "rooms": {
                                          "$elemMatch": {
                                              "name":
                                              url_args.get('room_name_old')
                                          }
                                      }
                                  })["rooms"][0]
        print("curr_room_stuff", curr_room_stuff)
        curr_room_stuff['name'] = url_args.get('room_name_new')
        print("curr_room_stuff after update", curr_room_stuff)
        db.update(
            {"username": url_args.get('owner')},
            {"$pull": {
                "rooms": {
                    "name": url_args.get('room_name_old')
                }
            }})

        db.update({'username': url_args.get('owner')},
                  {"$push": {
                      "rooms": curr_room_stuff
                  }})


class Stuff(Resource):
    def post(self):
        url_args = None
        json_data = None
        try:
            url_args = room_parser.parse_args()
            json_data = request.get_json()
        except Exception as err:
            print('Stuff POST err', err)
            return {'error': 'parse req err'}, 500

        print('Stuff POST', url_args, json_data)
        db_user = User.find_user(url_args['owner'])
        if not db_user:
            return {
                'error': 'User {} doesn\'t exist'.format(url_args['owner'])
            }, 500
        res = db_user.add_stuff_to_room(url_args['room_name'], json_data)

        if res:
            return {'success': 'Stuff added!'}, 200
        else:
            return {"error": "failed to add stuff"}, 500

    def delete(self):
        url_args = None
        json_data = None
        try:
            url_args = room_parser.parse_args()
            json_data = request.get_json()
        except Exception as err:
            print('Stuff delete err', err)
            return {'error': 'parse req err'}, 500

        if json_data:
            # Array of item(s) to delete
            update_cmd = {"$unset": dict()}
            for item in json_data:
                update_cmd["$unset"]["rooms.$[element].stuff." + item] = ""
            print("del stuff update cmd", update_cmd)
            db.update({"username": url_args.get('owner')},
                      update_cmd,
                      array_filters=[{
                          "element.name": url_args.get("room_name")
                      }])
        else:
            # Delete all stuff
            db.update({"username": url_args.get('owner')},
                      {"$set": {
                          "rooms.$[element].stuff": {}
                      }},
                      array_filters=[{
                          "element.name": url_args.get("room_name")
                      }])


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
        if db_user.check_password(url_args['password']):
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
