from app import create_app
from config import Config
from app.model.users import User
from app.model.recaptcha import google_recaptchaV2
from app.model.token import generate_token, verify_token

from flask import testing, session
from pymongo import MongoClient
from random import randint
import unittest, time


client = MongoClient()


class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.0:27017'

class UserAuthModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up user auth tests...')
        self.app = create_app(Config)
        self.app_context = self.app.app_context()
        self.db = client.InvestmenTracker['test_users']
        self.test_users = [
            {'username': 'Daviepoo', 'firstname': 'Davie', 'lastname': 'poo', 'email': 'random1@gg.com', 'password': 'pass1'},
            {'username': 'Bert', 'firstname': 'Gilbert', 'lastname': 'Quemuel', 'email': 'random2@gg.com', 'password': 'pass2'},
            {'username': 'Wambulance', 'firstname': 'Dennis', 'lastname': 'Menace', 'email': 'random3@gg.com', 'password': 'pass3'}
            ]
        self.app_context.push()
        User.connect(True) # connects to MongoDB
    
    def tearDown(self):
        print('tearing down tests...')
        self.db.drop()
        self.app_context.pop()
        User.disconnect() # disconnects from MongoDB

    def create_user(self):
        hash_password = User.hash_password(self.test_users[0]['password'])
        new_user = new_user = User(username=self.test_users[0]['username'],
                            firstname=self.test_users[0]['firstname'],
                            lastname=self.test_users[0]['lastname'],
                            email=self.test_users[0]['email'],
                            password=hash_password)
        
        new_user.switch_collection('test_users')
        new_user.save()

        return new_user

    def create_random_user(self):
        user_number = len(self.test_users) - 1
        hash_password = User.hash_password(self.test_users[randint(0, user_number)]['password'])

        new_random_user = User(username=self.test_users[randint(0, user_number)]['username'],
                        firstname=self.test_users[randint(0, user_number)]['firstname'],
                        lastname=self.test_users[randint(0, user_number)]['lastname'],
                        email=self.test_users[randint(0, user_number)]['email'],
                        password=hash_password)
        
        new_random_user.switch_collection('test_users')
        new_random_user.save()

        return new_random_user

    def test_user_login(self):
        # create new user
        new_user = self.create_user()
        hash_password = new_user['password']
        updated_user = None
        
        # retreive user data to compare hash passwords
        user = self.db.find_one({'username': new_user.username})
        hash_login_password = user['password']
        
        # test acct confirmation status
        new_user.update(acct_status=True)
        new_user.reload()
        updated_user = self.db.find_one({'username': new_user.username})
        
        self.assertFalse(user['acct_status']) # dict isnt updated so acct_status stays False
        self.assertTrue(updated_user['acct_status'])
        self.assertEqual(hash_login_password, hash_password, updated_user['password'])

        # test google reCaptcha API
        google_response = google_recaptchaV2(test=True)
        
        self.assertEqual(google_response['hostname'], 'testkey.google.com')
        self.assertTrue(google_response['success'])
        
        # test flask-session records
        with self.app.test_request_context(): # need to push/create a request context to use sessions
            session['username'] = updated_user['username']
            session['email'] = updated_user['email']
        
            self.assertEqual(session['username'], updated_user['username'])
            self.assertEqual(session['email'], updated_user['email'])

    def test_user_failed_logins(self):
        user = self.create_user()
        # test failed login attempts
        for i in range(0, 10):
            user['failed_login'] += 1
            user.save()
            self.assertLessEqual(user['failed_login'], 10)
        
        updated_user = self.db.find_one({'username': user.username})
        self.assertLessEqual(updated_user['failed_login'], 10)

    def test_acct_confirm(self):
        user = self.create_random_user()
        email_salt = 'email-confirm'
        token_from_get_request = generate_token(user.email, email_salt)
        email = verify_token(token_from_get_request, 100, email_salt)
        
        if email:
            self.assertFalse(user.acct_status)
            user.update(acct_status=True)
            user.reload()
            self.assertTrue(user.acct_status)

        self.assertEqual(user.email, email)
        self.assertIsNotNone(email)

    def test_acct_confirm_renewal(self):
        user = self.create_random_user()
        email = None
        email_salt = 'email-confirm'
        token_from_get_request = generate_token(user.email, email_salt)
        time.sleep(1)
        try:
            # expired token will raise an error
            email = verify_token(token_from_get_request, age=0, salt=email_salt)
        except:
            # creates a new token
            new_token = generate_token(user.email, email_salt)
            user['token'] = new_token
            user.save()
            # valid new token will return an email
            email = verify_token(new_token, age=10, salt=email_salt)

        if email:
            find_user = self.db.find_one({'email': email})
            
            self.assertIsNotNone(find_user)
            self.assertEqual(new_token, find_user['token'])
            self.assertFalse(find_user['acct_status'], user.acct_status)
            user.update(acct_status=True)
            user.reload()
            self.assertTrue(user.acct_status)

    def test_pass_reset_request(self):
        user = self.create_random_user()
        email_salt = 'password-reset'
        token_from_get_request = generate_token(user.email, email_salt)
        email = verify_token(token_from_get_request, 100, email_salt)
        
        self.assertIsNotNone(email)

    def test_pass_reset(self):
        user = self.create_random_user()
        incoming_post_data = {
            'username': user.username,
            'newpassword': 'newpass123'
        }

        new_hash_password = user.hash_password(incoming_post_data['newpassword'])

        # check to see if new password does not match old one, if it does return an error
        self.assertNotEqual(user.password, new_hash_password)

        if new_hash_password != user.password:
            user.update(password=new_hash_password)
            user.reload()

            self.assertEqual(user.password, new_hash_password)
        

if __name__ == "__main__":
    unittest.main(verbosity=2)