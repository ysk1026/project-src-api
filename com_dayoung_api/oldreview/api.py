from flask_restful import Resource, reqparse
from com_dayoung_api.review.dto import ReviewDto
from com_dayoung_api.review.dao import ReviewDao

class Review(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('user_id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('movie_id', type=int, required=False, help='This field cannot be left blank')
        parser.add_argument('title', type=str, required=False, help='This field cannot be left blank')
        parser.add_argument('content', type=str, required=False, help='This field cannot be left blank')
        
    def post(self):
        data = self.parser.parse_args()
        review = ReviewDto(data['title'], data['content'], data['user_id'], data['movie_id'])
        try:
            review.save()
        except:
            return {'message': 'An error occurred inserting the review'}, 500
        return review.json(), 201
    
    def get(self, id):
        review = ReviewDao.find_by_id(id)
        if review:
            return review.json()
        return {'message' : 'Review not found'}, 404
    
    def put(self, id):
        data = Review.parser.parse_args()
        review = ReviewDao.find_by_id(id)
        
        review.title = data['title']
        review.content = data['content']
        review.save()
        return Review.json()
    
class Reviews(Resource):
    def get(self):
        return {'reviews' : list(map(lambda review: review.json(), ReviewDao.find_all()))}
    # return {'articles':[article.json() for article in ArticleDao.find_all()]}