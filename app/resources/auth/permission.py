import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.errors import CustomException
from app.models.permission import PermissionModel
from app.models.user import UserModel
from app.models.validator.permission import validate_json
from app.response import ResponseAPI
from app.utils.strings import gettext

#
# class Permissions(Resource):
#     @classmethod
#     @jwt_required
#     #@User.is_permission("admin_permission")
#     def post(cls):
#         try:
#             user_id = get_jwt_identity()
#             data_json = request.get_json()
#             print(data_json)
#             if validate_json(data_json):
#
#                 if Permission.is_exist_by_name(data_json["name"]):
#                     return ResponseAPI.send(status_code=412, message=gettext("permission_name_exists"))
#
#                 obj = Permission(name=data_json["name"], description=data_json["description"], created_by=user_id)
#                 result = obj.save_to_db()
#                 return ResponseAPI.send(status_code=201, message=gettext("permission_created"), data=result)
#
#             return ResponseAPI.send(status_code=400, message=gettext("permission_bad_request"))
#         except Exception:
#             raise CustomException(gettext("permission_error_creating"), 500, 2001)
#
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def get(cls):
#         try:
#
#             permission_id = request.args.get('id')
#             print(permission_id)
#             prm = Permission.find_by_id(permission_id)
#             print(prm)
#             if prm is not None:
#                 user1 = User.find_by_id(prm.created_by, deleteitem=True)
#                 if user1:
#                     created_by = user1.username
#                 else:
#                     created_by = None
#                 user2 = User.find_by_id(prm.updated_by, deleteitem=True)
#                 if user2:
#                     updated_by = user2.username
#                 else:
#                     updated_by = None
#                 user3 = User.find_by_id(prm.deleted_by, deleteitem=True)
#                 if user3:
#                     deleted_by = user3.username
#                 else:
#                     deleted_by = None
#
#                 data_in = {"id": prm.id, "name": prm.name, "description": prm.description, "created_by": created_by,
#                            "created_at": prm.created_at, "updated_by": updated_by, "updated_at": prm.updated_at,
#                            "deleted_by": deleted_by, "deleted_at": prm.deleted_at}
#                 return ResponseAPI.send(status_code=200, message=gettext("permission_get"), data=data_in)
#             return ResponseAPI.send(status_code=404, message=gettext("permission_not_found").format(permission_id))
#         except Exception:
#             raise CustomException(gettext("permission_error"), 500, 2002)
#
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def delete(cls):
#         try:
#             user_id = get_jwt_identity()
#             data_json = request.get_json()
#             print(data_json)
#             result = Permission.delete_by_id(data_json["id"], user_id)
#             if result is not None:
#                 return ResponseAPI.send(status_code=200, message=gettext("permission_deleted"), data=result)
#             return ResponseAPI.send(status_code=404, message=gettext("permission_not_found").format(data_json["id"]))
#         except Exception:
#             raise CustomException(gettext("permission_error"), 404, 2003)
#
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")  # ("edit_permission")
#     def put(cls):
#         try:
#             user_id = get_jwt_identity()
#             data_json = request.get_json()
#             print(data_json)
#             prm = Permission.find_by_id(data_json["id"])
#             print(prm)
#             if prm is not None:
#                 if "name" in data_json and data_json["name"] != "":
#                     prm.name = data_json["name"]
#                 if "description" in data_json and data_json["description"] != "":
#                     prm.title = data_json["description"]
#                 result = prm.update(user_id)
#
#                 return ResponseAPI.send(status_code=200, message=gettext("permission_updated"), data=result)
#             return ResponseAPI.send(status_code=404, message=gettext("permission_not_found").format(data_json["id"]))
#         except Exception:
#             raise CustomException(gettext("permission_error"), 500, 2004)
#
#
# class PermissionList(Resource):
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def post(cls):
#         try:
#             data_json = request.get_json()
#             print(data_json)
#             permissions = Permission.find_all(data_json["page_size"], data_json["page_num"])
#             if permissions[0] is not None:
#                 permissions_list = []
#                 for item in permissions[0]:
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
#                     user3 = User.find_by_id(item.deleted_by, deleteitem=True)
#                     if user3:
#                         deleted_by = user3.username
#                     else:
#                         deleted_by = None
#
#                     data_in = {"id": item.id, "name": item.name, "description": item.description, "created_by": created_by,
#                                "created_at": item.created_at, "updated_by": updated_by,
#                                "deleted_by": deleted_by, "deleted_at": item.deleted_at}
#
#                     permissions_list.append(data_in)
#                 data = {"permissions": permissions_list, "lastPage": permissions[1]}
#                 return ResponseAPI.send(status_code=200, message=gettext("permission_get"), data=data)
#             return ResponseAPI.send(status_code=404, message=gettext("permission_not_data"))
#         except Exception:
#             raise CustomException(gettext("permission_error"), 500, 2005)
