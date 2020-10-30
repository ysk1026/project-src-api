from typing import List
from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
import pandas as pd
import numpy as np
import os
from com_dayoung_api.utils.file_helper import FileReader
from pathlib import Path
from com_dayoung_api.ext.db import db, openSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func
# from com_dayoung_api.user.dto import UserDto
# from com_dayoung_api.movie.dto import MovieDto

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

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    
    rev_id: int = db.Column(db.Integer, primary_key=True, index=True)
    title: str = db.Column(db.String(100))
    content: str = db.Column(db.String(500))
    label: int = db.Column(db.Integer)
     
    user_id: str = db.Column(db.String(30)) # db.ForeignKey(UserDto.user_id
    movie_id: int = db.Column(db.Integer) # db.ForeignKey(MovieDto.movie_id)
    
    def __init__(self, title, content, label, user_id, movie_id):
        self.title = title
        self.content = content
        self.label = label
        self.user_id = user_id
        self.movie_id = movie_id
        
    def __repr__(self):
        return f'rev_id = {self.rev_id}, user_id = {self.user_id}, movie_id = {self.movie_id},\
            title = {self.title}, content = {self.content}, label = {self.label}'
    
    def json(self):
        return {
            'rev_id' : self.rev_id,
            'user_id' : self.user_id,
            'movie_id' : self.movie_id,
            'title' : self.title,
            'content' : self.content,
            'label' : self.label
        }
        
class ReviewVo:
    rev_id: int = 0
    title: str = ''
    content: str = ''
    label: int = 0
    user_id: str = ''
    movie_id: int = 0
    

# ==============================================================
# ==============================================================
# ====================     Service  ============================
# ==============================================================
# ==============================================================

class ReviewService:
    def __init__(self):
        self.fileReader = FileReader()
        self.data = os.path.join(os.path.abspath(os.path.dirname(__file__)) + '/data')
        
    def hook(self):
        train = 'rating.csv'
        this = self.fileReader
        this.train = self.new_model(train) # payload
        
        df = pd.DataFrame(
            {
                'user_id' : this.train.id,
                'movie_id' : '1',
                'title' : 'Avengers',
                'content' : this.train.document,
                'label' : this.train.label
            }
        )
        df = df.dropna()
        df = df[:1000]
        print(df.head())
        
        return df
    
    def new_model(self, payload) -> object:
        this = self.fileReader
        this.data = self.data
        this.fname = payload
        print(f'{self.data}')
        print(f'{this.fname}')
        return pd.read_csv(Path(self.data, this.fname))
    
'''
service = UserService()
service.hook()
'''
Session = openSession()
session = Session()
service = ReviewService()

           
class ReviewDao(ReviewDto):
    
    @classmethod
    def count(cls):
        return cls.query.count()
    
    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        # print(df)
        return json.loads(df.to_json(orient='records'))
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name == name)
    
    @classmethod
    def find_by_id(cls, id):
        print("FIND BY ID method 진입!")
        print(f'ID : {id}')
        sql = session.query(ReviewDto).filter(ReviewDto.rev_id.like(id))
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))
        # return session.query(ReviewDto).filter(ReviewDto.rev_id.like(id))
        # return cls.query.filter_by(id == id).first()
    
    @staticmethod
    def save(review):
        print('진입')
        print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
            User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        Session = openSession()
        print('1 clear')
        session = Session()
        print('2 clear')
        session.add(review)
        print('3 clear')
        session.commit()
        print('4 clear')
    
    @staticmethod   
    def insert_many():
        service = ReviewService()
        Session = openSession()
        session = Session()
        df = service.hook()
        print(df.head())
        session.bulk_insert_mappings(ReviewDto, df.to_dict(orient="records"))
        session.commit()
        session.close()
            
    @staticmethod
    def modify(review):
        Session = openSession()
        session = Session()
        session.add(review)
        session.commit()
        
    @classmethod
    def delete(cls,rev_id):
        Session = openSession()
        session = Session()
        data = cls.query.get(rev_id)
        session.delete(data)
        session.commit()
        
    @staticmethod
    def modify_review(review):
        print('진입')
        print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
            User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        Session = openSession()
        session = Session()
        print('Success 1')
        session.query(ReviewDto).filter(ReviewDto.rev_id == review['rev_id']).update(review)
        session.commit()
        print('movie data modify complete')
        
# ==============================================================
# ==============================================================
# ====================        API       ========================
# ==============================================================
# ==============================================================

parser = reqparse.RequestParser()
parser.add_argument('user_id', type =str, required =False, help ='This field cannot be left blank')
parser.add_argument('movie_id', type =int, required =False, help ='This field cannot be left blank')
parser.add_argument('title', type =str, required =False, help ='This field cannot be left blank')
parser.add_argument('content', type =str, required =False, help ='This field cannot be left blank')
parser.add_argument('label', type =int, required =False, help ='This field cannot be left blank')

class Review(Resource):
    
    @staticmethod
    def post():
        # service = ReviewService()
        args = parser.parse_args()
        review = ReviewDto(args.title, args.content, 3, args.user_id, args.movie_id)
        print('=======3======')
        # print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
        #     User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        # review = ReviewDao(args['title'], args['movie_id'], \
        #     args['user_id'], args['content'])
        try: 
            ReviewDao.save(review)
            return {'code' : 0, 'message' : 'SUCCESS'}, 200    
        except:
            return {'message': 'An error occured inserting the article'}, 500

    def get(self, id):
        print("진입 성공!")
        print(id)
        review = ReviewDao.find_by_id(id)
        print("Review 가져옴!")
        print(f'리뷰 정보: \n {review}')
        return review
        # if review:
        #     return review.json()
        # return {'message' : 'Article not found'}, 404
    
    def put(self, id):
        data = Review.parser.parse_args()
        review = ReviewDao.find_by_id(id)
        
        review.title = data['title']
        review.content = data['content']
        review.save()
        return review.json()
    
    def update(self, id):
        data = Review.parser.parse_args()
        review = ReviewDao.find_by_id(id)
        
# class DelReview(Resource):
     
#      @staticmethod
#      def post():
#          args = parser.parse_args()
#          review = ReviewDto(args.rev_id)
        
class Reviews(Resource):
    def get(self):
        # return {'review' : list(map(lambda review: review.json(), ReviewDao.find_all()))}
        # return {'articles':[article.json() for article in ArticleDao.find_all()]}
  
        print('========== 10 ==========')
        data = ReviewDao.find_all()
        return data, 200
    

# rd = ReviewDao()
# rd.bulk()


# service = ReviewService()
# Session = sessionmaker(bind=engine)
# s = Session()
# df = service.hook()
# print(df.head())
# s.bulk_insert_mappings(ReviewDto, df.to_dict(orient="records"))
# s.commit()
# s.close()