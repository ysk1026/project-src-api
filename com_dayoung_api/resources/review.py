from typing import List
from flask_restful import Resource, reqparse
from flask import request
import json
from flask import jsonify
import pandas as pd
import numpy as np
import os
from com_dayoung_api.utils.file_helper import FileReader
from com_dayoung_api.resources.movie import RecoMovieDto, RecoMovieVo
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
    movie_id: int = db.Column(db.Integer, db.ForeignKey(RecoMovieDto.movieid))
    
    # movie = db.relationship('MovieDto', back_populates="reviews")
    
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
        movie = 'kmdb_csv.csv'
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
        df = df[:50] # 데이터 불러올 갯수, 너무 많아지면 핸들링하기 힘드니 상황에 맞게 조절한다.
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

service = ReviewService()

           
class ReviewDao(ReviewDto):
    
    @classmethod
    def count(cls):
        return cls.query.count()
    
    @classmethod
    def group_by(cls):
        Session = openSession()
        session = Session()
        titledict = {}
        titles = session.query(cls.title, cls.label).all() # 타이틀 뽑아 왔음
        # return session.query(cls.title, cls.label).all() # 타이틀 뽑아 왔음
        for title in titles:
            if title[0] not in titledict:
                titledict[title[0]] = 1
            else:
                titledict[title[0]] += 1
            if title[1] == 1:
                titledict[title[0]] += 1
        titledict = {k: v for k, v in sorted(titledict.items(), key=lambda item: item[1])}
        return titledict
            
                
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
        Session = openSession()
        session = Session()
        print("FIND BY ID method 진입!")
        print(f'ID : {id}')
        # sql = session.query(ReviewDto).filter(ReviewDto.rev_id.like(id))
        # df = pd.read_sql(sql.statement, sql.session.bind)
        # return json.loads(df.to_json(orient='records'))

        return session.query(ReviewDto).filter(ReviewDto.rev_id.like(id)).one()
        # return cls.query.filter_by(id == id).first()
    
    @classmethod
    def find_review_by_user_id(cls, user_id):
        Session = openSession()
        session = Session()
        print("FIND BY USER ID METHOD 진입!")
        # print (session.query(ReviewDto).filter(ReviewDto.user_id.like(user_id)).all())
        print ("성공")
        return session.query(ReviewDto).filter(ReviewDto.user_id.like(user_id)).all()
    
    @classmethod
    def find_by_movie_title(cls, title):
        Session = openSession()
        session = Session()
        print("FIND BY TITLE 진입 !")
        # sql = cls.query
        # df = pd.read_sql(sql.statement, sql.session.bind)
        # print(df)
        # sql = cls.query
        # return json.loads(df.to_json(orient=‘records’))
        return session.query(ReviewDto).filter(ReviewDto.title.like(title)).all()
    
    @staticmethod
    def save(review):
        Session = openSession()
        session = Session()
        print('진입')
        print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
            User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        print('1 clear')
        session.add(review)
        print('2 clear')
        session.commit()
        session.close()
        print('3 clear')
    
    @staticmethod
    def update(review, id):
        Session = openSession()
        session = Session()
        print('진입')
        print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
            User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
        print('update 1 clear')
        print(f'************ID : {id} **************** ')
        print('update 2 clear')
        session.query(ReviewDto).filter(ReviewDto.rev_id == review.rev_id).update({ReviewDto.user_id:review.user_id,
                                                                                   ReviewDto.movie_id:review.movie_id,
                                                                                   ReviewDto.title:review.title,
                                                                                   ReviewDto.content:review.content,
                                                                                   ReviewDto.label:review.label
                                                                                   })
        print('update 3 clear')
        session.commit()
        session.close()
        print('update 4 clear')
    
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
            
    # @staticmethod
    # def modify(review):
    #     Session = openSession()
    #     session = Session()
    #     session.add(review)
    #     session.commit()
        
    @classmethod
    def delete(cls,rev_id):
        print('##### review data delete #####')
        print(rev_id)
        data = cls.query.get(rev_id)
        print(f'###### review data: {data}')
        db.session.delete(data)
        print("Delete in progress")
        db.session.commit()
        # db.session.close()
        print('##### review data delete complete #####')
        
    # @staticmethod
    # def modify_review(review):
    #     print('진입')
    #     print(f'Rev id : {review.rev_id} / Movie_id :{review.movie_id}/\
    #         User_id: {review.user_id}/ Title: {review.title}/ Content: {review.content} / Label: {review.label}')
    #     Session = openSession()
    #     session = Session()
    #     print('Success 1')
    #     session.query(ReviewDto).filter(ReviewDto.rev_id == review['rev_id']).update(review)
    #     session.commit()
    #     print('movie data modify complete')
        
