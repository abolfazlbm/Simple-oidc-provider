from marshmallow import fields

from src.utils.ma import ma
from src.models.role import RoleModel
from src.models.schema.permission import PermissionSchema


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel

    permissions = fields.Pluck(PermissionSchema, "name", many=True)
