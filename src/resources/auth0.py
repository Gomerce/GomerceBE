"""
Define the resources for the customer, vendor and admin auth

"""

from os import environ as env
from urllib.parse import quote_plus, urlencode

from flask import redirect, session, url_for
from flask_restful import Resource

import config
from server import oauth


class Auth0Resource(Resource):
    def login_user():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )

    def callback():
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect("/")

    def logout_user():
        session.clear()
        return redirect(
            "https://" + config.AUTH0_DOMAIN
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("home", _external=True),
                    "client_id": config.AUTH0_CLIENT_ID,
                },
                quote_via=quote_plus,
            )
        )
