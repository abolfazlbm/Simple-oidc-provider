# from flask import Blueprint
# from flask_restful import Api
#
# from app.resources.main.device import DeviceTransactionsCheckResource
# from app.resources.main.member import MemberResource, MemberListResource, MemberSearchResource, MemberAddCardResource
# from app.resources.main.transactions import MemberTransactionsResource, \
#     MemberLastTransactionsResource, MemberGroupTransactionsResource, TransactionsResource
#
# MEMBER_BLUEPRINT = Blueprint("Member", __name__)
# api = Api(MEMBER_BLUEPRINT)
#
# # Staff
# # api.add_resource(MemberResource, "/staff/<int:id>")
# # api.add_resource(MemberTransactionsResource, "/staff/<int:userid>/transactions")
# # api.add_resource(MemberListResource, "/staff")
# # api.add_resource(MemberSearchResource, "/staff/search")
# # api.add_resource(MemberGroupTransactionsResource, "/staff/transaction")
# # api.add_resource(MemberTransactionsCheckResource, "/staff/transaction/check")
# # api.add_resource(MemberLastTransactionsResource, "/staff/transaction/last/<cartid>")
#
# # Member
# api.add_resource(MemberResource, "/member/<int:id>")
# api.add_resource(MemberTransactionsResource, "/member/<int:userid>/transactions")
# api.add_resource(MemberListResource, "/member")
# api.add_resource(MemberSearchResource, "/member/search")
# api.add_resource(MemberGroupTransactionsResource, "/member/transaction")
# api.add_resource(DeviceTransactionsCheckResource, "/device/transaction/check")
# api.add_resource(MemberLastTransactionsResource, "/member/transaction/last/<cartcode>")
#
# # Card
# api.add_resource(MemberAddCardResource, "/member/<int:member_id>/card")
#
# # Transaction
# api.add_resource(TransactionsResource, "/transactions")
