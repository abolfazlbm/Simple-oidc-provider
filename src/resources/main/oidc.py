from flask import render_template, redirect, url_for, request, session
from flask_restful import Resource
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from src.errors import CustomException
from src.repositories.auth.auth import AuthHandler, TokenHandler
from src.repositories.datastore.memorydb import Challenge
from src.response import ResponseAPI
from src.routes.pages import PAGES_BLUEPRINT
from src.utils.strings import gettext


class AuthorizationResource(Resource):

    # Get the Authorization code
    @use_kwargs({"response_type": fields.Str(missing="code"),
                 "client_id": fields.Str(required=True,
                                         validate=[validate.Length(min=1, max=80)]),
                 "redirect_uri": fields.Str(required=True,
                                            validate=[validate.Length(min=1, max=250)]),
                 "scope": fields.Str(missing="profile"),
                 "state": fields.Str(missing=""), "code_challenge": fields.Str(missing=""),
                 "code_challenge_method": fields.Str(missing="")}, location="query")
    def get(self, response_type, client_id, redirect_uri, scope, state, code_challenge, code_challenge_method):
        try:
            a = Challenge(response_type, client_id, redirect_uri, scope, state, code_challenge, code_challenge_method)
            a.save()
            return redirect(url_for("Pages.login", challenge_id=a.challenge_id))

        except Exception as e:
            raise CustomException(gettext("server_error"), 500, 2201, e.args)


class TokenResource(Resource):
    @use_kwargs({"grant_type": fields.Str(missing="authorization_code"),
                 "client_id": fields.Str(required=True,
                                         validate=[validate.Length(min=1, max=80)]),
                 "client_secret": fields.Str(required=True,
                                         validate=[validate.Length(min=1, max=80)]),
                 "redirect_uri": fields.Str(required=True,
                                            validate=[validate.Length(min=1, max=250)]),
                 "code": fields.Str(required=True,
                                    validate=[validate.Length(min=1, max=250)]),
                 "code_verifier": fields.Str(missing="")}, location="json")
    def post(self, grant_type, client_id,client_secret,code, redirect_uri,  code_verifier):
        try:
            b = TokenHandler(grant_type, client_id, client_secret, code, redirect_uri, code_verifier)
            tokens = b.generate_token()
            if tokens is not None:
                return ResponseAPI.send(status_code=200, message=gettext("token_success"), data=tokens)

            raise CustomException(gettext("invalid_code"), 403, 10801)

        except Exception as e:
            raise CustomException(gettext("server_error"), 500, 2201, e.args)


@PAGES_BLUEPRINT.route("/login/<challenge_id>", methods=["GET", "POST"])
def login(challenge_id):
    if request.method == "POST":
        # getting input with name = fname in HTML form
        username = request.form.get("username")
        password = request.form.get("password")
        challenge_id = request.form.get("challenge")
        auth_handler = AuthHandler(challenge_id)
        if auth_handler.login(username, password):
            challenge = auth_handler.get_challenge_with_code()
            if challenge is not None:
                session['username'] = username
                return redirect(
                    challenge.redirect_uri + "?code=" + challenge.authorization_code + "&state=" + challenge.state)
        return render_template(
            "login.html",
            challenge_id=challenge_id,
            description="Login Single Sign On",
            login_state=gettext("user_invalid_credentials")
        )

    if 'username' in session:
        username = session['username']
        auth_handler = AuthHandler(challenge_id, username)
        challenge = auth_handler.get_challenge_with_code()
        if challenge is not None:
            return redirect(
                challenge.redirect_uri + "?code=" + challenge.authorization_code + "&state=" + challenge.state)
        session.pop('username', None)

    return render_template(
        "login.html",
        challenge_id=challenge_id,
        description="Login Single Sign On",
        login_state=None
    )
