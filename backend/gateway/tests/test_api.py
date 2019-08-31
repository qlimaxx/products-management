import uuid
import unittest
import requests_mock

from .. import api


CATEGORY1 = {'name': 'Category1', 'uuid': str(uuid.uuid4())}
CATEGORY2 = {'name': 'Category2', 'uuid': str(uuid.uuid4())}
PRODUCT1 = {'name': 'Product1', 'price': 100,
            'uuid': str(uuid.uuid4()), 'categories': [CATEGORY1['uuid']]}
PRODUCT2 = {'name': 'Product2', 'price': 100,
            'uuid': str(uuid.uuid4()), 'categories': []}
PRODUCT12 = {'name': 'Product12', 'price': 100,
             'uuid': str(uuid.uuid4()), 'categories': [CATEGORY1['uuid'], CATEGORY2['uuid']]}


class ApiTest(unittest.TestCase):

    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()
        self.headers = {'X-API-Key': api.app.config['API_KEY']}

    @requests_mock.Mocker()
    def test_unauthorized_request(self, m):
        m.get('{}/products'.format(api.URL_PRODUCTS), status_code=403)
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, 403)

    @requests_mock.Mocker()
    def test_request_with_invalid_api_key(self, m):
        m.get('{}/products'.format(api.URL_PRODUCTS), status_code=403)
        resp = self.app.get(
            '/products', headers={'X-API-Key': 'invalid'})
        self.assertEqual(resp.status_code, 403)

    @requests_mock.Mocker()
    def test_get_categories(self, m):
        m.get(api.URL_CATEGORIES, json=[CATEGORY1, CATEGORY2])
        resp = self.app.get('/categories', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 2)

    @requests_mock.Mocker()
    def test_get_categories_with_products(self, m):
        m.get(api.URL_CATEGORIES, json=[CATEGORY1, CATEGORY2])
        m.get(api.URL_PRODUCTS, json=[PRODUCT1, PRODUCT2])
        resp = self.app.get('/categories?products=1', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        for e in resp.json:
            if e['products']:
                self.assertEqual(e['products'][0], PRODUCT1)
        self.assertEqual(len(resp.json), 2)

    @requests_mock.Mocker()
    def test_get_category(self, m):
        m.get('{0}/{1}'.format(api.URL_CATEGORIES,
                               CATEGORY1['uuid']), json=CATEGORY1)
        resp = self.app.get(
            'categories/{}'.format(CATEGORY1['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, CATEGORY1)

    @requests_mock.Mocker()
    def test_get_category_with_products(self, m):
        m.get('{0}/{1}'.format(api.URL_CATEGORIES,
                               CATEGORY1['uuid']), json=CATEGORY1)
        m.get('{0}/?category={1}'.format(api.URL_PRODUCTS,
                                         CATEGORY1['uuid']), json=[PRODUCT1])
        resp = self.app.get(
            'categories/{}?products=1'.format(CATEGORY1['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['uuid'], CATEGORY1['uuid'])
        self.assertEqual(resp.json['products'], [PRODUCT1])

    @requests_mock.Mocker()
    def test_create_category_success(self, m):
        m.post(api.URL_CATEGORIES, json=CATEGORY1)
        resp = self.app.post(
            'categories', headers=self.headers, json=CATEGORY1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, CATEGORY1)

    @requests_mock.Mocker()
    def test_create_category_with_empty_data(self, m):
        m.post(api.URL_CATEGORIES, status_code=400)
        resp = self.app.post('categories', headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_update_category_success(self, m):
        m.put('{0}/{1}'.format(api.URL_CATEGORIES,
                               CATEGORY1['uuid']), json=CATEGORY1)
        resp = self.app.put(
            'categories/{}'.format(CATEGORY1['uuid']), headers=self.headers, json=CATEGORY1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, CATEGORY1)

    @requests_mock.Mocker()
    def test_update_category_with_invalid_uuid(self, m):
        m.put('{}/invalid'.format(api.URL_CATEGORIES), status_code=400)
        resp = self.app.put('categories/invalid',
                            headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_update_category_with_empty_data(self, m):
        m.put('{0}/{1}'.format(api.URL_CATEGORIES,
                               CATEGORY1['uuid']), status_code=400)
        resp = self.app.put(
            'categories/{}'.format(CATEGORY1['uuid']), headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_delete_category_success(self, m):
        m.delete('{0}/{1}'.format(api.URL_CATEGORIES,
                                  CATEGORY1['uuid']), status_code=200)
        m.delete('{0}/?category={1}'.format(api.URL_PRODUCTS,
                                            CATEGORY1['uuid']), status_code=200)
        resp = self.app.delete(
            'categories/{}'.format(CATEGORY1['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)

    @requests_mock.Mocker()
    def test_delete_category_with_invalid_uuid(self, m):
        m.delete('{0}/invalid'.format(api.URL_CATEGORIES), status_code=400)
        resp = self.app.delete('categories/invalid', headers=self.headers)
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_get_products(self, m):
        m.get(api.URL_PRODUCTS, json=[PRODUCT1, PRODUCT2])
        resp = self.app.get('/products', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 2)

    @requests_mock.Mocker()
    def test_get_products_with_categories(self, m):
        m.get(api.URL_CATEGORIES, json=[CATEGORY1, CATEGORY2])
        m.get(api.URL_PRODUCTS, json=[PRODUCT1, PRODUCT2])
        resp = self.app.get('/products?categories=1', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        for e in resp.json:
            if e['categories']:
                self.assertEqual(e['categories'][0], CATEGORY1)
        self.assertEqual(len(resp.json), 2)

    @requests_mock.Mocker()
    def test_get_product(self, m):
        m.get('{0}/{1}'.format(api.URL_PRODUCTS,
                               PRODUCT1['uuid']), json=PRODUCT1)
        resp = self.app.get(
            'products/{}'.format(PRODUCT1['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, PRODUCT1)

    @requests_mock.Mocker()
    def test_get_product_with_categories_has_one_category(self, m):
        m.get('{0}/{1}'.format(api.URL_PRODUCTS,
                               PRODUCT1['uuid']), json=PRODUCT1)
        m.get('{0}/{1}'.format(api.URL_CATEGORIES,
                               CATEGORY1['uuid']), json=CATEGORY1)
        resp = self.app.get(
            'products/{}?categories=1'.format(PRODUCT1['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['uuid'], PRODUCT1['uuid'])
        self.assertEqual(resp.json['categories'], [CATEGORY1])

    @requests_mock.Mocker()
    def test_get_product_with_categories_has_two_categories(self, m):
        m.get('{0}/{1}'.format(api.URL_PRODUCTS,
                               PRODUCT12['uuid']), json=PRODUCT12)
        m.get(api.URL_CATEGORIES, json=[CATEGORY1, CATEGORY2])
        resp = self.app.get(
            'products/{}?categories=1'.format(PRODUCT12['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['uuid'], PRODUCT12['uuid'])
        self.assertEqual(resp.json['categories'], [CATEGORY1, CATEGORY2])

    @requests_mock.Mocker()
    def test_create_product_success(self, m):
        m.post(api.URL_PRODUCTS, json=PRODUCT1)
        resp = self.app.post(
            'products', headers=self.headers, json=PRODUCT1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, PRODUCT1)

    @requests_mock.Mocker()
    def test_create_product_with_empty_data(self, m):
        m.post(api.URL_PRODUCTS, status_code=400)
        resp = self.app.post('products', headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_update_product_success(self, m):
        m.put('{0}/{1}'.format(api.URL_PRODUCTS,
                               PRODUCT1['uuid']), json=PRODUCT1)
        resp = self.app.put(
            'products/{}'.format(PRODUCT1['uuid']), headers=self.headers, json=PRODUCT1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, PRODUCT1)

    @requests_mock.Mocker()
    def test_update_product_with_invalid_uuid(self, m):
        m.put('{}/invalid'.format(api.URL_PRODUCTS), status_code=400)
        resp = self.app.put('products/invalid',
                            headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_update_product_with_empty_data(self, m):
        m.put('{0}/{1}'.format(api.URL_PRODUCTS,
                               PRODUCT1['uuid']), status_code=400)
        resp = self.app.put(
            'products/{}'.format(PRODUCT1['uuid']), headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)

    @requests_mock.Mocker()
    def test_delete_product_success(self, m):
        m.delete('{0}/{1}'.format(api.URL_PRODUCTS,
                                  PRODUCT1['uuid']), status_code=200)
        resp = self.app.delete(
            'products/{}'.format(PRODUCT1['uuid']), headers=self.headers)
        self.assertEqual(resp.status_code, 200)

    @requests_mock.Mocker()
    def test_delete_product_with_invalid_uuid(self, m):
        m.delete('{0}/invalid'.format(api.URL_PRODUCTS),
                 status_code=400, json={})
        resp = self.app.delete('products/invalid', headers=self.headers)
        self.assertEqual(resp.status_code, 400)
