"""
Define the resources for the sellers
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import SellerRepository
from utils import parse_params
from utils.errors import DataNotFound


class SellerResource(Resource):
    """ methods relative to the seller """

    @staticmethod
    @swag_from("../swagger/seller/get_one.yml")
    def get_one(seller_id):
        """ Return a seller key information based on seller_id """

        try:
            seller = SellerRepository.get(seller_id=seller_id)
            return jsonify({"data": seller.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/seller/get_all.yml")
    def get_all():
        """ Return all seller key information based on the query parameter """
        sellers = SellerRepository.getAll()
        return jsonify({"data": sellers})

    @staticmethod
    @parse_params(
        Argument("first_name", location="json",
                 help="The first_name of the seller."),
        Argument("last_name", location="json",
                 help="The last_name of the seller."),
        Argument("phone", location="json",
                 help="The phone details of the seller.")
    )
    # @swag_from("../swagger/seller/PUT.yml")
    def update_seller(seller_id, last_name, first_name):
        """ Update a seller based on the provided information """
        print(seller_id)
        repository = SellerRepository()
        seller = repository.update(
            seller_id=seller_id, last_name=last_name, first_name=first_name
        )
        return jsonify({"data": seller.json})

    @staticmethod
    @parse_params(
        Argument("first_name", location="json", required=True,
                 help="The first_name of the seller."),
        Argument("last_name", location="json", required=True,
                 help="The last_name of the seller."),
        Argument("phone", location="json", required=True,
                 help="The phone details of the seller.")
    )
    # @swag_from("../swagger/seller/POST.yml")
    def post(last_name, first_name, phone):
        """ Create a seller based on the provided information """
        # Check duplicates
        seller = SellerRepository.create(
            last_name=last_name, first_name=first_name, phone=phone
        )
        return jsonify({"data": seller.json})
