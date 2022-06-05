from src.db import sqlAlchemydb as db
from .base.baseModel import TimestampMixin, BaseModel
from .role import RoleModel
from .realm import RealmModel


class ClientModel(TimestampMixin, BaseModel):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.String(80), nullable=False, unique=True)
    client_secret = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    valid_redirect_uri = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    realm_id = db.Column(db.Integer, db.ForeignKey("realms.id"), nullable=False)
    roles = db.relationship(RoleModel, backref='client', lazy=True)

    @classmethod
    def find_by_client_id(cls, client_id: str, deleteitem=False) -> "ClientModel":
        if deleteitem:
            return cls.query.filter_by(client_id=client_id, deleted_at=not None).first()
        else:
            return cls.query.filter_by(client_id=client_id, deleted_at=None).first()
