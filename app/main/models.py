from flask import Flask, g, current_app, json
from marshmallow import Schema, fields, post_load, EXCLUDE
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    '''User represents the document in the DB and provides access
    to CRUDing all fields.
    '''
    def __init__(self, username, password=None, rooms=None):
        self._username = username
        self._password = password
        self.rooms = rooms
        print("User __init__", self.rooms, type(self.rooms))

        self.room_schema = RoomSchema()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_name):
        '''Update username in DB
        '''
        pass
        # self.username = new_name

    @username.deleter
    def username(self):
        '''Delete self from DB.
        '''
        pass

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        '''Update password in DB
        '''
        pass
        # self.password = new_password

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

    def remove_room(self, room):
        '''Delete room(s) from DB.
        '''
        pass

    def add_stuff_to_room(self, _room, stuff):
        ''' 
        @param name: str
        @param stuff: dict
        '''
        # Get room from db
        selector = {"username": self.username, "rooms.name": _room}

        update_cmd = {"$set": {}}
        for key, value in stuff.items():
            update_cmd["$set"]["rooms.$[element]" + ".stuff." + key] = value

        print("update cmd", update_cmd)
        arr_filter = [{"element.name": _room}]

        return db.update(selector, update_cmd, array_filters=arr_filter)

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
    '''A Room provides deeper DB access to CRUD rooms directly 
    '''
    def __init__(self, name, stuff=None):
        # stuff: A dict of items: {item: price}
        self._name = name
        self.stuff = stuff

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self):
        '''Update name of Room in DB.
        '''
        pass

    def add_stuff(self, stuff):
        '''Add items to stuff in this room in DB.
        '''
        print("add stuff in Room", stuff)
        for key, value in stuff.items():
            self.stuff[key] = value

    def update_stuff(self, changes):
        '''Update stuff for this room in DB.
        @param changes: dict mapping old items to new.
        '''
        pass

    def remove_stuff(self, items):
        '''Remove items from stuff in this room in DB.
        '''
        pass

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