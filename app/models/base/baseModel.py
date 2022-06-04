from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy import inspect, or_
from sqlalchemy.ext.declarative import declared_attr

from app.db import sqlAlchemydb as db
from datetime import datetime


class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    @declared_attr
    def deleted_at(cls):
        return db.Column(db.DateTime, nullable=True)


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted_at=None) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(self._only_full_mapper_zero('get'),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None


class BaseModel(db.Model):
    __abstract__ = True
    query_class = QueryWithSoftDelete

    @classmethod
    def find(cls, per_page=10, page=1, sort_by="id", sort_desc=True):

        query: Model.query = cls.query
        if sort_desc is True:
            query = query.order_by(getattr(cls, sort_by).desc())
        else:
            query = query.order_by(getattr(cls, sort_by).asc())
        total_record = query.count()
        return query.paginate(page, per_page, False), total_record

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def add(self) -> None:
        try:
            db.session.add(self)
        except Exception as e:
            db.session.rollback()
            raise

    def commit_db(self) -> None:
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def delete(self) -> None:
        try:
            self.deleted_at = datetime.utcnow()
        except:
            db.session.rollback()
            raise

    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)

        except:
            db.session.rollback()
            raise

    def update(self, args):
        try:
            mapper = inspect(self)
            for column in mapper.attrs:
                print(column.key)
                if args.get(column.key) is not None:
                    setattr(self, column.key, args.get(column.key))

        except:
            raise Exception("Error update Mapping")
