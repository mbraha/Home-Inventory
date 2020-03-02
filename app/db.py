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

    def find_all(self, selector, collection):
        return self.db[collection].find(selector)

    def find(self, selector, collection):
        return self.db[collection].find_one(selector)

    def create(self, document, collection):
        return self.db[collection].insert_one(document)

    def update(self, selector, document, collection):
        return self.db[collection].replace_one(selector,
                                               document).modified_count

    def delete(self, selector, collection):
        return self.db[collection].delete_one(selector).deleted_count

    def reset(self, collection):
        self.db[collection].drop()


def get_db():
    if 'db' not in g:
        g.db = MongoDB()

    return g.db


db = LocalProxy(get_db)