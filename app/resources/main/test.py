from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import parser

from app.errors import CustomException
from app.response import ResponseAPI


class Test(Resource):
    def get(self):
        try:
            # members = MemberModel.find_all()
            # accounttypes = AccountTypeModel.get_all()
            # for m in members:
            # for accounttype in accounttypes:
            #     account_number = random.randint(100000000, 999999999)
            #     while AccountModel.is_account_exist(account_number):
            #         account_number = random.randint(100000000, 999999999)
            #     account = AccountModel(account_number=account_number, account_type_id=accounttype.id,
            #                            member_id=m.id, credit=m.credit)
            #     account.add()
            #     print(account.account_number, account.credit)
            # ----
            # account = AccountModel.find_by_memberid_and_typeid(m.id, 3)
            # account.credit = 0
            # print(account.account_type_id, account.credit)
            # ----
            # newcard = CardModel(card_code=m.activecartcode, member_id=m.id, is_active=True,status=1,type=1)
            # newcard.add()
            # print(newcard.card_code, newcard.member_id)
            # -----
            # print(m.id)

            # with open('data3.json') as json_file:
            #     data = json.load(json_file)
            #
            #     # Print the type of data variable
            #     # print("Type:", type(data))
            #
            #     for i in data["RECORDS"]:
            #         member = MemberModel.find_by_id(i["staff_id"])
            #         if member is not None:
            #             account = AccountModel.find_by_memberid_and_typeid(member.id, 2)
            #             if account is not None:
            #                 print(i["id"], account.account_number, account.credit, member.id)
            #                 trancode = i["transactioncode"]
            #                 if trancode is None:
            #                     trancode = generate_transaction_code()
            #                     print("New GENERATED CODE:", trancode)
            #                 newtran = TransactionModel(transaction_code=trancode, action=i["action"], date=i["date"],
            #                                            amount=i["amount"], member_id=member.id,
            #                                            account_number=account.account_number,
            #                                            description=i["description"])
            #                 print(newtran.transaction_code)
            #                 newtran.add()

            # MemberModel.find_by_id(44).commit_db()
            # data = []
            # group = GroupModel.find_by_id(3)
            # #member = MemberModel(firstname='Ali', lastname='Tavakoli', nationalcode='11124672901', status=1,credit=0)
            # members = MemberModel.find_all()
            # for member in members:
            #     print(member.firstname)
            #     if member in group.members:
            #         print('member in group')
            #     else:
            #         print('member not in group')
            #         group.members.append(member)
            #
            # group.add()
            # group.commit_db()

            # groups = MemberModel.find_by_id(3).groups
            # for group in groups :
            #     data.append(group.title)
            # organization = OrganizationModel(title='test', description='test')
            # organization.add()
            # organization.commit_db()
            # organization = OrganizationModel.find_by_id(1)
            # organization.update({'title': 'Jahad', 'description': 'Khorasan Razavi 1'})
            # organization.commit_db()
            # accountType = AccountTypeModel(name="عمومی", postfix="Rial", status=1,organization=organization)
            # accountType.add()
            # accountType.commit_db()
            #
            # ss = AccountTypeModel.find_by_id(2)
            # ss.name = "Special"
            # ss.commit_db()
            # data = ss.name
            # sp = ServiceProviderModel.find_by_id(1)
            # sp.update({'name': 'Service 33'})
            # sp.name = 'Service 11'
            # print("***********************")
            # print(sp.name)
            # sp.add()
            # sp.commit_db()

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
