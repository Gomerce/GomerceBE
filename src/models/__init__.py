from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin import Admin
from .coupon import Coupon
from .customer import Customer
<<<<<<< HEAD

from .verification_token import VerificationToken

=======
>>>>>>> 3ceca22a53e5284108de638a3ee4da27ad8a9ee9
from .order_detail import OrderDetail
from .order import Order
from .payment_detail import PaymentDetail
from .payment_method import PaymentMethod
from .product_category import ProductCategory
from .product import Product
from .review import Review
from .seller import Seller
from .shipping_address import ShippingAddress
from .status import Status
from .store import Store
<<<<<<< HEAD
from .verification_token import VerificationToken
=======
from .verification_token import VerificationToken
>>>>>>> 3ceca22a53e5284108de638a3ee4da27ad8a9ee9
