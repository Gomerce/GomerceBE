"""
Define the resources for the customers
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import CustomerRepository
from utils import parse_params
from utils.errors import DataNotFound, InternalServerError, Unauthorized
from validators.auth import requires_auth


class CustomerResource(Resource):
    """ methods relative to the customer """

    @staticmethod
    @swag_from("../swagger/customers/get_one.yml")
    @requires_auth('get:user')
    def get_one(customer_id):
        """ Return a customer key information based on customer_id """

        try:
            customer = CustomerRepository.get(customer_id=customer_id)
            if not customer:
                return jsonify({"message": f" customer with the id {customer_id} not found"})  # noqa
            data = {
                "id": customer.id,
                "username": customer.username,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
                "country": customer.country,
                "state": customer.state,
                "city": customer.city,
                "street_name": customer.street_name,
                "zipcode": customer.zipcode,
            }
            return jsonify({"data": data})
        except DataNotFound as data_error:
            abort(404, data_error.message)
        except Unauthorized as data_error:
            abort(401, data_error.message)
        except InternalServerError as data_error:
            abort(500, data_error.message)

    @staticmethod
    @swag_from("../swagger/customers/get_all.yml")
    @requires_auth('get:users')
    def get_all():
        """ Return all customer key information based on the
        query parameter """
        customers = CustomerRepository.getAll()
        return jsonify({"data": customers})

    @staticmethod
    @parse_params(
        Argument("first_name", location="json",
                 help="The first_name of the customer."),
        Argument("last_name", location="json",
                 help="The last_name of the customer."),
        Argument("age", location="json",
                 help="The age of the customer.")
    )
    @swag_from("../swagger/customers/put.yml")
    @requires_auth('patch:user')
    def update_customer(customer_id, last_name, first_name, age):
        """ Update a customer based on the provided information """
        print(customer_id)
        repository = CustomerRepository()
        customer = repository.update(
            customer_id=customer_id, last_name=last_name,
            first_name=first_name, age=age
        )
        return jsonify({"data": customer.json})

    @staticmethod
    @parse_params(
        Argument("username", location="json", required=True,
                 help="The username of the customer."),
        Argument("last_name", location="json", required=True,
                 help="The last name of the customer."),
        Argument("first_name", location="json", required=True,
                 help="The first name of the customer."),
        Argument("email", location="json", required=True,
                 help="The email address of the customer."),
        Argument("password", location="json", required=True,
                 help="The password of the customer."),
        Argument("phone", location="json",
                 help="The phone number of the customer."),
        Argument("country", location="json",
                 help="The country of the customer."),
        Argument("state", location="json",
                 help="The state of the customer."),
        Argument("city", location="json",
                 help="The city of the customer."),
        Argument("street_name", location="json",
                 help="The street name of the customer."),
        Argument("zipcode", location="json",
                 help="The ZIP code of the customer."),
    )
    @swag_from("../swagger/customers/post.yml")
    def post(username, last_name, first_name, email, password, phone=None,
             country=None, state=None, city=None, street_name=None,
             zipcode=None):
        """ Create a customer based on the provided information """

        # Check duplicates
        customer = CustomerRepository.create(
            username=username, first_name=first_name,
            last_name=last_name, email=email, password=password,
            phone=phone, country=country, state=state,
            city=city, street_name=street_name,
            zipcode=zipcode
        )
        return jsonify({"data": customer.json})
