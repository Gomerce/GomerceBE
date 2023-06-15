"""
Define the resources for the customers
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import StatusRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class StatusResource(Resource):
    """ methods relative to the status """

    @staticmethod
    @swag_from("../swagger/status/get_one.yml")
    @requires_auth('get:status')
    def get_one(status_id):
        """ Return a status key information based on status_id """

        try:
            status = StatusRepository.get(status_id=status_id)
            if not status:
                return jsonify({"message": "status not found"})
            data = {
                "id": status.id,
                "status": status.status,
                "order_id": status.order_id,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/status/get_all.yml")
    @requires_auth('get:statuses')
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
    @swag_from("../swagger/status/put.yml")
    @requires_auth('patch:status')
    def update_status(status_id, status, order_id):
        """ Update a status based on the provided information """
        status = StatusRepository().update(
            status_id=status_id, status=status, order_id=order_id
        )
        return jsonify({"message": "status successfully updated"})

    @staticmethod
    @parse_params(
        Argument("status", location="json",
                 help="The status of the Statuses."),
        Argument("order_id", location="json",
                 help="The order_id of the Statuses."),
    )
    @swag_from("../swagger/status/post.yml")
    @requires_auth('post:status')
    def post(status, order_id):
        """ Create a status based on the provided information """
        status = StatusRepository.create(
            status=status, order_id=order_id
        )
        data = {
            "status": status.status,
            "order_id": status.order_id,
        }
        return jsonify({"data": data})

    @swag_from("../swagger/status/delete.yml")
    @requires_auth('delete:status')
    def delete(status_id):
        """ delete a status via the provided id """
        StatusRepository.delete(status_id=status_id)

        return jsonify({"message": "status successfully deleted"})
