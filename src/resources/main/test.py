from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import parser

from src.errors import CustomException
from src.response import ResponseAPI


class Test(Resource):
    def get(self):
        try:
            message = {'message': 'API Test Successfully'}
            return ResponseAPI.send(status_code=201, message=message, data=message)
        except Exception as err:
            raise CustomException(err.args, 500, 2101)

    @parser.use_kwargs({"posts_per_page": fields.Int(missing=10)}, location="json")
    def post(self, posts_per_page):
        try:
            message = {'message': 'Hello, World!'}
            return ResponseAPI.send(status_code=201, message=message, data={'posts_per_page': posts_per_page})
        except Exception as err:
            raise CustomException(err.args, 500, 2101)
