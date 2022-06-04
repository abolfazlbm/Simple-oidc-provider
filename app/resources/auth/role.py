import datetime

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.errors import CustomException
from app.models.permission import PermissionModel
from app.models.role import RoleModel
from app.models.user import UserModel
from app.models.validator.role import validate_json
from app.response import ResponseAPI
from app.utils.strings import gettext

#
# class Roles(Resource):
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")  # ("create_role")
#     def post(cls):
#         try:
#             user_id = get_jwt_identity()
#             role_json = request.get_json()
#             if validate_json(role_json):
#                 if Role.is_exist_by_name(role_json["name"]):
#                     return ResponseAPI.send(status_code=412, message=gettext("role_name_exists"))
#
#                 list_in = []
#                 for item in role_json["permissions"]:
#                     prm = Permission.find_by_id(item)
#                     if prm:
#                         data_in = {"id": prm.id, "name": prm.name}
#                         list_in.append(data_in)
#                     else:
#                         return ResponseAPI.send(status_code=404,
#                                                 message=gettext("permission_not_found").format(item))
#
#                 role = Role(name=role_json['name'], description=role_json['description'], permissions=list_in,
#                             created_by=user_id)
#                 result = role.save_to_db()
#                 return ResponseAPI.send(status_code=201, message=gettext("role_created"), data=result)
#             else:
#                 return ResponseAPI.send(status_code=400, message=gettext("role_bad_request"))
#         except Exception:
#             raise CustomException(gettext("role_error_creating"), 500, 2101)
#
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def get(cls):
#         try:
#             role_json = request.get_json()
#             role = Role.find_by_id(role_json["id"])
#             if role is not None:
#                 user1 = User.find_by_id(role.created_by, deleteitem=True)
#                 if user1:
#                     created_by = user1.username
#                 else:
#                     created_by = None
#                 user2 = User.find_by_id(role.updated_by, deleteitem=True)
#                 if user2:
#                     updated_by = user2.username
#                 else:
#                     updated_by = None
#                 user3 = User.find_by_id(role.deleted_by, deleteitem=True)
#                 if user3:
#                     deleted_by = user3.username
#                 else:
#                     deleted_by = None
#
#                 data_in = {"id": role.id, "name": role.name, "description": role.description,
#                            "permissions": role.permissions, "created_by": created_by,
#                            "created_at": role.created_at, "updated_by": updated_by, "updated_at": role.updated_at,
#                            "deleted_by": deleted_by, "deleted_at": role.deleted_at}
#                 return ResponseAPI.send(status_code=200, message=gettext("role_get"), data=data_in)
#             return ResponseAPI.send(status_code=404, message=gettext("role_not_found").format(role_json["id"]))
#         except Exception:
#             raise CustomException(gettext("role_error"), 500, 2102)
#
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")
#     def delete(cls):
#         try:
#             role_json = request.get_json()
#             user_id = get_jwt_identity()
#             result = Role.delete_by_id(role_json["id"], user_id)
#             if result is not None:
#                 return ResponseAPI.send(status_code=200, message=gettext("role_deleted"), data=result)
#
#             return ResponseAPI.send(status_code=404, message=gettext("role_not_found").format(role_json["id"]))
#         except Exception:
#             raise CustomException(gettext("role_error"), 500, 2103)
#
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")  # ("edit_role")
#     def put(cls):
#
#         try:
#             user_id = get_jwt_identity()
#             role_json = request.get_json()
#             list_in = []
#             role = Role.find_by_id(role_json["id"])
#             if role is not None:
#                 if "name" in role_json:
#                     role.name = role_json["name"]
#                 if "permissions" in role_json:
#                     for item in role_json["permissions"]:
#                         prm = Permission.find_by_id(item)
#                         data_in = {"id": prm.id, "name": prm.name}
#                         list_in.append(data_in)
#                     role.permissions = list_in
#                 result = role.update(user_id)
#
#                 return ResponseAPI.send(status_code=200, message=gettext("role_updated"), data=result)
#
#             return ResponseAPI.send(status_code=404, message=gettext("role_not_found").format(role_json["id"]))
#         except Exception:
#             raise CustomException(gettext("role_error"), 500, 2104)
#
#
# class RoleList(Resource):
#     @classmethod
#     @jwt_required
#     @User.is_permission("admin_permission")#("get_all_roles")
#     def get(cls):
#         try:
#
#             roles = Role.find_all()
#             if roles is not None:
#                 result = []
#                 for item in roles:
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
#
#                     data_in = {"id": item.id, "name": item.name, "descripition": item.description,
#                                "permissions": item.permissions, "created_by": created_by,
#                                "created_at": item.created_at, "updated_by": updated_by}
#                     result.append(data_in)
#                 return ResponseAPI.send(status_code=200, message=gettext("role_get"), data=result)
#             return ResponseAPI.send(status_code=404, message=gettext("role_not_data"))
#         except Exception:
#             raise CustomException(gettext("role_error"), 500, 2105)
