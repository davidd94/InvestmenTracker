from app import create_app
from config import Config
from app.model.stocks import Stocks

from flask import Flask
from random import randint
from pymongo import MongoClient
import unittest, hashlib, os

client = MongoClient()

class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.0:27017'

class UserDocModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up stock data test...')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.db = client.InvestmenTracker['test_stocks']
        self.test_users = [
            {'username': 'Daviepoo', 'email': 'random1@gg.com'},
            {'username': 'Bert', 'email': 'random2@gg.com'},
            {'username': 'Wambulance', 'email': 'random3@gg.com'}
        ]
        self.test_stocks = [
            {
            'StockTicker': 'AAPL', 
            'StockData': {
                'date': '01/05/2020',
                'purchase': 297.43,
                'qty': 5,
                'notes': 'bought it during its highs'}
            },
            {
            'StockTicker': 'VOO',
            'StockData': {
                'date': '09/20/2019',
                'purchase': 263.33,
                'qty': 11,
                'notes': 'bought it during its rise. lowest 245'}
            },
            {
            'StockTicker': 'AMZN',
            'StockData': {
                'date': '11/23/2019',
                'purchase': 1923.22,
                'qty': 2,
                'notes': 'banking on autonomous trucks'}
            },
            {
            'StockTicker': 'KO',
            'StockData': {
                'date': '02/02/2019',
                'purchase': 48.98,
                'qty': 25,
                'notes': ''}
            },
            {
            'StockTicker': 'JNJ',
            'StockData': {
                'date': '01/02/2020',
                'purchase': 54.30,
                'qty': 40,
                'notes': 'good dividend investment of 3%'}
            },
            {
            'StockTicker': 'BTC-USD',
            'StockData': {
                'date': '01/20/2019',
                'purchase': 9200,
                'qty': 2,
                'notes': 'still hoping to hit millions..'}
            },
            {
            'StockTicker': 'MMM',
            'StockData': {
                'date': '04/20/2019',
                'purchase': 155.21,
                'qty': 55,
                'notes': 'excellent dividend yields of 3%'}
            },
            {
            'StockTicker': 'GOOG',
            'StockData': {
                'date': '03/03/2018',
                'purchase': 1199,
                'qty': 3,
                'notes': 'google..'}
            },
            {
            'StockTicker': 'COST',
            'StockData': {
                'date': '07/30/2019',
                'purchase': 279.21,
                'qty': 7,
                'notes': 'costco'}
            },
            {
            'StockTicker': 'AMD',
            'StockData': {
                'date': '10/20/2019',
                'purchase': 48.60,
                'qty': 20,
                'notes': 'AMD CPUs'}
            },
        ]
        self.app_context.push()
        Stocks.connect(True)
    
    def tearDown(self):
        print('tearing down tests...')
        self.db.drop()
        self.app_context.pop()
        Stocks.disconnect()

    def create_user(self):
        new_user = new_user = Stocks(username=self.test_users[0]['username'],
                            email=self.test_users[0]['email'],
                            stocks=[
                                self.test_stocks[0],
                                self.test_stocks[4], 
                                self.test_stocks[7]
                            ])
        
        new_user.switch_collection('test_stocks')
        new_user.save()

        return new_user

    def create_random_user(self):
        user_number = len(self.test_users) - 1

        new_random_user = Stocks(username=self.test_users[randint(1, user_number)]['username'],
                        email=self.test_users[randint(1, user_number)]['email'],
                        stocks=[
                            self.test_stocks[randint(0,3)],
                            self.test_stocks[randint(4,6)],
                            self.test_stocks[randint(7,9)]
                        ])
        
        new_random_user.switch_collection('test_stocks')
        new_random_user.save()

        return new_random_user

    def test_add_user_stocks(self):
        new_user = self.create_user()
        find_user = self.db.find_one({'username': new_user.username})
        
        # test if default users and stocks have been added
        self.assertEqual(find_user['username'], new_user.username)
        self.assertEqual(find_user['stocks'], new_user.stocks)
        self.assertEqual(find_user['stocks'][0]['StockTicker'], new_user.stocks[0]['StockTicker'])

        # mock-post data incoming to add
        add_stock = self.test_stocks[1]
        add_stock2 = self.test_stocks[2]
        add_stock3 = self.test_stocks[5]
        add_stock4 = self.test_stocks[6]
        existing_stock = new_user.stocks[0]
        existing_stock2 = new_user.stocks[1]
        
        # check to see if stocks are in DB, if not proceed to add to DB
        existing_user_stock = self.db.find_one({'username': new_user.username,
                                                'stocks.StockTicker': add_stock['StockTicker']})
        existing_user_stock2 = Stocks.objects(username=new_user.username,
                                                stocks__StockTicker=add_stock2['StockTicker']).first()
        
        self.assertIsNone(existing_user_stock)
        self.assertIsNone(existing_user_stock2)

        # insert new stocks for existing users using two DOM methods (mongoDB and mongoengine)
        add_stock_list = [add_stock, add_stock2]
        for each_stock in add_stock_list:
            # checks if stock is already in users profile
            find_existing_stock = self.db.find_one({'username': new_user.username,
                                                    'stocks.StockTicker': each_stock['StockTicker']})
            # adds if doesn't exists else it should return an error in production code
            if find_existing_stock is None:
                self.db.find_one_and_update({'username': new_user.username},
                                                        {'$push': 
                                                            {'stocks': 
                                                                {'$each': [each_stock]}
                                                            }
                                                        })
        new_user.update(push_all__stocks=[add_stock, add_stock4])
        #new_user.update(**{'push_all__stocks': [add_stock3, add_stock4]})

        # find user via using two DOM methods (mongoDB and mongoengine)
        find_stock = self.db.find_one({'username': new_user.username, 'stocks.StockTicker': add_stock['StockTicker']})

        # test if users can be found using recently added stock data
        self.assertIsNotNone(find_stock)
        # test if sum len stocks is correct after adding new stocks
        self.assertEqual(len(find_stock['stocks']), 7)
        # test if each individually added stocks were actuall added
        self.assertEqual(find_stock['stocks'][6], add_stock4)
        self.assertEqual(find_stock['stocks'][4], add_stock2)

    def test_find_users_and_stocks(self):
        new_user = self.create_user()
        new_user2 = self.create_random_user()
        # stocks
        add_stock = self.test_stocks[1]
        add_stock2 = self.test_stocks[2]
        add_stock3 = self.test_stocks[5]
        add_stock4 = self.test_stocks[6]
        # adding stocks
        new_user.update(push_all__stocks=[add_stock, add_stock2, add_stock3, add_stock4])
        new_user2.update(push_all__stocks=[add_stock, add_stock4])

        # test if we can find user stock info by username
        find_userstocks = self.db.find_one({'username': new_user.username})
        self.assertEqual(new_user.username, find_userstocks['username'])

        # test if we can find all users stock info by stock ticker
        find_all_users_len = self.db.count_documents({'stocks.StockTicker': add_stock['StockTicker']})
        self.assertEqual(find_all_users_len, 2)

    def test_delete_stocks(self):
        new_user = self.create_user()
        stock_to_delete = self.test_stocks[0]['StockTicker']

        self.db.find_one_and_update({'username': new_user.username,
                                    'stocks.StockTicker': stock_to_delete},
                                        {'$pull': 
                                            {'stocks': {'StockTicker': stock_to_delete}}
                                        }
                                    )

        saved_user = self.db.find_one({'username': new_user.username})
        saved_stock = self.db.find_one({'username': new_user.username,
                                        'stocks.StockTicker': self.test_stocks[4]['StockTicker']})
        # two ways to delete stock using mongoDB and mongoengine
        deleted_stock = self.db.find_one({'username': new_user.username,
                                        'stocks.StockTicker': self.test_stocks[0]['StockTicker']})
        """deleted_stock = new_user.update(pull__stocks__StockTicker=self.test_stocks[0]['StockTicker'])
        new_user.reload()"""

        self.assertIsNotNone(saved_user)
        self.assertIsNotNone(saved_stock)
        self.assertIsNone(deleted_stock)
        #self.assertEqual(deleted_stock, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)