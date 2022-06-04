from datetime import datetime

# from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound

from src.models.tokenblacklist import TokenBlacklist


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param encoded_token:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token['identity']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db_token.save_to_db()


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        token = TokenBlacklist.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    return TokenBlacklist.query.filter_by(user_identity=str(user_identity)).all()


def revoke_token(user_identity, jti=None):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        if jti is not None:
            token = TokenBlacklist.find_by_jti_user(user_identity=user_identity, jti=jti)
            token.revoked = True
            token.save()
        else:
            TokenBlacklist.revoke_by_user(user_identity=user_identity)

    except NoResultFound:
        print("Could not find the token {}".format(jti))


# def unrevoke_token(token_id, user):
#     """
#     Unrevokes the given token. Raises a TokenNotFound error if the token does
#     not exist in the database
#     """
#     try:
#         token = TokenBlacklist.query.filter_by(id=token_id, user_identity=user).one()
#         token.revoked = False
#         token.save_to_db()
#     except NoResultFound:
#         print("Could not find the token {}".format(token_id))
#

def prune_database():
    """
    Delete tokens that have expired from the database.

    How (and if) you call this is entirely up you. You could expose it to an
    endpoint that only administrators could call, you could run it as a cron,
    set it up with flask cli, etc.
    """
    now = datetime.now()
    expired = TokenBlacklist.query.filter(TokenBlacklist.expires < now).all()
    for token in expired:
        token.delete_from_db()
