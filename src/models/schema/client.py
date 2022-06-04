from marshmallow import fields, EXCLUDE, post_load

from src.models.client import ClientModel
from src.models.schema.role import RoleSchema
from src.utils.ma import ma


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientModel
        load_only = ("password",)
        dump_only = {"id", "created_at", "updated_at"}
        unknown = EXCLUDE

    @post_load
    def make_client(self, data, **kwargs):
        return ClientModel(**data)


class ClientFullSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientModel
        load_only = ("password",)

    roles = fields.Nested(RoleSchema, many=True)

