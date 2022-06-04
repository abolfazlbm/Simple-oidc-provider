from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from flask_restful import Resource, reqparse

from app.errors import CustomException
from app.models.role import RoleModel
from app.models.schema.user import UserSchema
from app.models.user import UserModel
from app.resources.auth.blacklist_helpers import revoke_token
from app.response import ResponseAPI
from app.utils.cryptography import Cryptography
from app.utils.strings import gettext


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
                            "email": user1.email, "mobile": user1.mobile, "username": user1.username}
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
                    user.save_to_db()
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
            if UserModel.is_exist_by_mobile(args["mobile"]):
                return ResponseAPI.send(status_code=409, message=gettext("user_mobile_exists"))

            role = RoleModel.find_by_name(args["role"])
            if role is not None:
                newuser = UserModel(firstname=args["firstname"], lastname=args["lastname"], username=args["username"],
                                    email=args["email"], mobile=args["mobile"])
                print(newuser)
                newuser.roles.append(role)
                newuser.password = Cryptography.hash_password(args["password"])

                newuser.save_to_db()
                return ResponseAPI.send(status_code=201, message=gettext("user_registered"), data="OK")
            else:
                return ResponseAPI.send(status_code=404, message=gettext("role_not_data"))

        except Exception:
            raise CustomException(gettext("user_error_creating"), 500, 2201)

    # @classmethod
    # @jwt_required
    # @UserModel.is_permission("admin_permission")
    # def post(cls):
    #     try:
    #         data_json = request.get_json()
    #         print(data_json)
    #         users = User.find_all(data_json["page_size"], data_json["page_num"])
    #         if users[0] is not None:
    #             result = []
    #             for item in users[0]:
    #                 user1 = User.find_by_id(item.created_by, deleteitem=True)
    #                 if user1:
    #                     created_by = user1.username
    #                 else:
    #                     created_by = None
    #                 user2 = User.find_by_id(item.updated_by, deleteitem=True)
    #                 if user2:
    #                     updated_by = user2.username
    #                 else:
    #                     updated_by = None
    #                 data_out = {"id": item.id, "username": item.username, "firstname": item.firstname,
    #                             "lastname": item.lastname, "email": item.email, "roles": item.roles,
    #                             "created_by": created_by,
    #                             "created_at": item.created_at, "updated_by": updated_by, "updated_at": item.updated_at}
    #                 result.append(data_out)
    #             data = {"users": result, "lastPage": users[1]}
    #             return ResponseAPI.send(status_code=200, message=gettext("user_get"), data=data)
    #         return ResponseAPI.send(status_code=404, message=gettext("user_not_found"))
    #
    #     except Exception:
    #         raise CustomException(gettext("user_error"), 500, 2205)

#
# class UserProfile(Resource):
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def get(cls):
#         try:
#             user_info = get_jwt_claims()
#             result = Locations.find_count_by_createdby(user_info["user_id"])
#             data = {"user": user_info, "location_count": result}
#             return ResponseAPI.send(status_code=200, message=gettext("successful"), data=data)
#
#         except Exception:
#             raise CustomException(gettext("user_error"), 500, 2206)
#
#
# class UserSearch(Resource):
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def post(cls):
#         try:
#             data_json = request.get_json()
#             users = User.find_by_search(data_json["keyword"], data_json["page_size"], data_json["page_num"])
#             if users[0] is not None:
#                 result = []
#                 for item in users[0]:
#                     user1 = User.find_by_id(item.created_by, deleteitem=True)
#                     if user1:
#                         created_by = user1.username
#                     else:
#                         created_by = None
#                     user2 = User.find_by_id(item.updated_by, deleteitem=True)
#                     if user2:
#                         updated_by = user2.username
#                     else:
#                         updated_by = None
#                     data_out = {"id": item.id, "username": item.username, "firstname": item.firstname,
#                                 "lastname": item.lastname, "email": item.email, "roles": item.roles,
#                                 "created_by": created_by,
#                                 "created_at": item.created_at, "updated_by": updated_by, "updated_at": item.updated_at}
#                     result.append(data_out)
#                 data = {"users": result, "lastPage": users[1]}
#                 return ResponseAPI.send(status_code=200, message=gettext("user_get"), data=data)
#             return ResponseAPI.send(status_code=404, message=gettext("user_not_found"))
#
#         except Exception:
#             raise CustomException(gettext("user_error"), 500, 2207)
