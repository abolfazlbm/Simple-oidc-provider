import base64
import hashlib
import uuid

import bcrypt


class Cryptography:

    @staticmethod
    def hash_password(password: str) -> "String":
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password_hash.decode('utf-8')

    @staticmethod
    def verify_password(password, password_hash: str) -> "Boolean":
        return bcrypt.checkpw(password_hash.encode('utf-8'), password.encode('utf-8'))

    @staticmethod
    def verify_code_challenge(code_verify, code_challenge, code_challenge_method="SHA256") -> "Boolean":
        if code_challenge_method == "SHA256":
            print(hashlib.sha256(code_verify.encode('ascii')).hexdigest())
            print(code_challenge)
            if hashlib.sha256(code_verify.encode('ascii')).hexdigest() == code_challenge:
                return True

    @staticmethod
    def rand_uuid() -> "String":
        return uuid.uuid4().hex
