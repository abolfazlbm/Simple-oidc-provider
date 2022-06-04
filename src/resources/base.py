import json

from flask_restful import Resource


class Hello(Resource):
    @classmethod
    def get(cls):
        # jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        # user_id = get_jwt_identity()
        # print(user_id)
        return json.dumps('Hello World'), 200

