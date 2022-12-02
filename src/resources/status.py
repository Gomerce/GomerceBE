"""
Define the resources for the customers
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import StatusRepository
from utils import parse_params
from utils.errors import DataNotFound


class StatusResource(Resource):
    """ methods relative to the status """

    @staticmethod
    @swag_from("../swagger/status/get_one.yml")
    def get_one(status_id):
        """ Return a status key information based on status_id """

        try:
            status = StatusRepository.get(status_id=status_id)
            return jsonify({"data": status.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/status/get_all.yml")
    def get_all():
        """ Return all status key information based on the query parameter """
        status = StatusRepository.getAll()
        return jsonify({"data": status})

    @staticmethod
    @parse_params(
        Argument("status", location="json",
                 help="The status of the Statuses."),
        Argument("order_id", location="json",
                 help="The order_id of the Statuses."),
    )
    def update_status(status_id, status, order_id):
        """ Update a status based on the provided information """
        repository = StatusRepository()
        status = repository.update(
            status_id=status_id, status=status, order_id=order_id
        )
        return jsonify({"data": status.json})

    @staticmethod
    @parse_params(
        Argument("status", location="json",
                 help="The status of the Statuses."),
        Argument("order_id", location="json",
                 help="The order_id of the Statuses."),
    )
    def post(status, order_id):
        """ Create a status based on the provided information """
        status = StatusRepository.create(
            status=status, order_id=order_id
        )
        return jsonify({"data": status.json})
