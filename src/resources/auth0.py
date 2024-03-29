"""
Define the resources for the customer, vendor and admin auth

"""

from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import redirect, session, url_for
from flask_restful import Resource

import config

oauth = OAuth()


class Auth0Resource(Resource):
    """ This class define Auth0 Resource """

    # pylint: disable=E0211

    def login():
        """ This define the login function """

        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )

    def callback():
        """ This define the callback function """

        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect(url_for("index.index"))

    def logout():
        """ This define the logout function """

        session.clear()
        return redirect(
            "https://" + config.AUTH0_DOMAIN
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("index.index", _external=True),
                    "client_id": config.AUTH0_CLIENT_ID,
                },
                quote_via=quote_plus,
            )
        )
