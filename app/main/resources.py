from flask import render_template, jsonify, request
from app.main.models import UserDB, RoomDB, BlacklistToken, UserSchema, RoomSchema
from flask_restful import Resource, reqparse
from app.db import db
from pymongo.errors import DuplicateKeyError
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# TODO: Could this all be in a custom RequestParser class?
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

PARSE_ERROR = -1
PARSE_ERROR_MSG = {'error': 'parse req err'}, 500


def fetch_user_args():
    try:
        return user_parser.parse_args()
    except Exception as err:
        print('USERS parse req err', err)
        return PARSE_ERROR


def fetch_auth_args():
    try:
        return auth_parser.parse_args()
    except Exception as err:
        print('AUTH parse req err', err)
        return PARSE_ERROR


def fetch_room_args():
    url_args = None
    json_data = None
    try:
        url_args = room_parser.parse_args()
        json_data = request.get_json()
    except Exception as err:
        print('ROOM parse req err', err)
        return PARSE_ERROR

    return url_args, json_data


class Users(Resource):
    def get(self):
        url_args = fetch_user_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        uname = url_args.get('username')
        msg = None
        # Get all users or 1 user?
        if uname:
            # Create User-DB interface, if they exist.
            u = UserDB.find_user(uname)

            # Get from DB
            if u and u.username:
                return user_schema.dump(u), 200
            else:
                msg = {'error': 'could not find ' + u}, 500
        else:
            # Basically a full pull on the DB, so no interface.
            # TODO: Add projection to hide things, like password hash
            cursor = db.find_all({})
            users = []
            for doc in cursor:
                users.append(user_schema.dump(doc))
            msg = users, 200

        return msg

    def delete(self):
        url_args = fetch_user_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        uname = url_args.get('username')
        msg = None
        # Delete all users or this user?
        # TODO: Control who can delete all users.
        if uname:
            # Create User-DB interface
            u = UserDB(uname)
            if u.delete_user():
                msg = {'success': 'deleted user ' + u.username}, 200
            else:
                msg = {'error': 'failed to delete user ' + u.username}, 500
        else:
            db.drop()
            msg = {'message': 'deleted all users'}, 200

        return msg


class Room(Resource):
    # Add/delete a room that may/may not contain stuff
    # @jwt_required
    def post(self):
        '''Adding a room
        '''
        url_args, json_data = fetch_room_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        print('Room POST', url_args, json_data)
        u = UserDB.find_user(url_args['owner'])
        msg = None
        if not u:
            msg = {
                'error': 'User {} doesn\'t exist'.format(url_args['owner'])
            }, 500

        if u.add_room(url_args['room_name'], json_data):
            msg = {'success': url_args['room_name'] + ' added!'}, 200
        else:
            msg = {"error": "failed to add room"}, 500

        return msg

    def delete(self):
        url_args, json_data = fetch_room_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        print('Room POST', url_args)

        room = url_args.get('room_name')
        owner = url_args['owner']
        msg = None
        u = UserDB.find_user(owner)
        if not u:
            msg = {'error': 'User {} doesn\'t exist'.format(owner)}, 500
        if u.remove_room(room):
            if room:
                msg = {'success': 'deleted room ' + room}, 200
            else:
                msg = {'success': 'deleted all rooms'}, 200
        else:
            msg = {'error': 'could not deletee room ' + room}, 500

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
        url_args, json_data = fetch_room_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        print('Stuff POST', url_args, json_data)
        u = UserDB.find_user(url_args['owner'])

        if not u:
            return {
                'error': 'User {} doesn\'t exist'.format(url_args['owner'])
            }, 500

        msg = None
        if u.put_stuff_in_room(url_args['room_name'], json_data):
            msg = {'success': 'Stuff added!'}, 200
        else:
            msg = {"error": "failed to add stuff"}, 500
        return msg

    def delete(self):
        url_args, json_data = fetch_room_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        u = UserDB.find_user(url_args['owner'])
        if not u:
            return {
                'error': 'User {} doesn\'t exist'.format(url_args['owner'])
            }, 500

        msg = None
        u.remove_stuff()
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

    # def patch(self):
    #     url_args = None
    #     json_data = None
    #     try:
    #         url_args = room_parser.parse_args()
    #         json_data = request.get_json()
    #     except Exception as err:
    #         print('Stuff PATCH err', err)
    #         return {'error': 'parse req err'}, 500

    #     # Get name changes, if any
    #     # print("req_updates", json_data)
    #     # name_updates = [for key in ]

    #     # if req_updates.get("name"):
    #     curr_stuff = db.find({"username": url_args.get("owner")},
    #                          projection={
    #                              "_id": 0,
    #                              "rooms": {
    #                                  "$elemMatch": {
    #                                      "name": url_args.get('room_name')
    #                                  }
    #                              }
    #                          })['rooms'][0]["stuff"]
    #     print("curr_stuff", curr_stuff)
    #     for item in json_data:
    #         for key, value in json_data[item].items():
    #             print("key", key, value)
    #             if key == "name":
    #                 curr_stuff[value] = curr_stuff[item]
    #                 del curr_stuff[item]
    #                 item = value
    #             if key == "value":
    #                 curr_stuff[item] = value
    #             print("inter curr_stuff", curr_stuff)
    #     print("curr_stuff updated", curr_stuff)
    #     db.update({"username": url_args.get('owner')},
    #               {"$set": {
    #                   "rooms.$[element].stuff": curr_stuff
    #               }},
    #               array_filters=[{
    #                   "element.name": url_args.get("room_name")
    #               }])


class Register(Resource):
    def post(self):
        url_args = fetch_auth_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        print('Register POST', url_args)
        uname = url_args['username']
        msg = None
        # First, does the requested user account exist?
        u = UserDB.find_user(uname)
        if u:
            msg = {'error': 'Username already exists'}, 500
        else:
            # Replace the empty var with a new User
            u = UserDB(uname)
            u.password = (url_args['password'])
            db.create(user_schema.dump(u))
            # JWT stuff
            access_token = create_access_token(identity=uname)
            refresh_token = create_refresh_token(identity=uname)
            msg = {
                'success': uname + ' added!',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return msg


class Login(Resource):
    def post(self):
        url_args = fetch_auth_args()
        if url_args == PARSE_ERROR:
            return PARSE_ERROR_MSG

        uname = url_args['username']
        u = UserDB.find_user(uname)
        msg = None
        if not u:
            msg = {'error': 'User {} doesn\'t exist'.format(uname)}
        # same password?
        # print('****', user_schema.load(db_user))
        if u.check_password(url_args['password']):
            access_token = create_access_token(identity=uname)
            refresh_token = create_refresh_token(identity=uname)
            msg = {
                'success': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            msg = {"error": "Login unsuccessful"}
        return msg


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
