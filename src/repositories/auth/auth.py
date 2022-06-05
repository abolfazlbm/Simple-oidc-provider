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

    def check_auth(self):
        if not self.challenge or not self.user:
            return False
        self.client = ClientModel.find_by_client_id(self.challenge.client_id)
        if self.client is None:
            return False
        return True

    def get_challenge_with_code(self) -> Challenge:
        """
        Method that generates an authorization code
        :param:
        :return:
        """
        try:
            if self.check_auth():
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
