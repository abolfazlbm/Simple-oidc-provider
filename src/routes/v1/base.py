from flask import Blueprint
from flask_restful import Api

from src.resources.auth.login import UserLoginResource, TokenRefreshResource, SignoutResource, Singout2Resource
from src.resources.auth.user import UserListResource, UserResource, UserChangePassResource

BASE_BLUEPRINT = Blueprint("base", __name__)
api = Api(BASE_BLUEPRINT)
# Auth
api.add_resource(SignoutResource, "/signout")
api.add_resource(Singout2Resource, "/signout2")
api.add_resource(UserLoginResource, "/login")
api.add_resource(TokenRefreshResource, "/refresh-token")

# User
api.add_resource(UserChangePassResource, "/changepassword")
api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/user/<int:id>")

