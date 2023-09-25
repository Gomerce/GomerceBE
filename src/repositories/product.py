""" Defines the Product repository """


import sys

from sqlalchemy.exc import IntegrityError

from models import Product, ProductCategory, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError


class ProductRepository:
    """ The repository for the product model """

    @staticmethod
    def get(product_id=None):
        """ Query a product by product_id """

        # make sure one of the parameters was passed
        if not product_id:
            raise DataNotFound("Product not found, no detail provided")

        try:
            query = Product.query
            if product_id:
                query = query.filter(Product.id == product_id)

            product = query.first()

            return product

        except DataNotFound:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")
        
    @staticmethod
    def search_filter(title, min=None, max=None, category=None):
        try:
            products = None
            if title and isinstance(title, str):
                search = title.strip() 
                products = Product.query.filter(or_(Product.title.ilike(f'%{search}%'), Product.short_desc.ilike(f'%{search}%'))).all()
                
            if min and isinstance(min, float):
                products = Product.query.filter(Product.price >= float(min)).all()
                
            if max and isinstance(max, float):
                products = Product.query.filter(Product.price <= float(max)).all()
            if max and title:
                query = Product.query.filter(Product.title.ilike(f'%{title}%'))
                products = query.filter(Product.price >= float(max)) # chaining the previous query and thus filtering it
                
            if min and title:
                query = Product.query.filter(Product.title.ilike(f'%{title}%'))
                products = query.filter(Product.price <float(min))
                
            if category:
                products = Product.query.join(ProductCategory).filter(ProductCategory.name.ilike(f'%{category}%')).all()
                
            response = []
            for product in products:
                response.append({
                    'id': product.id,
                    'title': product.title,
                    'price': str(product.price),
                    'quantity': product.quantity,
                    'short_desc': product.short_desc,
                    'long_desc': product.long_desc,
                    'rating': product.rating,
                    'thumbnail': product.thumbnail,
                    'image': product.image,
                    'created_at': product.created_at,
                    'updated_at': product.updated_at
                })

            return response
        except DataNotFound as e:
            raise DataNotFound(f"Search field cannot be empty else check for the correct data type of float and string")


    @staticmethod
    def getAll():
        """ Query all products"""
        products = db.session.query(Product).join(ProductCategory).all()
        data = []

        for product in products:
            data.append({
                "title": product.title,
                "id": product.id,
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
    def create(title, price, quantity, short_desc, thumbnail, image,
               sellers_id, product_categories_id, brand_id,
               long_desc, rating):
        """ Create a new product """

        try:
            new_product = Product(title=title, price=price, quantity=quantity,
                                  short_desc=short_desc,
                                  thumbnail=thumbnail, image=image,
                                  sellers_id=sellers_id,
                                  product_categories_id=product_categories_id,
                                  brand_id=brand_id, long_desc=long_desc,
                                  rating=rating)

            return new_product.save()

        except IntegrityError as e:
            message = e.orig.diag.message_detail
            db.session.rollback()
            raise DuplicateData(message)

        except Exception:
            db.session.rollback()
            raise InternalServerError

    @staticmethod
    def delete(product_id):
        """ Delete a product by product_id """

        # make sure product_id was passed
        if not product_id:
            raise DataNotFound("Product not found, no detail provided")

        try:
            query = Product.query.filter(Product.id == product_id)

            product = query.first()
            return product.delete()

        except DataNotFound:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")
