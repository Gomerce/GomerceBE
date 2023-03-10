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
            if not product:
                return jsonify({"message": f" Product with the id {product_id} not found"})
            
            return jsonify({
                "id": product.id,
                "title": product.title,
                "quantity": product.quantity,
                "price": product.price,
                "category": product.product_categories_id,
                "rating": product.rating,
                "image": product.image,
                "short_desc": product.short_desc,
                "thumbnail": product.thumbnail,
                "sellers_id": product.sellers_id
            })
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
    
    @staticmethod
    @parse_params(
        Argument("title", location="json", required=True,
                 help="The title of the product."),
        Argument("price", location="json", required=True,
                 help="The price of the product."),
        Argument("quantity", location="json", required=True,
                 help="The quantity of the product."),
        Argument("short_desc", location="json", required=True,
                 help="The short_desc of the product."),
        Argument("thumbnail", location="json", required=True,
                 help="The thumbnail of the product."),
        Argument("image", location="json", required=True,
                 help="The image of the product."),
        Argument("sellers_id", location="json", required=True,
                 help="The sellers_id that created the product."),
        Argument("product_categories_id", location="json", required=True,
                 help="The product_categories of the product."),  
    )
    # @swag_from("../swagger/product/POST.yml")
    def post(title, price, quantity, short_desc, thumbnail, image, sellers_id, product_categories_id):
        """ Create a product based on the provided information """
        # Check duplicates
        product = ProductRepository.create(
            title=title, price=price, quantity=quantity, short_desc=short_desc, thumbnail=thumbnail, image=image, sellers_id=sellers_id, product_categories_id=product_categories_id
        )
        return jsonify({
            "title": product.title,
            "price": product.price,
            "quantity": product.quantity,
            "short_desc": product.short_desc,
            "thumbnail": product.thumbnail,
            "image": product.image,
            "sellers_id": product.sellers_id,
            "product_category_id": product.product_categories_id
        })
    
    def delete(product_id):
        """ delete a product based on the product id provided """
        # fetch product
        product = ProductRepository.delete(product_id=product_id)

        return jsonify({"message": "product successfully deleted"})
    
    @staticmethod
    @parse_params(
        Argument("title", location="json", required=True,
                 help="The title of the product."),
        Argument("price", location="json", required=True,
                 help="The price of the product."),
        Argument("quantity", location="json", required=True,
                 help="The quantity of the product."),
        Argument("short_desc", location="json", required=True,
                 help="The short_desc of the product."),
        Argument("thumbnail", location="json", required=True,
                 help="The thumbnail of the product."),
        Argument("image", location="json", required=True,
                 help="The image of the product."),
        Argument("rating", location="json", required=True,
                 help="The rating of the product.")
    )
    # @swag_from("../swagger/product/PUT.yml")
    def update_product(product_id, title, price, quantity, short_desc, thumbnail, image, rating):
        """ Update a product based on the provided information """
        print(product_id)
        repository = ProductRepository()
        product = repository.update(
            product_id=product_id, title=title, price=price, quantity=quantity, short_desc=short_desc, thumbnail=thumbnail, image=image, rating=rating
        )
        return jsonify({"message": "updated successfully"})


    
   
   
