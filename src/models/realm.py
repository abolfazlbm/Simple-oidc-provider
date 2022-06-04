from src.db import sqlAlchemydb as db
from .base.baseModel import BaseModel, TimestampMixin


class RealmModel(TimestampMixin, BaseModel):
    __tablename__ = "realms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=True)

    clients = db.relationship('ClientModel', backref='realm', lazy=True)
    users = db.relationship('UserModel', backref='realm', lazy=True)

