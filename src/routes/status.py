"""
Defines the blueprint for the status
"""
from flask import Blueprint

from resources import StatusResource

STATUS_BLUEPRINT = Blueprint("status", __name__)
STATUS_BLUEPRINT.route(
    "/status", methods=['GET'])(StatusResource.get_all)
STATUS_BLUEPRINT.route("/status", methods=['POST'])(StatusResource.post)
STATUS_BLUEPRINT.route("/status/<int:status_id>",
                         methods=['GET'])(StatusResource.get_one)
