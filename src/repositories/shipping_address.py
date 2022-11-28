""" Defines the Shipping Address repository """
import sys
from sqlalchemy import or_, and_
from models import ShippingAddress
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class ShippingAddressRepository:
    """ The repository for the shipping address model """

    @staticmethod
    def get(address_id=None):
        """ Query a shipping address by address_id """

        # make sure one of the parameters was passed
        if not address_id:
            raise DataNotFound(f"Shipping Address not found, no detail provided")

        try:
            query = ShippingAddress.query
            if address_id:
                query = query.filter(ShippingAddress.id == address_id)

            address_item = query.first()
            return address_item
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Shipping Address with {address_id} not found")

    @staticmethod
    def getAll():
        """ Query all shipping addresses"""
        addresses = ShippingAddress.query.all()
        all_addresses = [address_item.json for address_item in addresses]
        return all_addresses

