"""
Defines the blueprint for the auth
"""
from flask import jsonify
from flask_jwt_extended import JWTManager

from src.blacklist import BLACKLIST
from src.errors import CustomException
from src.resources.auth.blacklist_helpers import is_token_revoked
from src.response import ResponseAPI
from src.utils.strings import gettext


class Auth:

    def __init__(self, app):
        jwt = JWTManager(app)

        # This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
        # @jwt.token_in_blacklist_loader
        # def check_if_token_in_blacklist(decrypted_token):
        #     return decrypted_token["jti"] in BLACKLIST

        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
            return is_token_revoked(jwt_payload)

        @jwt.expired_token_loader
        def custom_expired_token_loader_callback(jwt_header, jwt_payload):
            return ResponseAPI.send(status_code=401, message=gettext("token_expired"),data={"code": 4010})

        @jwt.revoked_token_loader
        def custom_revoked_token_loader_callback(jwt_header, jwt_payload):
            return ResponseAPI.send(status_code=401, message=gettext("token_revoked"), data={"code": 4011})

        @jwt.needs_fresh_token_loader
        def custom_fresh_token_loader_callback(jwt_header, jwt_payload):
            return ResponseAPI.send(status_code=401, message=gettext("login_again"), data={"code": 4012})
