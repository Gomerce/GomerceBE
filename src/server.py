from authlib.integrations.flask_client import OAuth
from flasgger import Swagger
from flask import Flask, jsonify
from flask.blueprints import Blueprint
from flask_migrate import Migrate

import config
import routes
from models import db
from resources import oauth
from validators.auth import AuthError

server = Flask(__name__)

server.debug = config.DEBUG
server.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS  # noqa
db.init_app(server)
db.app = server
migrate = Migrate(server, db)

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(
            blueprint, url_prefix=config.APPLICATION_ROOT)

oauth.init_app(server)
oauth.app = server

oauth.register(
    "auth0",
    client_id=config.AUTH0_CLIENT_ID,
    client_secret=config.AUTH0_CLIENT_SECRET,
    api_base_url=config.AUTH0_DOMAIN,
    access_token_url=config.AUTH0_DOMAIN + "/oauth/token",
    authorize_url=config.AUTH0_DOMAIN + "/authorize",
    client_kwargs={
        "scope": "openid profile email",
    },
    # server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration'
)


# swagger configuration

server.config["SWAGGER"] = {
    "swagger_version": "2.0",
    "title": "Gomerce API",

    "description": """ Gomerce is a modern ecommerce app designed to provide
    users with a seamless online shopping experience. With its sleek interface,
    the app offers a wide range of products from various brands and sellers.
    It features advanced search and filtering options for easy product
    discovery. Personalized recommendations and curated collections help users
    find new items that align with their interests. Gomerce ensures secure
    transactions through a reliable payment gateway and offers multiple
    payment options. Additionally, it provides a user-friendly and intuitive
    interface for managing orders, tracking shipments, and handling returns,
    ensuring a hassle-free post-purchase experience. """,

    "termsOfService": "#",
    "version": "1.0.0",
    "static_url_path": "/apidocs",
    "servers": [
        {"url": "http://127.0.0.1:3303", "description": "Local development server"},
        {"url": "http://3.16.135.85", "description": "Production server"}
    ],

    "components": {
        "schemas": {},
        "securitySchemes": {
            "implicit": {
                "type": "oauth2",
                "flows": {
                    "implicit": {
                        "authorizationUrl": "https://dev-g4gsowubo2qcoa42.us.auth0.com/authorize",
                        "scopes": {
                            "get": "allows retrieving resources",
                            "post": "allows creating of resources",
                        }
                    }
                }
            }
        }
    }
}

swagger_config = Swagger.DEFAULT_CONFIG.copy()
swagger_config["openapi"] = "3.0.3"
# Add the security definitions
swagger_config["securityDefinitions"] = {
    "BearerAuth": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header"
    }
}

# Add the security requirement
swagger_config["security"] = [{"BearerAuth": []}]
Swagger(server, config=swagger_config)

""" Error handling """

# error handler for 422


@server.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# error handler for 400
@server.errorhandler(400)
def bad_request(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


# error handler for 401
@server.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": error.description
    }), 401


# error handler for 403
@server.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": error.description
    }), 403


# error handler for 404
@server.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


# error handler for 500
@server.errorhandler(500)
def internal_server_error(error):
    print({"error": error})
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500


@server.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == "__main__":
    server.debug = True
    server.run(host=config.HOST, port=config.PORT)
