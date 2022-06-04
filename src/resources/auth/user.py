from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from flask_restful import Resource, reqparse

from src.errors import CustomException
from src.models.role import RoleModel
from src.models.schema.user import UserSchema
from src.models.user import UserModel
from src.resources.auth.blacklist_helpers import revoke_token
from src.response import ResponseAPI
from src.utils.cryptography import Cryptography
from src.utils.strings import gettext


class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('firstname', type=str, location='json')
        self.reqparse.add_argument('lastname', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('mobile', type=str, location='json')
        self.reqparse.add_argument('role', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        super(UserResource, self).__init__()

    @classmethod
    @jwt_required
    def get(cls, id):
        try:
            user_id = get_jwt_identity()
            user1 = UserModel.find_by_id(id)
            if user_id == id or UserModel.find_by_id(_id=user_id).is_permission_by_db("read_users"):
                if user1 is not None:
                    user_schema = UserSchema()
                    data = {"id": user1.id, "firstname": user1.firstname, "lastname": user1.lastname,
                            "email": user1.email, "username": user1.username}
                    if user1.roles.count() > 0:
                        data["role"] = user1.roles[0].name

                    return ResponseAPI.send(status_code=200, message=gettext("user_get"), data=data)
                return ResponseAPI.send(status_code=404, message=gettext("user_not_found"))
            return ResponseAPI.send(status_code=401, message=gettext("user_not_permission"))
        except Exception:
            raise CustomException(gettext("user_error"), 500, 2202)

    @fresh_jwt_required
    @UserModel.is_permission("edit_users")  # ("create_role")
    def put(self, id):
        try:
            args = self.reqparse.parse_args()
            user = UserModel.find_by_id(id)
            newrolename = args['role']
            oldrole = user.roles[0]
            if oldrole != newrolename:
                revoke_token(user.id)
            user.update_user(args)

            return ResponseAPI.send(status_code=200, message=gettext("user_updated"), data=user.id)
        except Exception:
            raise CustomException(gettext("server_error"), 500, 2101)

    @fresh_jwt_required
    @UserModel.is_permission("del_users")
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(id)
            if user is not None:
                revoke_token(user.id)
                user.delete()
                return ResponseAPI.send(status_code=200, message=gettext("user_deleted"), data="OK")
            return ResponseAPI.send(status_code=404, message=gettext("user_not_found"))

        except Exception:
            raise CustomException(gettext("user_error"), 404, 2203)


class UserChangePassResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('oldpassword', type=str, location='json', required=True)
        self.reqparse.add_argument('newpassword', type=str, location='json', required=True)
        super(UserChangePassResource, self).__init__()

    @fresh_jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            args = self.reqparse.parse_args()
            user = UserModel.find_by_id(user_id)
            if user is not None:
                if Cryptography.verify_password(user.password, args["oldpassword"]):
                    user.resetpassword(args["newpassword"])
                    user.commit_db()
                    return ResponseAPI.send(status_code=202, message=gettext("user_changed_password"), data="OK")

                else:
                    return ResponseAPI.send(status_code=403, message=gettext("user_invalid_oldpassword"))
            return ResponseAPI.send(status_code=400, message=gettext("bad_request"))
        except Exception:
            raise CustomException(gettext("server_error"), 500, 2201)


class UserListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('firstname', type=str, location='json', required=True)
        self.reqparse.add_argument('lastname', type=str, location='json', required=True)
        self.reqparse.add_argument('email', type=str, location='json', required=True)
        self.reqparse.add_argument('username', type=str, location='json', required=True)
        self.reqparse.add_argument('mobile', type=str, location='json', required=True)
        self.reqparse.add_argument('role', type=str, location='json', required=True)
        self.reqparse.add_argument('password', type=str, location='json', required=True)
        super(UserListResource, self).__init__()

    @classmethod
    @jwt_required
    @UserModel.is_permission("read_users")
    def get(cls):
        try:
            print("OK")
            users_schema = UserSchema(many=True)
            users = UserModel.find_all()
            result = users_schema.dump(users)
            return ResponseAPI.send(status_code=201, message=gettext("successful"), data=result)
        except Exception:
            raise CustomException(gettext("server_error"), 500, 2101)

    @fresh_jwt_required
    @UserModel.is_permission("create_users")
    def post(self):
        try:
            user_id = get_jwt_identity()
            args = self.reqparse.parse_args()

            if UserModel.is_exist_by_username(args["username"]):
                return ResponseAPI.send(status_code=409, message=gettext("user_username_exists"))
            if UserModel.is_exist_by_email(args["email"]):
                return ResponseAPI.send(status_code=409, message=gettext("user_email_exists"))

            role = RoleModel.find_by_name(args["role"])
            if role is not None:
                newuser = UserModel(firstname=args["firstname"], lastname=args["lastname"], username=args["username"],
                                    email=args["email"])
                print(newuser)
                newuser.roles.append(role)
                newuser.password = Cryptography.hash_password(args["password"])

                newuser.add()
                newuser.commit_db()
                return ResponseAPI.send(status_code=201, message=gettext("user_registered"), data="OK")
            else:
                return ResponseAPI.send(status_code=404, message=gettext("role_not_data"))

        except Exception:
            raise CustomException(gettext("user_error_creating"), 500, 2201)

