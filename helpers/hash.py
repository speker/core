# -*- coding: utf-8 -*-
import secrets
import uuid
import bcrypt
import hashlib
import string
import random

from core.utilities.jwt import (
    JWT,
    jwk_from_pem
)
from core.helpers.presenter import Presenter


class Hash:
    jwt = JWT()

    @staticmethod
    def get_uuid():
        return uuid.uuid4()

    @staticmethod
    def get_secret(length):
        return secrets.token_hex(length)

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(rounds=12)).decode("utf-8")

    @staticmethod
    def verify_password(user_password, db_password):
        return bcrypt.checkpw(bytes(user_password, 'utf-8'), bytes(db_password, 'utf-8'))

    @staticmethod
    def generate_jwt(aud, sub, jti, now, exp):

        payload = {
            'iss': 'auth.reactor.io',
            'sub': sub,
            'aud': aud,
            'exp': exp.timestamp(),
            'iat': now.timestamp(),
            'jti': str(jti)
        }
        with open(str(Presenter().get_project_root()) + '/core/certs/rsa_private_key.pem', 'rb') as fh:
            signing_key = jwk_from_pem(fh.read())

        jwt_token = Hash.jwt.encode(payload, signing_key, 'RS512')
        return jwt_token

    @staticmethod
    def check_jwt(token):
        try:
            with open(str(Presenter().get_project_root()) + '/core/certs/rsa_public_key.pem', 'rb') as fh:
                verifying_key = jwk_from_pem(fh.read())
            message_received = Hash.jwt.decode(token, verifying_key)
            return message_received
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def password_generator(size=8, chars=string.ascii_letters + string.digits + string.punctuation):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def ldap_password_generator():
        special_char = "!.+%&*-_"
        pwlist = ([random.choice(special_char),
                   random.choice(string.digits),
                   random.choice(string.ascii_lowercase),
                   random.choice(string.ascii_uppercase),
                   ]
                  + [random.choice(string.ascii_lowercase
                                   + string.ascii_uppercase
                                   + special_char
                                   + string.digits) for i in range(10)])
        random.shuffle(pwlist)
        return ''.join(pwlist)
