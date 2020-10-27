from typing import List
from flask_restful import Resource, reqparse
from com_dayoung_api.movie.dto import MovieDto
from com_dayoung_api.movie.dao import MovieDao

class Movie(Resource):
    def __init__(self):
        pass

class Movies(Resource):
    ...