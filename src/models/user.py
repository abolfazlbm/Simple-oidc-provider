from datetime import datetime
from functools import wraps
from typing import Dict, Union

from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

from src.db import sqlAlchemydb as db
from src.models.base.baseModel import TimestampMixin, BaseModel
from src.models.role import RoleModel
from src.models.role import users_to_roles
from src.response import ResponseAPI
from src.utils.cryptography import Cryptography
from src.utils.strings import gettext

UserJSON = Dict[str, Union[int, str]]


class UserModel(TimestampMixin, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), nullable=True)
    lastname = db.Column(db.String(40), nullable=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=True, unique=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    realm_id = db.Column(db.Integer, db.ForeignKey("realms.id"), nullable=False)

    roles = db.relationship("RoleModel", secondary=users_to_roles, backref='users', lazy="dynamic")

    @classmethod
    def find_by_username(cls, username: str, deleteitem=False) -> "UserModel":
        if deleteitem:
            return cls.query.filter_by(username=username, deleted_at=not None).first()
        else:
            return cls.query.filter_by(username=username, deleted_at=None).first()

    @classmethod
    def find_by_email(cls, email: str, deleteitem=False) -> "UserModel":
        if deleteitem:
            return cls.query.filter_by(email=email, deleted_at=not None).first()
        else:
            return cls.query.filter_by(email=email, deleted_at=None).first()

    @classmethod
    def find_by_id(cls, _id: str, deleteitem=False) -> "UserModel":
        if deleteitem:
            return cls.query.filter_by(id=_id, deleted_at=not None).first()
        else:
            return cls.query.filter_by(id=_id, deleted_at=None).first()

    @classmethod
    def find_all(cls, deleteitem=False):
        if deleteitem:
            return cls.query.filter_by(deleted_at=not None).all()
        else:
            return cls.query.filter_by(deleted_at=None).all()

    @classmethod
    def is_exist_by_username(cls, username: str) -> "boolean":
        result = cls.query.filter_by(username=username).count()
        if result >= 1:
            return True
        return False

    @classmethod
    def is_exist_by_email(cls, email: str) -> "boolean":
        result = cls.query.filter_by(email=email).count()
        if result >= 1:
            return True
        return False

    def resetpassword(self, password: str):
        self.password = Cryptography.hash_password(password)

    @staticmethod
    def is_permission_by_jwt(permission_name: str) -> "boolean":
        claims = get_jwt().get("claims")
        for item in claims["roles"]:
            for i in item["permissions"]:
                if permission_name in i["name"]:
                    return True
        return False

    @staticmethod
    @jwt_required()
    def is_permission_by_db(permission_name) -> "boolean":
        user_id = get_jwt_identity()
        for role in UserModel.find_by_id(user_id).roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False

    @staticmethod
    def is_permission(permission_name):
        def simple_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if UserModel.is_permission_by_db(permission_name):
                    return f(*args, **kwargs)
                return ResponseAPI.send(status_code=403, message=gettext("user_not_permission"))

            return wrapper

        return simple_decorator

    def update_user(self, args):
        if args['firstname'] is not None:
            self.firstname = args['firstname']
        if args['lastname'] is not None:
            self.lastname = args['lastname']
        if args['email'] is not None:
            self.email = args['email']
        if args['username'] is not None:
            self.username = args['username']

        if args['password'] is not None and args['password'] != "":
            self.resetpassword(args['password'])

        if args['role'] is not None:
            newrolename = args['role']
            oldrole = self.roles[0]
            if oldrole != newrolename:
                newrole = RoleModel.find_by_name(newrolename)
                self.roles.remove(oldrole)
                self.roles.append(newrole)

        self.save_to_db()

    def delete(self):
        self.deleted_at = str(datetime.now())
        self.save_to_db()

    # def update(self, args):
    #     super().update(args)
    #     print(args)
    #     if 'password' in args and args['password'] is not None:
    #         print(args['password'])
    #         self.password = Cryptography.hash_password(args['password'])
    #     self.commit_db()
