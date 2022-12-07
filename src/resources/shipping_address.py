"""
Define the resources for the shipping address
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import ShippingAddressRepository
from utils import parse_params
from utils.errors import DataNotFound


class ShippingAddressResource(Resource):
    """ methods relative to the shipping address """

    @staticmethod
    @swag_from("../swagger/shipping_address/get_one.yml")
    def get_one(address_id):
        """ Return an order key information based on address_id """

        try:
            address = ShippingAddressRepository.get(address_id=address_id)
            return jsonify({"data": address.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/shipping_address/get_all.yml")
    def get_all():
        """ Return all shipping address key information based on the query parameter """
        addresses = ShippingAddressRepository.getAll()
        return jsonify({"data": addresses})
