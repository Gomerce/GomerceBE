"""
Define the resources for the product
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import ProductRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class ProductResource(Resource):
    """ methods relative to the product """

    @staticmethod
    @swag_from("../swagger/product/get_one.yml")
    def get_one(product_id):
        """ Return a product key information based on product_id """

        try:
            product = ProductRepository.get(product_id=product_id)
            if not product:
                return jsonify({
                    "message": f" Product with the id {product_id} not found"
                })

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
        """
        Return all products key information based on the query parameter
        """
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
        Argument("thumbnail", location="json",
                 help="The thumbnail of the product."),
        Argument("image", location="json",
                 help="The image of the product."),
        Argument("sellers_id", location="json",
                 help="The sellers_id that created the product."),
        Argument("product_categories_id", location="json",
                 help="The product_categories of the product."),
    )
    # @swag_from("../swagger/product/POST.yml")
    @requires_auth('post:product')
    def post(title, price, quantity, short_desc,
             thumbnail, image, sellers_id, product_categories_id):
        """ Create a product based on the provided information """

        if title is None:
            abort(400, "Sorry, title cannot be null.")
        if title == "":
            abort(400, "Sorry, title cannot be empty.")
        if price is None:
            abort(400, "Sorry, price cannot be null.")
        if price == "":
            abort(400, "Sorry, price cannot be empty.")

        if quantity is None:
            abort(400, "Sorry, quantity cannot be null.")
        if quantity == "":
            abort(400, "Sorry, quantity cannot be empty.")

        if short_desc is None:
            abort(400, "Sorry, you have to give a short description.")
        if short_desc == "":
            abort(400, "Sorry, your description cannit be empty.")

        if thumbnail is None:
            abort(400, "Sorry, thumbnail cannot be null.")
        if thumbnail == "":
            abort(400, "Sorry, thumbnail cannot be empty.")

        if image is None:
            abort(400, "Sorry, image cannot be null.")
        if image == "":
            abort(400, "Sorry, image cannot be empty.")

        if sellers_id is None:
            abort(400, "Sorry, sellers_id cannot be null.")
        if sellers_id == "":
            abort(400, "Sorry, product cannot belong to an empty seller.")
        if product_categories_id is None:
            abort(400, "Sorry, product has to belong to a category.")
        if product_categories_id == "":
            abort(400, "Sorry, product cannot belong to an empty category.")

        product = ProductRepository.create(
            title=title,
            price=price,
            quantity=quantity,
            short_desc=short_desc,
            thumbnail=thumbnail,
            image=image,
            sellers_id=sellers_id,
            product_categories_id=product_categories_id)

        return jsonify({
            "title": product.title,
            "id": product.id,
            "price": product.price,
            "quantity": product.quantity,
            "short_desc": product.short_desc,
            "thumbnail": product.thumbnail,
            "image": product.image,
            "sellers_id": product.sellers_id,
            "product_category_id": product.product_categories_id
        })

    @requires_auth('delete:product')
    def delete(product_id):
        """ delete a product based on the product id provided """
        # fetch product

        product = ProductRepository

        if not (product.get(product_id=product_id)):
            abort(
                404, f"Sorry, the product with id {product_id} was not found."
            )

        product.delete(product_id=product_id)

        return jsonify({
            "message": f"product with id {product_id} was successfully deleted"
        })

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
        Argument("thumbnail", location="json",
                 help="The thumbnail of the product."),
        Argument("image", location="json",
                 help="The image of the product."),
        Argument("rating", location="json",
                 help="The rating of the product.")
    )
    # @swag_from("../swagger/product/PUT.yml")
    @requires_auth('patch:product')
    def update_product(product_id, title, price, quantity,
                       short_desc, thumbnail, image, rating):
        """ Update a product based on the provided information """
        if product_id is None:
            abort(400, "Sorry, product_id cannot be null.")
        if product_id == "":
            abort(400, "Sorry, product_id cannot be empty.")

        product = ProductRepository()

        if title is None:
            abort(400, "Sorry, title cannot be null.")
        if title == "":
            abort(400, "Sorry, title cannot be empty.")
        if price is None:
            abort(400, "Sorry, price cannot be null.")
        if price == "":
            abort(400, "Sorry, price cannot be empty.")

        if quantity is None:
            abort(400, "Sorry, quantity cannot be null.")
        if quantity == "":
            abort(400, "Sorry, quantity cannot be empty.")

        if short_desc is None:
            abort(400, "Sorry, you have to give a short description.")
        if short_desc == "":
            abort(400, "Sorry, your description cannit be empty.")

        if thumbnail is None:
            abort(400, "Sorry, thumbnail cannot be null.")
        if thumbnail == "":
            abort(400, "Sorry, thumbnail cannot be empty.")

        if image is None:
            abort(400, "Sorry, image cannot be null.")
        if image == "":
            abort(400, "Sorry, image cannot be empty.")

        if rating is None:
            abort(400, "Sorry, rating cannot be null.")
        if rating == "":
            abort(400, "Sorry, rating cannot be empty.")

        product.update(
            product_id=product_id,
            title=title,
            price=price,
            quantity=quantity,
            short_desc=short_desc,
            thumbnail=thumbnail,
            image=image,
            rating=rating)

        return jsonify({
            "message": f"Product with id {product_id} updated successfully"
        })
