import json
from functools import wraps
from urllib.request import urlopen

from flask import _request_ctx_stack, request
from jose import ExpiredSignatureError, JWTError, jwt

import config

AUTH0_DOMAIN = config.AUTH0_DOMAIN
ALGORITHMS = config.ALGORITHMS
API_AUDIENCE = config.AUTH0_AUDIENCE

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    # Check for Authorization
    co_auth = request.headers.get('Authorization', None)

    if not co_auth:
        raise AuthError({
            'code': '401 Unauthorized',
            'description': 'You are not authorized, Header missing'
        }, 401)

    # Split bearer and the token
    co_bearer_split = co_auth.split(' ')

    if len(co_bearer_split) != 2 or not co_bearer_split:
        raise AuthError({
            'code': '401 Unauthorized',
            'description': 'You are not authorized to make this request.'
        }, 401)

    elif len(co_bearer_split) == 1:
        raise AuthError({
            'code': '401 Unauthorized',
            'description': 'Token not found'
        }, 401)

    elif len(co_bearer_split) > 2:
        raise AuthError({
            'code': '401 Unauthorized',
            'description': 'Invalid Token'
        }, 401)

    elif co_bearer_split[0].lower() != 'bearer':
        raise AuthError({
            'code': '401 Unauthorized',
            'description': 'Header didn\'t start with bearer.'
        }, 401)

    token = co_bearer_split[1]

    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': '400 Bad Request',
            'description': 'A bad request was made'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': '403 Forbidden',
            'description': 'Your request is forbidden because you don\'t have the permission to perform this task'
        }, 403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': '401 Unauthorized',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Verification for RSA Key
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )
            return payload

    # Failure during verification of RSA Key
        except ExpiredSignatureError:
            raise AuthError({
                'code': '401 Unauthorized',
                'description': 'Expired Token.'
            }, 401)

        except JWTError:
            raise AuthError({
                'code': '401 Unauthorized',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': '400 Bad Request',
                'description': 'Unable to parse authentication token.'
            }, 400)

    _request_ctx_stack.top.current_user = payload

    return verify_decode_jwt(token)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
