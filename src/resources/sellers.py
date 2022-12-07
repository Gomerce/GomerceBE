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
    """ sellers resource definition """

    @staticmethod
    @swag_from("../swagger/sellers/get_one.yml")
    def get_one(seller_id):
        """ return seller information based on the search id """

        try:
            seller = SellerRepository.get(id=seller_id)
            return jsonify({"data": seller.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/sellers/get_all.yml")
    def get_all():
        """ get all seller information """
        sellers = SellerRepository.getAll()
        return jsonify({"data": sellers})