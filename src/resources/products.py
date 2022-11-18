"""
Define the resources for the products
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import ProductRepository
from utils import parse_params
from utils.errors import DataNotFound


class ProductResource(Resource):
    """ product resource definition """

    @staticmethod
    @swag_from("../swagger/products/get_one.yml")
    def get_one(product_id):
        """ return product information based on the search id """
        try:
            product = ProductRepository.get(id=product_id)
            return jsonify({"data": product.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/products/get_all.yml")
    def get_all():
        """ get all product information """
        products = ProductRepository.getAll()
        return jsonify({"data": products})