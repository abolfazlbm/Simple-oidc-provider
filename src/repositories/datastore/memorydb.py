# This is temporary alternative for Redis DB
import uuid

from src.utils.singleton import Singleton


class Challenge:
    def __init__(self, response_type, client_id, redirect_uri, scope, state, code_challenge,
                 code_challenge_method):
        self.response_type = response_type
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method
        self.challenge_id = uuid.uuid4().hex
        self.authorization_code = None
        self.authorization_code_expires = None

    def save(self):
        ChallengeList().add_challenge(new_challenge=self)
        return self


class ChallengeList(metaclass=Singleton):

    def __init__(self):
        self.challenge = {}

    def add_challenge(self, new_challenge: Challenge):
        self.challenge[new_challenge.challenge_id] = new_challenge

    def pop_challenge(self, challenge_id):
        if challenge_id in self.challenge:
            return self.challenge.pop(challenge_id)
        return None

    def get_challenge(self, challenge_id):
        if challenge_id in self.challenge:
            return self.challenge[challenge_id]
        return None

    def pop_challenge_by_auth_code(self, authorization_code):
        for challenge in self.challenge.values():
            if challenge.authorization_code == authorization_code:
                return self.challenge.pop(challenge.challenge_id)
        return None