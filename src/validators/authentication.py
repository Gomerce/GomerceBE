"""auth_access.py

Keyword arguments:
argument -- description
Return: return_description
"""

from functools import wraps

# import jwt
from flask import request

from utils import decode_auth_token

# import config


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_token = None

        if "Authorization" in request.headers:
            request_header = request.headers["Authorization"]
            auth_token = request_header.split(" ")[1].encode('utf-8')

        if not auth_token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        try:
            current_user = decode_auth_token(auth_token)

            if current_user == "Signature expired. Please log in again.":
                return {
                    "message": "Signature expired. Please log in again.",
                    "current_user": "No current user",
                    "error": "Unauthorized"
                }, 401

            if current_user == "Invalid token. Please log in again.":
                return {
                    "message": "Invalid token. Please log in again.",
                    "current_user": "No current user",
                    "error": "Unauthorized"
                }, 401

        except Exception as e:
            return {
                "message": "Something went wrong",
                "current_user": "No current user",
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated
