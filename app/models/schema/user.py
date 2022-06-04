from app.utils.ma import ma
from app.models.user import UserModel
from app.models.schema.role import RoleSchema
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

    roles = fields.Pluck(RoleSchema, "name", many=True)
