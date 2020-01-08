import os, sys
from config import Config

from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_recaptcha import ReCaptcha


mongo = PyMongo()
recaptcha = ReCaptcha()
mail = Mail()


""" App Factory """
def create_app(config_class=Config):
    app = Flask(__name__)

    # Loads the config file
    app.config.from_object(config_class)
    
    mongo.init_app(app)
    recaptcha.init_app(app)
    mail.init_app(app)
    
    #from all_func import bp as tempfunc
    from app.model import bp as modelbp
    from app.controller import bp as controllerbp
    from app.view import bp as viewbp

    #app.register_blueprint(tempfunc)
    app.register_blueprint(modelbp)
    app.register_blueprint(controllerbp)
    app.register_blueprint(viewbp)

    return app