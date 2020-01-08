from flask import Blueprint


bp = Blueprint('model', __name__)


from app.model import users, stocks, email, feedback, token, recaptcha