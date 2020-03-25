from flask import Flask, g, current_app
from marshmallow import Schema, fields, post_load, EXCLUDE
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    '''A User interacts with the site and CRUDs Rooms.
    '''
    def __init__(self, username, password=None, rooms=None):
        self.username = username
        self.password = password
        if rooms is None:
            self.rooms = []
        else:
            self.rooms = rooms
        print("User __init__", self.rooms, type(self.rooms))

    def add_room(self, name, stuff=None):
        ''' A wrapper for Room's constructor
        '''
        room_schema = RoomSchema(many=True)
        room = Room(name, stuff)
        self.rooms.append(room)

        # Dump rooms for db to handle
        rooms = room_schema.dump(self.rooms)
        print('room added, adding to db', rooms)
        return db.update({'username': self.username},
                         {"$set": {
                             "rooms": rooms
                         }}, 'users')

    @classmethod
    def find_user(cls, username):
        # print('looking for {}'.format(user.username))
        usr = db.find({'username': username}, 'users')
        # print('usr found:', usr)
        return usr

    @classmethod
    def delete(cls, user=None):
        '''Delete all records of user. If None, delete all users.
        '''
        if user:
            db.delete({'username': user.username}, 'users')
        else:
            db.reset('users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # print('checking {} to {} or {}'.format(
        #     self.password, password, generate_password_hash(password)))
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username} {self.password}>'


# Framework and internet recommended way of handling blacklisted
# tokens, those that should no longer be given access.
class BlacklistToken(object):
    def __init__(self, jti):
        self.jti = jti

    def add(self):
        db.create({'jti': self.jti}, 'jwt_tokens')

    @classmethod
    def is_jti_blacklisted(cls, jti):
        res = db.find({'jti': jti}, 'jwt_tokens')
        return bool(res)


class Room(object):
    '''A Room has a name and may contain stuff.
    '''
    def __init__(self, name, stuff=None):
        # stuff: A list of tuples: (item, price)
        self.name = name
        if stuff is None:
            self.stuff = []
        else:
            self.stuff = stuff

    # def __repr__(self):
    #     return f'<Room {self.name} has {len(self.stuff)} stuff.>'


class RoomSchema(Schema):
    name = fields.Str()
    stuff = fields.List(fields.Tuple((fields.Str(), fields.Str())))

    @post_load
    def make_room(self, data, **kwargs):
        # print('loading room into Class', data)
        return Room(**data)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    rooms = fields.List(fields.Nested(RoomSchema))

    @post_load
    def make_user(self, data, **kwargs):
        # print('loading user into Class', data)
        return User(**data)

    class Meta:
        unknown = EXCLUDE