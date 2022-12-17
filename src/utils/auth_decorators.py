from jose import jwt
import os
from functools import wraps
from flask import jsonify, request, g
from .errors import *
import json
import config
import sys
# from repositories import UserRepository
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-attahiru-kamba-fsnd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'gomerceRS'


def get_token_auth_header():
    """ Get token from the request header """
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers.get('x-access-token', None)
    if 'Authorization' in request.headers:
        auth = request.headers.get('Authorization', None)
        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise Unauthorized('Authorization header must start with "Bearer"')
        elif len(parts) == 1:
            raise Unauthorized('Token not found.')
        elif len(parts) > 2:
            raise Unauthorized('Authorization header must be bearer token.')
        token = parts[1]
    if not token:
        raise Unauthorized(
            'Authorization or x-access-token header is expected.')
    return token


# def token_required(f):
#     """ Verify token for restricted routes"""
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = get_token_auth_header()

#         try:
#             data = jwt.decode(
#                 token, config.SECRET_KEY, algorithms=["HS256"])
#             current_user = UserRepository.get(user_id=data['user_id'])
#         except Unauthorized as e:
#             return jsonify({'message': e.message}), e.code
#         except Exception:
#             return jsonify({'message': "Unauthorized"}), 401

#         return f(current_user, *args, **kwargs)
#     return decorator


# def seller_auth_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         token = request.headers.get("x-access-token", None)
#         secret = os.environ.get("SECRET_KEY")
#         if token:
#             try:
#                 payload = jwt.decode(token, secret, algorithms=["HS256"])
#                 user_id = payload["id"]
#                 if user_id:
#                     g.user = SellerRepository.query.filter(
#                         SellerRepository.id == user_id).one()
#                     return func(*args, **kwargs)

#             except AccessDenied:
#                 return jsonify({
#                 "error": "No user found with provided token"}), 403
#             except Exception as e:
#                 return func(*args, **kwargs)
#         return func(*args, **kwargs)

#     return wrapper


def check_permissions(permission, payload):
    '''
    implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission
    string is not in the payload permissions array
    return true otherwise
    '''

    # checks if the payload has permissions within
    if 'permissions' not in payload:
        raise AccessDenied('Permission not included')

    # checks if the claimed permission is indeed true
    if permission not in payload['permissions']:
        raise AccessDenied('Permission not included')

    return True


def verify_decode_jwt(token):
    '''
    implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    '''

    # get the public key from auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # gets the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # select the key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AccessDenied('Authotization malformed')

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # verify the key
    if rsa_key:
        try:
            # using the key, we valide the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        # error if jwt is expired
        except jwt.ExpiredSignatureError:
            raise Unauthorized('Token expired')

        # error if claims are not valid
        except jwt.JWTClaimsError:
            raise Unauthorized(
                'Incorrect claims. Please, check the audience and issuer.')

        # error if header is invalid
        except Exception:
            raise AccessDenied('Unable to parse authentication token.')

    # error if no matching key was found
    raise AccessDenied('Unable to find the appropriate key.')


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
