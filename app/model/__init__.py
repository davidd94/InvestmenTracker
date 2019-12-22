from flask import Blueprint


bp = Blueprint('models', __name__)


from app.model import users