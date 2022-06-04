from marshmallow import EXCLUDE, post_load

from app.models.realm import RealmModel
from app.utils.ma import ma


class RealmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RealmModel
        load_only = ()
        dump_only = {"id", "created_at", "updated_at"}
        unknown = EXCLUDE

    @post_load
    def make_realm(self, data, **kwargs):
        return RealmModel(**data)
