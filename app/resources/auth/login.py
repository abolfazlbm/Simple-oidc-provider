import datetime

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_claims,
                                get_jwt_identity, jwt_required, get_raw_jwt)
from flask_restful import Resource

from app.blacklist import BLACKLIST
from app.errors import CustomException
from app.models.schema.user import UserSchema
from app.models.user import UserModel
from app.resources.auth.blacklist_helpers import add_token_to_database, revoke_token
from app.response import ResponseAPI
from app.utils.cryptography import Cryptography
from app.utils.strings import gettext


class UserLoginResource(Resource):

    @classmethod
    def post(cls):

        try:
            user_json = request.get_json()
            password = user_json["password"]
            user = UserModel.find_by_username(user_json["username"],)
            if user is not None:
                if Cryptography.verify_password(user.password, password):
                    user_schema = UserSchema()
                    userdump = user_schema.dump(user)
                    print(user.roles[0].name)
                    user_info = {
                        "firstname": userdump["firstname"],
                        "lastname": userdump["lastname"],
                        'user_id': userdump["id"],
                        "username": userdump["username"],
                        "roles": userdump["roles"]
                    }
                    expires = datetime.timedelta(minutes=15)
                    expires_refresh = datetime.timedelta(days=20)
                    access_token = create_access_token(identity=user.id, user_claims=user_info, fresh=True,
                                                       expires_delta=expires)
                    refresh_token = create_refresh_token(identity=user.id, user_claims=user_info,
                                                         expires_delta=expires_refresh)

                    add_token_to_database(access_token)
                    add_token_to_database(refresh_token)

                    userdump['displayName'] = user.firstname + " " + user.lastname
                    data_in = {"userData": userdump, "access_token": access_token, "refresh_token": refresh_token}
                    return ResponseAPI.send(status_code=200, message=gettext("user_login"), data=data_in)

                return ResponseAPI.send(status_code=403, message=gettext("user_invalid_credentials"), data={"code": 1020})
            return ResponseAPI.send(status_code=403, message=gettext("user_invalid_credentials"), data={"code": 1021})
        except Exception:
            raise CustomException(gettext("user_not_found"), 403, 1001)


class SignoutResource(Resource):

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()["jti"]
        user_identity = get_jwt_identity()
        BLACKLIST.add(jti)
        revoke_token(user_identity)
        return ResponseAPI.send(status_code=200, message=gettext("user_logged_out"))


class Singout2Resource(Resource):
    # Endpoint for revoking the current users refresh token
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        user_identity = get_jwt_identity()
        BLACKLIST.add(jti)
        # revoke_token(user_identity,jti)
        return ResponseAPI.send(status_code=200, message=gettext("user_logged_out"))


class TokenRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        user_info = get_jwt_claims()
        expires = datetime.timedelta(hours=1)
        new_token = create_access_token(identity=current_user, user_claims=user_info, expires_delta=expires,
                                        fresh=False)
        data = {"access_token": new_token}

        add_token_to_database(new_token)

        return ResponseAPI.send(status_code=200, message=gettext("successful"), data=data)
#
#
# class Fresh_login(Resource):
#     @classmethod
#     def post(cls):
#         try:
#             user_json = request.get_json()
#             password = user_json["password"]
#             user = User.find_by_username(user_json["username"])
#             if user:
#                 if Cryptography.verify_password(user.password, password):
#                     use_info = {
#                         "firstname": user.firstname,
#                         "lastname": user.lastname,
#                         'user_id': user.id,
#                         "roles": user.roles
#                     }
#                     expires = datetime.timedelta(hours=10)
#                     access_token = create_access_token(identity=user.id, user_claims=use_info, fresh=True,
#                                                        expires_delta=expires)
#                     data_in = {"access_token": access_token}
#                     return ResponseAPI.send(status_code=200, message=gettext("user_login"), data=data_in)
#
#                 return ResponseAPI.send(status_code=401, message=gettext("user_invalid_credentials"))
#             return ResponseAPI.send(status_code=404, message=gettext("user_username_not_exists"))
#         except Exception:
#             raise CustomException(gettext("user_not_found"), 404, 1001)
