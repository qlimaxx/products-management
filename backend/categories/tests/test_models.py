import unittest

from mongoengine import connect, disconnect
from mongoengine.errors import ValidationError

from ..models import Category


NAME = 'Category1'


class CategoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('db', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        Category.drop_collection()
        disconnect()

    def test_create(self):
        category = Category(name=NAME)
        category.save()
        category2 = Category.objects().first()
        self.assertEqual(category2.name, NAME)

    def test_create_with_no_name(self):
        category = Category()
        self.assertRaises(ValidationError, category.save)
