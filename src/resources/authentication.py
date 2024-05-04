"""authentication_authorisation.py

Keyword arguments:
argument -- description
Return: return_description
"""

from datetime import datetime, timedelta

from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from models import Customer
from utils.errors import Forbidden, InternalServerError
from utils import parse_params


class AuthenticationResource(Resource):

    """  """

    # Login Details

    @staticmethod
    @parse_params(
        Argument("email", location="json", required=True,
                 help="The email address of the customer"),
        Argument("password", location="json", required=True,
                 help="The password of the customer"),
    )
    def login(email, password):
        """ """

        try:

            login_email_address = Customer.query.filter_by(email=email).first()

            if not login_email_address:
                return jsonify({
                    "code": 404,
                    "error message": "Email Not Found",
                    "message": f"The email address {login_email_address} was not found, it might be incorrect."  # noqa
                }), 404

            login_password = login_email_address.check_password(password)

            if not login_password:
                return jsonify({
                    "code": 404,
                    "error message": "Incorrect Data",
                    "message": f"The password {password} is not correct."
                }), 404

            auth_token = login_email_address.encode_token(
                str(login_email_address.id), login_email_address.first_name,
                login_email_address.last_name)

            expires = (datetime.now() + timedelta(seconds=3600)
                       ).strftime("%H:%M")

            if login_email_address:
                if login_password:
                    return jsonify({
                        "code": 200,
                        'status': 'success',
                        'message': 'Successfully logged in as business.',
                        'auth_token': auth_token,
                        'token_expires_by': expires,
                        'business_id': login_email_address.id
                    }), 200

        except Forbidden as e:
            return {
                'Code': e.code,
                'Type': e.type,
                'Error Message': e.message
            }

        except InternalServerError as e:
            return {
                'Code': e.code,
                'Type': e.type,
                'Error Message': e.message
            }
