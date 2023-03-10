""" Defines the product repository """
import sys
from sqlalchemy import or_, and_
from models import Product, ProductCategory, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class ProductRepository:
    """ The repository for the products model """

    @staticmethod
    def get(product_id):
        """ Query product by id """
        if not product_id:
            raise DataNotFound(f"can't check for empty product id")

        try:
            query = Product.query
            if id:
                query = query.filter(Product.id == product_id)
            product = query.first()
            return product
        except:
            print(sys.exc_info())
            raise DataNotFound(f"product with {product_id} not found")

    @staticmethod
    def getAll():
        """ get all product"""
        products = db.session.query(Product).join(ProductCategory).all()
        all_product = []

        for product in products:
            all_product.append({
                "title": product.title,
                "id": product.id,
                "price": product.price,
                "image": product.image,
                "quantity": product.quantity,
                "short_desc": product.short_desc,
                "rating": product.rating,
                "price": product.price,
                "sellers_id": product.sellers_id,
                "product_category": product.product_categories_id,
                "thumbnail": product.thumbnail,
            })

        return all_product

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

    @staticmethod
    def delete(product_id):
        """ Delete product by product_id """

        if not product_id:
            raise DataNotFound(f"Product not found")
        try:
            query = Product.query.filter(Product.id == product_id).first()
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")
