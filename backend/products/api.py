import os

from functools import wraps
from flask import Flask, request, jsonify
from mongoengine import connect
from mongoengine.errors import ValidationError, NotUniqueError

from .models import Product


app = Flask(__name__)
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['MONGO_URI'] = os.environ.get(
    'MONGO_URI', default='mongodb://localhost')

connect('db', host=app.config['MONGO_URI'])


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
        except (ValueError, ValidationError, NotUniqueError) as ex:
            return jsonify({'details': str(ex)}), 400
        except Product.DoesNotExist as ex:
            return jsonify({'details': str(ex)}), 404
    return error


@app.route('/', methods=['GET'])
@require_auth
@handle_error
def get_products():
    data = []
    if request.args.get('category'):
        products = Product.objects(
            categories=request.args.get('category'))
    else:
        products = Product.objects.all()
    for product in products:
        data.append(product.to_dict())
    return jsonify(data)


@app.route('/', methods=['POST'])
@require_auth
@handle_error
def create_product():
    data = request.get_json()
    if not data:
        return '', 400
    product = Product(name=data.get('name'),
                      price=data.get('price'),
                      categories=data.get('categories'))
    product.save()
    return jsonify(product.to_dict())


@app.route('/<product_id>', methods=['GET'])
@require_auth
@handle_error
def get_product(product_id):
    product = Product.objects.get(uuid=product_id)
    return jsonify(product.to_dict())


@app.route('/<product_id>', methods=['PUT'])
@require_auth
@handle_error
def update_product(product_id):
    data = request.get_json()
    if not data:
        return '', 400
    product = Product.objects.get(uuid=product_id)
    if 'name' in data:
        product.name = data.get('name')
    if 'price' in data:
        product.price = data.get('price')
    if 'categories' in data:
        product.categories = data.get('categories')
    product.save()
    return jsonify(product.to_dict())


@app.route('/<product_id>', methods=['DELETE'])
@require_auth
@handle_error
def delete_product(product_id):
    Product.objects.get(uuid=product_id).delete()
    return ''


@app.route('/', methods=['DELETE'])
@require_auth
@handle_error
def delete_products():
    if request.args.get('category'):
        Product.objects(
            categories=request.args.get('category')).delete()
        return '', 200
    else:
        return '', 400
