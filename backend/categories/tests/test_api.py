import unittest

from .. import api
from ..models import Category


NAME = 'Category1'
NAME2 = 'Category2'


class ApiTest(unittest.TestCase):

    def tearDown(self):
        Category.drop_collection()

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

    def test_get_categories(self):
        Category(name=NAME).save()
        resp = self.app.get('/', headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 1)

    def test_get_existing_category(self):
        category = Category(name=NAME).save()
        resp = self.app.get('/{}'.format(category.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, category.to_dict())

    def test_get_category_not_found(self):
        category = Category(name=NAME)
        resp = self.app.get('/{}'.format(category.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 404)

    def test_get_category_with_invalid_uuid(self):
        resp = self.app.get('/invalid', headers=self.headers)
        self.assertEqual(resp.status_code, 400)

    def test_create_category_success(self):
        resp = self.app.post('/', headers=self.headers, json={'name': NAME})
        category = Category.objects.first()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, NAME)

    def test_create_category_without_name(self):
        resp = self.app.post('/', headers=self.headers, json={})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Category.objects.count(), 0)

    def test_update_category_success(self):
        category = Category(name=NAME).save()
        resp = self.app.put('/{}'.format(category.uuid),
                            headers=self.headers, json={'name': NAME2})
        category2 = Category.objects.get(uuid=category.uuid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(category2.name, NAME2)

    def test_update_category_without_name(self):
        category = Category(name=NAME).save()
        resp = self.app.put('/{}'.format(category.uuid),
                            headers=self.headers, json={})
        category2 = Category.objects.get(uuid=category.uuid)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(category2.name, NAME)

    def test_update_category_not_found(self):
        category = Category(name=NAME)
        resp = self.app.put(
            '/{}'.format(category.uuid), headers=self.headers, json={'name': NAME})
        self.assertEqual(resp.status_code, 404)

    def test_delete_category_success(self):
        category = Category(name=NAME).save()
        self.assertEqual(Category.objects.count(), 1)
        resp = self.app.delete(
            '/{}'.format(category.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Category.objects.count(), 0)

    def test_delete_category_not_found(self):
        category = Category(name=NAME)
        resp = self.app.delete(
            '/{}'.format(category.uuid), headers=self.headers)
        self.assertEqual(resp.status_code, 404)
