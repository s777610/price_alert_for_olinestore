import uuid

import requests
from bs4 import BeautifulSoup
import re
from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        # for same store, the tag_name and query are same
        # Amazon: <span id="priceblock_ourprice" class="a-size-medium a-color-price">$83.95</span>

        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)  # span = tag_name in Amazon, query is dict in python
        string_price = element.text.strip()

        pattern = re.compile("(\d.\d+)")  # () is able to match $115.00
        match = pattern.search(string_price)
        self.price = float(match.group())  # updating price whenever we load this price

        return self.price

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())  # ItemConstants = items

    def json(self):
        return{
            "_id": self._id,
            "name": self.name,
            "url": self.url
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))

