from flask import Blueprint


bp = Blueprint('views', __name__)


from app.view import user_views, home_views