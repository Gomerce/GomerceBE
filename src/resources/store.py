"""
Define the resources for the store
"""
import json

from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import StoreRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class StoreResource(Resource):
    """ methods relative to the status """

    @staticmethod
    @swag_from("../swagger/store/get_one.yml")
    @requires_auth('get:store')
    def get_one(store_id):
        """ Return a store key information based on status_id """

        try:
            store = StoreRepository.get(store_id=store_id)
            data = {
                "id": store.id,
                "name": store.name,
                "address": store.address,
                "phone": store.phone,
                "email": store.email,
                "created_at": store.created_at,
                "updated_at": store.updated_at,
                "email_verified": store.email_verified,
                "phone_verified": store.phone_verified,
                "sellers_id": store.sellers_id,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception as err:
            print(err)
            abort(500)

    @staticmethod
    @swag_from("../swagger/store/get_all.yml")
    @requires_auth('get:stores')
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
    )
    @swag_from("../swagger/store/put.yml")
    @requires_auth('patch:store')
    def update_store(
            store_id,
            phone,
            name,
            email,
            address,
            email_verified,
            phone_verified):
        """ Update a store """
        store = StoreRepository().update(
            store_id=store_id,
            phone=phone,
            name=name,
            email=email,
            address=address,
            email_verified=email_verified,
            phone_verified=phone_verified)
        data = {
            "id": store.id,
            "name": store.name,
            "address": store.address,
            "phone": store.phone,
            "email": store.email,
            "created_at": store.created_at,
            "updated_at": store.updated_at,
            "email_verified": store.email_verified,
            "phone_verified": store.phone_verified,
        }
        return jsonify({"data": data})

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
    @swag_from("../swagger/store/post.yml")
    @requires_auth('post:store')
    def post(
            phone,
            name,
            email,
            address,
            email_verified,
            phone_verified,
            sellers_id):
        """ Create a store """
        store = StoreRepository.create(
            name=name, address=address,
            email=email, phone=phone,
            email_verified=email_verified,
            phone_verified=phone_verified,
            sellers_id=sellers_id,
        )
        data = {
            'name': store.name,
            'address': store.address,
            'email': store.email,
            'phone': store.phone,
            'sellers_id': store.sellers_id,
        }
        return jsonify({"data": data})

    @swag_from("../swagger/store/delete.yml")
    @requires_auth('delete:store')
    def delete(store_id):
        """ delete a Store via the provided id """
        StoreRepository.delete(store_id=store_id)
        return jsonify({"message": "store successfully deleted"})
