""" Defines the product repository """
import sys
from sqlalchemy import or_, and_
from models import Product
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class ProductRepository:
    """ The repository for the products model """

    @staticmethod
    def get(id, title=None, price=None):
        """ Query product by id """
        if not id and not title and not price:
            raise DataNotFound(f"can't check for empty product id")

        try:
            query = Product.query
            if id:
                query = query.filter(Product.id == id)

            if title:
                query = query.filter(
                    or_(Product.title == title, Product.price == title))
            if price:
                query = query.filter(
                    or_(Product.price == price, Product.title == title))
            product = query.first()
            return product
        except:
            print(sys.exc_info())
            raise DataNotFound(f"product with {id} not found")

    @staticmethod
    def getAll():
        """ get all product"""
        products = Product.query.all()
        all_products = [product.json for product in products]
        return all_products

    def update(self, product_id, **args):
        """ Update a product's """
        product = self.get(product_id)
        if 'title' in args and args['title'] is not None:
            product.title = args['title']

        if 'price' in args and args['price'] is not None:
            product.price = args['price']

        if 'quantity' in args and args['quantity'] is not None:
            product.quantity = args['quantity']

        if 'short_desc' in args and args['short_desc'] is not None:
            product.short_desc = args['short_desc']

        if 'long_desc' in args and args['long_desc'] is not None:
            product.long_desc = args['long_desc']

        if 'rating' in args and args['rating'] is not None:
            product.rating = args['rating']

        if 'thumbnail' in args and args['thumbnail'] is not None:
            product.thumbnail = args['thumbnail']

        if 'image' in args and args['image'] is not None:
            product.image = args['image']
        
        if 'sellers_id' in args and args['sellers_id'] is not None:
            product.sellers_id = args['sellers_id']
        
        if 'product_categories_id' in args and args['product_categories_id'] is not None:
            product.product_categories_id = args['product_categories_id']

        return product.save()

    @staticmethod
    def create(title, price, quantity, short_desc, long_desc, rating, thumbnail, image, sellers_id, product_categories_id):
        """ Create a new product """
        try:
            product = Product(title=title,
                              price=price,
                              quantity=quantity,
                              short_desc=short_desc,
                              long_desc=long_desc,
                              rating=rating,
                              thumbnail=thumbnail,
                              image=image,
                              sellers_id=sellers_id,
                              product_categories_id=product_categories_id)
            return product.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError
