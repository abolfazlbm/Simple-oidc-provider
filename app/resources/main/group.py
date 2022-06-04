# from flask import request
# from flask_jwt_extended import jwt_required
# from flask_restful import Resource
# from webargs import fields
# from webargs.flaskparser import use_kwargs
#
# from app.errors import CustomException
# from app.models.group import GroupModel
# from app.models.organization import OrganizationModel
# from app.models.schema.group import GroupSchema
# from app.models.user import UserModel
# from app.response import ResponseAPI
# from app.utils.strings import gettext
#
#
# class GroupsResource(Resource):
#
#     # Get List Of Group
#     @jwt_required
#     @UserModel.is_permission("read_groups")
#     @use_kwargs({"q": fields.Str(missing=""), "perPage": fields.Int(missing=10), "page": fields.Int(missing=1),
#                  "sortBy": fields.Str(missing="id"), "sortDesc": fields.Bool(missing=True)}, location="query")
#     def get(self, q, perPage, page, sortBy, sortDesc):
#         try:
#             group_schema = GroupSchema(many=True)
#             groups, total_record = GroupModel.find(per_page=perPage, page=page, sort_by=sortBy, sort_desc=sortDesc)
#             result = group_schema.dump(groups.items)
#             return ResponseAPI.send(status_code=201, message=gettext("successful"),
#                                     data={"groups": result, "meta": {"total": total_record}})
#         except Exception as e:
#             raise CustomException(gettext("server_error"), 500, 2201, e.args)
#
#     # Create New Member
#     @jwt_required
#     @UserModel.is_permission("create_groups")
#     @use_kwargs({"title": fields.Str(required=True), "description": fields.Str(missing=""),
#                  "organization_id": fields.Int(required=True)}, location="json")
#     def post(self, **kwargs):
#         try:
#             new_group = GroupModel(**kwargs)
#             if OrganizationModel.find_by_id(new_group.organization_id) is None:
#                 raise CustomException(gettext("organization_not_found"), 400, 2301, new_group.organization_id)
#             new_group.add()
#             new_group.commit_db()
#
#             return ResponseAPI.send(status_code=201, message=gettext("groups_created"), data=new_group.id)
#
#         except CustomException as e:
#             raise e
#         except Exception as e:
#             raise CustomException(gettext("server_error"), 500, 2203, e.args)
