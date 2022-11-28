"""
Define the resources for the product
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import ProductRepository
from utils import parse_params
from utils.errors import DataNotFound


class ProductResource(Resource):
    """ methods relative to the product """

    @staticmethod
    @swag_from("../swagger/product/get_one.yml")
    def get_one(product_id):
        """ Return a product key information based on product_id """

        try:
            product = ProductRepository.get(product_id=product_id)
            return jsonify({"data": product.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/product/get_all.yml")
    def get_all():
        """ Return all products key information based on the query parameter """
        products = ProductRepository.getAll()
        return jsonify({"data": products})


    
   
   
