""" Defines the Cart repository """


import sys

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from models import Cart, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError


class CartRepository:
    """ The repository for the Cart model """

    @staticmethod
    def get_one(cart_id=None, customer_id=None):
        """ Query a Cart by cart_id """

        # ensure that atleast one parameter is passed
        if not cart_id and not customer_id:
            raise DataNotFound("Cart id must be provided")

        try:
            result = db.session.query(Cart).filter(
                or_(Cart.id == cart_id, Cart.customer_id == customer_id))

            if not result:
                raise DataNotFound(f"Cart Detail with {cart_id} not found")

            return result
        except DataNotFound:
            print(sys.exc_info())
            raise DataNotFound(
                f"Cart with {cart_id or customer_id } not found")

    @staticmethod
    def get_all(customer_id):
        """ Query all Carts"""

        carts = Cart.query.filter(Cart.customer_id == customer_id)
        if not carts:
            return []
        data = []

        for cart in carts:
            data.append({
                "quantity": cart.quantity,
                "id": cart.id,
                "product_id": cart.product_id,
                "unit_price": cart.unit_price,
                "total_cost": cart.total_cost
            })
        return data

    def update(self, cart_id, **args):
        """ Update a Cart"""

        cart = self.get_one(cart_id)
        if not cart:
            raise DataNotFound(f"Order Detail with {cart_id} not found")
        if 'unit_price' in args and args['unit_price'] is not None:
            cart.unit_price = args['unit_price']

        if 'quantity' in args and args['quantity'] is not None:
            cart.quantity = args['quantity']

        if 'total_cost' in args and args['total_cost'] is not None:
            cart.total_cost = args['total_cost']

        return cart.save()

    @staticmethod
    def create(unit_price, quantity, total_cost, product_id, customer_id):
        """ Create a new Cart """

        try:

            if not (type(quantity) is int):
                raise DataNotFound(f"quantity {quantity} must not an integer ")

            if not (product_id or customer_id):
                raise DataNotFound("both product and customer id required")

            if (unit_price or total_cost) < 0:
                raise DataNotFound(
                    "both price and total cost cannot be a negative value"
                )

            if not (unit_price or total_cost):
                raise DataNotFound(
                    "both price and total cost must be provided")

            new_cart = Cart(unit_price=unit_price,
                            quantity=quantity,
                            total_cost=total_cost,
                            customer_id=customer_id,
                            product_id=product_id)
            return new_cart.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception as err:
            print(err)
            raise InternalServerError

    @staticmethod
    def delete(cart_id):
        """ Delete a cart by id """

        if not cart_id:
            raise DataNotFound("Cart not found")

        try:
            query = Cart.query.filter(Cart.id == cart_id).first()
            if not query:
                raise DataNotFound(f"Cart Detail with {cart_id} not found")
            return query.delete()
        except DataNotFound:
            print(sys.exc_info())
            raise DataNotFound(f"Cart with {cart_id} not found")
