from app import mongo
from pymongo import MongoClient
from mongoengine import Document, DynamicDocument, StringField, ListField, DictField, ValidationError, \
                        connect, disconnect
import os, hashlib, string, random


class Stocks(Document):
    meta = {'collection': 'Stocks'}
    username = StringField(required=True, max_length=30, unique=True)
    email = StringField(required=True, max_length=50, unique=True)
    stocks = ListField(db_field='stocks')

    @classmethod
    def connect(cls, test=False):
        if test is False:
            connect('InvestmenTracker', host=os.environ.get('MONGO_URI'))
        else:
            connect('InvestmenTracker')

    @classmethod
    def disconnect(cls):
        disconnect()

    @staticmethod
    def get_userstocks_by_username(username, test=False):
        Stocks.connect(test=test)
        user_stocks = Stocks.objects(username=username).first()
        return user_stocks if user_stocks else None

    @staticmethod
    def get_users_by_stockticker(stockticker, test=False):
        Stocks.connect(test=test)
        users = Stocks.objects(stocks__StockTicker=stockticker)
        return users if users else None