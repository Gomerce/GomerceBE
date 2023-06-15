"""
Define the resources for the sellers
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import SellerRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth
import jwt
import os
from datetime import datetime, timedelta

# from utils.auth_decorators import seller_auth_required


class SellerResource(Resource):
    """ methods relative to the seller """

    @staticmethod
    @swag_from("../swagger/seller/get_one.yml")
    @requires_auth('get:seller')
    def get_one(seller_id):
        """ Return a seller key information based on seller_id """

        try:
            seller = SellerRepository.get(seller_id=seller_id)
            if not seller:
                return jsonify(
                    {"message": f" Seller with the id {seller_id} not found"})
            return jsonify({"data": seller.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/seller/get_all.yml")
    @requires_auth('get:sellers')
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
    @swag_from("../swagger/seller/put.yml")
    @requires_auth('patch:seller')
    def update_seller(seller_id, last_name, first_name, phone):
        """ Update a seller based on the provided information """

        repository = SellerRepository()

        if first_name is None:
            abort(400, "Sorry, first name cannot be null.")
        if first_name == "":
            abort(400, "Sorry, first name cannot be empty.")

        if last_name is None:
            abort(400, "Sorry, last name cannot be null.")
        if last_name == "":
            abort(400, "Sorry, last name cannot be empty.")

        if phone is None:
            abort(400, "Sorry, phone cannot be null.")
        if phone == "":
            abort(400, "Sorry, phone cannot be empty.")

        seller = repository.update(
            seller_id=seller_id,
            last_name=last_name,
            first_name=first_name,
            phone=phone)
        return jsonify({"data": seller.json})

    @staticmethod
    @parse_params(
        Argument("first_name", location="json",
                 help="The first_name of the seller."),
        Argument("last_name", location="json",
                 help="The last_name of the seller."),
        Argument("phone", location="json",
                 help="The phone details of the seller."),
        Argument("username", location="json",
                 help="The username of the seller."),
        Argument("email", location="json",
                 help="The email of the seller."),
        Argument("password", location="json",
                 help="The password of the seller.")
    )
    @swag_from("../swagger/seller/post.yml")
    @requires_auth('post:seller')
    def post(last_name, first_name, phone, username, email, password):
        """ Create a seller based on the provided information """
        error = False

        if first_name is None:
            error = True
            abort(400, "Sorry, first name cannot be null.")
        if first_name == "":
            error = True
            abort(400, "Sorry, first name cannot be empty.")

        if last_name is None:
            error = True
            abort(400, "Sorry, last name cannot be null.")
        if last_name == "":
            error = True
            abort(400, "Sorry, last name cannot be empty.")

        if email is None:
            error = True
            abort(400, "Sorry, email cannot be null.")
        if email == "":
            error = True
            abort(400, "Sorry, email cannot be empty.")

        if username is None:
            error = True
            abort(400, "Sorry, username cannot be null.")
        if username == "":
            error = True
            abort(400, "Sorry, username cannot be empty.")

        if phone is None:
            error = True
            abort(400, "Sorry, phone cannot be null.")
        if phone == "":
            error = True
            abort(400, "Sorry, phone cannot be empty.")

        if password is None:
            error = True
            abort(400, "Sorry, password cannot be null.")
        if password == "":
            error = True
            abort(400, "Sorry, password cannot be empty.")
        if len(password) < 6:
            error = True
            abort(400, "Password must be at least 6 characters")

        if not error:
            seller = SellerRepository.create(
                last_name=last_name,
                first_name=first_name,
                phone=phone,
                username=username,
                email=email,
                password=password
            )

            token = jwt.encode(
                {"id": seller.id, "exp":
                    datetime.now() + timedelta(days=1)},
                os.environ.get("SECRET_KEY"),
                algorithm="HS256",
            )
            # return jsonify({"data": seller.json})

            return jsonify({
                "id": seller.id,
                "seller": seller.username,
                "email": seller.email,
                "firstName": seller.first_name,
                "lastName": seller.last_name,
                "token": token
            })
    @swag_from("../swagger/seller/delete.yml")
    @requires_auth('delete:seller')
    def delete(seller_id):
        """ delete a seller based on the seller id provided """
        # fetch seller
        seller = SellerRepository

        if (seller.get(seller_id)) is None:
            abort(404, f"Seller with id {seller_id} does not exist.")

        seller.delete(seller_id=seller_id)

        return jsonify({
            "message": f"Seller with id {seller_id} successfully deleted"
        })
