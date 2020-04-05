from flask import Flask, g, current_app, json
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

        self.room_schema = RoomSchema()

    def add_room(self, name, stuff=None):
        ''' A wrapper for Room's constructor
        @param name: str
        @param stuff: dict
        '''

        room = None
        try:
            print("add room stuff", stuff)
            room = self.room_schema.load({"name": name, "stuff": stuff})
        except Exception as err:
            print('load error add room', err)
            return False

        print(room)
        # self.rooms.append(room)

        # Dump rooms for db to handle
        room = self.room_schema.dump(room)
        print('room added, adding to db', room)
        return db.update({'username': self.username},
                         {"$push": {
                             "rooms": room
                         }})

    def add_stuff_to_room(self, _room, stuff):
        ''' 
        @param name: str
        @param stuff: dict
        '''
        # Get room from db
        selector = {"username": self.username, "rooms.name": _room}
        projection = {"rooms": 1, "_id": 0}
        db_rooms = db.find(selector, projection).get("rooms")
        print("db_rooms", db_rooms, type(db_rooms))
        curr_room = [room for room in db_rooms if room['name'] == _room][0]
        for room in db_rooms:
            print(room)
        print("curr_room", curr_room)
        room_obj = self.room_schema.load(curr_room)
        print("room_obj", room_obj)
        room_obj.add_stuff(stuff)
        print('room_obj after add', room_obj)

        res = self.room_schema.dump(room_obj)
        print('dump res', res)

        l = db.update(selector,
                      {"$set": {
                          "rooms.$[element]" + ".stuff": res['stuff']
                      }},
                      array_filters=[{
                          "element.name": _room
                      }])
        print('add stuff result', l)

    @classmethod
    def find_user(cls, username):
        # print('looking for {}'.format(user.username))
        usr = db.find({'username': username})
        # print('usr found:', usr)
        if usr:
            return UserSchema().load(usr)
        return usr

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # print('checking {} to {} or {}'.format(
        #     self.password, password, generate_password_hash(password)))
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username} {self.password}>'


class Room(object):
    '''A Room has a name and may contain stuff.
    '''
    def __init__(self, name, stuff=None):
        # stuff: A dict of items: {item: price}
        self.name = name
        if stuff is None:
            self.stuff = dict()
        else:
            self.stuff = stuff

    def add_stuff(self, stuff):
        print("add stuff in Room", stuff)
        for key, value in stuff.items():
            self.stuff[key] = value

    def __repr__(self):
        return f'<Room {self.name} has {len(self.stuff)} stuff.>'


class RoomSchema(Schema):
    name = fields.Str(required=True)
    stuff = fields.Dict(keys=fields.Str(),
                        values=fields.Str(),
                        allow_none=True)

    @post_load
    def make_room(self, data, **kwargs):
        print('loading room into Class', data)
        return Room(**data)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str()
    rooms = fields.List(fields.Nested(RoomSchema))

    @post_load
    def make_user(self, data, **kwargs):
        # print('loading user into Class', data)
        return User(**data)

    class Meta:
        unknown = EXCLUDE


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