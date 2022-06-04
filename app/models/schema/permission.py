from app.models.permission import PermissionModel
from app.utils.ma import ma


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PermissionModel
        include_fk = True


