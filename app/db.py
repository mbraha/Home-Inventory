from pymongo import MongoClient, DESCENDING
from flask import current_app, g
from werkzeug.local import LocalProxy


class MongoDB(object):
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGO_URI'])
        self.db = self.client.home_inventory_db['user_collection']

        # Set index to enforce uniquness
        self.db.create_index([('username', DESCENDING)], unique=True)

    def find_all(self, selector):
        return self.db.find(selector)

    def find(self, selector):
        return self.db.find_one(selector)

    def create(self, document):
        return self.db.insert_one(document)

    def update(self, selector, document):
        return self.db.replace_one(selector, document).modified_count

    def delete(self, selector):
        return self.db.delete_one(selector).deleted_count

    def reset(self):
        self.db.drop()


def get_db():
    if 'db' not in g:
        g.db = MongoDB()

    return g.db


db = LocalProxy(get_db)