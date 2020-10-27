from com_dayoung_api.ext.db import db
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from com_dayoung_api.movie.search import NaverMovie
import pandas as pd
from com_dayoung_api.utils.file_helper import FileReader

# config = {
#     'user' : 'root',
#     'password' : 'root',
#     'host': '127.0.0.1',
#     'port' : '3306',
#     'database' : 'dayoungdb'
# }
# charset = {'utf8':'utf8'}
# url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
# engine = create_engine(url)

class MovieDto(db.Model):
    
    __tablename__ = 'movies'
    __table_args__= {'mysql_collate':'utf8_general_ci'}

    # ,id,title,subtitle,description,imageurl,year,rating
    movieid : str = db.Column(db.String(10), primary_key = True, index = True)
    title : str = db.Column(db.String(30))
    subtitle : str = db.Column(db.String(30))
    description : str = db.Column(db.String(200))
    imageurl : str = db.Column(db.String(100))
    year : str = db.Column(db.String(5))
    rating : float = db.Column(db.Float)

    def __init__(self,movieid,title,subtitle,description,imageurl,year,rating):
        self.movieid = movieid
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.imageurl = imageurl
        self.year = year
        self.rating = rating

    # def __repr__(self):
    #     return f'Movie(movieid=\'{self.movieid}\',\
    #         title=\'{self.title}\',\
    #         genre=\'{self.genre}\',\
    #         country=\'{self.country}\',\
    #         year=\'{self.year}\',\
    #         company=\'{self.company}\',\
    #         director=\'{self.director}\',\
    #         actor=\'{self.actor}\',\
    #         date=\'{self.date}\',\
    #         running_time=\'{self.running_time}\',\
    #         keyword=\'{self.keyword}\',\
    #         plot=\'{self.plot}\',)'

    @property
    def json(self):
        return {
            'movieid' : self.movieid,
            'title' : self.title,
            'subtitle' : self.subtitle,
            'description' : self.description,
            'imageurl' : self.imageurl,
            'year' : self.year,
            'rating' : self.rating
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# search = NaverMovie()
# Session = sessionmaker(bind=engine)
# s = Session()
# df = search.hook()
# print(df.head())
# s.bulk_insert_mappings(MovieDto, df.to_dict(orient="records"))
# s.commit()
# s.close()