from com_dayoung_api.home.api import Home
from com_dayoung_api.movie.api import Movie, Movies
# from com_dayoung_api.review.api import Review, Reviews
from com_dayoung_api.resources.review import Review, Reviews
from com_dayoung_api.actor.api import Actor, Actors
from com_dayoung_api.user.api import User, Users, Auth, Access
from com_dayoung_api.item.api import Item, Items

def initialize_routes(api):
    print('========== 2 ==========')
    api.add_resource(Home, '/api')
    api.add_resource(Movie, '/Movie/<string:id>')
    api.add_resource(Movies, '/Movies')
    api.add_resource(Review, '/Review<string:id>')
    api.add_resource(Reviews, '/api/reviews')
    api.add_resource(Actor, '/Actor<string:id>')
    api.add_resource(Actors, '/Actors')
    api.add_resource(User, '/api/user/<string:id>')
    api.add_resource(Users, '/api/users')
    api.add_resource(Auth, '/api/auth')
    api.add_resource(Access, '/api/access')
    api.add_resource(Item, '/api/item/<string:id>')
    api.add_resource(Items,'/api/items')

