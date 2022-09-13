"""
Define the REST verbs relative to the users
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import UserRepository
from utils import parse_params


class UserResource(Resource):
    """ Verbs relative to the user """

    @staticmethod
    @swag_from("../swagger/user/get_one.yml")
    def get(user_id):
        """ Return an user key information based on user_id """

        try:
            user = UserRepository.get(user_id=user_id)
            return jsonify({"data": user.json})
        except Exception as e:
            abort(404, e.message)

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
    def put(user_id, last_name, first_name, age):
        """ Update an user based on the sent information """
        print(user_id)
        repository = UserRepository()
        user = repository.update(
            user_id=user_id, last_name=last_name, first_name=first_name, age=age
        )
        return jsonify({"data": user.json})


class UsersResource(Resource):
    """ Verbs relative to the users """

    @staticmethod
    @swag_from("../swagger/user/get_all.yml")
    def get():
        """ Return all user key information based on the query parameter """
        users = UserRepository.getAll()
        return jsonify({"data": users})

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
