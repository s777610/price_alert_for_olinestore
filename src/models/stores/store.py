import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        h -> ?
        ht -> ?
        ...
        http://www.target -> http://www.target.com -> Store("Target")
        http://www,target -> {'_id': ...,'name': 'target'...}
        :param url_prefix:
        :return:
        """
        #  http: // www.target -> http: // www.target.com
        #  http: // www, target -> {'_id': ..., 'name': 'target'...}
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    """
    Return a store from a url like "http://www.target.com/item/sdjf2.html"
    :param url: The item's URL
    :return: a Store, or raise a StoreNoFoundException if no store matchs the URL
    """

    @classmethod
    def find_by_url(cls, url):
        for i in range(len(url) - 1, - 1, -1):
            try:
                if Database.find_one(StoreConstants.COLLECTION,
                                    {'url_prefix': {"$regex": '^{}'.format(url[:i])}}) is not None:
                    store = cls.get_by_url_prefix(url[:i])
                    return store
            except:
                raise StoreErrors.StoreNotFoundException(
                    "The URL Prefix used to find the store did not fetch any resutls")


    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})
