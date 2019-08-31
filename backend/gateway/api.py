import os
import requests

from functools import wraps
from json.decoder import JSONDecodeError
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.config['API_KEY'] = os.environ.get('API_KEY')
CORS(app)

URL_CATEGORIES = os.environ.get(
    'URL_CATEGORIES', default='http://localhost:5001')
URL_PRODUCTS = os.environ.get(
    'URL_PRODUCTS', default='http://localhost:5002')

HEADERS = {'Content-Type': 'application/json',
           'X-API-Key': app.config['API_KEY']}


def require_auth(func):
    @wraps(func)
    def auth(*args, **kwargs):
        if request.headers.get('X-API-Key') is None:
            return jsonify({'details': 'X-API-Key is missing'}), 403
        elif request.headers.get('X-API-Key') != app.config['API_KEY']:
            return jsonify({'details': 'Invalid X-API-Key'}), 403
        return func(*args, **kwargs)
    return auth


def handle_error(func):
    @wraps(func)
    def error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except JSONDecodeError:
            return '', 400
    return error


@app.route('/categories', methods=['GET'])
@require_auth
def get_categories():
    categories = requests.get(URL_CATEGORIES, headers=HEADERS).json()
    if not request.args.get('products'):
        return jsonify(categories)
    products = requests.get(URL_PRODUCTS, headers=HEADERS).json()
    data = {
        e['uuid']: {**e, 'products': []} for e in categories
    }
    for product in products:
        for category in product['categories']:
            if category in data:
                data[category]['products'].append(product)
    return jsonify(list(data.values()))


@app.route('/categories', methods=['POST'])
@require_auth
@handle_error
def create_category():
    resp = requests.post(
        URL_CATEGORIES, headers=HEADERS, json=request.get_json())
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    return jsonify(resp.json())


@app.route('/categories/<category_id>', methods=['GET'])
@require_auth
def get_category(category_id):
    resp = requests.get(
        '{0}/{1}'.format(URL_CATEGORIES, category_id), headers=HEADERS)
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    category = resp.json()
    if not request.args.get('products'):
        return jsonify(category)
    products = requests.get(URL_PRODUCTS, params={
                            'category': category['uuid']}, headers=HEADERS).json()
    category['products'] = products
    return jsonify(category)


@app.route('/categories/<category_id>', methods=['PUT'])
@require_auth
@handle_error
def update_category(category_id):
    resp = requests.put(
        '{0}/{1}'.format(URL_CATEGORIES, category_id), headers=HEADERS,
        json=request.get_json())
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    return jsonify(resp.json())


@app.route('/categories/<category_id>', methods=['DELETE'])
@require_auth
@handle_error
def delete_category(category_id):
    resp = requests.delete('{0}/{1}'.format(URL_CATEGORIES,
                                            category_id), headers=HEADERS)
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    requests.delete(URL_PRODUCTS, params={
        'category': category_id}, headers=HEADERS)
    return ''


@app.route('/products', methods=['GET'])
@require_auth
def get_products():
    products = requests.get(URL_PRODUCTS, headers=HEADERS).json()
    if not request.args.get('categories'):
        return jsonify(products)
    resp_categories = requests.get(URL_CATEGORIES, headers=HEADERS).json()
    categories_dict = {e['uuid']: e for e in resp_categories}
    for product in products:
        categories = []
        for category in product['categories']:
            if category in categories_dict:
                categories.append(categories_dict[category])
        product['categories'] = categories
    return jsonify(products)


@app.route('/products', methods=['POST'])
@require_auth
@handle_error
def create_product():
    resp = requests.post(URL_PRODUCTS, headers=HEADERS,
                         json=request.get_json())
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    return jsonify(resp.json())


@app.route('/products/<product_id>', methods=['GET'])
@require_auth
def get_product(product_id):
    resp = requests.get(
        '{0}/{1}'.format(URL_PRODUCTS, product_id), headers=HEADERS)
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    product = resp.json()
    if not request.args.get('categories') or not product['categories']:
        return jsonify(product)
    if len(product['categories']) > 1:
        resp_categories = requests.get(URL_CATEGORIES, headers=HEADERS).json()
        categories = []
        for category in resp_categories:
            if category['uuid'] in product['categories']:
                categories.append(category)
        if categories:
            product['categories'] = categories
    else:
        category = requests.get(
            '{0}/{1}'.format(URL_CATEGORIES, product['categories'][0]),
            headers=HEADERS).json()
        product['categories'] = [category]
    return jsonify(product)


@app.route('/products/<product_id>', methods=['PUT'])
@require_auth
@handle_error
def update_product(product_id):
    resp = requests.put(
        '{0}/{1}'.format(URL_PRODUCTS, product_id),
        headers=HEADERS, json=request.get_json())
    if not resp.ok:
        return jsonify(resp.json()), resp.status_code
    return jsonify(resp.json())


@app.route('/products/<product_id>', methods=['DELETE'])
@require_auth
def delete_product(product_id):
    resp = requests.delete('{0}/{1}'.format(URL_PRODUCTS,
                                            product_id), headers=HEADERS)
    if resp.ok:
        return ''
    else:
        return jsonify(resp.json()), resp.status_code
