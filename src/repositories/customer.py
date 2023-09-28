""" Defines the Customer repository """

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from models import Customer
from utils.errors import DataNotFound, InternalServerError


class CustomerRepository:
    """ The repository for the customer model """

    @staticmethod
    def get(customer_id=None, username=None, email=None):
        """ Query a customer by customer_id """

        # make sure one of the parameters was passed
        if not customer_id and not username and not email:
            raise DataNotFound("Customer not found, no detail provided")

        try:
            query = Customer.query
            if customer_id:
                query = query.filter(Customer.id == customer_id)
            if username:
                query = query.filter(
                    or_(Customer.username == username,
                        Customer.email == username))
            if email:
                query = query.filter(
                    or_(Customer.email == email, Customer.username == email))

            customer = query.first()
            return customer

        except DataNotFound:
            return (f"Customer with {customer_id} was not found")

    @staticmethod
    def get_all():
        """ Query all customers"""

        customers = Customer.query.all()

        if not customers:
            return []
        data = []
        for cus in customers:
            data.append({
                "id": cus.id,
                "username": cus.username,
                "first_name": cus.first_name,
                "last_name": cus.last_name,
                "email": cus.email,
                "phone": cus.phone,
                "country": cus.country,
                "state": cus.state,
                "city": cus.city,
                "street_name": cus.street_name,
                "zipcode": cus.zipcode,
            })

        return data

    @staticmethod
    def update(customer_id, **args):
        """ Update a customer's age """

        # customer = self.get(customer_id)

        customer = Customer.query.filter_by(id=customer_id).first()

        if customer:

            if 'username' in args and args['username'] is not None:
                customer.username = args['username']

            if 'last_name' in args and args['last_name'] is not None:
                customer.last_name = args['last_name']

            if 'first_name' in args and args['first_name'] is not None:
                customer.first_name = args['first_name']

            if 'email' in args and args['email'] is not None:
                customer.email = args['email']

            if 'phone' in args and args['phone'] is not None:
                customer.phone = args['phone']

            if 'country' in args and args['country'] is not None:
                customer.country = args['country']

            if 'state' in args and args['state'] is not None:
                customer.state = args['state']

            if 'city' in args and args['city'] is not None:
                customer.city = args['city']

            if 'street_name' in args and args['street_name'] is not None:
                customer.street_name = args['street_name']

            if 'zipcode' in args and args['zipcode'] is not None:
                customer.zipcode = args['zipcode']

            return customer.save()

        return customer

    @staticmethod
    def create(username, last_name, first_name, email, password, phone=None,
               country=None, state=None, city=None, street_name=None,
               zipcode=None):
        """ Create a new customer """
        try:
            new_customer = Customer(username=username, first_name=first_name,
                                    last_name=last_name, email=email,
                                    phone=phone, country=country, state=state,
                                    city=city, street_name=street_name,
                                    zipcode=zipcode)
            new_customer.set_password(password)

            return new_customer.save()

        except IntegrityError as error:
            raise ValueError("Duplicated Data") from error

        except InternalServerError as exc:
            raise InternalServerError from exc
