"""
Define the resources user, vendor and admin auth
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
# from ..repositories import UserRepository
from ..utils import parse_params


class AuthResource(Resource):
    """ methods relative to the authorization """

    @staticmethod
    @parse_params(
        Argument("email", location="json",
                 help="The email of the user."),
        Argument("password", location="json",
                 help="The password of the user.")
    )
    # @swag_from("../swagger/auth/login_user.yml")
    def login_user(email, password):
        """ Return a user key information based on user_id """

        try:
            user = UserRepository.get(user_id=user_id)
            return jsonify({"data": user.json})
        except Exception as e:
            abort(404, e.message)

    @staticmethod
    @swag_from("../swagger/user/get_all.yml")
    def get_all():
        """ Return all user key information based on the query parameter """
        users = UserRepository.getAll()
        return jsonify({"data": users})

    @staticmethod
    @parse_params(
        Argument("first_name", location="json",
                 help="The first_name of the user."),
        Argument("last_name", location="json",
                 help="The last_name of the user."),
        Argument("age", location="json",
                 help="The age of the user.")
    )
    # @swag_from("../swagger/user/PUT.yml")
    def update_user(user_id, last_name, first_name, age):
        """ Update an user based on the sent information """
        print(user_id)
        repository = UserRepository()
        user = repository.update(
            user_id=user_id, last_name=last_name, first_name=first_name, age=age
        )
        return jsonify({"data": user.json})

    @staticmethod
    @parse_params(
        Argument("first_name", location="json", required=True,
                 help="The first_name of the user."),
        Argument("last_name", location="json", required=True,
                 help="The last_name of the user."),
        Argument("age", location="json", required=True,
                 help="The age of the user.")
    )
    # @swag_from("../swagger/user/POST.yml")
    def post(last_name, first_name, age):
        """ Create an user based on the sent information """
        # TODO: Check duplicates
        user = UserRepository.create(
            last_name=last_name, first_name=first_name, age=age
        )
        return jsonify({"data": user.json})
