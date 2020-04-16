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

    def find_all(self, selector, projection=None, collection="users"):
        return self.db[collection].find(
            selector,
            projection=None,
        )

    def find(self, selector, projection=None, collection="users"):
        print('looking for ', selector)
        return self.db[collection].find_one(selector, projection=projection)

    def create(self, document, collection="users"):
        return self.db[collection].insert_one(document)

    def update(self, selector, update, array_filters=None, collection="users"):
        res = None
        try:
            res = self.db[collection].find_one_and_update(
                selector, update, array_filters=array_filters)
            print('db update res', res)
        except Exception as err:
            print('db update error', err)

        return res

    def delete(self, selector, collection="users"):
        return self.db[collection].delete_one(selector).deleted_count

    def drop(self, collection="users"):
        self.db[collection].drop()


def get_db():
    if 'db' not in g:
        g.db = MongoDB()

    return g.db


db = LocalProxy(get_db)