from flask import Blueprint
from flask_restful import Api

from src.resources.main.oidc import AuthorizationResource, TokenResource

OIDC_BLUEPRINT = Blueprint("OIDC", __name__)
api = Api(OIDC_BLUEPRINT)

# OpenID Connect
api.add_resource(AuthorizationResource, "/oidc/authorize")
api.add_resource(TokenResource, "/oidc/token")
# api.add_resource(UserinfoResource, "/oidc/userinfo")
# api.add_resource(LogoutResource, "/oidc/logout")


