from typing import Union, Dict

from src.db import sqlAlchemydb as db
from src.models.base.baseModel import TimestampMixin, BaseModel


PermissionJSON = Dict[str, Union[int, str]]

roles_to_permissions = db.Table(
    "roles_to_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id")),
)


class PermissionModel(TimestampMixin, BaseModel):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)

