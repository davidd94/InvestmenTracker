from mongoengine import Document, StringField, connect, disconnect, ValidationError
import os


class FeedbackModel(Document):
    meta = {'collection': 'Feedback'}
    email = StringField(required=True, max_length=50)
    firstname = StringField(max_length=50)
    feedback = StringField(max_length=500)
    
    def validate_self(self):
        try:
            self.validate()
        except ValidationError as e:
            return e.errors

    @classmethod
    def connect(cls, test=False):
        if test is False:
            connect(db='InvestmenTracker', host=os.environ.get('MONGO_URI'))
        else:
            connect('InvestmenTracker')

    @classmethod
    def disconnect(cls):
        disconnect()