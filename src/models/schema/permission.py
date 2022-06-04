from src.models.permission import PermissionModel
from src.utils.ma import ma


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PermissionModel
        include_fk = True


