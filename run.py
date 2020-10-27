
from main import app
app.run(host='127.0.0.1', port='8080', debug=True)

# from flask import Flask
# from flask_restful import Resource, Api
# from flask_cors import CORS


# app = Flask(__name__)
# api = Api(app)
# CORS(app, resources={r'/api/*': {"origins": "*"}})

# class Rest(Resource):
#     def get(self):
#         return {'rest': 'Good !'}

#     def post(self):
#         return {'data':{'userid': '1', 'password': '1'}}
 
# api.add_resource(Rest, '/api/access')
 
# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=8080)