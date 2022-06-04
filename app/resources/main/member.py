# import random
# from datetime import datetime
#
# from webargs import fields
# from webargs.flaskparser import use_kwargs, use_args
# from werkzeug.datastructures import FileStorage
# from flask import request
# from flask_jwt_extended import jwt_required
# from flask_restful import Resource, reqparse
# from sqlalchemy import exc
#
# from app.errors import CustomException
# from app.models.account import AccountModel
# from app.models.accounttype import AccountTypeModel
# from app.models.card import CardModel
# from app.models.schema.card import CardSchema
# from app.models.schema.member import MemberSchema, MemberFullSchema, MemberWithAccountSchema
# from app.models.member import MemberModel
# from app.models.user import UserModel
# from app.mqtt import MqttClass
# from app.response import ResponseAPI
# from app.utils.cryptography import Cryptography
# from app.utils.strings import gettext
#
#
# class MemberResource(Resource):
#
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('firstname', type=str, location='json')
#         self.reqparse.add_argument('lastname', type=str, location='json')
#         self.reqparse.add_argument('activecartcode', type=str, location='json')
#         # self.reqparse.add_argument('avatar', type=FileStorage, location='files')
#         self.reqparse.add_argument('company', type=str, location='json')
#         self.reqparse.add_argument('nationalcode', type=str, location='json')
#         self.reqparse.add_argument('post', type=str, location='json')
#         self.reqparse.add_argument('status', type=int, location='json')
#         self.reqparse.add_argument('username', type=str, location='json')
#         self.reqparse.add_argument('password', type=str, location='json')
#         self.reqparse.add_argument('email', type=str, location='json')
#         self.reqparse.add_argument('mobile', type=str, location='json')
#         self.reqparse.add_argument('expires_at', type=str, location='json')
#         self.reqparse.add_argument('is_active', type=bool, location='json')
#
#         super(MemberResource, self).__init__()
#
#     @classmethod
#     @jwt_required
#     @UserModel.is_permission("read_member")
#     def get(cls, id):
#         try:
#             member_schema = MemberFullSchema()
#             member = MemberModel.find_by_id(id)
#             if member is None:
#                 return ResponseAPI.send(status_code=404, message=gettext("member_not_found"), data=[])
#
#             result = member_schema.dump(member)
#             # MqttClass().mqtt.publish("staff/trans", str(members.credit))
#             return ResponseAPI.send(status_code=201, message=gettext("successful"), data=result)
#
#         except Exception:
#             raise CustomException(gettext("server_error"), 500, 2101)
#
#     @jwt_required
#     @UserModel.is_permission("edit_member")
#     def put(self, id):
#         try:
#             args = self.reqparse.parse_args()
#             member = MemberModel.find_by_id(id)
#             if member is None:
#                 return ResponseAPI.send(status_code=404, message=gettext("member_not_found"), data=[])
#
#             member.update_staff(args)
#             return ResponseAPI.send(status_code=200, message=gettext("staff_edited"), data=member.id)
#         except exc.IntegrityError:
#             raise CustomException("خطا در مقدار تکراری در دیتابیس، مقدار کد ملی بررسی شود", 500, 2301)
#         except Exception:
#             raise CustomException(gettext("server_error"), 500, 2101)
#
#     @classmethod
#     @jwt_required
#     @UserModel.is_permission("delete_member")
#     def delete(cls, id):
#         try:
#             member = MemberModel.find_by_id(id)
#             if member is None:
#                 return ResponseAPI.send(status_code=404, message=gettext("member_not_found"), data=[])
#
#             member.delete()
#             member.commit_db()
#             return ResponseAPI.send(status_code=201, message=gettext("successful"), data={})
#
#         except Exception:
#             raise CustomException(gettext("server_error"), 500, 2101)
#
#
# class MemberListResource(Resource):
#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('firstname', type=str, location='json')
#         self.reqparse.add_argument('lastname', type=str, location='json')
#         self.reqparse.add_argument('activecartcode', type=str, location='json')
#         # self.reqparse.add_argument('avatar', type=FileStorage, location='files')
#         self.reqparse.add_argument('company', type=str, location='json')
#         self.reqparse.add_argument('nationalcode', type=str, location='json')
#         self.reqparse.add_argument('post', type=str, location='json')
#         self.reqparse.add_argument('status', type=int, location='json')
#         super(MemberListResource, self).__init__()
#
#     # Get List Of Staff
#     @jwt_required
#     @UserModel.is_permission("read_member")
#     @use_kwargs({"q": fields.Str(missing=""), "perPage": fields.Int(missing=10), "page": fields.Int(missing=1),
#                  "sortBy": fields.Str(missing="id"), "sortDesc": fields.Bool(missing=True)}, location="query")
#     def get(self, q, perPage, page, sortBy, sortDesc):
#         try:
#             member_schema = MemberWithAccountSchema(many=True)
#             members = MemberModel.find(q=q, per_page=perPage, page=page, sort_by=sortBy, sort_desc=sortDesc)
#             result = member_schema.dump(members.items)
#             total_record = MemberModel.count()
#             return ResponseAPI.send(status_code=201, message=gettext("successful"),
#                                     data={"members": result, "meta": {"total": total_record}})
#         except Exception as e:
#             raise CustomException(gettext("server_error"), 500, 2101, e.args)
#
#     # Create New Member
#     @jwt_required
#     @UserModel.is_permission("create_member")
#     def post(self):
#         try:
#             member_schema = MemberSchema()
#             req_json = request.get_json()
#             new_member = member_schema.load(req_json)
#
#             new_member.password = Cryptography.hash_password(new_member.password)
#             accounttypes = AccountTypeModel.get_all()
#             new_member.add()
#             new_member.commit_db()
#
#             # Add New Account For Member
#             for accounttype in accounttypes:
#                 account_number = random.randint(100000000, 999999999)
#                 if AccountModel.is_account_exist(account_number):
#                     account_ok = False
#                     for i in range(1, 10):
#                         account_number = random.randint(100000000, 999999999)
#                         if not AccountModel.is_account_exist(account_number):
#                             account_ok = True
#                             break
#                     if not account_ok:
#                         raise CustomException("خطا در ایجاد حساب مالی", 400, 2302)
#
#                 account = AccountModel(account_number=account_number, account_type_id=accounttype.id,
#                                        member_id=new_member.id)
#                 account.add()
#
#             # Add New Card
#             if new_member.activecartcode != "":
#                 card = CardModel(member_id=new_member.id, card_code=new_member.activecartcode)
#                 card.add()
#
#             new_member.commit_db()
#
#             return ResponseAPI.send(status_code=201, message=gettext("staff_created"), data=new_member.id)
#
#         except CustomException as e:
#             raise e
#         except exc.IntegrityError as e:
#             raise CustomException("خطا در مقدار تکراری در دیتابیس، مقدار کد ملی بررسی شود", 400, 2301, e.args)
#         except Exception as e:
#             print(e)
#             raise CustomException(gettext("staff_error_creating"), 500, 2101)
#
#
# class MemberSearchResource(Resource):
#
#     # Search By Cart Number
#     @jwt_required
#     @UserModel.is_permission("read_member")
#     @use_kwargs({"card_code": fields.Str(required=True)})
#     def post(self, card_code):
#         try:
#
#             if card_code is not None:
#                 card = CardModel.find_by_card_code(card_code)
#                 if card is not None:
#                     member_schema = MemberSchema()
#                     member_json = member_schema.dump(card.member)
#                     return ResponseAPI.send(status_code=200, message=gettext("data_get"), data=member_json)
#                 return ResponseAPI.send(status_code=404, message=gettext("staff_error_findcart"))
#             return CustomException(message=gettext("bad_request"), status=400, code=2102)
#         except Exception:
#             raise CustomException(gettext("server_error"), 500, 2101)
#
#
# class MemberAddCardResource(Resource):
#
#     # Add Cart
#     @jwt_required
#     @UserModel.is_permission("read_member")
#     @use_kwargs({"card_code": fields.Str(required=True)})
#     def post(self, card_code, member_id):
#         try:
#             if card_code is not None:
#                 member = MemberModel.find_by_id(member_id)
#                 if member is not None:
#                     card_schema = CardSchema()
#                     print(member.id)
#                     new_card = card_schema.load({"card_code": card_code})
#                     new_card.member = member
#                     new_card.add()
#                     new_card.commit_db()
#                     card_json = card_schema.dump(new_card)
#                     return ResponseAPI.send(status_code=200, message=gettext("card_created"), data=card_json)
#                 return ResponseAPI.send(status_code=404, message=gettext("member_not_found"))
#             return CustomException(message=gettext("bad_request"), status=400, code=2102)
#
#         except exc.IntegrityError:
#             raise CustomException("شماره کارت تکراری است. این کارت برای شخص دیگری ثبت شده است.", 400, 2408)
#         except Exception as e:
#             raise CustomException(gettext("server_error"), 500, 2101, e.args)
#
#     @jwt_required
#     @UserModel.is_permission("read_member")
#     @use_kwargs({"card_code": fields.Str(required=True)})
#     def delete(self, card_code, member_id):
#         try:
#             card = CardModel.find_by_card_code(card_code)
#             if card is not None:
#                 if card.member_id == member_id:
#                     card.delete_from_db()
#                     card.commit_db()
#                     return ResponseAPI.send(status_code=200, message=gettext("card_deleted"))
#                 return ResponseAPI.send(status_code=404, message=gettext("member_not_found"))
#             return CustomException(message=gettext("bad_request"), status=400, code=2102)
#
#         except exc.IntegrityError:
#             raise CustomException("شماره کارت تکراری است. این کارت برای شخص دیگری ثبت شده است.", 400, 2408)
#         except Exception as e:
#             raise CustomException(gettext("server_error"), 500, 2101, e.args)
