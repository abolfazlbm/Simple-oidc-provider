"""
Defines the blueprint for the auth
"""
from flask import jsonify
from flask_jwt_extended import JWTManager

from app.blacklist import BLACKLIST
from app.errors import CustomException
from app.resources.auth.blacklist_helpers import is_token_revoked


class Auth:

    def __init__(self, app):
        jwt = JWTManager(app)

        # This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
        # @jwt.token_in_blacklist_loader
        # def check_if_token_in_blacklist(decrypted_token):
        #     return decrypted_token["jti"] in BLACKLIST

        @jwt.token_in_blacklist_loader
        def check_if_token_revoked(decoded_token):
            return is_token_revoked(decoded_token)

        @jwt.expired_token_loader
        def custom_expired_token_loader_callback():
            return jsonify({
                'status': 401,
                'message': "توکن منقصی شده است.",
                'data': {
                    'code': 4010
                }
            }), 401

        @jwt.revoked_token_loader
        def custom_revoked_token_loader_callback():
            return jsonify({
                'status': 401,
                'message': "توکن باطل شده است. دوباره وارد شوید.",
                'data': {
                    'code': 4010
                }
            }), 401

        @jwt.needs_fresh_token_loader
        def custom_fresh_token_loader_callback():
            return jsonify({
                'status': 401,
                'message': "نیاز به ورود مجدد. لطفا دوباره وارد شوید.",
                'data': {
                    'code': 4020
                }
            }), 401
