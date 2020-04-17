from flask import Flask, g, current_app, json
from marshmallow import Schema, fields, post_load, EXCLUDE
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserDB(object):
    '''User represents the document in the DB and provides access
    to CRUDing all fields.
    '''
    def __init__(self, username, password=None, rooms=[]):
        self._username = username
        self._password = password
        self.rooms = rooms

        # We set owner here because we didn't want to store owner
        # field in DB, as it's redundant with username field and we
        # don't plan on supporting acting on roooms if user isn't the
        # username.
        for room in self.rooms:
            room.owner = username
        print("User done __init__", self.rooms, type(self.rooms))

        self.room_schema = RoomSchema()
        self.user_schema = UserSchema()

    @property
    def username(self):
        # Return this User from db
        return self._username
        # try:
        #     return db.find({'username': self._username})
        # except Exception as err:
        #     print('Users GET find err', err)
        #     return False

    @username.setter
    def username(self, new_name):
        '''Update username in DB
        '''
        pass
        # self._username = new_name

    def delete_user(self):
        '''Delete self from DB.
        '''
        return db.delete({"username": self._username}) == 1

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        '''Set/Update password in DB.
        Use set_password() below to initial create the password
        '''
        self._password = generate_password_hash(new_password)

    def add_room(self, name, stuff):
        ''' A wrapper for RoomDB's constructor
        @param name: str
        @param stuff: dict
        '''
        room = None
        print("add room stuff", stuff)
        stuff = dict() if stuff is None else stuff
        room = RoomDB(name, self._username, stuff)

        print(room)

        # Dump rooms for db to handle
        room = self.room_schema.dump(room)
        print('room added, adding to db', room)
        return db.update({'username': self._username},
                         {"$push": {
                             "rooms": room
                         }})

    def remove_room(self, room=None):
        '''Delete room(s) from DB.

        @param room: name(s) of room to delete
        '''
        if room is None:
            # Delete all rooms
            db.update({"username": self._username}, {"$set": {"rooms": []}})
        elif isinstance(room, list):
            # delete these rooms
            pass
            # db.update({"username": self._username}, {"$set": {"rooms": []}})
        else:
            try:
                # only delete this room
                # Because of $pull, all rooms with this name will be deleted.
                # Client should take care of enforcing unique names.
                db.update({"username": self._username},
                          {"$pull": {
                              "rooms": {
                                  "name": room
                              }
                          }})
            except Exception as err:
                print('could not deletee room ' + room)
                return False

        return True

    def put_stuff_in_room(self, _room, stuff):
        ''' 
        @param name: str
        @param stuff: dict
        '''
        # Find room list item to put stuff in.
        rm = [r for r in self.rooms if r.name == _room][0]
        rm.update_stuff(stuff)

    @classmethod
    def find_user(cls, username):
        usr = db.find({'username': username})
        print('usr found:', usr)
        if usr:
            return UserSchema().load(usr)
        return None

    def check_password(self, password):
        # print('checking {} to {} or {}'.format(
        #     self.password, password, generate_password_hash(password)))
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f'<UserDB {self._username}>'


class RoomDB(object):
    '''A RoomDB provides deeper DB access to CRUD rooms directly 
    '''
    def __init__(self, name, owner=None, stuff=dict()):
        # stuff: A dict of items: {item: price}
        # owner: not used in DB
        self._name = name
        self.owner = owner
        self.stuff = stuff

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self):
        '''Update name of Room in DB.
        '''
        # Mongo does not support rename on embedded doc
        # in array.
        # Use $set

        # curr_room_stuff = db.find({"username": url_args.get('owner')},
        #                           projection={
        #                               "_id": 1,
        #                               "rooms": {
        #                                   "$elemMatch": {
        #                                       "name":
        #                                       url_args.get('room_name_old')
        #                                   }
        #                               }
        #                           })["rooms"][0]
        curr_room_stuff = self.stuff
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

    def update_stuff(self, changes):
        '''Add/Update stuff for this room in DB.
        @param changes: dict mapping old items to new.

        {
            "item": {
                "name": "item_name",
                "value": "item_value"
            },
        }
        name or value may not be present
        '''
        selector = {"username": self.owner, "rooms.name": self._name}

        # Build cmd based on requested changes
        set_cmd = {"$set": dict()}
        unset_cmd = {"$unset": dict()}
        arr_filter = [{"element.name": self._name}]
        print("current stuff: ", self.stuff)

        for key, change in changes.items():
            # print(f"key: {key}, change: {change}")
            # otherwise, a new item
            if change.get("name") and change.get("value"):
                # Set, or possibly replace, item.
                if key in self.stuff.keys():
                    # Remove current item
                    unset_cmd["$unset"]["rooms.$[element]" + ".stuff." +
                                        key] = ""

                set_cmd["$set"]["rooms.$[element]" + ".stuff." +
                                change["name"]] = change["value"]
            elif change.get("name"):
                # Update item name.
                set_cmd["$set"]["rooms.$[element]" + ".stuff." +
                                change["name"]] = self.rooms[key]
            elif change.get("value"):
                # Update item value.
                set_cmd["$set"]["rooms.$[element]" + ".stuff." +
                                self.stuff[key]] = change["value"]

        # print("unset_cmd", unset_cmd)
        # print("set_cmd", set_cmd)
        # print("selector", selector)
        update_cmd = set_cmd
        if len(unset_cmd["$unset"]) > 0:
            update_cmd["$unset"] = unset_cmd["$unset"]
        # print("update_cmd", update_cmd)

        return db.update(selector, update_cmd, array_filters=arr_filter)

    def remove_stuff(self, items=None):
        '''Remove items from stuff in this room in DB.

        @param items: List of names to delete
                      None: Delete all stuff
        '''
        if items:
            # Array of item(s) to delete
            update_cmd = {"$unset": dict()}
            for item in items:
                update_cmd["$unset"]["rooms.$[element].stuff." + item] = ""
            print("del stuff update cmd", update_cmd)
            db.update({"username": self.owner},
                      update_cmd,
                      array_filters=[{
                          "element.name": self._name
                      }])
        else:
            # Delete all stuff
            db.update({"username": self.owner},
                      {"$set": {
                          "rooms.$[element].stuff": {}
                      }},
                      array_filters=[{
                          "element.name": self._name
                      }])

    def __repr__(self):
        return f'<RoomDB {self.name} has {len(self.stuff)} stuff.>'


class RoomSchema(Schema):
    name = fields.Str(required=True)
    stuff = fields.Dict(keys=fields.Str(),
                        values=fields.Str(),
                        allow_none=True)

    @post_load
    def make_room(self, data, **kwargs):
        print('loading room into Class', data, kwargs)
        return RoomDB(**data)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str()
    rooms = fields.List(fields.Nested(RoomSchema), allow_none=True)

    @post_load
    def make_user(self, data, **kwargs):
        print('loading user into Class', data, kwargs)
        return UserDB(**data)

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