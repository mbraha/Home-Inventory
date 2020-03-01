from flask import Flask, g, current_app
from marshmallow import Schema, fields, post_load, EXCLUDE
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash

# class AddObject(object):
#     '''Base class
#     '''
#     def


class User(object):
    '''A User interacts with the site and CRUDs Rooms.
    '''
    def __init__(self, username):
        self.username = username
        # self.rooms = []

    # def add_room(self, name, stuff=None):
    #     room = Room(name, self.username, stuff)
    #     self.rooms.append(room)
    #     db.create(room)

    @classmethod
    def find_user(cls, user):
        print('looking for {}'.format(user.username))
        usr = db.find({'username': user.username})
        print('usr found:', usr)
        return usr

    @classmethod
    def delete(cls, user=None):
        '''Delete all records of user. If None, delete all users.
        '''
        if user:
            db.delete({'username': user.username})
        else:
            db.reset()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        print('checking {} to {} or {}'.format(
            self.password, password, generate_password_hash(password)))
        return check_password_hash(self.password, password)

    # def __str__(self):
    #     print(f'username: {self.username}')
    #     print(f'password_hash: {self.password_hash}')
    # print(f'rooms: {self.rooms} ({len(self.rooms)})')

    def __repr__(self):
        return f'<User {self.username} {self.password}>'


# class BlacklistTokens(object):
#     def __init__(self, id, jti):
#         self.id = id
#         self.jti = jti

#     @classmethod
#     def is_jti_blacklisted(cls, jti):
#         pass


class Room(object):
    '''A Room has a name and may contain stuff.
    '''
    def __init__(self, name, stuff=None):
        # stuff: A list of tuples: (item, price)
        self.name = name
        self.owner = owner
        self.stuff = stuff


class RoomSchema(Schema):
    name = fields.Str()
    owner = fields.Str()
    stuff = fields.List(fields.Tuple((fields.Integer(), fields.Float())))

    def __repr__(self):
        return f'<Room {self.name}>'


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    # rooms = fields.Nested(RoomSchema)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

    class Meta:
        unknown = EXCLUDE