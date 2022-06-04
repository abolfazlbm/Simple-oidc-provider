from marshmallow import fields

from app.utils.ma import ma
from app.models.role import RoleModel
from app.models.schema.permission import PermissionSchema


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel

    permissions = fields.Pluck(PermissionSchema, "name", many=True)
