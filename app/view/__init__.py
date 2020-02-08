from flask import Blueprint


bp = Blueprint('views', __name__)


from app.view import home_views, user_views, user_stock_views