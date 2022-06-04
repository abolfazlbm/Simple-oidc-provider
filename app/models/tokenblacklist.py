from app.db import sqlAlchemydb as db


class TokenBlacklist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }

    @classmethod
    def find_by_username(cls, username: str, deleteitem=False) -> "UserModel":
        if deleteitem:
            return cls.query.filter_by(username=username, deleted_at=not None).first()
        else:
            return cls.query.filter_by(username=username, deleted_at=None).first()

    @classmethod
    def revoke_by_user(cls, user_identity: str) -> "UserModel":
        cls.query.filter_by(user_identity=str(user_identity)).update({cls.revoked: True})
        db.session.commit()

    @classmethod
    def find_by_jti_user(cls, user_identity: str , jti: str) -> "UserModel":
        return cls.query.filter_by(jti=jti, user_identity=str(user_identity)).one()

    def save(self):
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
