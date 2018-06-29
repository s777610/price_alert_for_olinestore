import uuid

import datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item
from src.models.stores.store import Store


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, store=None, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = float(price_limit)
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active
        store = Store.find_by_url(self.item.url)
        self.store = store.name

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    """
    The (navigate to alert) is going to be running from alert_updater, 
    not from app.py, the alert_updater doesn't know the endpoint, 
    doesn't know the methods which are associated with them,
    so we can not use url_for in here,
    because it is not going to be running through flask application
    """
    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={"from": AlertConstants.FROM,
                  "to": [self.user_email],
                  "subject": "Price limit reached for {}".format(self.item.name),
                  "text": "We have found a deal! ({}). To navigate to the alert, visit {}".format(
                    self.item.url, "https://priceing-alerts.herokuapp.com/alerts/{}".format(self._id))})




    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)  # 10 minutes
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit},  # gte = greater than or equal to
                                                       "active": True  # just check the active alerts
                                                       })]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active,
            "store": self.store
        }

    def load_item_price(self):
        """loading the price, and update the last checked time"""
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()  # save the alert to mongodb
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):  # To find a list of all alerts for specific user, return many alert object
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user_email": user_email})]

    @classmethod
    def find_by_id(cls, alert_id):  # To find one alert for specific user, return an alert object
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))


    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})


