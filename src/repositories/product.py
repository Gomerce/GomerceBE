""" Defines the Product repository """
import sys
from sqlalchemy import or_
from models import db, Product, ProductCategory
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError
from flask import jsonify


class ProductRepository:
    """ The repository for the product model """

    @staticmethod
    def get(product_id=None):
        """ Query a product by product_id """

        # make sure one of the parameters was passed
        if not product_id:
            raise DataNotFound(f"Product not found, no detail provided")

        try:
            query = Product.query
            if product_id:
                query = query.filter(Product.id == product_id)

            product = query.first()
            return product
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")

    @staticmethod
    def getAll():
        """ Query all products"""
        products = db.session.query(Product).join(ProductCategory).all()
        data = []

        for product in products:
            data.append({
                "title": product.title,
                "id": product.id,
                "price": product.price,
                "quantity": product.quantity,
                "short_desc": product.short_desc,
                "rating": product.rating,
                "thumbnail": product.thumbnail,
                "image": product.image, 
                "price": product.price,
                "sellers_id": product.sellers_id,
                "product_category": product.product_categories_id
            })
            
        return data
    
    def update(self, product_id, **args):
        """ Update a product details """
        product = self.get(product_id)
        if 'title' in args and args['title'] is not None:
            product.title = args['title']

        if 'price' in args and args['price'] is not None:
            product.price = args['price']

        if 'quantity' in args and args['quantity'] is not None:
            product.quantity = args['quantity']

        if 'short_desc' in args and args['short_desc'] is not None:
            product.short_desc = args['short_desc']

        if 'thumbnail' in args and args['thumbnail'] is not None:
            product.thumbnail = args['thumbnail']
            
        if 'image' in args and args['image'] is not None:
            product.image = args['image']
            
        if 'rating' in args and args['rating'] is not None:
            product.rating = args['rating']

        return product.save()
    
    @staticmethod
    def create(title, price, quantity, short_desc, thumbnail, image, sellers_id, product_categories_id):
        """ Create a new product """
        try:
            new_product = Product(title=title, price=price, quantity=quantity, short_desc=short_desc,
                                  thumbnail=thumbnail, image=image, sellers_id=sellers_id, product_categories_id=product_categories_id)

            return new_product.save()

        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError
        
    @staticmethod
    def delete(product_id):
        """ Delete a product by product_id """

        # make sure product_id was passed
        if not product_id:
            raise DataNotFound(f"Product not found, no detail provided")

        try:
            query = Product.query.filter(Product.id == product_id)

            product = query.first()
            return product.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")\


   
