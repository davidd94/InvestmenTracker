from app import create_app
from config import Config
from pymongo import MongoClient
from mongoengine import ValidationError
from random import randint
from app.model.feedback import FeedbackModel
from app.model.email import send_email
import unittest, os


client = MongoClient()


class TestConfig(Config):
    #TESTING = True
    MONGO_URI = 'mongodb://127.0.0.0:27017'

class FeedbackModelCase(unittest.TestCase):
    def setUp(self):
        print('setting up feedback test...')
        self.app = create_app(TestConfig)
        self.test_users = [
            {'username': 'Daviepoo', 'firstname': 'Davie', 'lastname': 'poo', 'email': 'random1@gg.com'},
            {'username': 'Bert', 'firstname': 'Gilbert', 'lastname': 'Quemuel', 'email': 'random2@gg.com'},
            {'username': 'Wambulance', 'firstname': 'Dennisfdjfjfjdjfjdjsfjdfafahafjfhufufhwuehufewhfuwefhiwefwiefuhfhuefhuifwhweif', 'lastname': 'Menace', 'email': 'random3@gg.com'},
            {'username': 'Puth', 'firstname': 'Charlie', 'lastname': 'Ice', 'email': 'random4@gg.com'},
            {'username': 'Lee', 'firstname': 'Robert', 'lastname': 'Cream', 'email': 'random5@gg.com'},
            {'username': 'Huawei', 'firstname': 'uwefhiwefwiefuhfhuefhuifwhweifffdsfdaffffdjfksjflfjkdsfjdsffjslkfjsfdskfieiiieieieieiei', 'lastname': 'Seems', 'email': 'random6@gg.com'},
            {'username': 'Biden', 'firstname': 'Joe', 'lastname': 'Lean', 'email': 'random7@gg.com'},
            {'username': 'Kim', 'firstname': 'Jin', 'lastname': 'Gleam', 'email': 'random8@gg.com'}
            ]
        self.random_comments = [
            'hello... i love your stock web app!',
            'does this website even work???',
            'I havent seen updates in forever!!!',
            'yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow \
                bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow \
                mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow \
                yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow \
                bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow \
                mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow \
                yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow \
                bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow \
                mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow \
                yellow bellow mellow yellow bellow mellow yellow bellow mellow yellow bellow mellow ',
            'what is dirt + ice? dice...',
            'good day to you sir!',
            'happy new years!!!',
            'spending the new years just coding'
        ]
        self.db = client.InvestmenTracker['Feedback']
        self.errors = None
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        self.db.drop()

    def test_feedback(self):
        failed_validations = []
        FeedbackModel.connect(True)

        # attempt to add feedback comments to DB
        for i in range(0, len(self.test_users)):
            user_email = self.test_users[i]['email']
            user_firstname = self.test_users[i]['firstname']
            user_feedback = self.random_comments[i]
            feedback = FeedbackModel(email=user_email,
                                        firstname=user_firstname,
                                        feedback=user_feedback)
            
            validation_errors = feedback.validate_self()
            if validation_errors:
                user_error = {}
                user_error[user_email] = validation_errors
                failed_validations.append(user_error)
            else:
                feedback.save()

        # Test validation errors (not being saved to DB)
        for dictionary in failed_validations:
            for key, value in dictionary.items():
                email = key
                error = str(value)

                user = FeedbackModel.objects(email=email).first()
                self.assertIsNone(user)
        
        # find user if feedback passes validations
        user1 = FeedbackModel.objects(email=self.test_users[0]['email']).first()
        user2 = FeedbackModel.objects(email=self.test_users[7]['email']).first()
        
        # test email functions
        subject = f'InvestmenTracker Feedback from {user1.email}'
        sender = self.app.config['MAIL_USERNAME']
        recipient = self.app.config['MAIL_USERNAME']
        
        send_email(subject, sender, recipient, email_type='feedback', app=self.app,
                    firstname=user1.firstname,
                    email=user1.email,
                    feedback=user1.feedback)

        self.assertIsInstance(user1, FeedbackModel)
        self.assertIsInstance(user2, FeedbackModel)


if __name__ == "__main__":
    unittest.main(verbosity=2)