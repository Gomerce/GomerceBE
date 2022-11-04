""" Defines the Google repository """

""" How to Use it """
"""
apply the @login_is_required for users just like applied below
    @app.route("/route")
    @login_is_required
    def protected_area():
"""

""" when dealing with OAuth 2.0 app secret is necessary"""
import os
import pathlib
import requests
import config
from flask import session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import server
server.secret_key = config.APP_SECRET
"""this is to set environment to https because OAuth 2.0 only supports https environments"""
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

"""setting path to the parent directory where the .json file from google is kept"""
client_secrets_file = os.path.join(pathlib.Path(
    __file__).parent.parent.parent, "client_secret.json")
# client_secrets_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "client_secret.json")

""" 
    Flow is OAuth 2.0 class that stores 
    all users authorization information
"""
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    # the redirect URI route to after authorization
    redirect_uri="http://127.0.0.1:5000/callback"
)


class GoogleResource:
    """ The repository for google """
    ''' 
    a function to check if a user is authorized 
    or not 
    '''
    @staticmethod
    def login_is_required(function):
        def wrapper(*args, **kwargs):
            if "google_id" not in session:
                return abort(401)
            else:
                return function()
        return wrapper

    '''
      Asking the flow class for the authorization (login) url
    '''
    @staticmethod
    def google_login():
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    '''
        the callback method handles redirection after 
        authorization
    '''
    @staticmethod
    def callback():
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(
            session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=config.GOOGLE_CLIENT_ID
        )

        ''' defining the results to show on the page'''
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        '''page to redirect to after authorization'''
        return redirect("/")