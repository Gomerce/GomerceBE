"""
Defines the welcome page for the users
"""
from flask import Blueprint
from flask_restful import Api
from resources import IndexResource

INDEX_BLUEPRINT = Blueprint("/", __name__)
api = Api(INDEX_BLUEPRINT)
api.add_resource(IndexResource, "")
