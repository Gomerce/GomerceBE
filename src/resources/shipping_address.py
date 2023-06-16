"""
Define the resources for the shipping address
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import ShippingAddressRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class ShippingAddressResource(Resource):
    """ methods relative to the shipping address """

    @staticmethod
    @swag_from("../swagger/shipping_address/get_one.yml")
    @requires_auth('get:shipping_address')
    def get_one(address_id):
        """ Return an order key information based on address_id """

        try:
            address = ShippingAddressRepository.get(address_id=address_id)
            data = {
                "id": address.id,
                "country": address.country,
                "state": address.state,
                "city": address.city,
                "street_name": address.street_name,
                "zipcode": address.zipcode,
                "phone": address.phone,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception as err:
            print(err)
            abort(500)

    @staticmethod
    @swag_from("../swagger/shipping_address/get_all.yml")
    @requires_auth('get:shipping_addresses')
    def get_all():
        """ Return all shipping address key information based on the query parameter """
        addresses = ShippingAddressRepository.getAll()
        return jsonify({"data": addresses})

    @staticmethod
    @parse_params(
        Argument("country", location="json",
                 help="The country of the address."),
        Argument("state", location="json",
                 help="The state of the address."),
        Argument("city", location="json",
                 help="The city of the address."),
        Argument("zipcode", location="json",
                 help="The zipcode of the address."),
        Argument("phone", location="json",
                 help="The phone of the address."),
        Argument("street_name", location="json",
                 help="The street_name of the address."),
    )
    @swag_from("../swagger/shipping_address/put.yml")
    @requires_auth('patch:shipping_address')
    def update_address(
            address_id,
            country,
            state,
            city,
            street_name,
            zipcode,
            phone):
        """ Update an address based on the provided information """
        address = ShippingAddressRepository().update(
            address_id=address_id,
            country=country,
            state=state,
            city=city,
            street_name=street_name,
            zipcode=zipcode,
            phone=phone
        )
        data = {
            "country": address.country,
            "id": address.id,
            "state": address.state,
            "city": address.city,
            "street_name": address.street_name,
            "zipcode": address.zipcode,
            "phone": address.phone,
        }
        return jsonify({"data": data})

    @staticmethod
    @parse_params(
        Argument("country", location="json",
                 help="The country of the address."),
        Argument("state", location="json",
                 help="The state of the address."),
        Argument("city", location="json",
                 help="The city of the address."),
        Argument("zipcode", location="json",
                 help="The zipcode of the address."),
        Argument("phone", location="json",
                 help="The phone of the address."),
        Argument("street_name", location="json",
                 help="The street_name of the address."),
    )
    @swag_from("../swagger/shipping_address/post.yml")
    @requires_auth('post:shipping_address')
    def post(country, state, city, street_name, zipcode, phone):
        """ Create a address based on the provided information """
        data = ShippingAddressRepository.create(
            country=country,
            state=state,
            city=city,
            street_name=street_name,
            zipcode=zipcode,
            phone=phone,
        )
        return jsonify({"data": data.json})

    @swag_from("../swagger/shipping_address/delete.yml")
    @requires_auth('delete:shipping_address')
    def delete(address_id):
        """ delete a address via the provided id """
        ShippingAddressRepository.delete(address_id=address_id)
        return jsonify({"message": "address successfully deleted"})
