from src.utils.ma import ma
from src.models.user import UserModel
from src.models.schema.role import RoleSchema
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

    roles = fields.Pluck(RoleSchema, "name", many=True)
