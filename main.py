from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes

from com_dayoung_api.item.api import Item, Items
from com_dayoung_api.movie.api import Movie, Movies
# from com_dayoung_api.review.api import Review, Reviews
from com_dayoung_api.resources.review import Review, Reviews
from com_dayoung_api.actor.api import Actor, Actors
from com_dayoung_api.user import user


print('========== 1 ==========')
app = Flask(__name__)
CORS(app)
app.register_blueprint(user)


print(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
# @app.before_first_request
# def create_tables():
#     db.create_all()
initialize_routes(api)
