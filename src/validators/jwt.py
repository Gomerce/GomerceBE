
"""jwt.py

Keyword arguments:
argument -- auth_token
Return: integer|string
"""

from datetime import datetime, timedelta

import jwt

import config


def encode_auth_token(id, first_name, last_name):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=3600),  # noqa
            'iat': datetime.utcnow(),
            'sub': id,
            'name': f'{first_name} {last_name}'
        }
        return jwt.encode(
            payload,
            config.SECRET_KEY,
            algorithm=config.AUTH_ALGORITHMS
        )
    except Exception as e:
        return e


@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, config.SECRET_KEY,
                             algorithms=[config.AUTH_ALGORITHMS])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
