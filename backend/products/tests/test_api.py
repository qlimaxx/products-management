import uuid
import unittest

from .. import api
from ..models import Product


NAME = 'Product1'
NAME2 = 'Product2'
PRICE = 100.5
PRICE2 = 200.5
CATEGORIES = [uuid.uuid4()]
CATEGORIES2 = [uuid.uuid4()]


class ApiTest(unittest.TestCase):

    def tearDown(self):
        Product.drop_collection()

    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()
        self.headers = {'X-API-Key': api.app.config['API_KEY']}

    def test_unauthorized_request(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 403)

    def test_request_with_invalid_api_key(self):
        resp = self.app.get(
            '/', headers={'X-API-Key': 'invalid'})
        self.assertEqual(resp.status_code, 403)

    def test_get_products(self):
        Product(name=NAME, price=PRICE).save()
        resp = self.app.get('/', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 1)

    def test_get_products_with_category_filter(self):
        product = Product(name=NAME, price=PRICE, categories=CATEGORIES).save()
        Product(name=NAME2, price=PRICE2, categories=CATEGORIES2).save()
        resp = self.app.get(
            '/?category={}'.format(str(CATEGORIES[0])), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 1)
        self.assertEqual(resp.json, [product.to_dict()])

    def test_get_existing_product(self):
        product = Product(name=NAME, price=PRICE).save()
        resp = self.app.get('/{}'.format(product.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, product.to_dict())

    def test_get_product_not_found(self):
        product = Product()
        resp = self.app.get('/{}'.format(product.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 404)

    def test_get_product_with_invalid_uuid(self):
        resp = self.app.get('/invalid', headers=self.headers)
        self.assertEqual(resp.status_code, 400)

    def test_create_product_success(self):
        resp = self.app.post('/', headers=self.headers, json={
            'name': NAME,
            'price': PRICE,
            'categories': CATEGORIES})
        product = Product.objects.first()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, NAME)
        self.assertEqual(product.price, PRICE)
        self.assertEqual(product.categories, CATEGORIES)

    def test_create_product_without_name(self):
        resp = self.app.post('/', headers=self.headers, json={
            'price': PRICE,
            'categories': CATEGORIES})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_without_price(self):
        resp = self.app.post('/', headers=self.headers, json={
            'name': NAME,
            'categories': CATEGORIES})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_without_categories(self):
        resp = self.app.post('/', headers=self.headers, json={
            'name': NAME,
            'price': PRICE})
        product = Product.objects.first()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, NAME)
        self.assertEqual(product.price, PRICE)
        self.assertEqual(product.categories, [])

    def test_update_product_success(self):
        product = Product(name=NAME, price=PRICE,
                          categories=CATEGORIES).save()
        resp = self.app.put('/{}'.format(product.uuid),
                            headers=self.headers, json={
                                'name': NAME2,
                                'price': PRICE2,
                                'categories': CATEGORIES2})
        product2 = Product.objects.get(uuid=product.uuid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(product2.name, NAME2)
        self.assertEqual(product2.price, PRICE2)
        self.assertEqual(product2.categories, CATEGORIES2)

    def test_update_prodduct_without_name_only(self):
        prodduct = Product(name=NAME, price=PRICE,
                           categories=CATEGORIES).save()
        resp = self.app.put('/{}'.format(prodduct.uuid),
                            headers=self.headers, json={
                                'name': NAME2})
        prodduct2 = Product.objects.get(uuid=prodduct.uuid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(prodduct2.name, NAME2)

    def test_update_prodduct_without_categories_only(self):
        prodduct = Product(name=NAME, price=PRICE,
                           categories=CATEGORIES).save()
        resp = self.app.put('/{}'.format(prodduct.uuid),
                            headers=self.headers, json={
                                'categories': CATEGORIES2})
        prodduct2 = Product.objects.get(uuid=prodduct.uuid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(prodduct2.categories, CATEGORIES2)

    def test_update_prodduct_not_found(self):
        prodduct = Product()
        resp = self.app.put(
            '/{}'.format(prodduct.uuid), headers=self.headers, json={'name': NAME})
        self.assertEqual(resp.status_code, 404)

    def test_delete_product_success(self):
        product = Product(name=NAME, price=PRICE).save()
        self.assertEqual(Product.objects.count(), 1)
        resp = self.app.delete(
            '/{}'.format(product.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_not_found(self):
        product = Product()
        resp = self.app.delete(
            '/{}'.format(product.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 404)

    def test_delete_products_with_category_filter(self):
        Product(name=NAME, price=PRICE, categories=CATEGORIES).save()
        Product(name=NAME2, price=PRICE2, categories=CATEGORIES).save()
        self.assertEqual(Product.objects.count(), 2)
        resp = self.app.delete(
            '/?category={}'.format(str(CATEGORIES[0])), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_products_without_category_filter(self):
        resp = self.app.delete('/', headers=self.headers)
        self.assertEqual(resp.status_code, 400)
