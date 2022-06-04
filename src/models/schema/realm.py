from marshmallow import EXCLUDE, post_load

from src.models.realm import RealmModel
from src.utils.ma import ma


class RealmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RealmModel
        load_only = ()
        dump_only = {"id", "created_at", "updated_at"}
        unknown = EXCLUDE

    @post_load
    def make_realm(self, data, **kwargs):
        return RealmModel(**data)
