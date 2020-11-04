from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from com_dayoung_api.ext.db import url, db
from com_dayoung_api.ext.routes import initialize_routes

from com_dayoung_api.item.api import Item, Items
# from com_dayoung_api.movie.api import Movie, Movies
# from com_dayoung_api.review.api import Review, Reviews
from com_dayoung_api.resources.review import Review, Reviews, ReviewDao
from com_dayoung_api.resources.movie import MovieDao
from com_dayoung_api.actor.api import Actor, Actors
from com_dayoung_api.user.dao import UserDao


print('========== 1 ==========')
app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
with app.app_context():
    db.create_all()
with app.app_context():
    print("진입 1")
    review_count = ReviewDao.count()
    review_group_by = ReviewDao.group_by()
    # user_id = 8425305
    # review_user_by = ReviewDao.find_by_user_id(user_id)
    user_count = UserDao.count()
    movie_count = MovieDao.count()
    print("진입 2") 
    # print(movie_count)
    print(f'>>>>>>>>> Review Total Count is {review_count}')
    if review_count == 0:
        ReviewDao.insert_many()
        print(f'>>>>>>>>> Review Total Count is {review_count}')
    # print('#' * 30)
    # print(f'Review Group by : {review_group_by}')
    # print('#' * 30)
    # print('#' * 30)
    # print(f'Review of {user_id} : {review_user_by}')
    # print('#' * 30)
    print(f'>>>>>>>>> User Total Count is {user_count}')
    if user_count == 0:
        UserDao.insert_many()
        print(f'>>>>>>>>> User Total Count Now {user_count}')
    print(f'>>>>>>>>> Movie Total Count is {movie_count}')
    if movie_count == 0:
        MovieDao.insert_many()
        print(f'>>>>>>>>> User Total Count Now {user_count}')

initialize_routes(api)