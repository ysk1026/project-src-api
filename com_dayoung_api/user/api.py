from typing import List
from flask import request
from flask_restful import Resource, reqparse
from com_dayoung_api.user.dao import UserDao
from com_dayoung_api.user.dto import UserDto, UserVo
import json
from flask import jsonify

parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
parser.add_argument('userid', type=str, required=True,
                                        help='This field should be a userid')
parser.add_argument('password', type=str, required=True,
                                        help='This field should be a password')

class User(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        print(f'User {args["id"]} added ')
        params = json.loads(request.get_data(), encoding='utf-8')
        if len(params) == 0:

            return 'No parameter'

        params_str = ''
        for key in params.keys():
            params_str += 'key: {}, value: {}<br>'.format(key, params[key])
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def get(id):
        print('==========3===========')
        try:
            print('진입')
            user = UserDao.find_by_id(id)
            print(type(user))
            if user:
                print('성공!')
                return user.json()
        except Exception as e:
            return {'message': 'User not found'}, 404
        


    @staticmethod
    def update():
        args = parser.parse_args()
        print(f'User {args["id"]} updated ')
        return {'code':0, 'message': 'SUCCESS'}, 200

    @staticmethod
    def delete():
        args = parser.parse_args()
        print(f'USer {args["id"]} deleted')
        return {'code' : 0, 'message' : 'SUCCESS'}, 200

    
    
class Users(Resource):
    
    def post(self):
        ud = UserDao()
        ud.insert_many('users')

    def get(self):
        print('========== 10 ==========')
        data = UserDao.find_all()
        return data, 200

class Auth(Resource):

    def post(self):
        body = request.get_json()
        user = UserDto(**body)
        UserDao.save(user)
        id = user.userid
        
        return {'id': str(id)}, 200 


class Access(Resource):
    def __init__(self):
        print('========== 5 ==========')
    def post(self):
        print('========== 6 ==========')
        args = parser.parse_args()
        user = UserVo()
        user.userid = args.userid
        user.password = args.password
        print(user.userid)
        print(user.password)
        data = UserDao.login(user)
        return data[0], 200




