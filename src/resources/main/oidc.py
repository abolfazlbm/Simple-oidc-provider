from flask import render_template, redirect, url_for
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

import src.resources.main.oidc
from src.errors import CustomException
from src.repositories.datastore.memorydb import Challenge
from src.routes.pages import PAGES_BLUEPRINT
from src.utils.strings import gettext


class AuthorizationResource(Resource):

    # Get the Authorization code
    @use_kwargs({"response_type": fields.Str(missing="code"),
                 "client_id": fields.Str(required=True,
                                         validate=[validate.Length(min=1,
                                                                   max=80)]),
                 "redirect_uri": fields.Str(required=True,
                                            validate=[validate.Length(min=1, max=250)]),
                 "scope": fields.Str(missing="profile"),
                 "state": fields.Str(missing=""), "code_challenge": fields.Str(missing=""),
                 "code_challenge_method": fields.Str(missing="")}, location="query")
    def get(self, response_type, client_id, redirect_uri, scope, state, code_challenge, code_challenge_method):
        try:
            a = Challenge(response_type, client_id, redirect_uri, scope, state, code_challenge, code_challenge_method)
            a.save()
            return redirect("/login/"+a.challenge_id)
            # return ResponseAPI.send(status_code=200, message=gettext("success"), data={"code": a.challenge_id})

        except Exception as e:
            raise CustomException(gettext("server_error"), 500, 2201, e.args)


@PAGES_BLUEPRINT.route("/login/<challenge_id>", methods=["GET"])
def login(challenge_id):
    return render_template(
        "login.html",
        challenge_id=challenge_id,
        description="Login Single Sign On",
    )
