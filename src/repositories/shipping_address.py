""" Defines the Shipping Address repository """
import sys
from sqlalchemy import or_, and_
from models import ShippingAddress
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError
from flask import jsonify


class ShippingAddressRepository:
    """ The repository for the shipping address model """

    @staticmethod
    def get(address_id=None):
        """ Query a shipping address by address_id """

        # make sure one of the parameters was passed
        if not address_id:
            raise DataNotFound(
                f"Shipping Address not found, no detail provided")

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
        data = []
        for add in addresses:
            data.append({
                "id": add.id,
                "country": add.country,
                "state": add.state,
                "city": add.city,
                "street_name": add.street_name,
                "zipcode": add.zipcode,
                "phone": add.phone,
            })

        return data

    @staticmethod
    def create(country, state, city, street_name, zipcode, phone):
        """ Create a new address """
        try:
            created_address = ShippingAddress(
                country=country,
                state=state,
                phone=phone,
                city=city,
                zipcode=zipcode,
                street_name=street_name
            )
            review = created_address.save()

        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

        return jsonify({
            "country": created_address.country,
            "state": created_address.state,
            "phone": created_address.phone,
            "zipcode": created_address.zipcode,
            "city": created_address.city,
            "street_name": created_address.street_name,
        })

    def update(self, address_id, **args):
        """ Update a address """
        address = self.get(address_id)
        if not address:
            raise DataNotFound(f"Address Detail with {address_id} not found")

        if 'country' in args and args['country'] is not None:
            address.country = args['country']

        if 'state' in args and args['state'] is not None:
            address.state = args['state']

        if 'city' in args and args['city'] is not None:
            address.city = args['city']

        if 'street_name' in args and args['street_name'] is not None:
            address.street_name = args['street_name']

        if 'zipcode' in args and args['zipcode'] is not None:
            address.zipcode = args['zipcode']

        if 'phone' in args and args['phone'] is not None:
            address.phone = args['phone']

        return address.save()

    @staticmethod
    def delete(address_id):
        """ Delete a address by address_id """
        if not address_id:
            raise DataNotFound(f"Address not found")

        try:
            query = ShippingAddress.query.filter(
                ShippingAddress.id == address_id).first()
            if not query:
                raise DataNotFound(
                    f"Address Detail with {address_id} not found")
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Address with {address_id} not found")
