import os
import pymongo

class Database(object):

    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None

    @staticmethod  # not using self
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data) #data=json

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query) #query={dict}

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)  # upsert: if we can find element by query, insert it

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)