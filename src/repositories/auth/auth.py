import datetime
import uuid

from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt,
                                get_jwt_identity, jwt_required)

from src.errors import CustomException
from src.models.client import ClientModel
from src.models.schema.user import UserSchema
from src.models.user import UserModel
from src.repositories.datastore.memorydb import ChallengeList, Challenge
from src.resources.auth.blacklist_helpers import add_token_to_database
from src.utils.cryptography import Cryptography
from src.utils.strings import gettext


class AuthHandler:
    """
    Class that handles the login process
    """

    def __init__(self, challenge_id, username=None):
        """
        Constructor
        :param challenge_id:
        """
        try:
            self.challenge: Challenge = ChallengeList().pop_challenge(challenge_id)
            self.user = None
            if username is not None:
                self.user = UserModel.find_by_username(username)
            self.client = None

        except Exception as e:
            raise CustomException(gettext("user_not_found"), 403, 10801, e.args)

    def validate(self):
        if not self.challenge or not self.user:
            return False
        self.client = ClientModel.find_by_client_id(self.challenge.client_id)
        if self.client is None:
            return False
        # Temperory Comment
        # if not self.check_valid_return_uri():
        #     return False
        return True

    def get_challenge_with_code(self) -> Challenge:
        """
        Method that generates an authorization code
        :param:
        :return:
        """
        try:
            if self.validate():
                if self.client.realm.id == self.user.realm.id:
                    if self.challenge.authorization_code is None:
                        self.challenge.authorization_code = uuid.uuid4().hex
                        self.challenge.authorization_code_expires = datetime.datetime.now() + datetime.timedelta(
                            minutes=15)
                        ChallengeList().add_challenge(self.challenge)
                        return self.challenge

            return None
        except Exception:
            raise CustomException(gettext("user_not_found"), 403, 1002)

    def login(self, username, password):
        """
        Method that handles the login process
        :param username:
        :param password:
        :return:
        """
        try:
            user = UserModel.find_by_username(username)
            if user is not None:
                if Cryptography.verify_password(user.password, password):
                    self.user = user
                    return True
            return False
        except Exception as e:
            raise CustomException(gettext("user_not_found"), 403, 1003, e.args)

    def check_valid_return_uri(self):
        """
        Method that checks if the redirect uri is valid
        :param:
        :return:
        """
        if self.client.redirect_uri is not None:
            if self.client.redirect_uri == self.challenge.redirect_uri:
                return True
        return False


class TokenHandler:
    """
    Class that handles the token process
    """

    def __init__(self, grant_type, client_id, client_secret, code, redirect_uri, code_verifier):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.grant_type = grant_type
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier
        self.client = None
        self.challenge = None

    def validate(self):
        """
        Method that validates the token request
        :param:
        :return:
        """
        try:
            self.challenge: Challenge = ChallengeList().pop_challenge_by_auth_code(self.code)
            if self.challenge is None:
                return False

            self.client: ClientModel = ClientModel.find_by_client_id(self.client_id)
            if self.client is None:
                return False

            if self.client.client_secret != self.client_secret:
                return False

            # .....
            # Check 'Grant Type' and 'Redirect URI' and 'Code Verifier Algorithm'
            # .....

            if not Cryptography.verify_code_challenge(self.code_verifier, self.challenge.code_challenge,
                                                      self.challenge.code_challenge_method):
                return False
            if self.challenge.authorization_code != self.code:
                return False

            # if self.challenge.authorization_code_expires is not None:
            #     if self.challenge.authorization_code_expires < datetime.datetime.now():
            #         return False

            return True
        except Exception as e:
            print(e.args)
            return False

    def generate_token(self):
        if self.validate():
            expires = datetime.timedelta(minutes=60)
            expires_refresh = datetime.timedelta(days=30)
            access_token = create_access_token(identity=self.client.client_id,
                                               additional_claims={'realm': self.client.realm.name},
                                               expires_delta=expires)
            refresh_token = create_refresh_token(identity=self.client.client_id,
                                                 additional_claims={'realm': self.client.realm.name},
                                                 expires_delta=expires_refresh)
            add_token_to_database(access_token)
            add_token_to_database(refresh_token)
            return {"access_token": access_token, "refresh_token": refresh_token, "expires_in": 3600}
        return None