# ==============================================================
# ==============================================================
# ====================        API       ========================
# ==============================================================
# ==============================================================

# parser = reqparse.RequestParser()
# parser.add_argument('user_id', type =str, required =False, help ='This field cannot be left blank')
# parser.add_argument('movie_id', type =int, required =False, help ='This field cannot be left blank')
# parser.add_argument('title', type =str, required =False, help ='This field cannot be left blank')
# parser.add_argument('content', type =str, required =False, help ='This field cannot be left blank')
# parser.add_argument('label', type =int, required =False, help ='This field cannot be left blank')

class ReviewPost(Resource):
    
    @staticmethod
    def post():
        print('진입')
        # service = ReviewService()
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('movie_id', type =int, required =False, help ='This field cannot be left blank')
        parser.add_argument('title', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('content', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('label', type =int, required =False, help ='This field cannot be left blank')

        args = parser.parse_args()

        # review = ReviewDto(args.title, args.content, 1, args.user_id, args.movie_id)
        review = ReviewDto(args.title, args.content, 1, "jason", args.movie_id)
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
    
    @staticmethod
    def get():
        print("진입")
        top_movie = ReviewDao.group_by()
        return top_movie
    
class Review(Resource):

    def get(self, id):
        print("진입 성공!")
        print(id)
        review = ReviewDao.find_by_id(id)
        print("Review 가져옴!")
        # print(f'리뷰 정보: \n {review}')
        # print(f'리뷰 타입 {type(review)}')
        # print(f'제이슨 변환 이후: {review.json()}')
        return review.json()
        # if review:
        #     return review.json()
        # return {'message' : 'Article not found'}, 404
    
    def put(self, id):
        print('PUT 진입')
        parser = reqparse.RequestParser()
        parser.add_argument('title', type =str, required =False, help ='This field cannot be left blank')
        parser.add_argument('content', type =str, required =False, help ='This field cannot be left blank')
        
        args = parser.parse_args()
        print(args)
        review = ReviewDao.find_by_id(id)
        review.title = args['title']
        review.content = args['content']
        # review = ReviewDto(args)
        # data = review.json()
        # return data
        print('리뷰', review)
        print('리뷰 타입', type(review))
        try: 
            ReviewDao.update(review, id)
            return {'code' : 0, 'message' : 'SUCCESS'}, 200    
        except:
            return {'message': 'An error occured inserting the article'}, 500
    
    # def update(self, id):
    #     data = Review.parser.parse_args()
    #     review = ReviewDao.find_by_id(id)
        
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

class ReviewDel(Resource):
    
    def post(self, rev_id):
        print('Delete 진입')
        review = ReviewDao.find_by_id(rev_id)
        print('리뷰 아이디', review.rev_id)
        print('전체 리뷰', review)
        print('리뷰 타입', type(review))
        try:
            ReviewDao.delete(review.rev_id)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500

# 리뷰 서치 기능 구현 클래스
class ReviewSearch(Resource):
    
    def get(self, title):
        print("SEARCH 진입")
        print(f'타이틀 : {title}')
        review = ReviewDao.find_by_movie_title(title)
        # review = {review[i]: review[i + 1] for i in range(0, len(review), 2)}
        # review = json.dump(review)
        reviewlist = []
        # for review in reviews:
            # reviewdic
        for rev in review:
            reviewlist.append(rev.json())
        # print(f’Review type : {type(review[0])}‘)
        print(f'Review List: {reviewlist}')
        return reviewlist[:]
    
# User ID에 해당하는 리뷰들 관리
class ReviewByUser(Resource):
    
    def get(self, user_id):
        print("마이 리뷰 찾기 진입!")
        print(f"User ID : {user_id}의 리뷰들를 불러오는 중 . . .")
        review = ReviewDao.find_review_by_user_id(user_id)
        # 여기서 이제 review를 제이슨화 시킨후 보내주면 됨
        reviewlist = []
        for rev in review:
            reviewlist.append(rev.json())
        print(f"{user_id}의 전체 리뷰: {reviewlist}")
        return reviewlist[:]
        