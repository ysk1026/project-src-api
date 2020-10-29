from com_dayoung_api.home.api import Home
from com_dayoung_api.movie.api import Movie, Movies
from flask import Blueprint
from flask_restful import Api
# from com_dayoung_api.review.api import Review, Reviews
from com_dayoung_api.resources.review import Review, Reviews
from com_dayoung_api.actor.api import Actor, Actors
from com_dayoung_api.user.api import User, Users, Auth, Access
from com_dayoung_api.item.api import Item, Items

home = Blueprint('home', __name__, url_prefix='/api')
user = Blueprint('user', __name__, url_prefix='/api/user')
users = Blueprint('users', __name__, url_prefix='/api/users')
auth = Blueprint('auth', __name__, url_prefix='/api/auth')
access = Blueprint('access', __name__, url_prefix='/api/access')
review = Blueprint('review', __name__, url_prefix='/api/review')
reviews = Blueprint('review', __name__, url_prefix='/api/reviews')

api = Api(home)
api = Api(user)
api = Api(users)
api = Api(auth)
api = Api(access)
api = Api(review)
api = Api(reviews)

def initialize_routes(api):
    
    api.add_resource(Home, '/api')
    api.add_resource(Movie, '/Movie/<string:id>')
    api.add_resource(Movies, '/Movies')
    print('========== 2 ==========')
    api.add_resource(Review, '/api/review<string:id>')
    api.add_resource(Reviews, '/api/reviews')
    api.add_resource(Actor, '/Actor<string:id>')
    api.add_resource(Actors, '/Actors')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/api/access')
    api.add_resource(Item, '/api/item/<string:id>')
    api.add_resource(Items,'/api/items')

