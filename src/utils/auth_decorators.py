
from jose import jwt
import os
#import jwt
from functools import wraps
from flask import jsonify, request, g
from .errors import *
import config
import sys
#from repositories import UserRepository
from repositories import SellerRepository


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


def token_required(f):
    """ Verify token for restricted routes"""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = get_token_auth_header()

        try:
            data = jwt.decode(
                token, config.SECRET_KEY, algorithms=["HS256"])
            current_user = UserRepository.get(user_id=data['user_id'])
        except Unauthorized as e:
            return jsonify({'message': e.message}), e.code
        except Exception:
            return jsonify({'message': "Unauthorized"}), 401

        return f(current_user, *args, **kwargs)
    return decorator


def seller_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-access-token", None)
        secret = os.environ.get("SECRET_KEY")
        if token:
            try:
                payload = jwt.decode(token, secret, algorithms=["HS256"])
                user_id = payload["id"]
                if user_id:
                    g.user = SellerRepository.query.filter(
                        SellerRepository.id == user_id).one()
                    return func(*args, **kwargs)

            except AccessDenied:
                return jsonify({"error": "No user found with provided token"}), 403
            except Exception as e:
                return func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper
