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
    @swag_from("../swagger/product/get_one.yml")
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
    @swag_from("../swagger/product/get_all.yml")
    def get_all():
        """ get all product information """
        products = ProductRepository.getAll()
        return jsonify({"data": products})

    @staticmethod
    @parse_params(
        Argument("title", location="json",
                 help="The title of the product."),
        Argument("price", location="json",
                 help="The price of the product."),
        Argument("quantity", location="json",
                 help="The quantity of the product."),
        Argument("short_desc", location="json",
                 help="The short_desc of the product."),
        Argument("long_desc", location="json",
                 help="The long_desc of the product."),
        Argument("rating", location="json",
                 help="The rating of the product."),
        Argument("thumbnail", location="json",
                 help="The thumbnail of the product."),
        Argument("image", location="json",
                 help="The image of the product."),
        Argument("sellers_id", location="json",
                 help="The sellers id of the product."),
        Argument("product_categories_id", location="json",
                 help="The product categories id of the product.")
    )
    def update_product(product_id, title, price, quantity, short_desc, long_desc, rating, thumbnail, image, sellers_id, product_categories_id):
        """ Update a customer based on the provided information """
        repository = ProductRepository()
        product = repository.update(
            product_id=product_id, title=title, price=price, quantity=quantity,
            short_desc=short_desc, long_desc=long_desc, rating=rating, thumbnail=thumbnail,
            image=image, sellers_id=sellers_id,
            product_categories_id=product_categories_id
        )
        return jsonify({"data": product.json})

    @staticmethod
    @parse_params(
        Argument("title", location="json",
                 help="The title of the product."),
        Argument("price", location="json",
                 help="The price of the product."),
        Argument("quantity", location="json",
                 help="The quantity of the product."),
        Argument("short_desc", location="json",
                 help="The short_desc of the product."),
        Argument("long_desc", location="json",
                 help="The long_desc of the product."),
        Argument("rating", location="json",
                 help="The rating of the product."),
        Argument("thumbnail", location="json",
                 help="The thumbnail of the product."),
        Argument("image", location="json",
                 help="The image of the product."),
        Argument("sellers_id", location="json",
                 help="The sellers id of the product."),
        Argument("product_categories_id", location="json",
                 help="The product categories id of the product.")
    )
    def post(title, price, quantity, short_desc, long_desc, rating, thumbnail, image, sellers_id, product_categories_id):
        """ Create a product based on the provided information """
        customer = ProductRepository.create(
            title=title,
            price=price,
            quantity=quantity,
            short_desc=short_desc,
            long_desc=long_desc,
            rating=rating,
            thumbnail=thumbnail,
            image=image,
            sellers_id=sellers_id,
            product_categories_id=product_categories_id
        )
        return jsonify({"data": customer.json})