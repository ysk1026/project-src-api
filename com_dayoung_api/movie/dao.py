from com_dayoung_api.ext.db import db

class MovieDao:
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, movie_name):
        return cls.query.filter_by(movie_name == movie_name).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id == id).first
