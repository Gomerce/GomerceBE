"""
Define the resources for the store
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import StoreRepository
from utils import parse_params
from utils.errors import DataNotFound


class StoreResource(Resource):
    """ methods relative to the status """

    @staticmethod
    @swag_from("../swagger/store/get_one.yml")
    def get_one(store_id):
        """ Return a store key information based on status_id """

        try:
            store = StoreRepository.get(store_id=store_id)
            return jsonify({"data": store.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/store/get_all.yml")
    def get_all():
        """ Return all store key information based on the query parameter """
        store = StoreRepository.getAll()
        return jsonify({"data": store})

    @staticmethod
    @parse_params(
        Argument("phone", location="json",
                 help="The phone of the store."),
        Argument("name", location="json",
                 help="The name of the store."),
        Argument("email", location="json",
                 help="The email of the store."),
        Argument("address", location="json",
                 help="The address of the store."),
        Argument("email_verified", location="json",
                 help="The email_verified of the store."),
        Argument("phone_verified", location="json",
                 help="The phone_verified of the store."),
        Argument("sellers_id", location="json",
                 help="The sellers_id of the store."),
    )
    def update_store(store_id, phone, name, email, address, email_verified, phone_verified):
        """ Update a store based on the provided information """
        print(store_id)
        repository = StoreRepository()
        status = repository.update(
            store_id=store_id, phone=phone, name=name, email=email, address=address,
            email_verified=email_verified, phone_verified=phone_verified
        )
        return jsonify({"data": status.json})

    @staticmethod
    @parse_params(
        Argument("phone", location="json",
                 help="The phone of the store."),
        Argument("name", location="json",
                 help="The name of the store."),
        Argument("email", location="json",
                 help="The email of the store."),
        Argument("address", location="json",
                 help="The address of the store."),
        Argument("email_verified", location="json",
                 help="The email_verified of the store."),
        Argument("phone_verified", location="json",
                 help="The phone_verified of the store."),
        Argument("sellers_id", location="json",
                 help="The sellers_id of the store."),
    )
    def post(phone, name, email, address, email_verified, phone_verified, sellers_id):
        """ Create a store based on the provided information """
        store = StoreRepository.create(
            name, address,
            email=email, phone=phone,
            email_verified=email_verified,
            phone_verified=phone_verified,
            sellers_id=sellers_id,
        )
        return jsonify({"data": store.json})