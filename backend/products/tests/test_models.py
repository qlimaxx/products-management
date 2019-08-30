import uuid
import unittest

from mongoengine import connect, disconnect
from mongoengine.errors import ValidationError

from ..models import Product


NAME = 'Product1'
PRICE = 100.5
CATEGORIES = [uuid.uuid4()]


class ProductTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('db', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        Product.drop_collection()
        disconnect()

    def test_create(self):
        product = Product(name=NAME, price=PRICE,
                          categories=CATEGORIES)
        product.save()
        product2 = Product.objects().first()
        self.assertEqual(product2.name, NAME)
        self.assertEqual(product2.price, PRICE)
        self.assertEqual(product2.categories, CATEGORIES)

    def test_create_with_no_name(self):
        product = Product(price=PRICE)
        self.assertRaises(ValidationError, product.save)

    def test_create_with_no_price(self):
        product = Product(name=NAME)
        self.assertRaises(ValidationError, product.save)

    def test_create_with_invalid_categories(self):
        product = Product(name=NAME, price=PRICE,
                          categories=['invalid'])
        self.assertRaises(ValidationError, product.save)
