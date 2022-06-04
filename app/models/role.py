from typing import Dict, Union

from app.db import sqlAlchemydb as db
from app.models.base.baseModel import TimestampMixin, BaseModel
from app.models.permission import roles_to_permissions, PermissionModel

RoleJSON = Dict[str, Union[int, str]]


users_to_roles = db.Table(
    "users_to_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


class RoleModel(TimestampMixin, BaseModel):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)
    permissions = db.relationship(PermissionModel, secondary=roles_to_permissions, lazy="dynamic")

    @classmethod
    def find_by_name(cls, _name: str) -> "RoleModel":
        return cls.query.filter_by(name=_name).first()
