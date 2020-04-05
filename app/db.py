from pymongo import MongoClient, DESCENDING
from flask import current_app, g
from werkzeug.local import LocalProxy


class MongoDB(object):
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client.home_inventory_db

        # Set index to enforce uniquness
        self.db['users'].create_index([('username', DESCENDING)], unique=True)

        print('created DB instance')

    def find_all(self, selector, collection="users"):
        return self.db[collection].find(selector)

    def find(self, selector, projection=None, collection="users"):
        print('looking for ', selector)
        return self.db[collection].find_one(selector, projection=projection)

    def create(self, document, collection="users"):
        return self.db[collection].insert_one(document)

    def update(self, selector, update, collection="users"):
        try:
            res = self.db[collection].update_one(selector, update)
            print('db update res', res)
        except Exception as err:
            print('db update error', err)

        return res.matched_count

    def delete(self, selector, collection="users"):
        return self.db[collection].delete_one(selector).deleted_count

    def reset(self, collection="users"):
        self.db[collection].drop()


def get_db():
    if 'db' not in g:
        g.db = MongoDB()

    return g.db


db = LocalProxy(get_db)