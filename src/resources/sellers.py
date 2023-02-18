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

    @staticmethod
    @parse_params(
        Argument("first_name", location="json", required=True,
                 help="The first_name of the seller."),
        Argument("last_name", location="json", required=True,
                 help="The last_name of the seller."),
        Argument("phone", location="json", required=True,
                 help="The phone details of the seller."),
        Argument("username", location="json", required=True,
                 help="The username of the seller."),
        Argument("email", location="json", required=True,
                 help="The email of the seller."),
        Argument("password", location="json", required=True,
                 help="Sellers password"),
    )
    def post(last_name, first_name, phone, username, email, password):
        """ Create a seller """
        seller = SellerRepository.create(
            last_name=last_name, first_name=first_name, phone=phone, username=username, email=email, password=password
        )
        return jsonify({"data": seller.json})

    @staticmethod
    @parse_params(
        Argument("last_name", location="json",
                 help="The last name of the seller."),
        Argument("first_name", location="json",
                 help="The first name of the seller."),
        Argument("phone", location="json",
                 help="The phone number of the seller.")
    )
    def update_seller(seller_id, last_name, first_name, phone):
        """ Update a seller information via id passed"""
        seller = SellerRepository().update(
            seller_id=seller_id, last_name=last_name, first_name=first_name, phone=phone
        )
        return jsonify({"data": seller.json})

    def delete(seller_id):
        """ delete a seller via the provided id """
        seller = SellerRepository.delete(seller_id=seller_id)

        return jsonify({"message": "seller successfully deleted"})
