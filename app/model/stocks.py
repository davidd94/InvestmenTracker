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